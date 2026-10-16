#!/usr/bin/env python3
"""One chi128 warm-continuation step; unchanged half-row optimizer.
Only checkpoint serialization is compacted: four real physical/canonical MPS
arrays are preserved, while FL/FR caches are recomputed on a restart.
"""
from pathlib import Path
import hashlib, json, os, signal, sys, time
import numpy as np
import replica_halfrow as H
import replica_vumps as V

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent


def save_json(path, data):
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(data, indent=2) + '\n')
    os.replace(tmp, path)


def install_compact_checkpointer(progress=None):
    original = H.checkpoint
    def compact(path, state, metadata):
        physical = dict(state, FL=None, FR=None)
        meta = dict(metadata, environment_cache_omitted=True,
                    checkpoint_contents='AL, AR, AC, C; recompute FL/FR on restart')
        original(path, physical, meta)
        if progress is not None:
            progress(state, meta)
    H.checkpoint = compact
    return original


def color_diagnostics(state, p):
    _, G, gh, gmh = H.build_half(3, 2, p)
    amplitudes = []
    for i in range(G['N']):
        op = np.zeros((G['N'], G['N'])); op[i, i] = 1
        amplitudes.append(V.local_expect(state['AC'], gh @ op @ gmh))
    q = np.asarray(amplitudes)
    return dict(color_one_point_amplitudes=q.tolist(),
                color_sum=float(q.sum()),
                color_l2_order=float(np.linalg.norm(q-1/6)*np.sqrt(6/5)),
                color_qualification='symmetry-invariant one-point order diagnostic; not a phase certificate or a probability-positivity assertion')


def smoke():
    cache = ROOT / '.arena/branch128-smoke'; cache.mkdir(parents=True, exist_ok=True)
    os.environ['STAGE_SECONDS'] = '0'; os.environ['CORR_RMAX'] = '20'
    initial = None
    a, oa = H.solve(3, 2, .3045, 4, init=initial, tol=1e-12, maxiter=3,
                    checkpoint_path=cache/'full.npz', verbose=False)
    original = install_compact_checkpointer()
    try:
        b, ob = H.solve(3, 2, .3045, 4, init=initial, tol=1e-12, maxiter=3,
                        checkpoint_path=cache/'physical.npz', verbose=False)
    finally:
        H.checkpoint = original
    assert max(np.max(abs(a[k]-b[k])) for k in ['AL','AR','AC','C']) < 1e-12
    st, meta = H.load_state(cache/'physical.npz', operator='hermitian-halfrow')
    assert st['FL'] is None and st['FR'] is None
    assert all(np.array_equal(st[k], b[k]) for k in ['AL','AR','AC','C'])
    print('2/2 compact-serialization smoke checks passed; identical physical optimizer result, exact four-array roundtrip; not added to 246')


def main():
    point_path = Path(sys.argv[1]).resolve(); side = sys.argv[2]
    assert side in ['ordered','disordered']
    point = json.loads(point_path.read_text())
    master_path = ROOT / point['master_protocol']
    master = json.loads(master_path.read_text())
    assert hashlib.sha256(master_path.read_bytes()).hexdigest() == point['master_sha256']
    for name, digest in master['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    source_spec = master['preparations'][side]
    source = ROOT / source_spec['checkpoint']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_spec['sha256']
    initial, source_meta = H.load_state(source, operator='hermitian-halfrow')
    assert source_meta['n']==3 and source_meta['d']==2 and source_meta['chi']==128
    p, tol = point['p'], master['tol']
    assert tol==1e-7 and master['chi']==128
    stem=f'branch128_pilot_{side}_p{p:.7f}'
    out=R/(stem+'.json'); checkpoint=R/'checkpoints'/(stem+'.npz')
    if out.exists():
        raise SystemExit('Refusing accidental repeat of an existing scan case')
    started=time.monotonic(); remaining=point['deadline_unix']-time.time()
    if remaining<150:raise SystemExit('Insufficient allocated time remains')
    os.environ['STAGE_SECONDS']=str(min(master['optimizer_seconds'], remaining-120))
    os.environ['CORR_RMAX']=str(master['correlation_rmax'])
    result=dict(campaign=master['campaign'],preparation=side,n=3,d=2,p=p,chi=128,tol=tol,
                status='running',converged=False,source=source_spec,source_metadata=source_meta,
                source_is_accepted_observation=bool(source_spec.get('accepted_source',False)),master_sha256=point['master_sha256'],
                point_protocol=str(point_path.relative_to(ROOT)),
                checkpoint=str(checkpoint.relative_to(R)),
                preparation_mode='unbiased warm continuation from the previous accepted state; initialization history is not a certified phase',
                qualification='criterion-passed finite-chi optimizer states are not thermodynamic phases')
    def progress(st, meta):
        result.update(eps=float(st['eps']),iters=int(st['iters']),optimizer_seconds=float(st['seconds']),
                      intermediate_eta_half=float(st['eta']))
        save_json(out,result)
    original=install_compact_checkpointer(progress)
    def limit(signum,frame):raise TimeoutError('allocated point wall-clock deadline reached')
    signal.signal(signal.SIGALRM,limit);signal.signal(signal.SIGTERM,limit)
    signal.setitimer(signal.ITIMER_REAL,remaining)
    save_json(out,result);print('BRANCH_CASE_START',side,p,flush=True)
    try:
        state,obs=H.solve(3,2,p,128,init=initial,tol=tol,maxiter=master['maxiter'],
                         checkpoint_path=checkpoint,tag='branch128-pilot-'+side,verbose=True)
        result.update(obs)
        AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
        left=float(np.linalg.norm(AC.reshape(768,128)-AL.reshape(768,128)@C))
        right=float(np.linalg.norm(AC.reshape(128,768)-C@AR.reshape(128,768)))
        lc=float(np.linalg.norm(AL.reshape(768,128).T@AL.reshape(768,128)-np.eye(128)))
        rc=float(np.linalg.norm(AR.reshape(128,768)@AR.reshape(128,768).T-np.eye(128)))
        result.update(gauge_left_residual=left,gauge_right_residual=right,
                      left_canonical_residual=lc,right_canonical_residual=rc,
                      optimizer_tolerance_passed=bool(obs['eps']<tol))
        if not (obs['eps']<tol and max(left,right)<tol and max(lc,rc)<master['canonical_ceiling']):
            result.update(status='iteration-cap-or-stationarity-check-failed',converged=False)
        else:
            result.update(status='stationarity-passed-period-contraction-pending')
            save_json(out,result)
            W,_,_,_=V.build_mpo(3,2,p)
            lam,F=V.dominant(lambda x:V.apply_TL(x,AL,W),(128,W.shape[0],128),tol=1e-10)
            residual=float(np.linalg.norm(V.apply_TL(F,AL,W)-lam*F)/abs(lam))
            if lam<=0 or not np.isfinite(residual):raise RuntimeError('Invalid period contraction')
            result.update(f_full_rayleigh=float(-np.log(lam)),period_contraction_relative_residual=residual)
            accepted=residual<master['period_contraction_ceiling']
            result.update(converged=bool(accepted),status='accepted-finite-chi' if accepted else 'period-contraction-check-failed')
            result.update(color_diagnostics(state,p))
    except (RuntimeError,TimeoutError) as exc:
        result.update(status='budget-stopped' if isinstance(exc,TimeoutError) or 'budget' in str(exc).lower()
                      else 'optimizer-or-validation-failed',reason=str(exc),converged=False)
        if checkpoint.exists():
            _,meta=H.load_state(checkpoint,operator='hermitian-halfrow')
            result['last_state_metadata']=meta
            result.update(eps=meta.get('eps'),iters=meta.get('iters'))
    except Exception as exc:
        result.update(status='unexpected-error',converged=False,reason=f'{type(exc).__name__}: {exc}')
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);H.checkpoint=original
        result['total_stage_seconds']=time.monotonic()-started
        if checkpoint.exists():result['checkpoint_sha256']=hashlib.sha256(checkpoint.read_bytes()).hexdigest()
        save_json(out,result)
        print('BRANCH_CASE_RESULT',json.dumps({k:result.get(k) for k in ['preparation','p','status','eps','iters','total_stage_seconds','m_species','color_l2_order','f_full_rayleigh']}),flush=True)


if __name__=='__main__':
    smoke() if len(sys.argv)>1 and sys.argv[1]=='--smoke' else main()

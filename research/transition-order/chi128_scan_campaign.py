#!/usr/bin/env python3
"""Authorized fixed-source six-rate chi128 campaign, at most two CPU workers.
Parent owns both subprocesses and waits for them; no detached shell jobs, no
automatic chi192, no scalar-cache substitution for actual MPS states.
"""
from pathlib import Path
import hashlib,json,os,signal,subprocess,sys,threading,time,math,fcntl
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(R))
import scan128_worker as worker
import compare_stationary as compare
import replica_halfrow as H
from replica_tm import make_group


def save(path,data):
    tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');os.replace(tmp,path)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def command(args,**kwargs):return subprocess.run(args,check=True,cwd=ROOT,**kwargs)

def verify_accepted(r):
    if not r.get('converged'):return
    assert r['eps']<1e-7 and max(r['gauge_left_residual'],r['gauge_right_residual'])<1e-7
    assert max(r['left_canonical_residual'],r['right_canonical_residual'])<1e-9
    assert r['period_contraction_relative_residual']<1e-8
    assert digest(R/r['checkpoint'])==r['checkpoint_sha256']
    state,meta=H.load_state(R/r['checkpoint'],operator='hermitian-halfrow')
    assert meta['p']==r['p'] and meta['chi']==128 and meta['n']==3 and meta['d']==2
    assert state['AL'].shape==(128,6,128)


def fidelity(a,b,deadline):
    if not (a.get('converged') and b.get('converged')):
        return dict(status='not applicable: fewer than two accepted preparations',orientations=[])
    available=min(90,deadline-time.time()-2)
    if available<5:return dict(status='deferred at point wall-clock limit',orientations=[])
    A=H.load_state(R/a['checkpoint'],operator='hermitian-halfrow')[0]['AL']
    B=H.load_state(R/b['checkpoint'],operator='hermitian-halfrow')[0]['AL']
    out=dict(kind='symmetry-aligned finite-chi similarity; not a phase classifier',status='partial',orientations=[])
    def alarm(signum,frame):raise TimeoutError('comparison time gate')
    previous=signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,available)
    try:
        na,nb=compare.radius(A,A),compare.radius(B,B);denom=math.sqrt(na['radius']*nb['radius'])
        out.update(normalization_A=na,normalization_B=nb);G=make_group(3)
        for left in range(6):
            for right in range(6):
                v=compare.radius(A,compare.transform(B,G,left,right))
                v.update(left=left,right=right,normalized_fidelity_per_site=v['radius']/denom)
                out['orientations'].append(v)
        out['status']='all 36 symmetry orientations evaluated'
    except TimeoutError:
        out['status']='budget-stopped partial orientation search'
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous)
    if out['orientations']:out['largest_evaluated_fidelity_per_site']=max(x['normalized_fidelity_per_site'] for x in out['orientations'])
    return out


def publish(db):
    command([sys.executable,str(HERE/'scan128_report.py')])
    v34=ROOT/'papers/v34/revise_manuscript.py'
    if v34.exists():command([sys.executable,str(v34)])
    command([sys.executable,str(HERE/'bundle_review.py')])
    command([sys.executable,str(HERE/'prepare_publication.py')])
    C=ROOT/'.arena/publish'
    env=os.environ.copy();env.update(GIT_ASKPASS=str(ROOT/'.private/github-askpass.py'),GIT_TERMINAL_PROMPT='0')
    for k in ['GIT_TRACE','GIT_TRACE_PACKET','GIT_TRACE_CURL','GIT_CURL_VERBOSE']:env.pop(k,None)
    def git(*args,capture=False):
        return subprocess.check_output(['git','-c','credential.helper=','-C',str(C),*args],env=env,text=True) if capture else subprocess.run(['git','-c','credential.helper=','-C',str(C),*args],env=env,check=True)
    git('fetch','--quiet','origin','main')
    head=git('rev-parse','HEAD',capture=True).strip();remote=git('rev-parse','origin/main',capture=True).strip()
    if head!=remote:
        check=subprocess.run(['git','-C',str(C),'merge-base','--is-ancestor',remote,head])
        if check.returncode!=0:raise RuntimeError('Remote changed; refuse automatic overwrite/rebase/force-push')
        git('push','origin','main')
        assert git('ls-remote','origin','refs/heads/main',capture=True).split()[0]==head
    assert not git('diff','--','LICENSE',capture=True)
    git('add','--all')
    if not git('diff','--cached','--name-only',capture=True).strip():return
    git('-c','user.name=Arena Research Assistant','-c','user.email=assistant@arena.invalid','-c','commit.gpgsign=false','commit','-m',f"Record chi128 rate-scan progress: {db['status']}")
    git('push','origin','main')
    local=git('rev-parse','HEAD',capture=True).strip();remote=git('ls-remote','origin','refs/heads/main',capture=True).split()[0]
    assert local==remote
    receipt=dict(commit=local,remote_equals_local=True,status=db['status'],ordinary_push=True,case_count=len(db['cases']))
    # Operational receipt outside its own commit avoids a self-referential hash.
    (ROOT/'handoff').mkdir(exist_ok=True)
    save(ROOT/'handoff/scan-publication-receipt.json',receipt)
    print('SCAN_PUSH_VERIFIED',json.dumps(receipt),flush=True)


def main():
    (ROOT/'.arena').mkdir(exist_ok=True)
    lock=(ROOT/'.arena/scan128.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    protocol_path=HERE/'chi128-scan-protocol.json';protocol=json.loads(protocol_path.read_text())
    for name,value in protocol['source_sha256'].items():assert digest(ROOT/name)==value,name
    data_path=R/'n3_chi128_scan.json'
    if data_path.exists():raise SystemExit('Existing campaign record; inspect processes/outcomes before a restart')
    db=dict(campaign=protocol['campaign'],status='running',cases={},phase_order='unresolved',protocol_sha256=digest(protocol_path),new_optimizations_requested=10,reference_reused=True)
    reference={}
    for side in ['ordered','disordered']:
        source=json.loads((R/f'n3_chi128_bounded_{side}.json').read_text())
        verify_accepted(source)
        assert source['warm_source_is_accepted_observation'] is False
        assert source['warm_source']['sha256']==protocol['preparations'][side]['sha256']
        state,_=H.load_state(R/source['checkpoint'],operator='hermitian-halfrow')
        source.update(worker.color_diagnostics(state,.30486))
        reference[side]=source
    reference['reused_verified_reference']=True
    reference['comparison']=json.loads((R/'n3_chi128_stationary_comparison.json').read_text())
    db['cases']['0.3048600']=reference;save(data_path,db)
    try:publish(db)
    except Exception as exc:
        db['publication_error']=f'{type(exc).__name__}: {exc}';save(data_path,db);print('PUBLICATION_PENDING',db['publication_error'],flush=True)
    for p in protocol['priority_new_rates']:
        if time.time()>protocol['campaign_deadline_unix']-180:
            db['status']='remaining rates deferred at authorized campaign wall limit';break
        point=dict(p=p,master_protocol=str(protocol_path.relative_to(ROOT)),master_sha256=digest(protocol_path),deadline_unix=min(time.time()+5400,protocol['campaign_deadline_unix']))
        point_path=HERE/'scan128'/f'point-{p:.7f}.json';point_path.parent.mkdir(exist_ok=True)
        if point_path.exists():raise RuntimeError('Refusing overwrite of a dated point protocol')
        save(point_path,point);print('PAIR_START',p,'deadline',point['deadline_unix'],flush=True)
        children=[];threads=[]
        def relay(pipe,path,side):
            with path.open('w') as f:
                for line in pipe:
                    f.write(line);f.flush();print(f'[{p:.7f} {side}] '+line.rstrip(),flush=True)
        env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
        for side in ['ordered','disordered']:
            seconds=max(1,math.ceil(point['deadline_unix']-time.time()))
            args=['timeout','--signal=TERM','--kill-after=5s',str(seconds)+'s',sys.executable,'-u',str(R/'scan128_worker.py'),str(point_path),side]
            child=subprocess.Popen(args,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
            t=threading.Thread(target=relay,args=(child.stdout,R/f'scan128_{side}_p{p:.7f}.log',side),daemon=True);t.start();threads.append(t);children.append((side,child))
        case={}
        for side,child in children:
            code=child.wait();out=R/f'scan128_{side}_p{p:.7f}.json'
            value=json.loads(out.read_text()) if out.exists() else dict(p=p,chi=128,preparation=side,converged=False,status='worker-exited-without-record')
            if value.get('status') in ['running','stationarity-passed-period-contraction-pending']:
                value.update(status='worker-terminated-before-final-record',converged=False)
            value['process_exit_code']=code;verify_accepted(value);case[side]=value;save(out,value)
        for t in threads:t.join()
        case['comparison']=fidelity(case['ordered'],case['disordered'],point['deadline_unix'])
        case['reused_verified_reference']=False
        db['cases'][f'{p:.7f}']=case
        save(R/f'scan128_comparison_p{p:.7f}.json',case['comparison']);save(data_path,db)
        print('PAIR_DONE',p,json.dumps({s:case[s]['status'] for s in ['ordered','disordered']}),flush=True)
        try:publish(db)
        except Exception as exc:
            db['publication_error']=f'{type(exc).__name__}: {exc}';save(data_path,db);print('PUBLICATION_PENDING',db['publication_error'],flush=True)
    else:
        good=sum(r.get(s,{}).get('converged') is True for r in db['cases'].values() for s in ['ordered','disordered'])
        db['status']='complete: all 12 preparation results accepted' if good==12 else 'grid attempted: some preparations not accepted'
    db['completed_at_unix']=time.time();save(data_path,db)
    try:publish(db)
    except Exception as exc:
        db['publication_error']=f'{type(exc).__name__}: {exc}';save(data_path,db);print('PUBLICATION_PENDING',db['publication_error'],flush=True)
    print('SCAN_DONE',json.dumps(dict(status=db['status'],rates=len(db['cases']),phase_order='unresolved')),flush=True)


if __name__=='__main__':main()

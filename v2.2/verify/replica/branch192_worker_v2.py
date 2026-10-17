#!/usr/bin/env python3
"""Bounded chi192 same-p continuation or disposable warm-start resource benchmark.
The benchmark performs one exact-objective VUMPS iteration but writes no MPS
checkpoint; it is not an optimizer observation. The production path uses actual
accepted chi128 .30480 states, unchanged external gates, and compact real-state
checkpoints. Stop status is not phase/order evidence.
"""
from pathlib import Path
import hashlib,json,os,sys,time,signal,resource,traceback
import numpy as np
import replica_halfrow as H
import replica_vumps as V

ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
PROTOCOL=ROOT/'research/transition-order/branch192-protocol.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(path,obj):
 p=Path(path);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,p)
def alarm(signum,frame):raise TimeoutError('Authorized chi192 stage/deadline reached')
def load_inputs(side,protocol):
 spec=protocol['sources'][side];path=ROOT/spec['checkpoint'];assert sha(path)==spec['sha256']
 state,meta=H.load_state(path,operator='hermitian-halfrow')
 assert meta['n']==3 and meta['d']==2 and meta['chi']==128 and meta['p']==.3048
 return state,meta,spec

def disposable_benchmark(side):
 protocol=json.loads(PROTOCOL.read_text());state,meta,spec=load_inputs(side,protocol)
 t0=time.monotonic();W,G,gh,gmh=H.build_half(3,2,.3048)
 N=G['N']
 def mirror(F):
  B=.5*(F[:,:N,:]+F[:,N:,:].transpose(2,1,0))
  return np.concatenate([B,B.transpose(2,1,0)],axis=1)
 out=V.vumps(W,192,init=state,tol=protocol['internal_goal'],maxiter=1,verbose=True,env_project=mirror,paired_env_dim=N)
 elapsed=time.monotonic()-t0
 # This single exploratory iterate is discarded. No NPZ is written or considered an observation.
 row=dict(kind='disposable one-iteration resource/finite-output benchmark; not an accepted state',
          preparation=side,p=.3048,source_checkpoint=spec['checkpoint'],source_sha256=spec['sha256'],
          initial_chi=meta['chi'],trial_chi=out['chi'],iterations=out['iters'],seconds=elapsed,
          seconds_per_iteration=elapsed/out['iters'],eps_after_single_iteration=out['eps'],
          finite_output=all(np.isfinite(out[k]).all() for k in ['AL','AR','AC','C']),
          peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          no_state_checkpoint_written=True,not_a_convergence_observation=True)
 atomic(R/f'branch192_benchmark_{side}.json',row)
 print('CHI192_BENCHMARK',json.dumps(row),flush=True)

def production(side):
 protocol=json.loads(PROTOCOL.read_text())
 for name,digest in protocol['source_sha256'].items():assert sha(ROOT/name)==digest,name
 initial,source_meta,spec=load_inputs(side,protocol);p=protocol['p'];chi=192
 outpath=R/f'n3_branch192_retry1_{side}.json';cp=R/'checkpoints'/f'branch192_retry1_{side}_p{p:.7f}.npz'
 if outpath.exists() or cp.exists():raise SystemExit('Named chi192 output already exists; inspect before any continuation')
 remaining=protocol['deadline_unix']-time.time()
 if remaining<protocol['validation_reserve_seconds']+60:raise SystemExit('Insufficient authorized time remains')
 optimizer_budget=min(protocol['optimizer_budget_seconds'],remaining-protocol['validation_reserve_seconds'])
 os.environ['STAGE_SECONDS']=str(optimizer_budget);os.environ['CORR_RMAX']=str(protocol['correlation_rmax'])
 result=dict(campaign=protocol['campaign'],history=side,n=3,d=2,p=p,chi=chi,
             external_tol=protocol['external_tol'],optimizer_internal_goal=protocol['internal_goal'],
             status='running',converged=False,source=spec,source_metadata=source_meta,
             source_is_accepted_observation=True,checkpoint=str(cp.relative_to(R)),
             qualification='finite-chi warm continuation, not a global minimum, thermodynamic phase or coexistence certificate')
 saver=H.checkpoint
 def compact(path,st,meta):
  physical=dict(st,FL=None,FR=None)
  info=dict(meta,environment_cache_omitted=True,checkpoint_contents='AL,AR,AC,C; recompute FL/FR on restart',
            acceptance_tol=protocol['external_tol'],optimizer_internal_goal=protocol['internal_goal'],campaign=protocol['campaign'])
  saver(path,physical,info)
  result.update(eps=float(st['eps']),iters=int(st['iters']),optimizer_seconds=float(st['seconds']))
  atomic(outpath,result)

# Temporarily wrap the checked atomic saver. The stored physical tensors/gauges are exact;
# the paired environments are only caches and VUMPS recomputes them after a restart.
 original=H.checkpoint
 H.checkpoint=compact
 started=time.monotonic();alarm_seconds=max(1,int(remaining));signal.signal(signal.SIGALRM,alarm);signal.signal(signal.SIGTERM,alarm)
 signal.setitimer(signal.ITIMER_REAL,alarm_seconds);atomic(outpath,result)
 try:
  state=None;obs=None;error=None
  try:
   state,obs=H.solve(3,2,p,chi,init=initial,tol=protocol['internal_goal'],maxiter=protocol['maxiter'],checkpoint_path=cp,tag='chi192-'+side,verbose=True)
  except RuntimeError as exc:
   if 'budget' not in str(exc).lower():raise
   error=str(exc)
   if cp.exists():state,meta=H.load_state(cp,operator='hermitian-halfrow')
   else:raise
  if state is not None:
   AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
   left=float(np.linalg.norm(AC.reshape(1152,192)-AL.reshape(1152,192)@C))
   right=float(np.linalg.norm(AC.reshape(192,1152)-C@AR.reshape(192,1152)))
   lc=float(np.linalg.norm(AL.reshape(1152,192).T@AL.reshape(1152,192)-np.eye(192)))
   rc=float(np.linalg.norm(AR.reshape(192,1152)@AR.reshape(192,1152).T-np.eye(192)))
   result.update(eps=float(state['eps']),iters=int(state['iters']),optimizer_seconds=float(state['seconds']),
                 gauge_left_residual=left,gauge_right_residual=right,left_canonical_residual=lc,right_canonical_residual=rc,
                 internal_goal_met=bool(state['eps']<protocol['internal_goal']))
   if error:result['optimizer_budget_reason']=error
   if not (state['eps']<protocol['external_tol'] and max(left,right)<protocol['external_tol']
           and max(lc,rc)<protocol['canonical_ceiling']):
    result.update(status='unconverged or original external geometry gates failed',converged=False)
   else:
    if obs is None:
     _,G,gh,gmh=H.build_half(3,2,p);obs=V.observables(state,G,gh,gmh,rmax=protocol['correlation_rmax'])
    result.update(obs);result['f_half']=float(-2*np.log(state['eta']));result['eta_half']=float(state['eta']);result['f']=result['f_half']
    W,_,_,_=V.build_mpo(3,2,p)
    lam,F=V.dominant(lambda x:V.apply_TL(x,AL,W),(chi,W.shape[0],chi),tol=1e-10)
    defect=float(np.linalg.norm(V.apply_TL(F,AL,W)-lam*F)/abs(lam))
    if lam<=0 or not np.isfinite(defect):raise RuntimeError('Invalid full-period expectation contraction')
    import branch128_pilot_worker as diagnostics
    result.update(f_full_rayleigh=float(-np.log(lam)),period_contraction_relative_residual=defect)
    result.update(diagnostics.color_diagnostics(state,p))
    result.update(converged=bool(defect<protocol['period_contraction_ceiling']),
                  status='accepted finite-chi numerical state' if defect<protocol['period_contraction_ceiling'] else 'period contraction gate failed')
  result['process_peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 except TimeoutError as exc:
  result.update(status='authorized deadline reached',converged=False,reason=str(exc))
  if cp.exists():
   try:
    state,meta=H.load_state(cp,operator='hermitian-halfrow');result.update(last_state_metadata=meta,eps=meta.get('eps'),iters=meta.get('iters'),optimizer_seconds=meta.get('seconds'))
   except Exception:pass
 except Exception as exc:
  result.update(status='unexpected error',converged=False,reason=f'{type(exc).__name__}: {exc}');traceback.print_exc()
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);H.checkpoint=original;result['total_stage_seconds']=time.monotonic()-started
  if cp.exists():result['checkpoint_sha256']=sha(cp)
  atomic(outpath,result);print('CHI192_RESULT',json.dumps({k:result.get(k) for k in ['history','status','converged','eps','gauge_right_residual','iters','total_stage_seconds','f_half','f_full_rayleigh','m_species','color_l2_order']}),flush=True)

if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='--benchmark':disposable_benchmark(sys.argv[2])
 else:production(sys.argv[1])

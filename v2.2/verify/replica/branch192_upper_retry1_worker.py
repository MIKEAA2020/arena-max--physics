#!/usr/bin/env python3
"""One ordered-history chi192 continuation to p=.30485 after a disposable gate."""
from pathlib import Path
import hashlib,json,os,sys,time,signal,resource,traceback
import numpy as np
import replica_halfrow as H
import replica_vumps as V
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
PROTOCOL=ROOT/'research/transition-order/branch192-upper-retry1-protocol.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,obj):
 p=Path(p);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,p)
def mirror_fn(N):
 def mirror(F):
  B=.5*(F[:,:N,:]+F[:,N:,:].transpose(2,1,0))
  return np.concatenate([B,B.transpose(2,1,0)],axis=1)
 return mirror
def source(protocol):
 spec=protocol['source'];cp=ROOT/spec['checkpoint'];assert sha(cp)==spec['sha256'];st,meta=H.load_state(cp,operator='hermitian-halfrow')
 assert meta['n']==3 and meta['d']==2 and meta['chi']==192 and meta['p']==.3048 and st['AL'].shape==(192,6,192)
 return st,meta,spec
def benchmark():
 p=json.loads(PROTOCOL.read_text());init,meta,spec=source(p);start=time.monotonic();W,G,gh,gmh=H.build_half(3,2,p['p']);N=G['N']
 out=V.vumps(W,192,init=init,tol=p['internal_goal'],maxiter=1,verbose=True,env_project=mirror_fn(N),paired_env_dim=N)
 row=dict(kind='disposable one-step χ192 p=.30485 warm-enlargement/runtime benchmark; no scientific result',
  preparation='ordered',p=p['p'],chi=192,initial_chi=192,source_checkpoint=spec['checkpoint'],source_sha256=spec['sha256'],
  iterations=out['iters'],vumps_seconds=out['seconds'],seconds_per_iteration=out['seconds']/out['iters'],
  wall_seconds=time.monotonic()-start,eps_after_one_step=out['eps'],finite_output=all(np.isfinite(out[k]).all() for k in ['AL','AR','AC','C']),
  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,no_state_checkpoint_written=True,not_a_convergence_observation=True)
 atomic(R/'branch192_upper_retry1_benchmark.json',row);print('CHI192_UPPER_BENCHMARK',json.dumps(row),flush=True)
def production():
 p=json.loads(PROTOCOL.read_text());
 for rel,h in p['source_sha256'].items():assert sha(ROOT/rel)==h,rel
 init,srcmeta,spec=source(p);rate=p['p'];chi=192;outpath=R/'n3_branch192_upper_retry1_ordered.json';cp=R/'checkpoints/branch192_upper_retry1_ordered_p0.3048500.npz'
 if outpath.exists() or cp.exists():raise SystemExit('Named p=.30485 production output already exists')
 remaining=p['deadline_unix']-time.time()
 setup_reserve=p['setup_reserve_seconds']
 if remaining<p['validation_reserve_seconds']+setup_reserve+60:raise SystemExit('Insufficient time for the pre-reserved validation window')
 stage=min(p['optimizer_budget_seconds'],remaining-p['validation_reserve_seconds']-setup_reserve)
 os.environ['STAGE_SECONDS']=str(stage);os.environ['CORR_RMAX']=str(p['correlation_rmax'])
 result=dict(campaign=p['campaign'],history='ordered',p=rate,n=3,d=2,chi=chi,external_tol=p['external_tol'],internal_goal=p['internal_goal'],
  status='running',converged=False,source=spec,source_metadata=srcmeta,source_is_accepted_observation=True,
  checkpoint=str(cp.relative_to(R)),qualification='single finite-chi ordered-history continuation; not a global minimum, phase boundary or spinodal certificate')
 saver=H.checkpoint
 def compact(path,st,meta):
  physical=dict(st,FL=None,FR=None);info=dict(meta,environment_cache_omitted=True,checkpoint_contents='AL,AR,AC,C; recompute FL/FR on restart',
    acceptance_tol=p['external_tol'],optimizer_internal_goal=p['internal_goal'],campaign=p['campaign'])
  saver(path,physical,info);result.update(eps=float(st['eps']),iters=int(st['iters']),optimizer_seconds=float(st['seconds']));atomic(outpath,result)
 original=H.checkpoint;H.checkpoint=compact
 started=time.monotonic();signal.signal(signal.SIGALRM,lambda s,f:(_ for _ in ()).throw(TimeoutError('fresh six-hour deadline reached')));signal.signal(signal.SIGTERM,lambda s,f:(_ for _ in ()).throw(TimeoutError('campaign manager stop at deadline')))
 signal.setitimer(signal.ITIMER_REAL,max(1,int(remaining)));atomic(outpath,result)
 try:
  try:state,obs=H.solve(3,2,rate,chi,init=init,tol=p['internal_goal'],maxiter=p['maxiter'],checkpoint_path=cp,tag='chi192-upper-ordered',verbose=True)
  except RuntimeError as e:
   if 'budget' not in str(e).lower():raise
   result['optimizer_budget_reason']=str(e)
   if not cp.exists():raise
   state,meta=H.load_state(cp,operator='hermitian-halfrow');obs=None
  AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
  left=float(np.linalg.norm(AC.reshape(1152,192)-AL.reshape(1152,192)@C));right=float(np.linalg.norm(AC.reshape(192,1152)-C@AR.reshape(192,1152)))
  lc=float(np.linalg.norm(AL.reshape(1152,192).T@AL.reshape(1152,192)-np.eye(192)));rc=float(np.linalg.norm(AR.reshape(192,1152)@AR.reshape(192,1152).T-np.eye(192)))
  result.update(eps=float(state['eps']),iters=int(state['iters']),optimizer_seconds=float(state['seconds']),gauge_left_residual=left,gauge_right_residual=right,
   left_canonical_residual=lc,right_canonical_residual=rc,internal_goal_met=bool(state['eps']<p['internal_goal']))
  if not (state['eps']<p['external_tol'] and max(left,right)<p['external_tol'] and max(lc,rc)<p['canonical_ceiling']):
   result.update(status='optimizer/gauge gates not passed',converged=False)
  else:
   if obs is None:
    _,G,gh,gmh=H.build_half(3,2,rate);obs=V.observables(state,G,gh,gmh,rmax=p['correlation_rmax'])
   result.update(obs);result['f_half']=float(-2*np.log(state['eta']));result['eta_half']=float(state['eta'])
   W,_,_,_=V.build_mpo(3,2,rate);lam,F=V.dominant(lambda x:V.apply_TL(x,AL,W),(chi,W.shape[0],chi),tol=1e-10)
   defect=float(np.linalg.norm(V.apply_TL(F,AL,W)-lam*F)/abs(lam))
   if lam<=0 or not np.isfinite(defect):raise RuntimeError('Invalid full-period trial contraction')
   import branch128_pilot_worker as diagnostic
   result.update(f_full_rayleigh=float(-np.log(lam)),period_contraction_relative_residual=defect);result.update(diagnostic.color_diagnostics(state,rate))
   accepted=defect<p['period_contraction_ceiling'];result.update(converged=bool(accepted),status='accepted finite-chi numerical state' if accepted else 'period contraction gate failed')
  result['process_peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 except TimeoutError as e:
  result.update(status='authorized wall-clock budget reached',converged=False,reason=str(e))
  if cp.exists():
   try:_,m=H.load_state(cp,operator='hermitian-halfrow');result.update(last_state_metadata=m,eps=m.get('eps'),iters=m.get('iters'),optimizer_seconds=m.get('seconds'))
   except Exception:pass
 except Exception as e:
  result.update(status='unexpected execution/validation error',converged=False,reason=f'{type(e).__name__}: {e}');traceback.print_exc()
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);H.checkpoint=original;result['total_stage_seconds']=time.monotonic()-started
  if cp.exists():result['checkpoint_sha256']=sha(cp)
  atomic(outpath,result);print('CHI192_UPPER_RESULT',json.dumps({k:result.get(k) for k in ['status','converged','iters','eps','color_l2_order','f_half','f_full_rayleigh','total_stage_seconds']}),flush=True)
if __name__=='__main__':benchmark() if len(sys.argv)>1 and sys.argv[1]=='--benchmark' else production()

#!/usr/bin/env python3
"""Resume the interrupted small-order χ192 midpoint continuation from its last atomic checkpoint."""
from pathlib import Path
import json,hashlib,os,time,signal,resource,traceback
import numpy as np
import replica_halfrow as H
import replica_vumps as V
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
BASE=ROOT/'research/transition-order/branch192-mid-pair-protocol.json'
REC=ROOT/'research/transition-order/branch192-mid-pair-small-resume-protocol.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,obj):
 p=Path(p);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,p)
def mirror_fn(N):
 def mirror(F):
  B=.5*(F[:,:N,:]+F[:,N:,:].transpose(2,1,0));return np.concatenate([B,B.transpose(2,1,0)],axis=1)
 return mirror
def run():
 p=json.loads(BASE.read_text());r=json.loads(REC.read_text());
 for rel,h in r['source_sha256'].items():assert sha(ROOT/rel)==h,rel
 src=r['interrupted_checkpoint'];srcpath=ROOT/src['path'];assert sha(srcpath)==src['sha256']
 init,meta=H.load_state(srcpath,operator='hermitian-halfrow')
 assert meta.get('n')==3 and meta.get('d')==2 and meta.get('p')==.304825 and meta.get('chi')==192
 assert all(np.isfinite(init[k]).all() for k in ['AL','AR','AC','C'])
 outpath=R/'branch192_mid_pair_small_resume1.json';cp=R/'checkpoints/branch192_mid_pair_small_resume1_p0.3048250.npz'
 if outpath.exists() or cp.exists():raise SystemExit('Resume outputs already exist; refusing duplicate segment')
 remaining=p['deadline_unix']-time.time();reserves=r['feasibility_gate']['reserves'];stage=min(r['small_resume_budget_seconds'],remaining-reserves['setup_seconds']-reserves['validation_seconds']-reserves['postreserve_safety_buffer_seconds'])
 if stage<60:raise SystemExit('Recovery stage infeasible after retaining both validations and safety reserve')
 os.environ['STAGE_SECONDS']=str(stage);os.environ['CORR_RMAX']=str(p['correlation_rmax'])
 base_row=json.loads((R/'branch192_mid_pair_small_restart1.json').read_text())
 base_iters=int(base_row['iters']);base_optimizer=float(base_row['optimizer_seconds'])
 result=dict(campaign=p['campaign'],history='small',p=.304825,n=3,d=2,chi=192,status='resuming from interrupted checkpoint',converged=False,
  external_tol=p['external_tol'],internal_goal=p['internal_goal'],source_checkpoint=str(srcpath.relative_to(ROOT)),source_checkpoint_sha256=src['sha256'],
  source_metadata=meta,previous_segment_iterations=base_iters,previous_segment_optimizer_seconds=base_optimizer,
  checkpoint=str(cp.relative_to(R)),resume_segment=1,qualification='Resumption of the originally authorized small-order preparation; no additional rate or independent preparation.')
 saver=H.checkpoint
 def compact(path,st,met):
  physical=dict(st,FL=None,FR=None);info=dict(met,environment_cache_omitted=True,checkpoint_contents='AL,AR,AC,C; recompute FL/FR on restart',
   acceptance_tol=p['external_tol'],optimizer_internal_goal=p['internal_goal'],campaign=p['campaign'],resume_segment=1,previous_checkpoint_sha256=src['sha256'])
  saver(path,physical,info);result.update(continuation_segment_iterations=int(st['iters']),continuation_segment_optimizer_seconds=float(st['seconds']),
   iters=base_iters+int(st['iters']),optimizer_seconds=base_optimizer+float(st['seconds']),eps=float(st['eps']));atomic(outpath,result)
 original=H.checkpoint;H.checkpoint=compact;started=time.monotonic()
 signal.signal(signal.SIGALRM,lambda s,f:(_ for _ in ()).throw(TimeoutError('original 12-hour campaign deadline reached')))
 signal.signal(signal.SIGTERM,lambda s,f:(_ for _ in ()).throw(TimeoutError('resume worker was stopped')))
 signal.setitimer(signal.ITIMER_REAL,max(1,int(remaining)));atomic(outpath,result)
 try:
  try:
   state,obs=H.solve(3,2,.304825,192,init=init,tol=p['internal_goal'],maxiter=p['maxiter'],checkpoint_path=cp,tag='chi192-mid-small-resume1',verbose=True)
  except RuntimeError as e:
   if 'budget' not in str(e).lower():raise
   result['optimizer_budget_reason']=str(e)
   if not cp.exists():raise
   state,meta2=H.load_state(cp,operator='hermitian-halfrow');obs=None
  AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
  left=float(np.linalg.norm(AC.reshape(1152,192)-AL.reshape(1152,192)@C));right=float(np.linalg.norm(AC.reshape(192,1152)-C@AR.reshape(192,1152)))
  lc=float(np.linalg.norm(AL.reshape(1152,192).T@AL.reshape(1152,192)-np.eye(192)));rc=float(np.linalg.norm(AR.reshape(192,1152)@AR.reshape(192,1152).T-np.eye(192)))
  cumit=base_iters+int(state['iters']);cumsec=base_optimizer+float(state['seconds'])
  result.update(eps=float(state['eps']),iters=cumit,optimizer_seconds=cumsec,continuation_segment_iterations=int(state['iters']),
   continuation_segment_optimizer_seconds=float(state['seconds']),gauge_left_residual=left,gauge_right_residual=right,left_canonical_residual=lc,right_canonical_residual=rc,
   internal_goal_met=bool(state['eps']<p['internal_goal']))
  if not(state['eps']<p['external_tol'] and max(left,right)<p['external_tol'] and max(lc,rc)<p['canonical_ceiling']):
   result.update(status='optimizer/gauge gates not passed',converged=False)
  else:
   if obs is None:
    _,G,gh,gmh=H.build_half(3,2,.304825);obs=V.observables(state,G,gh,gmh,rmax=p['correlation_rmax'])
   result.update(obs);result['iters']=cumit;result['optimizer_seconds']=cumsec;result['f_half']=float(-2*np.log(state['eta']));result['eta_half']=float(state['eta'])
   W,_,_,_=V.build_mpo(3,2,.304825);lam,F=V.dominant(lambda x:V.apply_TL(x,AL,W),(192,W.shape[0],192),tol=1e-10)
   defect=float(np.linalg.norm(V.apply_TL(F,AL,W)-lam*F)/abs(lam))
   if lam<=0 or not np.isfinite(defect):raise RuntimeError('Invalid full-period trial contraction')
   import branch128_pilot_worker as diagnostic
   result.update(f_full_rayleigh=float(-np.log(lam)),period_contraction_relative_residual=defect);result.update(diagnostic.color_diagnostics(state,.304825));result['iters']=cumit;result['optimizer_seconds']=cumsec
   ok=defect<p['period_contraction_ceiling'];result.update(converged=bool(ok),status='accepted finite-chi numerical state' if ok else 'period contraction gate failed')
  result['process_peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 except TimeoutError as e:
  result.update(status='original 12-hour wall-clock deadline reached',converged=False,reason=str(e))
  if cp.exists():
   try:_,m=H.load_state(cp,operator='hermitian-halfrow');result.update(eps=m.get('eps'),continuation_segment_iterations=m.get('iters'),continuation_segment_optimizer_seconds=m.get('seconds'))
   except Exception:pass
 except Exception as e:
  result.update(status='unexpected resume/validation error',converged=False,reason=f'{type(e).__name__}: {e}');traceback.print_exc()
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);H.checkpoint=original;result['resume_stage_wall_seconds']=time.monotonic()-started
  if cp.exists():result['checkpoint_sha256']=sha(cp)
  atomic(outpath,result);print('CHI192_MID_PAIR_RESUME_RESULT',json.dumps({k:result.get(k) for k in ['status','converged','iters','eps','optimizer_seconds','resume_stage_wall_seconds']}),flush=True)
if __name__=='__main__':run()

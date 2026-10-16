#!/usr/bin/env python3
"""One authorized p=.304825 warm continuation from an accepted .30480 state.
Unbiased original operator; stricter internal driver, unchanged external gates.
"""
from pathlib import Path
import hashlib,json,os,signal,sys,time
import numpy as np
import replica_halfrow as H
import replica_vumps as V
import branch128_pilot_worker as compact

ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
P=ROOT/'research/transition-order/branch128-mid-protocol.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
 t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(x,indent=2)+'\n');os.replace(t,p)
def main():
 side=sys.argv[1];assert side in ['ordered','disordered']
 protocol=json.loads(P.read_text())
 for name,digest in protocol['source_sha256'].items():assert sha(ROOT/name)==digest,name
 spec=protocol['sources'][side];source=ROOT/spec['checkpoint'];assert sha(source)==spec['sha256']
 initial,source_meta=H.load_state(source,operator='hermitian-halfrow')
 assert source_meta['n']==3 and source_meta['d']==2 and source_meta['chi']==128 and source_meta['p']==.3048
 target=protocol['p'];assert target==.304825 and protocol['chi']==128
 external=protocol['external_tol'];internal=protocol['internal_goal'];assert external==1e-7 and internal==5e-8
 stem=f'branch128_mid_{side}_p{target:.7f}';out=R/(stem+'.json');cp=R/'checkpoints'/(stem+'.npz')
 if out.exists():raise SystemExit('Existing closer-rate case: inspect instead of repeating')
 remaining=protocol['deadline_unix']-time.time()
 if remaining<180:raise SystemExit('No authorized time remains')
 started=time.monotonic()
 result=dict(campaign=protocol['campaign'],history=side,preparation=side,n=3,d=2,p=target,chi=128,
             external_tol=external,optimizer_internal_goal=internal,status='running',converged=False,
             source=spec,source_metadata=source_meta,source_is_accepted_observation=True,
             protocol_sha256=sha(P),checkpoint=str(cp.relative_to(R)),
             qualification='accepted-state warm continuation; history label not a phase; no energy-error or global-minimum certificate')
 def progress(st,meta):
  result.update(eps=float(st['eps']),iters=int(st['iters']),optimizer_seconds=float(st['seconds']))
  save(out,result)
 original=compact.install_compact_checkpointer(progress);saver=H.checkpoint
 def annotated(path,st,meta):return saver(path,st,dict(meta,acceptance_tol=external,optimizer_internal_goal=internal,upper_rate_campaign=protocol['campaign']))
 H.checkpoint=annotated
 def alarm(signum,frame):raise TimeoutError('authorized closer-rate deadline reached')
 signal.signal(signal.SIGALRM,alarm);signal.signal(signal.SIGTERM,alarm);signal.setitimer(signal.ITIMER_REAL,remaining)
 os.environ['STAGE_SECONDS']=str(min(protocol['optimizer_seconds'],remaining-300));os.environ['CORR_RMAX']='240'
 save(out,result);print('CLOSER_CASE_START',side,target,'internal',internal,'external',external,flush=True)
 try:
  try:
   state,obs=H.solve(3,2,target,128,init=initial,tol=internal,maxiter=10000,checkpoint_path=cp,tag='branch128-mid-'+side,verbose=True)
   result['optimizer_stop']='internal-goal / iteration return'
  except RuntimeError as exc:
   if 'budget' not in str(exc).lower():raise
   state,meta=H.load_state(cp,operator='hermitian-halfrow');obs=None
   result.update(optimizer_stop='internal driving budget ended; original external gates checked independently',internal_budget_reason=str(exc))
  AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
  left=float(np.linalg.norm(AC.reshape(768,128)-AL.reshape(768,128)@C));right=float(np.linalg.norm(AC.reshape(128,768)-C@AR.reshape(128,768)))
  lc=float(np.linalg.norm(AL.reshape(768,128).T@AL.reshape(768,128)-np.eye(128)));rc=float(np.linalg.norm(AR.reshape(128,768)@AR.reshape(128,768).T-np.eye(128)))
  result.update(eps=float(state['eps']),iters=int(state['iters']),optimizer_seconds=float(state['seconds']),internal_goal_met=bool(state['eps']<internal),gauge_left_residual=left,gauge_right_residual=right,left_canonical_residual=lc,right_canonical_residual=rc)
  if not (state['eps']<external and max(left,right)<external and max(lc,rc)<1e-9):
   result.update(status='rejected: original external geometry gates not passed',converged=False)
  else:
   if obs is None:
    _,G,gh,gmh=H.build_half(3,2,target);obs=V.observables(state,G,gh,gmh,rmax=240)
   result.update(obs);result['f_half']=float(-2*np.log(state['eta']));result['f']=result['f_half'];result['eta_half']=float(state['eta'])
   result.update(status='geometry passed: period validation pending');save(out,result)
   W,_,_,_=V.build_mpo(3,2,target)
   lam,F=V.dominant(lambda x:V.apply_TL(x,AL,W),(128,W.shape[0],128),tol=1e-10)
   defect=float(np.linalg.norm(V.apply_TL(F,AL,W)-lam*F)/abs(lam))
   if lam<=0 or not np.isfinite(defect):raise RuntimeError('Invalid period contraction')
   result.update(f_full_rayleigh=float(-np.log(lam)),period_contraction_relative_residual=defect)
   result.update(compact.color_diagnostics(state,target))
   result.update(converged=bool(defect<1e-8),status='accepted closer-rate numerical state' if defect<1e-8 else 'rejected: period contraction gate')
 except (RuntimeError,TimeoutError) as exc:
  result.update(status='closer-rate stopped without full acceptance',converged=False,reason=str(exc))
 except Exception as exc:
  result.update(status='unexpected closer-rate error',converged=False,reason=f'{type(exc).__name__}: {exc}');raise
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);H.checkpoint=original
  result['total_stage_seconds']=time.monotonic()-started
  if cp.exists():result['checkpoint_sha256']=sha(cp)
  save(out,result);print('CLOSER_CASE_RESULT',json.dumps({k:result.get(k) for k in ['history','status','eps','gauge_right_residual','m_species','color_l2_order','f_half','f_full_rayleigh','total_stage_seconds']}),flush=True)

if __name__=='__main__':main()

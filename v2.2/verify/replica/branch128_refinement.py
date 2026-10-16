#!/usr/bin/env python3
"""Separately authorized same-point convergence-safety refinement.
Original rejected pilot state/record stay untouched. Internal optimizer goal is
stricter; external gates remain exactly those of the original chi128 pilot.
"""
from pathlib import Path
import hashlib,json,os,sys,time,signal,subprocess,math
import numpy as np
import replica_halfrow as H
import replica_vumps as V
import branch128_pilot_worker as W
import compare_stationary as compare

ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
HERE=ROOT/'research/transition-order';PP=HERE/'branch128-refinement-protocol.json'

def save(path,value):
 tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');os.replace(tmp,path)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def publish():
 try:subprocess.run([sys.executable,str(HERE/'publish_branch128.py')],cwd=ROOT,check=True)
 except Exception as exc:print('REFINEMENT_PUBLICATION_PENDING',type(exc).__name__,flush=True)
def main():
 protocol=json.loads(PP.read_text())
 for name,sha in protocol['source_sha256'].items():assert digest(ROOT/name)==sha,name
 source=ROOT/protocol['source']['checkpoint'];assert digest(source)==protocol['source']['sha256']
 original_path=R/'branch128_pilot_disordered_p0.3048000.json'
 assert digest(original_path)==protocol['original_rejected_json_sha256']
 original=json.loads(original_path.read_text());assert not original['converged']
 pilot_path=R/'n3_branch128_pilot.json';assert digest(pilot_path)==protocol['original_pilot_json_sha256']
 initial,source_meta=H.load_state(source,operator='hermitian-halfrow')
 assert source_meta['p']==.3048 and source_meta['chi']==128 and source_meta['n']==3 and source_meta['d']==2
 output=R/'n3_branch128_refinement.json';cp=R/'checkpoints/branch128_refinement_disordered_p0.3048000.npz'
 if output.exists():raise SystemExit('Refusing accidental refinement repeat')
 started=time.monotonic();remaining=protocol['deadline_unix']-time.time()
 if remaining<180:raise SystemExit('No authorized time remains')
 external=protocol['external_tol'];internal=protocol['internal_goal']
 result=dict(campaign=protocol['campaign'],p=.3048,n=3,d=2,chi=128,history='disordered',
             status='running',converged=False,external_tol=external,optimizer_internal_goal=internal,
             source=protocol['source'],source_is_accepted_observation=False,source_metadata=source_meta,
             original_failed_pilot_unchanged=True,protocol_sha256=digest(PP),checkpoint=str(cp.relative_to(R)),
             qualification='same-point unbiased numerical refinement, not a new rate or a thermodynamic phase certificate')
 def progress(state,meta):
  result.update(eps=float(state['eps']),iters=int(state['iters']),optimizer_seconds=float(state['seconds']))
  save(output,result)
 original_saver=W.install_compact_checkpointer(progress)
 compact_saver=H.checkpoint
 def annotated_checkpoint(path,state,meta):
  return compact_saver(path,state,dict(meta,acceptance_tol=external,optimizer_internal_goal=internal,convergence_safety_amendment=protocol['campaign']))
 H.checkpoint=annotated_checkpoint
 def alarm(signum,frame):raise TimeoutError('authorized refinement deadline reached')
 signal.signal(signal.SIGALRM,alarm);signal.signal(signal.SIGTERM,alarm);signal.setitimer(signal.ITIMER_REAL,remaining)
 os.environ['STAGE_SECONDS']=str(min(1500,remaining-300));os.environ['CORR_RMAX']='240'
 save(output,result);print('REFINEMENT_START p .30480 chi128 internal',internal,'external',external,flush=True)
 try:
  try:
   state,obs=H.solve(3,2,.3048,128,init=initial,tol=internal,maxiter=10000,checkpoint_path=cp,tag='branch128-refinement',verbose=True)
   result['optimizer_stop']='internal target / iteration return'
  except RuntimeError as exc:
   if 'budget' not in str(exc).lower():raise
   state,meta=H.load_state(cp,operator='hermitian-halfrow')
   result['optimizer_stop']='internal driving-target budget reached; external gates evaluated independently'
   result['internal_budget_reason']=str(exc)
   obs=None
  AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
  left=float(np.linalg.norm(AC.reshape(768,128)-AL.reshape(768,128)@C))
  right=float(np.linalg.norm(AC.reshape(128,768)-C@AR.reshape(128,768)))
  lc=float(np.linalg.norm(AL.reshape(768,128).T@AL.reshape(768,128)-np.eye(128)))
  rc=float(np.linalg.norm(AR.reshape(128,768)@AR.reshape(128,768).T-np.eye(128)))
  result.update(eps=float(state['eps']),iters=int(state['iters']),optimizer_seconds=float(state['seconds']),
                gauge_left_residual=left,gauge_right_residual=right,left_canonical_residual=lc,right_canonical_residual=rc,
                internal_goal_met=bool(state['eps']<internal))
  if not (state['eps']<external and max(left,right)<external and max(lc,rc)<1e-9):
   result.update(status='rejected: original external geometry gates not passed',converged=False)
  else:
   if obs is None:
    _,G,gh,gmh=H.build_half(3,2,.3048);obs=V.observables(state,G,gh,gmh,rmax=240)
    obs.update(f_half=float(-2*np.log(state['eta'])),eta_half=state['eta'])
   result.update(obs)
   # Keep the correctly normalized half-row field separate from old generic f.
   result['f_half']=float(-2*np.log(state['eta']));result['f']=result['f_half']
   Wp,_,_,_=V.build_mpo(3,2,.3048)
   lam,F=V.dominant(lambda x:V.apply_TL(x,AL,Wp),(128,Wp.shape[0],128),tol=1e-10)
   defect=float(np.linalg.norm(V.apply_TL(F,AL,Wp)-lam*F)/abs(lam))
   if lam<=0 or not np.isfinite(defect):raise RuntimeError('Invalid period contraction')
   result.update(f_full_rayleigh=float(-np.log(lam)),period_contraction_relative_residual=defect)
   accepted=defect<1e-8
   result.update(converged=bool(accepted),status='accepted under unchanged external gates' if accepted else 'rejected: period-contraction gate')
   result.update(W.color_diagnostics(state,.3048))
   if accepted:
    comp=dict(status='optional comparison pending',orientations=[])
    try:
     pilot=json.loads((R/'n3_branch128_pilot.json').read_text());o=pilot['stages']['2']['ordered'];assert o['converged']
     assert digest(R/o['checkpoint'])==o['checkpoint_sha256']
     A=H.load_state(R/o['checkpoint'],operator='hermitian-halfrow')[0]['AL']
     na,nb=compare.radius(A,A),compare.radius(AL,AL);den=math.sqrt(na['radius']*nb['radius']);G=H.make_group(3)
     comp=dict(status='partial',orientations=[],delta_f_half=o['f_half']-result['f_half'],delta_f_period_trial=o['f_full_rayleigh']-result['f_full_rayleigh'],large_order_source_checkpoint=o['checkpoint'])
     for a in range(6):
      for b in range(6):
       if time.time()>protocol['deadline_unix']-5:break
       v=compare.radius(A,compare.transform(AL,G,a,b));v.update(left=a,right=b,normalized_fidelity_per_site=v['radius']/den);comp['orientations'].append(v)
      else:continue
      break
     if len(comp['orientations'])==36:comp['status']='all 36 symmetry orientations evaluated'
     else:comp['status']='partial orientation search at authorized deadline'
     if comp['orientations']:comp['largest_evaluated_fidelity_per_site']=max(x['normalized_fidelity_per_site'] for x in comp['orientations'])
     result['common_comparison']=comp
    except TimeoutError:
     comp['status']='optional orientation comparison stopped at authorized deadline'
     result['common_comparison']=comp

 except (RuntimeError,TimeoutError) as exc:
  result.update(status='refinement stopped without full acceptance',converged=False,reason=str(exc))
 except Exception as exc:
  result.update(status='unexpected refinement error',converged=False,reason=f'{type(exc).__name__}: {exc}');raise
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);H.checkpoint=original_saver
  result['total_refinement_seconds']=time.monotonic()-started
  if cp.exists():result['checkpoint_sha256']=digest(cp)
  assert digest(original_path)==protocol['original_rejected_json_sha256'],'Original rejected record changed'
  assert digest(pilot_path)==protocol['original_pilot_json_sha256'],'Original pilot record changed'
  assert digest(source)==protocol['source']['sha256'],'Original rejected physical state changed'
  save(output,result);print('REFINEMENT_RESULT',json.dumps({k:result.get(k) for k in ['status','converged','eps','gauge_right_residual','internal_goal_met','m_species','color_l2_order','f_half','f_full_rayleigh','total_refinement_seconds']}),flush=True)
 publish()

if __name__=='__main__':main()

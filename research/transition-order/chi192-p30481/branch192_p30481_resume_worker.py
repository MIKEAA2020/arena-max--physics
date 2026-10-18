#!/usr/bin/env python3
"""Single-thread χ192 p=.30481 paired warm continuations, with resumable checkpoint recovery."""
from pathlib import Path
import hashlib,json,os,sys,time,signal,resource,traceback
import numpy as np
import replica_halfrow as H
import replica_vumps as V
ROOT=Path(os.environ.get('WORKER_ROOT',Path(__file__).resolve().parents[3])).resolve();R=Path(os.environ.get('CAMPAIGN_OUTPUT_DIR',Path(__file__).resolve().parent)).resolve();R.mkdir(parents=True,exist_ok=True)
PROTOCOL=Path(os.environ.get('CAMPAIGN_PROTOCOL_PATH',ROOT/'research/transition-order/branch192-mid-pair-p30481-protocol.json')).resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,obj):
 p=Path(p);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,p)
def mirror_fn(N):
 def mirror(F):
  B=.5*(F[:,:N,:]+F[:,N:,:].transpose(2,1,0))
  return np.concatenate([B,B.transpose(2,1,0)],axis=1)
 return mirror
def load_source(p,prep):
 spec=p['sources'][prep];cp=ROOT/spec['checkpoint'];assert sha(cp)==spec['sha256'];st,meta=H.load_state(cp,operator='hermitian-halfrow')
 assert meta['n']==3 and meta['d']==2 and meta['chi']==192 and st['AL'].shape==(192,6,192)
 assert meta['p']==spec['p']
 return st,meta,spec
def benchmark(prep):
 p=json.loads(PROTOCOL.read_text());init,meta,spec=load_source(p,prep);start=time.monotonic();W,G,gh,gmh=H.build_half(3,2,p['p']);N=G['N']
 out=V.vumps(W,192,init=init,tol=p['internal_goal'],maxiter=1,verbose=True,env_project=mirror_fn(N),paired_env_dim=N)
 row=dict(kind='disposable one-step χ192 p=.30481 branch-retention feasibility benchmark; no scientific result',preparation=prep,p=p['p'],chi=192,initial_chi=192,
  source_checkpoint=spec['checkpoint'],source_sha256=spec['sha256'],iterations=out['iters'],vumps_seconds=out['seconds'],seconds_per_iteration=out['seconds']/out['iters'],
  wall_seconds=time.monotonic()-start,eps_after_one_step=out['eps'],finite_output=all(np.isfinite(out[k]).all() for k in ['AL','AR','AC','C']),
  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,no_state_checkpoint_written=True,not_a_convergence_observation=True)
 atomic(R/f'branch192_p30481_{prep}_benchmark.json',row);print('CHI192_MID_PAIR_BENCHMARK',json.dumps(row),flush=True)
def solve_every_step(n,d,p,chi,init=None,tol=1e-8,maxiter=400,checkpoint_path=None,tag='run',verbose=True):
    """Same paired-half-row VUMPS solve as H.solve, checkpointed after every iteration."""
    W,G,gh,gmh=H.build_half(n,d,p)
    meta=dict(n=n,d=d,p=p,operator='hermitian-halfrow',tag=tag,
              checkpoint_schema=1,tol=tol,maxiter=maxiter,
              stage_budget_seconds=float(os.environ.get('STAGE_SECONDS','0')))
    N=G['N']
    def mirror(F):
        B=.5*(F[:,:N,:]+F[:,N:,:].transpose(2,1,0))
        return np.concatenate([B,B.transpose(2,1,0)],axis=1)
    def cb(st):
        if checkpoint_path: H.checkpoint(checkpoint_path,st,meta)
        budget=float(os.environ.get('STAGE_SECONDS','0'))
        if budget and st['seconds']>budget:
            if checkpoint_path: H.checkpoint(checkpoint_path,st,{**meta,'budget_exhausted':True})
            raise RuntimeError('Stage wall-clock budget exhausted; resumable checkpoint saved')
    st=V.vumps(W,chi,init=init,tol=tol,maxiter=maxiter,verbose=verbose,callback=cb,
               env_project=mirror,paired_env_dim=N)
    if checkpoint_path: H.checkpoint(checkpoint_path,st,meta)
    ob=V.observables(st,G,gh,gmh,rmax=int(os.environ.get('CORR_RMAX','400')))
    ob['eta_half']=ob['eta'];ob['f_half']=-2*np.log(ob['eta_half']);ob['f']=ob['f_half']
    ob.update(n=n,d=d,p=p,tag=tag,operator='hermitian-halfrow',chi=chi)
    return st,ob

def production(prep,resume=False):
 p=json.loads(PROTOCOL.read_text())
 for rel,h in p['source_sha256'].items():assert sha(ROOT/rel)==h,rel
 if p.get('recovery_worker'):
  assert sha(Path(__file__))==p['recovery_worker']['sha256'],'recovery worker hash mismatch'
 init,srcmeta,spec=load_source(p,prep);rate=p['p'];chi=192
 outpath=R/f'branch192_p30481_{prep}.json';cp=R/f'checkpoints/branch192_p30481_{prep}_p0.3048100.npz';cp.parent.mkdir(parents=True,exist_ok=True)
 base_iters=0;base_seconds=0.0;resume_meta=None;resume_hash=None
 if resume:
  if not outpath.exists() or not cp.exists():raise SystemExit('Cannot resume: named progress row/checkpoint missing')
  prior=json.loads(outpath.read_text())
  assert prior['history']==prep and prior['p']==rate and prior['chi']==chi
  resume_meta_state,resume_meta=H.load_state(cp,operator='hermitian-halfrow')
  assert resume_meta.get('p')==rate and resume_meta.get('n')==3 and resume_meta.get('d')==2 and resume_meta.get('chi')==chi
  assert resume_meta.get('tag')=='chi192-p30481-'+prep
  init=resume_meta_state;base_iters=int(init['iters']);base_seconds=float(init['seconds']);resume_hash=sha(cp)
  expected=p.get('resume_source',{}).get('sha256')
  if expected:assert resume_hash==expected,'resume checkpoint hash differs from protocol'
  result=dict(prior);result.update(status='running',converged=False,resumed_from_checkpoint=str(cp.relative_to(R)),
      resumed_from_sha256=resume_hash,resume_source_iterations=base_iters,resume_source_optimizer_seconds=base_seconds)
  result.pop('reason',None)
 else:
  if outpath.exists() or cp.exists():raise SystemExit('Named paired-midpoint output already exists')
  result=dict(campaign=p['campaign'],history=prep,p=rate,n=3,d=2,chi=chi,external_tol=p['external_tol'],internal_goal=p['internal_goal'],status='running',converged=False,
    source=spec,source_metadata=srcmeta,source_is_accepted_observation=True,checkpoint=str(cp.relative_to(R)),qualification='one of a paired single-rate finite-chi branch-retention test; not a global-minimum or transition certificate')
 remaining=p['deadline_unix']-time.time()
 validation_left=int(os.environ.get('PAIR_REMAINING_VALIDATION_SECONDS',p['validation_reserve_seconds_total']))
 setup_left=int(os.environ.get('PAIR_REMAINING_SETUP_SECONDS',p['setup_reserve_seconds_total']))
 optimizer_left=max(0.0,float(p['optimizer_budget_seconds'][prep])-base_seconds)
 stage=min(optimizer_left,remaining-validation_left-setup_left)
 if stage<60:raise SystemExit('Insufficient stage budget; validation reserves protected')
 os.environ['STAGE_SECONDS']=str(stage);os.environ['CORR_RMAX']=str(p['correlation_rmax'])
 result.update(status='running',converged=False,stage_budget_seconds=stage)
 if resume:result['resume_count']=int(result.get('resume_count',0))+1
 saver=H.checkpoint
 def compact(path,st,meta):
  cumulative=dict(st);cumulative['iters']=base_iters+int(st['iters']);cumulative['seconds']=base_seconds+float(st['seconds'])
  physical=dict(cumulative,FL=None,FR=None);info=dict(meta,environment_cache_omitted=True,checkpoint_contents='AL,AR,AC,C; recompute FL/FR on restart',
    acceptance_tol=p['external_tol'],optimizer_internal_goal=p['internal_goal'],campaign=p['campaign'],
    cumulative_iteration_offset=base_iters,cumulative_seconds_offset=base_seconds)
  saver(path,physical,info);result.update(eps=float(st['eps']),iters=int(cumulative['iters']),optimizer_seconds=float(cumulative['seconds']));atomic(outpath,result)
 original=H.checkpoint;H.checkpoint=compact;started=time.monotonic()
 signal.signal(signal.SIGALRM,lambda s,f:(_ for _ in ()).throw(TimeoutError('authorized p=.30481 campaign deadline reached')))
 signal.signal(signal.SIGTERM,lambda s,f:(_ for _ in ()).throw(TimeoutError('paired campaign manager stop')))
 signal.setitimer(signal.ITIMER_REAL,max(1,int(remaining)));atomic(outpath,result)
 try:
  try:
   solver=solve_every_step if resume else H.solve
   state,obs=solver(3,2,rate,chi,init=init,tol=p['internal_goal'],maxiter=p['maxiter'],checkpoint_path=cp,tag='chi192-p30481-'+prep,verbose=True)
  except RuntimeError as e:
   if 'budget' not in str(e).lower():raise
   result['optimizer_budget_reason']=str(e)
   if not cp.exists():raise
   state,meta=H.load_state(cp,operator='hermitian-halfrow');obs=None
   state['iters']=int(state['iters'])-base_iters;state['seconds']=float(state['seconds'])-base_seconds
  state['iters']=int(state['iters'])+base_iters;state['seconds']=float(state['seconds'])+base_seconds
  AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
  left=float(np.linalg.norm(AC.reshape(1152,192)-AL.reshape(1152,192)@C));right=float(np.linalg.norm(AC.reshape(192,1152)-C@AR.reshape(192,1152)))
  lc=float(np.linalg.norm(AL.reshape(1152,192).T@AL.reshape(1152,192)-np.eye(192)));rc=float(np.linalg.norm(AR.reshape(192,1152)@AR.reshape(192,1152).T-np.eye(192)))
  result.update(eps=float(state['eps']),iters=int(state['iters']),optimizer_seconds=float(state['seconds']),gauge_left_residual=left,gauge_right_residual=right,
   left_canonical_residual=lc,right_canonical_residual=rc,internal_goal_met=bool(state['eps']<p['internal_goal']))
  if not(state['eps']<p['external_tol'] and max(left,right)<p['external_tol'] and max(lc,rc)<p['canonical_ceiling']):
   result.update(status='optimizer/gauge gates not passed',converged=False)
  else:
   if obs is None:
    _,G,gh,gmh=H.build_half(3,2,rate);obs=V.observables(state,G,gh,gmh,rmax=p['correlation_rmax'])
   result.update(obs);result['f_half']=float(-2*np.log(state['eta']));result['eta_half']=float(state['eta']);result['iters']=int(state['iters']);result['optimizer_seconds']=float(state['seconds'])
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
  atomic(outpath,result);print('CHI192_MID_PAIR_RESULT',json.dumps({k:result.get(k) for k in ['history','status','converged','iters','eps','color_l2_order','f_half','total_stage_seconds']}),flush=True)
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='--benchmark':benchmark(sys.argv[2])
 elif len(sys.argv)==2 and sys.argv[1] in ['ordered','small']:production(sys.argv[1])
 elif len(sys.argv)==3 and sys.argv[1]=='--resume' and sys.argv[2] in ['ordered','small']:production(sys.argv[2],resume=True)
 else:raise SystemExit('usage: worker --benchmark {ordered|small} | {ordered|small} | --resume {ordered|small}')

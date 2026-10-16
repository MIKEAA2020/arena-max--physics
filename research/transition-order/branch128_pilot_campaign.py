#!/usr/bin/env python3
"""Two-stage, three-hour unbiased branch-retention pilot at chi128.
Two workers maximum. Stage 2 uses only accepted stage-1 tensors. No constrained
phase branch, automatic extra rate, perturbation production or chi192.
"""
from pathlib import Path
import json,hashlib,os,sys,subprocess,time,math,threading,fcntl
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(HERE))
import chi128_scan_campaign as base


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,data):
 tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');os.replace(tmp,path)
def publish(db):
 try:subprocess.run([sys.executable,str(HERE/'publish_branch128.py')],cwd=ROOT,check=True)
 except Exception as exc:
  db.setdefault('publication_error_history',[]).append(f'{type(exc).__name__}: {exc}')
  save(R/'n3_branch128_pilot.json',db);print('BRANCH_PUBLICATION_PENDING',type(exc).__name__,flush=True)


def main():
 (ROOT/'.arena').mkdir(exist_ok=True)
 lock=(ROOT/'.arena/branch128-pilot.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 path=HERE/'branch128-pilot-protocol.json';protocol=json.loads(path.read_text())
 for name,sha in protocol['source_sha256'].items():assert digest(ROOT/name)==sha,name
 data_path=R/'n3_branch128_pilot.json'
 if data_path.exists():raise SystemExit('Existing pilot record: inspect processes/real checkpoints; do not blindly rerun')
 scan=json.loads((R/'n3_chi128_scan.json').read_text())
 anchors={}
 for side,p in [('ordered',.3047),('disordered',.30486)]:
  r=scan['cases'][f'{p:.7f}'][side];base.verify_accepted(r)
  assert r['checkpoint_sha256']==protocol['anchors'][side]['sha256']
  anchors[side]=r
 db=dict(campaign=protocol['campaign'],status='running: authorized stage 1',anchors=anchors,stages={},
         protocol_sha256=digest(path),thermodynamic_order='unresolved',crossing_bracket_measured=False,
         perturbation_stability_tests_performed=False,chi192_launched=False)
 save(data_path,db);publish(db)
 sources=dict(protocol['anchors'])
 terminal={'accepted-finite-chi','budget-stopped','iteration-cap-or-stationarity-check-failed','period-contraction-check-failed','optimizer-or-validation-failed','unexpected-error','worker-exited-without-record','worker-terminated-before-final-record'}
 for stage,targets in enumerate(protocol['targets'],1):
  if time.time()>protocol['global_deadline_unix']-180:
   db['status']='remaining stage deferred at authorized overall deadline';break
  deadline=min(time.time()+5400,protocol['global_deadline_unix'])
  stage_master=dict(protocol)
  stage_master.update(preparations=sources,optimizer_seconds=5280,correlation_rmax=240,
                      canonical_ceiling=1e-9,period_contraction_ceiling=1e-8)
  master_path=HERE/'branch128'/f'stage-{stage}-master.json';master_path.parent.mkdir(exist_ok=True)
  if master_path.exists():raise RuntimeError('Refusing overwrite of a frozen stage master')
  save(master_path,stage_master)
  children=[];threads=[];print('BRANCH_STAGE_START',stage,json.dumps(targets),flush=True)
  def relay(pipe,logfile,side,p):
   with logfile.open('w') as f:
    for line in pipe:
     f.write(line);f.flush();print(f'[stage {stage} {side} p={p:.7f}] '+line.rstrip(),flush=True)
  env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
  for side in ['ordered','disordered']:
   p=targets[side]
   point=dict(p=p,master_protocol=str(master_path.relative_to(ROOT)),master_sha256=digest(master_path),deadline_unix=deadline,stage=stage,history=side)
   point_path=HERE/'branch128'/f'stage-{stage}-{side}.json';save(point_path,point)
   seconds=max(1,math.ceil(deadline-time.time()))
   cmd=['timeout','--signal=TERM','--kill-after=5s',str(seconds)+'s',sys.executable,'-u',str(R/'branch128_pilot_worker.py'),str(point_path),side]
   child=subprocess.Popen(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
   log=R/f'branch128_pilot_{side}_p{p:.7f}.log'
   t=threading.Thread(target=relay,args=(child.stdout,log,side,p),daemon=True);t.start()
   threads.append(t);children.append((side,p,child))
  result={}
  for side,p,child in children:
   code=child.wait();out=R/f'branch128_pilot_{side}_p{p:.7f}.json'
   r=json.loads(out.read_text()) if out.exists() else dict(p=p,chi=128,tol=1e-7,preparation=side,status='worker-exited-without-record',converged=False)
   if r.get('status') not in terminal:r.update(status='worker-terminated-before-final-record',converged=False)
   r['process_exit_code']=code
   base.verify_accepted(r);result[side]=r;save(out,r)
  for t in threads:t.join()
  db['stages'][str(stage)]=result;save(data_path,db)
  print('BRANCH_STAGE_DONE',stage,json.dumps({s:result[s]['status'] for s in ['ordered','disordered']}),flush=True)
  if not all(result[s].get('converged') for s in ['ordered','disordered']):
   db['status']=f'stopped: stage {stage} acceptance gate not passed for both histories';save(data_path,db);publish(db);break
  if stage==2:
   assert result['ordered']['p']==result['disordered']['p']==.3048
   db['common_comparison']=base.fidelity(result['ordered'],result['disordered'],deadline)
   db['common_comparison']['delta_f_half']=result['ordered']['f_half']-result['disordered']['f_half']
   db['common_comparison']['delta_f_period_trial']=result['ordered']['f_full_rayleigh']-result['disordered']['f_full_rayleigh']
  sources={s:dict(checkpoint=str((R/result[s]['checkpoint']).relative_to(ROOT)),sha256=result[s]['checkpoint_sha256'],source_p=result[s]['p'],accepted_source=True,qualification='actual accepted state from previous continuation step; not a certified thermodynamic phase') for s in ['ordered','disordered']}
  db['status']=f'running: stage {stage} accepted; next step remains separately gated' if stage==1 else 'complete: four continuation steps accepted at finite chi'
  save(data_path,db);publish(db)
 else:
  db['status']='complete: four continuation steps accepted at finite chi'
 db['finished_at_unix']=time.time();save(data_path,db)
 publish(db)
 print('BRANCH_PILOT_DONE',json.dumps(dict(status=db['status'],stages=len(db['stages']),order='unresolved')),flush=True)


if __name__=='__main__':main()

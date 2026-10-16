#!/usr/bin/env python3
"""One authorized additional common rate, p=.30485, two workers, one hour.
No automatic rate refinement, chi192 or stability campaign. No automatic physical
classification from pressure signs or optimizer outcomes.
"""
from pathlib import Path
import os,sys,json,hashlib,subprocess,threading,time,math,fcntl
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(HERE))
import chi128_scan_campaign as base

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
 t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(x,indent=2)+'\n');os.replace(t,p)
def publish(db):
 try:subprocess.run([sys.executable,str(HERE/'publish_branch128.py')],cwd=ROOT,check=True)
 except Exception as exc:
  db.setdefault('publication_error_history',[]).append(f'{type(exc).__name__}: {exc}')
  save(R/'n3_branch128_upper.json',db);print('UPPER_PUBLICATION_PENDING',type(exc).__name__,flush=True)
def main():
 (ROOT/'.arena').mkdir(exist_ok=True);lock=(ROOT/'.arena/branch128-upper.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 path=HERE/'branch128-upper-protocol.json';protocol=json.loads(path.read_text())
 for name,digest in protocol['source_sha256'].items():assert sha(ROOT/name)==digest,name
 previous={}
 for side,spec in protocol['sources'].items():
  record=ROOT/spec['record'];assert sha(record)==spec['record_sha256']
  row=json.loads(record.read_text());base.verify_accepted(row)
  assert row['p']==.3048 and row['chi']==128 and sha(ROOT/spec['checkpoint'])==spec['sha256']
  previous[side]=row
 output=R/'n3_branch128_upper.json'
 if output.exists():raise SystemExit('Named upper-rate experiment already exists; inspect instead of repeating')
 db=dict(campaign=protocol['campaign'],status='running: one common upper rate',p=.30485,chi=128,
         protocol_sha256=sha(path),previous_common=previous,results={},thermodynamic_order='unresolved',
         automatic_physical_bracket=False,stability_tests_performed=False,chi192_launched=False)
 save(output,db);publish(db)
 if time.time()>protocol['deadline_unix']-180:raise SystemExit('Insufficient authorized time remains to launch')
 children=[];threads=[];env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
 def relay(pipe,logfile,side):
  with logfile.open('w') as f:
   for line in pipe:
    f.write(line);f.flush();print(f'[upper {side}] '+line.rstrip(),flush=True)
 print('UPPER_PAIR_START p .30485 deadline',protocol['deadline_unix'],flush=True)
 for side in ['ordered','disordered']:
  seconds=max(1,math.ceil(protocol['deadline_unix']-time.time()))
  cmd=['timeout','--signal=TERM','--kill-after=5s',str(seconds)+'s',sys.executable,'-u',str(R/'branch128_upper_worker.py'),side]
  child=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
  thread=threading.Thread(target=relay,args=(child.stdout,R/f'branch128_upper_{side}_p0.3048500.log',side),daemon=True);thread.start()
  threads.append(thread);children.append((side,child))
 for side,child in children:
  rc=child.wait();p=R/f'branch128_upper_{side}_p0.3048500.json'
  row=json.loads(p.read_text()) if p.exists() else dict(p=.30485,chi=128,history=side,status='worker exited without record',converged=False)
  if row.get('status') in ['running','geometry passed: period validation pending']:row.update(status='worker terminated before final validation',converged=False)
  row['process_exit_code']=rc;base.verify_accepted(row);save(p,row);db['results'][side]=row
 for thread in threads:thread.join()
 if all(db['results'][s].get('converged') for s in ['ordered','disordered']):
  a,b=db['results']['ordered'],db['results']['disordered'];assert a['p']==b['p']==.30485
  db['upper_comparison']=base.fidelity(a,b,protocol['deadline_unix'])
  lowerH=previous['ordered']['f_half']-previous['disordered']['f_half'];upperH=a['f_half']-b['f_half']
  lowerC=previous['ordered']['f_full_rayleigh']-previous['disordered']['f_full_rayleigh'];upperC=a['f_full_rayleigh']-b['f_full_rayleigh']
  db.update(delta_f_half_lower=lowerH,delta_f_half_upper=upperH,delta_f_period_lower=lowerC,delta_f_period_upper=upperC,
            half_objective_sign_change=bool(lowerH*upperH<0),period_trial_sign_change=bool(lowerC*upperC<0),
            upper_order_contrast=abs(a['color_l2_order']-b['color_l2_order']),
            order_diagnostic_paths={s:dict(lower=previous[s]['color_l2_order'],upper=db['results'][s]['color_l2_order']) for s in ['ordered','disordered']},
            status='complete: both upper-rate numerical states accepted')
 else:db['status']='upper rate attempted: fewer than two preparations passed all gates'
 db['finished_at_unix']=time.time();save(output,db)
 publish(db)
 print('UPPER_RATE_DONE',json.dumps(dict(status=db['status'],physical_order='unresolved')),flush=True)

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Execute the authorized one-hour cap extension for the one χ192 .30485 path."""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess,math
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
P=HERE/'branch192-upper-protocol.json';E=HERE/'branch192-upper-extension-addendum.json';A=R/'n3_branch192_upper.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,x):
 p=Path(p);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(x,indent=2)+'\n');os.replace(tmp,p)
def mem_available():return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))
def env1():
 e=os.environ.copy()
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:e[k]='1'
 e['PYTHONUNBUFFERED']='1';e['PYTHONPATH']=str(R)+(os.pathsep+e['PYTHONPATH'] if e.get('PYTHONPATH') else '')
 return e
def main():
 p=json.loads(P.read_text());db=json.loads(A.read_text());bench=json.loads((R/'branch192_upper_benchmark.json').read_text())
 if E.exists():raise SystemExit('Extension addendum already exists; refusing a second launch')
 if db.get('status')!='feasibility gate failed; production not launched' or db.get('result') is not None:raise SystemExit('Expected the original benchmark-only stop record')
 if p.get('feasibility_gate',{}).get('production_authorized') is not False:raise SystemExit('Original stopped gate does not match expected provenance')
 if not (bench.get('finite_output') is True and bench.get('no_state_checkpoint_written') is True and bench.get('not_a_convergence_observation') is True):raise SystemExit('Disposable benchmark integrity check failed')
 if (R/'n3_branch192_upper_ordered.json').exists() or (R/'checkpoints/branch192_upper_ordered_p0.3048500.npz').exists():raise SystemExit('Production output/checkpoint already exists; no retry')
 if sha(ROOT/p['source']['checkpoint'])!=p['source']['sha256']:raise SystemExit('Accepted χ192 .30480 source hash mismatch')
 ps=subprocess.check_output(['ps','-eo','args='],text=True)
 active=[x for x in ps.splitlines() if any(t in x for t in ['replica_halfrow.py','branch192_worker_v2.py','branch192_upper_worker.py','branch192_upper_extension_worker.py']) and 'branch192_upper_extension.py' not in x]
 if active:raise SystemExit('Another replica/χ192 optimizer is active')
 # User selected a one-hour addition to the original five-hour absolute cap (six hours total from its frozen start).
 old_deadline=float(p['deadline_unix']);new_deadline=float(p['started_unix'])+6*3600;now=time.time()
 if abs(old_deadline-(float(p['started_unix'])+5*3600))>1:raise SystemExit('Original deadline is not the expected five-hour absolute cap')
 remaining=new_deadline-now;gate0=p['feasibility_gate'];forecast=float(gate0['forecast_seconds']);rss=int(bench['peak_rss_kib']);avail=mem_available()
 time_ok=remaining>=forecast;memory_ok=1.25*rss<=.75*avail
 worker=R/'branch192_upper_extension_worker.py';runner=Path(__file__).resolve();report=HERE/'branch192_upper_extension_report.py';audit=R/'branch192_upper_audit.py'
 code_hashes={str(x.relative_to(ROOT)):sha(x) for x in [worker,runner,report,audit]}
 headroom=remaining-forecast
 gate=dict(time_passed=bool(time_ok),memory_passed=bool(memory_ok),forecast_seconds=forecast,remaining_seconds=remaining,headroom_seconds=headroom,
  forecast_iterations=int(gate0['forecast_iterations']),per_iteration_seconds=float(gate0['per_iteration_seconds']),setup_reserve_seconds=int(p['setup_reserve_seconds']),
  validation_reserve_seconds=int(p['validation_reserve_seconds']),peak_rss_kib=rss,mem_available_kib=avail,production_authorized=bool(time_ok and memory_ok),
  decision='PROCEED with exactly one ordered χ192 p=.30485 continuation under the extended six-hour absolute cap' if time_ok and memory_ok else 'STOP; extension gate does not fit')
 add=dict(kind='user-authorized cap-extension addendum; preserves original frozen protocol and failed five-hour gate',
  authorization='User selected +60 minutes: extend the same campaign absolute cap from five hours to six hours, measured from the original protocol start. Exactly one ordered χ192 p=.30485 continuation from the accepted χ192 p=.30480 state remains in scope.',
  extension_seconds=3600,total_wall_cap_seconds=21600,original_started_unix=p['started_unix'],original_deadline_unix=old_deadline,extended_deadline_unix=new_deadline,
  extension_decision_unix=now,original_protocol_sha256=sha(P),original_benchmark_sha256=sha(R/'branch192_upper_benchmark.json'),benchmark_seconds_per_iteration=bench['seconds_per_iteration'],
  benchmark_peak_rss_kib=rss,forecast_rule='Preserve the original frozen forecast unchanged: 205 iterations × measured/reference seconds per iteration, plus 120-second setup reserve and 900-second independent validation/report reserve.',
  optimizer_budget_seconds=max(0,remaining-int(p['validation_reserve_seconds'])-int(p['setup_reserve_seconds'])),setup_reserve_seconds=int(p['setup_reserve_seconds']),
  validation_reserve_seconds=int(p['validation_reserve_seconds']),extended_gate=gate,extension_code_sha256=code_hashes,extension_worker_sha256=sha(worker),
  scope='Only the previously authorized single ordered χ192 p=.30485 continuation. No new rates, preparation, excited-state/gap, perturbation or stability calculations.')
 atomic(E,add)
 print('CHI192_UPPER_EXTENSION_GATE',json.dumps(gate),flush=True)
 if not gate['production_authorized']:
  db.update(status='extended feasibility gate failed; production not launched',extension_addendum=str(E.relative_to(ROOT)),extension_gate=gate,extension_authorization=add['authorization'])
  atomic(A,db);subprocess.run([sys.executable,str(report)],cwd=ROOT,check=True);return
 # Existing aggregate becomes an explicit one-worker running record before launch.
 db.update(status='extended-cap production running',extension_addendum=str(E.relative_to(ROOT)),extension_gate=gate,extension_authorization=add['authorization'],result=None)
 atomic(A,db)
 log=R/'branch192_upper_ordered.log';env=env1()
 with log.open('w') as out:
  proc=subprocess.Popen([sys.executable,str(worker)],cwd=R,env=env,stdout=out,stderr=subprocess.STDOUT)
  try:
   code=proc.wait(timeout=max(1,new_deadline-time.time()+30))
  except subprocess.TimeoutExpired:
   proc.terminate()
   try:code=proc.wait(timeout=30)
   except subprocess.TimeoutExpired:proc.kill();code=proc.wait()
 result=json.loads((R/'n3_branch192_upper_ordered.json').read_text()) if (R/'n3_branch192_upper_ordered.json').exists() else dict(status='worker produced no result record',converged=False)
 db=json.loads(A.read_text());db.update(status='accepted finite-chi upper-rate state' if result.get('converged') else 'upper-rate optimizer/gates incomplete',extension_worker_exit_code=code,result=result,
  interpretation='One finite-chi continuation at one rate/history; not a phase boundary, spinodal, or transition-order certificate.')
 atomic(A,db)
 if result.get('converged'):
  left=max(1,min(900,new_deadline-time.time()-30))
  audit_run=subprocess.run([sys.executable,str(audit)],cwd=ROOT,env=env,capture_output=True,text=True,timeout=left)
  db=json.loads(A.read_text());db.update(audit_status='passed' if audit_run.returncode==0 else 'failed',audit_output=audit_run.stdout+audit_run.stderr);atomic(A,db)
 subprocess.run([sys.executable,str(report)],cwd=ROOT,check=True)
 print('CHI192_UPPER_EXTENSION_FINAL',json.dumps(dict(status=db['status'],converged=result.get('converged'),worker_exit_code=code,remaining_to_extended_deadline=max(0,new_deadline-time.time()),audit_status=db.get('audit_status'))),flush=True)
if __name__=='__main__':main()

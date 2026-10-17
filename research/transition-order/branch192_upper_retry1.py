#!/usr/bin/env python3
"""Fresh, benchmark-first six-hour single-path χ192 p=.30485 continuation."""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
P=HERE/'branch192-upper-retry1-protocol.json';AGG=R/'n3_branch192_upper_retry1.json'
WORKER=R/'branch192_upper_retry1_worker.py';AUDIT=R/'branch192_upper_retry1_audit.py';REPORT=HERE/'branch192_upper_retry1_report.py'
SOURCES={
 'v2.2/verify/replica/replica_vumps.py':R/'replica_vumps.py',
 'v2.2/verify/replica/replica_halfrow.py':R/'replica_halfrow.py',
 'v2.2/verify/replica/replica_tm.py':R/'replica_tm.py',
 'v2.2/verify/replica/branch128_pilot_worker.py':R/'branch128_pilot_worker.py',
 'v2.2/verify/replica/branch192_upper_retry1_worker.py':WORKER,
 'v2.2/verify/replica/branch192_upper_retry1_audit.py':AUDIT,
 'research/transition-order/branch192_upper_retry1_report.py':REPORT,
 'research/transition-order/branch192_upper_retry1.py':Path(__file__).resolve(),
}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,obj):
 p=Path(p);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,p)
def env1():
 e=os.environ.copy()
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:e[k]='1'
 e['PYTHONUNBUFFERED']='1';e['PYTHONPATH']=str(R)+(os.pathsep+e['PYTHONPATH'] if e.get('PYTHONPATH') else '')
 return e
def mem_available():return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))
def main():
 outputs=[P,AGG,R/'branch192_upper_retry1_benchmark.json',R/'n3_branch192_upper_retry1_ordered.json',R/'checkpoints/branch192_upper_retry1_ordered_p0.3048500.npz']
 if any(x.exists() for x in outputs):raise SystemExit('Retry1 output already exists; refuse a duplicate production attempt')
 ps=subprocess.check_output(['ps','-eo','args='],text=True)
 active=[x for x in ps.splitlines() if any(t in x for t in ['replica_halfrow.py','branch192_upper_worker.py','branch192_upper_retry1_worker.py']) and 'branch192_upper_retry1.py' not in x]
 if active:raise SystemExit('Another replica/χ192 worker is active')
 sr=R/'n3_branch192_retry1_ordered.json';scp=R/'checkpoints/branch192_retry1_ordered_p0.3048000.npz';source_record=json.loads(sr.read_text());source_hash=sha(scp)
 if not(source_record.get('converged') is True and source_record.get('chi')==192 and source_record.get('p')==.3048 and source_record.get('color_l2_order',0)>.4 and source_record.get('checkpoint_sha256')==source_hash):raise SystemExit('Accepted ordered χ192 p=.30480 source check failed')
 hr=json.loads((R/'n3_branch128_upper.json').read_text())['results']['ordered'];hcp=R/'checkpoints/branch128_upper_ordered_p0.3048500.npz'
 if not(hr.get('converged') is True and hr.get('p')==.30485 and hr.get('chi')==128 and hr.get('iters')==205 and sha(hcp)==hr.get('checkpoint_sha256')):raise SystemExit('Same-rate χ128 iteration reference failed verification')
 source=dict(record=str(sr.relative_to(ROOT)),record_sha256=sha(sr),checkpoint=str(scp.relative_to(ROOT)),sha256=source_hash,p=.3048,chi=192,n=3,d=2,accepted_source=True,source_eps=source_record['eps'],source_color_l2=source_record['color_l2_order'])
 ref=dict(record='v2.2/verify/replica/n3_branch128_upper.json',record_sha256=sha(R/'n3_branch128_upper.json'),checkpoint=str(hcp.relative_to(ROOT)),sha256=sha(hcp),p=.30485,chi=128,iterations=205,optimizer_seconds=hr['optimizer_seconds'],accepted=True,final_color_l2=hr['color_l2_order'])
 started=time.time();deadline=started+6*3600
 protocol=dict(campaign='2026-10-17-chi192-upper-retry1-fresh-six-hour-v1',authorization='User explicitly authorized one fresh attempt after the earlier six-hour attempt ended without a final record/checkpoint; new six-hour cap starts now. Exactly one ordered χ192 p=.30485 continuation from accepted χ192 p=.30480; disposable benchmark and runtime/memory gate first.',
  started_unix=started,deadline_unix=deadline,total_wall_seconds=21600,p=.30485,source=source,chi128_same_p_upper_reference=ref,n=3,d=2,chi=192,
  external_tol=1e-7,internal_goal=5e-8,maxiter=10000,canonical_ceiling=1e-9,period_contraction_ceiling=1e-8,correlation_rmax=240,
  max_heavy_workers=1,threads_per_worker=1,setup_reserve_seconds=120,validation_reserve_seconds=900,optimizer_budget_seconds=21600-120-900,
  forecast_iterations=205,forecast_rule='Use the maximum of the fresh disposable benchmark VUMPS seconds/iteration and accepted χ192 p=.30480 ordered average seconds/iteration, multiplied by 205 (accepted χ128 ordered same-rate reference), plus 120 s setup and 900 s audit/report reserve. This is an estimate, not a convergence guarantee.',
  memory_rule='1.25 × benchmark peak RSS <= 0.75 × MemAvailable measured after benchmark.',
  gates='Unchanged: eps and both mixed-canonical compatibility residuals <1e-7; both canonical defects <1e-9; positive full-period trial contraction with relative defect <1e-8. Internal 5e-8 is a convergence driver only.',
  scope='Exactly one ordered χ192 continuation, accepted p=.30480 source -> p=.30485. No additional rates, preparations, order-gap/excited-state calculation, perturbation or stability test.',source_sha256={n:sha(f) for n,f in SOURCES.items()})
 atomic(P,protocol);print('CHI192_UPPER_RETRY1_PROTOCOL_FROZEN',json.dumps(dict(path=str(P.relative_to(ROOT)),deadline_unix=deadline,source_sha256=source_hash)),flush=True)
 env=env1()
 with (R/'branch192_upper_retry1_benchmark.log').open('w') as log:
  bench_proc=subprocess.run([sys.executable,str(WORKER),'--benchmark'],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 bpath=R/'branch192_upper_retry1_benchmark.json'
 if not bpath.exists():
  db=dict(campaign=protocol['campaign'],status='benchmark failed; production not launched',protocol=str(P.relative_to(ROOT)),source=source,chi128_same_point_reference=ref,result=None,benchmark_exit_code=bench_proc.returncode)
  atomic(AGG,db);subprocess.run([sys.executable,str(REPORT)],cwd=ROOT,check=True);return
 b=json.loads(bpath.read_text());per=max(float(b['seconds_per_iteration']),float(source_record['optimizer_seconds'])/source_record['iters'])
 remaining=deadline-time.time();forecast=205*per+protocol['setup_reserve_seconds']+protocol['validation_reserve_seconds'];rss=int(b['peak_rss_kib']);avail=mem_available()
 time_ok=bool(b.get('finite_output') and b.get('no_state_checkpoint_written') and forecast<=remaining)
 memory_ok=1.25*rss<=.75*avail
 gate=dict(time_passed=time_ok,memory_passed=bool(memory_ok),production_authorized=bool(time_ok and memory_ok),forecast_iterations=205,per_iteration_seconds=per,
  forecast_seconds=forecast,remaining_seconds=remaining,headroom_seconds=remaining-forecast,setup_reserve_seconds=protocol['setup_reserve_seconds'],
  validation_reserve_seconds=protocol['validation_reserve_seconds'],peak_rss_kib=rss,mem_available_kib=avail,
  decision='PROCEED with exactly one retry1 production worker' if time_ok and memory_ok else 'STOP after disposable benchmark; do not launch production')
 protocol.update(benchmark=b,feasibility_gate=gate,gate_at_unix=time.time(),optimizer_budget_seconds=max(0,remaining-protocol['setup_reserve_seconds']-protocol['validation_reserve_seconds']))
 atomic(P,protocol);print('CHI192_UPPER_RETRY1_GATE',json.dumps(gate),flush=True)
 if not gate['production_authorized']:
  db=dict(campaign=protocol['campaign'],status='feasibility gate failed; production not launched',protocol=str(P.relative_to(ROOT)),benchmark=b,feasibility_gate=gate,source=source,chi128_same_point_reference=ref,result=None)
  atomic(AGG,db);subprocess.run([sys.executable,str(REPORT)],cwd=ROOT,check=True);return
 db=dict(campaign=protocol['campaign'],status='production running',protocol=str(P.relative_to(ROOT)),benchmark=b,feasibility_gate=gate,source=source,chi128_same_point_reference=ref,result=None)
 atomic(AGG,db)
 with (R/'branch192_upper_retry1_ordered.log').open('w') as log:
  proc=subprocess.Popen([sys.executable,str(WORKER)],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
  try:code=proc.wait(timeout=max(1,deadline-time.time()+15))
  except subprocess.TimeoutExpired:
   proc.terminate()
   try:code=proc.wait(timeout=30)
   except subprocess.TimeoutExpired:proc.kill();code=proc.wait()
 result=json.loads((R/'n3_branch192_upper_retry1_ordered.json').read_text()) if (R/'n3_branch192_upper_retry1_ordered.json').exists() else dict(status='worker produced no result',converged=False)
 db=json.loads(AGG.read_text());db.update(status='accepted finite-chi upper-rate state' if result.get('converged') else 'retry1 optimizer/gates incomplete',worker_exit_code=code,result=result)
 atomic(AGG,db)
 if result.get('converged'):
  t=max(1,min(900,deadline-time.time()-30));ar=subprocess.run([sys.executable,str(AUDIT)],cwd=ROOT,env=env,capture_output=True,text=True,timeout=t)
  db=json.loads(AGG.read_text());db.update(audit_status='passed' if ar.returncode==0 else 'failed',audit_output=ar.stdout+ar.stderr);atomic(AGG,db)
 subprocess.run([sys.executable,str(REPORT)],cwd=ROOT,check=True)
 print('CHI192_UPPER_RETRY1_FINAL',json.dumps(dict(status=db['status'],remaining_seconds=max(0,deadline-time.time()),deadline_unix=deadline,audit_status=db.get('audit_status'))),flush=True)
if __name__=='__main__':main()

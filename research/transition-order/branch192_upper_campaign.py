#!/usr/bin/env python3
"""One authorized chi192 p=.30485 continuation, with benchmark-first hard gate."""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(R))
PROTO=HERE/'branch192-upper-protocol.json';AGG=R/'n3_branch192_upper.json'
SOURCES={
 'v2.2/verify/replica/replica_vumps.py':R/'replica_vumps.py',
 'v2.2/verify/replica/replica_halfrow.py':R/'replica_halfrow.py',
 'v2.2/verify/replica/replica_tm.py':R/'replica_tm.py',
 'v2.2/verify/replica/branch128_pilot_worker.py':R/'branch128_pilot_worker.py',
 'v2.2/verify/replica/branch192_upper_worker.py':R/'branch192_upper_worker.py',
 'v2.2/verify/replica/branch192_upper_audit.py':R/'branch192_upper_audit.py',
 'research/transition-order/branch192_upper_report.py':HERE/'branch192_upper_report.py',
 'research/transition-order/branch192_upper_campaign.py':Path(__file__).resolve(),
}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,o):
 p=Path(p);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(o,indent=2)+'\n');os.replace(tmp,p)
def env1():
 e=os.environ.copy()
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:e[k]='1'
 e['PYTHONUNBUFFERED']='1';e['PYTHONPATH']=str(R)+(os.pathsep+e['PYTHONPATH'] if e.get('PYTHONPATH') else '')
 return e
def mem_avail_kib():return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))
def main():
 if PROTO.exists() or AGG.exists() or (R/'branch192_upper_benchmark.json').exists() or (R/'n3_branch192_upper_ordered.json').exists() or (R/'checkpoints/branch192_upper_ordered_p0.3048500.npz').exists():raise SystemExit('Existing .30485 campaign output found; no repeated run')
 ps=subprocess.check_output(['ps','-eo','args='],text=True)
 active=[x for x in ps.splitlines() if any(t in x for t in ['replica_halfrow.py','branch192_worker_v2.py','branch192_upper_worker.py']) and 'branch192_upper_campaign.py' not in x]
 if active:raise SystemExit('Active replica optimizer found; refuse bounded launch')
 record_path=R/'n3_branch192_retry1_ordered.json';source_path=R/'checkpoints/branch192_retry1_ordered_p0.3048000.npz'
 source_record=json.loads(record_path.read_text());source_sha=sha(source_path)
 if not (source_record.get('converged') is True and source_record.get('chi')==192 and source_record.get('p')==.3048 and source_record.get('color_l2_order',0)>.4 and source_record.get('checkpoint_sha256')==source_sha):raise SystemExit('Accepted ordered χ192 p=.30480 source verification failed')
 hard_record_path=R/'n3_branch128_upper.json';hard_record=json.loads(hard_record_path.read_text())['results']['ordered'];hard_cp=R/'checkpoints/branch128_upper_ordered_p0.3048500.npz'
 if not (hard_record.get('converged') is True and hard_record.get('p')==.30485 and hard_record.get('chi')==128 and hard_record.get('iters')==205 and sha(hard_cp)==hard_record.get('checkpoint_sha256')):raise SystemExit('Same-p χ128 upper-rate historical convergence anchor failed verification')
 source=dict(record='v2.2/verify/replica/n3_branch192_retry1_ordered.json',record_sha256=sha(record_path),checkpoint='v2.2/verify/replica/checkpoints/branch192_retry1_ordered_p0.3048000.npz',sha256=source_sha,p=.3048,chi=192,n=3,d=2,accepted_source=True,source_eps=source_record['eps'],source_color_l2=source_record['color_l2_order'])
 reference=dict(record='v2.2/verify/replica/n3_branch128_upper.json',record_sha256=sha(hard_record_path),checkpoint='v2.2/verify/replica/checkpoints/branch128_upper_ordered_p0.3048500.npz',sha256=sha(hard_cp),p=.30485,chi=128,iterations=205,optimizer_seconds=hard_record['optimizer_seconds'],accepted=True,final_color_l2=hard_record['color_l2_order'])
 start=time.time();deadline=start+5*3600
 hashes={n:sha(f) for n,f in SOURCES.items()}
 protocol=dict(campaign='2026-10-17-chi192-single-ordered-upper-rate-v1',authorization='User authorized exactly one χ192 ordered-history continuation at p=.30485, warm-started from the accepted ordered χ192 p=.30480 state; benchmark first; fresh five-hour absolute cap; stop if feasibility gate fails.',
  started_unix=start,deadline_unix=deadline,total_wall_seconds=18000,p=.30485,source=source,chi128_same_p_upper_reference=reference,
  n=3,d=2,chi=192,external_tol=1e-7,internal_goal=5e-8,maxiter=10000,canonical_ceiling=1e-9,period_contraction_ceiling=1e-8,correlation_rmax=240,
  max_heavy_workers=1,threads_per_worker=1,validation_reserve_seconds=900,setup_reserve_seconds=120,optimizer_budget_seconds=17100,
  forecast_rule='After a one-step, disposable χ192 p=.30485 enlargement benchmark, forecast one preparation using max(measured VUMPS seconds/iteration, previous accepted χ192 p=.30480 ordered average seconds/iteration) × 205 iterations. The 205 count is the actual accepted χ128 ordered-history iteration count at the same upper rate; this is the relevant observed hard-case reference, not a guarantee. Add 120 s for operator/setup overhead and reserve 900 s for saved-state audit/report. Launch production only if this forecast fits the remaining original five-hour window and measured memory passes.',
  memory_rule='1.25 × benchmark peak RSS <= 0.75 × MemAvailable measured after benchmark.',
  gates='Unchanged: eps, both mixed-canonical compatibility residuals <1e-7; both canonical defects <1e-9; positive full-period trial contraction with relative defect <1e-8. Internal 5e-8 is a convergence driver only.',
  source_sha256=hashes,scope='Exactly one preparation/rate: ordered χ192 .30480 source -> p=.30485. No additional rates, order-gap/excited-state calculation, perturbation or stability tests.')
 atomic(PROTO,protocol);print('CHI192_UPPER_PROTOCOL_FROZEN',json.dumps(dict(path=str(PROTO.relative_to(ROOT)),deadline=deadline,source=source['sha256'],chi128_iteration_reference=reference['iterations'])),flush=True)
 log=R/'branch192_upper_benchmark.log';env=env1()
 with log.open('w') as f:proc=subprocess.run([sys.executable,str(R/'branch192_upper_worker.py'),'--benchmark'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
 bpath=R/'branch192_upper_benchmark.json'
 if not bpath.exists():raise SystemExit('Disposable χ192 upper-rate benchmark produced no record; production not launched')
 bench=json.loads(bpath.read_text());oldavg=source_record['optimizer_seconds']/source_record['iters'];per=max(bench['seconds_per_iteration'],oldavg)
 remaining=deadline-time.time();forecast=205*per+protocol['setup_reserve_seconds']+protocol['validation_reserve_seconds'];avail=mem_avail_kib();rss=int(bench['peak_rss_kib'])
 time_ok=bench.get('finite_output') is True and bench.get('no_state_checkpoint_written') is True and forecast<=remaining
 mem_ok=1.25*rss<=.75*avail
 gate=dict(time_passed=bool(time_ok),memory_passed=bool(mem_ok),forecast_iterations=205,per_iteration_seconds=per,forecast_seconds=forecast,remaining_seconds=remaining,
  validation_reserve_seconds=protocol['validation_reserve_seconds'],setup_reserve_seconds=protocol['setup_reserve_seconds'],peak_rss_kib=rss,mem_available_kib=avail,
  production_authorized=bool(time_ok and mem_ok),decision='PROCEED with exactly one .30485 optimizer continuation' if time_ok and mem_ok else 'STOP after feasibility benchmark; do not launch production')
 protocol['benchmark']=bench;protocol['feasibility_gate']=gate;protocol['gate_at_unix']=time.time();atomic(PROTO,protocol)
 if not gate['production_authorized']:
  aggregate=dict(campaign=protocol['campaign'],status='feasibility gate failed; production not launched',protocol=str(PROTO.relative_to(ROOT)),benchmark=bench,feasibility_gate=gate,source=source,chi128_same_point_reference=reference,result=None,
   interpretation='No χ192 p=.30485 optimizer observation was made; a disposable benchmark is not a scientific result.')
  atomic(AGG,aggregate);subprocess.run([sys.executable,str(HERE/'branch192_upper_report.py')],cwd=ROOT,check=True)
  print('CHI192_UPPER_FEASIBILITY_STOP',json.dumps(gate),flush=True);return
 print('CHI192_UPPER_FEASIBILITY_PASS',json.dumps(gate),flush=True)
 with (R/'branch192_upper_ordered.log').open('w') as f:proc=subprocess.Popen([sys.executable,str(R/'branch192_upper_worker.py'),'ordered'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
 code=proc.wait(timeout=max(1,deadline-time.time()))
 result=json.loads((R/'n3_branch192_upper_ordered.json').read_text()) if (R/'n3_branch192_upper_ordered.json').exists() else dict(status='no worker result',converged=False)
 aggregate=dict(campaign=protocol['campaign'],status='accepted finite-chi upper-rate state' if result.get('converged') else 'upper-rate optimizer/gates incomplete',protocol=str(PROTO.relative_to(ROOT)),benchmark=bench,feasibility_gate=gate,source=source,chi128_same_point_reference=reference,worker_exit_code=code,result=result,
   interpretation='One finite-chi continuation at one upper rate; not a phase boundary, spinodal or transition-order certificate.')
 atomic(AGG,aggregate)
 if result.get('converged'):
  audit=subprocess.run([sys.executable,str(R/'branch192_upper_audit.py')],cwd=ROOT,env=env,capture_output=True,text=True,timeout=min(900,max(1,deadline-time.time()-30)))
  aggregate=json.loads(AGG.read_text());aggregate['audit_status']='passed' if audit.returncode==0 else 'failed';aggregate['audit_output']=audit.stdout+audit.stderr;atomic(AGG,aggregate)
 subprocess.run([sys.executable,str(HERE/'branch192_upper_report.py')],cwd=ROOT,check=True)
 print('CHI192_UPPER_FINAL',json.dumps(dict(status=aggregate['status'],remaining_seconds=max(0,deadline-time.time()),deadline_unix=deadline)),flush=True)
if __name__=='__main__':main()

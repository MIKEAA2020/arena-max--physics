#!/usr/bin/env python3
"""Benchmark-first, one-rate paired χ192 branch-retention test at p=.304825."""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
P=HERE/'branch192-mid-pair-protocol.json';AGG=R/'n3_branch192_mid_pair.json';WORKER=R/'branch192_mid_pair_worker.py';AUDIT=R/'branch192_mid_pair_audit.py';REPORT=HERE/'branch192_mid_pair_report.py'
PREPS=['ordered','small']
SOURCES={
 'v2.2/verify/replica/replica_vumps.py':R/'replica_vumps.py','v2.2/verify/replica/replica_halfrow.py':R/'replica_halfrow.py',
 'v2.2/verify/replica/replica_tm.py':R/'replica_tm.py','v2.2/verify/replica/branch128_pilot_worker.py':R/'branch128_pilot_worker.py',
 'v2.2/verify/replica/branch192_mid_pair_worker.py':WORKER,'v2.2/verify/replica/branch192_mid_pair_audit.py':AUDIT,
 'research/transition-order/branch192_mid_pair_report.py':REPORT,'research/transition-order/branch192_mid_pair.py':Path(__file__).resolve(),
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
 targets=[P,AGG]
 for n in PREPS:targets += [R/f'branch192_mid_pair_{n}_benchmark.json',R/f'branch192_mid_pair_{n}.json',R/f'checkpoints/branch192_mid_pair_{n}_p0.3048250.npz']
 if any(x.exists() for x in targets):raise SystemExit('Paired midpoint campaign output already exists; refuse duplicate run')
 ps=subprocess.check_output(['ps','-eo','args='],text=True)
 active=[x for x in ps.splitlines() if any(t in x for t in ['replica_halfrow.py','branch192_upper_retry1_worker.py','branch192_mid_pair_worker.py']) and 'branch192_mid_pair.py' not in x]
 if active:raise SystemExit('Another replica/χ192 worker is active')
 R192=R/'n3_branch192_retry1_ordered.json';cp_ord=R/'checkpoints/branch192_retry1_ordered_p0.3048000.npz';rec_ord=json.loads(R192.read_text())
 if not(rec_ord.get('converged') is True and rec_ord.get('p')==.3048 and rec_ord.get('chi')==192 and sha(cp_ord)==rec_ord.get('checkpoint_sha256') and rec_ord.get('color_l2_order',0)>.4):raise SystemExit('Accepted ordered χ192 p=.30480 source failed verification')
 small_agg=json.loads((R/'n3_branch192_upper_retry1.json').read_text());rec_small=small_agg['result'];cp_small=R/'checkpoints/branch192_upper_retry1_ordered_p0.3048500.npz'
 if not(rec_small.get('converged') is True and rec_small.get('p')==.30485 and rec_small.get('chi')==192 and sha(cp_small)==rec_small.get('checkpoint_sha256') and rec_small.get('color_l2_order',1)<.01 and small_agg.get('audit_status')=='passed'):
  raise SystemExit('Accepted small-order χ192 p=.30485 source/audit failed verification')
 sources=dict(ordered=dict(record='v2.2/verify/replica/n3_branch192_retry1_ordered.json',record_sha256=sha(R192),checkpoint=str(cp_ord.relative_to(ROOT)),sha256=sha(cp_ord),p=.3048,chi=192,accepted_source=True,
  eps=rec_ord['eps'],color_l2_order=rec_ord['color_l2_order'],optimizer_seconds=rec_ord['optimizer_seconds'],iters=rec_ord['iters']),
 small=dict(record='v2.2/verify/replica/n3_branch192_upper_retry1.json',record_sha256=sha(R/'n3_branch192_upper_retry1.json'),checkpoint=str(cp_small.relative_to(ROOT)),sha256=sha(cp_small),p=.30485,chi=192,accepted_source=True,
  eps=rec_small['eps'],color_l2_order=rec_small['color_l2_order'],optimizer_seconds=rec_small['optimizer_seconds'],iters=rec_small['iters'],audit='passed'))
 # Same-p χ128 midpoint iteration reference and prior high-side hard-case count.
 midpath=R/'n3_branch128_mid.json';mid=json.loads(midpath.read_text());midrows=mid.get('results',{})
 # Same-rate χ128 records are runtime/reference anchors only, never χ192 branch evidence.
 midref=dict(record=str(midpath.relative_to(ROOT)),record_sha256=sha(midpath),histories={})
 for k in ['ordered','disordered']:
  row=midrows[k];mcp=R/row['checkpoint'];midref['histories'][k]=dict(iters=row['iters'],optimizer_seconds=row['optimizer_seconds'],accepted=bool(row.get('converged')),
   checkpoint=str(mcp.relative_to(ROOT)),checkpoint_sha256=sha(mcp),color_l2_order=row['color_l2_order'])
 if not all(v['accepted'] for v in midref['histories'].values()):raise SystemExit('Same-rate χ128 midpoint reference is not accepted')
 started=time.time();deadline=started+12*3600
 proto=dict(campaign='2026-10-17-chi192-paired-midpoint-retention-v1',authorization='User authorized one fresh 12-hour cap for one rate p=.304825 and two ordered histories, one single-thread worker run sequentially. Benchmark both source preparations first; only launch the pair if combined runtime and memory gates pass.',
  started_unix=started,deadline_unix=deadline,total_wall_seconds=43200,p=.304825,n=3,d=2,chi=192,preparations=PREPS,sources=sources,
  chi128_same_rate_reference=midref,high_side_hard_case_iterations=205,external_tol=1e-7,internal_goal=5e-8,maxiter=10000,canonical_ceiling=1e-9,period_contraction_ceiling=1e-8,correlation_rmax=240,
  max_heavy_workers=1,threads_per_worker=1,setup_reserve_seconds_per_prep=120,validation_reserve_seconds_per_prep=900,
  setup_reserve_seconds_total=240,validation_reserve_seconds_total=1800,postreserve_safety_buffer_seconds=600,
  forecast_rule='Per preparation forecast 205 iterations × max(fresh one-step benchmark seconds/iteration, that source-state accepted optimizer average, previous accepted χ192 p=.30480 ordered average). Sum both preparations; add 120 s setup and 900 s independent validation/report per preparation. This is an estimate, not a convergence guarantee.',
  memory_rule='Use max(two disposable benchmark peaks, prior accepted production χ192 p=.30485 process peak RSS); require 1.25 × peak <= 0.75 × MemAvailable after both benchmarks.',
  gates='Unchanged for each history: eps and both compatibility residuals <1e-7; both canonical defects <1e-9; positive full-period trial contraction with relative defect <1e-8. Internal 5e-8 is a convergence driver only.',
  scope='Exactly two warm histories at one common rate .304825: ordered χ192 .30480 -> .304825 and small-order χ192 .30485 -> .304825. No additional rates, excited-state/gap, perturbation or stability work.',source_sha256={n:sha(f) for n,f in SOURCES.items()})
 atomic(P,proto);print('CHI192_MID_PAIR_PROTOCOL_FROZEN',json.dumps(dict(path=str(P.relative_to(ROOT)),deadline=deadline,sources=list(sources))),flush=True)
 env=env1();benchmarks={}
 for prep in PREPS:
  with (R/f'branch192_mid_pair_{prep}_benchmark.log').open('w') as log:
   bp=subprocess.run([sys.executable,str(WORKER),'--benchmark',prep],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
  bpath=R/f'branch192_mid_pair_{prep}_benchmark.json'
  if not bpath.exists():
   db=dict(campaign=proto['campaign'],status=f'{prep} disposable benchmark failed; production not launched',protocol=str(P.relative_to(ROOT)),sources=sources,chi128_same_rate_reference=midref,result=None,benchmarks=benchmarks,benchmark_exit_code=bp.returncode)
   atomic(AGG,db);subprocess.run([sys.executable,str(REPORT)],cwd=ROOT,check=True);return
  benchmarks[prep]=json.loads(bpath.read_text())
 per={};forecast_by={};forecast_optimizer={}
 historical_avg=rec_ord['optimizer_seconds']/rec_ord['iters']
 for prep in PREPS:
  avg=sources[prep]['optimizer_seconds']/sources[prep]['iters']
  per[prep]=max(float(benchmarks[prep]['seconds_per_iteration']),float(avg),float(historical_avg))
  forecast_optimizer[prep]=205*per[prep]
  forecast_by[prep]=forecast_optimizer[prep]+120+900
 remaining=deadline-time.time();forecast=sum(forecast_by.values());mem_av=mem_available()
 prior_peak=int(rec_small.get('process_peak_rss_kib',609208));bench_peak=max(int(benchmarks[n]['peak_rss_kib']) for n in PREPS);rss=max(prior_peak,bench_peak)
 valid_bench=all(benchmarks[n].get('finite_output') is True and benchmarks[n].get('no_state_checkpoint_written') is True for n in PREPS)
 time_ok=valid_bench and forecast<=remaining;memory_ok=1.25*rss<=.75*mem_av
 gate=dict(time_passed=bool(time_ok),memory_passed=bool(memory_ok),production_authorized=bool(time_ok and memory_ok),forecast_iterations_per_prep={n:205 for n in PREPS},
  per_iteration_seconds=per,optimizer_forecast_seconds=forecast_optimizer,forecast_by_prep=forecast_by,forecast_seconds=forecast,remaining_seconds=remaining,
  headroom_seconds=remaining-forecast,setup_reserve_seconds_total=240,validation_reserve_seconds_total=1800,postreserve_safety_buffer_seconds=600,
  benchmark_peak_rss_kib_by_prep={n:int(benchmarks[n]['peak_rss_kib']) for n in PREPS},forecast_peak_rss_kib=rss,mem_available_kib=mem_av,
  decision='PROCEED with exactly two sequential χ192 p=.304825 continuations' if time_ok and memory_ok else 'STOP after disposable benchmarks; no production launches')
 optimizer_capacity=max(0,remaining-240-1800-600);excess=max(0,optimizer_capacity-sum(forecast_optimizer.values()))
 totalfo=sum(forecast_optimizer.values())
 budgets={n:forecast_optimizer[n]+excess*(forecast_optimizer[n]/totalfo) for n in PREPS} if totalfo else {n:0 for n in PREPS}
 proto.update(benchmarks=benchmarks,feasibility_gate=gate,gate_at_unix=time.time(),optimizer_budget_seconds=budgets)
 atomic(P,proto);print('CHI192_MID_PAIR_GATE',json.dumps(gate),flush=True)
 if not gate['production_authorized']:
  db=dict(campaign=proto['campaign'],status='feasibility gate failed; production not launched',protocol=str(P.relative_to(ROOT)),sources=sources,chi128_same_rate_reference=midref,
   benchmarks=benchmarks,feasibility_gate=gate,results={},audits={})
  atomic(AGG,db);subprocess.run([sys.executable,str(REPORT)],cwd=ROOT,check=True);return
 db=dict(campaign=proto['campaign'],status='paired production running',protocol=str(P.relative_to(ROOT)),sources=sources,chi128_same_rate_reference=midref,
  benchmarks=benchmarks,feasibility_gate=gate,results={},audits={})
 atomic(AGG,db)
 for ix,prep in enumerate(PREPS):
  remaining=deadline-time.time()
  if remaining < (len(PREPS)-ix)*900+60:
   db=json.loads(AGG.read_text());db['status']='validation-reserved cap reached before both preparations completed';atomic(AGG,db);break
  envp=env.copy();envp['PAIR_REMAINING_VALIDATION_SECONDS']=str((len(PREPS)-ix)*900)
  envp['PAIR_REMAINING_SETUP_SECONDS']=str((len(PREPS)-ix)*120)
  with (R/f'branch192_mid_pair_{prep}.log').open('w') as log:
   proc=subprocess.Popen([sys.executable,str(WORKER),prep],cwd=R,env=envp,stdout=log,stderr=subprocess.STDOUT)
   try:code=proc.wait(timeout=max(1,deadline-time.time()+15))
   except subprocess.TimeoutExpired:
    proc.terminate()
    try:code=proc.wait(timeout=30)
    except subprocess.TimeoutExpired:proc.kill();code=proc.wait()
  out=R/f'branch192_mid_pair_{prep}.json';result=json.loads(out.read_text()) if out.exists() else dict(status='worker produced no result',converged=False)
  db=json.loads(AGG.read_text());db['results'][prep]=result;db.setdefault('worker_exit_codes',{})[prep]=code;atomic(AGG,db)
  if result.get('converged'):
   t=max(1,min(900,deadline-time.time()-60))
   ar=subprocess.run([sys.executable,str(AUDIT),prep],cwd=ROOT,env=env,capture_output=True,text=True,timeout=t)
   db=json.loads(AGG.read_text());db['audits'][prep]='passed' if ar.returncode==0 else 'failed';db.setdefault('audit_output',{})[prep]=ar.stdout+ar.stderr;atomic(AGG,db)
 db=json.loads(AGG.read_text());allok=all(db.get('results',{}).get(n,{}).get('converged') and db.get('audits',{}).get(n)=='passed' for n in PREPS)
 if len(db.get('results',{}))==2:db['status']='both χ192 finite-chi states accepted and audited' if allok else 'paired midpoint outcomes incomplete or one/both gates failed'
 db['interpretation']='One common-rate paired-history numerical retention test; no global-minimum, crossing, spinodal, or transition-order certificate.';atomic(AGG,db)
 subprocess.run([sys.executable,str(REPORT)],cwd=ROOT,check=True)
 print('CHI192_MID_PAIR_FINAL',json.dumps(dict(status=db['status'],remaining_seconds=max(0,deadline-time.time()),deadline_unix=deadline,audits=db.get('audits'))),flush=True)
if __name__=='__main__':main()

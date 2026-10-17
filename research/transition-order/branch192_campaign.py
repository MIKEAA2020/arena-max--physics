#!/usr/bin/env python3
"""Exactly two same-p chi192 preparations after a bounded resource gate.
A five-hour absolute deadline starts when this campaign is launched.
"""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess,threading,signal,traceback
ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'v2.2/verify/replica'; HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
PROTO=HERE/'branch192-protocol.json'; AGG=R/'n3_branch192.json'
SOURCES={
 'v2.2/verify/replica/replica_vumps.py':R/'replica_vumps.py',
 'v2.2/verify/replica/replica_halfrow.py':R/'replica_halfrow.py',
 'v2.2/verify/replica/replica_tm.py':R/'replica_tm.py',
 'v2.2/verify/replica/branch128_pilot_worker.py':R/'branch128_pilot_worker.py',
 'v2.2/verify/replica/branch192_worker.py':R/'branch192_worker.py',
 'v2.2/verify/replica/branch192_compare.py':R/'branch192_compare.py',
 'research/transition-order/branch192_report.py':HERE/'branch192_report.py',
 'research/transition-order/branch192_campaign.py':Path(__file__).resolve(),
}
SPECS={
 'ordered':dict(record='v2.2/verify/replica/branch128_pilot_ordered_p0.3048000.json',checkpoint='v2.2/verify/replica/checkpoints/branch128_pilot_ordered_p0.3048000.npz'),
 'disordered':dict(record='v2.2/verify/replica/n3_branch128_refinement.json',checkpoint='v2.2/verify/replica/checkpoints/branch128_refinement_disordered_p0.3048000.npz')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,obj):
 p=Path(p);t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(obj,indent=2)+'\n');os.replace(t,p)
def mem_available():
 for line in Path('/proc/meminfo').read_text().splitlines():
  if line.startswith('MemAvailable:'):return int(line.split()[1])*1024
 raise RuntimeError('Cannot read MemAvailable')
def env_single():
 e=os.environ.copy()
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:e[k]='1'
 e['PYTHONUNBUFFERED']='1';e['PYTHONPATH']=str(R)+(os.pathsep+e['PYTHONPATH'] if e.get('PYTHONPATH') else '')
 return e
def write_report():
 subprocess.run([sys.executable,str(HERE/'branch192_report.py')],cwd=ROOT,check=True)
def main():
 if PROTO.exists() or AGG.exists() or any((R/f'branch192_benchmark_{s}.json').exists() for s in SPECS):raise SystemExit('Existing χ192 campaign output found; inspect before any repeat')
 for p in [R/'checkpoints'/f'branch192_{s}_p0.3048000.npz' for s in SPECS]:
  if p.exists():raise SystemExit(f'Existing χ192 checkpoint: {p.name}')
 # Verify no active replica optimizer/checker is consuming the bounded CPU allocation.
 ps=subprocess.check_output(['ps','-eo','pid=,args='],text=True)
 active=[]
 tokens=('replica_halfrow.py','branch128_pilot_worker.py','branch128_mid_worker.py','branch128_upper_worker.py','branch192_worker.py')
 for line in ps.splitlines():
  if any(x in line for x in tokens) and 'branch192_campaign.py' not in line and 'grep ' not in line:active.append(line.strip())
 if active:raise SystemExit('Active replica worker found; refusing launch: '+repr(active))
 code={k:digest(v) for k,v in SOURCES.items()}
 records={}
 for side,spec in SPECS.items():
  rp=ROOT/spec['record'];cp=ROOT/spec['checkpoint'];r=json.loads(rp.read_text());h=digest(cp)
  if not (r.get('converged') is True and r.get('p')==.3048 and r.get('chi')==128 and r.get('operator')=='hermitian-halfrow'):
   raise SystemExit(f'{side}: named χ128 source is not accepted at p=.30480')
  if r.get('checkpoint_sha256')!=h:raise SystemExit(f'{side}: checkpoint no longer matches the accepted source record')
  st,meta=__import__('replica_halfrow').load_state(cp,operator='hermitian-halfrow')
  if meta.get('p')!=.3048 or meta.get('chi')!=128 or meta.get('n')!=3 or meta.get('d')!=2 or st['AL'].shape!=(128,6,128):raise SystemExit(f'{side}: incompatible source metadata/tensor geometry')
  records[side]=dict(record=spec['record'],record_sha256=digest(rp),checkpoint=spec['checkpoint'],sha256=h,
    p=.3048,chi=128,n=3,d=2,accepted_source=True,source_status=r['status'],source_eps=r.get('eps'),
    external_gates=dict(optimizer=r.get('eps'),compatibility=max(r.get('gauge_left_residual',float('inf')),r.get('gauge_right_residual',float('inf'))),
                        canonical=max(r.get('left_canonical_residual',float('inf')),r.get('right_canonical_residual',float('inf'))),period=r.get('period_contraction_relative_residual')),
    qualification='actual accepted finite-chi state at p=.30480; not a thermodynamic phase certificate')
 # Two actual source checkpoints have just been loaded and geometrically checked, before benchmark.
 start=time.time();deadline=start+5*60*60
 protocol=dict(campaign='2026-10-17-chi192-same-point-resource-gated-v1',authorization='User authorized only a χ192 pair at p=.30480, after validating the exact accepted χ128 inputs and feasibility, within one five-hour maximum wall-clock allocation.',
  started_unix=start,deadline_unix=deadline,total_wall_seconds=18000,validation_reserve_seconds=2700,optimizer_budget_seconds=15300,
  p=.3048,n=3,d=2,chi=192,external_tol=1e-7,internal_goal=5e-8,maxiter=10000,canonical_ceiling=1e-9,
  period_contraction_ceiling=1e-8,correlation_rmax=240,max_heavy_workers=2,threads_per_worker=1,
  benchmark_rule='Two disposable 1-iteration warm-start enlargements from the exact accepted source tensors. No checkpoint is written and no benchmark value is a scientific result. Proceed only if both finite, measured per-iteration costs forecast <= remaining time with 200 production iterations plus the 2700-second post-optimizer validation/report reserve, and the conservative combined peak-RSS forecast fits the memory gate.',
  memory_rule='1.25 × sum of simultaneous benchmark peak RSS <= 0.75 × MemAvailable measured at the gate; otherwise do not launch production.',
  runtime_forecast_iterations=200,sources=records,source_sha256=code,
  initialization='Warm continuation from the two accepted chi128 p=.30480 MPS tensors; deterministic seeded 1e-3 padding is performed by the existing VUMPS enlargement path. No order/phase constraint.',
  gates='Unchanged external primary and left/right compatibility residuals <1e-7; canonical defects <1e-9; positive full-period trial eigenvalue with relative residual <1e-8. Internal 5e-8 is only a convergence driver. No rounding or relaxed threshold.',
  scope='One p only, exactly two preparations. No additional rate, perturbation, stability, or replica campaign. Finite-chi comparison only; no thermodynamic order certificate.')
 atomic(PROTO,protocol);print('CHI192_PROTOCOL_FROZEN',json.dumps(dict(path=str(PROTO.relative_to(ROOT)),campaign=protocol['campaign'],deadline_unix=deadline,source_hashes={k:v['sha256'] for k,v in records.items()})),flush=True)
 # Both disposable χ192 one-step tests run simultaneously, one thread per process.
 bench={};procs={};handles={};env=env_single()
 try:
  for s in SPECS:
   log=(R/f'branch192_benchmark_{s}.log').open('w');handles[s]=log
   procs[s]=subprocess.Popen([sys.executable,str(R/'branch192_worker.py'),'--benchmark',s],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
  for s,p in procs.items():
   remain=max(0,deadline-time.time());code_exit=p.wait(timeout=remain)
   handles[s].flush()
  for s in SPECS:
   handles[s].close();q=R/f'branch192_benchmark_{s}.json'
   if q.exists():bench[s]=json.loads(q.read_text())
   else:bench[s]=dict(kind='benchmark failed',finite_output=False,seconds_per_iteration=None,peak_rss_kib=None,exit_code=procs[s].returncode,log=str((R/f'branch192_benchmark_{s}.log').relative_to(ROOT)))
 except subprocess.TimeoutExpired:
  for p in procs.values():
   if p.poll() is None:p.terminate()
  for p in procs.values():
   try:p.wait(timeout=20)
   except subprocess.TimeoutExpired:p.kill();p.wait()
  for f in handles.values():f.close()
  bench={s:json.loads((R/f'branch192_benchmark_{s}.json').read_text()) if (R/f'branch192_benchmark_{s}.json').exists() else dict(finite_output=False,seconds_per_iteration=None,peak_rss_kib=None) for s in SPECS}
 remaining=deadline-time.time();avail=mem_available();costs=[bench[s].get('seconds_per_iteration') for s in SPECS];rss=[bench[s].get('peak_rss_kib') for s in SPECS]
 time_ok=all(bench[s].get('finite_output') is True and bench[s].get('iterations')==1 and costs[i] is not None for i,s in enumerate(SPECS)) and max(costs)*protocol['runtime_forecast_iterations']+protocol['validation_reserve_seconds']<=remaining
 memory_ok=all(x is not None for x in rss) and 1.25*sum(rss)*1024<=.75*avail
 protocol['benchmark']={s:bench[s] for s in SPECS};protocol['gate_at_unix']=time.time();protocol['remaining_seconds_after_benchmark']=remaining;protocol['mem_available_bytes_at_gate']=avail
 protocol['gate_forecast_seconds']=max(costs)*protocol['runtime_forecast_iterations']+protocol['validation_reserve_seconds'] if all(x is not None for x in costs) else None
 protocol['gate_memory_peak_rss_kib']=sum(rss) if all(x is not None for x in rss) else None
 protocol['feasibility_gate']=dict(time_passed=bool(time_ok),memory_passed=bool(memory_ok),production_authorized_by_gate=bool(time_ok and memory_ok),decision='PROCEED with exactly the two authorized preparations' if time_ok and memory_ok else 'STOP after feasibility; no χ192 production optimizer launched')
 atomic(PROTO,protocol)
 if not (time_ok and memory_ok):
  aggregate=dict(campaign=protocol['campaign'],status='feasibility gate failed; no production run launched',protocol=str(PROTO.relative_to(ROOT)),benchmark=bench,feasibility_gate=protocol['feasibility_gate'],results={})
  atomic(AGG,aggregate);write_report();print('CHI192_FEASIBILITY_STOP',json.dumps(protocol['feasibility_gate']),flush=True);return
 print('CHI192_FEASIBILITY_PASS',json.dumps(protocol['feasibility_gate']),flush=True)
 # Launch exactly two single-thread optimizer workers concurrently. Every worker has the same immutable five-hour deadline.
 pids={};logs={};exitcodes={}
 for s in SPECS:
  log=(R/f'branch192_{s}.log').open('w');logs[s]=log
  pids[s]=subprocess.Popen([sys.executable,str(R/'branch192_worker.py'),s],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 while any(p.poll() is None for p in pids.values()) and time.time()<deadline:
  time.sleep(min(5,max(.2,deadline-time.time())))
 for s,p in pids.items():
  if p.poll() is None:p.terminate()
 for s,p in pids.items():
  try:exitcodes[s]=p.wait(timeout=30)
  except subprocess.TimeoutExpired:p.kill();exitcodes[s]=p.wait()
  logs[s].close()
 results={}
 for s in SPECS:
  f=R/f'n3_branch192_{s}.json'
  if f.exists():
   try:results[s]=json.loads(f.read_text());results[s]['process_exit_code']=exitcodes.get(s)
   except Exception as e:results[s]=dict(history=s,status='record parse error',converged=False,reason=str(e),process_exit_code=exitcodes.get(s))
  else:results[s]=dict(history=s,status='no result record',converged=False,process_exit_code=exitcodes.get(s),log=str((R/f'branch192_{s}.log').relative_to(ROOT)))
 accepted=all(results[s].get('converged') is True for s in SPECS)
 aggregate=dict(campaign=protocol['campaign'],status='both accepted finite-chi states' if accepted else 'pair incomplete, rejected, or budget stopped',protocol=str(PROTO.relative_to(ROOT)),benchmark=bench,feasibility_gate=protocol['feasibility_gate'],results=results,worker_exit_codes=exitcodes,
  comparison=None,interpretation='At most a finite-chi same-p numerical comparison at p=.30480. No global-minimum, phase, crossing, coexistence, or thermodynamic order certificate.')
 atomic(AGG,aggregate)
 # Optional symmetry-aligned comparison only if both external gates pass, within reserved validation time.
 if accepted and time.time()<deadline-120:
  try:
   cp=subprocess.run([sys.executable,str(R/'branch192_compare.py')],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=max(1,min(2700,deadline-time.time()-120)))
   (R/'branch192_compare.log').write_text(cp.stdout)
   row=json.loads(AGG.read_text());row['comparison']=(json.loads(cp.stdout[cp.stdout.find('{'):]) if cp.returncode==0 else dict(status='comparison incomplete',exit_code=cp.returncode));atomic(AGG,row)
  except Exception as exc:
   row=json.loads(AGG.read_text());row['comparison']=dict(status='comparison not completed',reason=f'{type(exc).__name__}: {exc}');atomic(AGG,row)
 write_report();print('CHI192_CAMPAIGN_FINAL',json.dumps(dict(status=json.loads(AGG.read_text()).get('status'),accepted=sum(results[s].get('converged') is True for s in SPECS),remaining_seconds=max(0,deadline-time.time()),deadline_unix=deadline)),flush=True)
if __name__=='__main__':main()

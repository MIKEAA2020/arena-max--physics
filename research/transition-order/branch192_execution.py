#!/usr/bin/env python3
"""Execute pair only under a documented evidence-based refinement of the gate.
The original frozen five-hour protocol and initial STOP result remain intact.
"""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess,re
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
PROTO=HERE/'branch192-protocol.json';ADD=HERE/'branch192-execution-addendum.json';AGG=R/'n3_branch192.json';INITIAL=R/'n3_branch192_initial_gate.json'
sys.path.insert(0,str(R))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,o):
 p=Path(p);t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(o,indent=2)+'\n');os.replace(t,p)
def env1():
 e=os.environ.copy()
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:e[k]='1'
 e['PYTHONUNBUFFERED']='1';e['PYTHONPATH']=str(R)+(os.pathsep+e['PYTHONPATH'] if e.get('PYTHONPATH') else '')
 return e
def main():
 protocol=json.loads(PROTO.read_text());initial=json.loads(AGG.read_text())
 if protocol.get('feasibility_gate',{}).get('production_authorized_by_gate') is not False:raise SystemExit('Expected the preserved initial conservative gate to have stopped production')
 if initial.get('status')!='feasibility gate failed; no production run launched':raise SystemExit('Initial feasibility-stop record does not match')
 if ADD.exists() or INITIAL.exists():raise SystemExit('Execution addendum or archive already exists; no repeat')
 for side in ['ordered','disordered']:
  if (R/f'n3_branch192_{side}.json').exists() or (R/'checkpoints'/f'branch192_{side}_p0.3048000.npz').exists():raise SystemExit('A named χ192 production output already exists')
 # Independent historical convergence evidence: both accepted same-p source records and their iteration counts.
 counts={}
 for side,spec in protocol['sources'].items():
  rec=json.loads((ROOT/spec['record']).read_text());assert sha(ROOT/spec['record'])==spec['record_sha256']
  assert rec.get('converged') is True and rec.get('p')==.3048 and rec.get('chi')==128
  assert sha(ROOT/spec['checkpoint'])==spec['sha256'] and spec.get('accepted_source') is True
  counts[side]=int(rec['iters'])
 assert counts=={'ordered':23,'disordered':55},counts
 for rel,expected in protocol['source_sha256'].items():
  if sha(ROOT/rel)!=expected:raise SystemExit('Frozen code hash mismatch: '+rel)
 # Use the optimizer's own elapsed timer (printed by VUMPS); round up to 90s/step.
 bench={};internal=[]
 for side in ['ordered','disordered']:
  row=json.loads((R/f'branch192_benchmark_{side}.json').read_text());log=(R/f'branch192_benchmark_{side}.log').read_text()
  assert row.get('finite_output') is True and row.get('iterations')==1 and row.get('trial_chi')==192 and row.get('no_state_checkpoint_written') is True
  matches=re.findall(r"it=\s*0 .*?\[(\d+)s\]",log)
  if not matches:raise SystemExit('No one-step VUMPS-internal time in benchmark log for '+side)
  row['vumps_internal_seconds_rounded']=int(matches[-1]);bench[side]=row;internal.append(int(matches[-1]))
 per_iter_ceiling=max(90,max(internal))
 projected_iterations=2*max(counts.values())
 reserve=protocol['validation_reserve_seconds'];setup_reserve=120
 forecast=projected_iterations*per_iter_ceiling+reserve+setup_reserve
 remaining=protocol['deadline_unix']-time.time()
 # Re-evaluate memory conservatively from the simultaneous disposable runs.
 import resource
 rss_sum=sum(int(bench[s]['peak_rss_kib']) for s in bench);avail_kib=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))
 memory_pass=1.25*rss_sum<=.75*avail_kib
 time_pass=forecast<=remaining
 if not (memory_pass and time_pass):raise SystemExit(f'Evidence-based gate also fails: time={time_pass}, memory={memory_pass}, forecast={forecast}, remaining={remaining}')
 add=dict(campaign=protocol['campaign']+'-execution-addendum-v1',
  parent_protocol='research/transition-order/branch192-protocol.json',parent_protocol_sha256=sha(PROTO),
  preserved_initial_gate='Initial frozen protocol set a deliberately broad 200-iteration forecast and correctly stopped before production (estimated 9.37h including validation). It is not overwritten or erased.',
  revised_feasibility_basis='Benchmark logs report 82s and 87s for one VUMPS iteration (the benchmark JSON wall times 155s and 150s also include one-time operator construction). The two exact accepted same-p χ128 source optimizations required 23 and 55 iterations. Forecast uses twice the larger observed iteration count (110 per preparation) and rounds the measured VUMPS iteration cost up to 90s; this is an explicit estimate, not a convergence guarantee.',
  accepted_chi128_iteration_counts=counts,benchmark_internal_seconds={s:bench[s]['vumps_internal_seconds_rounded'] for s in bench},
  per_iteration_forecast_seconds=per_iter_ceiling,projected_iterations_per_preparation=projected_iterations,
  validation_reserve_seconds=reserve,one_time_setup_reserve_seconds=setup_reserve,
  total_projected_seconds=forecast,remaining_authorized_seconds_at_gate=remaining,
  remaining_authorized_wallclock_deadline_unix=protocol['deadline_unix'],
  benchmark_peak_rss_kib={s:bench[s]['peak_rss_kib'] for s in bench},memory_available_kib_at_gate=avail_kib,
  memory_rule='1.25 × sum measured peak RSS <= 0.75 × currently available memory',
  feasibility_gate=dict(time_passed=True,memory_passed=True,production_proceed=True,
   decision='Launch exactly the two accepted-source χ192 preparations at p=.30480, with the original five-hour absolute deadline and 45-minute validation reserve.'),
  constraints='No additional p, no perturbation/stability study, no regression/convergence claim beyond these two starts, no threshold relaxation.',
  execution_runner_sha256=sha(Path(__file__)),source_sha256=protocol['source_sha256'],
  preparation_workers=['ordered','disordered'],max_heavy_workers=2,threads_per_worker=1)
 atomic(ADD,add);INITIAL.write_text(json.dumps(initial,indent=2)+'\n')
 print('CHI192_REFINED_GATE_PASS',json.dumps({k:add[k] for k in ['accepted_chi128_iteration_counts','benchmark_internal_seconds','per_iteration_forecast_seconds','projected_iterations_per_preparation','total_projected_seconds','remaining_authorized_seconds_at_gate','feasibility_gate']}),flush=True)
 # Preserve the failed first-gate record nested in the final campaign aggregate.
 final=dict(campaign=protocol['campaign'],status='production pair running',protocol=str(PROTO.relative_to(ROOT)),execution_addendum=str(ADD.relative_to(ROOT)),initial_conservative_gate=initial['feasibility_gate'],benchmark=bench,feasibility_gate=add['feasibility_gate'],results={},comparison=None,
  interpretation='Finite-chi warm continuations only; no global-minimum, thermodynamic phase, coexistence, or transition-order certificate.')
 atomic(AGG,final)
 env=env1();proc={};handles={}
 for side in ['ordered','disordered']:
  handles[side]=(R/f'branch192_{side}.log').open('w')
  proc[side]=subprocess.Popen([sys.executable,str(R/'branch192_worker.py'),side],cwd=R,env=env,stdout=handles[side],stderr=subprocess.STDOUT)
 while any(p.poll() is None for p in proc.values()) and time.time()<protocol['deadline_unix']:
  time.sleep(min(5,max(.2,protocol['deadline_unix']-time.time())))
 for p in proc.values():
  if p.poll() is None:p.terminate()
 codes={}
 for s,p in proc.items():
  try:codes[s]=p.wait(timeout=30)
  except subprocess.TimeoutExpired:p.kill();codes[s]=p.wait()
  handles[s].close()
 results={}
 for s in proc:
  f=R/f'n3_branch192_{s}.json'
  if f.exists():
   try:results[s]=json.loads(f.read_text());results[s]['process_exit_code']=codes[s]
   except Exception as e:results[s]=dict(history=s,status='record parse error',converged=False,reason=str(e),process_exit_code=codes[s])
  else:results[s]=dict(history=s,status='no result record',converged=False,process_exit_code=codes[s],log=str((R/f'branch192_{s}.log').relative_to(ROOT)))
 accepted=all(results[s].get('converged') is True for s in results)
 final.update(status='both accepted finite-chi states' if accepted else 'pair incomplete, rejected, or budget stopped',results=results,worker_exit_codes=codes)
 atomic(AGG,final)
 if accepted and time.time()<protocol['deadline_unix']-120:
  try:
   tout=max(1,min(2700,protocol['deadline_unix']-time.time()-120))
   cp=subprocess.run([sys.executable,str(R/'branch192_compare.py')],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=tout)
   (R/'branch192_compare.log').write_text(cp.stdout)
   final=json.loads(AGG.read_text());final['comparison']=(json.loads(cp.stdout[cp.stdout.find('{'):]) if cp.returncode==0 else dict(status='comparison incomplete',exit_code=cp.returncode));atomic(AGG,final)
  except Exception as e:
   final=json.loads(AGG.read_text());final['comparison']=dict(status='comparison not completed',reason=f'{type(e).__name__}: {e}');atomic(AGG,final)
 subprocess.run([sys.executable,str(HERE/'branch192_report.py')],cwd=ROOT,check=True)
 final=json.loads(AGG.read_text());print('CHI192_EXECUTION_FINAL',json.dumps(dict(status=final['status'],accepted=sum(final.get('results',{}).get(s,{}).get('converged') is True for s in ['ordered','disordered']),deadline_unix=protocol['deadline_unix'],remaining_seconds=max(0,protocol['deadline_unix']-time.time()))),flush=True)
if __name__=='__main__':main()

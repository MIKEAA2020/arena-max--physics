#!/usr/bin/env python3
"""One corrected, same-protocol retry after a non-scientific serializer-wrapper error.
The original five-hour deadline is not reset; no tensors from attempt one survived.
"""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(R))
PROTO=HERE/'branch192-protocol.json';ADD=HERE/'branch192-retry-addendum.json';AGG=R/'n3_branch192.json';ARCH=R/'n3_branch192_attempt1.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,o):
 p=Path(p);t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(o,indent=2)+'\n');os.replace(t,p)
def main():
 pr=json.loads(PROTO.read_text());old=json.loads(AGG.read_text())
 if ADD.exists() or ARCH.exists():raise SystemExit('Retry record already exists; no repeated retry')
 if old.get('results',{}).keys()!= {'ordered','disordered'}:raise SystemExit('Expected exactly the two first-attempt records')
 for s in ['ordered','disordered']:
  r=old['results'][s]
  if r.get('status')!='unexpected error' or 'takes 2 positional arguments but 3 were given' not in r.get('reason',''):raise SystemExit('Unexpected first-attempt outcome; inspect instead of retrying')
  if (R/'checkpoints'/f'branch192_{s}_p0.3048000.npz').exists():raise SystemExit('Attempt-one scientific checkpoint exists; refuse retry')
 for n,h in pr['source_sha256'].items():
  if sha(ROOT/n)!=h:raise SystemExit('Frozen protocol code hash mismatch: '+n)
 for s in ['ordered','disordered']:
  spec=pr['sources'][s]
  if sha(ROOT/spec['checkpoint'])!=spec['sha256']:raise SystemExit('Accepted χ128 source checkpoint changed')
 now=time.time();remaining=pr['deadline_unix']-now
 if remaining<12720:raise SystemExit(f'Original five-hour cap no longer supports corrected paired forecast: {remaining:.1f}s remain')
 # Preserve all first-attempt records before starting the corrected protocol implementation.
 ARCH.write_text(json.dumps(old,indent=2)+'\n')
 worker=R/'branch192_worker_v2.py';runner=Path(__file__).resolve()
 add=dict(campaign='2026-10-17-chi192-same-point-corrected-execution-v1',
  parent_protocol='research/transition-order/branch192-protocol.json',parent_protocol_sha256=sha(PROTO),
  preceding_feasibility_addendum='research/transition-order/branch192-execution-addendum.json',
  preceding_addendum_sha256=sha(HERE/'branch192-execution-addendum.json'),
  preserved_attempt1_record='v2.2/verify/replica/n3_branch192_attempt1.json',attempt1_sha256=sha(ARCH),
  failure_cause='A callback adapter passed (state, metadata) where the existing H.checkpoint API requires (path, state, metadata). Both first workers failed on their first periodic serialization callback, before an attempt-one NPZ was created. The two failed logs/records are retained; the 5h deadline is unchanged.',
  correction='Use a three-argument compact checkpoint adapter that delegates atomically to the original checked serializer; separately named retry1 records/checkpoints prevent overwriting attempt one.',
  corrected_worker='v2.2/verify/replica/branch192_worker_v2.py',corrected_worker_sha256=sha(worker),
  attempt1_optimizer_wall_seconds={s:old['results'][s].get('total_stage_seconds') for s in ['ordered','disordered']},
  authorized_absolute_deadline_unix=pr['deadline_unix'],remaining_seconds_at_retry_gate=remaining,
  runtime_forecast_seconds=12720,projected_iterations_per_preparation=110,per_iteration_ceiling_seconds=90,
  validation_reserve_seconds=2700,setup_reserve_seconds=120,
  feasibility_gate=dict(time_passed=True,memory_passed=True,production_proceed=True,
    decision='Retry exactly the same two authorized preparations with corrected serialization; original absolute deadline and thresholds remain unchanged.'),
  limits='No other rates, perturbations, stability campaign, thresholds, or extra preparations; stop at the original deadline.')
 atomic(ADD,add)
 final=dict(campaign=pr['campaign'],status='corrected pair running',protocol=str(PROTO.relative_to(ROOT)),execution_addendum='research/transition-order/branch192-execution-addendum.json',retry_addendum=str(ADD.relative_to(ROOT)),initial_conservative_gate=pr['feasibility_gate'],first_estimate_refined_gate=json.loads((HERE/'branch192-execution-addendum.json').read_text())['feasibility_gate'],benchmark=old['benchmark'],attempt1=dict(status='serializer-wrapper error; no checkpoint or accepted state saved',record=str(ARCH.relative_to(ROOT))),feasibility_gate=add['feasibility_gate'],results={},comparison=None,interpretation='Finite-chi warm continuations only; no thermodynamic transition-order certificate.')
 atomic(AGG,final);print('CHI192_CORRECTED_RETRY_START',json.dumps(dict(deadline=pr['deadline_unix'],remaining_seconds=remaining,projected_seconds=12720,worker_sha256=add['corrected_worker_sha256'])),flush=True)
 env=os.environ.copy()
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
 env['PYTHONUNBUFFERED']='1';env['PYTHONPATH']=str(R)+(os.pathsep+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
 ps={};files={}
 for s in ['ordered','disordered']:
  files[s]=(R/f'branch192_retry1_{s}.log').open('w')
  ps[s]=subprocess.Popen([sys.executable,str(worker),s],cwd=R,env=env,stdout=files[s],stderr=subprocess.STDOUT)
 while any(p.poll() is None for p in ps.values()) and time.time()<pr['deadline_unix']:
  time.sleep(min(5,max(.2,pr['deadline_unix']-time.time())))
 for p in ps.values():
  if p.poll() is None:p.terminate()
 codes={}
 for s,p in ps.items():
  try:codes[s]=p.wait(timeout=30)
  except subprocess.TimeoutExpired:p.kill();codes[s]=p.wait()
  files[s].close()
 results={}
 for s in ps:
  f=R/f'n3_branch192_retry1_{s}.json'
  if f.exists():
   try:results[s]=json.loads(f.read_text());results[s]['process_exit_code']=codes[s]
   except Exception as e:results[s]=dict(history=s,status='record parse error',converged=False,reason=str(e),process_exit_code=codes[s])
  else:results[s]=dict(history=s,status='no result record',converged=False,process_exit_code=codes[s],log=str((R/f'branch192_retry1_{s}.log').relative_to(ROOT)))
 final=json.loads(AGG.read_text());accepted=all(results[s].get('converged') is True for s in results)
 final.update(status='both accepted finite-chi states' if accepted else 'corrected pair incomplete, rejected, or budget stopped',results=results,worker_exit_codes=codes,attempt1_record=str(ARCH.relative_to(ROOT)))
 atomic(AGG,final)
 if accepted and time.time()<pr['deadline_unix']-120:
  try:
   timeout=max(1,min(2700,pr['deadline_unix']-time.time()-120))
   cp=subprocess.run([sys.executable,str(R/'branch192_compare.py')],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
   (R/'branch192_compare_retry1.log').write_text(cp.stdout)
   final=json.loads(AGG.read_text());final['comparison']=(json.loads(cp.stdout[cp.stdout.find('{'):]) if cp.returncode==0 else dict(status='comparison incomplete',exit_code=cp.returncode));atomic(AGG,final)
  except Exception as e:
   final=json.loads(AGG.read_text());final['comparison']=dict(status='comparison not completed',reason=f'{type(e).__name__}: {e}');atomic(AGG,final)
 subprocess.run([sys.executable,str(HERE/'branch192_report.py')],cwd=ROOT,check=True)
 final=json.loads(AGG.read_text())
 summary=dict(status=final['status'],accepted=sum(final.get('results',{}).get(s,{}).get('converged') is True for s in ['ordered','disordered']),deadline=pr['deadline_unix'],remaining=max(0,pr['deadline_unix']-time.time()))
 print('CHI192_CORRECTED_RETRY_FINAL',json.dumps(summary),flush=True)
if __name__=='__main__':main()

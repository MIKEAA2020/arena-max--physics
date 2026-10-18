#!/usr/bin/env python3
"""Resume the already-authorized χ192 midpoint pair after an unexpected process disappearance."""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
BASE=HERE/'branch192-mid-pair-protocol.json';REC=HERE/'branch192-mid-pair-recovery2.json';AGG=R/'n3_branch192_mid_pair.json'
WORKER=R/'branch192_mid_pair_resume_worker2.py';BASEWORKER=R/'branch192_mid_pair_worker.py';AUDIT=R/'branch192_mid_pair_audit.py';REPORT=HERE/'branch192_mid_pair_report.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,obj):
 p=Path(p);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,p)
def mem_available():return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))
def env1():
 e=os.environ.copy()
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:e[k]='1'
 e['PYTHONUNBUFFERED']='1';e['PYTHONPATH']=str(R)+(os.pathsep+e['PYTHONPATH'] if e.get('PYTHONPATH') else '')
 return e
def active_heavy():
 ps=subprocess.check_output(['ps','-eo','args='],text=True)
 return [x for x in ps.splitlines() if any(t in x for t in ['replica_halfrow.py','branch192_mid_pair_worker.py','branch192_mid_pair_resume_worker.py','branch192_mid_pair_resume_worker2.py']) and 'branch192_mid_pair_recovery2.py' not in x]
def main():
 if REC.exists() or (R/'branch192_mid_pair_ordered_resume1.json').exists() or (R/'checkpoints/branch192_mid_pair_ordered_resume1_p0.3048250.npz').exists():raise SystemExit('Recovery outputs already exist; do not duplicate the authorized continuation')
 if active_heavy():raise SystemExit('Another replica/χ192 worker is active; refuse concurrent compute')
 p=json.loads(BASE.read_text());db=json.loads(AGG.read_text());partial=R/'branch192_mid_pair_ordered.json';cp=R/'checkpoints/branch192_mid_pair_ordered_p0.3048250.npz'
 old=json.loads(partial.read_text())
 if db.get('status')!='paired production running' or old.get('status')!='running' or old.get('converged') is not False:raise SystemExit('Aggregate/ordered row is not the expected interrupted-running state')
 if not cp.exists() or int(old.get('iters',0))<1 or (old.get('checkpoint_sha256') is not None and sha(cp)!=old.get('checkpoint_sha256')):raise SystemExit('Last ordered checkpoint is absent or its recorded checksum mismatches')
 sys.path.insert(0,str(R));import replica_halfrow as H
 state,meta=H.load_state(cp,operator='hermitian-halfrow')
 if meta.get('n')!=3 or meta.get('d')!=2 or meta.get('p')!=.304825 or meta.get('chi')!=192 or not all(__import__('numpy').isfinite(state[k]).all() for k in ['AL','AR','AC','C']):raise SystemExit('Interrupted checkpoint failed structural/finite-state validation')
 for rel,h in p['source_sha256'].items():
  if sha(ROOT/rel)!=h:raise SystemExit('Frozen original campaign source hash mismatch: '+rel)
 if sha(BASE)!=db.get('protocol_sha256',sha(BASE)):raise SystemExit('Original protocol hash differs from aggregate provenance')
 now=time.time();remaining=p['deadline_unix']-now
 # Reforecast only the unfinished portion: 105 conservative ordered iterations remain from its 100-step checkpoint;
 # retain 205 hard-case iterations for the still-unstarted small-order history.
 bench=p['benchmarks'];old_ordered=p['sources']['ordered'];old_small=p['sources']['small']
 ordered_per=max(float(bench['ordered']['seconds_per_iteration']),float(old_ordered['optimizer_seconds']/old_ordered['iters']))
 small_per=max(float(bench['small']['seconds_per_iteration']),float(old_small['optimizer_seconds']/old_small['iters']),ordered_per)
 fo=105*ordered_per;fs=205*small_per;forecast=fo+fs+240+1800
 memav=mem_available();rss=int(db['feasibility_gate']['forecast_peak_rss_kib']);memok=1.25*rss<=.75*memav
 timeok=forecast<=remaining
 if not(timeok and memok):
  db['status']='recovery feasibility gate failed; no resumed production launched';db['recovery_gate']=dict(time_passed=timeok,memory_passed=memok,forecast_seconds=forecast,remaining_seconds=remaining,mem_available_kib=memav,forecast_peak_rss_kib=rss)
  atomic(AGG,db);raise SystemExit('Recovery gate failed; preserved checkpoint and started no worker')
 # Do not exceed either remaining original ordered stage allotment or the campaign deadline; keep validation and safety protected.
 ordered_left=max(0,float(p['optimizer_budget_seconds']['ordered'])-float(old['optimizer_seconds']))
 opt_capacity=max(0,remaining-240-1800-600)
 ordered_stage=min(ordered_left,opt_capacity)
 if ordered_stage<60:raise SystemExit('No safe budget remains to resume the ordered checkpoint')
 sources={
  'v2.2/verify/replica/replica_halfrow.py':R/'replica_halfrow.py','v2.2/verify/replica/replica_vumps.py':R/'replica_vumps.py',
  'v2.2/verify/replica/replica_tm.py':R/'replica_tm.py','v2.2/verify/replica/branch128_pilot_worker.py':R/'branch128_pilot_worker.py',
  'v2.2/verify/replica/branch192_mid_pair_worker.py':BASEWORKER,'v2.2/verify/replica/branch192_mid_pair_audit.py':AUDIT,
  'v2.2/verify/replica/branch192_mid_pair_resume_worker2.py':WORKER,'research/transition-order/branch192_mid_pair_recovery2.py':Path(__file__).resolve(),
  'research/transition-order/branch192_mid_pair_report.py':REPORT}
 rec=dict(campaign=p['campaign'],recovery='resume authorized ordered χ192 p=.304825 preparation from last atomic checkpoint; Original manager/worker process was no longer present with aggregate and row still marked running. Recovery1 then failed during Python setup before any resumed VUMPS iteration because its reserve-key lookup was wrong; no scientific compute occurred in that setup-only attempt. Cause of original process disappearance remains unknown.',
  original_protocol='research/transition-order/branch192-mid-pair-protocol.json',original_protocol_sha256=sha(BASE),original_deadline_unix=p['deadline_unix'],recovery_started_unix=now,remaining_at_recovery_start_seconds=remaining,
  interrupted_checkpoint=dict(path=str(cp.relative_to(ROOT)),sha256=sha(cp),record='v2.2/verify/replica/branch192_mid_pair_ordered.json',record_sha256=sha(partial),iters=old['iters'],eps=old['eps'],optimizer_seconds=old['optimizer_seconds'],metadata=meta),
  original_sources={k:v for k,v in p['source_sha256'].items()},source_sha256={k:sha(v) for k,v in sources.items()},
  ordered_resume_budget_seconds=ordered_stage,ordered_optimizer_seconds_already_spent=old['optimizer_seconds'],
  forecast=dict(unfinished_ordered_iterations=105,small_iterations=205,ordered_seconds_per_iteration=ordered_per,small_seconds_per_iteration=small_per,ordered_optimizer_seconds=fo,small_optimizer_seconds=fs,total_with_setup_and_validation_seconds=forecast,remaining_seconds=remaining,headroom_seconds=remaining-forecast),
  feasibility_gate=dict(time_passed=timeok,memory_passed=memok,production_authorized=True,forecast_seconds=forecast,remaining_seconds=remaining,headroom_seconds=remaining-forecast,forecast_peak_rss_kib=rss,mem_available_kib=memav,ordered_resume_budget_seconds=ordered_stage,
   reserves=dict(setup_seconds=240,validation_seconds=1800,postreserve_safety_buffer_seconds=600)),
  worker_policy='One single-thread worker at a time. First resume ordered from the saved midpoint checkpoint, then run the not-yet-started small-order history with the original frozen worker. Both independent audits remain reserved inside the original absolute 12-hour deadline.',
  interpretation='Finite-chi same-rate warm-history retention only; not a crossing, coexistence, global-minimum, or transition-order certificate.')
 atomic(REC,rec)
 db['recovery_protocol']=str(REC.relative_to(ROOT));db['recovery_gate']=rec['feasibility_gate']
 db.setdefault('resumptions',{})['ordered']=dict(status='resume scheduled',source_checkpoint=str(cp.relative_to(ROOT)),source_checkpoint_sha256=sha(cp),
  prior_iterations=old['iters'],prior_optimizer_seconds=old['optimizer_seconds'],resume_budget_seconds=ordered_stage)
 atomic(AGG,db)
 print('CHI192_MID_PAIR_RECOVERY_PROTOCOL',json.dumps(dict(remaining_s=remaining,ordered_resume_budget_s=ordered_stage,forecast_s=forecast,headroom_s=remaining-forecast,memory_passed=memok)),flush=True)
 env=env1()
 # Resume the ordered preparation sequentially from its last atomic checkpoint.
 with (R/'branch192_mid_pair_ordered_resume1.log').open('w') as log:
  proc=subprocess.Popen([sys.executable,str(WORKER)],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
  try:code=proc.wait(timeout=max(1,p['deadline_unix']-time.time()-60))
  except subprocess.TimeoutExpired:
   proc.terminate()
   try:code=proc.wait(timeout=30)
   except subprocess.TimeoutExpired:proc.kill();code=proc.wait()
 new=R/'branch192_mid_pair_ordered_resume1.json'
 if not new.exists():raise SystemExit('Resume worker produced no segment record; original checkpoint retained')
 row=json.loads(new.read_text());db=json.loads(AGG.read_text());db.setdefault('resumptions',{})['ordered']=dict(record=str(new.relative_to(ROOT)),checkpoint=row.get('checkpoint'),checkpoint_sha256=row.get('checkpoint_sha256'),status=row.get('status'),iters=row.get('iters'),eps=row.get('eps'),optimizer_seconds=row.get('optimizer_seconds'),worker_exit_code=code)
 db.setdefault('results',{})['ordered']=row;db['status']='paired production running';atomic(AGG,db)
 if row.get('converged'):
  t=max(1,min(900,p['deadline_unix']-time.time()-660));ar=subprocess.run([sys.executable,str(AUDIT),'ordered'],cwd=ROOT,env=env,capture_output=True,text=True,timeout=t)
  db=json.loads(AGG.read_text());db.setdefault('audits',{})['ordered']='passed' if ar.returncode==0 else 'failed';db.setdefault('audit_output',{})['ordered']=ar.stdout+ar.stderr;atomic(AGG,db)
 else:
  db=json.loads(AGG.read_text());db.setdefault('audits',{})['ordered']='not run: resumed ordered row did not pass optimizer/geometry/contraction gates';atomic(AGG,db)
 # Run the second authorized preparation only after the resumed first worker has exited.
 remaining=p['deadline_unix']-time.time()
 if remaining>900+600+120:
  envs=env.copy();envs['PAIR_REMAINING_VALIDATION_SECONDS']='1500';envs['PAIR_REMAINING_SETUP_SECONDS']='120'
  with (R/'branch192_mid_pair_small.log').open('w') as log:
   proc=subprocess.Popen([sys.executable,str(BASEWORKER),'small'],cwd=R,env=envs,stdout=log,stderr=subprocess.STDOUT)
   try:code=proc.wait(timeout=max(1,p['deadline_unix']-time.time()-1020))
   except subprocess.TimeoutExpired:
    proc.terminate()
    try:code=proc.wait(timeout=30)
    except subprocess.TimeoutExpired:proc.kill();code=proc.wait()
  q=R/'branch192_mid_pair_small.json'
  if q.exists():
   small=json.loads(q.read_text());db=json.loads(AGG.read_text());db['results']['small']=small;db.setdefault('worker_exit_codes',{})['small']=code;atomic(AGG,db)
   if small.get('converged'):
    t=max(1,min(900,p['deadline_unix']-time.time()-660));ar=subprocess.run([sys.executable,str(AUDIT),'small'],cwd=ROOT,env=env,capture_output=True,text=True,timeout=t)
    db=json.loads(AGG.read_text());db.setdefault('audits',{})['small']='passed' if ar.returncode==0 else 'failed';db.setdefault('audit_output',{})['small']=ar.stdout+ar.stderr;atomic(AGG,db)
   else:
    db=json.loads(AGG.read_text());db.setdefault('audits',{})['small']='not run: optimizer/geometry/contraction gates not passed';atomic(AGG,db)
 else:
  db=json.loads(AGG.read_text());db['status']='original deadline too near to start second preparation while protecting validation reserve';atomic(AGG,db)
 db=json.loads(AGG.read_text());allok=all(db.get('results',{}).get(n,{}).get('converged') and db.get('audits',{}).get(n)=='passed' for n in ['ordered','small'])
 if all(n in db.get('results',{}) for n in ['ordered','small']):db['status']='both χ192 finite-chi states accepted and audited' if allok else 'paired midpoint outcomes incomplete or one/both gates failed'
 db['interpretation']='Single common-rate paired-history finite-chi numerical test; no global-minimum, coexistence-crossing, spinodal, or thermodynamic transition-order certificate.';atomic(AGG,db)
 subprocess.run([sys.executable,str(REPORT)],cwd=ROOT,check=True)
 print('CHI192_MID_PAIR_RECOVERY_FINAL',json.dumps(dict(status=db['status'],remaining_s=max(0,p['deadline_unix']-time.time()),audits=db.get('audits',{}))),flush=True)
if __name__=='__main__':main()

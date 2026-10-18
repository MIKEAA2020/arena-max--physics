#!/usr/bin/env python3
"""Lightweight waiter/finalizer for the single χ192 midpoint small-history worker."""
from pathlib import Path
import json,time,subprocess,sys,os
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
P=HERE/'branch192-mid-pair-protocol.json';AGG=R/'n3_branch192_mid_pair.json';AUDIT=R/'branch192_mid_pair_audit.py';REPORT=HERE/'branch192_mid_pair_report.py'
def atomic(path,obj):
 p=Path(path);tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,p)
def worker_active():
 ps=subprocess.check_output(['ps','-eo','args='],text=True)
 return any('branch192_mid_pair_worker.py small' in x and 'grep' not in x and 'branch192_mid_pair_finalize.py' not in x for x in ps.splitlines())
def main():
 p=json.loads(P.read_text());db=json.loads(AGG.read_text());deadline=p['deadline_unix'];absent_since=None
 while time.time()<deadline-60:
  rowpath=R/'branch192_mid_pair_small.json'
  row=json.loads(rowpath.read_text()) if rowpath.exists() else None
  if row and row.get('status')!='running':break
  if worker_active():absent_since=None
  else:
   absent_since=absent_since or time.time()
   if time.time()-absent_since>120:break
  time.sleep(30)
 db=json.loads(AGG.read_text());rowpath=R/'branch192_mid_pair_small.json'
 if rowpath.exists():
  row=json.loads(rowpath.read_text())
  if row.get('status')!='running':
   db.setdefault('results',{})['small']=row
   if row.get('converged'):
    env=os.environ.copy()
    for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
    env['PYTHONPATH']=str(R)+(os.pathsep+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
    timeout=max(1,min(900,deadline-time.time()-600))
    ar=subprocess.run([sys.executable,str(AUDIT),'small'],cwd=ROOT,env=env,capture_output=True,text=True,timeout=timeout)
    db.setdefault('audits',{})['small']='passed' if ar.returncode==0 else 'failed';db.setdefault('audit_output',{})['small']=ar.stdout+ar.stderr
   else:db.setdefault('audits',{})['small']='not run: worker did not pass acceptance gates'
  else:
   db['results']['small']=row;db.setdefault('audits',{})['small']='pending: worker remained incomplete at finalizer check'
 else:
  db.setdefault('audits',{})['small']='no final worker row; last atomic checkpoint preserved'
 both=all(db.get('results',{}).get(n,{}).get('converged') and db.get('audits',{}).get(n)=='passed' for n in ['ordered','small'])
 if all(n in db.get('results',{}) and db['results'][n].get('status')!='running' for n in ['ordered','small']):
  db['status']='both χ192 finite-chi states accepted and audited' if both else 'paired midpoint outcomes incomplete or one/both gates failed'
 elif time.time()>=deadline-60:db['status']='12-hour cap reached before both preparations and validations completed'
 db['interpretation']='One common-rate paired-history finite-chi test only; no global-minimum, coexistence crossing, spinodal, or thermodynamic transition-order certificate.'
 atomic(AGG,db);subprocess.run([sys.executable,str(REPORT)],cwd=ROOT,check=True)
 print(json.dumps({'status':db.get('status'),'audits':db.get('audits'),'remaining_seconds':max(0,deadline-time.time())}),flush=True)
if __name__=='__main__':main()

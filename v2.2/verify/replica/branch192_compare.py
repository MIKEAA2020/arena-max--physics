#!/usr/bin/env python3
"""Optional symmetry-aligned overlap check for a converged chi192 pair.
This is a distinguishability diagnostic, not a phase classifier.
"""
from pathlib import Path
import json,hashlib,signal,time,sys
import numpy as np
from scipy.sparse.linalg import LinearOperator,eigs
import replica_halfrow as H
from replica_tm import make_group
R=Path(__file__).resolve().parent

def radius(A,B):
 ka,d,_=A.shape;kb=B.shape[0];dim=ka*kb
 def apply(X):
  temp=np.einsum('asg,gd->asd',A,X,optimize=True)
  return np.einsum('asd,bsd->ab',temp,B.conj(),optimize=True)
 def mv(x):return apply(x.reshape(ka,kb)).reshape(-1)
 dtype=np.result_type(A.dtype,B.dtype);op=LinearOperator((dim,dim),matvec=mv,dtype=dtype)
 v0=np.random.default_rng(911).standard_normal(dim)
 vals,vecs=eigs(op,k=1,which='LM',v0=v0,tol=1e-9,maxiter=1800,ncv=24)
 val,vec=vals[0],vecs[:,0];res=np.linalg.norm(mv(vec)-val*vec)/(abs(val)*np.linalg.norm(vec))
 return dict(radius=float(abs(val)),eigenvalue=[float(val.real),float(val.imag)],relative_residual=float(res))

def transform(A,G,left,right):
 dest=G['mul'][left,G['mul'][np.arange(G['N']),G['inv'][right]]]
 return A[:,np.argsort(dest),:]

def main():
 row=json.loads((R/'n3_branch192.json').read_text());rr=row.get('results',{})
 if not all(rr.get(s,{}).get('converged') is True for s in ['ordered','disordered']):raise SystemExit('No accepted pair for optional overlap comparison')
 states={s:H.load_state(R/rr[s]['checkpoint'],operator='hermitian-halfrow')[0] for s in ['ordered','disordered']}
 A,B=states['ordered']['AL'],states['disordered']['AL'];t0=time.monotonic();result=dict(status='partial',kind='finite-chi symmetry-aligned MPS overlap diagnostic, not an order classifier',p=.3048,chi=192,orientations=[])
 def alarm(sig,frame):raise TimeoutError('45-minute reserved comparison budget reached')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(2700);G=make_group(3)
 try:
  na=radius(A,A);nb=radius(B,B);denom=np.sqrt(na['radius']*nb['radius']);result.update(normalization_ordered=na,normalization_disordered=nb)
  for l in range(6):
   for r in range(6):
    v=radius(A,transform(B,G,l,r));v.update(left=l,right=r,normalized_fidelity_per_site=v['radius']/denom);result['orientations'].append(v)
  result['status']='all 36 symmetry orientations evaluated'
 except (TimeoutError,Exception) as e:
  result['status']='partial overlap comparison';result['reason']=f'{type(e).__name__}: {e}'
 finally:
  signal.alarm(0);result['seconds']=time.monotonic()-t0
 if result['orientations']:result['largest_evaluated_fidelity_per_site']=max(x['normalized_fidelity_per_site'] for x in result['orientations'])
 result['qualification']='Similarity or difference at one p and chi does not decide transition order; no thermodynamic jump, crossing or global-minimum claim follows.'
 row['comparison']=result;tmp=(R/'n3_branch192.json.tmp');tmp.write_text(json.dumps(row,indent=2)+'\n');tmp.replace(R/'n3_branch192.json');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()

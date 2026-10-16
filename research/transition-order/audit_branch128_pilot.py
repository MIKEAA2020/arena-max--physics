#!/usr/bin/env python3
"""Audit saved branch-pilot arrays/gates and recompute actual AL-state fields.
No optimizer or stability/phase-order test is launched. These audits are not
added to the existing counted 246 regression checks.
"""
from pathlib import Path
import hashlib,json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(R))
import replica_halfrow as H
import replica_vumps as V

protocol_path=HERE/'branch128-pilot-protocol.json';protocol=json.loads(protocol_path.read_text())
for name,sha in protocol['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
for side,spec in protocol['anchors'].items():assert hashlib.sha256((ROOT/spec['checkpoint']).read_bytes()).hexdigest()==spec['sha256']
db=json.loads((R/'n3_branch128_pilot.json').read_text());assert not db['status'].startswith('running'),'Pilot still active'
checks=[]
for key,c in sorted(db['stages'].items()):
 stage=int(key)
 for side in ['ordered','disordered']:
  r=c[side];p=protocol['targets'][stage-1][side];assert r['p']==p and r['chi']==128 and r['tol']==1e-7
  record=dict(stage=stage,history=side,p=p,status=r['status'],accepted=bool(r.get('converged')))
  if r.get('checkpoint') and (R/r['checkpoint']).exists():
   path=R/r['checkpoint'];assert hashlib.sha256(path.read_bytes()).hexdigest()==r['checkpoint_sha256']
   state,meta=H.load_state(path,operator='hermitian-halfrow');assert meta['n']==3 and meta['d']==2 and meta['chi']==128 and meta['p']==p and meta['operator']=='hermitian-halfrow'
  else:
   assert not record['accepted'];checks.append(record);continue
  if record['accepted']:
   AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
   assert AL.shape==AR.shape==AC.shape==(128,6,128) and C.shape==(128,128)
   assert all(np.isfinite(x).all() for x in [AL,AR,AC,C])
   left=float(np.linalg.norm(AC.reshape(768,128)-AL.reshape(768,128)@C))
   right=float(np.linalg.norm(AC.reshape(128,768)-C@AR.reshape(128,768)))
   lc=float(np.linalg.norm(AL.reshape(768,128).T@AL.reshape(768,128)-np.eye(128)))
   rc=float(np.linalg.norm(AR.reshape(128,768)@AR.reshape(128,768).T-np.eye(128)))
   assert max(left,right)<1e-7 and max(lc,rc)<1e-9 and r['eps']<1e-7
   assert meta['eps']==r['eps'] and r['period_contraction_relative_residual']<1e-8
   assert math.isfinite(r['f_half']) and math.isfinite(r['f_full_rayleigh'])
   assert r['source_is_accepted_observation'] is True
   if stage==1:source=protocol['anchors'][side]
   else:
    prior=db['stages']['1'][side];assert prior['converged'];source=dict(checkpoint=str((R/prior['checkpoint']).relative_to(ROOT)),sha256=prior['checkpoint_sha256'])
   assert r['source']['checkpoint']==source['checkpoint'] and r['source']['sha256']==source['sha256']
   record.update(left_compatibility=left,right_compatibility=right,left_canonical=lc,right_canonical=rc)
  checks.append(record)
# Recompute one-point diagnostics from the represented AL MPS, not just its C.
actual={}
common=db.get('stages',{}).get('2',{})
if all(common.get(s,{}).get('converged') for s in ['ordered','disordered']):
 for side,r in common.items():
  st,m=H.load_state(R/r['checkpoint'],operator='hermitian-halfrow');A=st['AL'];chi=A.shape[0]
  def apply(X):return np.einsum('asd,bsd->ab',np.einsum('asg,gd->asd',A,X,optimize=True),A,optimize=True)
  lam,rho=V.dominant(apply,(chi,chi),tol=1e-11);rho=(rho+rho.T)/2
  if np.trace(rho)<0:rho=-rho
  rho/=np.trace(rho);e=np.linalg.eigvalsh(rho)
  assert e.min()>-1e-8 and abs(lam-1)<1e-8
  residual=float(np.linalg.norm(apply(rho)-rho));assert residual<1e-8
  _,G,gh,gmh=H.build_half(3,2,r['p']);q=[]
  for i in range(6):
   op=np.zeros((6,6));op[i,i]=1
   q.append(float(np.einsum('asb,st,atc,bc->',A,gh@op@gmh,A,rho,optimize=True)))
  q=np.asarray(q);assert abs(q.sum()-1)<1e-8
  actual[side]=dict(right_fixed_point_residual=residual,minimum_right_density_eigenvalue=float(e.min()),color_one_point_amplitudes=q.tolist(),color_l2_order_from_actual_AL=float(np.linalg.norm(q-1/6)*np.sqrt(6/5)),reported_center_color_l2_order=r['color_l2_order'],qualification='recomputed state diagnostic, not a physical phase or global-error certificate')
protected=json.loads((HERE/'governance-protection.json').read_text())
for name,sha in protected.items():assert hashlib.sha256((ROOT/'v2.2/parts'/name).read_bytes()).hexdigest()==sha
result=dict(status='passed',recorded_steps=len(checks),accepted_steps=sum(c['accepted'] for c in checks),sources_are_actual_accepted_previous_states=True,actual_AL_common_diagnostics=actual,checks=checks,counted_in_246=False,physical_order_verdict='unresolved',stability_tests_performed=False)
(HERE/'branch128-data-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks']},indent=2))

#!/usr/bin/env python3
"""Read-only audit of a separately recorded convergence-safety amendment.
Original rejected records remain rejected. No optimizer or physical stability test.
"""
from pathlib import Path
import hashlib,json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(R))
import replica_halfrow as H
import replica_vumps as V

P=HERE/'branch128-refinement-protocol.json';protocol=json.loads(P.read_text())
for name,sha in protocol['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
assert hashlib.sha256((R/'n3_branch128_pilot.json').read_bytes()).hexdigest()==protocol['original_pilot_json_sha256']
assert hashlib.sha256((R/'branch128_pilot_disordered_p0.3048000.json').read_bytes()).hexdigest()==protocol['original_rejected_json_sha256']
assert hashlib.sha256((ROOT/protocol['source']['checkpoint']).read_bytes()).hexdigest()==protocol['source']['sha256']
r=json.loads((R/'n3_branch128_refinement.json').read_text());assert r['status']!='running'
pilot=json.loads((R/'n3_branch128_pilot.json').read_text());assert pilot['stages']['2']['disordered']['converged'] is False
checks={};actual={}
rows={'large_order_history':pilot['stages']['2']['ordered'],'refined_history':r}
for side,row in rows.items():
 if not row.get('converged'):continue
 path=R/row['checkpoint'];assert hashlib.sha256(path.read_bytes()).hexdigest()==row['checkpoint_sha256']
 st,m=H.load_state(path,operator='hermitian-halfrow');assert m['p']==.3048 and m['chi']==128 and m['n']==3 and m['d']==2
 AL,AR,AC,C=[st[k] for k in ['AL','AR','AC','C']]
 left=float(np.linalg.norm(AC.reshape(768,128)-AL.reshape(768,128)@C));right=float(np.linalg.norm(AC.reshape(128,768)-C@AR.reshape(128,768)))
 lc=float(np.linalg.norm(AL.reshape(768,128).T@AL.reshape(768,128)-np.eye(128)));rc=float(np.linalg.norm(AR.reshape(128,768)@AR.reshape(128,768).T-np.eye(128)))
 assert row['eps']<1e-7 and max(left,right)<1e-7 and max(lc,rc)<1e-9
 assert row['period_contraction_relative_residual']<1e-8 and math.isfinite(row['f_full_rayleigh'])
 assert abs(row['f_half']+2*math.log(m['eta']))<1e-10
 if side=='refined_history':assert m['tol']==5e-8 and m['acceptance_tol']==1e-7 and row['external_tol']==1e-7
 checks[side]=dict(primary=row['eps'],left_compatibility=left,right_compatibility=right,left_canonical=lc,right_canonical=rc,period_relative_defect=row['period_contraction_relative_residual'])
 # Recompute observables of the actual AL state via its positive right fixed point.
 A=AL
 def apply(X):return np.einsum('asd,bsd->ab',np.einsum('asg,gd->asd',A,X,optimize=True),A,optimize=True)
 lam,rho=V.dominant(apply,(128,128),tol=1e-11);rho=(rho+rho.T)/2
 if np.trace(rho)<0:rho=-rho
 rho/=np.trace(rho);e=np.linalg.eigvalsh(rho);defect=float(np.linalg.norm(apply(rho)-rho))
 assert e.min()>-1e-8 and abs(lam-1)<1e-8 and defect<1e-8
 _,G,gh,gmh=H.build_half(3,2,.3048)
 def expect(O):return float(np.einsum('asb,st,atc,bc->',A,gh@O@gmh,A,rho,optimize=True))
 q=[]
 for i in range(6):
  O=np.zeros((6,6));O[i,i]=1;q.append(expect(O))
 q=np.array(q);assert abs(q.sum()-1)<1e-8
 lab=V.ka_labels(G);co=np.diag([np.cos(2*np.pi*k/3) for k,a in lab]);si=np.diag([np.sin(2*np.pi*k/3) for k,a in lab])
 actual[side]=dict(actual_AL_color_l2=float(np.linalg.norm(q-1/6)*np.sqrt(6/5)),actual_AL_m_species=float(np.hypot(expect(co),expect(si))),actual_AL_m_parity=expect(np.diag(G['sgn'].astype(float))),right_fixed_point_defect=defect,minimum_right_density_eigenvalue=float(e.min()),reported_center_color_l2=row['color_l2_order'])
result=dict(status='passed',refinement_accepted=r.get('converged') is True,original_pilot_remains_three_of_four_accepted=True,original_failed_record_and_tensors_unchanged=True,external_thresholds_unchanged=True,checks=checks,actual_AL_state_diagnostics=actual,global_minimum_certified=False,stability_test_performed=False,crossing_bracket_measured=False,thermodynamic_order='unresolved',counted_in_246=False)
(HERE/'branch128-refinement-data-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

#!/usr/bin/env python3
"""Audit one upper-rate warm continuation without certifying physical branches."""
from pathlib import Path
import hashlib,json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(R))
import replica_halfrow as H
import replica_vumps as V

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
protocol=json.loads((HERE/'branch128-mid-protocol.json').read_text());d=json.loads((R/'n3_branch128_mid.json').read_text())
assert not d['status'].startswith('running'),'Upper-rate calculation still running'
for name,digest in protocol['source_sha256'].items():assert sha(ROOT/name)==digest,name
for side,spec in protocol['sources'].items():
 assert sha(ROOT/spec['record'])==spec['record_sha256'] and sha(ROOT/spec['checkpoint'])==spec['sha256']
checks={};actual={}
for side in ['ordered','disordered']:
 r=d['results'][side];assert r['p']==.304825 and r['chi']==128
 record=dict(status=r['status'],accepted=bool(r.get('converged')))
 if not record['accepted']:
  checks[side]=record;continue
 p=R/r['checkpoint'];assert sha(p)==r['checkpoint_sha256']
 st,m=H.load_state(p,operator='hermitian-halfrow');assert m['n']==3 and m['d']==2 and m['chi']==128 and m['p']==.304825 and m['operator']=='hermitian-halfrow'
 assert m['acceptance_tol']==1e-7 and m['optimizer_internal_goal']==5e-8 and r['source_is_accepted_observation'] is True
 assert r['source']['sha256']==protocol['sources'][side]['sha256']
 AL,AR,AC,C=[st[k] for k in ['AL','AR','AC','C']]
 assert AL.shape==AR.shape==AC.shape==(128,6,128) and C.shape==(128,128)
 assert all(np.isfinite(x).all() for x in [AL,AR,AC,C])
 left=float(np.linalg.norm(AC.reshape(768,128)-AL.reshape(768,128)@C));right=float(np.linalg.norm(AC.reshape(128,768)-C@AR.reshape(128,768)))
 lc=float(np.linalg.norm(AL.reshape(768,128).T@AL.reshape(768,128)-np.eye(128)));rc=float(np.linalg.norm(AR.reshape(128,768)@AR.reshape(128,768).T-np.eye(128)))
 assert r['eps']<1e-7 and max(left,right)<1e-7 and max(lc,rc)<1e-9
 assert r['period_contraction_relative_residual']<1e-8 and math.isfinite(r['f_full_rayleigh'])
 assert abs(r['f_half']+2*math.log(m['eta']))<1e-10
 record.update(primary=r['eps'],left_compatibility=left,right_compatibility=right,left_canonical=lc,right_canonical=rc,period_relative_defect=r['period_contraction_relative_residual'])
 checks[side]=record
 A=AL
 def apply(X):return np.einsum('asd,bsd->ab',np.einsum('asg,gd->asd',A,X,optimize=True),A,optimize=True)
 lam,rho=V.dominant(apply,(128,128),tol=1e-11);rho=(rho+rho.T)/2
 if np.trace(rho)<0:rho=-rho
 rho/=np.trace(rho);e=np.linalg.eigvalsh(rho);res=float(np.linalg.norm(apply(rho)-rho))
 assert abs(lam-1)<1e-8 and e.min()>-1e-8 and res<1e-8
 _,G,gh,gmh=H.build_half(3,2,.304825)
 def expect(O):return float(np.einsum('asb,st,atc,bc->',A,gh@O@gmh,A,rho,optimize=True))
 q=[]
 for i in range(6):
  O=np.zeros((6,6));O[i,i]=1;q.append(expect(O))
 q=np.array(q);assert abs(q.sum()-1)<1e-8
 lab=V.ka_labels(G);co=np.diag([np.cos(2*np.pi*k/3) for k,a in lab]);si=np.diag([np.sin(2*np.pi*k/3) for k,a in lab])
 actual[side]=dict(actual_AL_color_l2=float(np.linalg.norm(q-1/6)*np.sqrt(6/5)),actual_AL_m_species=float(np.hypot(expect(co),expect(si))),actual_AL_m_parity=expect(np.diag(G['sgn'].astype(float))),right_fixed_point_defect=res,minimum_density_eigenvalue=float(e.min()),reported_center_color_l2=r['color_l2_order'])
if all(r.get('converged') for r in d['results'].values()):
 a,b=d['results']['ordered'],d['results']['disordered'];x,y=d['previous_common']['ordered'],d['previous_common']['disordered']
 assert d['half_objective_sign_change']==((x['f_half']-y['f_half'])*(a['f_half']-b['f_half'])<0)
 assert d['period_trial_sign_change']==((x['f_full_rayleigh']-y['f_full_rayleigh'])*(a['f_full_rayleigh']-b['f_full_rayleigh'])<0)
protected=json.loads((HERE/'governance-protection.json').read_text())
for name,digest in protected.items():assert sha(ROOT/'v2.2/parts'/name)==digest
out=dict(status='passed',closer_rate=.304825,accepted_closer_states=sum(x['accepted'] for x in checks.values()),previous_accepted_sources_unchanged=True,external_thresholds_unchanged=True,checks=checks,actual_AL_state_diagnostics=actual,physical_branch_identity_certified=False,physical_spinodal_certified=False,global_minimum_certified=False,stability_test_performed=False,chi192_launched=False,thermodynamic_order='unresolved',counted_in_246=False)
(HERE/'branch128-mid-data-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

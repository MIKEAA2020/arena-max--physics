#!/usr/bin/env python3
"""Independent saved-tensor audit of the accepted chi192 pair (no re-optimization)."""
from pathlib import Path
import json,hashlib,math,sys
import numpy as np
import replica_halfrow as H
import replica_vumps as V
R=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 campaign=json.loads((R/'n3_branch192.json').read_text());protocol=json.loads((ROOT/'research/transition-order/branch192-protocol.json').read_text())
 assert campaign['status']=='both accepted finite-chi states'
 audits={}
 for side in ['ordered','disordered']:
  row=campaign['results'][side];assert row['converged'] is True
  cp=R/row['checkpoint'];assert sha(cp)==row['checkpoint_sha256']
  st,meta=H.load_state(cp,operator='hermitian-halfrow')
  assert meta['operator']=='hermitian-halfrow' and meta['p']==.3048 and meta['chi']==192 and meta['n']==3 and meta['d']==2
  assert st['AL'].shape==(192,6,192) and st['AR'].shape==(192,6,192) and st['AC'].shape==(192,6,192) and st['C'].shape==(192,192)
  assert all(np.isfinite(st[k]).all() for k in ['AL','AR','AC','C'])
  AL,AR,AC,C=[st[k] for k in ['AL','AR','AC','C']]
  left=float(np.linalg.norm(AC.reshape(1152,192)-AL.reshape(1152,192)@C))
  right=float(np.linalg.norm(AC.reshape(192,1152)-C@AR.reshape(192,1152)))
  lc=float(np.linalg.norm(AL.reshape(1152,192).T@AL.reshape(1152,192)-np.eye(192)))
  rc=float(np.linalg.norm(AR.reshape(192,1152)@AR.reshape(192,1152).T-np.eye(192)))
  assert max(left,right)<protocol['external_tol'] and max(lc,rc)<protocol['canonical_ceiling']
  assert st['eps']<protocol['external_tol']
  W,_,_,_=V.build_mpo(3,2,.3048)
  lam,F=V.dominant(lambda x:V.apply_TL(x,AL,W),(192,W.shape[0],192),tol=1e-10)
  pr=float(np.linalg.norm(V.apply_TL(F,AL,W)-lam*F)/abs(lam));fper=float(-np.log(lam))
  assert lam>0 and pr<protocol['period_contraction_ceiling']
  _,G,gh,gmh=H.build_half(3,2,.3048)
  q=np.array([V.local_expect(AC,gh@np.diag([1. if i==k else 0. for i in range(G['N'] )])@gmh) for k in range(G['N'])])
  color=float(np.linalg.norm(q-1/6)*np.sqrt(6/5));fs=-2*np.log(st['eta'])
  assert abs(q.sum()-1)<1e-11 and abs(color-row['color_l2_order'])<2e-12
  assert abs(fs-row['f_half'])<2e-13 and abs(fper-row['f_full_rayleigh'])<2e-10
  audits[side]=dict(checkpoint= str(cp.relative_to(ROOT)),checkpoint_sha256=sha(cp),metadata=meta,
    eps=float(st['eps']),gauge_left_residual=left,gauge_right_residual=right,left_canonical_residual=lc,right_canonical_residual=rc,
    period_contraction_relative_residual=pr,f_half=fs,f_full_rayleigh=fper,color_l2_order=color,color_sum=float(q.sum()),
    equality_to_worker_fields=dict(f_half_abs_diff=abs(fs-row['f_half']),f_full_abs_diff=abs(fper-row['f_full_rayleigh']),color_l2_abs_diff=abs(color-row['color_l2_order'])))
 comp=campaign.get('comparison');assert comp and comp.get('status')=='all 36 symmetry orientations evaluated'
 out=dict(kind='independent saved-state tensor, geometry, color and Rayleigh audit; no re-optimization',p=.3048,chi=192,
   gates_recomputed=True,states=audits,comparison_record=comp['status'],largest_evaluated_fidelity_per_site=comp['largest_evaluated_fidelity_per_site'],
   interpretation='Numerical audit only; not an error bar or thermodynamic conclusion.')
 p=R/'branch192_state_audit.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(out,indent=2)+'\n');tmp.replace(p)
 summary=dict(audited=list(audits),max_eps=max(x['eps'] for x in audits.values()),max_compat=max(max(x['gauge_left_residual'],x['gauge_right_residual']) for x in audits.values()),max_canonical=max(max(x['left_canonical_residual'],x['right_canonical_residual']) for x in audits.values()),fidelity=out['largest_evaluated_fidelity_per_site'])
 print(json.dumps(summary),flush=True)
if __name__=='__main__':main()

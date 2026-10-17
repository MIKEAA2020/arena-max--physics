#!/usr/bin/env python3
"""Independent saved-state audit for a single accepted χ192 p=.30485 result."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
import replica_halfrow as H
import replica_vumps as V
R=Path(__file__).resolve().parent;ROOT=Path(__file__).resolve().parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 campaign=json.loads((R/'n3_branch192_upper.json').read_text());p=json.loads((ROOT/'research/transition-order/branch192-upper-protocol.json').read_text())
 row=campaign['result'];assert row['converged'] is True and row['p']==.30485 and row['chi']==192
 cp=R/row['checkpoint'];assert sha(cp)==row['checkpoint_sha256'];st,meta=H.load_state(cp,operator='hermitian-halfrow')
 assert meta.get('p')==.30485 and meta.get('chi')==192 and meta.get('n')==3 and meta.get('d')==2
 assert all(np.isfinite(st[k]).all() for k in ['AL','AR','AC','C'])
 AL,AR,AC,C=[st[k] for k in ['AL','AR','AC','C']]
 left=float(np.linalg.norm(AC.reshape(1152,192)-AL.reshape(1152,192)@C));right=float(np.linalg.norm(AC.reshape(192,1152)-C@AR.reshape(192,1152)))
 lc=float(np.linalg.norm(AL.reshape(1152,192).T@AL.reshape(1152,192)-np.eye(192)));rc=float(np.linalg.norm(AR.reshape(192,1152)@AR.reshape(192,1152).T-np.eye(192)))
 assert max(left,right)<p['external_tol'] and max(lc,rc)<p['canonical_ceiling'] and st['eps']<p['external_tol']
 W,_,_,_=V.build_mpo(3,2,.30485);lam,F=V.dominant(lambda x:V.apply_TL(x,AL,W),(192,W.shape[0],192),tol=1e-10)
 defect=float(np.linalg.norm(V.apply_TL(F,AL,W)-lam*F)/abs(lam));fper=float(-np.log(lam));assert lam>0 and defect<p['period_contraction_ceiling']
 _,G,gh,gmh=H.build_half(3,2,.30485);q=[]
 for i in range(G['N']):
  op=np.zeros((G['N'],G['N']));op[i,i]=1;q.append(V.local_expect(AC,gh@op@gmh))
 q=np.asarray(q);color=float(np.linalg.norm(q-1/6)*np.sqrt(6/5));fhalf=float(-2*np.log(st['eta']))
 assert abs(q.sum()-1)<1e-11 and abs(color-row['color_l2_order'])<2e-12 and abs(fhalf-row['f_half'])<2e-13 and abs(fper-row['f_full_rayleigh'])<2e-10
 out=dict(kind='independent single saved-state geometry/objective/color/Rayleigh audit; no re-optimization',p=.30485,chi=192,
  checkpoint=str(cp.relative_to(ROOT)),checkpoint_sha256=sha(cp),metadata=meta,eps=float(st['eps']),gauge_left_residual=left,gauge_right_residual=right,
  left_canonical_residual=lc,right_canonical_residual=rc,period_contraction_relative_residual=defect,f_half=fhalf,f_full_rayleigh=fper,color_l2_order=color,color_sum=float(q.sum()),passed=True,
  qualification='Acceptance/integrity audit only, not a free-energy error bar, phase boundary or spinodal certificate.')
 dest=R/'branch192_upper_state_audit.json';tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps(out,indent=2)+'\n');tmp.replace(dest)
 print(json.dumps(dict(passed=True,eps=out['eps'],max_compatibility=max(left,right),max_canonical=max(lc,rc),period=defect,color_l2=color),flush=True))
if __name__=='__main__':main()

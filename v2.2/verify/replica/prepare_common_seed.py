#!/usr/bin/env python3
"""Prepare a smaller-chi common-rate warm initialization from a real checkpoint.
Truncation is approximate and NOT an accepted observation or a free-energy bound.
The source partial state is retained separately; both gauges are recomputed.
"""
from pathlib import Path
import sys,json,shutil
import numpy as np
import replica_vumps as V
import replica_halfrow as H

def truncate(st,k):
    old=st['AL'].shape[0]
    if k>old:raise ValueError('This helper only preserves/reduces a seed; growth is handled by VUMPS')
    U,s,_=np.linalg.svd(st['C'],full_matrices=False)
    lost=float(np.sum(s[k:]**2)/np.sum(s**2))
    if k==old:
        out={x:st.get(x) for x in H.STATE_KEYS};out['chi']=k
    else:
        U=U[:,:k]
        A=np.einsum('ia,isb,bj->asj',U,st['AL'],U,optimize=True)
        AL,AR,AC,C=V.mixed_canonical(A)
        out=dict(AL=AL,AR=AR,AC=AC,C=C,FL=None,FR=None,chi=k)
    AL=out['AL'];AR=out['AR'];C=out['C'];AC=out['AC']
    diag=dict(discarded_one_cut_weight=lost,
      left_canonical_error=float(np.linalg.norm(np.einsum('asb,asc->bc',AL,AL)-np.eye(k))),
      right_canonical_error=float(np.linalg.norm(np.einsum('asb,csb->ac',AR,AR)-np.eye(k))),
      gauge_compatibility_error=float(np.linalg.norm(AC-np.tensordot(C,AR,axes=([1],[0])))))
    if max(diag['left_canonical_error'],diag['right_canonical_error'])>1e-9:raise RuntimeError('Seed gauge validation failed')
    return out,diag

if __name__=='__main__':
    side=sys.argv[1];k=int(sys.argv[2]) if len(sys.argv)>2 else 96
    src=Path(f'checkpoints/n3_{side}_latest.npz');st,m=H.load_state(src,operator='hermitian-halfrow')
    assert m['n']==3 and m['d']==2
    frozen=src.with_name(f'n3_{side}_chi{m["chi"]}_p{m["p"]:.7f}_partial_iter{m.get("iters",0)}.npz')
    shutil.copyfile(src,frozen)
    seed,diag=truncate(st,k)
    out=src.with_name(f'seed_{side}_chi{k}_common.npz')
    meta=dict(n=3,d=2,p=m['p'],operator='hermitian-halfrow',tag='common-rate-warm-seed',
              not_an_accepted_observation=True,source_checkpoint=str(frozen),source_metadata=m,**diag)
    H.checkpoint(out,seed,meta)
    print(json.dumps(dict(seed=str(out),source=str(frozen),diagnostics=diag),indent=2),flush=True)

#!/usr/bin/env python3
"""Reproduce the half-row calibration schedule without overwriting its archive.
Default output is half_controls_reproduction.json (a LIST, like half_controls.json).
Use --quick for one fresh Ising chi=8 case. This is not the production order test.
"""
from pathlib import Path
import os,sys,json
import replica_halfrow as H
quick='--quick' in sys.argv
out=Path(os.environ.get('CONTROL_OUT','half_controls_reproduction.json'))
rows=[]
schedule=[(2,2,.233810,[8])] if quick else [(2,2,.233810,[8,16,32,64]),(3,2,.300,[16,24,48]),(3,2,.310,[16,24,48])]
for n,d,p,chis in schedule:
    state=None
    for chi in chis:
        state,r=H.solve(n,d,p,chi,init=state,tol=1e-8,maxiter=300,
                checkpoint_path=f'checkpoints/reproduced_control_n{n}_p{p:.6f}.npz',tag='control-reproduction',verbose=False)
        r['f_full_rayleigh']=H.full_rayleigh(state,n,d,p)
        r['tol']=1e-8;r['converged']=bool(r['eps']<1e-8)
        rows.append(r);tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(rows,indent=2));tmp.replace(out)
        print('CONTROL',n,d,p,chi,'f',r['f'],'full_Ritz',r['f_full_rayleigh'],'eps',r['eps'],'converged',r['converged'],flush=True)

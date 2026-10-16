#!/usr/bin/env python3
"""Dependency-ordered, resumable n=3 transition campaign. No cached scalar JSON
is treated as a saved MPS. Each completed/partial stage records its own tolerance,
iterations and optimizer status. The rolling NPZ is a real state checkpoint.

Usage: order_campaign.py ordered|disordered
       optional resume via RESUME_STATE; stage limits via STAGE_SECONDS, MAXITER.
"""
import sys,os,json,time,shutil
from pathlib import Path
import replica_halfrow as H

side=sys.argv[1]
if side not in ['ordered','disordered']:raise SystemExit('ordered or disordered')
start=.300 if side=='ordered' else .310
seed=Path(os.environ.get('RESUME_STATE',f'checkpoints/control_n3_p{start:.6f}.npz'))
state,meta=H.load_state(seed,operator='hermitian-halfrow')
assert meta['n']==3 and meta['d']==2
roll=Path(f'checkpoints/n3_{side}_latest.npz')
# First establish converged anchors, then compare at a common candidate rate.
if side=='ordered':cases=[(.3045,48),(.3048,48),(.3048,72),(.3048,96),(.3048,128),(.30486,128),(.30486,192)]
else:cases=[(.306,48),(.305,48),(.305,72),(.305,96),(.305,128),(.30486,128),(.30486,192)]
if os.environ.get('CASE_FILE'):
    cases=[(float(p),int(c)) for p,c in json.loads(Path(os.environ['CASE_FILE']).read_text())]
out=Path(f'order_{side}.json');db=json.loads(out.read_text()) if out.exists() else {}
tol=float(os.environ.get('MPS_TOL','1e-7'))
# Resume from the checkpoint's exact stage, never by skipping observations only.
if 'RESUME_STATE' in os.environ:
    exact=(float(meta['p']),int(meta['chi']))
    if exact in cases:cases=cases[cases.index(exact):]
for p,chi in cases:
    key=f'p{p:.7f}:chi{chi}'
    print('STAGE',side,'p',p,'chi',chi,'tol',tol,flush=True)
    try:
        state,ob=H.solve(3,2,p,chi,init=state,tol=tol,maxiter=int(os.environ.get('MAXITER','400')),
                          checkpoint_path=roll,tag=side,verbose=True)
    except RuntimeError as exc:
        _,last=H.load_state(roll,operator='hermitian-halfrow')
        db[key]=dict(n=3,d=2,p=p,chi=chi,status='budget-stopped' if 'budget' in str(exc).lower() else 'optimizer-failed',reason=str(exc),
                     checkpoint=str(roll),tol=tol,converged=False,last_state_metadata=last)
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(db,indent=2));tmp.replace(out)
        print('STOPPED',json.dumps(db[key]),flush=True);raise
    ob['tol']=tol;ob['converged']=bool(ob['eps']<tol);ob['checkpoint']=str(roll)
    # Keep the common-point states and first high-chi anchors, while bounding disk use.
    if chi>=96:
        saved=Path(f'checkpoints/n3_{side}_chi{chi}_p{p:.7f}.npz')
        shutil.copyfile(roll,saved);ob['checkpoint']=str(saved)
    if chi==128 and abs(p-.30486)<1e-9 and os.environ.get('FULL_RITZ','1')=='1':
        print('FULL_RITZ_START',side,flush=True)
        ob['f_full_rayleigh']=H.full_rayleigh(state,3,2,p)
    db[key]=ob;tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(db,indent=2));tmp.replace(out)
    print('RESULT',side,json.dumps(ob),flush=True)
    if not ob['converged']:
        print('STOP: unconverged optimizer stage; checkpoint retained; higher chi not automatically launched',flush=True)
        break

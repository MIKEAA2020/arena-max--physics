#!/usr/bin/env python3
"""Same-p PERIOD-Rayleigh comparison of frozen MPS trial states.
This is allowed for unconverged states, but is NOT a stationary-branch or
coexistence result. Contraction residuals do NOT bound optimizer/truncation error.
One worker; benchmark/time gated; atomic per-evaluation output.
"""
from pathlib import Path
import time,json,signal
import numpy as np
import replica_vumps as V
import replica_halfrow as H

def save(path,x):
    p=Path(path);t=p.with_suffix('.tmp');t.write_text(json.dumps(x,indent=2));t.replace(p)
def alarm(signum,frame):raise TimeoutError('single contraction wall limit')
signal.signal(signal.SIGALRM,alarm)
path=Path('n3_trial_period_rayleigh.json');db=dict(kind='frozen-trial-state evaluation, NOT coexistence',states={},evaluations=[])
start=time.time();states={}
for side in ['ordered','disordered']:
    st,m=H.load_state(f'checkpoints/n3_{side}_latest.npz',operator='hermitian-halfrow')
    if m['chi']!=96:raise RuntimeError('Require the stopped/completed common-rate chi96 states')
    A=st['AL'];k=A.shape[0]
    def mv(X):return np.einsum('asd,bsd->ab',np.einsum('asg,gd->asd',A,X,optimize=True),A,optimize=True)
    lam,rho=V.dominant(mv,(k,k),tol=1e-11)
    rho=(rho+rho.T)/2
    if np.trace(rho)<0:rho=-rho
    rho/=np.trace(rho)
    eig=np.linalg.eigvalsh(rho)
    if eig.min() < -1e-8:raise RuntimeError('Trial-state right fixed point is not positive')
    eig=np.maximum(eig,0);eig/=eig.sum()
    _,G,gh,gmh=H.build_half(3,2,float(m['p']))
    labs=V.ka_labels(G);par=np.diag(G['sgn'].astype(float));co=np.diag([np.cos(2*np.pi*j/3) for j,a in labs]);si=np.diag([np.sin(2*np.pi*j/3) for j,a in labs])
    def expect(O):return float(np.einsum('asb,st,atc,bc->',A,gh@O@gmh,A,rho,optimize=True))
    w=V.transfer_second(st)
    db['states'][side]=dict(source_metadata=m,source_optimizer_converged=bool(m.get('eps',1)<m.get('tol',1e-7)),
        m_species=float(np.hypot(expect(co),expect(si))),m_parity=expect(par),
        xi_chi=float(-1/np.log(abs(w[1]/w[0]))),S_ent=float(-np.sum(eig*np.log(eig+1e-300))),
        right_fixed_point_residual=float(np.linalg.norm(mv(rho)-rho)),
        qualification='a valid normalized frozen trial MPS, not necessarily a stationary phase')
    states[side]=st
save(path,db)
# Central comparison first. More rates only when the first measured contraction is cheap.
queue=[('ordered',.30488),('disordered',.30488)];i=0
while i<len(queue):
    side,p=queue[i];i+=1
    if time.time()-start>180:
        db['status']='remaining grid deferred at total time gate';break
    st=states[side];W,_,_,_=V.build_mpo(3,2,p);chi=st['AL'].shape[0]
    t0=time.time()
    try:
        signal.alarm(90)
        lam,F=V.dominant(lambda x:V.apply_TL(x,st['AL'],W),(chi,W.shape[0],chi),tol=1e-10)
        res=float(np.linalg.norm(V.apply_TL(F,st['AL'],W)-lam*F)/abs(lam))
        r=dict(preparation=side,p=p,chi=chi,f_period_Rayleigh=float(-np.log(lam)),contraction_relative_residual=res,seconds=time.time()-t0,
               qualification='frozen trial estimate; contraction error is not global eigenstate/variational error')
        db['evaluations'].append(r);save(path,db);print('TRIAL_RITZ',json.dumps(r),flush=True)
        if i==1 and r['seconds']<15:
            queue.extend([(s,q) for q in [.30486,.30490] for s in ['ordered','disordered']])
    except TimeoutError as e:
        db['status']='single evaluation budget-stopped';db['reason']=str(e);save(path,db);break
    finally:signal.alarm(0)
else:db['status']='benchmark-selected grid complete'
db['seconds_total']=time.time()-start;save(path,db)

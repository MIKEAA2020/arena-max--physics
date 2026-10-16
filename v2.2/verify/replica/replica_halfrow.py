#!/usr/bin/env python3
"""Lower-cost half-row transfer MPS, with exact-operator validation gates.

H=M1; H^dagger=H T in the bond-Gram metric, T a one-bond shift.
Thus H restricted to ring momentum zero is self-adjoint and C=H T H=H^2
there. A uniform periodic MPS is momentum zero. The bulk period free energy
from its half-row variational eigenvalue is f_half=-2 log eta_half.
This does NOT make finite-chi half-row and full-period variational estimates
identical. Cross-check full-period Rayleigh values and converged controls.
It is the same replica transfer problem, not an independent disorder tilt.
"""
import os,sys,json,time
from pathlib import Path
import numpy as np
import replica_vumps as V
from replica_tm import make_group,bond_weights,weingarten,ReplicaTM

STATE_KEYS=('AL','AR','AC','C','FL','FR')

def build_half(n,d,p,hermitian_sum=True):
    G=make_group(n);N=G['N'];Wb,_,_=bond_weights(G,d,p)
    _,gram=weingarten(G,d*d)
    w,U=np.linalg.eigh(gram)
    if w.min()<=1e-10: raise ValueError('Use an independent bond basis when the Gram matrix is singular')
    gh=(U*np.sqrt(w))@U.T;gmh=(U/np.sqrt(w))@U.T
    W=np.einsum('stb,at->abst',Wb,np.eye(N))
    W=np.einsum('xy,abyz,zt->abxt',gh,W,gmh)
    if hermitian_sum:
        # Global direct sum represents H+H^dagger. Its global factor 2 is
        # subextensive: the infinite per-site eigenvalue is that of H on k=0.
        W=V.block_diagonal_mpo([W,W.transpose(0,1,3,2)])
    return W,G,gh,gmh

def checkpoint(path,st,meta):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    payload={k:st[k] for k in STATE_KEYS if st.get(k) is not None}
    info=dict(meta)
    for k in ['eta','eps','chi','iters','seconds']:
        if k in st:info[k]=float(st[k]) if k not in ['chi','iters'] else int(st[k])
    payload['metadata']=np.array(json.dumps(info))
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('wb') as f:np.savez_compressed(f,**payload)
    os.replace(tmp,path)

def load_state(path,operator=None):
    with np.load(path,allow_pickle=False) as z:
        meta=json.loads(str(z['metadata']));st={k:z[k].copy() if k in z else None for k in STATE_KEYS}
    if operator is not None and meta.get('operator')!=operator:
        st['FL']=st['FR']=None
    st.update({k:meta[k] for k in ['eta','eps','chi','iters','seconds'] if k in meta})
    return st,meta

def full_rayleigh(st,n,d,p):
    W,_,_,_=V.build_mpo(n,d,p)
    chi=st['AL'].shape[0];D=W.shape[0]
    eta,_=V.dominant(lambda F:V.apply_TL(F,st['AL'],W),(chi,D,chi),tol=1e-10)
    return float(-np.log(eta))

def solve(n,d,p,chi,init=None,tol=1e-8,maxiter=400,checkpoint_path=None,tag='run',verbose=True):
    W,G,gh,gmh=build_half(n,d,p)
    meta=dict(n=n,d=d,p=p,operator='hermitian-halfrow',tag=tag,
              checkpoint_schema=1,tol=tol,maxiter=maxiter,
              stage_budget_seconds=float(os.environ.get('STAGE_SECONDS','0')))
    def cb(st):
        interval=5 if chi>=96 else 20
        if checkpoint_path and (st['iters']%interval==0 or st['eps']<tol):checkpoint(checkpoint_path,st,meta)
        budget=float(os.environ.get('STAGE_SECONDS','0'))
        if budget and st['seconds']>budget:
            if checkpoint_path:checkpoint(checkpoint_path,st,{**meta,'budget_exhausted':True})
            raise RuntimeError('Stage wall-clock budget exhausted; resumable checkpoint saved')
    N=G['N']
    def mirror(F):
        B=.5*(F[:,:N,:]+F[:,N:,:].transpose(2,1,0))
        return np.concatenate([B,B.transpose(2,1,0)],axis=1)
    if init is not None:
        init=dict(init)
        if init.get('FL') is not None and init['FL'].shape[1]!=2*N: init['FL']=init['FR']=None
    st=V.vumps(W,chi,init=init,tol=tol,maxiter=maxiter,verbose=verbose,callback=cb,env_project=mirror,paired_env_dim=N)
    if checkpoint_path:checkpoint(checkpoint_path,st,meta)
    ob=V.observables(st,G,gh,gmh,rmax=int(os.environ.get('CORR_RMAX','400')))
    ob['eta_half']=ob['eta'];ob['f_half']=-2*np.log(ob['eta_half']);ob['f']=ob['f_half']
    ob.update(n=n,d=d,p=p,tag=tag,operator='hermitian-halfrow',chi=chi)
    return st,ob

def validation():
    tests=[]
    for n,d,p in [(2,2,.233810),(3,2,.305),(3,3,.6),(4,2,.38)]:
        W,G,gh,gmh=build_half(n,d,p,hermitian_sum=False)
        if n==4: m=2
        else:m=3
        tm=ReplicaTM(n,d,2*m,p)
        H=V.mpo_dense_periodic(W,m)
        # Direct half-row and full-period dense matrices (small rings).
        M=np.column_stack([tm.apply_M1(np.eye(tm.dim)[:,j]).ravel() for j in range(tm.dim)])
        S1=tm.apply_local(M.T,gh) if False else None
        # Gram similarity by explicit Kronecker products.
        K=gh
        Kinv=gmh
        for _ in range(m-1): K=np.kron(K,gh);Kinv=np.kron(Kinv,gmh)
        exact=K@M@Kinv
        P=np.column_stack([tm.project_momentum0(np.eye(tm.dim)[:,j]).ravel() for j in range(tm.dim)])
        C=K@tm.dense_C()@Kinv
        err=float(np.max(np.abs(H-exact)))
        herm=float(np.max(np.abs(P@H@P-(P@H@P).T)))
        sq=float(np.max(np.abs(P@H@H@P-P@C@P)))
        r=dict(n=n,d=d,p=p,L=2*m,operator_error=err,k0_hermitian_error=herm,k0_square_error=sq)
        tests.append(r);print(r,flush=True)
        assert max(err,herm,sq)<1e-11
    return tests

if __name__=='__main__':
    if len(sys.argv)<2 or sys.argv[1]=='check':
        print(json.dumps(validation(),indent=2))
    else:
        n=int(sys.argv[1]);d=int(sys.argv[2]);p=float(sys.argv[3]);chis=[int(x) for x in sys.argv[4].split(',')]
        tag=sys.argv[5] if len(sys.argv)>5 else 'half';out=Path(os.environ.get('HALF_OUT',f'half_n{n}_d{d}.json'))
        checkpoint_path=os.environ.get('MPS_STATE',f'checkpoints/{tag}.npz')
        init=None
        if os.environ.get('RESUME_STATE'):
            init,_=load_state(os.environ['RESUME_STATE'],operator='hermitian-halfrow')
        db=json.loads(out.read_text()) if out.exists() else {}
        for chi in chis:
            st,ob=solve(n,d,p,chi,init=init,checkpoint_path=checkpoint_path,tag=tag,maxiter=int(os.environ.get('MAXITER','400')),verbose=True)
            init=st;db[f'n{n}:d{d}:p{p:.7f}:chi{chi}:{tag}']=ob
            tmp=out.with_name(out.name+'.tmp');tmp.write_text(json.dumps(db,indent=2));os.replace(tmp,out)
            print('RESULT',json.dumps(ob),flush=True)

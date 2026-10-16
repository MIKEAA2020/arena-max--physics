#!/usr/bin/env python3
"""Fourth Clifford moment transfer operator on a rank-29 physical bond span.

Use the 24 S4 permutation generators plus six integer factorized stabilizer-code
operators r_T=2 U_pi P_1. Their two-qubit tensors r_T tensor r_T have Gram rank 29.
We retain 30 closed labels with a Moore--Penrose Gram inverse. This is a rank-29
quotient representation, NOT a 30-dimensional independent commutant.

The exact twirl is a Hilbert--Schmidt orthogonal projection. At a measured wire
D_4(r_T)=|0000><0000|+|1111><1111| for every label, so the same overlap contraction
as in the Haar problem applies with h_st=tr(r_s^T r_t), G_st=h_st^2.
No critical-point split follows just from different fourth moments.
"""
import itertools,json,time,sys
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.sparse.linalg import LinearOperator,eigsh
from replica_tm import ReplicaTM,make_group,bond_weights
from clifford_tilt_smc import symplectic_group_4,gf2_rank_batch


def make_basis(ensemble='clifford'):
    G4=make_group(4);basis=np.arange(16).reshape((2,)*4)
    perms=np.array([np.eye(16)[basis.transpose(pi).ravel()] for pi in G4['elems']])
    X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.]);Y=np.array([[0,-1j],[1j,0]])
    def pow4(A):return np.kron(np.kron(A,A),np.kron(A,A))
    P=(np.eye(16)+pow4(X)+pow4(Y)+pow4(Z))/4
    extras=[]
    for U in perms:
        a=np.rint((2*U@P).real).astype(float)
        if not any(np.array_equal(a,b) for b in extras):extras.append(a)
    assert len(extras)==6
    r=perms if ensemble=='haar' else np.concatenate([perms,np.array(extras)])
    N=len(r);h=np.einsum('sij,tij->st',r,r);gram=h*h
    w,V=np.linalg.eigh(gram);keep=w>1e-8
    pinv=(V[:,keep]/w[keep])@V[:,keep].T
    gh=(V[:,keep]*np.sqrt(w[keep]))@V[:,keep].T
    gmh=(V[:,keep]/np.sqrt(w[keep]))@V[:,keep].T
    index={a.astype(np.int8).tobytes():i for i,a in enumerate(r)}
    left=[];right=[]
    for U in perms:
        left.append([index[(U@a).astype(np.int8).tobytes()] for a in r])
        right.append([index[(a@U.T).astype(np.int8).tobytes()] for a in r])
    inv=[index[a.T.astype(np.int8).tobytes()] for a in r]
    return dict(r=r,N=N,h=h,gram=gram,pinv=pinv,gh=gh,gmh=gmh,rank=int(keep.sum()),
                left=np.array(left),right=np.array(right),inv=np.array(inv),G4=G4,ensemble=ensemble)

class MomentTM(ReplicaTM):
    def __init__(self,L,p,ensemble='clifford',model=None):
        B=make_basis(ensemble) if model is None else model
        self.model=B;self.N=B['N'];self.n=4;self.d=2;self.L=L;self.m=L//2;self.p=p
        self.shape=(self.N,)*self.m;self.dim=self.N**self.m
        self.T=(1-p)*B['h']+2*p
        self.W=np.einsum('as,st,su->atu',B['pinv'],self.T,self.T)
        self.g_half=B['gh'];self.g_mhalf=B['gmh'];self.G=B['G4']
    def project_colour(self,v,sector):
        G=self.G;N=self.N
        if sector=='triv':ch=np.ones(24)
        elif sector=='sgn':ch=G['sgn'].astype(float)
        elif sector in ['std','stdsgn']:
            ch=np.array([sum(i==x for i,x in enumerate(p))-1 for p in G['elems']],float)
            if sector=='stdsgn':ch*=G['sgn']
        elif sector=='two':
            def cycle_type(p):
                seen=set();lens=[]
                for j in range(4):
                    if j in seen:continue
                    k=j;a=0
                    while k not in seen:seen.add(k);a+=1;k=p[k]
                    lens.append(a)
                return tuple(sorted(lens,reverse=True))
            tab={(1,1,1,1):2,(2,1,1):0,(2,2):2,(3,1):-1,(4,):0}
            ch=np.array([tab[cycle_type(p)] for p in G['elems']],float)
        else:raise ValueError(sector)
        v=v.reshape(self.shape)
        for actions in [self.model['left'],self.model['right']]:
            out=np.zeros(self.shape)
            for a,c in enumerate(ch):
                if c:out+=c*v[np.ix_(*([actions[a]]*self.m))]
            v=out*(ch[0]/24)
        return v
    def invert(self,v):return v.reshape(self.shape)[np.ix_(*([self.model['inv']]*self.m))]


def exact_pair_support_counts():
    S=symplectic_group_4();X=S[:,2:4,:2].copy()
    k=gf2_rank_batch(X);counts=np.bincount(k,minlength=3)
    return counts,[sum(Fraction(int(counts[j]),720)*Fraction(1,2**((n-1)*j)) for j in range(3)) for n in [2,3,4]]


def validate():
    B=make_basis();assert B['N']==30 and B['rank']==29
    assert np.all(B['r'][:,0,0]==1) and np.all(B['r'][:,-1,-1]==1)
    Q=B['pinv']@B['gram'];assert np.max(np.abs(Q@Q-Q))<1e-11
    counts,mom=exact_pair_support_counts();assert list(mom)==[Fraction(2,5),Fraction(1,5),Fraction(1,8)]
    BH=make_basis('haar');G4=make_group(4);W0,_,_=bond_weights(G4,2,.38)
    tmH=MomentTM(4,.38,'haar',BH)
    assert np.max(np.abs(tmH.W-W0))<1e-12
    # Explicit physical operators in interleaved two-qubit/replica ordering.
    idx=np.arange(256).reshape((2,)*8).transpose(0,2,4,6,1,3,5,7).ravel();iv=np.argsort(idx)
    ops=np.array([np.kron(r,r)[np.ix_(iv,iv)] for r in B['r']])
    H=np.array([[1,1],[1,-1]])/np.sqrt(2);S=np.diag([1,1j]);I=np.eye(2)
    CNOT=np.eye(4)[[0,1,3,2]]
    gate_errors=[]
    for U in [np.kron(H,I),np.kron(I,H),np.kron(S,I),np.kron(I,S),CNOT]:
        U4=np.kron(np.kron(U,U),np.kron(U,U))
        gate_errors.append(float(np.max(np.abs(U4@ops-ops@U4))))
    assert max(gate_errors)<1e-11
    rng=np.random.default_rng(61)
    for sector in ['triv','std','sgn','stdsgn','two']:
        v=rng.normal(size=(30,30));P=MomentTM(4,.38,model=B).project_colour
        assert np.linalg.norm(P(P(v,sector),sector)-P(v,sector))<1e-10
    results=[]
    for ens,model,target in [('haar',BH,Fraction(4,35)),('clifford',B,Fraction(1,8))]:
        tm=MomentTM(4,1.,ens,model)
        v=rng.normal(size=tm.dim)
        for _ in range(8):v=tm.apply_S(v).ravel();v/=np.linalg.norm(v)
        lam=float(v@tm.apply_S(v).ravel())
        assert abs(lam-float(target)**4)<1e-12
        results.append(dict(ensemble=ens,p=1,L=4,eigenvalue=lam,exact=float(target)**4))
    out=dict(labels=30,physical_bond_rank=29,pair_support_counts=counts.tolist(),
             pair_moments_n234=[str(x) for x in mom],gate_commutator_errors=gate_errors,
             haar_weight_error=float(np.max(np.abs(tmH.W-W0))),fully_monitored=results)
    print(json.dumps(out,indent=2),flush=True)
    Path('clifford4_validation.json').write_text(json.dumps(out,indent=2))
    return out


def levels(L,p,ensemble='clifford',sectors=('triv','std','sgn','two','stdsgn'),tol=1e-9):
    tm=MomentTM(L,p,ensemble)
    out=dict(L=L,p=p,ensemble=ensemble)
    rng=np.random.default_rng(212)
    for sector in sectors:
        def proj(v):return tm.project_momentum0(tm.project_colour(v,sector))
        def mv(v):return proj(tm.apply_S(proj(v))).ravel()
        v=proj(rng.normal(size=tm.shape)).ravel();v/=np.linalg.norm(v)
        A=LinearOperator((tm.dim,tm.dim),matvec=mv,dtype=float)
        vals,vecs=eigsh(A,k=2 if sector=='triv' else 1,which='LA',v0=v,tol=tol,ncv=16,maxiter=2000)
        order=np.argsort(vals)[::-1];vals=vals[order];vecs=vecs[:,order]
        res=[float(np.linalg.norm(mv(vecs[:,j])-vals[j]*vecs[:,j])) for j in range(len(vals))]
        out[sector]=vals.tolist();out[sector+'_residuals']=res
    if 'triv' in out:
        out['logl1']=float(np.log(out['triv'][0]));out['f_b_finite']=-out['logl1']/(L/2)
        for sec in sectors:
            if sec!='triv':out['X_'+sec]=float(L*np.log(out['triv'][0]/out[sec][0]))
    return out

if __name__=='__main__':
    if len(sys.argv)<2 or sys.argv[1]=='check':validate()
    else:
        L=int(sys.argv[1]);ps=[float(x) for x in sys.argv[2].split(',')];ens=sys.argv[3] if len(sys.argv)>3 else 'clifford'
        path=Path(f'clifford4_{ens}_L{L}.json');db=json.loads(path.read_text()) if path.exists() else {}
        for p in ps:
            key=f'{p:.7f}'
            if key in db:print('cached',key,flush=True);continue
            t0=time.time();r=levels(L,p,ens);r['seconds']=time.time()-t0
            db[key]=r;tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(db,indent=2));tmp.replace(path)
            print('RESULT',json.dumps(r),flush=True)

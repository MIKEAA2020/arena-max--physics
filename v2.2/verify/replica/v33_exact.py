#!/usr/bin/env python3
"""Independent finite-time replica normalisers and fourth Clifford commutant rank.

Conventions: computational product input; [measure, odd gates, measure, even gates].
Lambda=log Z/(2LT). The first measurement is inert. The Haar moment identity with
Clifford record counts applies at n=2,3 only. No thermodynamic extrapolation here.
"""
import itertools, json, numpy as np
from replica_tm import ReplicaTM

def exact_logZ(n, L, p, T):
    tm=ReplicaTM(n,2,L,p)
    # first Haar bond twirl of a rank-one product projector: constant coordinate barw
    barw=tm.Wg.sum(axis=1)[0]
    v=np.ones(tm.shape)
    logscale=(L//2)*np.log(barw)
    # First gate is already included in c1. Apply the second half-period, then T-1 periods.
    v=tm.apply_M1(v)
    a=np.max(np.abs(v)); v/=a; logscale+=np.log(a)
    for _ in range(T-1):
        v=tm.apply_C(v)
        a=np.max(np.abs(v)); v/=a; logscale+=np.log(a)
    tr=4.**tm.G['cyc']
    for _ in range(tm.m): v=np.tensordot(v,tr,axes=([0],[0]))
    return float(logscale+np.log(v))

def balanced_pauli_orbit_count():
    """Dimension of the two-qubit fourth commutant via balanced Pauli tuples.
    Pauli conjugation forces v1+v2+v3+v4=0. After normalizing by the scalar
    product W(v1)...W(v4), Clifford signs cancel, so invariant coefficients
    are constant on Sp(4,2) orbits of the first three vectors. Count these
    orbits by exact binary arithmetic, independently of the Gram-rank route.
    """
    from clifford_tilt_smc import symplectic_group_4
    S=symplectic_group_4().astype(np.int64)
    vectors=((np.arange(16)[:,None] >> np.arange(4)) & 1)
    powers=2**np.arange(4)
    maps=((vectors[None,:,:]@S)%2)@powers
    idx=np.arange(16**3)
    a=idx%16;b=(idx//16)%16;c=idx//256
    canonical=np.min(maps[:,a]+16*maps[:,b]+256*maps[:,c],axis=0)
    return int(np.unique(canonical).size)

def fourth_commutant_rank():
    """Span {U_pi, U_pi P}, P=(1/16) sum over two-qubit Pauli W of W^tensor4.
    This is a redundant 48-generator span of the two-qubit fourth Clifford commutant.
    Gram rank=29; hence a purported independent 30-label two-qubit basis is wrong.
    """
    paulis=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
    P=np.zeros((256,256),complex)
    for a,b in itertools.product(paulis,repeat=2):
        w=np.kron(a,b); w4=w
        for _ in range(3): w4=np.kron(w4,w)
        P+=w4/16
    permutations=list(itertools.permutations(range(4)))
    basis=np.arange(256).reshape((4,)*4)
    ops=[]
    for pi in permutations:
        U=np.eye(256)[basis.transpose(pi).ravel()]
        ops.append(U)
    ops+= [U@P for U in ops.copy()]
    B=np.array(ops).reshape(len(ops),-1)
    gram=B.conj()@B.T
    ev=np.linalg.eigvalsh(gram)
    import sympy as sp
    igram=np.rint(gram.real).astype(np.int64)
    assert np.max(np.abs(gram-igram))<1e-9
    from sympy.polys.matrices import DomainMatrix
    rank_exact=int(DomainMatrix.from_Matrix(sp.Matrix(igram.tolist())).rank())
    orbit_count=balanced_pauli_orbit_count()
    assert orbit_count==rank_exact
    return dict(rank=int((ev>1e-7).sum()),rank_exact=rank_exact,balanced_Pauli_orbits=orbit_count,generators=len(ops),
                positive_eigenvalues=ev[ev>1e-7].real.tolist(),
                projector_error=float(np.max(np.abs(P@P-P))))

if __name__=='__main__':
    rows=[]
    for n,L,p,T in [(2,16,.16,2),(3,8,.16,32),(3,8,.22,32),(3,12,.16,48),
                     (3,8,.305,32),(3,12,.305,48),(2,8,.233810,32)]:
        z=exact_logZ(n,L,p,T)
        r=dict(n=n,L=L,p=p,T=T,logZ=z,Lambda=z/(2*L*T)); rows.append(r)
        print(r,flush=True)
    rank=fourth_commutant_rank(); print('fourth Clifford:',rank)
    with open('v33_exact.json','w') as f: json.dump(dict(normalisers=rows,commutant=rank),f,indent=2)

#!/usr/bin/env python3
"""Half-row/checkpoint/fourth-Clifford extension regressions.
Fresh exact finite-ring identities and implementation checks, plus explicitly
labelled stored-data regressions. No transition-order or universality certificate.
"""
from pathlib import Path
import os,sys,time,json,tempfile
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'replica'))
import replica_vumps as V
import replica_halfrow as H
import clifford4_transfer as F
from replica_tm import ReplicaTM
checks=[];t0=time.time()
def check(name,ok,detail=''):
    checks.append(bool(ok));print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}",flush=True)

for n,d,p,m in [(2,2,.233810,3),(3,2,.305,3),(3,3,.6,3),(4,2,.38,2)]:
    W,G,gh,gmh=H.build_half(n,d,p,False);tm=ReplicaTM(n,d,2*m,p)
    A=V.mpo_dense_periodic(W,m)
    M=np.column_stack([tm.apply_M1(np.eye(tm.dim)[:,j]).ravel() for j in range(tm.dim)])
    K=gh;Ki=gmh
    for _ in range(m-1):K=np.kron(K,gh);Ki=np.kron(Ki,gmh)
    P=np.column_stack([tm.project_momentum0(np.eye(tm.dim)[:,j]).ravel() for j in range(tm.dim)])
    C=K@tm.dense_C()@Ki
    err=float(np.max(np.abs(A-K@M@Ki)))
    check(f'Half-row exact operator n={n},d={d}',err<1e-11,f'error={err:.2e}')
    B=P@A@P;err=float(np.max(np.abs(B-B.T)))
    check(f'Momentum-zero half-row Hermiticity n={n},d={d}',err<1e-11,f'error={err:.2e}')
    err=float(np.max(np.abs(P@(A@A-C)@P)))
    check(f'Momentum-zero C=H^2 n={n},d={d}',err<1e-11,f'error={err:.2e}')
    WH,_,_,_=H.build_half(n,d,p,True);D=V.mpo_dense_periodic(WH,m)
    err=float(np.max(np.abs(D-(A+A.T))))
    check(f'Global Hermitian direct sum n={n},d={d}',err<1e-11,f'error={err:.2e}')
    del D,WH,K,Ki,P,M,A,C

rng=np.random.default_rng(58);W=rng.normal(size=(3,3,2,2))
M=np.zeros((2,2,2,2))
for a in range(3):
    for b in range(3):M+=np.einsum('st,uv->sutv',W[a,b],W[b,a])
check('Memory-safe two-site periodic MPO contraction',np.max(np.abs(M.reshape(4,4)-V.mpo_dense_periodic(W,2)))<1e-12)
A=rng.normal(size=(6,3,6));X=rng.normal(size=(6,6))
y1=np.einsum('asg,gd,bsd->ab',A,X,A)
y2=np.einsum('asd,bsd->ab',np.einsum('asg,gd->asd',A,X,optimize=True),A,optimize=True)
check('O(d chi^3) transfer action equals the former contraction',np.max(np.abs(y1-y2))<1e-11)
E=np.einsum('asg,bsd->abgd',A,A).reshape(36,36)
a=np.sort(np.abs(np.linalg.eigvals(E)))[-6:];b=np.sort(np.abs(V.transfer_second({'AL':A})))
check('Transfer subleading spectrum agrees with dense reference',np.max(np.abs(a-b))<1e-8)

with tempfile.TemporaryDirectory(prefix='transfer-check-',dir=HERE) as td:
    cp=Path(td)/'state.npz';chi=4
    AL,AR,AC,C=V.mixed_canonical(rng.normal(size=(chi,2,chi)))
    st=dict(AL=AL,AR=AR,AC=AC,C=C,FL=rng.normal(size=(chi,4,chi)),FR=rng.normal(size=(chi,4,chi)),eta=.8,eps=1e-6,chi=4,iters=7,seconds=1.5)
    H.checkpoint(cp,st,dict(n=2,d=2,p=.2,operator='hermitian-halfrow'))
    ss,mm=H.load_state(cp,operator='hermitian-halfrow')
    check('NPZ checkpoint preserves all six MPS/environment tensors',all(np.array_equal(ss[k],st[k]) for k in H.STATE_KEYS))
    check('NPZ checkpoint preserves operator and scalar metadata',mm['n']==2 and mm['p']==.2 and mm['iters']==7 and mm['chi']==4 and ss['eta']==.8)
    ss,mm=H.load_state(cp,operator='different-functional')
    check('Incompatible operator invalidates cached environments only',ss['FL'] is None and ss['FR'] is None and np.array_equal(ss['AL'],AL))
    old=os.environ.get('STAGE_SECONDS');os.environ['STAGE_SECONDS']='1e-12'
    budget=False
    try:H.solve(2,2,.2,4,maxiter=3,checkpoint_path=cp,verbose=False)
    except RuntimeError as e:budget='budget' in str(e).lower()
    finally:
        if old is None:os.environ.pop('STAGE_SECONDS',None)
        else:os.environ['STAGE_SECONDS']=old
    ss,mm=H.load_state(cp,operator='hermitian-halfrow')
    check('Wall-budget stop persists a resumable partial state',budget and mm.get('budget_exhausted') and mm['iters']==1)
    W,_,_,_=H.build_half(2,2,.2);N=2
    def mirror(Z):
        B=.5*(Z[:,:N,:]+Z[:,N:,:].transpose(2,1,0));return np.concatenate([B,B.transpose(2,1,0)],axis=1)
    a=V.vumps(W,4,init=ss,maxiter=1,tol=1e-12,env_project=mirror)
    b=V.vumps(W,4,init=H.load_state(cp)[0],maxiter=1,tol=1e-12,env_project=mirror)
    check('Loaded checkpoint genuinely resumes the same numerical state',abs(a['eta']-b['eta'])<1e-10 and abs(a['eps']-b['eps'])<1e-9)

st,ob=H.solve(2,2,.233810,8,tol=1e-8,maxiter=150,verbose=False)
check('Fresh Ising half-row MPS converges at chi=8',ob['eps']<1e-8 and abs(ob['f']-.4702698384)<2e-9)
f=H.full_rayleigh(st,2,2,.233810)
check('Fresh Ising period-Rayleigh normalization cross-check',0<ob['f']-f<1e-7)
controls=json.loads((HERE/'replica/half_controls.json').read_text())
n2={r['chi']:r for r in controls if r['n']==2};xi=[n2[c]['xi_chi'] for c in [8,16,32,64]]
k=np.log(xi[2]/xi[1])/np.log(2)
check('Stored Ising chi ladder has expected finite-entanglement growth',all(x<y for x,y in zip(xi,xi[1:])) and 1.95<k<2.12 and all(n2[c]['eps']<1e-8 for c in n2),f'kappa(16,32)={k:.4f}')
for p in [.300,.310]:
    a={r['chi']:r for r in controls if r['n']==3 and r['p']==p}
    da=abs(a[24]['f']-a[24]['f_full_rayleigh']);db=abs(a[48]['f']-a[48]['f_full_rayleigh'])
    check(f'Stored n=3 p={p} functional discrepancy decreases with chi',db<da/5 and a[48]['eps']<3e-8,f'delta24={da:.2e},delta48={db:.2e}; lower-chi failures not promoted')

# Fresh physical fourth-moment construction; validate() also asserts local projector tests.
cwd=Path.cwd()
try:
    os.chdir(HERE/'replica');v=F.validate()
finally:os.chdir(cwd)
B=F.make_basis();Q=B['pinv']@B['gram']
check('Fourth Clifford has 30 closed labels but physical rank 29',v['labels']==30 and v['physical_bond_rank']==29)
check('Fourth Clifford Gram pseudoinverse is a quotient projector',np.max(np.abs(Q@Q-Q))<1e-11 and np.max(np.abs(B['gram']@B['pinv']@B['gram']-B['gram']))<1e-10)
check('Uniform Clifford support ranks are exactly 48,288,384',v['pair_support_counts']==[48,288,384])
check('Independent pair moments are 2/5,1/5,1/8',v['pair_moments_n234']==['2/5','1/5','1/8'])
check('Fourth Clifford generators commute with all tested physical gate generators',max(v['gate_commutator_errors'])<1e-11)
check('Fourth Haar control recovers permutation bond weights',v['haar_weight_error']<1e-12)
check('Fourth Haar and Clifford fully monitored endpoints',all(abs(r['eigenvalue']-r['exact'])<1e-12 for r in v['fully_monitored']) and v['fully_monitored'][0]['exact']!=v['fully_monitored'][1]['exact'])
tm=F.MomentTM(4,.38,model=B);x=rng.normal(size=(30,30))
for s in ['triv','std','sgn','two','stdsgn']:
    px=tm.project_colour(x,s)
    check(f'Fourth Clifford left/right {s} projector is idempotent',np.linalg.norm(tm.project_colour(px,s)-px)<1e-10)
lad=json.loads((HERE/'replica/clifford4_ladder.json').read_text())
check('Stored fourth-moment ladder completed all 52 requested cases',len(lad)==52 and all(len(r[s])>0 for r in lad.values() for s in ['triv','std','sgn','two','stdsgn']))
res=max(e for r in lad.values() for k,x in r.items() if k.endswith('_residuals') for e in x)
check('Stored fourth-moment ladder eigenpairs have small residuals',res<1e-8,f'max absolute residual={res:.2e}')
haar=lad['haar:L4:p0.38000']
check('Stored Haar fourth-moment L4 p=.38 anchor reproduced',abs(haar['triv'][0]-.0567288891621972)<1e-11 and abs(haar['X_std']-.991457926289)<1e-9)
print(f'\n{sum(checks)}/{len(checks)} checks passed [{time.time()-t0:.1f}s]',flush=True)
sys.exit(0 if all(checks) else 1)

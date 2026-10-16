#!/usr/bin/env python3
"""A-1/v33 extension checks. These validate algebra, implementation and source contracts;
they do not certify first order, universality, novelty, or unreviewed supplemental proofs.
Runs fixed-seed small-population validation afresh and writes per-run results to
replica/smc_validation_v33.json. NumPy, SciPy and SymPy required.
"""
from pathlib import Path
import sys, time, json, re, math
import numpy as np
from scipy.integrate import quad
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE/'replica'))
import clifford_tilt_smc as C
from v33_exact import exact_logZ, fourth_commutant_rank
from replica_tm import make_group
checks=[]; t0=time.time()
def check(name,ok,detail=''):
    checks.append(bool(ok)); print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}",flush=True)

C.SP4=C.symplectic_group_4(); S=C.SP4.astype(np.int64)
check('Sp(4,2) contains 720 distinct matrices', S.shape==(720,4,4) and len(np.unique(S.reshape(720,-1),axis=0))==720)
J=np.block([[np.zeros((2,2),int),np.eye(2,dtype=int)],[np.eye(2,dtype=int),np.zeros((2,2),int)]])
check('All sampled actions preserve the symplectic form', np.all((S@J@S.transpose(0,2,1))%2==J))
M,L=40,8; rng=np.random.default_rng(812)
X=np.zeros((M,L,L),np.uint8);Z=np.tile(np.eye(L,dtype=np.uint8),(M,1,1))
check('Product-state entropy is zero', np.all(C.half_chain_entropy(X,Z)==0))
for _ in range(8):
    for pairs in [np.array([(i,(i+1)%L) for i in range(1,L,2)]),np.array([(i,i+1) for i in range(0,L,2)])]:
        C.measure_layer(X,Z,.305,2,rng);C.apply_gate_layer(X,Z,pairs,rng)
comm=(X.astype(int)@Z.transpose(0,2,1).astype(int)+Z.astype(int)@X.transpose(0,2,1).astype(int))%2
check('Tableau rows stay commuting', np.all(comm==0))
check('Tableau rows stay independent', np.all(C.gf2_rank_batch(np.concatenate([X,Z],axis=2))==L))
BX=np.array([[[1,1],[0,0]]],np.uint8); BZ=np.array([[[0,0],[1,1]]],np.uint8)
check('Bell-pair entropy is one bit', C.half_chain_entropy(BX,BZ)[0]==1)
# Exhaustive uniform two-qubit Clifford action on |00>.
BX=C.SP4[:,2:4,:2].copy();BZ=C.SP4[:,2:4,2:].copy()
check('Uniform two-qubit Clifford gives 0.4 bits per crossed cut', abs(C.half_chain_entropy(BX,BZ).mean()-.4)<1e-14)
p=.305;b=2.;c=1-p+p*2**(-b);q=p*2**(-b)/c
check('Adapted measurement proposal has exact residual weights', abs((1-q)*c-(1-p))<1e-15 and abs(q*c-p*2**(-b))<1e-15)
r=C.run_smc(8,0,2,80,8,S_every=1,seed=912,verbose=False)
check('p=0 has zero random count and Z=1', r['logZ']==0 and max(r['filt_rand'])==0)
r=C.run_smc(8,.305,0,80,8,seed=913,verbose=False)
check('beta=0 has Z=1 and no resampling ancestry loss', r['logZ']==0 and min(r['n_distinct_lineages'])==80)
anc=np.array([[2,2,0],[1,0,1]]);inside=np.array([[1,0,2],[2,1,0]])
check('Within-period ancestry is reconstructed in the correct index space', np.array_equal(C.reconstruct_lineage(anc,inside),[[2,0,2],[1,0,1]]))
z=exact_logZ(2,16,.16,2)
check('Finite-time n=2 product-boundary anchor', abs(np.exp(z)-.032962)<1e-6,f'Z={np.exp(z):.9f}')
z8=exact_logZ(3,8,.16,32)/(2*8*32)
check('Finite-time n=3 benchmark independently contracted', abs(z8-(-.12192437222825833))<1e-12,f'Lambda={z8:.9f}')

# Fixed seed Monte Carlo regressions; exact finite-L,T targets, not infinite-size fits.
configs=[(16,.16,1,20000,2,5),(8,.16,2,4000,32,4),(8,.22,2,4000,32,4),
         (12,.16,2,4000,48,4),(16,.22,2,4000,64,4),
         (8,.305,2,4000,32,4),(12,.305,2,4000,48,4)]
validation=[]
for L,p,b,M,T,nseed in configs:
    vals=[]; runs=[]
    for seed in range(nseed):
        r=C.run_smc(L,p,b,M,T,seed=seed,verbose=False)
        value=np.exp(r['logZ']) if (b==1 and T==2) else r['Lambda']
        vals.append(value);runs.append(dict(seed=seed,logZ=r['logZ'],Lambda=r['Lambda'],ess_mean=r['ess_mean']))
    ex=(float(np.exp(exact_logZ(2,L,p,T))) if (b==1 and T==2) else -.173901 if L==16 else exact_logZ(int(b+1),L,p,T)/(2*L*T))
    av=float(np.mean(vals));se=float(np.std(vals,ddof=1)/np.sqrt(nseed))
    validation.append(dict(L=L,p=p,beta=b,M=M,T=T,nseed=nseed,mean=av,sem=se,exact=ex,
                           exact_source='v32 rounded anchor' if L==16 and b==2 else 'independent finite-time contraction',runs=runs))
    check(f'SMC exact-anchor regression L={L}, p={p}, beta={b}',abs(av-ex)<max(6*se,3e-5),f'{av:.9f} +/- {se:.9f}; exact={ex:.9f}')
(HERE/'replica/smc_validation_v33.json').write_text(json.dumps(validation,indent=2))
# Response relation in an exactly solvable always-random independent-site example.
lam_prime=(2**(-b)-1)/(1-p+p*2**(-b))
check('Tilted measured-density response identity has correct sign and normalization', abs(p+p*(1-p)*lam_prime-q)<1e-14)
rr=fourth_commutant_rank()
check('Two-qubit fourth Clifford commutant span has exact Gram rank 29',rr['rank_exact']==rr['rank']==29 and rr['projector_error']<1e-14)
check('Regular-bimodule sector dimensions are 1+4+1 and 1+9+9+4+1',sum(d*d for d in [1,2,1])==6 and sum(d*d for d in [1,3,3,2,1])==24)
G=make_group(3);rel=G['cyc'][G['mul'][G['inv'][:,None],np.arange(G['N'])[None,:]]]
check('n=3 wire and bond permutation spans differ (ranks 5 vs 6)',np.linalg.matrix_rank(2.**rel)==5 and np.linalg.matrix_rank(4.**rel)==6)
G=make_group(5);rel=G['cyc'][G['mul'][G['inv'][:,None],np.arange(G['N'])[None,:]]]
check('n=5 two-qubit bond Gram has rank 119 of 120',np.linalg.matrix_rank(4.**rel)==119)
# A sufficient condition that was too weak in v32 is disproved by an explicit sequence.
V=1000.;m=.2;f=math.log((1+math.exp(-m*V))/2)/(m*V)
check('Bounded intensive variance does not justify replica/volume interchange',abs(f+0.5)>.49 and .25<1)
# Reducible finite-state recorded process: initial sector coin, then either zeros or fair bits.
k=np.array([-1.,-.5,0,.5,1.]); psi=np.maximum(0,k*np.log(2))
check('Finite-state reducible process can expose an affine branch',np.all(psi[:2]==0) and np.allclose(psi[3:],k[3:]*np.log(2)))
a=np.array([-.2,-1.7,-4.]);w=np.array([.2,.5,.3]);m=.7
def var(s):
    pr=w*np.exp(s*a);pr/=pr.sum();return float(pr@(a*a)-(pr@a)**2)
g=math.log(float(w@np.exp(m*a)))
check('Exact interpolation identity retained',abs(g-m*(w@a)-quad(lambda ss:(m-ss)*var(ss),0,m,epsabs=1e-12)[0])<1e-11)
# Completed run is data, not a prediction about order.
d=json.loads((HERE/'replica/vumps_n3_chi96_dis.json').read_text());v96=[v for v in d.values() if v['chi']==96][0]
check('Disordered chi=96 result is complete and stored',abs(v96['f']-.99350654)<1e-8 and abs(v96['m_parity'])<.001 and v96['iters']==286)
old=(ROOT/'adjudications/adj-01-a-manuscript_revised_v32.txt').read_text()
new=(ROOT/'papers/v33/manuscript_revised_v33.tex').read_text()
labels=re.findall(r'\\label\{([^}]+)\}',new);refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',new)
check('v33 references resolve and labels are unique',set(refs)<=set(labels) and len(labels)==len(set(labels)))
cites={x.strip() for ss in re.findall(r'\\cite\{([^}]+)\}',new) for x in ss.split(',')};bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',new))
check('v33 citations have bibliography entries',cites<=bib)
check('v33 abstract retains CTD/CPD and explicit withdrawal',all(t in new.split('\\end{abstract}')[0] for t in ['conditional-purity','PostBQP-complete','withdraw','n!','genealogy']))
# Appendix C is byte-identical; no class claim enters either proof.
appendix=lambda ss:ss[ss.index('\\section{Precisely promised trajectory complexity}'):ss.index('\\begin{thebibliography}')]
old_app=appendix(old).replace('the same holds for any pair of thresholds $1-2^{-n}$ (YES) versus $1/2+2^{-n}$ (NO).',
                                'the same holds for the threshold pair $1-2^{-n}$ (YES) versus $1/2+2^{-n}$ (NO) for every integer $n\\ge3$.')
check('Complexity appendix unchanged except explicit non-overlap domain of optional thresholds',old_app==appendix(new))
check('Optional CPD amplified threshold gap is positive precisely for integers n>=3',
      all((1-2**(-n))>(.5+2**(-n)) for n in range(3,12)) and (1-2**(-2))==(.5+2**(-2)))
def block(ss,label):
    pos=ss.index('\\label{'+label+'}');beg=list(re.finditer(r'\\begin\{(theorem|proposition|corollary)\}',ss[:pos]))[-1]
    return ss[beg.start():ss.index('\\end{'+beg[1]+'}',pos)+len('\\end{'+beg[1]+'}')]
keep=['thm:fixed-algebra','thm:strobe','thm:compression','thm:rank','thm:general-n','prop:replica-derivative',
      'thm:no-go','prop:bivariate','thm:complexity','thm:record-mf','prop:replica-int','prop:z3closure']
check('Core operator, LDP, interpolation and dyadic statements preserved verbatim',all(block(old,k)==block(new,k) for k in keep))
print(f'\n{sum(checks)}/{len(checks)} checks passed [{time.time()-t0:.1f}s]',flush=True)
sys.exit(0 if all(checks) else 1)

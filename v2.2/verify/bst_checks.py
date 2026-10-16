#!/usr/bin/env python3
"""bst_checks.py -- independent checks on A. Abaee, 'The Rate-Distortion Theory of Bounded Sequential
Transduction' (Zenodo 10.5281/zenodo.22260638, v1, 2 Sep 2026; TeX automata_corrected_v9.tex).
Written from the statements, not from the author's verification suite.  numpy only.

  1  Full-KL information-bottleneck identity   RetKL(phi) = I(S;Z) - I(K;Z) = I(S;Z|K)
  2  Mixture centroid is the optimal block representative (Jensen)
  3  Zero-retention threshold: RetKL(M)=0 iff M >= #distinct predictive rows (brute force)
  4  Probability-coordinate chain with constant 1: KL(p||q) >= ||p-q||_2^2 ; sharp (2e^2 + 4/3 e^4)
     and the spectral converse  RetKL(M) >= sum_{i>=M} lambda_i(Sigma_pi)  (Pinsker + centring + Ky Fan)
  5  Grounding: unrestricted gap = sigma_{M+1} (Eckart-Young-Mirsky); Hankel-structured gap >= sigma_{M+1}
     (direct minimisation respects it); one-letter finite-rank rational symbol -> AAK equality attained numerically
  6  Temporal axis: log2 |H_M| = Theta(M log M) (halving upper bound); Ambainis exponent is o(k)
  7  Controlled zero threshold: the manuscript's A,B,C example (N* = 3 > 2 distinct kernels) re-derived
Prints PASS/FAIL/INFO.
"""
import math, itertools, sys
import numpy as np
rng = np.random.default_rng(1)
RES = []
def check(name, ok, info=""):
    RES.append(bool(ok)); print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {info}" if info else ""))
def info(name, text): print(f"[INFO] {name}  -- {text}")

def kl(p, q):
    m = p > 0
    return float(np.sum(p[m]*np.log(p[m]/q[m])))
def mutual_info(joint):
    px = joint.sum(1, keepdims=True); py = joint.sum(0, keepdims=True)
    m = joint > 0
    return float(np.sum(joint[m]*np.log(joint[m]/(px@py)[m])))

# random predictive family: S states with weights pi and rows P_s over Z
S, Zn = 7, 5
pi = rng.dirichlet(np.ones(S)); P = rng.dirichlet(np.ones(Zn), size=S)

def retkl(phi):
    tot = 0.0
    for k in set(phi):
        idx = [s for s in range(S) if phi[s] == k]
        w = pi[idx]; Pbar = (w[:, None]*P[idx]).sum(0)/w.sum()
        tot += sum(pi[s]*kl(P[s], Pbar) for s in idx)
    return tot

# ------------------------------------------------------------- 1
print("\n== 1. Information-bottleneck identity ==")
phi = rng.integers(0, 3, size=S)
joint_SZ = pi[:, None]*P
K = int(phi.max())+1
joint_KZ = np.zeros((K, Zn))
for s in range(S): joint_KZ[phi[s]] += joint_SZ[s]
lhs = retkl(phi); rhs = mutual_info(joint_SZ) - mutual_info(joint_KZ)
check("RetKL(phi) = I(S;Z) - I(K;Z) on a random 7-state family", abs(lhs-rhs) < 1e-12, f"{lhs:.10f} vs {rhs:.10f}")
# conditional form I(S;Z|K)
cond = 0.0
for k in range(K):
    idx = [s for s in range(S) if phi[s] == k]; wk = pi[idx].sum()
    j = joint_SZ[idx]/wk
    cond += wk*mutual_info(j)
check("... = I(S;Z|K)", abs(lhs-cond) < 1e-12)

# ------------------------------------------------------------- 2
print("\n== 2. Mixture centroid optimal ==")
idx = [s for s in range(S) if phi[s] == 0]; w = pi[idx]; Pbar = (w[:, None]*P[idx]).sum(0)/w.sum()
base = sum(pi[s]*kl(P[s], Pbar) for s in idx)
worse = True
for _ in range(200):
    Q = Pbar + 0.05*rng.normal(size=Zn); Q = np.clip(Q, 1e-9, None); Q /= Q.sum()
    worse &= sum(pi[s]*kl(P[s], Q) for s in idx) >= base - 1e-12
check("sum_s pi_s KL(P_s||Q) minimised at the weighted mixture Q = Pbar (200 perturbations)", worse)

# ------------------------------------------------------------- 3
print("\n== 3. Zero threshold ==")
def best_retkl(M):
    best = math.inf
    for labels in itertools.product(range(M), repeat=S):
        best = min(best, retkl(labels))
    return best
P_dup = P.copy(); P_dup[6] = P_dup[0]; P_dup[5] = P_dup[1]   # 5 distinct rows
P_save = P; P = P_dup
vals = {M: best_retkl(M) for M in (3, 4, 5, 6)}
P = P_save
check("RetKL(M)=0 iff M >= 5 = #distinct rows (unconstrained lumping, S=7)",
      vals[5] < 1e-12 and vals[6] < 1e-12 and vals[4] > 1e-6 and vals[3] > vals[4],
      ", ".join(f"M={M}: {v:.4e}" for M, v in vals.items()))

# ------------------------------------------------------------- 4
print("\n== 4. Constant-1 probability-coordinate chain ==")
viol = 0; ratios = []
for _ in range(20000):
    n = rng.integers(2, 7); p = rng.dirichlet(np.ones(n)*rng.uniform(0.3, 3)); q = rng.dirichlet(np.ones(n)*rng.uniform(0.3, 3))
    d = kl(p, q); l2 = float(np.sum((p-q)**2))
    if d < l2 - 1e-12: viol += 1
    ratios.append(d/l2 if l2 > 0 else np.inf)
check("KL(p||q) >= ||p-q||_2^2 on 20,000 random pairs (Pinsker 1/2 ||d||_1^2 and centring ||d||_2^2 <= 1/2 ||d||_1^2)", viol == 0,
      f"min ratio KL/||d||^2 = {min(ratios):.4f}")
eps = 1e-2; p = np.array([0.5+eps, 0.5-eps]); q = np.array([0.5, 0.5])
check("sharpness: KL = 2 eps^2 + (4/3) eps^4 + O(eps^6) for the two-point perturbation (constant 1 attained)",
      abs(kl(p, q) - (2*eps**2 + 4/3*eps**4)) < 1e-10 and abs(kl(p, q)/np.sum((p-q)**2) - 1) < 1e-3)
# spectral converse: RetKL(M) >= sum_{i>=M} lambda_i(Sigma_pi)  with Sigma_pi = sum_s pi_s (P_s - Pbar)(P_s - Pbar)^T
Pbar_all = pi @ P; Sig = sum(pi[s]*np.outer(P[s]-Pbar_all, P[s]-Pbar_all) for s in range(S))
lam = np.sort(np.linalg.eigvalsh(Sig))[::-1]
ok = True; worst = math.inf
for M in (1, 2, 3, 4):
    bound = lam[M-1:].sum()        # eigenvalues lambda_M, lambda_{M+1}, ... (1-indexed i >= M)
    for labels in itertools.product(range(M), repeat=S):
        v = retkl(labels); ok &= v >= bound - 1e-12; worst = min(worst, v - bound)
check("RetKL(phi) >= sum_{i>=M} lambda_i(Sigma_pi) for every partition into <= M blocks (M=1..4, exhaustive)", ok, f"min slack {worst:.3e}")

# ------------------------------------------------------------- 5
print("\n== 5. Grounding gaps ==")
def hankel(c, N):
    i = np.arange(N); return np.asarray(c)[i[:, None]+i[None, :]]
N = 40; c = rng.normal(size=2*N-1); H = hankel(c, N)
sv = np.linalg.svd(H, compute_uv=False)
def best_unrestricted(H, M):
    U, s, Vt = np.linalg.svd(H); return (U[:, :M]*s[:M]) @ Vt[:M]
M = 3
B = best_unrestricted(H, M)
check("unrestricted gap = sigma_{M+1} (Eckart-Young-Mirsky, operator norm)", abs(np.linalg.norm(H-B, 2) - sv[M]) < 1e-10, f"sigma_4 = {sv[M]:.4f}")
from scipy.optimize import minimize
kk = np.arange(2*N-1)
def best_structured(H, M, N, restarts=10, seed=0):
    """Direct operator-norm minimisation over rank-<=M Hankel matrices parametrised as exponential sums
    (real poles, or one complex pair when M=2).  Returns the best error found: an UPPER bound on the
    structured gap, not a certificate of its value."""
    r = np.random.default_rng(seed); best = math.inf; k = np.arange(2*N-1)
    def err_real(x):
        a = x[:M]; m = x[M:]
        if np.max(np.abs(m)) >= 0.999: return 1e3
        return np.linalg.norm(H - hankel(np.sum(a[:, None]*m[:, None]**k[None, :], 0), N), 2)
    def err_cplx(x):
        ar, ai, mr, mi = x
        if abs(complex(mr, mi)) >= 0.999: return 1e3
        return np.linalg.norm(H - hankel(2*np.real(complex(ar, ai)*complex(mr, mi)**k), N), 2)
    fs = [err_real] + ([err_cplx] if M == 2 else [])
    for f in fs:
        for _ in range(restarts):
            x0 = r.uniform(-0.9, 0.9, 2*M)
            res = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-12, maxiter=20000, maxfev=40000))
            if res.fun < best: best, bestx, bestf = res.fun, res.x, f
    for _ in range(3):   # polish from the incumbent
        res = minimize(bestf, bestx, method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-14, maxiter=40000, maxfev=80000, initial_simplex=bestx + 1e-3*r.normal(size=(2*M+1, 2*M))))
        if res.fun < best: best, bestx = res.fun, res.x
    return best
# generic finite Hankel matrix: structured error found >= sigma_{M+1} (and no equality claim either way)
H2 = hankel(rng.normal(size=2*12-1), 12); sv2 = np.linalg.svd(H2, compute_uv=False)
e2 = best_structured(H2, 2, 12, restarts=6)
check("generic 12x12 Hankel: best rank-2 Hankel approximant found has error >= sigma_3 (lower bound respected)", e2 >= sv2[2]-1e-9,
      f"found {e2:.4f} vs sigma_3 {sv2[2]:.4f} (ratio {e2/sv2[2]:.3f}; the optimiser gives an upper bound only)")
# one-letter Hardy-space case: finite-rank Hankel operator from a rational symbol (poles inside the disc).
# Explicit Adamjan-Arov-Krein construction: with (xi, eta) the Schmidt pair for sigma = sigma_{M+1},
# the symbol of the error operator is u = sigma * eta(z)/conj(xi(z)), unimodular up to sigma; the
# Hankel operator with symbol phi - u has rank <= M and distance exactly sigma from H.
lams = np.array([0.9, -0.7, 0.5, 0.3]); amps = np.array([1.0, 0.8, -0.6, 0.4])
Nn = 120; cn = np.array([np.sum(amps*lams**k) for k in range(2*Nn-1)]); Hn = hankel(cn, Nn)
Un, sn, Vtn = np.linalg.svd(Hn); M2 = 2; sig = sn[M2]; xi = Vtn[M2]; eta = Un[:, M2]
L = 1 << 14; z = np.exp(2j*np.pi*np.arange(L)/L); jj = np.arange(Nn)
xiz = (xi[None, :]*z[:, None]**jj[None, :]).sum(1); etaz = (eta[None, :]*z[:, None]**jj[None, :]).sum(1)
u = sig*etaz/np.conj(xiz); uk = np.fft.fft(u)/L; e = np.real(uk[:2*Nn-1])
Hpsi = hankel(cn-e, Nn); svp = np.linalg.svd(Hpsi, compute_uv=False); errA = np.linalg.norm(Hn-Hpsi, 2)
check("one-letter rank-4 rational (H^oo) symbol: explicit AAK approximant has rank 2 and error exactly sigma_3",
      abs(np.abs(u).max()-sig) < 1e-9 and abs(np.abs(u).min()-sig) < 1e-9 and svp[2] < 1e-4*svp[1] and abs(errA-sig) < 1e-12,
      f"|u| = {sig:.9f} on the circle; approximant sigma_3/sigma_2 = {svp[2]/svp[1]:.1e}; error {errA:.12f} = sigma_3 {sig:.12f}")
info("AAK", "equality is the one-letter Hankel theory (Adamjan-Arov-Krein 1971; Peller 2003 Thm 4.1.1); the multiletter version is left open by the manuscript")

# ------------------------------------------------------------- 6
print("\n== 6. Temporal axis arithmetic ==")
I, O = 2, 2
def log2_HM(M): return M*I*math.log2(M*O) + math.log2(M)     # transition+output tables times initial state
vals = [(M, log2_HM(M)/(M*math.log2(M))) for M in (4, 16, 64, 256, 1024)]
check("log2|H_M| / (M log2 M) stays bounded (halving bound Theta(M log M) for fixed alphabets)",
      max(v for _, v in vals) < 4 and min(v for _, v in vals) > 1, str([(M, round(v, 3)) for M, v in vals]))
amb = [(k, (k*math.log2(math.log2(k))/math.log2(k))/k) for k in (2**6, 2**10, 2**20)]
check("Ambainis exponent k loglog k / log k is o(k): sub-exponential, as the manuscript says", amb[-1][1] < amb[0][1] and amb[-1][1] < 0.3, str([(k, round(v, 3)) for k, v in amb]))

# ------------------------------------------------------------- 7
print("\n== 7. Controlled zero threshold (Remark controlled-zero-not-kernels example) ==")
# three states A,B,C; one input; outputs {0,1}; kernels P_A=P_B=Bern(1/2), P_C=Bern(1/10); unifilar update tau
Pk = {'A': np.array([.5, .5]), 'B': np.array([.5, .5]), 'C': np.array([.9, .1])}   # P(0), P(1)
tau = {('A', 0): 'A', ('A', 1): 'C', ('B', 0): 'C', ('B', 1): 'B', ('C', 0): 'A', ('C', 1): 'B'}
states = ['A', 'B', 'C']
T = np.zeros((3, 3))
for i, s in enumerate(states):
    for o in (0, 1): T[i, states.index(tau[(s, o)])] += Pk[s][o]
w, v = np.linalg.eig(T.T); st = np.real(v[:, np.argmin(abs(w-1))]); st /= st.sum()
check("stationary distribution strictly positive", np.all(st > 1e-9), f"pi = {np.round(st, 4)}")
def lumpable(blocks):
    lab = {s: i for i, b in enumerate(blocks) for s in b}
    return all(lab[tau[(s, o)]] == lab[tau[(t, o)]] for b in blocks for s in b for t in b for o in (0, 1) if Pk[s][o] > 0 and Pk[t][o] > 0)
two_block = [[['A', 'B'], ['C']], [['A', 'C'], ['B']], [['B', 'C'], ['A']]]
check("no two-block partition is unifilar-lumpable (so RetKLc(2) > 0 although only 2 distinct kernels)", not any(lumpable(b) for b in two_block))
check("the discrete partition is lumpable and has zero cost: N* = 3", lumpable([['A'], ['B'], ['C']]))
# Moore/Paige-Tarjan refinement from the kernel partition
part = {'A': 0, 'B': 0, 'C': 1}
while True:
    sig = {s: (part[s], tuple(part[tau[(s, o)]] for o in (0, 1) if Pk[s][o] > 0)) for s in states}
    keys = sorted(set(sig.values())); newp = {s: keys.index(sig[s]) for s in states}
    if newp == part: break
    part = newp
check("coarsest lumpable refinement of the kernel partition has index 3 (partition refinement)", len(set(part.values())) == 3)
# A and B are distinct causal states: two-step future laws differ
def fut2(s):
    out = np.zeros((2, 2))
    for o1 in (0, 1):
        s1 = tau[(s, o1)]
        for o2 in (0, 1): out[o1, o2] += Pk[s][o1]*Pk[s1][o2]
    return out
check("A and B have equal one-step kernels but different two-step futures (distinct causal states in the Crutchfield sense)",
      np.allclose(Pk['A'], Pk['B']) and not np.allclose(fut2('A'), fut2('B')), f"P(00|A)={fut2('A')[0,0]:.3f}, P(00|B)={fut2('B')[0,0]:.3f}")

print("\n== SUMMARY ==")
print(f"{sum(RES)}/{len(RES)} checks passed")
sys.exit(0 if all(RES) else 1)

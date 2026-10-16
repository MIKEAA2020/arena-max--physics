#!/usr/bin/env python3
"""
replica_checks.py — fast verification suite for adjudication A-1 (Abaee, manuscript_revised_v32: annealed n-replica
transfer operator of monitored Haar circuits; the n=3 "3-state Potts, x_sigma/x_eps -> 1/6" claim) and for
the adjudication in assessments/adj-01-replica-potts-dispute.md.  Runs in ~1 minute (L <= 12).
Independent implementation: verify/replica/replica_tm.py (compressed operator on bond permutations,
Weingarten weights, symmetric form, S_3 x S_3 isotypic projectors).  Long runs (L = 14, 16, 18) are in
verify/replica/spectra.json, diag.json, power.json and are NOT re-run here.
Prints "N/N checks passed".
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'replica'))
from replica_tm import ReplicaTM, make_group, bond_weights
from replica_diag import levels
from scipy.optimize import brentq

checks = []
def check(name, ok, detail=""):
    checks.append(bool(ok)); print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}")

t0 = time.time()
# 1. n=2 two-replica closure (a,b,c) of the paper, d=2, p=0.3
G2 = make_group(2); W2, _, _ = bond_weights(G2, 2, 0.3)
v = 2 - 0.3; a = (4 * v * v - 1) / 15; b = v / 5; c = (4 - v * v) / 15
check("1 n=2 closure (a,b,c) matches paper's Eq.", abs(W2[0, 0, 0] - a) < 1e-14 and abs(W2[0, 0, 1] - b) < 1e-14 and abs(W2[0, 1, 1] - c) < 1e-14,
      f"a={W2[0,0,0]:.6f} b={W2[0,0,1]:.6f} c={W2[0,1,1]:.6f}")
# 2. Weingarten at D=4 for S_3
G3 = make_group(3); W3, _, Wg3 = bond_weights(G3, 2, 0.0)
check("2 Wg_{D=4}(e, transposition, 3-cycle) = 7/360, -1/180, 1/360",
      abs(Wg3[0, 0] - 7 / 360) < 1e-14 and abs(Wg3[0, 1] + 1 / 180) < 1e-14 and abs(Wg3[0, 3] - 1 / 360) < 1e-14)
# 3. negative bond weights at p=0 (the paper's "12 negative entries, min -0.10")
neg = int((W3 < -1e-12).sum())
check("3 n=3 p=0 bond weights: 12 negative entries, min ~ -0.10", neg == 12 and abs(W3.min() + 0.10) < 0.01, f"neg={neg} min={W3.min():.4f}")
# 4. L=6, p=0.02 dense spectrum (paper: 0.836807 / 0.834268 x4 / 0.831750)
tm = ReplicaTM(3, 2, 6, 0.02); ev = np.sort(np.linalg.eigvals(tm.dense_C()).real)[::-1]
check("4 L=6 p=0.02 top levels 0.836807 / 0.834268 (x4) / 0.831750", abs(ev[0] - 0.836807) < 2e-6 and abs(ev[1] - 0.834268) < 2e-6
      and abs(ev[4] - 0.834268) < 2e-6 and abs(ev[5] - 0.831750) < 2e-6, f"{ev[0]:.6f} {ev[1]:.6f} {ev[4]:.6f} {ev[5]:.6f}")
# 5. sector assignment of those levels: triv (lam1), std x std (4-fold), sgn x sgn
r6 = levels(3, 6, 0.02)
check("5 sectors: lam1 triv, lam_sigma = std x std (0.834268), lam_sgn = sgn x sgn (0.831750)",
      abs(r6['lam1'] - 0.836807) < 2e-6 and abs(r6['lam_sigma'] - 0.834268) < 2e-6 and abs(r6['lam_sgn'] - 0.831750) < 2e-6)
# 6. n=2 control: R(L=10) = 0.118, R(L=32) = 0.1243 at p_c = 0.233810 (paper), -> 1/8 from below
r10 = levels(2, 10, 0.233810); r32 = levels(2, 32, 0.233810)
check("6 n=2 control R(10)=0.118, R(32)=0.1243, both below 1/8", abs(r10['ratio'] - 0.118) < 5e-4 and abs(r32['ratio'] - 0.1243) < 2e-4 and r32['ratio'] < 0.125,
      f"R10={r10['ratio']:.4f} R32={r32['ratio']:.5f}")
# 7. paper's n=3 crossings (4,6),(6,8),(8,10): p* and ratio at the larger size
def Xs(L, p): return levels(3, L, p)['X']
exp = {(4, 6): (0.27114, 0.107), (6, 8): (0.29678, 0.144), (8, 10): (0.30244, 0.161)}
ok7 = True; det = []
pst = {}
for (L1, L2), (pp, rr) in exp.items():
    ps = brentq(lambda p: Xs(L1, p) - Xs(L2, p), pp - 0.01, pp + 0.01, xtol=1e-6)
    R2 = levels(3, L2, ps)['ratio']; pst[(L1, L2)] = ps
    ok7 &= abs(ps - pp) < 5e-4 and abs(R2 - rr) < 1e-3; det.append(f"({L1},{L2}) p*={ps:.5f} R={R2:.4f}")
check("7 n=3 sigma-crossings reproduce the paper's table (p* to 5e-4, ratio to 1e-3)", ok7, "; ".join(det))
# 8. L=12 at the paper's p*=0.30403: ratio 0.171, X_eps = 6.0 (the paper's 'gap law' number)
r12 = levels(3, 12, 0.30403)
check("8 L=12 at p=0.30403: ratio 0.171 (paper), X_eps 6.0 (paper)", abs(r12['ratio'] - 0.171) < 1.5e-3 and abs(r12['Xeps'] - 6.0) < 0.05,
      f"ratio={r12['ratio']:.4f} Xeps={r12['Xeps']:.3f}")
# 9. the ratio has already passed 1/6 at L=12 (crossing value 0.1714 > 0.1667) and is still rising at fixed p=0.305
seq = [levels(3, L, 0.305)['ratio'] for L in (8, 10, 12)]
check("9 ratio passes 1/6 by L=12 and rises monotonically (fixed p=0.305: L=8,10,12)", r12['ratio'] > 1 / 6 and seq[0] < seq[1] < seq[2],
      f"fixed-p: {seq[0]:.4f} {seq[1]:.4f} {seq[2]:.4f}")
# 10. class structure of S_3: sigma^{-1}tau is a transposition iff parities differ; a 3-cycle iff same parity and k differs
els = G3['elems']; sg = G3['sgn']; cyc = G3['cyc']
def mul(x, y): return tuple(x[y[i]] for i in range(3))
def inv(x):
    r = [0] * 3
    for i, xi in enumerate(x): r[xi] = i
    return tuple(r)
idx = {e: i for i, e in enumerate(els)}
ok10 = True
for s_ in els:
    for t_ in els:
        rel = idx[mul(inv(s_), t_)]; same_par = sg[idx[s_]] == sg[idx[t_]]
        is_transp = (cyc[rel] == 2); is_3cyc = (cyc[rel] == 1)
        ok10 &= (is_transp == (not same_par)) and (is_3cyc == (same_par and s_ != t_))
check("10 S_3 class structure: Ising parity gating a 3-state Potts label (sigma^-1 tau transposition iff parities differ)", ok10)
# 11. two-step signature at L<=12: the sgn x sgn (parity) crossing lies above the std x std (sigma) crossing
def Xg(L, p): return levels(3, L, p)['Xsgn']
pg = brentq(lambda p: Xg(8, p) - Xg(10, p), 0.300, 0.320, xtol=1e-5)
pg2 = brentq(lambda p: Xg(10, p) - Xg(12, p), 0.300, 0.320, xtol=1e-5)
check("11 parity-sector crossings (8,10),(10,12) ~ 0.310 lie above the sigma crossings ~ 0.3026/0.3043",
      pg > pst[(8, 10)] + 0.004 and pg2 > 0.3043 + 0.004 and abs(pg - 0.3102) < 1e-3 and abs(pg2 - 0.3102) < 1e-3, f"p_sgn*(8,10)={pg:.5f} p_sgn*(10,12)={pg2:.5f}")
# 12. intermediate window p=0.3075: X_sigma grows with L (disordering) while X_sgn falls with L (still ordered), L=8,10,12
a8, a10, a12 = (levels(3, L, 0.3075) for L in (8, 10, 12))
check("12 p=0.3075: X_sigma increasing with L while X_sgn decreasing (intermediate-phase signature, L=8,10,12)",
      a8['X'] < a10['X'] < a12['X'] and a8['Xsgn'] > a10['Xsgn'] > a12['Xsgn'],
      f"X_sigma {a8['X']:.4f}<{a10['X']:.4f}<{a12['X']:.4f}; X_sgn {a8['Xsgn']:.4f}>{a10['Xsgn']:.4f}>{a12['Xsgn']:.4f}")
# 13. anisotropy-free ratio c/x_sigma = 12 A / X_sigma: n=2 calibration gives ~4 (Ising) by L=12 (4-pt fit); n=3 gives > 7.5, not 6
def A4(n, p, Ls):
    rs = [levels(n, L, p) for L in Ls]; Lt = np.array(Ls, float); y = -np.array([r['logl1'] for r in rs])
    M = np.stack([Lt, -1 / Lt, 1 / Lt ** 3], 1); (f, A, B), *_ = np.linalg.lstsq(M, y, rcond=None); return A, rs[-1]
A2, r2 = A4(2, 0.233810, (6, 8, 10, 12)); A3, r3 = A4(3, 0.305, (6, 8, 10, 12))
c2 = 12 * A2 / r2['X']; c3 = 12 * A3 / r3['X']
check("13 c/x_sigma: n=2 -> 4.05 (Ising 4); n=3 -> ~9 (3-Potts would be 6; 4-Potts 8; Ising+3-Potts 9.75)", abs(c2 - 4) < 0.1 and c3 > 7.5,
      f"n=2: {c2:.3f}; n=3: {c3:.3f}")
# ---- settlement run (replica_vumps.py, replica_n4.py; 15 Oct 2026) ----
import json
from replica_vumps import build_mpo, mpo_dense_periodic, vumps, observables
# 14. the uniform MPO (bond dimension 36) is the one-period operator C = M1 T M1, and its g^{1/2}-conjugate is symmetric
tm3 = ReplicaTM(3, 2, 6, 0.305); Cd = tm3.dense_C()
Wm, G3b, gh, gmh = build_mpo(3, 2, 0.305, symmetric=False); Cm = mpo_dense_periodic(Wm, 3)
Ws, _, _, _ = build_mpo(3, 2, 0.305, symmetric=True); Sm = mpo_dense_periodic(Ws, 3)
check("14 VUMPS MPO (D=36) reproduces the dense one-period operator at L=6; symmetric form symmetric",
      np.abs(Cm - Cd).max() < 1e-14 and np.abs(Sm - Sm.T).max() < 1e-14, f"|dC|={np.abs(Cm - Cd).max():.1e} |S-S^T|={np.abs(Sm - Sm.T).max():.1e}")
# 15. n=2 control at the exact Ising point: VUMPS chi=8 converges; xi_chi ~ 42, |m| ~ 0.47 (chi=16 gives kappa = 2.05, Ising 2.03)
W2m, G2m, gh2, gmh2 = build_mpo(2, 2, 0.233810)
st8 = vumps(W2m, 8, tol=1e-7, maxiter=300); ob8 = observables(st8, G2m, gh2, gmh2, rmax=500)
check("15 n=2 VUMPS at p_c=0.233810, chi=8: converged, f=0.470270, xi_chi in [35,50], |m| in [0.40,0.55]",
      ob8['eps'] < 1e-6 and abs(ob8['f'] - 0.4702698) < 2e-6 and 35 < ob8['xi_chi'] < 50 and 0.40 < abs(ob8['m_parity']) < 0.55,
      f"f={ob8['f']:.7f} xi={ob8['xi_chi']:.1f} m={abs(ob8['m_parity']):.3f} eps={ob8['eps']:.1e}")
# 16. n=4 sector crossings (n4.json): std (4,6)=0.3583, (6,8)=0.3790 (paper 0.35820, 0.37899); sgn crossings 0.3698, 0.3939 lie above and move away
n4 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'replica', 'n4.json')))
def X4(L, p, s):
    r = n4[f"{L}:{p:.7f}"]; l1 = r['triv'][0]; return L * np.log(l1 / r[s][0])
def cross4(s, L1, L2, p0, p1):
    d0 = X4(L1, p0, s) - X4(L2, p0, s); d1 = X4(L1, p1, s) - X4(L2, p1, s); return p0 + (p1 - p0) * d0 / (d0 - d1)
c46 = cross4('std', 4, 6, 0.355, 0.36); c68 = cross4('std', 6, 8, 0.375, 0.38)
g46 = cross4('sgn', 4, 6, 0.37, 0.375); g68 = cross4('sgn', 6, 8, 0.39, 0.395)
check("16 n=4: std crossings 0.3583/0.3790 reproduce the paper's 0.35820/0.37899; sgn crossings 0.3698/0.3939 are distinct and move away",
      abs(c46 - 0.3582) < 5e-4 and abs(c68 - 0.3790) < 5e-4 and g46 > c46 + 0.008 and g68 > c68 + 0.012 and (g68 - c68) > (g46 - c46),
      f"std {c46:.4f} {c68:.4f}; sgn {g46:.4f} {g68:.4f}")
# 17. n=3 VUMPS scans: no parity-ordered / species-disordered state at any chi (S1 excluded); both orders vanish together
rows = {}
for fn in ('vumps_n3.json', 'vumps_n3_down48.json', 'vumps_n3_fine24.json', 'vumps_n3_up72.json', 'vumps_n3_down72.json'):
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'replica', fn)
    if os.path.exists(fp): rows.update(json.load(open(fp)))
bad = [k for k, r in rows.items() if abs(r['m_parity']) > 0.1 and r['m_species'] < 0.1]
both = [k for k, r in rows.items() if abs(r['m_parity']) > 0.2 and r['m_species'] > 0.3]
none = [k for k, r in rows.items() if abs(r['m_parity']) < 0.01 and r['m_species'] < 0.05]
check("17 n=3 VUMPS (chi=24..72): no parity-ordered/species-disordered state anywhere; ordered and disordered states both present",
      len(bad) == 0 and len(both) > 10 and len(none) > 10, f"rows={len(rows)} parity-only={len(bad)} both={len(both)} neither={len(none)}")
n_ok = sum(checks)
print(f"\n{n_ok}/{len(checks)} checks passed  [{time.time()-t0:.0f}s]")
sys.exit(0 if n_ok == len(checks) else 1)

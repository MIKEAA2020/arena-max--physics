#!/usr/bin/env python3
"""Exploratory probe of the prime-spectral manuscript's occupation-sector ladders.

Model (manuscript Prop. 'jacobi', U=0, h=0, fixed V):
    H^{(S)} = sum_p log(p) n_p  +  V * sum_{p<q} (n_p+n_q)(a_p^dag a_q + h.c.)
on the sector with sum_p n_p = S, d modes (primes 2,3,5,7,11).
Diagnostics: kappa = std_window(<n_1>_j)/std_basis(n_1), <r>, near-degeneracy fraction,
with (a) isotropic V, (b) +-30% anisotropic V_pq, (c) strong O(1) symmetry breaking.
Benchmarks: Haar sqrt(2/n); semiclassical few-body n^{-(f-1)/(2f)}, f=d-1.
"""
import itertools, math, sys, time
import numpy as np

PR = [2, 3, 5, 7, 11]

def compositions(S, d):
    """All (k_1..k_d) with sum S."""
    out = []
    def rec(prefix, rem, slots):
        if slots == 1:
            out.append(tuple(prefix + [rem])); return
        for k in range(rem + 1):
            rec(prefix + [k], rem - k, slots - 1)
    rec([], S, d)
    return out

def build(S, d, V, Vpq=None, eps_diag=None, logp=None):
    basis = compositions(S, d)
    idx = {k: i for i, k in enumerate(basis)}
    n = len(basis)
    lp = np.log(PR[:d]) if logp is None else np.asarray(logp)
    if eps_diag is not None:
        lp = lp + eps_diag
    H = np.zeros((n, n))
    K = np.array(basis, dtype=float)
    H[np.arange(n), np.arange(n)] = K @ lp
    for i, k in enumerate(basis):
        for p in range(d):
            for q in range(d):
                if p == q or k[q] == 0:
                    continue
                k2 = list(k); k2[q] -= 1; k2[p] += 1
                j = idx[tuple(k2)]
                v = V if Vpq is None else Vpq[p][q]
                # bond weight (k_p+k_q) sqrt((k_p+1) k_q); (n_p+n_q) commutes with hop
                H[j, i] += v * (k[p] + k[q]) * math.sqrt((k[p] + 1) * k[q])
    return H, K

def rstat(E):
    s = np.diff(np.sort(E))
    s = s[s > 0]
    r = np.minimum(s[1:], s[:-1]) / np.maximum(s[1:], s[:-1])
    return r.mean()

def diag(S, d, V, Vpq=None, eps_diag=None, win=350, logp=None):
    H, K = build(S, d, V, Vpq, eps_diag, logp)
    n = H.shape[0]
    E, U = np.linalg.eigh(H)
    a = (U**2).T @ K[:, 0]            # <n_1>_j
    m = n // 2
    w = min(win, n // 3)
    sl = slice(m - w // 2, m + w // 2)
    Ew, aw = E[sl], a[sl]
    # detrend linearly in energy (manuscript bins; same purpose)
    c = np.polyfit(Ew, aw, 1)
    res = aw - np.polyval(c, Ew)
    std_basis = K[:, 0].std()
    kappa_raw = aw.std() / std_basis
    kappa_det = res.std() / std_basis
    # near-degeneracy: fraction of window spacings < 1e-3 of mean spacing
    sp = np.diff(Ew); frac_deg = np.mean(sp < 1e-3 * sp.mean())
    return dict(n=n, r=rstat(Ew), kappa=kappa_raw, kappa_det=kappa_det,
                deg=frac_deg, haar=math.sqrt(2 / n))

def ladder(d, Ss, V=0.3, mode="iso", seed=7):
    rng = np.random.default_rng(seed)
    rows = []
    for S in Ss:
        t0 = time.time()
        Vpq = None; eps = None; logp = None
        if mode == "aniso30":
            A = rng.uniform(-0.3, 0.3, size=(d, d)); A = (A + A.T) / 2
            Vpq = V * (1 + A)
        elif mode == "strong":
            # O(1) symmetry breaking: random on-site energies of order V*S^2/d (bandwidth scale)
            eps = rng.normal(0, 1, size=d) * V * S**2 / (4 * d)
        res = diag(S, d, V, Vpq, eps)
        res.update(S=S, t=time.time() - t0)
        rows.append(res)
        print(f"d={d} S={S:3d} n={res['n']:5d} <r>={res['r']:.3f} kappa={res['kappa']:.4f} "
              f"kappa_det={res['kappa_det']:.4f} deg={res['deg']:.3f} haar={res['haar']:.4f} "
              f"[{res['t']:.1f}s]", flush=True)
    ns = np.array([r['n'] for r in rows]); ks = np.array([r['kappa_det'] for r in rows])
    slope = np.polyfit(np.log(ns), np.log(ks), 1)[0]
    f = d - 1
    print(f"  fit kappa_det ~ n^({slope:+.3f});  Haar -0.5;  semiclassical f={f}: "
          f"-(f-1)/(2f) = {-(f-1)/(2*f):+.3f}")
    return rows

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "d3"
    if which == "d3":
        for mode in ["iso", "aniso30", "strong"]:
            print("== d=3", mode)
            ladder(3, [20, 30, 44, 60, 80, 100], mode=mode)
    elif which == "d4":
        for mode in ["iso", "strong"]:
            print("== d=4", mode)
            ladder(4, [8, 11, 14, 17, 20, 24], mode=mode)

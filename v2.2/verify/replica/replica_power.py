#!/usr/bin/env python3
"""
replica_power.py — memory-lean power iteration for L=18 (dim 6^9 = 10,077,696; 80 MB per vector).
Computes lambda_1, lambda_eps (trivial sector, deflated), lambda_sigma (std sector top, degenerate OK),
lambda_sgn (sgn sector top) of the symmetric form S = G^{1/2} C G^{-1/2}, projected to momentum 0.
At most ~4 full vectors live at any time. Validated against eigsh at L=10,12 (python3 replica_power.py test).
Usage: python3 replica_power.py L p [tol]
Results appended to power.json.
"""
import json, os, sys, time, gc
import numpy as np
from replica_tm import ReplicaTM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'power.json')

def power_top(tm, P, tol, deflate=None, maxit=400, seed=1, log=None):
    """power iteration for the top eigenvalue of P S P (restricted to the complement of `deflate`)."""
    rng = np.random.default_rng(seed)
    v = P(rng.standard_normal(tm.shape))
    if deflate is not None:
        v -= deflate * np.vdot(deflate, v)
    v /= np.linalg.norm(v)
    lam_old = 0.0
    for it in range(maxit):
        w = P(tm.apply_S(v))
        if deflate is not None:
            w -= deflate * np.vdot(deflate, w)
        lam = float(np.vdot(v, w))          # Rayleigh quotient (S symmetric)
        nrm = np.linalg.norm(w)
        res = np.linalg.norm(w - lam * v) / max(nrm, 1e-300)
        v = w / nrm
        del w
        if log and it % 10 == 0:
            print(f"      it={it:3d} lam={lam:.12e} res={res:.2e} dlam={abs(lam-lam_old):.1e}", flush=True)
        if res < tol and abs(lam - lam_old) < tol * abs(lam):
            break
        lam_old = lam
    return lam, v, it, res

def run(L, p, tol=1e-9, log=True):
    t0 = time.time()
    tm = ReplicaTM(3, 2, L, p)
    rec = dict(L=L, p=p, tol=tol)
    P_triv = tm.projector(colour='triv', k0=True)
    lam1, v1, it1, r1 = power_top(tm, P_triv, tol, log=log)
    rec.update(lam1=lam1, it1=it1, res1=r1)
    if log: print(f"  lam1={lam1:.12e} ({it1} its, res {r1:.1e}, {time.time()-t0:.0f}s)", flush=True)
    lam_eps, v2, it2, r2 = power_top(tm, P_triv, tol, deflate=v1, seed=2, log=log)
    rec.update(lam_eps=lam_eps, it2=it2, res2=r2)
    if log: print(f"  lam_eps={lam_eps:.12e} ({it2} its, res {r2:.1e}, {time.time()-t0:.0f}s)", flush=True)
    del v1, v2; gc.collect()
    P_std = tm.projector(colour='std', k0=True)
    lam_s, vs, it3, r3 = power_top(tm, P_std, tol, seed=3, log=log)
    rec.update(lam_sigma=lam_s, it3=it3, res3=r3)
    if log: print(f"  lam_sigma={lam_s:.12e} ({it3} its, res {r3:.1e}, {time.time()-t0:.0f}s)", flush=True)
    del vs; gc.collect()
    P_sgn = tm.projector(colour='sgn', k0=True)
    lam_g, vg, it4, r4 = power_top(tm, P_sgn, tol, seed=4, log=log)
    rec.update(lam_sgn=lam_g, it4=it4, res4=r4)
    del vg; gc.collect()
    rec['X'] = L * np.log(lam1 / lam_s); rec['Xeps'] = L * np.log(lam1 / lam_eps); rec['Xsgn'] = L * np.log(lam1 / lam_g)
    rec['ratio'] = rec['X'] / rec['Xeps']; rec['seconds'] = time.time() - t0
    print(f"L={L} p={p:.6f} lam1={lam1:.9e} lam_eps={lam_eps:.9e} lam_sigma={lam_s:.9e} lam_sgn={lam_g:.9e}  X={rec['X']:.5f} Xeps={rec['Xeps']:.5f} Xsgn={rec['Xsgn']:.5f} ratio={rec['ratio']:.5f} [{rec['seconds']:.0f}s]", flush=True)
    db = json.load(open(OUT)) if os.path.exists(OUT) else {}
    db[f"{L}:{p:.7f}"] = rec
    json.dump(db, open(OUT, 'w'), indent=1, sort_keys=True)
    return rec

if __name__ == '__main__':
    if sys.argv[1] == 'test':
        sp = json.load(open(os.path.join(HERE, 'spectra.json')))
        for L in (10, 12):
            r = run(L, 0.305, tol=1e-10, log=False)
            ref = sp[f"{L}:{0.305:.7f}"]
            print(f"  check vs eigsh: dlam1={abs(r['lam1']-ref['lam1'])/ref['lam1']:.1e} deps={abs(r['lam_eps']-ref['lam_eps'])/ref['lam_eps']:.1e} "
                  f"dsig={abs(r['lam_sigma']-ref['lam_sigma'])/ref['lam_sigma']:.1e} dsgn={abs(r['lam_sgn']-ref['lam_sgn'])/ref['lam_sgn']:.1e}")
    else:
        L = int(sys.argv[1]); p = float(sys.argv[2]); tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-9
        run(L, p, tol)

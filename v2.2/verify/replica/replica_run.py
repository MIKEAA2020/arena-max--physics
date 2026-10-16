#!/usr/bin/env python3
"""
replica_run.py — sector-resolved scaling spectra of C_comp^{(3)} (n=3, d=2) at sizes L=4..16,
crossings of X_L = L log(lambda_1/lambda_sigma), amplitude ratios, gaps, slope exponents.
Results are appended to spectra.json (cache keyed by (L,p)).
Usage:  python3 replica_run.py spectrum L p [p ...]
        python3 replica_run.py cross L1 L2
        python3 replica_run.py table
"""
import json, os, sys, time
import numpy as np
from replica_tm import ReplicaTM
from scipy.sparse.linalg import eigsh, LinearOperator

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'spectra.json')

def load():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    return {}

def save(db):
    tmp = CACHE + '.tmp'
    json.dump(db, open(tmp, 'w'), indent=1, sort_keys=True)
    os.replace(tmp, CACHE)

def key(L, p):
    return f"{L}:{p:.7f}"

def sector_eigs(tm, colour, k, ncv=None, tol=1e-11):
    """top-k eigenvalues of S restricted to (colour (x) colour, momentum 0). One projection per matvec."""
    P = tm.projector(colour=colour, k0=True)
    def mv(x):
        return P(tm.apply_S(np.asarray(x, float).reshape(tm.shape))).reshape(-1)
    A = LinearOperator((tm.dim, tm.dim), matvec=mv, dtype=float)
    rng = np.random.default_rng(2024 + tm.L)
    v0 = P(rng.standard_normal(tm.shape)).reshape(-1)
    v0 /= np.linalg.norm(v0)
    vals = eigsh(A, k=k, which='LA', v0=v0, ncv=ncv or max(2 * k + 1, 12), tol=tol,
                 return_eigenvectors=False, maxiter=10000)
    return np.sort(vals)[::-1]

def spectrum(L, p, db=None, force=False, verbose=True):
    db = load() if db is None else db
    kk = key(L, p)
    if kk in db and not force:
        return db[kk]
    t0 = time.time()
    tm = ReplicaTM(3, 2, L, p)
    triv = sector_eigs(tm, 'triv', 3)
    std = sector_eigs(tm, 'std', 6)
    sgn = sector_eigs(tm, 'sgn', 2)
    rec = dict(L=L, p=p, lam1=float(triv[0]), lam_eps=float(triv[1]), lam_triv3=float(triv[2]),
               lam_sigma=float(std[0]), std_mult=int(np.sum(np.abs(std - std[0]) < 1e-9 * std[0])),
               lam_std2=float(std[4]) if len(std) > 4 else None,
               lam_sgn=float(sgn[0]), lam_sgn2=float(sgn[1]), seconds=time.time() - t0)
    rec['X'] = L * np.log(rec['lam1'] / rec['lam_sigma'])
    rec['ratio'] = np.log(rec['lam1'] / rec['lam_sigma']) / np.log(rec['lam1'] / rec['lam_eps'])
    rec['gap_sigma'] = np.log(rec['lam1'] / rec['lam_sigma'])
    rec['gap_eps'] = np.log(rec['lam1'] / rec['lam_eps'])
    rec['gap_sgn'] = np.log(rec['lam1'] / rec['lam_sgn'])
    rec['Xsgn'] = L * rec['gap_sgn']
    rec['Xeps'] = L * rec['gap_eps']
    db[kk] = rec
    save(db)
    if verbose:
        print(f"L={L:2d} p={p:.6f}  lam1={rec['lam1']:.9f} lam_eps={rec['lam_eps']:.9f} lam_sigma={rec['lam_sigma']:.9f} (x{rec['std_mult']}) lam_sgn={rec['lam_sgn']:.9f}  X={rec['X']:.5f} ratio={rec['ratio']:.5f}  [{rec['seconds']:.1f}s]", flush=True)
    return rec

def X_of(L, p, db):
    return spectrum(L, p, db)['X']

def crossing(L1, L2, lo=0.24, hi=0.36, xtol=2e-6):
    """p*(L1,L2): root of X_{L1}(p) - X_{L2}(p) by Brent."""
    from scipy.optimize import brentq
    db = load()
    f = lambda p: X_of(L1, p, db) - X_of(L2, p, db)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise RuntimeError(f"no sign change in [{lo},{hi}]: {flo}, {fhi}")
    ps = brentq(f, lo, hi, xtol=xtol, rtol=1e-10)
    r1, r2 = spectrum(L1, ps, db), spectrum(L2, ps, db)
    out = dict(L1=L1, L2=L2, pstar=ps, ratio_L2=r2['ratio'], ratio_L1=r1['ratio'], gap_L2=r2['gap_sigma'],
               X=r2['X'], Xsgn_L1=r1['Xsgn'], Xsgn_L2=r2['Xsgn'], Xeps_L1=r1['Xeps'], Xeps_L2=r2['Xeps'])
    db = load(); db.setdefault('crossings', {})[f"{L1},{L2}"] = out; save(db)
    print(f"crossing ({L1},{L2}): p*={ps:.6f}  ratio(L2)={r2['ratio']:.5f} ratio(L1)={r1['ratio']:.5f}  gap(L2)={r2['gap_sigma']:.5f}  xi/L={1/r2['X']:.4f}", flush=True)
    return out

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'spectrum':
        L = int(sys.argv[2]); db = load()
        for p in map(float, sys.argv[3:]):
            spectrum(L, p, db)
    elif cmd == 'cross':
        L1, L2 = int(sys.argv[2]), int(sys.argv[3])
        lo = float(sys.argv[4]) if len(sys.argv) > 4 else 0.24
        hi = float(sys.argv[5]) if len(sys.argv) > 5 else 0.36
        crossing(L1, L2, lo, hi)
    elif cmd == 'table':
        db = load()
        for k, v in sorted(db.get('crossings', {}).items(), key=lambda kv: (int(kv[0].split(',')[0]))):
            print(k, {a: (round(b, 6) if isinstance(b, float) else b) for a, b in v.items()})

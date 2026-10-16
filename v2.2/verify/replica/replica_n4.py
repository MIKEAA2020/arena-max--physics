#!/usr/bin/env python3
"""
replica_n4.py — sector-resolved spectra of the n = 4 (d = 2) compressed transfer operator at L = 4, 6, 8,
with diagonal S_4 x S_4 colour-sector scans (characters by cycle type) and momentum zero.
The general projector supports other left/right pairs; the default scan is not the full spectrum.  Used for check (d)
of adjudication A-1: do the std(x)std ("sigma") and sgn(x)sgn ("parity") gaps close at the same p?

    python3 replica_n4.py L p [sectors]      -> appends to n4.json
"""
import json, os, sys, time
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh
from replica_tm import ReplicaTM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'n4.json')

def s4_characters(G):
    """characters of the five irreps of S_4 as vectors over group elements."""
    elems = G['elems']; n = G['n']
    fix = np.array([sum(1 for i, ai in enumerate(e) if ai == i) for e in elems], float)
    cyc = G['cyc'].astype(float); sgn = G['sgn'].astype(float)
    chi = {}
    chi['triv'] = np.ones(len(elems))
    chi['sgn'] = sgn.copy()
    chi['std'] = fix - 1
    chi['stdsgn'] = sgn * (fix - 1)
    # two-dimensional irrep: e 2, (12) 0, (123) -1, (12)(34) 2, (1234) 0
    two = np.zeros(len(elems))
    for i, e in enumerate(elems):
        c = int(cyc[i]); f = int(fix[i])
        if c == 4: two[i] = 2
        elif c == 3: two[i] = 0            # transposition
        elif c == 2 and f == 1: two[i] = -1  # 3-cycle
        elif c == 2 and f == 0: two[i] = 2   # double transposition
        else: two[i] = 0                     # 4-cycle
    chi['two'] = two
    return chi

class N4(ReplicaTM):
    def __init__(self, L, p):
        super().__init__(4, 2, L, p)
        self.chi = s4_characters(self.G)
        self.e = self.G['idx'][tuple(range(4))]

    def project_lr(self, v, lam, mu):
        """P_{lam (x) mu} = P^L_lam P^R_mu (left and right regular actions commute)."""
        G = self.G; N = self.N
        v = v.reshape(self.shape)
        cl, cm = self.chi[lam], self.chi[mu]
        out = np.zeros(self.shape)
        for a in range(N):
            if cl[a] != 0:
                out += cl[a] * self.relabel(v, a, self.e)
        out *= cl[self.e] / N
        out2 = np.zeros(self.shape)
        for b in range(N):
            if cm[b] != 0:
                out2 += cm[b] * self.relabel(out, self.e, b)
        out2 *= cm[self.e] / N
        return out2

    def sector_op(self, lam, mu):
        def P(v):
            v = self.project_lr(v, lam, mu)
            return self.project_momentum0(v)
        def mv(x):
            x = P(np.asarray(x, float).reshape(self.shape))
            return P(self.apply_S(x)).reshape(-1)
        return LinearOperator((self.dim, self.dim), matvec=mv, dtype=float), P

def top(tm, lam, mu, k=2, tol=1e-10):
    A, P = tm.sector_op(lam, mu)
    rng = np.random.default_rng(7)
    v0 = P(rng.standard_normal(tm.shape)).reshape(-1)
    if tm.dim <= 1000:
        M = np.column_stack([A.matvec(np.eye(tm.dim)[:, j]) for j in range(tm.dim)])
        w = np.sort(np.linalg.eigvalsh(0.5 * (M + M.T)))[::-1]
        return [float(x) for x in w[:k]]
    w = eigsh(A, k=k, which='LA', v0=v0, tol=tol, return_eigenvectors=False, maxiter=10000, ncv=max(2 * k + 1, 12))
    return [float(x) for x in np.sort(w)[::-1]]

if __name__ == '__main__':
    L = int(sys.argv[1]); p = float(sys.argv[2])
    sectors = sys.argv[3].split(',') if len(sys.argv) > 3 else ['triv', 'std', 'sgn', 'stdsgn', 'two']
    tm = N4(L, p)
    db = json.load(open(OUT)) if os.path.exists(OUT) else {}
    key = f"{L}:{p:.7f}"
    rec = db.get(key, {})
    for s in sectors:
        if s in rec:
            print(f"L={L} p={p} {s}: cached {rec[s]}"); continue
        t0 = time.time()
        vals = top(tm, s, s, k=(3 if s == 'triv' else 2))
        rec[s] = vals
        db[key] = rec
        json.dump(db, open(OUT, 'w'), indent=1, sort_keys=True)
        print(f"L={L} p={p} {s}x{s}: {vals}  [{time.time()-t0:.0f}s]", flush=True)
    if 'triv' in rec:
        l1 = rec['triv'][0]
        out = {s: L * np.log(l1 / rec[s][0]) for s in rec if s != 'triv'}
        out['eps'] = L * np.log(l1 / rec['triv'][1])
        print("  X_L:", {k: round(v, 5) for k, v in out.items()})

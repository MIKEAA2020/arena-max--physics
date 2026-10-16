#!/usr/bin/env python3
"""
replica_diag.py — diagnostics the paper (Abaee v32, Sec. n=3 annealed) does not report:

  A. n=2 calibration at p_c^{(2)} = 0.233810 (Ising): free-energy amplitude A(L) from
     -log lambda_1 = f L - A/L, and the anisotropy-free universal ratios
         c/x_sigma = 12 A / X_sigma   (Ising: 4),   c/x_eps = 12 A / X_eps (Ising: 1/2)
     plus the amplitude ratio R(L) = X_sigma/X_eps (-> 1/8).
  B. the same quantities for n=3 at p = 0.305 (and p = 0.300, 0.310 for sensitivity).
     3-state Potts predicts c/x_sigma = (4/5)/(2/15) = 6, c/x_eps = 1;
     4-state Potts predicts 8 and 2; Ising 4 and 1/2.
  C. the sgn(x)sgn (parity) sector: is its scaled gap X_sgn critical at the same p as X_sigma?
     scan p in [0.29, 0.40] for L = 6..12 and locate the crossings of X_sgn(L), X_sgn(L+2).
  D. extrapolation spread of the n=3 ratio sequence under different correction forms.

Results -> diag.json (separate from spectra.json so that it never races with replica_run.py).
"""
import json, os, sys, time
import numpy as np
from replica_tm import ReplicaTM
from scipy.sparse.linalg import eigsh, LinearOperator
from scipy.optimize import brentq, curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'diag.json')
PC2 = 0.233810

def sector_eigs(tm, colour, k, tol=1e-11):
    P = tm.projector(colour=colour, k0=True)
    mv = lambda x: P(tm.apply_S(np.asarray(x, float).reshape(tm.shape))).reshape(-1)
    A = LinearOperator((tm.dim, tm.dim), matvec=mv, dtype=float)
    rng = np.random.default_rng(7 + tm.L)
    v0 = P(rng.standard_normal(tm.shape)).reshape(-1); v0 /= np.linalg.norm(v0)
    vals = eigsh(A, k=k, which='LA', v0=v0, ncv=max(2 * k + 1, 12), tol=tol,
                 return_eigenvectors=False, maxiter=10000)
    return np.sort(vals)[::-1]

def levels(n, L, p):
    tm = ReplicaTM(n, 2, L, p)
    triv = sector_eigs(tm, 'triv', 3)
    rec = dict(n=n, L=L, p=p, lam1=float(triv[0]), lam_eps=float(triv[1]))
    if n == 2:
        sg = sector_eigs(tm, 'sgn', 2)
        rec['lam_sigma'] = float(sg[0]); rec['lam_sgn'] = float(sg[0])
    else:
        st = sector_eigs(tm, 'std', 5); sg = sector_eigs(tm, 'sgn', 2)
        rec['lam_sigma'] = float(st[0]); rec['lam_sgn'] = float(sg[0])
    rec['X'] = L * np.log(rec['lam1'] / rec['lam_sigma'])
    rec['Xeps'] = L * np.log(rec['lam1'] / rec['lam_eps'])
    rec['Xsgn'] = L * np.log(rec['lam1'] / rec['lam_sgn'])
    rec['ratio'] = rec['X'] / rec['Xeps']
    rec['logl1'] = float(np.log(rec['lam1']))
    return rec

def amplitude_A(Ls, logl1):
    """3-point fits of -log lambda_1 = f L - A/L on consecutive triples (least squares, exact for 2 params)."""
    out = []
    for i in range(len(Ls) - 2):
        Lt = np.array(Ls[i:i + 3], float); y = -np.array(logl1[i:i + 3])
        M = np.stack([Lt, -1 / Lt], 1)
        (f, A), *_ = np.linalg.lstsq(M, y, rcond=None)
        out.append((Ls[i + 2], float(f), float(A)))
    return out

def amplitude_A3(Ls, logl1):
    """4-point fits -log lambda_1 = f L - A/L + B/L^3."""
    out = []
    for i in range(len(Ls) - 3):
        Lt = np.array(Ls[i:i + 4], float); y = -np.array(logl1[i:i + 4])
        M = np.stack([Lt, -1 / Lt, 1 / Lt ** 3], 1)
        (f, A, B), *_ = np.linalg.lstsq(M, y, rcond=None)
        out.append((Ls[i + 3], float(f), float(A), float(B)))
    return out

def section_A(db):
    print("\n=== A. n=2 calibration at p_c = 0.233810 (Ising: c/x_sigma = 4, c/x_eps = 0.5, R = 0.125) ===")
    Ls = list(range(6, 27, 2)); recs = []
    for L in Ls:
        t0 = time.time(); r = levels(2, L, PC2); r['seconds'] = time.time() - t0; recs.append(r)
        print(f"L={L:2d} X_sigma={r['X']:.5f} X_eps={r['Xeps']:.5f} R={r['ratio']:.5f}  [{r['seconds']:.1f}s]", flush=True)
    for (L, f, A) in amplitude_A(Ls, [r['logl1'] for r in recs]):
        r = [q for q in recs if q['L'] == L][0]
        print(f"  3pt up to L={L:2d}: f={f:.6f} A={A:.5f}  c/x_sigma={12*A/r['X']:.3f}  c/x_eps={12*A/r['Xeps']:.3f}  zeta(c=1/2)={6*A/np.pi/0.5:.4f}")
    for (L, f, A, B) in amplitude_A3(Ls, [r['logl1'] for r in recs]):
        r = [q for q in recs if q['L'] == L][0]
        print(f"  4pt up to L={L:2d}: A={A:.5f} B={B:.4f}  c/x_sigma={12*A/r['X']:.3f}  c/x_eps={12*A/r['Xeps']:.3f}")
    db['n2_calibration'] = recs

def section_B(db, spectra):
    print("\n=== B. n=3: amplitude A(L) and anisotropy-free ratios at p = 0.305 (from spectra.json) ===")
    print("    3-Potts: c/x_sigma=6, c/x_eps=1 | 4-Potts: 8, 2 | Ising: 4, 0.5")
    rows = []
    for k, r in spectra.items():
        if k == 'crossings': continue
        if abs(r['p'] - 0.305) < 1e-9: rows.append(r)
    rows.sort(key=lambda r: r['L'])
    Ls = [r['L'] for r in rows]; logl1 = [np.log(r['lam1']) for r in rows]
    for r in rows:
        print(f"L={r['L']:2d} X_sigma={r['X']:.5f} X_eps={r['Xeps']:.5f} X_sgn={r['Xsgn']:.5f} R={r['ratio']:.5f} Xsgn/X={r['Xsgn']/r['X']:.4f} Xeps/Xsgn={r['Xeps']/r['Xsgn']:.4f}")
    res = []
    for (L, f, A) in amplitude_A(Ls, logl1):
        r = [q for q in rows if q['L'] == L][0]
        res.append(dict(L=L, f=f, A=A, c_over_xsigma=12 * A / r['X'], c_over_xeps=12 * A / r['Xeps'], c_over_xsgn=12 * A / r['Xsgn']))
        print(f"  3pt up to L={L:2d}: f={f:.6f} A={A:.5f}  c/x_sigma={12*A/r['X']:.3f}  c/x_eps={12*A/r['Xeps']:.3f}  c/x_sgn={12*A/r['Xsgn']:.3f}"
              f"  | if c=4/5: zeta={6*A/np.pi/0.8:.3f} x_sigma={r['X']/(2*np.pi)/(6*A/np.pi/0.8):.4f} ; if c=1: zeta={6*A/np.pi:.3f} x_sigma={r['X']/(2*np.pi)/(6*A/np.pi):.4f} x_eps={r['Xeps']/(2*np.pi)/(6*A/np.pi):.4f} x_sgn={r['Xsgn']/(2*np.pi)/(6*A/np.pi):.4f}")
    for (L, f, A, B) in amplitude_A3(Ls, logl1):
        r = [q for q in rows if q['L'] == L][0]
        print(f"  4pt up to L={L:2d}: A={A:.5f} B={B:.4f}  c/x_sigma={12*A/r['X']:.3f}  c/x_eps={12*A/r['Xeps']:.3f}")
    db['n3_p0.305'] = dict(rows=rows, fits=res)
    # sensitivity: p = 0.300 and 0.310, L = 6..14 (computed here, not cached in spectra.json)
    for p in (0.300, 0.310):
        rr = []
        for L in (6, 8, 10, 12, 14):
            rr.append(levels(3, L, p))
        Ls2 = [r['L'] for r in rr]
        print(f"  -- sensitivity p={p}:")
        for (L, f, A) in amplitude_A(Ls2, [r['logl1'] for r in rr]):
            r = [q for q in rr if q['L'] == L][0]
            print(f"     3pt up to L={L:2d}: A={A:.5f} c/x_sigma={12*A/r['X']:.3f} c/x_eps={12*A/r['Xeps']:.3f} R={r['ratio']:.5f} X_sigma={r['X']:.4f} X_sgn={r['Xsgn']:.4f}")
        db[f'n3_p{p}'] = rr

def section_C(db):
    print("\n=== C. parity (sgn x sgn) sector: where does X_sgn(L) cross X_sgn(L+2)? ===")
    ps = [0.29, 0.30, 0.305, 0.31, 0.32, 0.33, 0.34, 0.36, 0.38, 0.40]
    tab = {}
    for L in (6, 8, 10, 12):
        tab[L] = {}
        for p in ps:
            r = levels(3, L, p); tab[L][p] = r
        print(f"L={L:2d} X_sgn(p): " + "  ".join(f"{p:.3f}:{tab[L][p]['Xsgn']:.4f}" for p in ps))
    for L in (6, 8, 10, 12):
        print(f"L={L:2d} X_sig(p): " + "  ".join(f"{p:.3f}:{tab[L][p]['X']:.4f}" for p in ps))
    cross = {}
    for L in (6, 8, 10):
        f = lambda p: levels(3, L, p)['Xsgn'] - levels(3, L + 2, p)['Xsgn']
        vals = [(p, tab[L][p]['Xsgn'] - tab[L + 2][p]['Xsgn']) for p in ps]
        br = None
        for (p1, v1), (p2, v2) in zip(vals, vals[1:]):
            if v1 * v2 < 0: br = (p1, p2); break
        if br is None:
            print(f"  sgn crossing ({L},{L+2}): none in scan; differences {[(p, round(v,4)) for p, v in vals]}")
            cross[f'{L},{L+2}'] = None
        else:
            pst = brentq(f, br[0], br[1], xtol=1e-5)
            r2 = levels(3, L + 2, pst)
            print(f"  sgn crossing ({L},{L+2}): p_sgn*={pst:.5f}  X_sgn={r2['Xsgn']:.4f}  (sigma crossing of same pair: see spectra.json)")
            cross[f'{L},{L+2}'] = dict(pstar=pst, Xsgn=r2['Xsgn'])
    db['sgn_scan'] = {str(L): {str(p): tab[L][p] for p in ps} for L in tab}
    db['sgn_crossings'] = cross

def section_D(db, spectra):
    print("\n=== D. extrapolation spread of the n=3 ratio R(L) (crossing values, value at larger size) ===")
    cr = spectra.get('crossings', {})
    pts = sorted([(v['L2'], v['ratio_L2']) for v in cr.values()])
    Ls = np.array([p[0] for p in pts], float); R = np.array([p[1] for p in pts])
    print("  data:", ", ".join(f"L={int(l)}: {r:.5f}" for l, r in pts))
    inc = np.diff(R); print("  increments:", np.round(inc, 5), " ratios of successive increments:", np.round(inc[1:] / inc[:-1], 3))
    forms = {
        'R + a/L^2': (lambda L, R0, a: R0 + a / L ** 2, [0.2, -1]),
        'R + a/L': (lambda L, R0, a: R0 + a / L, [0.2, -1]),
        'R + a/L^b': (lambda L, R0, a, b: R0 + a / L ** b, [0.2, -1, 1.0]),
        'R + a/ln(L/L0)': (lambda L, R0, a, L0: R0 + a / np.log(L / L0), [0.25, -0.1, 1.0]),
    }
    out = {}
    for lo in (8, 10):
        m = Ls >= lo
        for name, (fn, p0) in forms.items():
            if m.sum() <= len(p0): continue
            try:
                popt, _ = curve_fit(fn, Ls[m], R[m], p0=p0, maxfev=20000)
                resid = np.sqrt(np.mean((fn(Ls[m], *popt) - R[m]) ** 2))
                print(f"  L>={lo:2d} {name:16s} R_inf={popt[0]:.4f} params={np.round(popt[1:],3)} rms={resid:.1e}")
                out[f'{name}|L>={lo}'] = dict(R_inf=float(popt[0]), params=[float(x) for x in popt[1:]], rms=float(resid))
            except Exception as e:
                print(f"  L>={lo:2d} {name:16s} fit failed: {e}")
    # the same for the fixed-p = 0.305 sequence
    rows = sorted([r for k, r in spectra.items() if k != 'crossings' and abs(r['p'] - 0.305) < 1e-9], key=lambda r: r['L'])
    Lf = np.array([r['L'] for r in rows], float); Rf = np.array([r['ratio'] for r in rows])
    print("  fixed p=0.305 data:", ", ".join(f"L={int(l)}: {r:.5f}" for l, r in zip(Lf, Rf)))
    incf = np.diff(Rf); print("  increments:", np.round(incf, 5), " ratios:", np.round(incf[1:] / incf[:-1], 3))
    for lo in (8, 10):
        m = Lf >= lo
        for name, (fn, p0) in forms.items():
            if m.sum() <= len(p0): continue
            try:
                popt, _ = curve_fit(fn, Lf[m], Rf[m], p0=p0, maxfev=20000)
                resid = np.sqrt(np.mean((fn(Lf[m], *popt) - Rf[m]) ** 2))
                print(f"  fixed-p L>={lo:2d} {name:16s} R_inf={popt[0]:.4f} params={np.round(popt[1:],3)} rms={resid:.1e}")
                out[f'fixedp|{name}|L>={lo}'] = dict(R_inf=float(popt[0]), params=[float(x) for x in popt[1:]], rms=float(resid))
            except Exception as e:
                print(f"  fixed-p L>={lo:2d} {name:16s} fit failed: {e}")
    db['extrapolations'] = out

if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C', 'D']
    db = json.load(open(OUT)) if os.path.exists(OUT) else {}
    spectra = json.load(open(os.path.join(HERE, 'spectra.json')))
    if 'A' in which: section_A(db)
    if 'B' in which: section_B(db, spectra)
    if 'C' in which: section_C(db)
    if 'D' in which: section_D(db, spectra)
    json.dump(db, open(OUT, 'w'), indent=1, sort_keys=True, default=float)

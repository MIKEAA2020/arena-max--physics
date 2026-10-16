#!/usr/bin/env python3
"""compare the tilted-SMC pilot with the VUMPS thermodynamic-limit predictions (Lambda(2;p) = -f/4; rho_t = p - p(1-p) f'(p)/4)."""
import json, glob, sys
import numpy as np
from scipy.interpolate import CubicSpline
# VUMPS f(p): best (lowest) f per p from all n=3 files
F = {}
for fn in glob.glob('vumps_n3*.json'):
    for k, v in json.load(open(fn)).items():
        p = round(v['p'], 5); F[p] = min(F.get(p, 9), v['f'])
ps = np.array(sorted(F)); fs = np.array([F[p] for p in ps])
lo = ps <= 0.3048; hi = ps >= 0.3050          # the two branches (p_c = 0.3049)
cs_lo = CubicSpline(ps[lo], fs[lo]); cs_hi = CubicSpline(ps[hi], fs[hi])
def f_vumps(p):   return float(cs_lo(p) if p <= 0.3049 else cs_hi(p))
def fp_vumps(p):  return float(cs_lo(p, 1) if p <= 0.3049 else cs_hi(p, 1))
def rho_t(p):     return p - p * (1 - p) * fp_vumps(p) / 4
rows = []
for fn in sys.argv[1:] or glob.glob('smc_pilot_*.json'):
    for r in json.load(open(fn)):
        T = r['T']; mid = slice(T // 4, 3 * T // 4)
        Sm = [m for m in (r['bulk_S']['mean'][mid] if r['bulk_S'] else []) if m is not None]
        Sv = [m for m in (r['bulk_S']['var'][mid] if r['bulk_S'] else []) if m is not None]
        # pooled mid-window histogram of the bulk S_half
        H = None
        if r['bulk_S']:
            for h in r['bulk_S']['hist'][mid]:
                if h is None: continue
                h = np.array(h); H = h if H is None else H + h
        rows.append((r['L'], r['p'], r['beta'], r['M'], T, r['seed'], r['Lambda'], r['bulk_meas_mid'], r['bulk_rand_mid'],
                     np.mean(Sm) if Sm else np.nan, np.sqrt(np.mean(Sv)) if Sv else np.nan, r['n_distinct_lineages'][T // 2], r['ess_mean'], H))
rows.sort(key=lambda x: (x[0], x[2], x[1], x[5]))
print(f"{'L':>4} {'p':>6} {'beta':>4} {'M':>5} {'T':>4} {'sd':>2} {'Lambda_L':>10} {'-f/4(VUMPS)':>11} {'rho_meas':>8} {'rho_t(VUMPS)':>12} {'x_rand':>7} {'S_half':>7} {'sd(S)':>6} {'lin':>4} {'ESS':>5}")
for L, p, b, M, T, sd, lam, rho, x, S, sS, lin, ess, H in rows:
    pred = -f_vumps(p) / 4 if b == 2 else np.nan
    rt = rho_t(p) if b == 2 else np.nan
    print(f"{L:4d} {p:6.3f} {b:4.0f} {M:5d} {T:4d} {sd:2d} {lam:+10.6f} {pred:+11.6f} {rho:8.4f} {rt:12.4f} {x:7.4f} {S:7.2f} {sS:6.2f} {lin:4d} {ess:5.0f}")
if '--hist' in sys.argv or True:
    print("\npooled mid-window bulk histograms of S_half (bits), per run:")
    for L, p, b, M, T, sd, lam, rho, x, S, sS, lin, ess, H in rows:
        if H is None: continue
        nz = np.nonzero(H)[0]
        print(f"L={L} p={p:.3f} beta={b:g} seed={sd}: S in [{nz.min()},{nz.max()}]  counts:", ' '.join(f"{s}:{H[s]}" for s in range(nz.min(), nz.max() + 1)))

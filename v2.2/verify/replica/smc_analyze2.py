#!/usr/bin/env python3
"""results table for the tilted-SMC pilot: SMC vs VUMPS thermodynamic-limit predictions."""
import json, glob, sys
import numpy as np
from scipy.interpolate import CubicSpline
def load_f(n):
    F = {}
    for fn in glob.glob(f'vumps_n{n}*.json') + (glob.glob('scratch_n2.json') + glob.glob('control_n2*.json') if n == 2 else []):
        for k, v in json.load(open(fn)).items():
            if not isinstance(v, dict) or 'p' not in v or v.get('n', n) != n: continue
            p = round(v['p'], 5); F[p] = min(F.get(p, 9), v['f'])
    return F
F3 = load_f(3); F2 = load_f(2)
ps3 = np.array(sorted(F3)); fs3 = np.array([F3[p] for p in ps3])
lo = ps3 <= 0.3048; hi = ps3 >= 0.3050
cs_lo = CubicSpline(ps3[lo], fs3[lo]); cs_hi = CubicSpline(ps3[hi], fs3[hi])
def f3(p):  return float(cs_lo(p) if p <= 0.3049 else cs_hi(p))
def fp3(p):
    # branch slopes measured directly at the transition (chi = 72/96 data); spline elsewhere (interior points only)
    if 0.3040 <= p <= 0.3049: return 3.244
    if 0.3050 <= p <= 0.3062: return 3.152
    return float(cs_lo(p, 1) if p <= 0.3049 else cs_hi(p, 1))
def pred(p, beta):
    if beta == 2: return -f3(p) / 4, p - p * (1 - p) * fp3(p) / 4
    if beta == 1:
        q = round(p, 5)
        return (-F2[q] / 4 if q in F2 else np.nan), np.nan
    return np.nan, np.nan
recs = {}
for fn in glob.glob('smc_pilot_*.json'):
    for r in json.load(open(fn)):
        key = (r['L'], round(r['p'], 4), r['beta'])
        recs.setdefault(key, []).append(r)
print(f"{'L':>4} {'p':>7} {'b':>2} {'runs':>4} {'Lambda_L':>10} {'-f/4':>9} {'offset':>8} {'rho':>7} {'rho_t':>7} {'x_rand':>7} {'S_bulk[T/2,7T/8]':>16} {'S_filt(last q)':>14} {'lin@T/2':>7} {'ESS/M':>6}")
for key in sorted(recs):
    L, p, b = key; rs = recs[key]
    lam = np.mean([r['Lambda'] for r in rs]); pl, rt = pred(p, b)
    rho = np.mean([r['bulk_meas_mid'] for r in rs]); x = np.mean([r['bulk_rand_mid'] for r in rs])
    Sb = []; Sf = []; lin = []
    for r in rs:
        T = r['T']; m = r['bulk_S']['mean']; mf = r['filt_S']['mean']
        Sb += [v for v in m[T // 2:7 * T // 8] if v is not None]; Sf += [v for v in mf[3 * T // 4:] if v is not None]
        lin.append(r['n_distinct_lineages'][T // 2])
    ess = np.mean([r['ess_mean'] / r['M'] for r in rs])
    print(f"{L:4d} {p:7.4f} {b:2.0f} {len(rs):4d} {lam:+10.6f} {pl:+9.6f} {lam-pl:+8.4f} {rho:7.4f} {rt:7.4f} {x:7.4f} {np.mean(Sb):16.2f} {np.mean(Sf):14.2f} {np.mean(lin):7.1f} {ess:6.2f}")

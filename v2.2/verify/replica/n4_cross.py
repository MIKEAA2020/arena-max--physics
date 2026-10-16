#!/usr/bin/env python3
"""crossings of X_L(p) = L log(lambda_1/lambda_sector) between consecutive L for the n=4 sectors."""
import json, numpy as np, os
db = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'n4.json')))
data = {}
for key, rec in db.items():
    L, p = key.split(':'); L = int(L); p = float(p)
    if 'triv' not in rec: continue
    l1 = rec['triv'][0]
    for s, vals in rec.items():
        if s == 'triv':
            data.setdefault(('eps', L), {})[p] = L * np.log(l1 / vals[1])
        else:
            data.setdefault((s, L), {})[p] = L * np.log(l1 / vals[0])
def cross(s, L1, L2):
    a = data.get((s, L1), {}); b = data.get((s, L2), {})
    ps = sorted(set(a) & set(b))
    out = []
    for i in range(len(ps) - 1):
        d0 = a[ps[i]] - b[ps[i]]; d1 = a[ps[i+1]] - b[ps[i+1]]
        if d0 * d1 < 0:
            pc = ps[i] + (ps[i+1] - ps[i]) * d0 / (d0 - d1)
            # X at crossing (larger L, linear interp) and ratio to eps
            Xb = b[ps[i]] + (b[ps[i+1]] - b[ps[i]]) * (pc - ps[i]) / (ps[i+1] - ps[i])
            e = data[('eps', L2)]; Xe = e[ps[i]] + (e[ps[i+1]] - e[ps[i]]) * (pc - ps[i]) / (ps[i+1] - ps[i])
            out.append((pc, Xb, Xb / Xe))
    return ps, out
for s in ('std', 'two', 'stdsgn', 'sgn'):
    for (L1, L2) in ((4, 6), (6, 8)):
        ps, out = cross(s, L1, L2)
        print(f"{s:7s} ({L1},{L2}) grid {[round(x,3) for x in ps]} -> crossings " + ", ".join(f"p*={pc:.4f} X={X:.4f} X/X_eps={r:.4f}" for pc, X, r in out))
print()
for L in (4, 6, 8):
    print(f"L={L}: p -> X_std, X_two, X_stdsgn, X_sgn, X_eps")
    for p in sorted(set.intersection(*[set(data.get((s, L), {})) for s in ("std", "two", "stdsgn", "sgn", "eps")])):
        print(f"   {p:.3f}: " + "  ".join(f"{data[(s, L)][p]:.4f}" for s in ('std', 'two', 'stdsgn', 'sgn', 'eps')))

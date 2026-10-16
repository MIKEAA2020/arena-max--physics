#!/usr/bin/env python3
"""driver: python3 smc_pilot.py out.json L:p:M:T:seed[:S_every] ...   (appends one record per config)"""
import sys, json, os, time
import numpy as np
import clifford_tilt_smc as C
out = sys.argv[1]
db = json.load(open(out)) if os.path.exists(out) else []
done = {(r['L'], round(r['p'], 5), r['M'], r['T'], r['seed'], r['beta']) for r in db}
for spec in sys.argv[2:]:
    f = spec.split(':'); L, p, M, T, seed = int(f[0]), float(f[1]), int(f[2]), int(f[3]), int(f[4])
    S_every = int(f[5]) if len(f) > 5 else 2
    beta = float(f[6]) if len(f) > 6 else 2.0
    if (L, round(p, 5), M, T, seed, beta) in done:
        print("cached", spec, flush=True); continue
    r = C.run_smc(L, p, beta, M, T, S_every=S_every, seed=seed, verbose=False)
    Smid = [m for m in r['bulk_S']['mean'][T // 4:3 * T // 4] if m is not None] if r['bulk_S'] else []
    print(f"L={L} p={p:.4f} beta={beta:g} M={M} T={T} seed={seed}: Lambda={r['Lambda']:+.6f} ESS {r['ess_mean']:.0f}/{M} "
          f"rho_meas={r['bulk_meas_mid']:.4f} x_rand={r['bulk_rand_mid']:.4f} S_half(bulk,mid)={np.mean(Smid) if Smid else float('nan'):.3f} "
          f"lineages(mid)={r['n_distinct_lineages'][T//2]} [{r['seconds']:.0f}s]", flush=True)
    db.append(r)
    json.dump(db, open(out + '.tmp', 'w')); os.replace(out + '.tmp', out)

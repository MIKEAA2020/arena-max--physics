# Fresh χ192 ordered-history continuation at p=.30485

17 October 2026 · separately authorized fresh six-hour attempt · one rate, one preparation, finite-χ only.

**Status:** accepted finite-chi upper-rate state.

## Authorization, source and cap

The prior six-hour attempt ended without a final record or target checkpoint. The user then explicitly authorized one fresh attempt under a new six-hour absolute cap, starting with a new disposable benchmark. This attempt reuses only the accepted ordered χ192 p=.30480 checkpoint; it does not resume or overwrite the interrupted attempt. No other rate, preparation, gap/excited-state calculation, perturbation or stability test is authorized.

Source checkpoint: `v2.2/verify/replica/checkpoints/branch192_retry1_ordered_p0.3048000.npz`; SHA-256 `d15055d94d8a527a698a7967f468704d4c5cdaf1513c2388198170f0652ca1da`; source color L2 0.47912668.
Same-rate iteration reference: accepted χ128 ordered p=.30485 in 205 iterations; used only for conservative runtime forecasting.

Acceptance gates remain unchanged: optimizer and both compatibility residuals <1e−7, canonical defects <1e−9, positive full-period trial contraction with relative defect <1e−8.

## Disposable benchmark and feasibility gate

Benchmark: 1 step(s), 64.63 s/iteration, wall 64.66 s, peak RSS 169372 KiB, finite=True; no benchmark checkpoint was written.
Forecast: 205 × 80.65 s + 120 s setup + 900 s validation = 17553.70 s versus 21534.53 s remaining; headroom 3980.82 s. Memory passed=True. Decision: **PROCEED with exactly one retry1 production worker**.

## Production result

| Status | Iterations | eps | Right compatibility | Color L2 | m_species | ξχ | f_half | f_period,trial |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| accepted finite-chi numerical state | 83 | 0.00000005 | 0.00000005 | 0.00030084 | 0.00029499 | 83.408 | 0.993029666181 | 0.993029606389 |

Independent saved-state audit passed: ε=4.820e-08, max compatibility=4.822e-08, max canonical=5.962e-14, period residual=2.890e-12.

## Interpretation

This is a one-point, one-history finite-χ continuation, not a global-minimum certificate or transition verdict. Numerical residuals and contraction residuals are acceptance diagnostics, not free-energy error bars. A single rate cannot locate a spinodal or determine transition order. No follow-up rate or stability/gap calculation is inferred.

Artifacts: `v2.2/verify/replica/n3_branch192_upper_retry1.json`, `branch192_upper_retry1_benchmark.json`, worker logs, and—only if a production state is saved—the retry1 checkpoint and independent audit.

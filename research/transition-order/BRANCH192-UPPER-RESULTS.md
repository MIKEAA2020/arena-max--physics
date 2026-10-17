# χ192 single ordered-history step at p=.30485

17 October 2026 · separately authorized one-rate continuation · finite-χ test, not a transition verdict.

**Status:** feasibility gate failed; production not launched.

## Scope and cap

The user authorized exactly one ordered-history χ192 continuation at p=.30485, warm-started from the accepted ordered χ192 state at p=.30480. This is a fresh five-hour absolute cap. The disposable enlargement benchmark and runtime/memory gate precede production; if the projected optimizer plus setup and validation reserve does not fit, production is not launched. No other p, second preparation, excited-state/gap computation, perturbation or stability test is in scope.

Acceptance remains unchanged: primary and both compatibility residuals <1e−7, canonical defects <1e−9, positive full-period trial contraction with relative defect <1e−8.

## Frozen references

Accepted χ192 source: `v2.2/verify/replica/checkpoints/branch192_retry1_ordered_p0.3048000.npz`, SHA-256 `d15055d94d8a527a698a7967f468704d4c5cdaf1513c2388198170f0652ca1da`; source order diagnostic L2 = 0.47912668.
Same-p χ128 upper-rate reference: `v2.2/verify/replica/checkpoints/branch128_upper_ordered_p0.3048500.npz`, accepted in 205 iterations at p=.30485, terminal color L2 0.00059494. This is the prior upper-rate warm-history reference, not a χ192 result.

## Disposable one-step benchmark

Iterations: 1; VUMPS time per step: 87.33s; total wall time including operator construction: 87.34s; peak RSS: 168784 KiB; finite output: True. No state checkpoint was written.

## Feasibility decision

Projection: 205 iterations × 87.33s/step + 120s setup + 900s validation = 18923.66s, versus 17912.24s remaining after benchmark.
Memory forecast: measured peak 168784 KiB; available memory 1384324 KiB. Gate decision: **STOP after feasibility benchmark; do not launch production**.

**No optimizer state at p=.30485 was produced.** Only the disposable one-step benchmark ran. The feasibility gate stopped before production; therefore there is no p=.30485 order diagnostic or phase inference.

## Interpretation

Comparison to χ128 is only a one-point, one-history finite-χ retention check. If a production optimizer was launched and retained high order, that would show this warm path remains ordered at .30485; if it lost order, that would show only that this unconstrained optimizer path changed character. Neither case identifies the thermodynamic transition point or order.

All optimizer residuals and transfer-contraction residuals are numerical acceptance diagnostics, not free-energy error bars. A VUMPS state is not certified globally minimal. Transition order remains unresolved.

Artifacts: `v2.2/verify/replica/n3_branch192_upper.json`, `branch192_upper_benchmark.json`, its log, and (only if production passed the gate) the named `.30485` result/checkpoint plus `branch192_upper_state_audit.json`.

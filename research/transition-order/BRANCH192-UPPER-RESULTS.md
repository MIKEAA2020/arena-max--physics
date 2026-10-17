# χ192 single ordered-history step at p=.30485

17 October 2026 · separately authorized one-rate continuation · finite-χ test, not a transition verdict.

**Current status:** the original five-hour gate failed; a later authorized one-hour extension passed and launched production. The worker then disappeared without a final result or saved target checkpoint. The six-hour absolute cap has now expired; there is no accepted p=.30485 χ192 observation.

## Scope and cap

The user authorized exactly one ordered-history χ192 continuation at p=.30485, warm-started from the accepted ordered χ192 state at p=.30480. The initial authorization set a fresh five-hour cap. A later addendum extended the absolute cap to six hours from the original start. The disposable enlargement benchmark and runtime/memory gate preceded production; the original gate failed, then the extension gate passed. No other p, second preparation, excited-state/gap computation, perturbation or stability test is in scope.

Acceptance remains unchanged: primary and both compatibility residuals <1e−7, canonical defects <1e−9, positive full-period trial contraction with relative defect <1e−8.

## Frozen references

Accepted χ192 source: `v2.2/verify/replica/checkpoints/branch192_retry1_ordered_p0.3048000.npz`, SHA-256 `d15055d94d8a527a698a7967f468704d4c5cdaf1513c2388198170f0652ca1da`; source order diagnostic L2 = 0.47912668.
Same-p χ128 upper-rate reference: `v2.2/verify/replica/checkpoints/branch128_upper_ordered_p0.3048500.npz`, accepted in 205 iterations at p=.30485, terminal color L2 0.00059494. This is the prior upper-rate warm-history reference, not a χ192 result.

## Disposable one-step benchmark

Iterations: 1; VUMPS time per step: 87.33s; total wall time including operator construction: 87.34s; peak RSS: 168784 KiB; finite output: True. No state checkpoint was written.

## Original five-hour feasibility decision (preserved)

Projection: 205 iterations × 87.33s/step + 120s setup + 900s validation = 18923.66s, versus 17912.24s remaining after benchmark.
Memory forecast: measured peak 168784 KiB; available memory 1384324 KiB. Gate decision: **STOP after feasibility benchmark; do not launch production**.

**Historical note:** at the original five-hour gate, no optimizer state had been produced and production had not launched. A later cap-extension decision superseded that stop; see the execution update below. No accepted or audited p=.30485 state is available.

## One-hour extension and subsequent execution interruption

The user authorized one additional hour, changing the absolute cap from five to six hours measured from the original campaign start. The original frozen protocol and failed five-hour gate remain unchanged. The extension gate reused the disposable benchmark and unchanged forecast: 205 iterations × 87.33s plus setup and validation = 18923.66s. At the extension decision, 19636.05s remained; forecast headroom was 712.39s. Runtime and memory gates passed, and the single production worker was launched.

Afterward, the worker no longer appeared in the process table. Its durable result record remains at status `running`; its log is 0 bytes, and the named p=.30485 checkpoint exists: False. The actual number of optimizer iterations completed is unknown; no final result or independent state audit exists. The six-hour deadline expired at Unix time 1792218960 before this interruption was documented. **No restart is authorized by the expired cap.** A renewed explicit cap is required before another attempt.

Interruption evidence: `research/transition-order/branch192-upper-interruption.json`; extension authorization/gate: `branch192-upper-extension-addendum.json`.

## Interpretation

Comparison to χ128 is only a one-point, one-history finite-χ retention check. If a production optimizer was launched and retained high order, that would show this warm path remains ordered at .30485; if it lost order, that would show only that this unconstrained optimizer path changed character. Neither case identifies the thermodynamic transition point or order.

All optimizer residuals and transfer-contraction residuals are numerical acceptance diagnostics, not free-energy error bars. A VUMPS state is not certified globally minimal. Transition order remains unresolved.

Artifacts: `v2.2/verify/replica/n3_branch192_upper.json`, the worker execution record and log, and `research/transition-order/branch192-upper-interruption.json`. No accepted target checkpoint, final optimizer record, or independent state audit exists.

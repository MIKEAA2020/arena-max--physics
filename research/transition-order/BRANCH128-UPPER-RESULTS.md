# χ128 second-common-rate test: p=.30485

16 October 2026 · A-1 continuation · one paired rate only.

**Status:** complete: both upper-rate numerical states accepted. The user authorized exactly one additional common rate, warm-continued from the accepted .30480 pair. No χ192, additional rate or stability production is included.

## Prospective protocol

Both accepted .30480 physical MPS states initialize the same zero-bias operator at .30485. The external gates are unchanged: primary and both compatibility residuals <1e-7, canonical defects <1e-9, positive period contraction with relative defect <1e-8. The internal driving goal is 5e-8 for a safety margin, not a new external criterion. Maximum overall allocation is 60 minutes, with two single-thread CPU workers; 55 minutes are available to optimization and time is reserved for validation/comparison.

A failed gate is not rounded into a pass. If the internal driving budget ends, the actual saved state is evaluated under the original external gates; a numerical state is accepted only if those complete checks pass. No pinning field or phase constraint forces a family to persist.

## Upper-rate numerical outcomes

| History | Status | Primary residual | Right compatibility | Color L2 | m_species | xi_chi |
|---|---|---:|---:|---:|---:|---:|
| ordered-start history | accepted upper-rate numerical state | 4.931426e-08 | 4.935708e-08 | 0.00059494 | 0.00060023 | 61.8615 |
| disordered-start history | accepted upper-rate numerical state | 4.826692e-08 | 4.833463e-08 | 0.00419878 | 0.00442549 | 63.8667 |

History labels are not automatically phase identities. An observed change/merger or numerical failure is not a measured physical spinodal or a bound on a thermodynamic metastability-window width.

## Same-objective pressure estimates

| p | Half-row O | Half-row D | Δf_half (O−D) | Period trial O | Period trial D | Δf_period,trial |
|---:|---:|---:|---:|---:|---:|---:|
| 0.30480 | 0.992869885471 | 0.992871751622 | -1.866150e-06 | 0.992869864438 | 0.992871518919 | -1.654481e-06 |
| 0.30485 | 0.993030549778 | 0.993030537045 | 1.273331e-08 | 0.993030341465 | 0.993030337815 | 3.649566e-09 |

The primary stationary objective is the Hermitian half-row functional. Full-period values are separate trial evaluations, not independently converged full-period branch optima. Do not mix the two columns into one pressure bracket. Last digits are numerical contraction outputs, not global error bars.

## Numerical similarity and pressure-sign diagnostics

Upper-rate symmetry comparison: all 36 symmetry orientations evaluated; largest evaluated aligned fidelity/site **0.999999504453**.

Half-row ranking sign change between the two endpoints: **True**. Period-trial ranking sign change: **True**. These are arithmetic diagnostics only, not coexistence certificates.

## Completed outcome: no retained two-family bracket

Both upper-rate numerical states passed every original gate. However, the large-order history changed from invariant order 0.48823244 at .30480 to **0.00059494** at .30485; the other upper-rate history has **0.00419878**. The upper endpoint therefore does not supply a retained large-order/small-order pair. The high aligned fidelity is a similarity diagnostic, not certified exact identity.

Although both tabulated ranking differences change sign, the upper O-history value now belongs to a small-order approximant. It cannot be relabeled as the ordered-phase branch pressure. Consequently **no retained large-/small-order pressure-crossing bracket was obtained** by this single-step test.

This does not invalidate the distinct constructed states previously retained at .30480. It says only that the selected unbiased warm step did not retain the large-order character at .30485. The test does not prove that such a branch is absent there, identify a physical spinodal, or give a thermodynamic retention-window width. A finer continuation step or different validated branch-following control would require separate authorization; none was run.

Read-only actual-AL-density audit gives upper invariant order 0.0005949339 / 0.0041987751, confirming the small-order endpoint diagnostics independently of the center-tensor estimate. This is not a perturbation or stability test.

## Interpretation safeguards

A candidate finite-χ pressure bracket requires two distinguishable, symmetry-inequivalent numerical families retained at BOTH endpoints and compared using the SAME objective. A sign change between nearly equivalent outputs after a history has merged is not such a branch crossing. A direct warm step that loses character does not locate a physical spinodal or prove how wide the retention window is.

Even if endpoint data support a candidate finite-χ bracket, this allocation does not supply local perturbation stability, global optimality, a physical coexistence point, a thermodynamic order-parameter jump, or χ/size-extrapolated transition order. Those are separately gated. If ordering does not flip, only the ranking of these computed trial states at these rates is known; no theorem places the thermodynamic transition further up.

Optimizer residuals are NOT free-energy-error bars. Comparing a pressure difference numerically to a residual does not yield a calibrated signal-to-error ratio. A lower trial functional among two states does not certify a global minimum, even at this χ. Finite-χ bias and optimizer systematics remain unbounded globally.

**Thermodynamic verdict remains unresolved.** The earlier six-rate data and original stopped pilot are preserved; the accepted same-point refinement is a separate numerical amendment. The Qur’anic/Lighthouse creator–creation interpretation and mathematical statements are not changed by these numerical outcomes.

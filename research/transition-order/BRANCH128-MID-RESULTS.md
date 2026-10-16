# χ128 closer-common-rate test: p=.304825

16 October 2026 · A-1 continuation · one paired rate only.

**Status:** complete: both closer-rate numerical states accepted. The user authorized exactly one additional common rate, warm-continued from the accepted .30480 pair. No χ192, additional rate or stability production is included.

## Prospective protocol

Both accepted .30480 physical MPS states initialize the same zero-bias operator at .304825. The external gates are unchanged: primary and both compatibility residuals <1e-7, canonical defects <1e-9, positive period contraction with relative defect <1e-8. The internal driving goal is 5e-8 for a safety margin, not a new external criterion. Maximum overall allocation is 60 minutes, with two single-thread CPU workers; 55 minutes are available to optimization and time is reserved for validation/comparison.

A failed gate is not rounded into a pass. If the internal driving budget ends, the actual saved state is evaluated under the original external gates; a numerical state is accepted only if those complete checks pass. No pinning field or phase constraint forces a family to persist.

## Closer-rate numerical outcomes

| History | Status | Primary residual | Right compatibility | Color L2 | m_species | xi_chi |
|---|---|---:|---:|---:|---:|---:|
| ordered-start history | accepted closer-rate numerical state | 4.997934e-08 | 5.129809e-08 | 0.46438614 | 0.49280272 | 88.9092 |
| disordered-start history | accepted closer-rate numerical state | 4.977077e-08 | 4.987014e-08 | 0.00582262 | 0.00618003 | 67.8047 |

History labels are not automatically phase identities. An observed change/merger or numerical failure is not a measured physical spinodal or a bound on a thermodynamic metastability-window width.

## Same-objective pressure estimates

| p | Half-row O | Half-row D | Δf_half (O−D) | Period trial O | Period trial D | Δf_period,trial |
|---:|---:|---:|---:|---:|---:|---:|
| 0.304800 | 0.992869885471 | 0.992871751622 | -1.866150e-06 | 0.992869864438 | 0.992871518919 | -1.654481e-06 |
| 0.304825 | 0.992950730534 | 0.992951166473 | -4.359393e-07 | 0.992950698762 | 0.992950951646 | -2.528837e-07 |

The primary stationary objective is the Hermitian half-row functional. Full-period values are separate trial evaluations, not independently converged full-period branch optima. Do not mix the two columns into one pressure bracket. Last digits are numerical contraction outputs, not global error bars.

## Numerical similarity and pressure-sign diagnostics

Closer-rate symmetry comparison: all 36 symmetry orientations evaluated; largest evaluated aligned fidelity/site **0.997919994252**.

Half-row ranking sign change between the two endpoints: **False**. Period-trial ranking sign change: **False**. These are arithmetic diagnostics only, not coexistence certificates.

## Completed closer-point retention finding

At .304825 the accepted histories have invariant order 0.46438614 / 0.00582262. These diagnostics retain a large/small constructed-state contrast, rather than merely opposite symmetry orientations. This is numerical retention, not a physical phase or stability certificate.

No sign reversal of the half-row objective was observed between .30480 and .304825. Thus this test supplies another retained numerical pair but no pressure bracket across those two endpoints. Ranking of these constructed trials alone does not place the thermodynamic transition or certify global optimality.

Full-period trial-ranking signs are a separate diagnostic; they are not mixed with half-row objective signs into one crossing.

## Interpretation safeguards

A candidate finite-χ pressure bracket requires two distinguishable, symmetry-inequivalent numerical families retained at BOTH endpoints and compared using the SAME objective. A sign change between nearly equivalent outputs after a history has merged is not such a branch crossing. A direct warm step that loses character does not locate a physical spinodal or prove how wide the retention window is.

Even if endpoint data support a candidate finite-χ bracket, this allocation does not supply local perturbation stability, global optimality, a physical coexistence point, a thermodynamic order-parameter jump, or χ/size-extrapolated transition order. Those are separately gated. If ordering does not flip, only the ranking of these computed trial states at these rates is known; no theorem places the thermodynamic transition further up.

Optimizer residuals are NOT free-energy-error bars. Comparing a pressure difference numerically to a residual does not yield a calibrated signal-to-error ratio. A lower trial functional among two states does not certify a global minimum, even at this χ. Finite-χ bias and optimizer systematics remain unbounded globally.

**Thermodynamic verdict remains unresolved.** The earlier six-rate data and original stopped pilot are preserved; the accepted same-point refinement is a separate numerical amendment. The Qur’anic/Lighthouse creator–creation interpretation and mathematical statements are not changed by these numerical outcomes.

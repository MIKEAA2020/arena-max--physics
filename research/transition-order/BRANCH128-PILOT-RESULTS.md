# χ128 unbiased branch-following pilot

16 October 2026 · A-1 continuation · numerical retention test, not an order verdict.

**Status:** stopped: stage 2 acceptance gate not passed for both histories. The user separately authorized at most three hours overall, with at most two single-thread CPU workers. No χ192, extra crossing point or perturbation production is automatic.

## Protocol and objective

Large-order history: accepted p=.30470 → .30475 → .30480. Small-order history: accepted p=.30486 → .30483 → .30480. The stage-1 targets differ, so their energies must not be compared as a same-p branch gap. Stage 2 starts only after both stage-1 results pass the unchanged numerical gates. Every step loads the actual previous accepted MPS, not a cached scalar or a reset to the old grid initializer.

The objective is the unchanged Hermitian half-row transfer-MPS functional, with residual and left/right compatibility below 1e-7, canonical checks below 1e-9 and full-period contraction defect below 1e-8. No phase, order-parameter or pinning constraint is imposed. A history can lose its original character; it is not forced to survive as a branch.

Half-row stationarity and full-period trial evaluation are different finite-χ objects. Both functionals are reported separately; do not mix them to infer a crossing. A local stopping test does not certify a global minimum, a physical spinodal or stability against all perturbations.

## Accepted anchors

| History | Anchor p | Color L2 | f_half | f_period_Rayleigh |
|---|---:|---:|---:|---:|
| ordered-start history | 0.30470 | 0.528373 | 0.992545683809 | 0.992545675311 |
| disordered-start history | 0.30486 | 0.003719 | 0.993062273705 | 0.993062080172 |

These anchors are at different rates and are not a coexistence pair. Their original accepted checkpoint hashes are retained.

## Continuation steps

| Stage | History | p | Status | Residual | Color L2 | f_half | f_period_Rayleigh |
|---:|---|---:|---|---:|---:|---:|---:|
| 1 | ordered | 0.30475 | accepted-finite-chi | 8.194e-08 | 0.513220 | 0.99270791085 | 0.99270789853 |
| 1 | disordered | 0.30483 | accepted-finite-chi | 9.913e-08 | 0.005362 | 0.99296704401 | 0.99296683247 |
| 2 | ordered | 0.30480 | accepted-finite-chi | 9.065e-08 | 0.488232 | 0.99286988547 | 0.99286986444 |
| 2 | disordered | 0.30480 | iteration-cap-or-stationarity-check-failed | 9.996e-08 | — | — | — |

Missing or rejected results are not zero and are not stationary branch observations. If a step fails, its path stops; it is not promoted by skipping to the next target.

## Common-target comparison

No two accepted common-target results yet; no energy-gap or coexistence inference is made.

## Exact validation failure — not rounded into acceptance

The common-target small-order history passed the primary optimizer tolerance (9.995603786506e-08), but its right compatibility defect was **1.000165012751e-07**, above **1e-7** by 0.016501%. The right gate was not relaxed. No full-period value was evaluated for this rejected step, and no accepted common-target branch comparison was constructed. This is a numerical gate failure, not evidence of a physical phase or spinodal.

A same-point safety refinement with a stricter internal goal and unchanged external gates is described in CONVERGENCE-REFINEMENT.md. It requires separate authorization; the original failed attempt remains preserved.

## Limits and next gates

This pilot samples continuity/retention from accepted anchors. It does not compute exact continuous free-energy functions. If both histories reach a similar family, that does not prove continuity; if distinct finite-χ states survive, that does not prove first order. A nonzero trial free-energy gap at one p is not coexistence.

A candidate crossing requires retained symmetry-inequivalent stationary families at at least another common rate, a controlled same-objective pressure bracket, and stability/χ/size-systematic analysis of a non-vanishing discontinuity. Perturb-and-return checks are not performed by this allocation; an exact fixed point remaining fixed is not a stability test. No physical spinodal or latent heat is certified.

For an ordinary continuous transition f′ is continuous while higher derivatives can be singular. A kink in f normally means a first-derivative jump in a generic tuning direction. Sharpening with χ can occur for continuous transitions as finite-entanglement rounding recedes.

**Thermodynamic order remains unresolved.** The original six-rate data, v33 and the v34 creator–creation interpretive governance remain preserved. No numerical result is inferred from theology or vice versa.

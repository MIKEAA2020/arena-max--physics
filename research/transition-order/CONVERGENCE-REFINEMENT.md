# Proposed same-point convergence-safety refinement

16 October 2026 · A-1 · **Proposal retained; the user subsequently selected `refine_same_point`, authorizing a separate at-most-30-minute refinement. Actual execution is in `branch128-refinement-protocol.json` and `BRANCH128-REFINEMENT-RESULTS.md`.**

The declared pilot stopped correctly with 3/4 continuation steps accepted. At p=.30480, the small-order history passed the primary optimizer test (9.995603786506007e-8), but its directly measured right compatibility defect was 1.0001650127505745e-7, above the strict 1e-7 ceiling by about 0.0165%. This is not rounded into a pass. The original rejected record and real MPS checkpoint are retained. A process exit of zero is not scientific acceptance.

The clean numerical repair is not to loosen the external threshold. Instead, separately authorize a short same-point refinement from the saved physical state, with a stricter **internal optimizer goal of 5e-8** and the **original external acceptance gates unchanged**. The operator, rate p=.30480, chi=128, phase-unbiased objective, and full-period contraction requirements remain unchanged. No new rate, branch pressure bracket, perturbation stability run or chi192 is included.

Proposed cap: **30 minutes**, including reserved time for geometry/period validation. The failed target is an approximate starting state for further refinement, not an accepted branch observation. Its original ancestry from the accepted .30483 state is retained. New results go in separate refinement files; the original pilot remains recorded as having stopped at its gate.

Acceptance still requires primary residual and BOTH compatibility residuals below 1e-7, canonical identities below 1e-9, a positive full-period contraction with relative defect below 1e-8, and actual state/checkpoint checks. An internal target is a convergence-driving parameter, not a replacement for these external acceptance tests. No rejected or partial state is promoted by rounding. If the unbiased refinement changes the state's order character, that outcome is recorded; its former character is not forced to persist.

Only if the refined state passes may it augment the common-target comparison with the already accepted large-order result. That would still be a finite-chi numerical comparison at one common rate, not a coexistence location, physical metastability certificate or thermodynamic order verdict. The original three-hour pilot is not silently restarted or its failure erased.

## Separate authorization

The user selected the same-point convergence-safety amendment after seeing the exact failed norm. Only the stated 30-minute, stricter-internal-goal refinement is authorized. External gates, unbiased objective, p and χ remain unchanged; prior rejection and tensors remain immutable.

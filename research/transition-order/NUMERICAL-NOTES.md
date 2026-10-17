# Numerical execution notes

## 2026-10-16: validation gate

Exact half/full identities passed for n=2,d=2; n=3,d=2; n=3,d=3; n=4,d=2. The raw non-Hermitian half-row optimizer failed a complex-eigenvalue check and was rejected. Production uses the globally Hermitian direct sum and paired environments, not a real-part workaround.

The Ising ladder converged at tolerance 1e-8 through chi=64. n=3 gapped controls at p=.300 and .310 show a shrinking half/full Rayleigh discrepancy. Some lower-chi control stages hit the iteration cap; the final chi=48 p=.310 residual is 1.17e-8, close to but above that run's nominal 1e-8, and below the 3e-8 calibration ceiling. These statuses remain in the raw JSON. This is not a statement that every control run converged at its requested tolerance.

Primary production tolerance is 1e-7, with 400 iterations and a 900-second optimizer-stage ceiling; states checkpoint every 20 iterations and on convergence/budget stop. This tolerance alone does not certify free-energy convergence. A tighter matched-branch continuation is required before an order verdict.

## 2026-10-16: disordered chi=48 continuation did not converge

The .310→.306, chi=48 stage reached 400 iterations, residual 2.11e-7 against requested 1e-7. It is stored as **unconverged**, not an accepted stationary phase. The default driver stopped rather than silently proceeding.

A documented retry is permitted: use that real MPS checkpoint **only as an initialization**, enlarge to chi=72 at the same p=.306, and require the new optimizer stage to pass before continuing toward .305. This tests whether additional variational freedom improves optimization. It does not turn the lower-chi observation into a converged result, nor prove that truncation caused the failure. The explicit queue is `cases-disordered-retry.json`; the default non-advancement rule remains in place. If that retry fails, preserve its checkpoint and report the budget/iteration limitation rather than changing tolerances retrospectively.

## 2026-10-16: fourth-moment ladder

All 52 Haar/Clifford cases (13 rates × L=4,6 × two ensembles) completed with all five S4-left/right sectors. Maximum absolute eigenpair residual: 1.18e-10. The fourth Clifford transfer is built on 30 closed labels with Gram rank 29 and a pseudoinverse quotient. L=8 is gated by a measured memory/runtime benchmark, not launched as an unbounded ladder.

## 2026-10-16: exact arithmetic-preserving contraction improvements

The Hermitian MPO's exact global-direct-sum blocks are now contracted separately. The paired environment `(B,B^T)` is an exact invariant subspace; its eigenproblem is solved using B alone and then reconstructed. **Both summands remain in the center map**. Dense/block and paired-map identities were checked to roundoff; the expanded transfer extension passed **49/49** freshly. The earlier integrated driver had passed 241/241 with its then-44-check extension. Final accounting is updated only from a completed fresh integrated run.

The ordered chi=128 stage was interrupted at a saved checkpoint to use these equivalent contractions, then exhausted its resumed 900-second optimizer-segment budget without reaching tolerance. Its two segment times are retained; neither the restart nor the new contractions imply that the sum of those times was below 900 seconds. The approximate state is retained, not called a converged chi=128 result.

## 2026-10-16: feasibility re-triage to the matched-rate test

The disordered chi=72 gapped retry plateaued just above 1e-7 and was stopped after 200 saved iterations at residual 1.044e-7. It remains unconverged. A documented critical-rate retry used that state only as initialization at chi=96,p=.305; that new stage **did** converge (residual 9.90e-8, 75 iterations). Its later chi=128 expansion was resource-triaged before convergence after the ordered chi=128 budget failure. The two chi=128 partial states are frozen separately.

To prioritize the central comparison rather than automatically launch chi=192, two fresh chi=96 continuation chains were scheduled prospectively at p=.30486 and .30490, in opposite directions, with tolerance 1e-7, maximum 300 iterations and a 750-second per-point optimizer-segment ceiling. Larger chi is deferred on the measured runtime/convergence evidence; it is not a claim that larger-chi MPS is impossible in a better implementation or larger budget.

The common-rate initializations are explicitly approximate Schmidt-based reductions of the saved chi=128 states, re-canonicalized in both gauges. Discarded one-cut weights are 3.10e-7 and 1.03e-6; these are **not** global/free-energy error bounds. Initial seed gauge errors are about 1e-14 (isometries) and 1e-12 (compatibility). The helper passed a fresh, separately logged smoke test; this is not added to the 49 counted checks. The fresh common-rate optimizer must independently pass before any phase/free-energy comparison is accepted. A stopped or seeded state is never substituted for such a comparison.

## 2026-10-16: cheap secondary computations completed

The n=3,d=3 finite-size cache has 67 exact cases and four root-solved crossings (root tolerance 3e-6); all eight bidirectional small-chi pilot cases converged at their requested tolerances. The fourth-Haar fully monitored endpoint and a chi=4,p=.38 MPS pilot also converged. A transient pilot JSON serialization error from a NumPy Boolean was fixed; the queue stopped on that error and was restarted after the fix, rather than silently treating the incomplete serialization as a saved result.

The fourth-Clifford L=8 projected-matvec benchmark measured 3.115 seconds, exceeding the prospectively adopted 1-second gate. The larger ladder is **deferred after a measured runtime gate**, not reported as attempted/converged and not called scientifically impossible. No higher-size critical-point split is inferred.

Legacy verification wording was narrowed without changing its tested condition: check 17 means no parity-only **sample among the loaded chi=24..72 rows**, not exclusion of an intermediate thermodynamic phase. The n=4 finite-spectrum header now distinguishes its default diagonal-sector scan from the general left/right projector and from a full spectrum. The paper-specific 17-check suite is re-run after this text-only clarification; no extra checks are added to the total.

## Final snapshot outcome

The common-rate chi=96,p=.30486 attempts did not satisfy tolerance before their prospective 750-second ceilings. Saved outcomes: ordered: budget-stopped, residual 8.753e-07, 153 iterations, 752.3 seconds; disordered: budget-stopped, residual 8.302e-07, 154 iterations, 751.7 seconds. The disordered-start p=.30490 point converged; the ordered-start .30490 point was not launched after its preceding failure. **No accepted stationary matched-rate pair is claimed.**

Six frozen-trial full-period Rayleigh evaluations at matched p=.30486,.30488,.30490 completed with small contraction residuals. These compare actual normalized trial MPS states, not converged stationary phases. They do not supply a global variational/truncation error bound or a latent-heat/order verdict. All campaign numerical workers have now stopped; remaining work is explicitly deferred or open.

## Authorized chi128 stage — completed outcome

ordered: accepted-stationary-at-finite-chi, eps=9.991478996514631e-08, iterations=186, total stage 2507.1s; disordered: accepted-stationary-at-finite-chi, eps=9.56534706713505e-08, iterations=79, total stage 1022.8s.

2/2 preparations passed the prospective acceptance gates at p=.30486. This does not decide first order versus continuous. At completion of this stage, before the later separate χ192 authorization, chi192 had not been launched and no campaign numerical production remained running. The earlier chi96 failures do not establish two stationary phases. See `CHI128-STAGE.md` for the interpretation contract and logical counterexamples.

## Completed six-rate chi128 scan

All six paired rates passed (10 new targets plus 2 reused reference states), with unchanged 1e-7 tolerance. Lower sampled rates .3040,.3045,.3047 have large order diagnostics, higher .30486,.3050,.3055 small ones. Symmetry-aligned comparisons are close at each rate. This does not establish first order or continuity; the fixed-chi sampled change interval .3047–.30486 is not a thermodynamic confidence interval. No χ192 was launched. The session interruption and saved-segment lower-bound times remain recorded; no exact end-to-end CPU total is inferred from them.

## One upper common rate — completed outcome

At .30485, chi128, both warm continuations passed unchanged external gates and the internal 5e-8 goal. The former large-order history took 205 iterations/3206.8 seconds; the other history took 33/538.2 seconds. Both final order diagnostics are small. Arithmetic pressure-sign reversals do not identify a retained ordered/disordered crossing because upper family character changed. This result does not prove a physical spinodal, missing branch, exact window width or transition order. No extra rate, chi192 or stability test was launched at that stage.

## Subsequent authorized chi192 same-p enlargement

A later, separate five-hour authorization tested only the two accepted chi128 p=.30480 source MPS at chi=192. Both corrected-run outputs passed unchanged external gates (116 and 72 iterations). The continuation from the low-order chi128 input moved to a high-order chi192 solution (color L2 .479027); it was nearly the same symmetry orbit as the ordered-start result (L2 .479127; 36-orientation maximum normalized fidelity per site .999999996013). Thus low-order branch retention was **not** observed along this enlargement path, but no theorem/thermodynamic branch-absence or order conclusion follows. See `BRANCH192-RESULTS.md`, the immutable staged protocol/addenda and independent `branch192_state_audit.json`. The first failed serialization attempt is retained, and the corrected retry stayed inside the original five-hour deadline. No other rate or stability work was run.

### Single χ192 upper-rate feasibility gate

The user then authorized one ordered-source p=.30485 follow-up, benchmark-first under a fresh five-hour cap. The disposable χ192 step measured 87.335s/iteration; the relevant accepted χ128 same-p ordered-history reference took 205 iterations. With the frozen 120s setup and 900s validation reserves, the forecast was 18,923.66s versus 17,912.24s remaining after the benchmark. Memory passed, runtime failed. Production was **not launched**; no p=.30485 χ192 MPS, order, energy, or collapse measurement exists. See `BRANCH192-UPPER-RESULTS.md` and `branch192-upper-protocol.json`.

### χ192 p=.30485 extension interruption

The user authorized one extra hour (six hours total from the original start). The unchanged forecast/runtime and memory gates passed and the single ordered production worker was launched. No final optimizer record, saved target checkpoint, or independent audit was produced before the worker disappeared; its log is empty and iteration count is unknown. The absolute cap has expired. There is no p=.30485 χ192 order, energy, or collapse observation; any restart requires renewed user authorization. See `BRANCH192-UPPER-RESULTS.md`.

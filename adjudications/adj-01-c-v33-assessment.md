# User-supplied assessment: the v33 improvement plan

Received 16 October 2026 (Asia/Tehran). This is input to adjudication A-1, not a numbered clue.

## The plan's spine is correct

The retract-vs-reframe decision is the right one. The class claims are contradicted, not unproven. A reader who sees only the abstract would be misled by "hypothesis tested and corrected." Retraction lets the paper state both the certain part (withdrawal) and the graded part (weakly first-order most likely, continuous not excluded at χ ≤ 96).

The identification of durable content is accurate: the exact channel/rank/closure theory, the n = 2 Ising point (credited to Bao–Choi–Altman), the record multifractality formalism, and the Clifford dyadic identity. These stand independently of the phase-transition dispute.

## The strongest upgrade: q = n!

The observation that the order parameter is the regular S_n-bimodule, and that the coexisting ordered states number q_eff = n!, is the most important new structural finding in the plan. It explains the whole ladder coherently: n = 2 is continuous (q_eff = 2, Ising), n ≥ 3 is first-order with strength increasing in n (q_eff = 6, 24, 120), and the changeover n* sits in (2, 3). The Vasseur–Potter–You–Ludwig large-bond-dimension q = n! result is the right connection, and it was already in the paper's own citation list.

This is a genuine reframing that turns the retraction into a sharper structural claim. The plan is right that it belongs in the abstract.

## The cleanest new test: the Clifford coexistence SMC

The tilted stabilizer SMC at p_c = 0.3049 is the plan's best proposal. It is sign-free, truncation-free, and cheap (L = 64–256, workstation-scale). It closes the one gap the VUMPS evidence leaves open — whether the coexistence correlation length saturates (first-order) or grows (continuous) — by an independent method. The paper already owns the estimator and the tableau code; only the tilt exponent and rate change.

If this runs, it settles the order of the n = 3 transition without the χ ≥ 96 caveat. That is the single highest-value computation in the plan.

## Where the plan should be more careful

**1. The n* ∈ (2, 3) claim is conditional on n = 3 being first-order.** The VUMPS result is "weakly first-order, most likely; continuous non-Potts with ξ ≥ 60 not excluded at χ ≤ 96." If the Clifford SMC shows a continuous transition, n* is not in (2, 3). The plan should state the conditional explicitly: if n = 3 is first-order, then n* ∈ (2, 3) and the ladder is q = n! from n = 3; if n = 3 is continuous with strong corrections, the changeover is at higher n and the q = n! story changes shape.

**2. The n = 4 claim is weaker than the plan sometimes says.** The plan notes it rests on one sector at L ≤ 10. But L ≤ 10 is smaller than L ≤ 18, which is already smaller than ξ_coex(3) ≈ 40–60. So the n = 4 crossings (0.358, 0.379) are even more crossover-contaminated than the n = 3 crossings were. The retraction of the n = 4 claim should be unqualified, not "unestablished pending VUMPS."

**3. "The paper already owns the exact machinery" is fair for the operators, less so for the method.** The L ≤ 18 exact-diagonalization method was unreliable for the phase-transition question. The upgrade is to use the machinery with the right method (VUMPS, tilted SMC), not to use the machinery as-is. The plan mostly says this, but the framing should be explicit in the abstract.

**4. The continuation to n → 1 is a conjecture, not a consistency check.** The plan correctly flags "there is no a-priori analyticity in n: the integer-n models have different symmetry groups." But the p_c(1) ≈ 0.16–0.17 bracket is presented as "the first quantitative consistency check that the annealed ladder is the replica continuation of the Born-rule transition." That overstates it. Three fit forms give 0.156, 0.163, 0.167–0.170 — a spread of ~0.014, comparable to the distance between the Clifford and Haar values. The fit is suggestive, not a check. Keep it as a conjecture with the fits shown.

## What the plan gets exactly right

- The five-year-program framing (§6): large-d structure stated, Pirogov–Sinai program named for feasibility-unknown, cluster representation named as the frontier. This is honest and well-targeted.
- The "retrospective subsection" (§7) as a result, not an apology. The L ≤ 18 crossover story is methodologically valuable and belongs in the body.
- The Clifford–Haar splitting at n = 4 as the first appearance of magic in annealed replica physics. This is a genuinely new publishable object, and the Gross–Nezami–Walter 30-label transfer matrix makes it exactly computable.
- The re-calibration of the size-ladder test (§5.5): the n = 3 "continuous control" was itself first-order, so the L ≤ 8 diagnostics rank ξ_coex/L, not order. The n = 5 conclusion survives; its logic changes.
- The decomposition into "retract at the headline, reframe in the body." The abstract must be corrected; the body can exhibit the reasoning.

## What I would add

**The complexity results are unaffected and should stay in the abstract.** CTD and CPD PostBQP-complete (Appendix C) are independent of the phase-transition dispute. They are among the paper's cleanest contributions. The plan mentions them as durable but does not emphasize they survive the retraction untouched.

**The record LDP results are also unaffected and should stay.** The no-freezing theorem (Theorem 9), the interpolation identity (Prop. 8), the first numerical quenched record SCGFs for Haar circuits, the Clifford record-count closure (Props. 10–13) — all stand. The plan treats them as "a face of f(n,p)," which is coherent, but they are also independently publishable.

**The interpretive section VII should be checked.** The "record as appearance-stream" framing does not depend on the Potts claim, but the specific connection to "the paper's theorems" (which included the Potts ladder) might need adjustment. Minor, but worth a pass.

## The honest bottom line

This is a serious, well-structured improvement plan. It correctly identifies what stands and what falls, gives a concrete path to a stronger v33, and is honest about its own limits. The q = n! reframing and the Clifford coexistence test are the two highest-value additions. The retraction recommendation is correct.

The main caveat: the n* ∈ (2, 3) claim should be stated as conditional on n = 3 being first-order. If the transition is continuous, the changeover moves and the q = n! story shifts. The plan should not present n* ∈ (2, 3) as settled; it should present it as the consequence of the VUMPS result and the prediction of the Clifford SMC test.

If the author follows the plan, the corrected paper is stronger than the original. Not because the original was bad, but because the retraction is honest, the q = n! reframing is sharper than the q = n claim, and the new tests (Clifford SMC, VUMPS at χ ≥ 96, n = 4 magic) are concrete and computable.

# χ192 paired-history test at p=.304825

17 October 2026 · separately authorized paired one-rate test · finite-χ branch-retention evidence only.

**Status:** paired preparations accepted and independently audited.

## Authorization and protocol

The user authorized one rate with two ordered histories, run sequentially by one single-thread worker under a fresh 12-hour absolute cap. The ordered preparation starts from the accepted χ192 p=.30480 state; the small-order preparation starts from the accepted χ192 p=.30485 state. Both target p=.304825 with identical gates and objective. No other rate, gap/excited-state, perturbation or stability calculation is included.

These histories test whether both numerical characters are retained at the same finite χ and same p. A two-state result at one p does not itself locate a coexistence crossing or determine transition order.

Ordered source: `v2.2/verify/replica/checkpoints/branch192_retry1_ordered_p0.3048000.npz` (SHA-256 `d15055d94d8a527a698a7967f468704d4c5cdaf1513c2388198170f0652ca1da`, source color L2 0.47912668).
Small-order source: `v2.2/verify/replica/checkpoints/branch192_upper_retry1_ordered_p0.3048500.npz` (SHA-256 `decf371716b717cfd059c268b198a73449423c593ba34bb2272c7dee37c896f1`, source color L2 0.00030084).
Execution provenance: the accepted small-order state resumes from the verified p=.304825 iteration-40 checkpoint. Its reported 199 cumulative iterations are for that accepted checkpoint lineage; the separate earlier no-checkpoint 65-iteration attempt is not added to these counts. The resume used the same preparation and rate, not an extra branch or rate.

Acceptance gates remain unchanged: optimizer and both compatibility residuals <1e−7, canonical defects <1e−9, positive full-period trial contraction with relative defect <1e−8.

## Disposable benchmarks and feasibility gate

- **ordered:** 1 step(s), 60.51 s/step, wall 60.51 s, peak RSS 168724 KiB; no state checkpoint written.
- **small:** 1 step(s), 61.39 s/step, wall 61.39 s, peak RSS 168708 KiB; no state checkpoint written.

Forecast for both preparations including setup and validation reserves: 37946.25 s versus 43077.52 s remaining; headroom 5131.28 s. Memory gate passed=True (forecast peak 609208 KiB; available 1362924 KiB). Decision: **PROCEED with exactly two sequential χ192 p=.304825 continuations**.

## Same-rate state outcomes

| Preparation | Reported status | Iterations | eps | Max compatibility | Max canonical defect | Color L2 | m_species | ξχ | f_half | f_period,trial | Audit record / current tensor |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ordered | accepted finite-chi state reported | 146 | 0.00000005 | 0.00000005 | 0.000 | 0.42451135 | 0.45108317 | 170.442 | 0.992950567266 | 0.992950547331 | historical audit pass; final file missing |
| small | accepted finite-chi state reported | 199 | 0.00000005 | 0.00000005 | 0.000 | 0.00062433 | 0.00060714 | 90.690 | 0.992950208167 | 0.992950139868 | historical audit pass; final file missing |

Same-p invariant-order separation |Δcolor L2| = 0.42388702. Same-objective half-row difference Δf_half (ordered−small) = +3.5909916507e-07. At χ128 and the same rate, the recorded Δf_half (ordered−disordered) was −4.359393e-07. The magnitudes are of the same order and the sign changes with χ. These are finite-χ numerical comparisons, not calibrated uncertainty or a thermodynamic crossing. Full-period Rayleigh trial values remain a separate objective.

## Cross-rate χ192 context

The accepted χ192 p=.30480 pair converged to nearly the same large-order state; the low-order-start path was not retained as a distinct low-order state. At p=.304825, the two authorized histories produced clearly separated accepted states (color L2 0.42451 versus 0.000624). At p=.30485, the ordered-start retry ended in the small-order state. Thus, among these sampled warm-history outcomes, p=.304825 is the first χ192 point with a retained pair, between the sampled .30480 and .30485 outcomes.

A useful shorthand is a **coarse sampled finite-χ warm-history change zone** of approximately (.30480, .30485), with distinct-state retention demonstrated at .304825. The spacing from .304825 to either sampled endpoint is 2.5×10⁻⁵. This is not a measured two-branch stability interval: the endpoints are path outcomes, not mapped boundaries, and no local stability or thermodynamic coexistence test was done. The actual retention limits could differ.

## Interpretation

This pattern strengthens a **first-order-like finite-χ reading** relative to the earlier χ192 .30480 result alone: two distinguishable states are now retained at one common rate, while the sampled warm paths change character at the neighboring rates. It is compatible with a narrow metastable-branch picture if the transition is first-order. A continuous transition with a small exponent β, together with finite-χ crossover or long-lived numerical configurations, remains possible. The current data cannot distinguish these explanations or place the thermodynamic critical point inside the sampled interval.

At p=.304825 the half-row objective difference is +3.59×10⁻⁷ at χ192 and −4.36×10⁻⁷ at χ128. The comparable magnitudes and opposite signs are worth recording, but residuals are not objective error bars; this is not a crossing bracket or evidence that the gap has a controlled χ-scaling.

> **Ledger:** χ192 at p=.304825: two distinct warm-history numerical states reported (color L2 0.4245 vs. 0.0006; Δf_half, ordered−small = +3.59×10⁻⁷). Both final accepted checkpoint files are missing; historical audit records say “passed,” but the final tensors cannot now be independently reopened. Coarse sampled warm-history change zone: .30480–.30485, with pair retention at .304825; not a thermodynamic window or coexistence bracket. First-order-like narrow-window reading strengthened; continuous transition with small β remains live. **Transition order unresolved.**

Optimizer residuals are not free-energy error bars. An accepted VUMPS state is not a global-minimum certificate. The result supports finite-χ warm-history branch retention at one sampled rate, not thermodynamic metastability, global optimality, or transition order.

## Follow-up status

One additional lower-side probe was authorized and selected at χ192 p=.30481 (closer to .30480 than .304815). Disposable benchmarks measured 101.90 s/step for the ordered source and 99.23 s/step for the small-order source. The paired forecast, including setup, both validations, and safety reserve, is 43,873 s (about 12.2 hours); the memory gate passed. A fresh 14-hour cap was set, and one single-thread worker is now running the two histories sequentially. At report update, the ordered history is in progress; no result is available yet. This run cannot restore the missing p=.304825 tensors. The alternative .304815 and the χ256 campaign have not been run.

Artifacts: `v2.2/verify/replica/n3_branch192_mid_pair.json`, surviving source checkpoints, audit records, disposable benchmarks/logs, and `branch192-mid-pair-protocol.json`.

## Artifact availability note

The two independent audit JSON records remain available and marked passed, but neither recorded accepted final checkpoint blob is currently present in the workspace or in the authorized repository main history. Ordered final: checkpoints/branch192_mid_pair_ordered_resume1_p0.3048250.npz (SHA-256 126569ca938197635600e219eb5f090b2997fa6987962e44269489f149568807); surviving source: checkpoints/branch192_mid_pair_ordered_p0.3048250.npz (SHA-256 329004f3403c79ea509b5b6d19abb0f97b41b5d38b20c1c8a144b9a27f78378c), which is the iteration-100 input and not the accepted state. Small-order final: checkpoints/branch192_mid_pair_small_resume1_p0.3048250.npz (SHA-256 dd125c15e6a955b27f43e28fb6834cf1257065b2ae75f15e9d9ce1b2e212f14b); surviving source: checkpoints/branch192_mid_pair_small_restart1_p0.3048250.npz (SHA-256 70e3d74ab46cd359a26c66c2e9b51c16e84a66c30f9f055c652e61719d9799f3), the verified iteration-40 resume input and not the accepted state. Workspace, temp directories, and the authorized repository main history were searched; no matching final binaries were found. No substitute was made and no optimizer was rerun. The accepted values and historical audit outcomes are preserved in the result/audit JSONs, but the final MPS arrays cannot currently be reopened; restore from an external backup before treating the numerical payload as fully reproducible.

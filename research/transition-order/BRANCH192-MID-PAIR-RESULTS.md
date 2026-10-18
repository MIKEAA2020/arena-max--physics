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

| Preparation | Status | Iterations | eps | Max compatibility | Max canonical defect | Color L2 | m_species | ξχ | f_half | f_period,trial | Audit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ordered | accepted finite-chi numerical state | 146 | 0.00000005 | 0.00000005 | 0.000 | 0.42451135 | 0.45108317 | 170.442 | 0.992950567266 | 0.992950547331 | passed |
| small | accepted finite-chi numerical state | 199 | 0.00000005 | 0.00000005 | 0.000 | 0.00062433 | 0.00060714 | 90.690 | 0.992950208167 | 0.992950139868 | passed |

Same-p invariant-order separation |Δcolor L2| = 0.42388702. Same-objective half-row difference Δf_half (ordered−small) = 3.5909916507e-07. These are finite-χ numerical state diagnostics, not calibrated uncertainty or a thermodynamic crossing. Full-period Rayleigh trial values remain a separate objective.

## Interpretation

If two accepted, distinguishable numerical families are retained at p=.304825, that supports finite-χ branch retention at this one common rate. Their same-objective values may be ranked arithmetically at this p, but one point cannot bracket a crossing. If the histories merge, this shows only that these warm paths did not retain distinct states; it does not prove no other stationary state exists. Neither outcome identifies a spinodal, global minimum, coexistence point, or thermodynamic transition order.

Optimizer residuals are not free-energy error bars. A VUMPS state is not a global-minimum certificate. No additional p, gap, or stability computation is inferred.

Artifacts: `v2.2/verify/replica/n3_branch192_mid_pair.json`, surviving source checkpoints, audit records, disposable benchmarks/logs, and `branch192-mid-pair-protocol.json`.

## Artifact availability note

The two independent audit JSON records remain available and marked passed, but neither recorded accepted final checkpoint blob is currently present in the workspace or in the authorized repository main history. Ordered final: checkpoints/branch192_mid_pair_ordered_resume1_p0.3048250.npz (SHA-256 126569ca938197635600e219eb5f090b2997fa6987962e44269489f149568807); surviving source: checkpoints/branch192_mid_pair_ordered_p0.3048250.npz (SHA-256 329004f3403c79ea509b5b6d19abb0f97b41b5d38b20c1c8a144b9a27f78378c), which is the iteration-100 input and not the accepted state. Small-order final: checkpoints/branch192_mid_pair_small_resume1_p0.3048250.npz (SHA-256 dd125c15e6a955b27f43e28fb6834cf1257065b2ae75f15e9d9ce1b2e212f14b); surviving source: checkpoints/branch192_mid_pair_small_restart1_p0.3048250.npz (SHA-256 70e3d74ab46cd359a26c66c2e9b51c16e84a66c30f9f055c652e61719d9799f3), the verified iteration-40 resume input and not the accepted state. Workspace, temp directories, and the authorized repository main history were searched; no matching final binaries were found. No substitute was made and no optimizer was rerun. The accepted values and historical audit outcomes are preserved in the result/audit JSONs, but the final MPS arrays cannot currently be reopened; restore from an external backup before treating the numerical payload as fully reproducible.

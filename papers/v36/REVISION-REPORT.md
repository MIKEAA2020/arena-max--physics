# v36 manuscript organization update

**Status:** author-review continuation generated from the preserved v35 on 2026-10-19. v35 and earlier versions remain unchanged.

## User-directed change

Run-specific χ192 values and the incomplete attempt belong in Supplementary Material; the finite-χ window characterization and unresolved transition order belong in the main text.

## Main-text changes

- Replaced the detailed χ192 results subsection with a concise account of the sampled warm-history outcomes at p=.30480, .304825, and .30485.
- Retained the characterization as a **coarse sampled finite-χ warm-history change zone**, not a thermodynamic coexistence interval or physical stability bracket.
- Kept the interpretation that first-order-like finite-χ evidence does not determine order; **transition order remains unresolved**.
- Kept the controlled χ256 paired-history study, same-objective comparisons, and χ extrapolation as future work only. The main text explicitly says no χ256 calculation is reported.
- Removed the p=.30481 attempt, exact pair values, iterations, residuals, checkpoint hash, and checkpoint-availability detail from the main manuscript. The main text only directs readers to Supplementary Material, Sec. S1 for numerical/provenance details.

## Supplementary Material, Sec. S1

The new standalone `supplementary_v36.tex` contains:

- The historical χ192 p=.304825 ordered/small-order values, iterations, residuals, color L2 values, and f_half values.
- Historical audit-pass status and the limitation that final p=.304825 MPS checkpoint blobs are unavailable for reopening.
- Exact same-rate objective/order comparisons, with explicit caution that the sign reversal is not a calibrated crossing or controlled χ scaling.
- The sampled neighboring path outcomes, to support the main-text window characterization without turning endpoints into stability limits.
- The incomplete p=.30481 continuation: cumulative iteration 19, residual `1.308536380704902e-6`, optimizer time `3222.734782934189` seconds, incomplete small-order companion, unidentified worker/manager loss, checkpoint path and SHA-256. The attempt is explicitly non-accepted and does not refine the zone.
- A statement that χ256 was not run.

## Checks

The generator verifies that all 65 mathematical statement/proof blocks are unchanged from v35, main-text labels remain unique, and internal references/citations resolve. It also asserts that the specific p=.30481 attempt and run-level numeric/checkpoint identifiers are absent from the main text and retained in the supplement.

PDF compilation and typographic/layout review have not been performed. This remains an author-review draft; the checks do not independently re-audit the missing final p=.304825 tensors or certify scientific claims.
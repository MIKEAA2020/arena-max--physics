# v35 manuscript revision report

**Status:** author-review continuation generated from the preserved v34 manuscript on 2026-10-19. v33 and v34 remain unchanged. This is not an author-approved or submission-certified version.

## Purpose

Bring the χ192 campaign evidence into the manuscript in a cautious form consistent with the finalized report at `research/transition-order/BRANCH192-MID-PAIR-RESULTS.md`. Explicitly preserve the distinction between sampled finite-χ warm-history behavior and thermodynamic transition claims.

## Changes

- Updated the abstract and the introduction's summary of the n=3 evidence to include the χ192 pair, the coarse sampled change zone, unresolved transition order, and future χ256 work.
- Added `\subsection{Later $\chi=192$ paired-history evidence}` and a compact table for the reported p=.304825 ordered/small-order pair:

  | Preparation | Iterations | Residual | Color L2 | f_half |
  |---|---:|---:|---:|---:|
  | Ordered | 146 | 4.8394e-8 | 0.424511 | 0.992950567266 |
  | Small-order | 199 | 4.9159e-8 | 0.000624 | 0.992950208167 |

- Identified these as historical audited observations: the audit records report acceptance, but final p=.304825 MPS checkpoint blobs are unavailable for tensor-level reopening.
- Characterized the sampled outcomes at p=.30480, .304825, and .30485 as a **coarse finite-χ warm-history change zone** approximately .30480–.30485. The endpoints are path outcomes, not physical stability or coexistence boundaries.
- Recorded Δf_half (ordered minus small-order) at χ192, p=.304825 as +3.5909916507e-7, and the χ128 same-rate value as −4.359393e-7. The opposite signs are explicitly not treated as error bars, a calibrated crossing, or controlled χ scaling.
- Kept the p=.30481 continuation non-accepted: cumulative iteration 19, residual 1.308536380704902e-6, and no completed small-order companion. Its surviving partial checkpoint is archived at `research/transition-order/chi192-p30481/` (SHA-256 `a8097162c27ca104556edd5c789bcf36e5c9c89ef5af7eb92ad3811248319cee`). This attempt does not refine the sampled zone.
- Updated the conclusion and numerical-artifact note. The transition order is explicitly unresolved.
- Named a controlled χ256 paired-history study with reopenable checkpoints, same-objective comparisons, and χ extrapolation/coexistence checks as future work. A single χ256 point is noted as insufficient by itself. **χ256 was not run.**

## Integrity checks

The generation script reads v34 and writes v35 as a new file. It asserts that all 65 theorem, proof, definition, assumption, proposition, lemma, corollary, and remark blocks are byte-for-byte unchanged. It also checks for duplicate labels, unresolved internal references, and unresolved citation keys.

Generation result: 162 unique labels; 314 internal references resolve; 57 citation keys resolve. Details and hashes are in `source-provenance.json`; the machine-readable output is `source-contract-check.log`.

PDF compilation and typographic/layout review have **not** been performed. The checks do not validate scientific correctness, broader manuscript statements, or the unavailable final χ192 tensors. Author review remains required.

## Key limitations retained in the manuscript

- The χ192 zone is a sampled finite-χ warm-history change zone, not a measured physical window, spinodal, coexistence interval, or transition bracket.
- Optimizer residuals are not free-energy error bars; accepted MPS states are not global-minimum certificates.
- The p=.304825 final pair is not independently reopenable from final MPS checkpoint blobs.
- The p=.30481 continuation is incomplete and non-accepted.
- Transition order remains unresolved; χ256 is only a future computation recommendation.
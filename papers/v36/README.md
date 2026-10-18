# v36 author-review continuation

v36 is a new continuation from the preserved v35 manuscript. It applies the requested separation between main-text interpretation and run-level supplementary details. v35 remains unchanged.

## Files

- `manuscript_revised_v36.tex` — concise main manuscript. It retains the finite-χ warm-history change-zone characterization, explicitly unresolved transition order, and the proposed χ256 follow-up.
- `supplementary_v36.tex` — separate Supplementary Material, Sec. S1, containing the χ192 table, exact observables/residuals, historical audit/checkpoint limitation, and the incomplete non-accepted p=.30481 attempt.
- `revise_manuscript.py` — reproducibly generates the main manuscript and supplement from `../v35/manuscript_revised_v35.tex`.
- `v35-to-v36.diff` — main-text diff.
- `source-provenance.json` and `source-contract-check.log` — hashes, structure checks, and explicit scientific status.
- `REVISION-REPORT.md` — what was moved and what remains in the main text.

Regenerate from the workspace root:

```bash
python papers/v36/revise_manuscript.py
```

## Separation of content

The main text characterizes the coarse sampled finite-χ warm-history change zone as approximately `p = 0.30480–0.30485`, states that transition order remains unresolved, and identifies a controlled χ256 paired-history study plus same-objective comparisons and χ extrapolation as future work. It does not report the p=.30481 attempt, iteration counts, residuals, checkpoint hash, or pair-level numeric table.

The supplementary source contains those run details. It clearly marks p=.30481 as incomplete and non-accepted, notes that the p=.304825 final checkpoint blobs are unavailable for reopening, and states that χ256 was not run.

All 65 mathematical statement/proof blocks are byte-for-byte unchanged from v35. The script checks unique labels and resolves internal references and citation keys. PDF compilation and layout review have not been performed; this remains an author-review draft.
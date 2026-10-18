# v35 author-review continuation

This directory contains a new manuscript continuation based on the preserved v34 source. It incorporates the χ192 paired-history observations and their limitations; it does not alter v33 or v34.

## Main file

- `manuscript_revised_v35.tex` — updated author-review manuscript.

## Reproducibility and audit files

- `revise_manuscript.py` — regenerates v35 from `../v34/manuscript_revised_v34.tex`.
- `v34-to-v35.diff` — source diff for review.
- `source-provenance.json` — source/output hashes and explicit numerical-status flags.
- `source-contract-check.log` — structural checks performed during generation.
- `REVISION-REPORT.md` — substantive changes and scientific limitations.

From the workspace root, regenerate with:

```bash
python papers/v35/revise_manuscript.py
```

The generator verifies that all 65 theorem/proof/statement blocks are byte-for-byte unchanged, that labels are unique, and that internal references and citation keys resolve. It does not compile the TeX source or certify the scientific claims. PDF compilation/layout review has not been performed.

## Scientific scope

The manuscript characterizes a coarse sampled **finite-χ warm-history change zone** of approximately `p = 0.30480–0.30485`, with a reported distinct pair at `p = 0.304825`. This is not a measured thermodynamic coexistence interval, spinodal, or transition bracket. Transition order remains unresolved.

The `p = 0.30481` ordered continuation is explicitly non-accepted: it stopped at cumulative iteration 19 with residual `1.308536380704902e-6`; its small-order companion was not completed. The reported `p = 0.304825` pair passed historical audits, but its final MPS checkpoint blobs are unavailable for reopening, limiting independent tensor-level reproducibility.

A controlled χ256 paired-history study with same-objective comparisons, reopenable audited checkpoints, and χ-extrapolation/coexistence checks is named as future work only. **No χ256 computation was run or is reported in this revision.**

This is an author-review draft, not a submission-ready or peer-reviewed manuscript. The author should review the new text, numbers, provenance, and all broader manuscript claims before release.
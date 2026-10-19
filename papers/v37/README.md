# Manuscript source package

This directory contains the journal manuscript source, Supplementary Material S1, the deterministic source generator, and machine-readable validation results.

## Files

- `manuscript_revised_v37.tex` — main article.
- `supplementary_v37.tex` — Supplementary Material S1, including the finite-\(\chi=192\) paired-history values and incomplete \(p=.30481\) continuation.
- `revise_manuscript.py` — generator for the manuscript, supplement, and validation metadata.
- `source-provenance.json` and `source-contract-check.log` — hashes and structural checks.

Regenerate from the repository root with:

```bash
python papers/v37/revise_manuscript.py
```

## Scientific scope

The main text describes the sampled finite-\(\chi\) warm-history change zone near \(p=.30480\)–\(.30485\) and leaves transition order unresolved. Run-level \(\chi=192\) data and the incomplete \(p=.30481\) attempt are in S1. No \(\chi=256\) result is reported; that calculation remains future work.

## Build status

The source checks pass: 103 displayed-equation environments are unchanged, 58 formal environments are byte-identical, eight specified formal environments were restyled, and labels, references, and citation keys resolve. PDF compilation and layout review have not been performed because no TeX engine is available in the environment. The source refers to `fig_fss.pdf`, which is not included in this package; the figure asset is required for compilation.

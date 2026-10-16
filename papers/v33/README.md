# v33 author-review package

Start with **REVISION-REPORT.md** or **v33-revision-report.docx**. The full revised paper is
**manuscript_revised_v33.tex**. This is a corrected author-review draft, not an approved
submission or a proof of first order. No external publication or repository was changed.

## Layout

The ZIP preserves these paths under its `v33-review/` root:

- `papers/v33/`: manuscript, report, unified diff, source provenance, revision script,
  section fragments and data-table generator.
- `adjudications/`: unmodified v32 input and the user's v33 assessment.
- `v2.2/verify/replica/`: independent finite-size transfer operator, VUMPS implementation,
  completed chi=96 runs, tilted-Clifford sampler, exact normalizer/rank code and stored runs.
- `v2.2/verify/replica_checks.py`, `v33_checks.py`: the two paper-specific regression suites.
- `v2.2/verify/*.log`: verification records. The legacy framework log includes unrelated
  suites; its 162 passes plus the 35 extension passes give the reported 197 in this workspace.

The broader theological/time framework is **not** bundled into a physics reproduction
package. Its revised `.md` and `.docx` remain separate workspace deliverables.

## Rebuild the source and check the paper-specific extension

From the extracted `v33-review/` root:

```bash
python3 -m pip install -r papers/v33/requirements.txt
python3 papers/v33/revise_manuscript.py
python3 papers/v33/make_revision_tables.py
bash papers/v33/run_review_checks.sh
```

The paper-specific runner performs **17 + 35 = 52** checks, including fresh fixed-seed
SMC validation (about two minutes on the original sandbox). The full workspace's
`v2.2/verify/run_all.sh` additionally runs the other framework suites; that runner and
those unrelated inputs are not required by, or shipped in, this paper-only package.

The checks validate operator agreement, exact finite-time targets, algebra, code invariants,
scope counterexamples and source contracts. They do **not** prove a phase order or all
manuscript theorems. Between-seed errors with four or five seeds are regression diagnostics,
not bounds on population systematics.

## Compile the paper

Use a TeX installation with REVTeX 4.2 and the listed packages. Restore the author's original
`fig_final_fss_v16.pdf` alongside the source; it was not uploaded. The v32 Supplemental
Material and its original numerical deposits must also be supplied for submission.
Then compile, for example with `latexmk -pdf manuscript_revised_v33.tex`. Labels,
bibliography keys and environments have been linted, but a submission PDF has not been
compiled or certified in this workspace. No replacement scientific figure is fabricated.

## Run a new tilted-Clifford case

```bash
cd v2.2/verify/replica
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
python3 clifford_tilt_smc.py 32 0.305 2 4000 128 4 101 new_run.json
```

Arguments are L, p, beta, particles, periods, entropy-sampling interval, seed, output JSON.
The target is `Lambda = log E[2^(-beta N_rand)]/(2LT)`. At beta=2 this equals the Haar
third replica moment; in the thermodynamic-limit conventions it is `-f_b/4`, not `-f_b`.
At finite L,T use `v33_exact.py` for independent small-system boundary-correct targets.

The initial large-system pilots have only 1–5 distinct interior ancestors at L=64–128.
They do not settle coexistence. Use population, time, phase-mixing and genealogy controls
before treating any histogram as thermodynamic evidence. Output-schema v2 adds descendant
ESS and count histograms; older pilot files retain distinct-ancestor counts but not every
new diagnostic.

`smc_pilot.py` atomically checkpoints each completed parameter case and can skip it on
restart. This does not checkpoint a partially completed particle population. Likewise,
VUMPS JSONs save observables, not the MPS state: skipping cached lower-chi stages does not
warm-resume a higher stage. Use a fresh output file and rerun the warm-start chain.

## Scope and provenance

The numerical fourth-Clifford task completed here is an **exact Gram-rank check: 29** for
two-qubit gates. No fourth-Clifford critical point, new n=4 VUMPS solution, n=3,d=3 production
scan, n* theorem or n→1 continuation is claimed. The source explicitly withdraws the earlier
n=3,4 Potts assignments. The main CTD/CPD promised completeness results are retained;
additional independent scope corrections are explained in the report.

SHA256SUMS in the ZIP records the supplied files. `source-provenance.json` identifies the
unaltered v32 input and generated v33 source hashes. The author must review all changes
before publication.

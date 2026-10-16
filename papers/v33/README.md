# v33 author-review package

Start with **REVISION-REPORT.md** or **v33-revision-report.docx**. The full revised paper is
**manuscript_revised_v33.tex**. This is a corrected author-review draft, not an approved
submission or a proof of first order. At the original v33 delivery no external publication or repository had been changed. The later, user-authorized GitHub snapshot and transition-order continuation are recorded separately in `research/transition-order/`.

## Layout

The ZIP preserves these paths under its `v33-review/` root:

- `papers/v33/`: manuscript, report, unified diff, source provenance, revision script,
  section fragments and data-table generator.
- `adjudications/`: unmodified v32 input and the user's v33 assessment.
- `v2.2/verify/replica/`: independent finite-size transfer operator, VUMPS implementation,
  completed chi=96 runs, tilted-Clifford sampler, exact normalizer/rank code and stored runs.
- `v2.2/verify/replica_checks.py`, `v33_checks.py`, `transfer_checks.py`: current paper-specific regression suites.
- `research/transition-order/`: the later method decision, exact/production status and resumable continuation instructions.
- `v2.2/verify/*.log`: verification records. The original legacy framework log includes unrelated
  suites; its 162 passes plus 35 extension passes gave the original 197. Current totals and
  fresh-run provenance are in the transition-order results, not silently substituted into the historical report.

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

The original paper-specific runner performed 17 + 35 = 52 checks. The current runner adds
49 half-row/checkpoint/fourth-Clifford regressions: **17 + 35 + 49 = 101** checks, including
fresh fixed-seed SMC validation and exact small-ring tests. The full workspace's
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
the original full-period VUMPS JSONs save observables, not the MPS state: skipping cached
lower-chi stages does not warm-resume a higher stage. The new `replica_halfrow.py` and
`order_campaign.py` instead save real NPZ tensors/environments and optimizer metadata;
see `research/transition-order/PLAN.md`, `NUMERICAL-NOTES.md` and the execution results.

## Scope and provenance

At the original v33 delivery, the fourth-Clifford task completed was an exact Gram-rank
check: 29 for two-qubit gates. The later continuation derives its physical transfer operator
and completes the L=4,6 diagonal-sector ladder; it also adds n=3,d=3 finite-size/coarse-MPS
data and a low-chi n=4 Haar MPS pilot. These are documented separately under
`research/transition-order/`. No fourth-Clifford critical point, controlled n=3 coexistence,
n* theorem or n→1 continuation is claimed. The source explicitly withdraws the earlier
n=3,4 Potts assignments. The main CTD/CPD promised completeness results are retained;
additional independent scope corrections are explained in the report.

SHA256SUMS in the ZIP records the supplied files. `source-provenance.json` identifies the
unaltered v32 input and generated v33 source hashes. The author must review all changes
before publication.

## Exact high-chi replay and inspection boundary

The compact physics package contains code, observations, comparisons, protocols, reports, and control/low-chi NPZ fixtures. It does **not duplicate any high-chi (chi>=96) state**, including the earlier accepted matched-point states; all real high-chi, scan/branch, rolling and partial/warm sources remain in the full Git repository. This packaging-only policy keeps the durable workspace below its snapshot capacity without deleting or changing scientific states. Older package bytes remain in Git history.

Exact high-chi replay with `prepare_chi128_reproduction.py` and actual high-chi state audits therefore require a **full checkout**, not the compact ZIP alone. The ZIP still supplies its documented 101-check paper subset and the numerical observation records; it is not a full-checkpoint deposit.

# Reproduction and continuation

All commands below are run from the full repository root unless a `cd` is shown. Long production is deliberately separate from counted regression. Source files and archived inputs retain their provenance; an output process finishing is not proof of convergence.

## 1. Fastest useful verification

```sh
python3 -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 bash papers/v33/run_review_checks.sh
# Current paper-specific total: 17 + 35 + 49 = 101.

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 bash v2.2/verify/run_all.sh
# Full framework + physics total: 246 across ten suites.
```

The original v33 delivery had 197 checks and its original paper-only package had 52. Those historical records are retained, not silently relabeled as the new full run. The optional corpus lookup/count scripts use separately acquired corpora and are not part of that counted total.

## 2. Reproduce the calibration schedule

```sh
cd v2.2/verify/replica
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 CORR_RMAX=1000 \
  python3 -u control_campaign.py
# Or one cheap fresh case:
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 control_campaign.py --quick
```

The output is a list named `half_controls_reproduction.json`, plus separately named actual NPZ states. It does not overwrite `half_controls.json`. Some low-chi stages may hit their iteration cap; each requested tolerance is reported. Approximate earlier controls may warm-initialize later calibration stages, but are not retrospectively accepted observations. The legacy generic half-row CLI writes a dictionary instead, so do **not** point it at the archived list file and assume the schemas match.

## 3. Secondary exact/coarse programs

```sh
cd v2.2/verify/replica
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 clifford4_transfer.py check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 secondary_campaign.py d3-exact
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 STAGE_SECONDS=120 CORR_RMAX=100 \
  python3 secondary_campaign.py d3-mps
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 STAGE_SECONDS=120 CORR_RMAX=100 \
  python3 secondary_campaign.py n4-mps
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 L8_SECTOR_SECONDS=120 \
  python3 secondary_campaign.py clifford8
```

The L=8 command benchmarks before deciding whether to launch eigenproblems. A deferred status is a real outcome, not a cached success. `clifford4_ladder.json` stores the completed 52-case L4/L6 grid, with per-eigenpair residuals. The script's standalone finite-spectrum command can add individual rates/sizes; do not launch an unbounded larger ladder without a measured resource estimate.

## Completed six-rate χ128 continuation

The requested fixed-source grid is recorded in `chi128-scan-protocol.json`, `SCAN128-RESULTS.md`, and `chi128-scan.csv`. All six paired rates passed their declared gates: ten new optimization targets and two actual reused .30486 reference states. `audit_scan128.py` independently rechecks the saved arrays and recorded gates without launching a new optimizer:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 research/transition-order/audit_scan128.py
```

The full Git checkout contains all real scan MPS states; the compact review ZIP intentionally omits them. Archived campaign/point deadlines and completed output guards must not be silently reset. A fresh production replay needs an explicitly allocated, separately named campaign and isolated outputs. `chi128_scan_campaign.py` is the original orchestrator; `resume_chi128_scan.py` documents physical-checkpoint continuation after a session pause, not scalar-cache warm starts. Publication helpers target only the authorized repository and must not be treated as generic unreviewed publishing commands.

The sampled change between .3047 and .30486 is finite-χ information, not a thermodynamic critical interval or order verdict. No automatic χ192 was authorized.

## 4. Earlier single-point chi=128 continuation

The later user authorization is one two-preparation chi=128 stage at p=.30486, with the original 1e-7 tolerance and at most 90 minutes walltime. See `chi128-90m-protocol.json` and `CHI128-STAGE.md`. Neither agreement nor disagreement at this one point is a binary transition-order verdict. No chi=192 stage is automatically authorized.

The archived protocol has an absolute deadline and the driver refuses accidental output overwrite. **Do not extend that historical deadline in place.** Using the **full Git checkout or owner-push Git bundle** (the compact ZIP omits the two partial warm sources), prepare an isolated reproduction allocating a new runtime but not launching any MPS:

```sh
python3 research/transition-order/prepare_chi128_reproduction.py \
  /path/to/new-reproduction-directory --seconds 5400
```

This copies only the hashed core code and immutable warm states, preserves the original archive, and prints two commands to run in separate terminals. The new shared deadline starts when preparation finishes, so launch promptly. The helper itself never launches a worker.

The older chi=96 example below is **historical reproduction only**, not a recommendation or authorization for another chi=96 production batch.

## 5. Historical matched-rate continuation example

Actual per-branch states are under `v2.2/verify/replica/checkpoints/`. Metadata, not an old JSON pointer or filename, identifies p, chi, functional, residual and whether a state was only a seed. A `latest` file is rolling. Immutable accepted anchors and partial states have separate names.

For example, after selecting the correct checkpoint:

```sh
cd v2.2/verify/replica
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 STAGE_SECONDS=750 MAXITER=300 \
  CORR_RMAX=240 RESUME_STATE=checkpoints/seed_ordered_chi96_common.npz \
  CASE_FILE=../../../research/transition-order/cases-common96-ordered.json \
  python3 -u order_campaign.py ordered
```

Use the disordered seed/queue/argument for the other preparation. These original warm seeds reproduce the named continuation; an accepted immutable anchor can instead warm-resume its own rate. A stopped latest checkpoint can continue its exact unfinished stage. Do not skip observation-only scalar JSON entries and mistake that for a saved MPS.

The default historical target list contains chi=128/192, but current feasibility policy **defers chi=192** after the recorded chi=128 budget problem. Use explicit queue files and a documented resource decision rather than blindly replaying larger targets. The current matched-rate queues hold .30486/.30490 in opposite directions. Tolerance is not relaxed when a result is inconvenient. Approximate truncated seeds are not observations; a fresh optimizer must pass before an accepted comparison.

## 6. Frozen-state comparison is a different diagnostic

After both common-rate workers stop, `trial_rayleigh.py` evaluates the same full-period operator on the two saved trial MPS states. It is benchmark/time gated. Even if the numerical contraction is accurate, an unconverged trial comparison does not establish stationary coexistence, latent heat or p_c. Its source optimizer metadata and qualifications are stored explicitly.

## 7. Refresh reports and the compact review bundle

```sh
python3 research/transition-order/summarize.py
python3 research/transition-order/render_report.py
python3 research/transition-order/bundle_review.py
```

The compact physics ZIP omits all high-chi (chi>=96) states, bulk scan/branch states and rolling/partial/warm sources; the full repository retains every real state. Use a full checkout for high-chi inspection/replay or data audits. Framework amendment and Git publication helpers are workspace operations, not additional physics proofs. They require a verified completed full-run receipt or an existing authorized Git clone respectively. No helper embeds an access token or automatically force-pushes.

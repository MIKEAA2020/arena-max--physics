# Arena research workspace — physics and evidence-governed time framework

Generated research, verification code, data and review drafts. The supplied repository history and MIT license are preserved. **Research artifacts are not a claim of peer review, a solved problem of time, or a proved replica universality class.**

## Start here

- **[Transition-order method and dependency plan](research/transition-order/PLAN.md)** — chosen deterministic transfer-MPS/DMRG method, acceptance tests and feasibility order.
- **[Latest execution results](research/transition-order/RESULTS.md)** — completed, unconverged, budget-stopped and deferred work; updated with the numerical snapshot.
- [Numerical execution notes](research/transition-order/NUMERICAL-NOTES.md) and [analytic proof-audit obligations](research/transition-order/PROOF-AUDIT.md).
- **[v33 manuscript](papers/v33/manuscript_revised_v33.tex)** and [revision report](papers/v33/REVISION-REPORT.md) — author-review draft withdrawing the earlier n=3,4 Potts assignments. Original figure/SM and specialist review are still required for submission.
- **[v2.2 framework](v2.2/Lighthouse-and-Plan-v2.2.md)** — a separate, evidence-governed lineage. The replica-paper adjudication is A-1, not clue 13; none of its physics decides the commitments in Parts I–II.
- [Previous v2.1](v2.1/Lighthouse-and-Plan-v2.1.md), [source-lineage records and visualizers](clues/), and [assessments](v2.2/assessments/).

## Accepted chi128 continuation

The later bounded stage produced **two accepted chi=128 optimizer results at p=.30486**, not a certified pair of coexisting phases. Both have small order diagnostics; the large ordered/disordered separation in the earlier unconverged chi=96 trials did not persist in this specific experiment. The same-period values are very close. This does not establish continuity or rule out first order elsewhere in the rate bracket. Chi=192 was not automatically launched.

See [the stage result and interpretation contract](research/transition-order/CHI128-STAGE.md), [reproduction instructions](research/transition-order/REPRODUCE.md), and [publication status at assistant delivery](research/transition-order/chi128-publication-status.json). That receipt distinguishes the previous verified remote commit from a new local owner-push handoff.

## Reproduce the checks

Python 3.11+ recommended. Numerical work uses NumPy/SciPy/SymPy; full framework checks also use Z3. Limit BLAS threads on small machines.

```sh
python3 -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 bash v2.2/verify/run_all.sh
# Paper-only checks:
bash papers/v33/run_review_checks.sh
```

The new transfer-MPS extension is `v2.2/verify/transfer_checks.py`. Counted checks validate specified finite identities, code contracts and regressions; they do **not** prove first order or every manuscript theorem. Long production datasets are stored and not automatically recomputed by the regression driver.

See `v2.2/verify/replica/replica_halfrow.py` and `order_campaign.py` for actual resumable MPS states. Earlier full-period VUMPS JSONs contain observations only and cannot warm-resume an MPS. Checkpoint metadata records the operator, rate, bond dimension and optimizer state; partial optimizer states are not accepted phase results.

## Publication scope and provenance

[PUBLICATION-SCOPE.md](PUBLICATION-SCOPE.md) describes the generated-artifact snapshot, narrowly identified supplied reproduction inputs, excluded bulk downloads and credential handling. `PUBLICATION-MANIFEST.json` records file hashes for the publication snapshot. The existing repository license is not a representation of ownership of quoted literature, translations or supplied manuscripts; those materials retain their original rights and attributions.

No access token belongs in this repository. Authentication metadata, dependency caches and bulk source downloads are excluded. The original repository history is retained; publication uses ordinary, non-force commits.

## Six-rate continuation and interpretation update

The requested χ128 fixed-source grid is recorded in [SCAN128-RESULTS.md](research/transition-order/SCAN128-RESULTS.md). Pending, interrupted, budget-stopped and accepted preparations remain distinct; no finite bulk gap or missing sampled separation is automatically called a transition-order verdict.

The [v34 author-review continuation](papers/v34/manuscript_revised_v34.tex) explicitly applies the governing Qur’anic/Lighthouse reading: real, dependent creation is distinct from its uncreated Creator. It does not identify God with a state, observable algebra or physical clock, and it does not derive theology from circuit physics. Original v33 is preserved; [the v34 report](papers/v34/REVISION-REPORT.md) records unchanged mathematical blocks and remaining submission blockers.

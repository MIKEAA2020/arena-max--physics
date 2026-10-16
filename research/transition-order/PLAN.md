# Settling the n = 3 transition: method decision and dependency-ordered execution

16 October 2026 · A-1 continuation · This is a research plan with explicit stopping rules, not a promise of a binary answer from finite resources.

## Decision

**Primary method: deterministic transfer-matrix MPS/DMRG on the exact n = 3 replica operator.** The Clifford beta=2 identity means the tilted record problem is already represented by the same six local labels. Do not build an exponentially large stabilizer-state transition matrix merely to call the calculation “tilted DMRG.” Existing VUMPS is an infinite/uniform transfer-MPS method in this family, not an independent alternative. The upgrade is a cheaper validated Hermitian half-row representation, resumable states, higher chi, same-p branch comparisons, and explicit convergence tests.

**Secondary discriminant if high-chi branches remain ambiguous:** finite-cylinder, symmetry-resolved transfer-MPS/DMRG gaps and interface free energies, with an independently validated finite-size boundary/operator contract and truncation/environment convergence. A generic open-boundary DMRG call is not automatically the periodic circuit operator. It is not reported as implemented before that contract exists.

**SMC is a secondary, gated program, not the next production run.** Resample-move/tempered trajectory updates or a guided/Doob proposal require independent small-system validation, population/time ladders and controlled phase mixing before another L=128–256 coexistence pilot. More particles or a different resampling rule alone does not prove that long genealogies or rare phases are sampled. Genealogy collapse diagnoses this pilot, not a no-go theorem for all SMC estimators.

## Why the cheaper row is legitimate, and why a naive version failed

Write the half row as H=M1 and a one-bond translation as T. In the bond-Gram metric H†=HT, and the full period is C=HTH. On ring momentum zero, H is self-adjoint and C=H². A uniform periodic MPS lies in that sector.

A naive one-center VUMPS use of the nonsymmetric H MPO produced a complex effective eigenvalue and was rejected. The usable construction is a **globally Hermitian MPO direct sum H + H†**, with paired/transposed environments. Its bond dimension is 2 n! = 12 at n=3, versus (n!)²=36 for the full-period MPO. The global factor two is subextensive in the infinite-row free energy; finite-ring comparisons divide the sum by two. This is checked directly, not assumed. The half-row and full-period finite-chi variational functionals are not identical; their differences are recorded and must vanish in the relevant convergence limit.

The period free energy is f_b = -2 log eta_half, not -log eta_half. Period Rayleigh cross-checks and the exact n=2 Ising point anchor normalization. A separate exact optimization of the MPS transfer contraction removes a spurious O(chi^4) contraction without changing its mathematical map.

## Dependency DAG and feasibility order

| ID | Work | Prerequisites | Acceptance / stopping rule |
|---|---|---|---|
| T0 | Preserve v32/v33, archive assessment without credentials, construct reproducible task ledger | None | No overwritten historical source; token absent from tracked files |
| T1 | Half-row exact finite-ring and momentum-zero identities; checkpoint round trip; contraction identity | T0 | Matrix errors < 1e-11; raw nonsymmetric optimization rejected; no unconverged output promoted |
| T2 | Ising chi=8,16,32,64 and n=3 gapped-side controls, plus full-period Rayleigh comparison | T1 | Correct f, Ising xi scaling, optimizer residuals, decreasing functional discrepancy |
| T3 | n=3,d=2 ordered/disordered warm chains chi=48,72,96,128,192; adaptive same-p rate refinement | T2 | Per-stage residual and budget recorded; checkpoints persist; do not fit off-critical chi slopes as exponents |
| T4 | n=3,d=3 coarse/fine scan with the same six-label operator | T1,T2 | Location only at first; forward/reverse branches and chi controls needed for order |
| T5 | Fourth Clifford local twirl on rank-29 quotient; exact endpoints and generator invariance | T0 | Haar control recovered, rank-29 support, exact Clifford p=1 moments and physical twirl checks |
| T6 | Fourth Haar/Clifford L=4,6 symmetry-resolved spectra, then L=8 only after measured feasibility | T5 | Reproduce known Haar crossings; residuals for all sectors; finite-size splitting is not critical-point splitting |
| T7 | Fourth Haar thermodynamic transfer-MPS pilot via low-bond Hermitian row | T1,T2,T6 | Independent p=1/dense controls first; avoid materializing the ~1.5 GB full-period tensor; increase chi only after residual checks |
| T8 | Finite-cylinder transfer-DMRG gap/interface implementation if T3 does not discriminate | T3 | Exact small-ring and boundary tests precede L>=64; environment and chi convergence required |
| T9 | Guided/resample-move SMC pilot, if an independent sampling discriminant is still needed | T3 plus separate proposal/mixing validation | Exact moments, unbiased normalizer checks, independent populations, time/population ladders before large L |
| T10 | Full-Haar analyticity proof audit; contour/cluster and real-replica programs | Independent mathematical work | No finite numerical run closes an unverified analytic hypothesis |
| T11 | Independent n=5 higher-size reproduction | Rank-119 quotient and symmetry/orbit-block assembler, after primary T3 priority | Naive L=8 requires >26 GB for 16 Krylov vectors; original assembler/deposit not supplied; do not use the singular inverse-Gram legacy path |

T3 is the priority compute queue. T5/T6 run on the second core while T2/T3 run on the first. T4 and T7 follow validation and resource availability. A dependency is not marked passed merely because a process exits.

## Measurements needed to decide order

At each chi locate a **same-p crossing or merger of independently continued ordered/disordered stationary branches**, not just a coarse-grid jump. Refine the rate adaptively around their variational competition; compare free-energy differences against optimizer error and half/full-functional systematics.

Record at matched p*(chi): both order diagnostics; free-energy slope difference; MPS correlation length; bond entropy; scan/initialization dependence; and full-/half-period consistency where feasible. Releasing a small symmetry-breaking field is a possible state-selection tool, not proof of a metastable phase.

**Evidence for first order:** a nonzero order-parameter discontinuity AND nonzero derivative jump survive increasing chi and all accepted extrapolations, with the bulk correlation length saturating and genuine branch coexistence resolved. A positive converged interface cost or exponentially closing finite-cylinder tunnelling gap is a strong independent corroboration. A three-point fit alone is not the decision rule.

**Evidence for continuity:** branches merge under controlled limits; apparent discontinuities trend to zero; tuning at the transition gives stable finite-entanglement/scaling behavior across several chi values; no finite jump above the measured sensitivity survives. Finite computations cannot exclude every arbitrarily weak first-order scenario. State the exclusion scale rather than inventing an absolute theorem.

**If neither test passes at the resource ceiling:** keep the order open, publish the numerical sensitivity and resumable states, and move to T8 rather than running unvalidated SMC indefinitely. The plan has finite acceptance and stopping rules even if nature has a longer crossover than this sandbox can resolve.

## Resource policy for this execution

Sandbox: two CPU cores, approximately 2 GB RAM. Each numerical worker uses one BLAS thread. At most two heavy workers. Stage budgets are explicit and checkpoint before a wall-clock stop; larger chi is not launched from an unconverged prerequisite without a documented reason. MPS states, not just scalar JSON observations, are saved. Data size is monitored against the workspace snapshot cap. No claim of free-energy convergence is based solely on a small local optimizer residual.

## Corrections to the latest assessment

- The previous report did discuss populations, phase mixing/tempering, boundary controls and larger same-p MPS studies; it did not choose a primary production method. This document makes that choice.
- The pilot did not settle coexistence; it does not prove that the SMC method class cannot work at useful sizes.
- The regular-bimodule algebra is not conditional on first order at n=3. Its fully ordered phase-orbit interpretation is conditional on the symmetry breaking; the transition order is a separate question.
- Some n=4 crossings and sector assignments have been independently reproduced. Their asymptotic class remains open; the exact sector algebra is not unsettled by the retraction.
- An unresolved transition order need not block a correctly scoped paper. “Publication-ready” nevertheless still requires the missing original figure/SM, author review and the outstanding analytic-hypothesis audit. No submission certification is made here.

## Repository and credentials

The user selected `https://github.com/MIKEAA2020/arena-max--physics`. Generated work is prepared for a non-force push preserving the existing history/license. Credentials are stored only in excluded owner-readable Git metadata for this run and must never enter commits, archives, reports or manifests. That storage is transient, not a durable vault. Source uploads and bulk third-party downloads are not generated deliverables and are separated from the publication snapshot; provenance and acquisition references remain.

# Transition-order continuation — execution results

16 October 2026 · A-1 continuation · **Interim snapshot; numerical production and regression are in progress.**

## Decision and current scientific conclusion

The selected primary method is deterministic transfer-MPS/DMRG on the exact n=3 replica operator, with a validated Hermitian half-row MPO, real resumable state checkpoints, higher chi and same-rate two-start comparisons. See [PLAN.md](PLAN.md) for the dependency DAG and acceptance/stopping rules.

The previous numerical reading remains **p_c approximately .3049(2); weak first order favored, continuity unresolved**. The new work is not represented as a settled order verdict. A coarse-grid jump, a local optimizer residual or a successful GitHub push cannot supply that verdict.

## Completed validation and fourth-moment work

- Exact finite-ring half-row identities passed at n=2,d=2; n=3,d=2; n=3,d=3; n=4,d=2. Production uses the globally Hermitian H+H† direct sum with paired environments. The naive nonsymmetric optimizer failed and was rejected.
- Ising p=.233810 controls at chi=8,16,32,64 converged at requested residual 1e-8. Correlation lengths: **39.2048, 165.8538, 681.2273, 2546.748**. The 16→32 finite-entanglement growth is approximately kappa=2.04. These are calibration data, not new critical-exponent estimates.
- At n=3,p=.300, the half/full-period free-energy discrepancy shrinks from 2.09e-7 at chi=24 to 5.79e-9 at chi=48. At p=.310 it shrinks from 3.97e-6 to 4.12e-7. The chi=48 p=.310 residual is 1.17e-8: slightly above that run's nominal 1e-8, below the calibration ceiling 3e-8. Lower-chi capped runs remain explicitly unaccepted at their requested tolerance.
- Fourth Clifford local twirl constructed on **30 closed labels with Gram rank 29**, using a pseudoinverse quotient. Physical gate commutators, Haar-weight agreement, projectors and p=1 endpoints pass. Independent support-rank counts are **[48,288,384]**; pair moments for replicas 2,3,4 are **2/5,1/5,1/8**. Haar fourth moment is **4/35**.
- **All 52** fourth-moment Haar/Clifford cases completed: 13 rates × L=4,6 × two ensembles, with all five S4 left/right sectors. Maximum absolute eigenpair residual: **1.18e-10**.

### Fourth-moment L=4,6 crossing diagnostics

The following are **linear interpolation estimates on the stored rate grid**, not finely root-solved values and not thermodynamic critical points.

| Sector | Haar L4/L6 estimate | Clifford L4/L6 estimate |
|---|---:|---:|
| standard | .3583 | .3340 |
| sign | .3698 | .3488 |
| two-dimensional | .3498 | .3340 |
| standard × sign | .3688 | .3488 |

The finite-size Haar/Clifford difference is resolved. Persistence of this difference in the thermodynamic critical point is **not** established by L=4,6. Larger-size feasibility is a separate gate.

## Primary n=3 production

The ordered warm chain has reached chi=72 at p=.3048 with f_half=.9928704222, m_species=.53897, |m_parity|=.36473 and xi_chi=38.52, residual 9.59e-8 at requested 1e-7. Higher-chi stages are in progress; see raw `order_ordered.json` and log for the exact snapshot.

The disordered .310→.306, chi=48 stage hit 400 iterations at residual **2.11e-7**, missing requested 1e-7. Its approximate values are retained, but it is **not a converged phase observation**. The default driver stopped. A documented retry may enlarge this saved state to chi=72 at the same rate, solely as a warm initialization; it must independently pass its tolerance. See [NUMERICAL-NOTES.md](NUMERICAL-NOTES.md).

Partial optimizer states are saved atomically every 20 iterations and at convergence/budget stop. Scalar JSON caching is never treated as a saved MPS. Production stages use one BLAS thread, at most two heavy workers overall, a 400-iteration cap and a 900-second optimizer-stage budget. Tighter tolerance and matched-rate/free-energy systematic controls are still needed before an order adjudication.

## Dependency/status ledger at this interim snapshot

| Task | Status | Meaning |
|---|---|---|
| T0 | Complete | Method-request decision log archived without credentials; immutable inputs preserved |
| T1 | Exact checks passed; counted extension regression running | Half-row operator identities, checkpoint/contraction checks |
| T2 | Calibration passed with stated capped-control exceptions | Ising ladder and n=3 gapped-side functional controls |
| T3 | Running; one lower-chi disordered stage unconverged | Higher chi and same-rate branches not yet completed |
| T4 | Validated operator; production pending | n=3,d=3 scan follows available resource slot |
| T5 | Complete | Fourth Clifford physical twirl on rank-29 quotient |
| T6 | L4/L6 ladder complete; L8 gate pending | Finite-size split measured, critical-point split not established |
| T7 | Validated small-ring half row; MPS pilot pending | No full-period n=4 tensor materialization |
| T8 | Deferred after T3 assessment | Finite-cylinder DMRG gaps/interfaces require their own boundary/operator contract |
| T9 | Gated / deferred | Guided or resample-move SMC needs new mixing/proposal validation; old pilot is not a no-go theorem |
| T10 | Audit obligations recorded, proof open | See [PROOF-AUDIT.md](PROOF-AUDIT.md); finite numerics do not certify Haar analyticity |

## Verification and publication

The earlier 197 checks passed in fresh legacy/extension invocations. The integrated driver now includes the new half-row/fourth-Clifford extension; a fresh full regression is running. Its exit status and exact total will replace this interim statement, not be assumed from process startup.

The authorized repository is `MIKEAA2020/arena-max--physics`; ordinary non-force publication preserves its existing license/history. Generated work plus narrowly identified A-1 reproduction inputs are credential-scanned, including archive contents. See `PUBLICATION-SCOPE.md` at the project root. This interim file does not assert a push before one has succeeded and the remote commit has been checked.

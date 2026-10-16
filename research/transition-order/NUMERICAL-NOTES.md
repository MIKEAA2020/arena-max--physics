# Numerical execution notes

## 2026-10-16: validation gate

Exact half/full identities passed for n=2,d=2; n=3,d=2; n=3,d=3; n=4,d=2. The raw non-Hermitian half-row optimizer failed a complex-eigenvalue check and was rejected. Production uses the globally Hermitian direct sum and paired environments, not a real-part workaround.

The Ising ladder converged at tolerance 1e-8 through chi=64. n=3 gapped controls at p=.300 and .310 show a shrinking half/full Rayleigh discrepancy. Some lower-chi control stages hit the iteration cap; the final chi=48 p=.310 residual is 1.17e-8, close to but above that run's nominal 1e-8, and below the 3e-8 calibration ceiling. These statuses remain in the raw JSON. This is not a statement that every control run converged at its requested tolerance.

Primary production tolerance is 1e-7, with 400 iterations and a 900-second optimizer-stage ceiling; states checkpoint every 20 iterations and on convergence/budget stop. This tolerance alone does not certify free-energy convergence. A tighter matched-branch continuation is required before an order verdict.

## 2026-10-16: disordered chi=48 continuation did not converge

The .310→.306, chi=48 stage reached 400 iterations, residual 2.11e-7 against requested 1e-7. It is stored as **unconverged**, not an accepted stationary phase. The default driver stopped rather than silently proceeding.

A documented retry is permitted: use that real MPS checkpoint **only as an initialization**, enlarge to chi=72 at the same p=.306, and require the new optimizer stage to pass before continuing toward .305. This tests whether additional variational freedom improves optimization. It does not turn the lower-chi observation into a converged result, nor prove that truncation caused the failure. The explicit queue is `cases-disordered-retry.json`; the default non-advancement rule remains in place. If that retry fails, preserve its checkpoint and report the budget/iteration limitation rather than changing tolerances retrospectively.

## 2026-10-16: fourth-moment ladder

All 52 Haar/Clifford cases (13 rates × L=4,6 × two ensembles) completed with all five S4-left/right sectors. Maximum absolute eigenpair residual: 1.18e-10. The fourth Clifford transfer is built on 30 closed labels with Gram rank 29 and a pseudoinverse quotient. L=8 is gated by a measured memory/runtime benchmark, not launched as an unbounded ladder.

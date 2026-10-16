# Analytic prerequisites: audit record, not a numerical certification

16 October 2026 · A-1 / task T10

## What is checked from the current source

The v33 no-freezing statement is conditional on an analytic non-affine growth-rate branch and explicit cocycle regularity. An analytic function that is affine on a nonempty interval of a connected real-analytic domain is affine on that domain. This implication is valid. It does not establish that the physical full-Haar cocycle is analytic on that domain.

For the fully monitored finite-size Haar problem, logarithmic integrability can establish an appropriate Lyapunov growth-rate existence statement. Logarithmic integrability alone is not a theorem of real analyticity. The source now explicitly leaves that hypothesis unverified; neither the numerical replica calculations nor a source-lint pass closes it.

The reducible finite-state counterexample is concrete: an initial sector coin followed by deterministic zeros or fair bits gives `psi(k) = max(0, k log 2)`. It has affine exposed branches even though each branch separately is analytic. Finite reachability or finite state count is therefore not a replacement for the necessary irreducibility/branch and nondegeneracy assumptions. This counterexample is recomputed by `v33_checks.py`.

The interpolation identity at finite volume is exact. A sufficient uniform limiting condition is `sup_{V,s in [0,m0]} Var_s(log Z)/V < infinity`; merely bounding `Var((log Z)/V)` does not suffice. The Bernoulli extensive-variable counterexample is also recomputed in that suite. The error estimate after division by `m V` is of order m under the stated extensive bound, not quadratic in m.

## Obligations still open for the full-Haar analyticity claim

1. Specify the exact random cocycle and the definition of the quenched growth rate, including finite L, monitoring p, allowed real tilt interval and zero-probability convention.
2. Name the precise analytic-Lyapunov/transfer-operator theorem being applied, its function space and each hypothesis. A reference title or a generic positivity assertion is insufficient.
3. Establish the required analytic parameter neighborhood and integrability/dominating bounds despite arbitrarily small Haar matrix elements. Distinguish log-moment existence from the stronger hypotheses of the selected theorem.
4. Establish the relevant irreducibility/proximality or cone-contraction/spectral-gap conditions, as applicable to that theorem, throughout the claimed parameter domain. Treat exceptional or rank-deficient parameter values explicitly rather than assuming an invertible-matrix theorem covers them.
5. Prove the non-affinity/nondegeneracy claim in the actual record process, not just in an unrelated model.
6. For any thermodynamic L→infinity conclusion, add control uniform in L and justify the order of limits. Analyticity at every finite L does not prove analyticity of their limit.

**Status:** conditional implication and counterexamples checked; physical full-Haar hypothesis certificate not completed. The existing specialist proof/SM material was not supplied. No numerical workload is represented as a substitute.

## Other independent analytic programs

A Peierls/contour proof first needs identified phases, a verified contour representation and a positive uniform contour cost for this monitored operator. A permutation count of n! or a signed coordinate representation supplies none of those bounds automatically. A real-replica/loop construction is not yet supplied, so n* in (2,3) and an n→1 continuation remain conditional scenarios. These tasks have no asserted finite sandbox completion time.

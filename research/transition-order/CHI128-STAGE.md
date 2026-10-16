# Authorized chi=128 stage and interpretation contract

16 October 2026 · A-1 continuation, not an additional Lighthouse clue.

## Completed result

**Both preparations passed** the prospective chi=128 gates at p=.30486. The maximum per-preparation walltime was 41.78 minutes, below the 90-minute ceiling. Chi=192 was not launched.

| Diagnostic | Ordered-start history | Disordered-start history |
|---|---:|---:|
| Optimizer residual | 9.991479e-08 | 9.565347e-08 |
| Iterations in this stage | 186 | 79 |
| Total stage seconds | 2507.05 | 1022.75 |
| f_half | 0.9930622852597 | 0.9930622737046 |
| f_period_Rayleigh | 0.9930620839286 | 0.9930620801716 |
| m_species | 0.00028389 | 0.00390943 |
| abs(m_parity) | 0.00000114 | 0.00283729 |
| xi_chi | 59.55774 | 62.49078 |

Full-period trial-value difference, ordered-start minus disordered-start: **3.756951e-09**. The 36-orientation symmetry-aligned mixed-transfer search completed; maximum normalized fidelity per site was **0.999999488638**. The states are very similar on this per-site diagnostic, not certified exactly identical.

The large order in the earlier unconverged chi=96 ordered-start trial did **not** persist in this accepted chi=128 experiment. Both accepted solutions have small order diagnostics. This is not a demonstration of an ordered/disordered coexistence pair at this point, and it does not establish continuity or rule out a first-order transition at another rate. The older chi=96 states were unconverged and used a shorter budget and different continuation steps; this is not a clean one-variable finite-chi scaling comparison.

The half/full functional differences are about 2e-7, larger than the between-state period-value difference. Neither those discrepancies nor the small contraction defects provide a global finite-chi free-energy error bound. No physical branch ranking, coexistence location or latent heat is certified from this tiny difference.

## Decision and prospective resource allocation

The user selected **Authorize bounded chi128 stage** in the runtime-budget question. This authorizes one two-preparation stage, at most 90 minutes walltime on two single-thread CPU workers. It does not authorize an automatic chi=192 stage. No chi=96 production is repeated.

The immutable, hashed protocol is `chi128-90m-protocol.json`. Its shared measurement rate is **p=.30486**, chi=128 and requested tolerance **1e-7**. The optimizer gets at most 5280 seconds, leaving time inside the 5400-second overall deadline for observables and the same full-period contraction. The high iteration limit is subordinate to this wall-clock limit, not an authorization for an unbounded run.

Two real chi=128 partial states from the previously distinct preparation histories initialize the run. Neither source is an accepted stationary observation. They are not truncated chi=96 observations or cached scalar JSON. The source checkpoint hashes and core-code hashes are fixed before launch. Earlier chi=96 rolling checkpoints and all immutable sources are left untouched.

Before launch, the existing transfer suite passed **49/49** freshly. These are the same identities already present in the earlier 246 total, not 49 additional distinct checks. The optimizer and its dynamic inner eigensolver schedule have not been changed.

## Acceptance and bookkeeping

Each preparation must satisfy:

1. Original optimizer residual strictly below 1e-7.
2. Both left/right center compatibility residuals below 1e-7, with canonical identities below 1e-9.
3. A positive full-period contraction eigenvalue with relative contraction residual below 1e-8.

These additional validation checks are prospective; they do not relax the optimizer tolerance. Numerical stationarity here refers to the **Hermitian half-row objective**. Full-period values are evaluations on those states, not independent convergence of a full-period optimizer; the two finite-chi functionals differ. If both preparations pass, an optional mixed-transfer fidelity calculation over the 36 S3-left/right symmetry orientations compares the physical states without confusing MPS gauge or symmetry orientation with distinct phases. This is a similarity diagnostic, not an additional phase-order criterion. Real partial states are atomically saved every five iterations and at the optimizer budget stop. Bounded-stage paths do not overwrite the old rolling chi=96 states. Source segments and the new stage have separate iteration/time counters.

Raw outcomes are `n3_chi128_bounded_ordered.json` and `n3_chi128_bounded_disordered.json` under `v2.2/verify/replica/`, with matching logs and NPZ checkpoints. A process exiting is not itself acceptance. Budget stop, solver failure, stationarity failure and accepted finite-chi result remain different statuses.

## What this stage can and cannot decide

At the earlier shared-rate chi=96 stage, **neither preparation reached the residual criterion**. This is not an observation of two established stationary phases. Non-convergence alone does not discriminate metastability from critical slowing, ill-conditioning or optimizer accuracy limitations; it supplies no calibrated additional phase-order evidence.

For chi=128 as well:

- Agreement at one p does not establish continuity. A first-order model generally has a single equilibrium phase away from its coexistence point.
- Disagreement at one p does not establish first order. Symmetry-related states, finite-chi variational artifacts and optimizer failures must be distinguished.
- The appropriate next physical comparison, if this stage converges, is a rate bracket with stationary branches compared using the **same full-period functional**, followed by chi/size-systematic control of the crossing, slope/order discontinuities and correlation behavior. A single matched-rate stage is not that complete campaign.
- The thermodynamic fourth-Clifford/Haar critical-point difference remains **unknown**, not established zero.
- v33 remains an author-review draft. Keeping transition order open is legitimate, but does not supply missing original figure/SM, author approval or outstanding proof hypotheses.

## Exact illustrative counterexamples to a binary convergence rule

These are logical examples, **not** derived effective potentials for the replica model and not evidence for its continuity.

Let x=m^2 and consider, near the transition, F(t,m)=t m^2-b m^4+m^6 with fixed b>0. It has first-order coexistence at t=b^2/4, between x=0 and x=b/2. Yet for t>b^2/3 its only stationary phase is m=0. An optimizer can therefore return the same state from both preparations in a genuinely first-order model.

Conversely, on |m|<=1 let b_chi>0 tend to zero and define

    F_chi(t,m) = t m^2 + m^6 + b_chi (1-m^4).

This is an upper approximation to F_infinity=t m^2+m^6, with uniform error between 0 and b_chi. At t_chi=b_chi^2/4,

    F_chi(t_chi,m)-b_chi = x (x-b_chi/2)^2.

Thus each finite chi has **two distinct global-minimum amplitudes**, x=0 and x=b_chi/2, at the crossing. Both are locally stable: second derivatives in m are b_chi^2/2 and 2 b_chi^2. Nevertheless the conjugate-slope jump is b_chi/2 -> 0, the amplitude jump also vanishes, and the limiting transition at t=0 is continuous. Even stationary finite-chi branch coexistence and uniformly convergent variational upper energies would not by themselves prove a non-vanishing thermodynamic discontinuity.

The original framework ontology and Qur'anic commitments are not changed by these numerical or logical observations.

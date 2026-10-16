# χ128 six-rate, two-preparation scan

16 October 2026 · A-1 continuation, not a new Lighthouse clue.

**Campaign status:** running: recovered after session interruption. **Accepted paired rates:** 6/6. **New terminal preparation records:** 10/10; the two previously accepted p=.30486 states are reused, not reoptimized.

## Method, allocation and scope

The grid is p={.3040,.3045,.3047,.30486,.3050,.3055}. Each target uses the same two immutable χ128 warm sources as the verified single-point experiment, with the same Hermitian half-row optimizer and 1e-7 residual tolerance. Thus this is a fixed-initial-state matrix, **not a bidirectional continuation/hysteresis experiment**. The old sources are initializers, not accepted phase observations. No χ96 production or automatic χ192 is scheduled.

Authorized allocation: at most two single-thread CPU workers, 90 minutes per paired new rate, up to 7.5 hours overall. Real AL/AR/AC/C arrays are atomically checkpointed; FL/FR are omitted caches, recomputed on a restart. This serialization policy was checked against the unchanged optimizer. Compact review ZIPs omit the bulk scan states; the full repository preserves them.

Session recovery is recorded separately when processes do not survive a pause. Real partial states, prior JSON segments and source hashes are retained; recomputable environments are rebuilt. Checkpoint timings are lower bounds for saved optimizer segments, not an exact total including lost work or downtime. The original overall campaign deadline is not silently reset.

## Results

Preparation labels describe initial histories, not guaranteed physical phases. Only accepted rows enter observable comparisons. Missing values are not zero. Optimizer residuals and contraction defects are not global free-energy error bounds.

| p | Preparation | Status | Residual | f_period_Rayleigh | m_species | Color L2 | xi_chi |
|---:|---|---|---:|---:|---:|---:|---:|
| 0.3040000 | ordered | accepted-finite-chi | 9.79e-08 | 0.9902621372 | 0.631456 | 0.599904 | 20.81 |
| 0.3040000 | disordered | accepted-finite-chi | 8.51e-08 | 0.9902621372 | 0.631456 | 0.599904 | 20.82 |
| 0.3045000 | ordered | accepted-finite-chi | 9.54e-08 | 0.9918951764 | 0.592863 | 0.561663 | 32.81 |
| 0.3045000 | disordered | accepted-finite-chi | 9.68e-08 | 0.9918951764 | 0.592863 | 0.561665 | 32.80 |
| 0.3047000 | ordered | accepted-finite-chi | 9.89e-08 | 0.9925456753 | 0.558892 | 0.528373 | 48.19 |
| 0.3047000 | disordered | accepted-finite-chi | 9.88e-08 | 0.9925456753 | 0.558909 | 0.528386 | 48.19 |
| 0.3048600 | ordered | accepted-stationary-at-finite-chi | 9.99e-08 | 0.9930620839 | 0.000284 | 0.000448 | 59.56 |
| 0.3048600 | disordered | accepted-stationary-at-finite-chi | 9.57e-08 | 0.9930620802 | 0.003909 | 0.003719 | 62.49 |
| 0.3050000 | ordered | accepted-finite-chi | 9.92e-08 | 0.9935058481 | 0.000159 | 0.000156 | 49.53 |
| 0.3050000 | disordered | accepted-finite-chi | 8.58e-08 | 0.9935058501 | 0.001305 | 0.001263 | 50.23 |
| 0.3055000 | ordered | accepted-finite-chi | 9.91e-08 | 0.9950840479 | 0.000015 | 0.000013 | 33.57 |
| 0.3055000 | disordered | accepted-finite-chi | 9.97e-08 | 0.9950840539 | 0.000161 | 0.000143 | 33.17 |

Color L2 is a symmetry-invariant norm of the six one-point amplitudes about their uniform value, not a claim that all signed-coordinate amplitudes are probabilities. It avoids confusing orientation-dependent species components with different phases.

## Same-period differences and symmetry alignment

| p | f_period,O − f_period,D | Largest evaluated aligned fidelity/site | Orientation search |
|---:|---:|---:|---|
| 0.3040000 | 9.08e-12 | 0.9999999999 | all 36 symmetry orientations evaluated |
| 0.3045000 | 4.77e-11 | 0.9999999992 | all 36 symmetry orientations evaluated |
| 0.3047000 | -2.03e-13 | 0.9999999989 | all 36 symmetry orientations evaluated |
| 0.3048600 | 3.76e-09 | 0.9999994886 | all 36 symmetry orientations evaluated |
| 0.3050000 | -2.07e-09 | 0.9999998435 | all 36 symmetry orientations evaluated |
| 0.3055000 | -5.99e-09 | 0.9999999588 | all 36 symmetry orientations evaluated |

At p=.3047 the accepted histories have m_species 0.558892 / 0.558909 and parity 0.382684 / -0.382692. Their invariant order and symmetry-aligned comparison must be used together: opposite parity signs alone do not identify different thermal phases. Largest evaluated aligned fidelity/site is 0.9999999989. These large-order solutions are consistent with symmetry-related orientations, not evidence by themselves of ordered/disordered coexistence.

## What would count as coexistence evidence

**A finite bulk free-energy gap is not coexistence.** At a genuine first-order coexistence point, the competing bulk free-energy densities agree. A non-vanishing observable/slope jump or positive interface cost is a different quantity. Distinct stationary branches can persist off coexistence; optimizers need not merge immediately on either side.

Small sign changes of f_period,O−f_period,D between nearly equivalent solutions do not identify a branch crossing: O/D are initialization labels, not certified ordered/disordered branches. Symmetry-related ordered orientations also have equal bulk pressure away from a thermal transition.

This coarse six-point scan can locate a change, identify finite-χ competing branches or bracket a candidate crossing. It cannot guarantee that a narrow metastability window was sampled. A candidate requires distinct symmetry-inequivalent stationary branches, a properly tuned same-functional crossing, and χ/size-systematic control of any non-vanishing discontinuity. Multiple finite-χ minima alone do not establish thermodynamic first order; no separation on this grid does not prove continuity.

Numerical stationarity is for the half-row objective. Full-period values are evaluations on those states, not independently optimized full-period branches. Half/full finite-χ differences, truncation and optimizer systematics remain explicit.

The previous latent-heat proxy near .11 and physical “coexistence length 40–60” remain withdrawn/unvalidated. Reported xi_chi is an MPS length, not a certified physical coexistence length. The χ128 single-point result did not isolate χ from runtime and initialization, and does not prove that every earlier large-order χ96 trial was merely an artifact or that p=.30486 is on the thermodynamic disordered side.

**Transition-order verdict: unresolved.** No automatic classifier promotes a finite gap, a small residual, or a lack of sampled branch separation to a verdict.

## Reproduction, framework and publication

See `chi128-scan-protocol.json`, `SCAN128-ASSESSMENT.md`, raw `n3_chi128_scan.json`, per-case JSON/logs, and the actual NPZ states. Qur’anic/Lighthouse governance retains real, dependent creation distinct from the Creator; this interpretation changes neither the replica operator nor an empirical result. It is not inferred from phase order. The v34 review continuation makes that scope explicit; original v33 remains preserved.

Publication uses ordinary non-force commits, with exact-secret/nested-archive scanning. The PAT is private workspace data, excluded from every repository snapshot and review archive. Source commit receipts and final remote verification are separate from numerical convergence.

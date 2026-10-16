# Transition-order continuation — executed work and status

16 October 2026 · A-1 continuation · Reproducible observations and explicit stopping rules, not a phase-order certificate.

## 1. Decision and outcome

**Chosen primary method:** deterministic transfer-MPS/DMRG on the exact n=3 replica operator. The implemented upgrade is a validated Hermitian half-row MPO, real resumable NPZ states, higher chi and matched-rate independently prepared states. Existing VUMPS is already in this method family. Finite-cylinder gaps/interfaces are the next independent discriminant if this remains ambiguous; unvalidated large SMC is not the next production run.

**Scientific conclusion:** the previous locator **p_c approximately .3049(2)** remains the working numerical estimate; **weak first order remains a preference, not a demonstrated verdict, and continuity is unresolved**. No latent heat, interface tension or asymptotic exponent is certified by this campaign. The standard n! algebra does not depend on n=3 being first order.

See [PLAN.md](PLAN.md), [NUMERICAL-NOTES.md](NUMERICAL-NOTES.md), [FEASIBILITY.md](FEASIBILITY.md) and the machine-readable [task ledger](task-ledger.json).

## 2. Primary n=3,d=2 computation

All rows below retain their own requested tolerance/status. Local optimizer residuals are not global free-energy error bounds. Preparations named ordered/disordered identify the continuation history, not a guaranteed physical phase. For stopped rows, any listed f_half is an intermediate center-eigenvalue estimate, not an accepted stationary Ritz/free energy.

**Higher-chi ceiling:** the ordered chi=128 stage exhausted its resumed optimizer budget without convergence; the disordered chi=128 expansion was triaged before convergence. Both partial states are retained. Chi=192 was not launched. Compute was redirected to the more feasible matched-rate chi=96 test without relaxing its tolerance.

| Preparation | p | chi | f_half | m_sp / abs(m_par) | xi_chi | residual | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| disordered | 0.3048600 | 96 | 0.9930634553 | — / — | — | 8.30e-07 | budget-stopped |
| disordered | 0.3049000 | 96 | 0.9931902376 | 0.00093 / 0.00343 | 47.80 | 9.51e-08 | optimizer converged |
| disordered | 0.3050000 | 96 | 0.9935068764 | 0.00158 / 0.00110 | 43.78 | 9.90e-08 | optimizer converged |
| disordered | 0.3050000 | 128 | 0.9935060214 | — / — | — | 2.34e-05 | triage-stopped-unconverged |
| disordered | 0.3060000 | 48 | 0.9966619872 | 0.00510 / 0.00488 | 18.93 | 2.11e-07 | unconverged |
| disordered | 0.3060000 | 72 | 0.9966563741 | — / — | — | 1.04e-07 | plateau-stopped-unconverged |
| ordered | 0.3045000 | 48 | 0.9918959919 | 0.60019 / 0.42063 | 18.86 | 9.97e-08 | optimizer converged |
| ordered | 0.3048000 | 48 | 0.9928717674 | 0.56060 / 0.38327 | 23.74 | 9.16e-08 | optimizer converged |
| ordered | 0.3048000 | 72 | 0.9928704222 | 0.53897 / 0.36473 | 38.52 | 9.59e-08 | optimizer converged |
| ordered | 0.3048000 | 96 | 0.9928700670 | 0.52769 / 0.35536 | 53.20 | 9.81e-08 | optimizer converged |
| ordered | 0.3048000 | 128 | 0.9928698856 | — / — | — | 1.15e-06 | budget-stopped |
| ordered | 0.3048600 | 96 | 0.9930640344 | — / — | — | 8.75e-07 | budget-stopped |

[Full production CSV](n3-production.csv). A row pointing to a rolling `latest.npz` describes that path at the time of recording; it may since have been superseded. Immutable high-chi anchor copies are separately named. Always read checkpoint metadata rather than inferring its state from an old JSON pointer. Partial states contain actual tensors but are not accepted stationary observations.

### Matched-rate comparisons

No pair has yet passed both optimizer tolerances at exactly the same p and chi. A partial checkpoint is not substituted into that comparison.

### Frozen-trial period-Rayleigh comparison — not coexistence

This evaluates the **same full-period operator at the same p** on two saved normalized MPS trial states, even when their source optimizers failed to converge. The right fixed point and spin diagnostics are recomputed for the actual frozen AL tensors. Small contraction residuals control only the MPS expectation contraction; they do **not** bound the distance to the true transfer eigenstate, optimizer error or finite-chi bias. No crossing of these trial curves is promoted to p_c or latent heat.

| p | Preparation | f_period_Rayleigh | Contraction residual |
|---|---|---:|---:|
| 0.3048800 | ordered | 0.9931284483 | 5.84e-12 |
| 0.3048800 | disordered | 0.9931265019 | 9.69e-12 |
| 0.3048600 | ordered | 0.9930639402 | 7.60e-13 |
| 0.3048600 | disordered | 0.9930630909 | 1.58e-11 |
| 0.3049000 | ordered | 0.9931929566 | 1.30e-11 |
| 0.3049000 | disordered | 0.9931899131 | 1.00e-12 |

| Frozen preparation | Source p | Source residual | m_species | abs(m_parity) | xi_chi |
|---|---:|---:|---:|---:|---:|
| ordered | 0.3048600 | 8.75e-07 | 0.46878 | 0.30772 | 79.43 |
| disordered | 0.3048600 | 8.30e-07 | 0.00114 | 0.00419 | 50.07 |

Frozen-state evaluation status: benchmark-selected grid complete. The distinct trial order diagnostics are **not** a converged jump. This is a valid trial-state comparison, **not** the missing pair of stationary phases.

### Normalization, controls and exact optimization changes

The raw nonsymmetric half-row optimizer produced a complex effective eigenvalue and was rejected. Production uses the global direct sum H+H† with paired/transposed environments. Both summands remain in the effective-center problem, even when the redundant environment eigenproblem is reduced to one component. Exact block/map identities and independent finite-ring tests guard these optimizations.

The n=3 MPO bond is 12 rather than full-period 36; **f_half = −2 log eta_half**. Half- and full-period finite-chi functionals differ, so their agreement is checked rather than assumed.

The Ising p=.233810 chi=8,16,32,64 ladder converged at requested 1e-8; xi_chi = **39.2048, 165.8538, 681.2273, 2546.748**. For n=3,p=.300 the half/full discrepancy falls from 2.09e-7 at chi=24 to 5.79e-9 at chi=48; at p=.310 it falls from 3.97e-6 to 4.12e-7. The final p=.310 residual 1.17e-8 missed its nominal 1e-8 but passed the separately stated 3e-8 calibration ceiling. Other capped lower-chi stages are not retrospectively called converged.

Warm-stage failures, planned checkpoint resumes and per-segment times are in `optimizer-segments.json`. A later solve may use an unconverged state solely as an initialization; that does not validate the earlier observation. Production stopping/tolerance rules are recorded prospectively, not relaxed after seeing the desired phase.

## 3. Fourth Clifford versus Haar

An exact local fourth-Clifford transfer operator is now implemented on **30 closed generators with Gram rank 29**, using a Moore–Penrose quotient. Physical gate-generator commutators, Haar weights, projectors and p=1 controls pass. Independent two-qubit support-rank counts are [48,288,384], giving moments **2/5, 1/5, 1/8** at replicas 2,3,4. Haar fourth moment is **4/35**.

**52 finite cases completed**: 13 rates × L=4,6 × two ensembles, five diagonal S4-left/right sectors per case. These are not a claim to exhaust every off-diagonal representation sector or the entire spectrum.

| Diagonal sector | Haar L4/L6 crossing | Clifford L4/L6 crossing |
|---|---:|---:|
| std | 0.3583 | 0.3340 |
| sgn | 0.3698 | 0.3488 |
| two | 0.3498 | 0.3340 |
| stdsgn | 0.3688 | 0.3488 |

These are **linear-grid finite-size crossing estimates**, not finely root-solved values and not thermodynamic critical points. The maximum absolute stored eigenpair residual is 1.17e-10. The finite-size Haar/Clifford difference is resolved; a thermodynamic critical-point split is not established. See [crossing CSV](fourth-moment-crossings.csv) and [finite-size gap plot](fourth-moment-gaps.svg).

L=8 benchmark: **3.115 seconds per projected matvec**, versus an adopted 1-second gate; status **deferred-after-runtime-benchmark**. A larger ladder was not launched merely because the L=4,6 cases were cheap.

## 4. n=3,d=3 and n=4 Haar pilots

### d=3 exact finite-size crossings

| Sector | Sizes | p_star |
|---|---:|---:|
| std | 4,6 | 0.6215745 |
| std | 6,8 | 0.6274929 |
| sgn | 4,6 | 0.6271769 |
| sgn | 6,8 | 0.6322530 |

The d=3 exact cache contains 67 cases, with root tolerance 3e-6. These are finite-size locators, not p_c-infinity error bars. The bidirectional MPS pilot has 8 recorded cases, including chi=12 edge controls and chi=24 continuation.

| d=3 preparation | p | chi | f_half | m_species | abs(m_parity) | Status |
|---|---:|---:|---:|---:|---:|---|
| up | 0.5874929 | 12 | 2.900770772 | 0.88996 | 0.80961 | optimizer converged |
| up | 0.5874929 | 24 | 2.900770734 | 0.88995 | 0.80961 | optimizer converged |
| up | 0.6274929 | 24 | 3.178619073 | 0.69301 | 0.54827 | optimizer converged |
| up | 0.6874929 | 24 | 3.550437392 | 0.00000 | 0.00000 | optimizer converged |
| down | 0.6874929 | 12 | 3.550439431 | 0.00000 | 0.00000 | optimizer converged |
| down | 0.6874929 | 24 | 3.550437392 | 0.00000 | 0.00000 | optimizer converged |
| down | 0.6274929 | 24 | 3.178619073 | 0.69318 | 0.54827 | optimizer converged |
| down | 0.5874929 | 24 | 2.900770734 | 0.88995 | 0.80961 | optimizer converged |

The d=3 pilot supplies a controlled implementation/continuation check and coarse location information. It is not a fine phase-order scan or a universality assignment.

### Fourth Haar thermodynamic-MPS pilot

- Fully monitored endpoint: chi=4, f_half=4.3381074007, exact −2 log(4/35)=4.3381074007, error=2.66e-15; optimizer converged.
- p=0.38, chi=4: f_half=1.5743586552, abs(m_parity)=0.67690, xi_chi=0.945; optimizer converged.

The exact endpoint precedes the pilot. A low-chi optimizer solution is not a chi-converged thermodynamic phase determination. The approximately 1.5 GB full-period n=4 local tensor was not materialized.

## 5. Dependency and stopping ledger

| Task | Status | Outcome |
|---|---|---|
| T0 | complete | immutable inputs and credential-free method-request log preserved |
| T1 | complete | exact half-row, direct-sum, paired-environment, checkpoint and contraction checks passed |
| T2 | complete-with-stated-control-exceptions | Ising ladder; n=3 gapped functional controls; lower-chi requested-tolerance misses retained |
| T3 | partial-order-unresolved | accepted new half-row observations through chi=96; 0 accepted same-rate/same-chi pair(s); inspect nonconverged and partial states |
| T4 | finite-and-coarse-pilots-complete-fine-order-open | 67 exact cases, 4 finite crossings, 8 MPS pilot cases |
| T5 | complete | fourth Clifford physical twirl on rank-29 quotient |
| T6 | L4-L6-complete-L8-runtime-deferred | 52 cases in five diagonal colour sectors; L8 benchmark 3.115 s/matvec |
| T7 | endpoint-and-low-chi-pilot-complete | 2 n=4 Haar cases; no converged chi-to-infinity phase result |
| T8 | deferred-not-implemented | finite-cylinder gaps/interfaces need an exact boundary/operator contract and convergence controls |
| T9 | gated-deferred | guided/resample-move SMC needs separate exact/mixing/population validation; pilot failure is not a no-go |
| T10 | audit-partial-proof-open | conditional implication and counterexamples checked; full-Haar analytic hypotheses, contour/real-replica constructions open |
| T11 | deferred-feasibility-gated | n=5 rank-119 quotient/orbit-block assembler required; naive L8 Krylov memory exceeds sandbox |

The chosen method has been implemented and feasible computations executed, but unfinished mathematical and large-size jobs are not represented as complete. Missing boundary-contract, mixing or analytic-hypothesis prerequisites remain explicit. See [proof audit](PROOF-AUDIT.md) and [resource feasibility](FEASIBILITY.md).

## 6. Verification, artifacts and GitHub

Fresh integrated regression: **246/246 across 10 suites**, exit 0; transfer extension 49. Log: `v2.2/verify/run_all_transition_2026-10-16-final.log`. The current paper-only runner performs 17+35+49=101 checks. These totals validate specified finite identities and implementation contracts, not every paper theorem or a phase-order verdict.

The first ordinary GitHub push was verified at commit `b121f258cabab2c28dce4d08d74a731f8a217ad4` on `MIKEAA2020/arena-max--physics`. The final delivery includes this report as a non-force follow-up snapshot; the exact verified final commit is supplied in the completion message. Existing history/license are preserved. Credentials are excluded and nested archive contents are scanned before staging. See `PUBLICATION-SCOPE.md` at the project root.

The v33 manuscript remains an **author-review draft**, not a certified submission: the original figure/SM, author approval and specialist analytic-hypothesis audit are still required. This continuation does not rewrite the original v33 numerical claims silently. A-1 stays separate from the Lighthouse source lineage, and Parts I–II commitments are unchanged.

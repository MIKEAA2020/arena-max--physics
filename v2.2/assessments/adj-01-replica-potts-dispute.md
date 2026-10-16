# Adjudication A-1 — the n = 3 annealed replica transition: "3-state Potts, x_σ/x_ε → 1/6" (paper) versus "ratio rising through 1/6, R∞ ≈ 0.194" (engine)

**Lineage.** This is not a clue to the problem of time and is not numbered as one: it is the first item of a separate lineage, *adjudications* (A-1, A-2, …), kept in `/home/user/adjudications/` and reviewed in `assessments/adj-NN-*.md`; it has no bearing on Parts I–III and enters the plan only as a §22 provenance note. (Clue 13 remains unassigned.)

**Date:** 15 October 2026. **Inputs:** `adjudications/adj-01-a-manuscript_revised_v32.txt` (A. Abaee, revtex source; the n = 3 annealed subsection, its Table, the general-n theorem and the two-replica closure) and `adjudications/adj-01-b-engine-contradicts-paper.txt` (analyst + reviewer report). **Method:** an independent implementation of the paper's compressed n-replica transfer operator (`v2.2/verify/replica/replica_tm.py`: Weingarten weights at D = d² = 4, bond-permutation variables, the symmetric form Ŝ = G^{1/2} C G^{−1/2}, isotypic projectors of S₃ × S₃ and momentum zero), sector-resolved Lanczos to L = 16 (`replica_run.py`, cache `spectra.json`), a memory-lean power iteration for L = 18 (`replica_power.py`, `power.json`), and diagnostics the paper does not report (`replica_diag.py`, `diag.json`). A one-minute subset is in the verification suite as `verify/replica_checks.py` (13/13). All numbers below were produced in this session; nothing is quoted from either side without having been recomputed.

**Verdict in one paragraph.** Both sides' *numbers* are right; both sides' *inferences* are wrong, in opposite directions. The paper's table is reproduced to its last digit, and so are the engine's L = 10 and L = 12 values; the sequence of amplitude ratios does pass 1/6 between L = 10 and 12 and keeps rising — 0.178 at L = 14, 0.183 at L = 16 — with increments that decay more slowly than any fixed power of 1/L, so the paper's "convergence to 1/6 with a 2.5 % overshoot" is not what its own data show (the overshoot is 9.8 % at L = 16 and growing, and the n = 2 control the paper invokes converges to 1/8 *from below*, monotonically, at every size to L = 32). But the engine's replacement, R∞ = 0.194 ± 0.005, rests on an arbitrary 1/L² form: 1/L gives 0.22, a free power gives 0.20–0.21, a logarithm gives 0.24, and the data cannot choose. The reason neither extrapolation is meaningful is a fact that neither side noticed: the six-state model is, exactly, an **Ising parity variable gating two 3-state Potts species**, and its **parity sector goes critical within Δp ≈ 0.004 of the σ sector** (sgn ⊗ sgn crossings at p ≈ 0.3102 → 0.3090, std ⊗ std crossings at 0.3026 → 0.3052). Every amplitude ratio measured at L ≤ 16 is therefore a crossover quantity. If the two transitions stay distinct, the σ transition is a 3-state Potts transition of one Potts species on an ordered parity background — the paper's universality claim would then be *right*, for a symmetry reason the paper never gives, and its ratio would return to 1/6 only at sizes L ≫ ξ_parity that no transfer matrix reaches; if the two merge — and the separation of the two crossings shrinks as a steady power law through L = 18, the parity order has no support of its own in the bare weights, and the large-d limit is a first-order 6-state transition — the transition is not 3-state Potts at all and the ratio has no 1/6 meaning. L ≤ 18 cannot separate these. **The settlement run (§10, same day) does:** the thermodynamic-limit fixed point (VUMPS, χ ≤ 72) shows a *single* transition at p_c = 0.3049(2) at which the species and the parity order parameters vanish together, no parity-ordered intermediate phase at any χ, order-parameter jumps (≈ 0.56 species, ≈ 0.39 parity) that do not shrink from χ = 24 to 72, and coexistence correlation lengths ≈ 35 and growing only as χ^{0.7} — a weakly first-order transition most likely, a continuous non-Potts transition at the outside; not 3-state Potts in either case, and every L ≤ 18 ratio a crossover quantity at L < ξ. **Re-keying recommendation:** key the finite-size facts, the two-sector structure and the single-transition/first-order finding, not an asymptotic number — see §7 and §10.3.

---

## 1. What each side claims

| | Paper (v32, n = 3 annealed subsection) | Engine report (A-1b) |
|---|---|---|
| Quantity | R(L) = log(λ₁/λ_σ)/log(λ₁/λ_ε) at the crossing p*(L−2, L) of X_L = L·log(λ₁/λ_σ), evaluated at the larger size | same ratio, reported as 0.167 / 0.173 / 0.18016 at L = 10 / 12 / 14 |
| Values | 0.107 (6), 0.144 (8), 0.161 (10), 0.171 (12); p* = 0.27114, 0.29678, 0.30244, 0.30403 | fit R∞ ≈ 0.194, b ≈ 1.95; 1/ν = 1.15 |
| Inference | "→ 1/6", 3-state Potts (x_σ = 2/15, x_ε = 4/5); the +2.5 % at L = 12 is an overshoot like the n = 2 control; p_c⁽³⁾ = 0.305(3); 1/ν_eff = 1.15(10); "not a proof" | monotone rise through 1/6 ⇒ not converging to 1/6; recommend re-keying to 0.19 ± 0.005; reviewer "independently reproduced L = 14 with residuals ~10⁻¹⁵" |

## 2. Reproduction (both sides)

**Model, as implemented.** Bond variables σ_k ∈ S₃ on m = L/2 bonds; W(π | μ, ν) = Σ_τ Wg_{D=4}(π⁻¹τ) T_p(τ, μ) T_p(τ, ν) with T_p(τ, μ) = (1 − p)·2^{c(τ⁻¹μ)} + 2p; one brick layer M₁[σ; τ] = Π_k W(σ_k | τ_k, τ_{k+1}); the second layer is M₁ with the bond axes rolled; C = M₂M₁; Ŝ = G^{1/2} C G^{−1/2} with g(σ, τ) = 4^{c(σ⁻¹τ)} is symmetric to 10⁻¹⁵. Checks against every number the paper prints: the n = 2 closure (a, b, c); Wg_{D=4} = 7/360, −1/180, 1/360; twelve negative bond weights with minimum −0.10 at p = 0; the L = 6, p = 0.02 levels 0.836807 / 0.834268 (×4) / 0.831750 with their sector assignment (trivial; std ⊗ std; sgn ⊗ sgn); the n = 2 control R(10) = 0.1176, R(32) = 0.12425 (paper: 0.118, 0.1243); the dimension count. All agree (`replica_checks.py` 1–8).

**The paper's table, and its extension to L = 16 (crossing definition, value at the larger size):**

| (L₁, L₂) | p* (here) | p* (paper) | R(L₂) (here) | R (paper / engine) | X_σ* | X_ε(L₂) | X_sgn(L₂) |
|---|---|---|---|---|---|---|---|
| (4, 6) | 0.271217 | 0.27114 | 0.10695 | 0.107 | 0.7591 | 7.098 | 1.391 |
| (6, 8) | 0.296964 | 0.29678 | 0.14424 | 0.144 | 0.9418 | 6.530 | 1.662 |
| (8, 10) | 0.302628 | 0.30244 | 0.16143 | 0.161 | 1.0024 | 6.210 | 1.724 |
| (10, 12) | 0.304334 | 0.30403 | 0.17137 | 0.171 | 1.0269 | 5.992 | 1.731 |
| (12, 14) | 0.304946 | — | 0.17806 | engine 0.18016 | 1.0380 | 5.829 | 1.720 |
| (14, 16) | 0.305180 | — | 0.18302 | — | 1.0432 | 5.700 | 1.697 |

At fixed p = 0.305 (the engine's apparent convention — it reproduces the engine's 0.167 and 0.173 exactly): R = 0.14117, 0.15730, 0.16685, 0.17337, 0.17827, 0.18219, 0.18548 for L = 6 … 18 (the last by power iteration; increments 0.0039 → 0.0033, still decelerating only slowly). The engine's L = 14 value 0.18016 is 1 % above both of ours (0.1781 at the crossing, 0.1783 at p = 0.305); it would be obtained at p ≈ 0.3055. The reviewer's "residuals ~10⁻¹⁵" certify an eigen-solve, not a value of p or an inference. Immaterial to the dispute.

## 3. The paper's inference fails on its own data

1. **The sequence crosses 1/6 at L ≈ 11 and keeps rising.** Crossing values 0.171 (12), 0.178 (14), 0.183 (16): +2.8 %, +6.8 %, +9.8 % above 1/6. Increments 0.0373, 0.0172, 0.0099, 0.0067, 0.0050; ratios of successive increments 0.46, 0.58, 0.67, 0.74. A pure L^{−2} correction would give 0.54, 0.60, 0.65 at these sizes and L^{−1} would give 0.67, 0.71, 0.75: the effective correction exponent is falling from ≈ 2 toward ≈ 1 as L grows, which is the signature of a crossover or a marginal correction, not of an approach to a nearby limit.
2. **The "overshoot" rationalisation does not transfer from n = 2.** The n = 2 (Ising) control approaches 1/8 from below at every size: 0.1056 (6), 0.1176 (10), 0.1220 (16), 0.1237 (24), 0.12425 (32); its increments decay as L^{−2} (ratios 0.60–0.65). Nothing in it licenses reading a monotone rise *past* the target as an overshoot.
3. **The "gap law" check is non-probative.** The paper compares L·gap_ε = 6.0 at L = 12 with 2πx_ε = 5.03, assuming an isotropic transfer matrix. The brick-layer operator has an anisotropy factor ζ (the n = 2 calibration gives ζ = 1.19 for the Ising case; §5 below gives ζ ≈ 1.4–1.9 for n = 3 depending on the assumed c), and L·gap_ε is itself still drifting: 7.12, 6.54, 6.21, 5.99, 5.83, 5.70 at L = 6 … 16.

## 4. The engine's inference fails too

Fits of R(L) = R∞ + a L^{−b} and variants to the crossing sequence (L ≥ 8 / L ≥ 10):

| form | R∞ (L ≥ 8) | R∞ (L ≥ 10) | rms |
|---|---|---|---|
| R∞ + a/L² (the engine's) | 0.1949 | 0.1963 | 7 × 10⁻⁴ / 4 × 10⁻⁴ |
| R∞ + a/L | 0.2224 | 0.2191 | 7 × 10⁻⁴ / 1.4 × 10⁻⁴ |
| R∞ + a/L^b (b free) | 0.2041 (b = 1.49) | 0.2098 (b = 1.26) | 1.3 × 10⁻⁴ / 3 × 10⁻⁵ |
| R∞ + a/ln(L/L₀) | 0.2408 | 0.2459 | 5 × 10⁻⁵ / 2 × 10⁻⁵ |

The fixed-p = 0.305 sequence gives 0.189–0.191 (1/L²), 0.207 (1/L), 0.218–0.226 (free b ≈ 0.6–0.8), 0.26–0.28 (log). The *better-fitting* forms give the *larger* limits; the engine's "0.194 ± 0.005" is the least-well-fitting form with an error bar that ignores form dependence. Note also that a b ≈ 1.95 power law cannot be fitted through three points (0.167, 0.173, 0.180) whose increments are non-decreasing; the engine's fit must have used other points or a different definition. Its 1/ν = 1.15 agrees with the paper and discriminates nothing (3-Potts 1.2; Ising 1; 4-Potts 1.5 with logs).

## 5. What neither side saw: the model is parity-gated Potts, and the parity sector is also critical

**Structure (exact).** Write σ = c^k s^a (c a 3-cycle, s a transposition, k ∈ ℤ₃, a ∈ ℤ₂). Then σ⁻¹τ is the identity iff (k, a) = (k′, a′); a transposition iff a ≠ a′ (for every k, k′); a 3-cycle iff a = a′ and k ≠ k′ (`replica_checks.py` 10). Every weight in the model — T_p and Wg — depends only on the conjugacy classes of relative permutations, so the six-state model is *exactly*: an Ising variable a (the parity sgn σ) and a 3-state Potts label k whose interaction is switched on only between sites of equal parity. Its symmetry (S₃ × S₃) ⋊ ℤ₂ = S₃ ≀ ℤ₂ is, in these variables, independent S₃ permutations of the Potts label on the even-parity and on the odd-parity sublattices, times the parity flip that exchanges them: two 3-state Potts species living on complementary parity domains. The order parameters: sgn ⊗ sgn ∋ (−1)^a (parity); std ⊗ std ∋ ω^{±k}, (−1)^a ω^{±k} (the Potts spin of whichever species occupies a site). Potts order of a species needs a percolating parity domain, so Potts order cannot outlive parity order; the converse is allowed, and the symmetry permits an **intermediate phase**: parity ordered, Potts species disordered, std ⊗ std correlations short-ranged.

**Numerics.** Crossings of the scaled gaps in the two sectors (the σ ones are the paper's; the parity ones are new):

| pair | p*_σ (std ⊗ std) | p*_parity (sgn ⊗ sgn) | separation |
|---|---|---|---|
| (6, 8) | 0.29696 | 0.30713 | 0.0102 |
| (8, 10) | 0.30263 | 0.31021 | 0.0076 |
| (10, 12) | 0.30433 | 0.31019 | 0.0059 |
| (12, 14) | 0.30495 | 0.30962 | 0.0047 |
| (14, 16) | 0.30518 | 0.30900 (X_sgn(14) = X_sgn(16) = 1.8634 at p = 0.309) | 0.0038 |
| (16, 18) | ≈ 0.3053 (est.; σ increments 0.0057, 0.0017, 0.0006, 0.0002) | ≈ 0.3084 (L = 18 power iteration at 0.3075 and 0.309, linear interpolation) | ≈ 0.0031 |

In the window between them, at p = 0.3075, X_σ rises with L (1.057, 1.074, 1.085, 1.096, 1.106, 1.116 for L = 8 … 18: the σ channel disordering) while X_sgn falls (1.852, 1.838, 1.822, 1.809, 1.800, 1.793: the parity channel still ordered, but with decrements 0.015, 0.013, 0.010, 0.0065 that are themselves shrinking) — the intermediate-window signature at every available size, weakening with L. At p = 0.305 the parity gap scales as L^{−1.07} over L = 6–16: a sector that is, at these sizes, indistinguishable from critical. **Two readings remain open.** (S1) Two transitions with a finite asymptotic separation: an intermediate phase, parity ordered and Potts species disordered, as the symmetry permits. (S2) A merger: a single transition at which both orders vanish together. The separation of the crossings, 0.0102, 0.0076, 0.0059, 0.0047, 0.0038, ≈ 0.0031 for (6,8) … (16,18), falls as a steady power law — local exponent 1.35, 1.41, 1.47, 1.51, ≈ 1.5 — with no sign yet of levelling off, which is what a merger looks like and what a small residual separation would also look like at these sizes. Three further facts lean toward S2 without deciding it: the bare bond weights give parity no independent support (in T_p a transposition neighbour, weight 4, is cheaper than a 3-cycle neighbour, weight 2 — parity order is propped up by Potts order, not by itself, and a propped-up order generically collapses with its prop, often discontinuously); the six states are the permutation representation of S₆, whose 5-dimensional standard irrep splits under S₃ ≀ ℤ₂ into exactly the std ⊗ std (4) and sgn ⊗ sgn (1) sectors, so the large-d limit the paper itself describes as n!-state Potts-like is a *first-order* 6-state transition, and X_sgn/X_σ = 1.81, 1.76, 1.72, 1.68, 1.66, 1.63 (L = 6 … 16) is drifting toward the S₆-degenerate value 1; and the anisotropy-free ratios (next paragraph) sit near 4-state-Potts-like pseudo-critical values, which is how a weakly first-order transition with a large correlation length presents at small L. One fact leans toward S1: at every size the parity crossing lies above the σ crossing with the intermediate-window signature in between. What is *not* open is that the parity sector is near-critical at p_σ for every L ≤ 18, so every amplitude ratio in the paper and in the engine report is measured in a crossover (S1) or pseudo-critical (S2) regime.

**An anisotropy-free check the paper did not make.** From −log λ₁(L) = fL − A/L, the combinations c/x_i = 12A/X_i are independent of the unknown anisotropy ζ. Calibration at n = 2, p_c = 0.233810: c/x_σ → 4.01, c/x_ε → 0.497 (Ising: 4, 1/2) by L = 26 with four-point fits (`replica_diag.py` A). At n = 3, p = 0.305, four-point fits give c/x_σ = 9.1–9.2 and c/x_ε = 1.59–1.66 (three-point: 8.2 → 8.9 rising, 1.36 → 1.61 rising). **Pure 3-state Potts predicts 6 and 1**; 4-state Potts 8 and 2; a decoupled Ising ⊗ 3-Potts product 9.75 and 1.625. Whatever the critical theory seen at L ≤ 16 is, it is not a single 3-state Potts sector: its finite-size free energy carries the parity sector's weight. This is the quantitative form of the crossover statement, and it is independent of the ratio R.

**Consequence for universality.** (S1): on an ordered parity background the majority Potts species is an S₃-symmetric three-state model, so its transition — if continuous, as the σ data suggest — is 3-state Potts by universality, with x_σ/x_ε = 1/6 *asymptotically*; the paper's conjecture would be correct for this reason, and its ratio would turn back toward 1/6 only for L ≫ ξ_parity(p_σ), which the L^{−1.07} scaling of the parity gap puts well beyond 16 (plausibly ≳ 50). (S2): a simultaneous continuous transition of a ℤ₂ and an S₃ order is non-generic — at the decoupled Ising ⊗ 3-Potts point the energy–energy coupling has x = 1 + 4/5 < 2 and is relevant — so a merger would mean a multicritical point reached by accident or a weakly first-order transition with pseudo-critical drifts; in neither case does 1/6 apply. Under S1 the engine's 0.194 is a crossover value; under S2 it is a pseudo-critical value; under neither is it x_σ/x_ε of a fixed point.

## 6. L = 18 (power iteration, `replica_power.py`, residual < 2 × 10⁻⁵, i.e. eigenvalues to ~10⁻⁹ relative; `power.json`)

| p | L | λ₁ | X_σ | X_ε | X_sgn | R | compare L = 16 |
|---|---|---|---|---|---|---|---|
| 0.3075 | 18 | 1.27103 × 10⁻⁴ | 1.1162 | 5.598 | 1.7932 | 0.1994 | X_σ 1.1059 ↑, X_sgn 1.7997 ↓, R 0.1938 |
| 0.309 | 18 | 1.21752 × 10⁻⁴ | 1.1658 | 5.607 | 1.8673 | 0.2079 | X_σ 1.1479 ↑, X_sgn 1.8634 ↑ (parity now on the disordered side at 0.309), R 0.2010 |
| 0.305 | 18 | 1.36587 × 10⁻⁴ | 1.0373 | 5.593 | 1.6749 | 0.1855 | X_σ 1.0385 (↓ slightly: 0.305 is still just below the σ crossing), X_sgn 1.6973 ↓, R 0.1822 ↑; X_sgn/X_σ 1.634 → 1.615 |

All three runs completed (28–31 minutes each). Each p-value costs ≈ 30 minutes on two cores (10 ⁷ states, 80 MB per vector, ~100 operator applications). L = 20 (3.6 × 10⁸ states) is out of reach of this sandbox.

## 7. Adjudication and re-keying

1. **Who is right about the data?** The engine: R(L) rises monotonically through 1/6 and has not converged by L = 14 (nor by 16). The paper's "→ 1/6 with a 2.5 % overshoot" is false as a description of the computed sequence.
2. **Who is right about the asymptote?** Neither has shown anything. 0.194 ± 0.005 is one form among several that fit worse than the alternatives; 1/6 is reachable only through a crossover that the paper did not identify and cannot resolve at its sizes.
3. **Who is right about the universality class?** Neither — settled in §10: a single weakly-first-order (at the outside, continuous non-Potts) transition at p_c = 0.3049(2), not 3-state Potts. (As written before the settlement run:) Undecided by the available finite-size numerics. The paper's 3-state Potts assignment has a symmetry basis (parity-gated Potts) that makes it the *expected* answer if the parity and σ transitions are distinct; it is the wrong answer if they merge, which the shrinking separation of the crossings, the bare weights and the large-d limit make the somewhat better-supported reading — in which case the transition may well be weakly first-order and every "exponent" in the subsection a pseudo-critical one. The paper itself calls the assignment "not a proof"; that sentence is the only fully correct one in the subsection.
4. **Key, as recommended.** Do not key 1/6; do not key 0.194 ± 0.005. Key: (i) the finite-size sequence R = 0.107, 0.144, 0.161, 0.171, 0.178, 0.183 (crossing definition, L = 6 … 16; ±0.001 across definitions and p-conventions at fixed L; the engine's 0.180 at L = 14 is 1 % high); (ii) "passes 1/6 at L ≈ 11; increments decay more slowly than L^{−2}; the asymptotic value is undetermined from L ≤ 16 (admissible extrapolations 0.19–0.25) and may be 1/6 after a crossover"; (iii) "a second sector (sgn ⊗ sgn, parity) is critical within Δp ≈ 0.004 of the σ transition; amplitude ratios at these sizes are crossover quantities." Scoring: an answer asserting 1/6 as demonstrated is wrong; an answer asserting R∞ = 0.19 ± 0.005 as established is wrong; an answer reporting the rising sequence and declining to extrapolate is right; an answer that identifies the parity sector or the two-transition structure is best. If the harness insists on a single number for "the ratio at L = 14", key 0.178 ± 0.002. (After §10:) add to (iii) "the thermodynamic-limit fixed point shows one transition at p_c = 0.3049(2) with both order parameters lost together, most likely weakly first-order; neither 1/6 nor 0.194 describes it", and score an answer that identifies the single transition or the first-order possibility best.
5. **On "engine yield".** The engine added two things an unaided reader could not: the L = 14 point and the monotone-rise observation. It subtracted one: an extrapolation stated with false precision. The missing analysis — sector resolution of the second order parameter — was available at L ≤ 12 in seconds (`replica_checks.py` 11–12 run in under a minute) and was missed by the paper, the analyst and the reviewer alike, because all three only ever looked at the two levels the paper named.

## 8. What would settle it (programme; executed in §10)

(a) DMRG/MPS on the transfer operator (the negative bond weights rule out Monte Carlo) at L ≈ 40–100 in the window 0.305–0.310: does the parity gap close at a p distinct from the σ gap, and does the separation of the two crossings level off or go to zero? (b) The parity order parameter ⟨(−1)^a⟩ in the ground state at p = 0.3075 versus L. (c′) A first-order test at the same sizes: the ε gap at the transition closing exponentially (coexistence) rather than as 1/L, and a double-peaked energy histogram in the ground state. (d) For the paper's larger programme: the same parity/species decomposition applies at every n (S_n = A_n ⋊ ℤ₂), so the n = 4 claim "4-state Potts with logarithmic corrections at p_c⁽⁴⁾ ≈ 0.383" needs the same sector-resolved check before it is keyed either way.

## 9. Bearing on v2.2

None on Parts I–II. The paper is a monitored-circuits paper by the author of clues 5 and 8, with the same profile: an exact layer that verifies completely (every printed number reproduced) and an interpretive layer that overreaches (a universality claim inferred from a ratio that its own data contradict). Recorded at §22.14 (as adjudication A-1, a separate lineage) and §23.2 items 107–108; scripts in `verify/replica/`; `replica_checks.py` (17 checks) in `run_all.sh`.

## 10. Settlement run (15 October 2026, later the same day): the thermodynamic-limit fixed point by VUMPS, and the n = 4 sector check

The programme of §8 was executed in the form that fits a 2-core/2 GB sandbox: instead of DMRG on rings of L ≈ 40–100, the dominant eigenvector of the transfer operator was computed **directly in the thermodynamic limit** as a uniform matrix-product state (VUMPS: Zauner-Stauber et al., PRB 97, 045145 (2018); Fishman et al., PRB 98, 235148 (2018), for 2D classical transfer matrices), at bond dimensions χ = 24, 48, 72, and the n = 4 claim was given the same sector resolution at L = 4, 6, 8. Code: `v2.2/verify/replica/replica_vumps.py` (MPO, VUMPS, observables, scan drivers), `replica_n4.py`, `n4_cross.py`, `vumps_table.py`; data: `vumps_n3*.json`, `control_n2_chi24.json`, `n4.json`; logs `scan_chi*.log`, `n4_L*.log`. Checks 14–17 of `replica_checks.py` cover the construction, the n = 2 control, the n = 4 crossings and the n = 3 "no intermediate phase" statement.

**10.1 Construction and validation.** The one-period operator C = M₁ T M₁ of `replica_tm.py` is written as a uniform MPO of bond dimension N² = 36: W[(a₂,a₁),(b₂,b₁); σ,τ] = δ(a₁,τ)·W(σ | a₂, b₂)·W(b₂ | τ, b₁), conjugated site-wise by g^{±1/2} (g[s,t] = 4^{c(s⁻¹t)}) into the symmetric form Ŝ, whose left and right dominant eigenvectors coincide, so one uniform MPS serves as bra and ket. Contracted on a ring, the MPO reproduces the dense operator of the earlier sections to 7 × 10⁻¹⁸ (n = 3, L = 6) and 1.4 × 10⁻¹⁷ (n = 2, L = 8), and Ŝ is symmetric to 4 × 10⁻¹⁷ (check 14). Observables: the free energy per bond site f = −ln η; the entanglement entropy S of the half-chain; the stat-mech order parameters ⟨(−1)^a⟩ (parity, sgn ⊗ sgn) and |⟨ω^k⟩| (species, std ⊗ std), evaluated with g^{1/2} O g^{−1/2} inside the symmetric state; the correlation lengths of the parity and species channels from connected two-point functions out to r = 2000; and ξ_χ from the MPS transfer matrix. **n = 2 control at the exact Ising point p_c = 0.233810:** ξ_χ = 42.1, 175.1, 722, 2700 for χ = 8, 16, 32, 64, i.e. ξ_χ ∝ χ^κ with κ = 2.05, 2.04, 1.90 against the c = ½ prediction 2.03; m ∝ ξ_χ^{−0.130, −0.122, −0.127} against β/ν = 0.125; f = 0.470269248 converged to 10⁻⁹; and a χ = 24 sweep up and down through p_c (with 10⁻³ random kicks on the way down) gives identical states to five decimals at every p — no hysteresis — with m falling continuously 0.648 → 0.535 → 0.475 → 0.368 → 0 and ξ_χ peaking at 460 (check 15; `control_n2_chi24.json`). The method therefore resolves a continuous transition of this family correctly at these χ.

**10.2 n = 3: the ordered and disordered branches, χ = 24, 48, 72.** Upward sweeps start deep in the ordered phase and warm-start each p from the previous one; downward sweeps start in the disordered phase and add a 10⁻³ random kick to the MPS at every step (a state that survives the kick is a genuine local optimum, not a symmetric saddle). Selected rows (f per bond site; |m_par| = |⟨(−1)^a⟩|; m_sp = |⟨ω^k⟩|; ξ_sp, ξ_par the channel correlation lengths; ξ_χ the MPS correlation length):

| χ | sweep | p | f | S | \|m_par\| | m_sp | ξ_sp | ξ_par | ξ_χ |
|---|---|---|---|---|---|---|---|---|---|
| 24 | up | 0.3040 | 0.99026625 | 0.378 | 0.463 | 0.642 | 9.2 | 9.3 | 9.3 |
| 24 | up | 0.3050 | 0.99353019 | 0.501 | 0.400 | 0.581 | 12.3 | 12.3 | 12.3 |
| 24 | up | 0.3052 | 0.99417885 | 0.550 | 0.376 | 0.557 | 13.3 | 13.4 | 13.6 |
| 24 | up | 0.3054 | 0.99482523 | 0.625 | 0.340 | 0.519 | 15.2 | 15.3 | 15.5 |
| 24 | up | 0.3056 | 0.99546782 | 0.785 | 0.257 | 0.427 | — | 18.7 | 19.0 |
| 24 | up | 0.3058 | 0.99609868 | 1.059 | 0.013 | 0.130 | 16.6 | 17.0 | 17.0 |
| 24 | up | 0.3060 | 0.99669705 | 1.071 | 0.000 | 0.000 | 10.9 | 7.0 | 10.9 |
| 24 | down | 0.3056 | 0.99544664 | 1.091 | 0.000 | 0.000 | 11.4 | 7.4 | 11.4 |
| 24 | down | 0.3050 | 0.99356663 | 1.123 | 0.000 | 0.000 | 12.4 | 8.0 | 12.4 |
| 24 | down | 0.3045 | 0.99199551 | 1.154 | 0.000 | 0.000 | 13.4 | 8.7 | 13.4 |
| 24 | down | 0.3040 | 0.99026625 | 0.378 | 0.463 | 0.642 | 9.2 | 9.3 | 9.3 |
| 48 | up | 0.3040 | 0.99026239 | 0.408 | 0.454 | 0.633 | 14.9 | 15.1 | 15.1 |
| 48 | up | 0.3050 | 0.99351839 | 0.822 | 0.293 | 0.454 | 40.5 | 40.6 | 40.9 |
| 48 | up | 0.3053 | 0.99446209 | 1.212 | 0.002 | 0.016 | 22.5 | 21.5 | 24.8 |
| 48 | up | 0.3060 | 0.99666041 | 1.144 | 0.001 | 0.006 | 18.0 | 14.5 | 19.5 |
| 48 | up | 0.3075 | 1.00134249 | 1.051 | 0.000 | 0.002 | 13.6 | 9.8 | 14.4 |
| 48 | up | 0.3100 | 1.00908359 | 0.954 | 0.000 | 0.000 | 10.2 | 7.1 | 10.7 |
| 48 | down | 0.3056 | 0.99540554 | 1.178 | 0.002 | 0.009 | 20.4 | 16.6 | 21.5 |
| 48 | down | 0.3053 | 0.99446225 | 1.209 | 0.002 | 0.014 | 22.5 | 20.2 | 24.2 |
| 48 | down | 0.3051 | 0.99383221 | 1.233 | 0.001 | 0.023 | 24.7 | 24.1 | 26.9 |
| 48 | down | 0.3050 | 0.99351678 | 1.246 | 0.002 | 0.031 | 26.6 | 27.3 | 29.2 |
| 48 | down | 0.3048 | 0.99287146 | 0.585 | 0.380 | 0.557 | 25.4 | 25.4 | 25.6 |
| 48 | down | 0.3045 | 0.99189581 | 0.486 | 0.419 | 0.599 | 19.1 | 19.1 | 19.2 |
| 72 | up | 0.3040 | 0.99026218 | 0.412 | 0.452 | 0.632 | 17.6 | 17.7 | 17.8 |
| 72 | up | 0.3047 | 0.99254592 | 0.578 | 0.387 | 0.564 | 33.9 | 34.0 | 34.0 |
| 72 | up | 0.3050 | 0.99350866 | 1.311 | 0.000 | 0.009 | 35.2 | 33.2 | 38.2 |
| 72 | down | 0.3056 | 0.99540012 | 1.210 | 0.000 | 0.002 | 25.2 | 18.5 | 26.5 |

(The χ = 72 downward sweep below p = 0.3056 — 0.3053, 0.3050, 0.3048, 0.3046 — was still running when this record was written; its rows are appended to `vumps_n3_down72.json` and `scan_chi72_down.log` as they complete and do not enter the conclusions below, which rest on the χ = 72 upward sweep and the complete χ = 24 and χ = 48 sweeps in both directions.)

(The χ = 24 "up" row at 0.3056 has no species length because the connected species correlator had not reached its asymptotic decay by r = 2000 in that state. In the ordered states the species order sits entirely on one parity class, as it must; the sign of ⟨(−1)^a⟩ is the symmetry-related choice of which class, and |m_par| is quoted.)

**(a) One transition, not two.** At every χ the parity and the species order parameters vanish *together*: at χ = 24 both are ≈ 0.5 at p = 0.3054 and both are gone by 0.3060; at χ = 48 (0.380, 0.557) at 0.3048 becomes (0.002, 0.031) at 0.3050; at χ = 72 (0.387, 0.564) at 0.3047 becomes (0.000, 0.009) at 0.3050. **No state with parity order and no species order appears at any χ or any p** (check 17 scans every converged state in the scan files). This is decisive against reading S1 of §5. Finite bond dimension *enlarges* ordered regions (it is the symmetric critical state that an MPS cannot represent; the n = 2 control shows the finite-χ ordered phase overshooting p_c), so a parity-ordered intermediate phase of width Δp ≈ 0.003–0.004 — what the L ≤ 18 crossings suggested — would have appeared enlarged at χ = 24, not suppressed. The two crossing sequences of §5 therefore converge to the same point, and the parity sector has the *shorter* correlation length in the disordered phase (ξ_par/ξ_sp = 0.65–0.80 for p ≥ 0.306, approaching 1 at the transition) — its gap closes "later" in the finite-size sequence because it is the larger gap, not because it is a separate transition. The residual separation visible at the melting edge (species order outliving parity order by one grid step: 0.3058 at χ = 24, 0.3050 at χ = 48) is the finite-χ melting sequence of a single transition; any true separation is < 0.0003 in p. **(b)** The parity order parameter at p = 0.3075 is zero at every χ (|⟨(−1)^a⟩| < 5 × 10⁻⁴ at χ = 48), and the parity channel there is gapped with ξ_par = 6.0, 9.8 (χ = 24, 48): p = 0.3075 lies in the disordered phase. The "intermediate window" of §5 was a finite-size effect.

**Location.** The free energies of the ordered and disordered branches cross at p_c(χ) = 0.30538 (χ = 24; slopes 3.265 and 3.130), 0.30498 (χ = 48; the branches at 0.3048 and 0.3050) and ≈ 0.3049 (χ = 72; ordered at 0.3047, disordered at 0.3050, with the disordered state already the better variational state at 0.3050 even when the sweep arrives from the ordered side). **p_c = 0.3049(2)**, slightly *below* the L = 16–18 crossing estimate 0.3052–0.3053 and inside the paper's 0.305(3).

**(c′) Order of the transition — what χ ≤ 72 can and cannot say.** Four finite-χ diagnostics, with their trend from χ = 24 to 72:

| diagnostic | χ = 24 | χ = 48 | χ = 72 | reading |
|---|---|---|---|---|
| coexistence/hysteresis window (both branches as kicked local optima) | 0.3045–0.3058 (≈ 0.0013) | 0.3048–0.3050 (≤ 0.0002) | none resolved (ordered branch collapses at 0.3050 on the way up) | shrinking: continuous-like |
| ξ_χ at the transition, disordered side (p = 0.3050) | 12.4 | 29.2 | 38.2 | growing but decelerating: χ^{1.2} then χ^{0.66} |
| ξ at the transition, ordered edge | 15.5 (0.3054) | 25.5 (0.3048) | 34.0 (0.3047) | χ^{0.7} throughout |
| order-parameter jump at the ordered edge (m_sp, \|m_par\|) | 0.52, 0.34 | 0.56, 0.38 | 0.56, 0.39 | **not decreasing**: first-order-like |
| latent-heat proxy Δ(df/dp) between branches | 0.131 | 0.113 | 0.111 | levelling at ≈ 0.11: first-order-like |
| S on the disordered side at p_c | 1.12 | 1.25 | 1.31 | ΔS/Δln ξ = 0.14 then 0.24: no clean (c/6) ln ξ law |

For a continuous transition the ordered-edge order parameter must fall as ξ_χ^{−x_σ}: with any x_σ in the candidate range (0.125–0.135) it should have dropped by ≈ 10 % between χ = 24 and 72; it rose by 8 %. For a continuous transition with c between 0.8 and 1.3 the correlation length at the transition should grow as χ^{1.2–1.5}; it grows as χ^{0.7} and the growth is slowing. Both point to a transition at which the two phases coexist with finite correlation lengths of order 40–60, i.e. **a weakly first-order transition**, as the large-d limit of the same model (a 6-state transition) and the bare weights (§5) suggested. Against this, the metastable branches lose their stability with increasing χ, and the entanglement at the transition keeps growing; a continuous transition in a class with both order parameters critical and unusually strong corrections cannot be excluded by χ ≤ 72. Either way: the L ≤ 18 rings are *smaller* than the correlation length at the transition (≥ 35), so every finite-size quantity in the paper's subsection and in the engine's report — the crossing sequence, the amplitude ratios 0.107 → 0.185, 1/ν_eff = 1.15, the c/x estimates of §5 — is a crossover quantity with no asymptotic meaning, which is why the ratio sequence drifts without settling and why its extrapolations disagree.

**(d) n = 4 (`replica_n4.py`, full S₄ × S₄ colour resolution at momentum zero, L = 4, 6, 8; dimensions 576, 13 824, 331 776).** The paper's std ⊗ std crossings are reproduced — (4,6): 0.3583 vs the paper's 0.35820; (6,8): 0.3790 vs 0.37899 — and so is its amplitude-ratio sequence at p = 0.383: 0.131, 0.183, 0.214 at L = 4, 6, 8 (paper 0.1315, 0.1829, 0.2142). The other sectors cross elsewhere:

| sector (λ ⊗ λ) | p*(4,6) | p*(6,8) | X at the (6,8) crossing | X/X_ε there |
|---|---|---|---|---|
| std (the paper's σ) | 0.3583 | 0.3790 | 1.048 | 0.203 |
| two (2-dim irrep) | 0.3502 | 0.3797 | 1.427 | 0.277 |
| std ⊗ sgn | 0.3688 | 0.3882 | 1.954 | 0.379 |
| sgn (parity) | 0.3698 | 0.3939 | 2.705 | 0.524 |

The parity crossing lies 0.0115 above the σ crossing at (4,6) and 0.0149 above it at (6,8) — moving *away*, not converging — and X_sgn ≈ 2.3–2.7 at these sizes means the parity correlation length is about L/2.5 ≈ 3 lattice units: the sgn and std ⊗ sgn sectors are nowhere near scaling at L ≤ 8 (nor at L = 10). The n = 4 assignment "q = 4 Potts with logarithmic corrections" is thus, like the n = 3 one was, a single-sector statement made at sizes where three other sectors with gaps of the same order have not been examined; given the n = 3 outcome (the sectors do not separate into distinct transitions, and the transition is at best marginally continuous), it should be keyed as *unestablished*, with p_c⁽⁴⁾ ≈ 0.38 as the only robust number (the std and two crossings agree on 0.379–0.380).

**10.3 Settlement.** (1) The n = 3 annealed transition is a single transition at p_c = 0.3049(2) at which the Potts-species and the Ising-parity order parameters disappear together; there is no parity-ordered intermediate phase. (2) It is not a 3-state Potts transition: a 3-state Potts critical point has one order parameter, and here the second one is critical (or jumps) at the same point; the best-supported reading at χ ≤ 72 is a weakly first-order transition with coexistence correlation lengths of order 40–60, the alternative a continuous transition in a class that is not 3-state Potts. In neither case does x_σ/x_ε = 1/6 describe the transition. (3) The engine's R∞ = 0.194 ± 0.005 describes nothing either: the ratio sequence is a crossover quantity at L < ξ. (4) The paper's p_c⁽³⁾ = 0.305(3) is right; its universality claim is wrong; its own caveat ("not a proof") was the correct statement. (5) The paper's n = 4 claim inherits the same unexamined sector structure and is unestablished. Re-keying: as in §7 item 4, with the class now keyed as "single transition at 0.3049(2); not 3-state Potts; weakly first-order most likely; not continuous-Potts and not R∞ = 0.194", and an answer that identifies the two-sector structure or the first-order possibility scored best.

**10.4 χ = 96 extension (15 October 2026, evening; `vumps_n3_chi96_{ord,mid,dis}.json`, logs `chi96_*.log`, table by `chi96_table.py`).** Three warm-started chains 48 → 72 → 96 at fixed p (each stage initialised from the previous χ; the p = 0.3050 chain happened to start, at χ = 48, in the ordered local optimum, which then melted at χ = 72 into the disordered state with f = 0.99350864 — equal to the earlier up-sweep value 0.99350866 — so at χ = 72 the point p = 0.3050 is disordered from either side: no metastability resolved there).

| p | χ | f | S | m_par | m_sp | ξ_χ | iterations |
|---|---|---|---|---|---|---|---|
| 0.3047 | 48 | 0.99254674 | 0.543 | +0.397 | 0.575 | 22.8 | 42 |
| 0.3047 | 72 | 0.99254592 | 0.579 | +0.387 | 0.564 | 33.6 | 124 |
| 0.3047 | 96 | 0.99254575 | 0.593 | +0.384 | 0.561 | 41.2 | 39 |
| 0.3048 | 48 | 0.99287146 | 0.585 | +0.380 | 0.557 | 25.6 | 45 |
| 0.3048 | 72 | 0.99287032 | 0.652 | +0.363 | 0.536 | 41.6 | 142 |
| 0.3048 | 96 | 0.99287002 | 0.692 | +0.353 | 0.525 | 56.8 | 39 |
| 0.3050 | 48 | 0.99351843 | 0.782 | +0.306 | 0.471 | 38.2 | 126 (ordered local optimum) |
| 0.3050 | 72 | 0.99350864 | 1.311 | −0.006 | 0.005 | 39.1 | 124 (disordered) |
| 0.3050 | 96 | 0.99350654 | 1.345 | +0.00006 | 0.00065 | 45.4 | 286 (disordered; completed 15 Oct 21:00 UTC / 16 Oct local) |

Effective exponents between successive χ (ξ_χ as the length scale): at p = 0.3047, κ_eff = 0.96 then 0.71 and β/ν_eff (species, parity) = (0.047, 0.060) then (0.032, 0.040); at p = 0.3048, κ_eff = 1.20 then 1.09 and β/ν_eff = (0.077, 0.096) then (0.068, 0.083). (ξ_sp, ξ_par read 208 at p = 0.3048, χ = 96 — the spurious ordered-phase reading noted before; ξ_χ is the usable scale there.)

**Reading, corrected 16 October 2026.** The completed disordered χ = 96 point lowers the approximate linear two-branch crossing to p* ≈ 0.30487 (ordered slope 3.2427, disordered slope 3.152); p_c ≈ 0.3049(2) remains a numerical estimate, not a certified bound. Persistent order and branch slopes favor weak first order, but ξ_χ has not converged and resolved hysteresis vanishes with increasing χ. The lengths 40–60 above are finite-χ lengths, not measured coexistence lengths. The fixed-p effective exponents above are off-critical diagnostics; they are not asymptotic β/ν values or bounds on ν. Earlier phrases assigning a definite ξ_coex or excluding every continuous class from those slopes are superseded. The previous Potts evidence and the report's asymptotic 0.194 claim remain withdrawn. No parity-only state was found in the scans; this is not a theorem of nonexistence.

The independent tilted-Clifford SMC is now implemented and validated, but its L = 64/128 pilots at p ≈ 0.305 retain only 4–5 / 1–2 distinct mid-time ancestors, and an L = 32 population ladder shows drift. Thus a completed sign-free run is not yet a controlled coexistence test. Current governing assessment and implemented paper: `adj-01-paper-improvement-plan-v2.md` / `papers/v33/REVISION-REPORT.md`. The n! symmetry comparison is standard algebra with a conditional orbit count, not a proof of first order. All replacement-class, real-replica and endpoint claims carry their explicit status there.

Resume note: the chain state is not stored in the JSON (only observables), so a stage cannot be warm-resumed from the file; rerun the whole chain into a fresh output file, e.g. `VUMPS_OUT=vumps_n3_chi96_dis2.json python3 replica_vumps.py chiscan 3 0.3050 48,72,96 chi96 400` (≈ 25–90 min on one core; the χ = 96 near-critical disordered stage is the slow one, 100–300 iterations at 12–17 s each).

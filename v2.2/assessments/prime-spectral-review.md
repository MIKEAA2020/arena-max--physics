# Review: "The Prime-Spectral Framework: Theorems, Conjectures, and Numerical Tests" (clue #6b)

Source: `clues/clue-06b-prime-spectral.tex` (LaTeX, ≈30.8k words). Checks: `v2.2/verify/primon_checks.py` (35/35 PASS, log in `primon_checks.log`), exploratory probe `v2.2/verify/sector_probe.py`.
Grading uses the Lighthouse scale ([C] confirmed/theorem · [H] well-posed hypothesis · [P] permissible model/interpretation · [F] fails).

## 1. One-paragraph verdict

The manuscript is a careful *demotion* document: it takes an informal "prime-spectral" cosmology and sorts it into theorems (all elementary and correct), registered conjectures C1–C12 (graded A/B/C, each with a falsifier), and two executed numerical programs whose results are **negative** and honestly reported. The theorem layer is sound but is, with one or two exceptions, textbook material (Julia's primon gas, Bost–Connes-type Hagedorn pole, Kronecker/Bohr almost-periodicity, Pólya recurrence, Kronecker–Weber/Chebotarev). The physics layer is entirely conjectural and the manuscript says so. What it under-reports is that its central negative result (C4 "obstruction") is measured against the **wrong null model**: a few-mode bosonic sector with f = d−1 classical degrees of freedom is not expected to show many-body strong-ETH scaling D^{-1/2}, and in d = 3, 4 the tested systems are not quantum-chaotic at all (⟨r⟩ ≈ 0.13–0.20 and ≈ 0.41 by its own numbers, reproduced here), so ETH makes no prediction for them. The "obstruction side" verdict should be downgraded to "no test performed in the ETH regime" except in d = 5, where the measured exponent is within ~1–2σ of the correct few-body benchmark 3/8. For the governing framework (v2.2) the manuscript's only load-bearing contact points are (i) the arithmetic clock theorem "the arrow cannot live here" (agrees with Prop 11.1), (ii) the Past Hypothesis "localized, not dissolved" (agrees with Prop 11.1/D-14 and contradicts clue #4's "arithmetic necessity" slogan), and (iii) a worked example of the register-and-falsifier discipline §24 asks for.

## 2. Theorem layer — verified

| Item | Statement | Status | Check |
|---|---|---|---|
| ℓ²(ℕ) ≅ Fock space Γ(ℓ²(𝒫)); H_P = ħω₀ log N̂ self-adjoint, simple spectrum, |1⟩ unique vacuum | [C] | unique factorization; 1.x |
| Z(β) = ζ(βħω₀), Hagedorn pole at σ = 1, ⟨E⟩ = −ħω₀ ζ'/ζ | [C] (Julia 1990; Spector; Bakas–Bowick; Bost–Connes 1995) | 1.x |
| Log-count identity: −log 2 ≤ log N(E) − E/ħω₀ ≤ 0, defect ≤ 2e^{−x}, smoothed growth rate exactly 1/ħω₀ | [C] | 2.x |
| Hardy–Ramanujan / Erdős–Kac for ω(n) under the **uniform** measure on n ≤ x; ensemble bridge canonical ≠ microcanonical | [C]; correctly stated | 3.x (under the zeta measure ω(n) has finite mean Σ_p p^{−σ}, no log log growth — the manuscript's own caveat, confirmed) |
| ζ_{ℚ(i)} = ζ·L(χ₋₄); Dedekind–Kummer, Chebotarev, Kronecker–Weber | [C] (standard) | — (minor: "entire on the half-plane" should read "holomorphic on Re s > 0 except the simple pole at s = 1") |
| Thm noperiod: exact periodicity ⇔ support ⊂ powers of one integer; ray version ⇔ one multiplicative coset | [C] | 4.x |
| Bohr almost-periodicity of the free flow for every ℓ² state; Dirichlet bound τ ≤ (2πC_F/ε)^{m_F} | [C] | 5.x |
| Pólya: multiplicative walk recurrent d ≤ 2, transient d ≥ 3 | [C] (Pólya 1921) | — |
| Zeta clock: covariance, kernel ζ(2ν ∓ iω₀Δτ)/ζ(2ν), Bochner positivity, Lorentzian peak, ⟨H⟩·Δτ_{1/2} → ħ | [C] | 6.x |
| Thm bohr: clock kernel almost periodic ⇒ no arrow in the clock | [C] | 6.x |
| Two-mode sector: picket fence, Krawtchouk eigenvectors, ⟨k₁⟩ linear in E | [C] | 7.x (passes with the manuscript's ordered-pair convention 2h₁₂ + VS) |
| Sector blocks Hermitian; kinetic term S_d-covariant at h = 0; log p diagonal breaks it | [C] | 7.x |
| Composite integers are product states; entanglement is superpositional (CHSH etc.) | [C] | — |
| Conditional Bekenstein–Hawking: assume E_max(A) = ħω₀A/4ℓ_P² ⇒ S = A/4ℓ_P² | [C] as a conditional, but **circular**: the premise *is* the area law divided by T_H | 9.x |

Small corrections to the theorem layer:
1. Thm noperiod, last sentence: the obstruction for H_tot is irrational **ratios** of energies in the support (vector periodicity) or of energy differences (ray periodicity), not an "irrational difference in units of ħ/ω₀".
2. "Generic return τ_ε ≳ ε^{−D}" is a heuristic lower bound (pigeonhole gives only upper bounds); it holds for Diophantine-generic frequencies, which should be said.
3. "Saturates Mandelstam–Tamm": the bound is in terms of ΔE, not ⟨E⟩; near the pole they coincide to O(1), so "saturates up to an O(1) constant" is the correct claim.
4. Prop returnbound's polynomial-in-entropy statement holds for states of *bounded or typical* support (m_F ≲ M log log x); for primorial-type supports m_F ~ x/log x and the bound is super-polynomial — the register entry C2 should carry that qualifier.
5. Hartnoll–Yang is arXiv:2502.02661 (2025), *The Conformal Primon Gas at the End of Time*, not 2026 — and its content is weaker for C1 than the manuscript implies: the near-singularity states are odd Maass forms whose L-functions are partition functions of Hecke-twisted primon gases with state-dependent chemical potentials; Z = ζ itself is not obtained (see `adelic-bridge-review.md`).

## 3. The numerical programs

### 3.1 C4 (ETH on the prime lattice) — wrong null model

What the manuscript measures. Occupation-sector ladders H^{(S)} on d = 3, 4, 5 modes (primes 2,3,5,7,11), kinetic completion V Σ(n_p+n_q)(a_p†a_q + h.c.) at fixed V = 0.3 (interaction-dominated) or at matched dose VS² = 36 (→ free limit). Diagnostics: κ = σ_ETH/std_basis of the mode-1 occupation in a 350-state median window; ⟨r⟩; PR/D; diagonal vs microcanonical. Verdict reported: "no rung crosses the Haar line √(2/n); κ flat at 0.19 (d=3), 0.14 (d=4); α = 0.195–0.26 (d=5) against the strong-ETH D^{−1/2}"; registered as "settled on the obstruction side".

Independent reproduction (`primon_checks.py` §8, `sector_probe.py`): with the same model (h = 0, V = 0.3, U = 0) I obtain in d = 3: ⟨r⟩ = 0.20 → 0.13 (S = 20 → 80), κ flat (slope −0.02), and a growing population of **(near-)exact doublets** (7% → 26% of window spacings below 10⁻³ of the mean) — the S₃ multiplet skeleton of the isotropic kinetic term, which the prime-log diagonal splits only weakly (the manuscript's "paired subpopulation", 64 of 350 at S = 116). In d = 4: ⟨r⟩ = 0.39–0.42, κ flat (slope −0.07). The ±30% anisotropic control removes the doublets but leaves ⟨r⟩ at 0.30–0.35, far from the GOE value 0.531. All of this matches the manuscript's numbers qualitatively.

Why the verdict does not follow.
1. **ETH is a hypothesis about quantum-chaotic systems.** In d = 3 and d = 4 the fixed-V windows are not in the GOE class (⟨r⟩ ≈ 0.15 and ≈ 0.41; the manuscript's own "stays off the GOE band"). Classical Lyapunov exponents of 0.03–0.11 at d = 3 are consistent with a mixed phase space; Eckhardt et al. (1995) explicitly predict *slower* decay of eigenstate fluctuations for mixed systems because of sticking. A flat κ in a non-chaotic few-mode system is the expected outcome, not an obstruction to thermalization "on the prime lattice".
2. **The benchmark is wrong even where the system is chaotic.** For a system with f classical degrees of freedom the semiclassical theory (Feingold–Peres 1986; Eckhardt–Fishman–Keating–Agam–Main–Müller 1995) gives Var(A_nn) ∝ 1/T_H ∝ ħ^{f−1}; with sector dimension n ∝ ħ_eff^{−f} (ħ_eff = 1/S on ℂP^{d−1}, f = d−1) this is κ ∝ n^{−(f−1)/(2f)}: **0 for d = 2, 1/4 for d = 3, 1/3 for d = 4, 3/8 for d = 5**. The many-body "strong-ETH" D^{−1/2} is the f → ∞ limit. The d = 2 "analytic obstruction floor" is simply f = 1 (one degree of freedom cannot be chaotic), and the "Haar line √(2/n)" is not a prediction of ETH for any finite f.
3. **Only d = 5 is a test**, and there the measured exponents (0.195 ± 0.082 seed-7; 0.26 with interval [0.158, 0.367] on replicates) sit within ~1–2σ below the few-body benchmark 0.375, over a range of ħ_eff of barely a factor 2–3 (S ≈ 12–28), where pre-asymptotic corrections are expected. The honest statement is: *consistent with few-body semiclassical ETH, inconsistent with the (inapplicable) many-body line.*
4. **Symmetry resolution.** At h = 0 the kinetic term is exactly S_d-covariant and the prime-log diagonal breaks it only at relative strength O(1/(VS)); ETH must be applied within symmetry sectors, and n̂₁ is not S_d-invariant, so an unresolved window carries an O(1) inter-multiplet term that never decays. The ±30% anisotropic control breaks S_d but not enough to reach GOE in d = 3, so it does not settle the point. A clean test needs (a) O(1) symmetry breaking or sector resolution, (b) a window certified GOE (⟨r⟩ ≈ 0.53), and (c) the exponent compared with (f−1)/(2f), with S large enough for a decade in ħ_eff.
5. The "matched-dose" family (VS² = const) is the free, integrable limit (the manuscript says so); its D^{−0.19} decay is the approach to a one-body spectrum, not an ETH exponent.

Net: C4's register entry should read "untested in the ETH regime for d ≤ 4; d = 5 compatible with few-body ETH; many-body scaling not applicable to finite-mode sectors". The *mathematical* programme the manuscript proposes (obstruction theorem κ/B_count ≥ c_d > 1) would, if proved, be a statement about few-mode semiclassics, not about arithmetic. A test that could bear on *arithmetic* thermalization needs the mode count to grow with the energy (the manuscript's own Remark on mode counts), i.e. f → ∞ with E, which none of the ladders do.

### 3.2 C9 (Chebotarev branching test) — ill-posed hook, correct execution

The protocol (common group order N, class sizes c_i | N, Σc_i = N, Monte-Carlo null, frozen before fitting) is well engineered, and the Z-pole and W results are clean exclusions. Three problems remain:
1. **Category.** Chebotarev densities count *primes* with a given Frobenius class in an arithmetic ensemble; decay branching ratios are dynamical quantities (couplings, phase space, QCD corrections, running). Nothing in the "dictionary" links the two beyond the word "branching", so a negative result at any scale carries no information about C9, and the "unification-scale placement" makes it unfalsifiable by this route at accessible energies.
2. **Not a discriminator from Lie GUTs.** Lie-group unification also predicts rational numbers at the unification scale (sin²θ_W = 3/8 in SU(5), Clebsch–Gordan ratios), so condition (ii) does not do the work the text assigns to it ("quite unlike the free parameters of Lie-group GUTs").
3. **Higgs "flag" is an artefact of the group-order range.** The registered range is N ∈ [5, 360]; the Higgs fits fire at N = 3672 and N = 3168 with 8–50% channel uncertainties. Any 7-vector is approximated by c_i/N with N ~ 3000 to ~1/3000, so the rule fires by construction once N is unbounded; the manuscript's own power check (0/100 recovery) says the same. The entry should be struck, not "flagged".

## 4. Conjecture layer — grading against the Lighthouse scale

| Register | Manuscript grade | Lighthouse grade | Reason |
|---|---|---|---|
| C1 spectral equivalence (BH near-singularity Z = ζ) | A | [H] | One external programme (Hartnoll–Yang 2025) in a BKL/conformal limit; no level-statistics derivation; grade A overstates evidence (the text admits this) |
| C2 arithmetic cutoff / polynomial recurrence | B | [H] with qualifier (typical support) | see §2 item 4 |
| C3 holographic bound | A | [P] | Conditional theorem is circular (premise is the area law ÷ T_H). Deeper mismatch: S_primon = E/T_H is linear in E, S_BH ∝ E²; C_primon = +∞ at T_H, C_BH < 0; universal ω₀ incompatible with E_max = Mc² (manuscript's own remark). Only the area *coefficient* survives, by construction |
| C4 cascade/ETH | A, "obstruction side" | [H] untested (d ≤ 4) / compatible (d = 5) | §3.1 |
| C5 arithmetic–chaos (GUE for BKL billiards) | B | [H]→ contradicted as stated | The BKL billiard is the modular/Bianchi-group billiard, whose Laplace spectrum (Maass forms) is Poissonian — arithmetic quantum chaos (Bogomolny et al. 1992; Bolte–Steil–Steiner 1992); GUE belongs to the L-function zeros, which are nodes of the wavefunction in Hartnoll–Yang, not levels |
| C6 Hagedorn wall as singularity | B | [P] | Interpretive; no BKL computation |
| C7 Janus boundary condition (Past Hypothesis localized) | B | [H] — agrees with v2.2 Prop 11.1 | Correctly demoted from "necessity" to conjecture; "any symmetry-like principle must select |1⟩" is a hope, not an argument (Hartle–Hawking selects a different object) |
| C8 two-sided entropy | B | [P] | Carroll–Chen/Barbour analogue; no test |
| C9 Galois–gauge dictionary | B | [P] | §3.2; "no proton decay" is the only clean prediction, shared with many non-GUT scenarios |
| C10 CP as σ-odd sector | B | [P] | no observable derived |
| C11 hierarchy (E_cut ≈ 74ħω₀) | B | [P] | relocation, as stated |
| C12 perspectival Everett | C | [P] | interpretation; conflicts with v2.2 G20 (actualization) — not adjudicable here |

## 5. Contact points with v2.2

1. **Arrow of time.** Thm bohr ("the arrow cannot live in the clock") and the relocation of all irreversibility to interaction + boundary condition are exactly Prop 11.1 (arrow needs a contingent low-entropy state; no spectrum supplies it). Record as independent support, with the manuscript's clock as a worked instance of D-14's "almost-periodic clock" branch.
2. **Problem of time.** The zeta-clock section supplies the kinematical Page–Wootters level only; the clock states are non-orthogonal (kernel ≠ δ), the covariant POVM is weighted by n^{−2ν} rather than resolving the identity, and the constraint is not solved. Its own sentence "all incompatibilities of principle dissolve at the kinematical level" contradicts its earlier "no claim is made that this section dissolves the problem of time"; keep the latter (v2.2 §23.2: "dissolution = relabeling").
3. **Past Hypothesis.** "Localizes, not dissolves" matches v2.2; the clue-#4 slogan "Past Hypothesis as arithmetic necessity" is explicitly withdrawn by the manuscript itself. Nothing in it reopens D-10/A9.
4. **Register discipline.** The A/B/C + M/P falsifier typing, pre-registration, replicate controls and the public repository are the §24 rules in practice; adopt the M/P typing for v2.2 §19.1 registers.
5. **Bost–Connes anchor (v2.2 §11.8).** The manuscript's Hagedorn/KMS material is the σ > 1 part of the Bost–Connes system; it adds nothing to the symmetry-breaking phase that §11.8 flagged as the interesting part.
6. **Lighthouse rule "candidates only".** Every physics claim here is a candidate ([H]/[P]); none is admissible as a premise in Part I.

## 6. Steelman and completion

Steelman (what survives at full strength): (a) a clean, fully elementary demonstration that *a free spectrum, however arithmetic, cannot carry an arrow* — the strongest form of the "no arrow from kinematics" lemma we had only argued; (b) the recurrence trichotomy (exact return forbidden; ε-return universal; walk transient for d ≥ 3), useful as a template for D-14; (c) the "register or demote" method. Completion supplied here: the few-body semiclassical null (§3.1), the symmetry-resolution requirement, the d = 2 floor explained as f = 1, the Higgs artefact, the Chebotarev category point, the S ∝ E vs S ∝ E² mismatch for C3, and the corrected citations. Recommended next computation for the authors: d = 5–7 ladders, O(1) symmetry breaking, GOE-certified windows, exponent vs (f−1)/(2f) over ≥ 1 decade in ħ_eff; and a genuinely many-mode truncation (primes ≤ X with X growing with E) if the claim is to be about arithmetic rather than about ℂP^{d−1} semiclassics.

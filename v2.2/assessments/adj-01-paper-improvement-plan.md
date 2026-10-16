# Adjudication A-1 — follow-up: how `manuscript_revised_v32` can be *substantially* improved

**Superseded (16 October 2026):** This is the historical first plan. Its unconditional n*, n ≥ 3 first-order, exponent-bound, endpoint and 30-independent-label claims are corrected in `adj-01-paper-improvement-plan-v2.md` and the implemented `papers/v33/REVISION-REPORT.md`. Do not treat this file as the current claim ledger.

Companion to `adj-01-replica-potts-dispute.md` (settlement: single transition at
p_c^{(3)} = 0.3049(2), not 3-state Potts, weakly first-order most likely). This note answers
the author's question "how can the paper be substantially improved — novelty, impact,
coherence — building on the settled result", and records the retract-vs-reframe decision.
It is advisory about the author's paper; nothing here changes v2.2.

Date: 15 Oct 2026. Inputs: `adjudications/adj-01-a-manuscript_revised_v32.txt` (line numbers
below refer to it), the VUMPS data in `v2.2/verify/replica/`, and the sources listed in §9.

---

## 0. One-paragraph summary

The paper's genuinely new and durable content is (i) the exact linear-channel / rank /
closure theory, (ii) the exact n = 2 triangular-Ising point (Bao–Choi–Altman's Eq. 65,
re-derived with certificates), (iii) the record-multifractality formalism with the
annealed–quenched interpolation identity, and (iv) the Clifford dyadic identity
Λ(k) = (2Lt)^{-1} ln Z̄_{k+1} for k = 1, 2 (2-design / 3-design). What is wrong is the
universality-class layer at n ≥ 3 (q = n Potts; "q > 4 criterion"). The upgrade that
turns a corrected paper into a *stronger* paper is to make the thing the paper already
computes — the annealed record-moment free energy f(n, p) — the single spine, and to state
the new structural facts about it that the settlement makes visible: the ladder is
first-order from n = 3 on (q = n! lore, not q = n), so there is a replica changeover
n* ∈ (2, 3) between the exactly continuous n = 2 rung and the first-order rungs; the
physical n → 1 end sits on the continuous side, and a smooth continuation of the ladder
lands at p ≈ 0.16–0.17, where the Born-rule transition of the same circuit is; and, by the
paper's own 3-design identity, the n = 3 first-order point is a first-order large-deviation
transition of the *Clifford random-outcome count*, testable without any sign problem and
without MPS truncation by a tilted stabilizer SMC. These are new claims (n*, q = n!, the
sector structure of the order parameter as the regular S_n-bimodule, the Clifford
coexistence test, the ladder's n → ∞ and d → ∞ ends) that no one else can make as cheaply,
because the paper already owns the exact machinery.

---

## 1. What is settled (the inputs the rewrite must respect)

| n | p_c (annealed, d = 2) | order | status |
|---|---|---|---|
| 1 (quenched, Born rule) | 0.1597(8) Clifford [paper App. A]; 0.17(1) Haar [Zabalo et al. 2020] | continuous, ν ≈ 1.24–1.3 | literature + paper |
| 2 | 0.233810 (exact) | continuous, triangular Ising | exact (BCA Eq. 65; paper Thm.) |
| 3 | 0.3049(2) | **weakly first-order most likely**; continuous non-Potts with ξ ≳ 60 not excluded; *not* 3-state Potts | VUMPS χ = 24–72(–96), this adjudication |
| 4 | ≈ 0.38 (std-sector crossings 0.358/0.379, sgn sector 0.37/0.39 at L ≤ 8) | unestablished; "q = 4 Potts + logs" rests on one sector at L ≤ 10 | paper + `n4_cross.py` |
| 5 | ≈ 0.47 (L ≤ 8) | first-order plausible (two-phase gap), but not by a q > 4 Potts criterion | paper |

Numbers behind the n = 3 verdict (χ = 24 / 48 / 72): f-crossing p_c(χ) = 0.30538 / 0.30498 /
≈0.3049; order parameters at the ordered edge (m_sp, |m_par|) = (0.52, 0.34) / (0.56, 0.38) /
(0.56, 0.39) — not shrinking with χ; ξ at the ordered edge 15.5 / 25.5 / 34.0 (∝ χ^0.7, slowing);
ξ_χ on the disordered side at p = 0.305: 12.4 / 29.2 / 38.2; latent-heat proxy
Δ(∂f/∂p) = 0.131 / 0.113 / 0.111 (≈ 3.4 % of ∂f/∂p ≈ 3.2); hysteresis 0.0013 / ≤ 0.0002 / none.
Both order parameters (parity-Ising and species-Potts) vanish at the same point; no
partially ordered phase exists (`replica_checks.py` check 17). χ = 96 (chains 48 → 72 → 96,
`chi96_*.log`, assessment §10.4): the ordered branch survives at p = 0.3048 with
(m_sp, |m_par|) = (0.525, 0.353) and ξ_χ = 57, and at p = 0.3047 with (0.561, 0.384) and
ξ_χ = 41; p = 0.3050 is disordered at χ = 72 from either start; β/ν_eff = 0.03–0.08. So
p_c(96) ∈ (0.3048, 0.3050) and the order remains "weakly first-order or continuous with
anomalously small β/ν" — not Potts either way; χ ≤ 96 cannot separate the two (hence
Upgrade 3).

---

## 2. Upgrade 1 — make f(n, p) the spine: "the replica phase diagram of the monitored circuit"

The paper already contains the identification but uses it only as a remark (Def. records,
line ~994: the annealed version at k = 1 − n "is computed by the n-replica operator"; Clifford
section: Λ(k) = (2Lt)^{-1} ln Z̄_{k+1}). Promote it to the organizing object:

  f(n, p) := − lim (LT)^{-1} log E_ω Σ_Y P_ω(Y)^n = − τ_ann(q = n, p) = − 2 Λ(n − 1; p)

with the singular set {p_c(n)} and the order of each singularity. Everything in the paper is
a face of this one function:

* Sec. II (linear channels, rank, exact n = 2): f at integer n ≥ 2, computed by transfer
  matrices / VUMPS.
* Sec. IV (record multifractality): f at real q, the annealed record spectrum; the ladder is
  the phase boundary of the annealed multifractal spectrum.
* Sec. IV-Clifford (dyadic identity): f(2, p) and f(3, p) are exactly the k = 1, 2 scaled
  cumulant generating functions of the Clifford random-outcome count N_rand.
* Sec. III (complexity): why f at n → 1 for Haar is not efficiently accessible while the
  Clifford rungs are.
* n → 1: f(1, p) ≡ 0 identically (Σ_Y P = 1), so the bulk singularity of f(n, ·) must have
  an amplitude that vanishes as n → 1; what survives in ∂_n f|_{n=1} = Born-averaged
  record-entropy density s(p) is a weak singularity of specific-heat type,
  |p − p_c|^{2ν} ≈ |p − p_c|^{2.6} (hyperscaling with 2 space-time dimensions, ν ≈ 1.3).
  This reconciles thm:nofreeze and the smooth x̄_L(p) of the Clifford section with the
  replica continuation, and it says precisely *why* the n ≥ 2 rungs are visible bulk
  transitions while the physical transition is invisible in the bulk free energy. This
  paragraph does not exist in the paper and it ties Secs. II, IV and App. A together.

Three *new* statements about f(n, p) at d = 2 become available:

(a) **Replica changeover.** n = 2 is exactly continuous (Ising); n = 3 is (most likely)
first-order; n = 4, 5 are first-order by the paper's own two-phase diagnostics once these are
re-read as in §5 below. Hence a changeover n* ∈ (2, 3): the n-family of annealed transitions
changes order between the exact Ising rung and the first rung above it, exactly as the Potts
family changes order at q = 4. The physical limit n → 1 lies on the continuous side,
consistent with the continuous Born-rule transition (ν ≈ 1.3). Conjectural corollary for
field theory: any one-parameter family of replica CFTs that is meant to reach the MIPT at
n → 1 and passes through the Ising point at n = 2 must terminate (merge with a tricritical
branch, as Potts does at q = 4) at some n* < 3. This is a sharp, new, falsifiable constraint
on proposed theories of the d = 2 MIPT, and it is a direct consequence of the settlement.

(b) **Continuation to the Born-rule point.** The ladder is nearly linear in n:
p_c(2) = 0.2338, p_c(3) = 0.3049, p_c(4) ≈ 0.380, p_c(5) ≈ 0.47 (increments 0.071, 0.075,
0.09). Continuing to n = 1 gives 0.163 (linear through n = 2, 3), 0.167–0.170 (quadratic
through n = 2, 3, 4 with p_c(4) = 0.380–0.383), 0.156 (cubic through all four, least
reliable): i.e. p_c(1) ≈ 0.16–0.17, bracketing the quenched Haar value 0.17(1) and the
Clifford locator 0.1597(8). This is the first quantitative consistency check that the
annealed ladder *is* the replica continuation of the Born-rule transition; it cannot
discriminate Haar from Clifford at n → 1 (the n = 2, 3 rungs are shared by both ensembles,
§4). State it as a conjecture with the fits shown, never as a derivation (there is no
a-priori analyticity in n: the integer-n models have different symmetry groups).

(c) **The two ends of the ladder.** n → ∞: Σ_Y P^n is dominated by the most probable
records; in the Clifford form E[2^{−(n−1)N_rand}] the tilt suppresses every random outcome
by 2^{−(n−1)}, i.e. the tilted ensemble is driven toward measurement-poor / outcome-
deterministic histories, so the ordered (volume-law) phase expands and p_c(n) should
approach 1 (heuristic; the growing increments 0.071, 0.075, 0.09 point the same way). d → ∞ at
fixed n ≥ 2: same mechanism with suppression d^{1−n} per measured site; the paper's own exact
p_c^{(2)}(d) = (d − θ_c)/(d − 1) = 0.234, 0.460, 0.595, 0.679, 0.847 (d = 2, 3, 4, 5, 10) shows
it. Contrast: the quenched (n → 1) d → ∞ limit is percolation at 1/2. So the double limit
(n → 1, d → ∞) does not commute — which is the cleanest possible statement of the paper's
recurring theme "annealed points recede from the quenched one", and it should replace the
verbal version in rem:whyqn(ii).

The paper's three-way "structures often conflated" framing (abstract, line 41) becomes
"one object, three faces", which is what a reader can remember.

---

## 3. Upgrade 2 — the right Potts analogy is q = n!, and the order parameter is the regular S_n-bimodule

Replace rem:whyqn(i) ("std has dimension n − 1 = q − 1, hence q = n Potts") by an exact
statement:

**Proposition (order-parameter sectors).** The site space of the n-replica model is C[S_n]
with the symmetry (S_n × S_n) ⋊ Z_2 acting by σ ↦ gσh^{−1}, σ ↦ σ^{−1}. As an
S_n × S_n-module, C[S_n] = ⊕_λ V_λ ⊗ V_λ*. The ordered phase breaks the symmetry to the
diagonal, leaving |S_n| = n! coexisting ordered states permuted transitively by the symmetry;
the magnetization sectors are the non-trivial isotypic components V_λ ⊗ V_λ, λ ≠ triv.

* n = 2: sgn ⊗ sgn (1-dim): Ising, q = 2! = 2 — both analogies agree, so n = 2 could not
  discriminate them.
* n = 3: (sgn ⊗ sgn) ⊕ (std ⊗ std) = 1 + 4 = 5 = 6 − 1: the "parity-Ising" and "species"
  order parameters found in the adjudication (S_3 ≀ Z_2; parity Ising with J = ln 2, 3-Potts
  with J = ln 4 on same-parity bonds). In 6-state Potts (full S_6) these five components are
  degenerate; the replica model's reduced symmetry (order 72 ⊂ 720) splits them, which is
  exactly the std-vs-sgn crossing offset seen at L ≤ 18 (0.305 vs 0.307–0.308) with a common
  p_c in the limit.
* n = 4: (sgn ⊗ sgn) ⊕ (std ⊗ std) ⊕ (std′ ⊗ std′) ⊕ (V_{(2,2)} ⊗ V_{(2,2)}) = 1 + 9 + 9 + 4
  = 23 = 24 − 1: the paper tracked only the 9-fold std ⊗ std sector (line 722); the
  `n4_cross.py` crossings show the sgn sector separated by ≈ 0.01–0.02 at L ≤ 8.

The Potts count that matters for the order of the transition is the number of coexisting
ordered states, q_eff = n! (this is Vasseur–Potter–You–Ludwig's q = n! at large bond
dimension), not the dimension of one irreducible sector. With q_eff = 6, 24, 120 the
two-dimensional lore predicts first order for every n ≥ 3 and continuity only at n = 2 —
which is what the data now say, with the first-order strength increasing with n: n = 3 is
weak (ξ_coex ≈ 40–60 transfer-matrix sites ≈ 70–120 qubit spacings; compare 6-state Potts,
ξ ≈ 159), n = 4 was "marginal" at L = 6 → 8, n = 5 clearly first-order at L ≤ 8. The
"x_σ/x_ε → 1/6" sequence (0.107, 0.144, 0.161, 0.171, 0.178, 0.183 at L = 4–16 pairs) is
then a crossover of a weakly first-order transition through a Potts-looking value, not an
exponent ratio. Reduced symmetry *can* rescue continuity in principle (clock-type models),
which is why the order had to be measured rather than inferred; the paper should say so.

This is a small theorem plus a reinterpretation, and it makes the whole ladder coherent in
one sentence: "a q = n! permutation-Potts family with reduced symmetry, continuous only at
n = 2".

---

## 4. Upgrade 3 — use the 3-design identity where it matters: a sign-free, truncation-free test of first order

rem:cliff3design + prop:z3closure establish Λ_L(2) = (2Lt)^{−1} ln Z̄_3 as an identity and
evaluate it only at p = 0.16, 0.22, L ≤ 16 (Table z3exact). The identity is far more valuable
at p = 0.305:

**Claim to add.** The annealed n = 3 transition at p_c = 0.3049(2) is a first-order
large-deviation transition of the Clifford random-outcome count: in the ensemble of
Clifford brickwork circuits tilted by 4^{−N_rand(ω,C)}, two phases coexist at p_c — an
outcome-random, measurement-rich phase and an outcome-deterministic, measurement-poor
phase — with a discontinuity in the tilted densities (the VUMPS Δ(∂f/∂p) ≈ 0.11 per
transfer-matrix site, ≈ 3 % of the density itself) and a tunnelling gap exp(−σL).

**Test.** Sequential Monte Carlo / cloning on stabilizer tableaux: walkers = (tableau mod
signs, since N_rand does not depend on outcomes), per-layer weight
4^{−(random outcomes in the layer)}, systematic resampling. All weights positive; cost
O(L²) per measurement; L = 64–256, T = 8L is a workstation job. Observables: histogram of the
per-period random-outcome density x (bimodal at p_c if first order; unimodal and narrowing
as L^{−1/ν}-type if continuous), the jump of ⟨x⟩_tilted across p_c, the system-size
dependence of the switching rate. The paper already owns the estimator (Sec. IV SMC with
N = 384 particles, line 1321) and the tableau code (App. A); only the tilt exponent and the
monitoring rate change. This closes the one gap the VUMPS evidence leaves open (ξ_coex
comparable to ξ_χ at χ ≤ 96) with an independent method.

Two cheaper companions: (i) the n = 2 rung, E[2^{−N_rand}], is the exact Ising point
0.233810 — the same SMC at large L reproduces the log-divergent specific heat of the
random-outcome count, a striking demonstration that a Clifford record statistic has an
Ising transition; (ii) thermodynamic-limit values of Λ(2) near the transition from VUMPS
(f(0.3047) = 0.99254592, f(0.3050) = 0.99350866 at χ = 72 in the code's per-site units)
upgrade Table z3exact from "L ≤ 16 away from p_c" to "L = ∞ at p_c".

**n = 4 and non-stabilizerness.** For n ≥ 4 the Clifford and Haar ladders separate (the
paper measured the n = 4 twirl deviation 0.578). The Clifford n = 4 rung is still exactly
computable: the commutant of the 4-fold Clifford action is spanned by the 30 stochastic
Lagrangian operators of Gross–Nezami–Walter, so a 30-label transfer matrix (instead of 24)
gives p_c^{Cl}(4) and E[8^{−N_rand}] exactly, while VUMPS gives the Haar p_c(4) ≈ 0.38. Their
difference is the first appearance of magic in annealed replica physics — a new, concrete,
publishable object that the paper's machinery is uniquely placed to compute.

---

## 5. Upgrade 4 — replace the class claims by a quantified first-order ladder

What to compute (all with the paper's existing operators; costs from this sandbox at
1 core, 2 GB):

1. n = 3, d = 2: VUMPS χ = 96, 128, 192 (χ = 96 ≈ 17 s/iteration; 100–300 iterations per
   near-critical point). Report p_c(χ), m at the ordered edge, ξ_χ(p_c) vs χ (saturation ⇒
   first order; unbounded χ^κ ⇒ continuous), Δ(∂f/∂p)(χ), and the metastability window.
   Replace Fig./Table of the Potts ratios by this table.
2. n = 3, d = 3: same MPO shape (6 labels), only the Weingarten weights change — the
   cheapest new datum in the paper. It gives the d-trend of p_c(3, d) (expected → 1) and of
   ξ_coex(d), and connects to the large-d permutation-Potts limit.
3. n = 4, d = 2: single-layer MPO with 24 labels, χ ≈ 64–128. Needs a two-sided (non-
   symmetric) fixed point because the Weingarten weights are not positive, or the
   sector-reduced MPO. Deliverables: p_c(4) to ±0.001, order, ξ_coex(4) (expected
   ≪ ξ_coex(3)), Δe(4).
4. n = 5: too heavy for single-layer MPS at χ ≳ 50 (120 labels); keep the L ≤ 8 two-phase
   diagnostics but re-calibrate them (next item).
5. Re-calibration of the size-ladder test (Table n5twosize, lines ~839–849). The test used
   n = 3 as its *continuous control*. n = 3 is itself weakly first-order with
   ξ_coex ≈ 40–60 ≫ L = 8, so at L ≤ 8 the diagnostics cannot discriminate order; they rank
   ξ_coex/L. Reinterpret honestly: "the closing-factor and L·gap diagnostics order the three
   rungs by first-order strength, ξ(5) < ξ(4) < ξ(3), consistent with q_eff = n!"; the
   n = 5 first-order conclusion survives, its logic changes.
6. Changeover estimate: with Δe(n) and ξ_coex(n) at n = 3, 4 (and Δe(2) = 0), bracket n*;
   a Potts-like essential-singularity form ξ_coex ∼ exp(c/√(n − n*)) is the natural ansatz,
   but with two or three points say only n* ∈ (2, 3).

What to drop: the "registered prediction" for the n = 4, L = 10 crossing (it predicts a
finite-size number, not a class — move to SM at most); the "q > 4 criterion"; the keyword
"Potts universality classes".

---

## 6. Upgrade 5 — analytic anchors and a theorem-level target

* **Large-d structure (state, don't prove).** At large d the site channel
  T_p(σ,τ)/[(1−p)d^n] = δ_{στ} + O(d^{−1}) + [p/(1−p)] d^{1−n} is a q = n! permutation-Potts
  model with reduced symmetry and with measurements acting as annealed bond dilution of
  weight ∝ d^{1−n}: hence p_c(n, d) → 1, the n = 2 formula being the exact instance. The
  order along the d-axis is an open question worth one sentence (annealed dilution of a
  q > 4 Potts model can end in a percolation-like continuous point as the dilution end is
  approached); the d = 3 run of §5.2 is the first datum.
* **Rigorous first order at large d (program).** For n ≥ 3 and d ≥ d_0(n), Pirogov–Sinai
  theory in the complex-weight form (Borgs–Imbrie 1989) is the natural tool to prove a
  first-order transition in a q = n!-state model whose weights are not positive (Weingarten
  signs). Kotecký–Shlosman needs reflection positivity, which the Weingarten weights
  probably break; Borgs–Imbrie does not. Feasibility is unknown; it is the right theorem to
  name in the outlook of a paper whose identity is "exact finite-dimensional statements".
* **Making n continuous (frontier).** The changeover n* is only a tricritical/merger point if
  n can be varied continuously, as q can in Potts through the FK cluster expansion. The
  n = 2 model has an FK representation (Ising). Finding a cluster/loop representation of the
  Haar replica model in which n (or n!) enters as a fugacity — with signed cluster weights
  from Weingarten — would turn the ladder into a one-parameter family and n* into a
  computable point. This is the open frontier the settlement exposes; name it as such.

---

## 7. Coherence: a concrete table of contents for v33

I. Exact linear structure (unchanged in substance): channels, rank certificates, exact
closure, approximate designs, the n = 2 triangular-Ising point (credited to Bao–Choi–Altman
Eq. 65 in abstract and theorem statement; the new content is the transfer-matrix form,
the rank certificate and the Clifford identity).

II. The replica phase diagram f(n, p): definition; the exact n = 2 rung; the n = 3 rung by
VUMPS (p_c, order, coexistence data); n = 4 (p_c, order from VUMPS if done, else bounds);
n = 5 (two-phase diagnostics, re-calibrated); the order-parameter proposition (§3); the
changeover n* and the ends of the ladder (§2); the continuation to n → 1 (§2b) as a
conjecture.

III. Record multifractality and complexity (unchanged), now introduced as "f at real q":
the ladder is the phase boundary of the annealed record spectrum; thm:nofreeze and the
(n − 1)-vanishing of the bulk singularity.

IV. Clifford: the dyadic identity; Λ(1), Λ(2) at and near their transitions; the tilted
SMC test of coexistence at n = 3 (new); the n = 4 Haar–Clifford splitting (new or outlook).

V. Discussion: what the ladder constrains in replica field theories (n* < 3; continuous
branch through Ising at n = 2 to c → 0 at n → 1); what remains open.

A retrospective subsection in II ("What L ≤ 18 showed, and why it misled") keeps the
crossing-ratio sequence as a documented crossover; it is methodologically valuable (a
weakly first-order transition with ξ ≈ 40–60 produces an apparent exponent ratio drifting
through a Potts value at L ≈ 12–14).

---

## 8. Retract or reframe — decision and wording

**Decision: retract the class claims outright; reframe only the reasoning that survives.**

Retract (abstract, introduction, Sec. II headings, rem:whyqn(i), conclusion, keywords):
* "n = 3 annealed point is in the three-state Potts class (x_σ/x_ε → 1/6)";
* "n = 4 is q = 4 Potts with logarithmic corrections";
* "the q = n Potts conjecture and the q > 4 first-order criterion predict n = 5".

Keep, with changed reasoning: p_c^{(3)} = 0.305(3) → 0.3049(2); p_c^{(4)} ≈ 0.38; "n = 5 is
first-order" (now: as n = 3 and 4 are, by direct evidence, with q_eff = n! as the heuristic).

Why retraction rather than "hypothesis tested and corrected" at the headline level:
1. The abstract's claims are contradicted, not merely unproven. Calling them hypotheses in
   the abstract would misstate the evidential status to a reader who reads only the abstract.
2. The replacement is probable, not certain ("weakly first-order most likely; a continuous
   non-Potts transition with ξ ≳ 60 is not excluded at χ ≤ 96"). Honest asymmetry: the
   withdrawal is certain, the replacement is graded. A retraction lets the paper say both.
3. "Tested and corrected" is the right frame *inside the body* (the retrospective subsection
   of §7), where the L ≤ 18 data, the drift of the ratio and the reason it misled are
   exhibited. That paragraph is a result, not an apology.
4. If v32 was circulated (arXiv or a submitted version), add a dated version note listing the
   withdrawn statements and the replacement numbers; referees and readers reward this and
   punish silent edits.

Suggested abstract sentence: "Exact symmetry-resolved transfer matrices and uniform
matrix-product-state computations locate the annealed critical points at n = 3, 4 (and
n = 5) and show that, unlike the exactly solvable continuous n = 2 point, the n = 3
transition is weakly first-order (coexistence correlation length ≈ 10² lattice spacings),
with the first-order character strengthening with n: the ladder is a q = n! permutation-
Potts family with reduced symmetry, continuous only at n = 2. An earlier identification of
the n = 3, 4 points with q = 3, 4 Potts classes, based on L ≤ 18 crossing ratios, is
withdrawn; those ratios are a crossover of the weakly first-order transition."

---

## 9. Sources used in this note

* Zabalo, Gullans, Wilson, Gopalakrishnan, Huse, Pixley, PRB 101, 060301(R) (2020),
  arXiv:1911.00008: Haar brickwork MIPT p_c = 0.17(1).
* Bao, Choi, Altman, PRB 101, 104301 (2020): n = 2 Ising mapping; Eq. 65 ≡ paper's Eq. pc2
  (paper, line 523).
* Vasseur, Potter, You, Ludwig, PRB 100, 134203 (2019): q = n! Potts at large bond
  dimension.
* Zhu, Kueng, Grassl, Gross (2016) / Webb (2016): qubit Cliffords are unitary 3-designs
  (paper's rem:cliff3design); Gross, Nezami, Walter, CMP 385, 1325 (2021): Clifford 4-copy
  commutant (stochastic Lagrangian subspaces).
* Borgs, Imbrie, CMP 123, 305 (1989): Pirogov–Sinai with complex weights.
* Paper lines: 41 (abstract), 520–523 (p_c^{(2)}(d)), 701, 722–724 (n = 3, 4, 5 claims),
  839–891 (size-ladder test, rem:whyqn), 973–1030 (records), 1169–1200 (replica
  interpolation), 1321 (SMC), 1501–1600 (3-design identity, z3closure), 1719–1735
  (conclusion).
* This workspace: `adj-01-replica-potts-dispute.md` §1–§10; `v2.2/verify/replica/*.json`.

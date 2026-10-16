# The Opfibration Ontology: Quantum Instruments, Irreversibility, and the Epistemic Asymptote
### Revised manuscript (Rev. 2.8) — deterministic dimension bound and citation-scope clarification; Rev. 2.7 preserved

> **Version status.** Rev. 2.8 is a new version based on Rev. 2.7; it does not overwrite Rev. 2.7,
> Rev. 2.6, Rev. 2.5, Rev. 2.4 (`paper/REVISED_PAPER.md`), or the original PDF. Every Rev. 2.7
> result is retained, including Theorem C.28: **R1 is closed** for finitary `Instr_D` with infinite
> `E`, a countable counit, every nonzero `B`, and every `R`. This revision adds a deterministic
> extreme-boundary program-dimension lower bound (C.35) and clarifies the source status of the earlier
> manuscript cited for version history. The pairwise deterministic overlap SDP, finite extreme-family
> Gram-rank consequence (C.29), and fixed-instrument heralded exact-cost benchmarks (C.30–C.34) are
> unchanged. The `δ_n` audit delimits these results rather than making a novelty or priority claim. R8
> remains open in the narrowed form in §7.2: no general operational or approximate-cost law is inferred
> from `δ_n`. The qutrit-family check is a numerical check, not an SDP optimization or proof assistant.
> See `paper/REVISION_CHANGELOG_v2.8.md` for the change record.

---

## Abstract

We study environment decoration `F_E = (−⊗E)` on finite-dimensional quantum systems in the
category of finite-outcome instruments and its deterministic subcategory `Chan`. For every
`d_E ≥ 2` and every fixed target `B`, the presheaf `A ↦ Instr(A⊗E,B)` is not representable in the
literal finite-tuple model. The proof is a two-slice dimension test at `A=ℂ`: if a proposed counit
has `m` outcomes and `r=d_{R(B)}²`, the ordered `n`-outcome slices would require
`n r−1 = d_E²(n m d_B²−1)` at `n=1,2`. The combination `q(2)−2q(1)` equals `1` on the representing
side and `d_E²` on the process side, a contradiction. The same argument descends to the quotient that
identifies outcome relabellings only; its fixed-grade strata have the same semialgebraic dimensions.
A separate one-slice argument at `B=E` rules out a global right adjoint in `Chan`; the grade-preserving
reduction transfers that global conclusion to literal `Instr_lab` and its multiplicity-preserving
outcome-permutation quotient `Instr_perm`, but does not by itself prove non-representability for each
target `B`. The monoidal-closedness statement is made for the symmetric
monoidal outcome-permutation quotient, not for the labelled tuple presentation before quotienting.

The obstruction is trace-preserving normalisation, not irreversibility: the same functor has a right
adjoint in compact-closed `CPM`, and it has no left adjoint in either `Chan` or literal `Instr`. The
classical stochastic analogue follows from the same two-grade mismatch. We separate standalone
convex-geometric claims, category-level adjunction claims, and category-specific quotient arguments;
none is inferred from a surjective record-forgetting map. Exact full-channel recovery is governed by
the full-space Knill–Laflamme condition and may include several orthogonal isometric branches, not
just a single isometry. Prior-indexed inversion is stated for full-support pointed channels.
Appendix C.28 also closes R1 for the finitary dyadic `Instr_D` quotient with infinite-dimensional
`E` and a countable counit, for every nonzero `B` and every register `R`, including `B=ℂ` and
non-separable `R`. Separately, Appendix C.29 formalizes a family of pairwise exact deterministic
overlap invariants `τ(f,f')` by SDP and proves a finite-family Gram-rank lower bound when the targets
are extreme. Appendices C.30–C.34 establish exact heralded-cost profiles and bounds for selected finite qubit
families, including a non-extreme full-Choi-rank five-channel benchmark; C.35 records a separate
deterministic extreme-boundary dimension bound. These programming results are distinct from `δ_n`; no
single formula unifying exact deterministic, heralded, and approximate cost is claimed. R8 and the other limitations—including the intended measurable-quotient
identification, non-normal states, and formal verification—remain explicit in §7.2 and Appendix C.

**Keywords.** Categorical quantum mechanics, quantum instruments, monoidal closure, causal
categories, normalisation, Petz recovery, Bayesian inversion.

---

## 1. Introduction

Tensoring with an environment is the canonical operation by which a closed description is promoted to
an open one. This paper asks the precise categorical question: does `(−⊗E)` have a right adjoint?
A right adjoint would supply, for every object `B`, an object `R(B)` and a natural bijection
`Instr(A⊗E, B) ≅ Instr(A, R(B))` — the universal "conditional instrument", i.e. **process currying**
for open systems.

**Results.** (i) In the literal finite-tuple category, for every fixed `B` the presheaf
`A ↦ Instr(A⊗E,B)` is not representable (Theorem 4.3); the proof compares only the `n=1,2` slices
at `A=ℂ`. The result also holds in the outcome-permutation quotient by semialgebraic dimension
(Rem. 3.4). (ii) Separately, `Chan(E,E)` is not affinely isomorphic to any finite-dimensional state
space (Theorem 4.5), so `F_E` has no right adjoint on `Chan` (Theorem 4.8). Proposition 4.9 transfers
this *global* no-adjunction conclusion to literal `Instr` and its permutation quotient. It does not
supply a pointwise obstruction for every target; that stronger quantifier comes from Theorem 4.3.
(iii) For finite `E,B` with `d_E,d_B≥2`, `Chan(E,B)` is not affinely isomorphic to any normal state
space (Theorem C.2); the `B=ℂ` case is a point. (iv) `F_E` has no left adjoint in `Chan` or literal
`Instr`, and `Instr` has neither a terminal nor an initial object (Theorem 4.12, Prop. 4.13).
(v) For each fixed `n≥1`, the ordered tuple body `Instr_n(E,E)` is not affinely isomorphic to
`Instr_n(ℂ,G)` for any finite-dimensional `G` (Theorem 4.6); this is a standalone convex-body
statement, not quotient-category representability. (vi) The obstruction is normalisation, not
quantumness: the classical stochastic-instrument category has the corresponding two-grade
obstruction (Theorem 5.2). (vii) Appendix C.28 proves pointwise nonrepresentability for the finitary
dyadic `Instr_D` quotient at infinite-dimensional `E` with a countable counit, for every nonzero
`B` and arbitrary `R`, including `B=ℂ`; this is a category-specific proof, not a Prop. 4.9 grade
transfer. (viii) Proposition 5.9 records the fixed finite-`m` affine defect as an auxiliary
candidate-processor comparison; Lemma 4.1 still forces `m=1` for an exact counit in rigid graded
`Instr`. (ix) Appendix C.29 defines the pairwise overlap family `τ(f,f')` as an SDP and proves the
finite extreme-target Gram-rank bound, while explicitly distinguishing its nonconvex rank step from
the SDP. (x) Appendices C.30–C.34 give exact heralded profiles or bounds for the Pauli unitary family, a
three-channel extreme family, a depolarizing calibration family, all qubit channels at a Bell-branch
threshold, and a constructed five-channel
non-extreme full-Choi-rank family. The last has `C_F(p)=log₂3` for all `p>0`, proved by Choi
linear independence rather than pure-program extremality. (xi) Proposition C.35 gives the necessary
deterministic program-dimension bound `d_R≥d_E²(d_B−1)+1` for universal channel programming; it is
not a heralded bound or a sufficiency result.

**Relation to the earlier draft [1].** The earlier unpublished draft [1] stated the deterministic obstruction for `Chan` via
an equation `d_R² = d_E²(d_B²−1)+1` whose integer solvability was asserted. In fact the equation has
infinitely many solutions — the family `(d_B, d_E, d_R) = (k, 2k, 2k²−1)` for every `k ≥ 1` — so no
statement of the form "this equation has no solutions" can be correct. The correct statement is a
**quantifier** statement: the dimension count must hold simultaneously for all `B`, and instantiating
`B = E` yields `d_R² = d_E⁴ − d_E² + 1`, which lies strictly between the consecutive squares
`(d_E²−1)²` and `d_E⁴`. This is the square-gap input to Theorem 4.8 below. The companion suite [8]
records finite checks, but the dimension-general nonsquare claim is proved by the displayed symbolic
sandwich in Theorem 4.5, not by computation. Reference [1] denotes the earlier working manuscript
supplied with this project; no public manuscript DOI or repository identifier has been verified. The
Zenodo DOI `10.5281/zenodo.20860298` identifies the software supplement, not that manuscript (see [9]).

**Interpretation.** §6 separates currying from retrodiction. An adjunction counit would be forward
evaluation; its absence is not a theorem about individual-channel recovery. Exact recovery of an
entire channel is characterized instead by the full-space Knill–Laflamme condition (Prop. 6.1), which
allows flagged orthogonal isometric branches. A specific prior supports a different, contravariant
Petz/Bayesian transpose on full-support pointed channels (Prop. 6.2). Neither statement follows from
the no-adjunction theorem.

**Conventions.** The main text uses finite-dimensional, nonzero Hilbert spaces; `d_X=dim X≥1`.
Instruments are in the Schrödinger picture; `Chan` is the `1`-outcome slice. Choi matrices satisfy
`Tr_B J=I_A` for trace-preserving maps. The main text's dimension and grading arguments use linear
algebra and convex geometry; Appendix C additionally states its normal-CP, Stinespring, semialgebraic,
and measure-theoretic hypotheses explicitly.

---

## 2. The category of quantum instruments (repaired foundations)

**Definition 2.1 (instrument).** An `n`-outcome instrument `A → B`, written
`ℰ = (ℰ₁,…,ℰₙ)`, is an `n`-tuple of completely positive maps `B(H_A) → B(H_B)` with
`Σᵢ ℰᵢ` trace-preserving. Equivalently, its Choi matrix is a positive semidefinite operator
`J_ℰ = Σᵢ |i⟩⟨i| ⊗ J_i` on `C^n ⊗ (H_A ⊗ H_B)` with `Σᵢ Tr_B J_i = I_A`.
This manuscript restricts to finite labelled outcome sets. General-outcome operational instruments
are treated by Davies–Lewis [5], and Ozawa studies quantum measuring processes for continuous
observables [6]; those broader outcome models are outside the present category.

**Definition 2.2 (labelled `Instr`; outcome sets).** Objects: nonzero finite-dimensional Hilbert
spaces. Morphisms `A → B`: instruments, with a labelled outcome set `[n] = {1,…,n}` for some `n ≥ 1`.
We write `Instr_lab` when distinguishing this ordered-tuple category from its outcome-permutation
quotient. Composition of
`(ℰ_i)_{i∈[n]} : A → B` and `(ℱ_j)_{j∈[m]} : B → C` is the `nm`-outcome instrument with
component at the **lexicographic index** `(i−1)m + j`:

```
(ℱ ∘ ℰ)_{(i−1)m + j} = ℱ_j ∘ ℰ_i .
```

*This index convention is not cosmetic: the mixed-radix encoding makes composition strictly
associative and unital* — `((I×J)×K) → [nmk]` and `(I×(J×K)) → [nmk]` give the *same* order
(finite check in `verification/verify_claims.py`, section I; the Rev. 2.5 rerun is recorded in the
changelog). With this convention the original manuscript's Remark 2.1 can be deleted.

**Definition 2.3 (grading; `Chan`).** The hom-sets carry a grading `Instr(A,B) = ⊔_{n≥1} Instr_n(A,B)`
with `O(ℱ∘ℰ) = O(ℱ)·O(ℰ)` and `O(id_A) = 1`. The `1`-outcome slice is a wide subcategory, which we
call `Chan`: its morphisms are the CPTP maps.

**Definition 2.4 (tensor and unit).** `A ⊗ B` on objects; on labelled morphisms
`(ℰ_i)_{i∈[n]} ⊗ (ℱ_j)_{j∈[m]}` has components `ℰ_i ⊗ ℱ_j` indexed by `[n]×[m] ≅ [nm]`. The unit is
`ℂ`. The lexicographic outcome convention makes composition strictly associative. On labelled tuples,
the interchange law for tensor holds only after a permutation of the fourfold outcome index, so this
presentation is not itself a monoidal category on the nose. Let `Instr_perm` be the quotient by
permutations of outcome labels, retaining zero components and repeated components with their
multiplicity. Tensor and composition of multisets then satisfy interchange as multiset equality; with
the usual Hilbert-space associators, `Instr_perm` is symmetric monoidal. The endofunctor
`F_E=(−⊗E)` is well-defined already on `Instr_lab`, since tensoring with the one-outcome
`id_E` preserves the chosen grade and composition order, and it descends to `Instr_perm`.

In §4 the right-adjoint obstruction is first proved for `Instr_lab` and then extended to `Instr_perm`
(Rem. 3.4). Whenever “monoidal closed” is used, it refers to `Instr_perm`; no monoidal structure is
claimed for the labelled presentation before quotienting. In affine-dimension statements,
`Instr_n` denotes the labelled tuple body; its permutation quotient is assigned semialgebraic
codimension/dimension only, not an affine structure.

**Convention 2.5.** All objects have `d ≥ 1`; the zero-dimensional space is excluded (Prop. 3.1 would
return a negative dimension for it).

**Remark 2.6 (modelling choices, stated as such).** Outcome components may vanish and may repeat:
`{0, Φ}` and `{Φ/2, Φ/2}` are legitimate morphisms, and the grading counts them. This is a choice, and
it is exactly the choice that makes the counting argument of Lemma 4.1 work and that Def. 2.3 records.
Categories in which coincident components are identified, zero components are dropped, or outcomes are
merged (coarse-grained) are outside the scope of the rigid-grade arguments of §4 unless treated by a
separate category-specific proof in Appendix C. The fixed-outcome affine statement in Theorem 4.6
concerns the explicitly defined tuple convex bodies only; it is not a theorem about representability in
any of these quotient categories. Section 6 concerns `Chan` separately. See §7.2 and Appendix C for
the individual results and remaining gaps.

---

## 3. Affine geometry of the slices

**Proposition 3.1 (affine dimension).** For all `d_A, d_B ≥ 1` and `n ≥ 1`,

```
dim_aff Instr_n(A,B) = d_A² (n d_B² − 1).
```

*Proof.* Under Choi–Jamiołkowski, `Instr_n(A,B)` is the set of `n`-tuples `(J₁,…,Jₙ)` of PSD operators
on `H_A⊗H_B` with `Σᵢ Tr_B J_i = I_A`. The ambient real vector space `Herm(A⊗B)^n` has dimension
`n d_A² d_B²`. The map `(J_i) ↦ Σᵢ Tr_B J_i` is linear and surjective onto `Herm(A)` (dimension
`d_A²`): given `H ∈ Herm(A)`, the tuple with `J₁ = H ⊗ I_B/d_B` and `J_i = 0` otherwise maps to `H`.
Hence the fibre is an affine subspace of codimension `d_A²`. The tuple `J_i = I_A⊗I_B/(n d_B)` lies
in the fibre and is strictly positive (identity), so it is an interior point of the PSD cone, and the
feasible set has nonempty relative interior inside the affine subspace. Therefore intersecting with
the PSD cone changes nothing: `n d_A²d_B² − d_A² = d_A²(n d_B² − 1)`. ∎

*Finite checks:* the normalisation-map rank and strictly positive interior examples were checked for
`d_A,d_B ≤ 3`, `n ≤ 4`; these are numerical certificates only. The independent Rev. 2.5 rerun is
summarized in `paper/REVISION_CHANGELOG_v2.5.md`. The proof above is dimension-general. Note
`dim_aff Chan(A,B) = d_A²(d_B² − 1)` (the case `n = 1`).

**Lemma 3.2 (affine dimension lemma).** Let `C` be a nonempty convex subset of a finite-dimensional
real vector space and `L` affine and injective on `C`. Then `L|aff(C)` is injective and
`dim aff C = dim aff L(C)`.

*Proof (affine independence).* Let `x₀,…,x_r ∈ C` be affinely independent, `r = dim aff C`. If their
images were affinely dependent, there would be scalars `λ_i`, not all zero, with `Σ_i λ_i = 0` and
`Σ_i λ_i L(x_i) = 0`. Separating positive and negative coefficients and normalising expresses this as
`L(x̂) = L(x̂′)` for two convex combinations `x̂, x̂′ ∈ C` (convexity is used here); injectivity gives
`x̂ = x̂′`, hence `Σ_i λ_i x_i = 0`, contradicting affine independence. So `L` carries affinely
independent families to affinely independent families and `dim aff C ≤ dim aff L(C)`; applying the
same to the affine inverse on `L(C)` gives equality. ∎

*Alternative proof (relative interiors), used implicitly in §4.3.* In finite dimensions `ri(C) ≠ ∅`.
If a nonzero `v ∈ ker(dL) ∩ dir(aff C)` existed, then for `x ∈ ri(C)` one has `x ± εv ∈ C` for small
`ε > 0` and `L(x+εv) = L(x)`, contradicting injectivity; hence `L|_{aff C}` is injective. The
companion article [14] states the affine-independence form, and the strictly positive point of
Prop. 3.1 is exactly what supplies `ri ≠ ∅` in applications.

*Remark 3.3.* The hypothesis is not decorative: on the non-convex set `{(t,t²)}` the map `(x,y) ↦ x`
is injective while dimension drops from 2 to 1 (a finite counterexample check is recorded in the
Rev. 2.5 changelog). In applications below, convexity is automatic and `ri ≠ ∅` is supplied by
Prop. 3.1's strictly positive point.

**Remark 3.4 (the adjunction obstruction survives relabelling).** In `Instr_perm`, the fixed-grade
stratum is the finite semialgebraic quotient of the labelled tuple body by the permutation group
`S_n`. The quotient map has finite fibres, so its semialgebraic dimension equals the affine dimension
of the labelled body in Proposition 3.1. Under a hypothetical pointwise representation, the inverse
adjunction map `g ↦ ε_B∘(g⊗id_E)` is componentwise polynomial on Choi tuples and descends to a
semialgebraic bijection from grade `n` to grade `nm`; its inverse is semialgebraic as well. Hence the
two quotient strata have equal semialgebraic dimension. This proves that Theorem 4.3 applies to
`Instr_perm` without assigning an affine structure to an unordered stratum. Proposition 4.9 also
survives because outcome multiplicity remains a multiplicative grade. The fixed-`n` affine-body result
in Theorem 4.6 remains a theorem about labelled tuples only.

## 4. The obstruction

### 4.1 The counit and the slice correspondence

**Lemma 4.1 (deterministic counit, two proofs).** Either suppose `F_E` has a global right adjoint
`R` with counit `ε_B : R(B)⊗E → B`, or fix a target `B` for which the presheaf
`A ↦ Instr(A⊗E,B)` is naturally represented by an object `R(B)` with universal map `ε_B`.

1. *(Triangle identity, global case.)* For a global adjunction, the triangle identity
   `ε_{F(A)} ∘ F(η_A) = id_{F(A)}` gives `O(ε_{F(A)}) · O(η_A) = 1` in `(ℕ⁺,·)`, so
   `O(ε_B) = 1` for every `B ∈ im(F_E)`. In particular `O(ε_{A⊗E}) = 1` for all `A`, and
   `O(ε_E) = 1` since `E ≅ F_E(ℂ)`.
2. *(Counting, for each represented target.)* In either situation, naturality gives the inverse
   `Φ⁻¹(g) = ε_B ∘ F_E(g)`. If `g` has `n` outcomes, `Φ⁻¹(g)` has `O(ε_B)·n` outcomes; surjectivity
   of this bijection therefore makes `O(ε_B)` divide the outcome count of every process instrument
   `A⊗E → B`. A `1`-outcome process always exists (e.g. trace-and-prepare), so `O(ε_B)=1`.

The same grade argument applied to a putative left adjoint's unit shows that the unit is deterministic.

*Remark 4.2.* In the original draft this was the "prime argument". The primes are idle: what is used
is that `(ℕ⁺,·)` has no nontrivial units, and route 1 replaces the whole argument for the sharpest
statement by the triangle identity at `ℂ`.

### 4.2 The main theorem, per-`B` form

> **Theorem 4.3 (pointwise non-representability).** Let `d_E ≥ 2`. For every object `B` in the
> literal finite-tuple category `Instr_lab`, there is no object `R(B)` with a natural bijection
> `Instr_lab(A⊗E,B) ≅ Instr_lab(A,R(B))`. Equivalently `Hom(−⊗E,B)` is not representable, for every
> `B`. The proof also yields the same pointwise conclusion in `Instr_perm` by Rem. 3.4.

*Proof.* Fix `B` and suppose a pointwise representation exists, with object `R(B)` and counit of
outcome grade `m`. Naturality gives the inverse map
`Φ⁻¹(g)=ε_B∘(g⊗id_E)`, so a grade-`n` source instrument maps to grade `nm` on the process side.
Because `Φ⁻¹` is a bijection on the total hom-sets and grade is multiplicative, every process
instrument of grade `nm` has a preimage `g` satisfying `m O(g)=nm`, hence `O(g)=n`. Thus the
restriction is a bijection from grade `n` to grade `nm` without substituting `m=1`. At `A=ℂ`, this
restricted map is affine in the labelled model; in `Instr_perm` it is a semialgebraic bijection
(Rem. 3.4). Put `r=d_{R(B)}²`, `e=d_E²`, and `b=d_B²`. The dimensions of the two slices must
therefore agree:

```
q_R(n) = n r − 1,
q_E(n) = e(n m b − 1).
```

For `n=1,2`, equality would give

```
r − 1       = e(mb − 1),
2r − 1      = e(2mb − 1).
```

Subtract twice the first equation from the second. The representing side is `1`; the process side is
`e`. Thus `e=1`, contradicting `d_E≥2`. The counit is in fact forced to have `m=1` by Lemma 4.1,
but the two-slice contradiction does not rely on substituting that value. ∎

*Remark.* The per-target conclusion is Theorem 4.3's own dimension argument. The separate reduction
in Proposition 4.9 is a global implication between adjunctions and should not be used as a pointwise
proof for each `B`.

*Remark 4.3b (where `Φ⁻¹(g) = ε_B ∘ F_E(g)` comes from).* It is naturality of the adjunction
bijection in the *source* variable together with the triangle identity: `ε_B = Φ(id_{R(B)})`, and
unwinding the naturality square gives `Φ⁻¹(g) = ε_B ∘ (g ⊗ id_E)`. In the labelled model this
formula is linear on Choi tuples and supplies the affine structure used in Theorem 4.3 and the
fixed-grade result of Theorem 4.6; it is not an assumed affine property of a bare hom-set bijection.
The finite linearity checks are recorded in the Rev. 2.5 changelog. For `Instr_perm`, no affine
structure on unordered strata is assumed: Rem. 3.4 uses semialgebraic dimensions instead. A bare
bijection of hom-sets carries no affine information at all, and any two non-singleton convex sets are
in bijection.

*Remark 4.4 (the representing dimension is a function of `B` alone).* The same object `R(B)` must
serve every source and every grade. In fact, at `A=ℂ`, only the two grades `n=1,2` are needed: the
combination `q(2)−2q(1)` is `1` for a state-space/instrument slice represented by `R(B)`, but `e=d_E²`
for the process-side slices. Lemma 4.1 separately forces `m=1`, which is needed for the graded
reduction in Proposition 4.9, not for this algebraic contradiction. This is a discrete two-slice
argument, distinct from the standalone one-slice square gap (Theorem 4.5) and the fixed-`n`
convex-body result (Theorem 4.6).

### 4.3 The one-slice convex-body obstruction and the fixed-`n` companion

> **Theorem 4.5 (one-slice square gap).** Let `d_E ≥ 2`. For every finite-dimensional object `G`,
> the convex bodies `Chan(E,E)` and `States(G)` are not affinely isomorphic.

*Proof.* Their affine dimensions are `d_E²(d_E²−1)` and `d_G²−1`. Equality would force
`d_G²=d_E⁴−d_E²+1`. But for `d_E≥2`,

```
(d_E²−1)² = d_E⁴−2d_E²+1 < d_E⁴−d_E²+1 < d_E⁴,
```

so the candidate square lies strictly between consecutive squares. Contradiction. ∎

*Finite check (not the proof):* an exhaustive search confirms the nonsquare claim for
`2 ≤ d_E < 200000`; the displayed sandwich inequality is the dimension-general proof. The fresh
Rev. 2.5 check is recorded in the changelog. If infinite-dimensional `G` is allowed, its normal state
space has infinite affine dimension, also excluding an affine isomorphism.

> **Theorem 4.6 (fixed-outcome affine-slice obstruction, uniform in `n`).** Let `d_E ≥ 2` and
> `n ≥ 1`. In the labelled tuple model, for every finite-dimensional object `G`, the convex bodies
> `Instr_n^lab(E,E)` and `Instr_n^lab(ℂ,G)` are not affinely isomorphic. Consequently, no family of
> affine bijections between `Instr_n^lab(A⊗E,E)` and `Instr_n^lab(A,G)` can exist for all `A`.

*Proof.* Put `e=d_E²` and `g=d_G²`. Proposition 3.1 gives

`dim_aff Instr_n(E,E)=n e²−e`,  while  `dim_aff Instr_n(ℂ,G)=n g−1`.

Equality would force `g=e²−(e−1)/n`. Since `0<(e−1)/n≤e−1<2e−1`,

```
(e−1)² = e² − (2e−1)  <  e² − (e−1)/n  <  e² .
```

Thus `g` lies strictly between consecutive integer squares, impossible because `g=d_G²`. ∎

*Scope and significance.* Theorem 4.6 is a standalone statement about the explicitly defined
fixed-`n` tuple convex bodies. It assumes neither naturality nor an adjunction and uses no outcome
grading; it is not a categorical representability theorem for `Instr_0`, `Instr_cg`, `Instr_D`,
`Instr_Q`, `D^ω`, or other quotients. The affine-dimension formula uses the finite-dimensional tensor
identity `d_{A⊗E}=d_A d_E`; the contradiction is already witnessed at `A=ℂ`, where `ℂ⊗E≅E`, so a
uniform-in-`A` family would necessarily include this one-slice obstruction. Its `n=1` instance is
Theorem 4.5. This is a transparent specialization of the companion article's fixed-outcome
pointwise obstruction [14] to `B=E`, where its hypothesis `2 d_E d_B−1>(e−1)/n` is automatic; the
all-`n` form is not claimed as an independent new mechanism. The numerical check covers the stated
finite examples; the all-`n` conclusion follows from the symbolic sandwich.

> **Proposition 4.7 (exact labelled-slice dimension-match locus).** In the labelled tuple model,
> fix `d_E ≥ 2`, `n ≥ 1`, and an object `B`; put
> `e = d_E²`, `w = d_E d_B`, and `c = (e−1)/n`. There is a positive integer `d_G` for which
> `dim_aff Instr_n(A⊗E,B) = dim_aff Instr_n(A,G)` for every `A` if and only if
> **(i)** `n | (e−1)`, and **(ii)** `c = j(2w − j)` for an integer `j` with `1 ≤ j ≤ w − 1`.
> In that case `d_G = w − j`. Outside this locus no family of affine bijections can exist. On the
> locus, the equality is only a dimension match; no general affine isomorphism or `A`-natural family
> is asserted. The degenerate `B=ℂ, n=1` point-to-point case is identified separately below.

*Proof.* Put `g=d_G²`. By Proposition 3.1 and `d_{A⊗E}=d_A d_E`, equality of the dimensions for
all `A` is equivalent to `g=w²−c`. Since `g` is an integer, `c` must be an integer, i.e.
`n | (e−1)`. Since `c>0`, a positive square `g` must be strictly below `w²`; write
`g=(w−j)²` with an integer `1≤j≤w−1`. Then
`c=w²−(w−j)²=j(2w−j)`. Conversely, if (i) and (ii) hold, `d_G=w−j` is a positive integer and the
same equation gives equality of affine dimensions for every `A`. ∎

*Examples.* **(a)** `n = 1` with `j = 1`: condition (ii) reads `d_E² − 1 = 2 d_E d_B − 1`, i.e.
`d_B = d_E/2` (`d_E` even), giving `d_G = d_E²/2 − 1`; the resulting family
`(d_B, d_E, d_G) = (k, 2k, 2k²−1)` is the displayed Pell-type boundary family, and for `n = 1` these are exactly the `j = 1` escapes. This is the "accidental boundary family" highlighted in the companion's supplementary
check 6b [14]. That check also records the general outside-hypothesis form with `j ≥ 2`, so this
boundary family is not exhaustive; for example, `(d_E,d_B,n,j)=(15,2,1,4)` gives
`c=224=4(60−4)` and `d_G=26`. Proposition 4.7 packages the square-escape algebra as an iff dimension
criterion, with the divisibility and positive-dimension conditions explicit; it does not claim a new
escape family or a representability result. **(b)** `B = E`: then `w = e` and
(ii) would need `c ≤ e − 1 < 2e − 1 ≤ j(2e − j)`, impossible — this is Theorem 4.6 again. **(c)** For
`n=1`, `B = ℂ` (`w = d_E`): conditions (i)–(ii) hold with `j = d_E − 1` and `d_G = 1` for every
`d_E ≥ 2`. The count matches here and the bodies themselves are both single points (the normalised
trace), so the affine bijection exists trivially.
*Status.* Conditions (i)–(ii) characterize exactly when the affine-dimension count can be matched for
every `A`; in general they do not imply affine isomorphism or representability. The degenerate
`B=ℂ, n=1` case above is an explicit point-to-point exception. Whether a non-degenerate match admits
an `A`-natural family of affine bijections is a finer question that no dimension count can answer — see
residual R7 in §7.2.

### 4.4 The deterministic case and the direction of implication

> **Theorem 4.8 (Chan no-right-adjoint).** For `d_E > 1`, `F_E=(−⊗E)` on `Chan` has no right
> adjoint. *Proof.* A right adjoint would give, at `A=ℂ,B=E`, an affine bijection
> `Chan(E,E) ≅ Chan(ℂ,R(E))=States(R(E))`, because the inverse is counit composition and is linear on
> Choi matrices. This contradicts Theorem 4.5. ∎
> *(Pointwise strengthening: for every finite-dimensional `E,B` with `d_E,d_B≥2`, Theorem C.2 shows
> `Chan(E,B)` is not affinely isomorphic to **any** normal state space — the extreme-boundary
> dimension `2d_E²(d_B−1)` is larger than `2(R−1)` even when total affine dimensions agree. See C.2–C.3.)*

> **Proposition 4.9 (graded reduction, and its exact scope).** In either the literal category
> `Instr_lab` of Definition 2.2 or its outcome-permutation quotient `Instr_perm` (zero and repeated
> components retain their multiplicity), if `F_E` has a right adjoint then `(−⊗E)` has a right
> adjoint on `Chan`.

*Proof.* Let `R` be the right adjoint, `ε_B` its counit, and
`Φ_{A,B}: Instr(A⊗E,B) → Instr(A,R(B))` the adjunction bijection. Lemma 4.1(2) gives
`O(ε_B)=1` for every `B`; hence
`O(Φ_{A,B}^{−1}(g))=O(ε_B)O(g)=O(g)`. Thus `Φ^{-1}` preserves every grade, and because it is a
bijection its inverse does too. In particular it restricts to bijections
`Chan(A⊗E,B) ≅ Chan(A,R(B))`.

It remains to check the *functor* restriction, not just the hom-set bijections. For a channel
`h:B→B'`, naturality in `B`, applied to `A=R(B)` and `g=id_{R(B)}`, gives
`Φ^{-1}_{R(B),B'}(R(h)) = h∘ε_B`. The right side has grade one; grade preservation of `Φ^{-1}`
therefore forces `R(h)` to have grade one. So `R` restricts on objects and morphisms to a functor
`Chan→Chan`, and the restricted bijections are natural. ∎

*Scope check.* This proof uses the exact multiplicativity and nonzero unit of the grade, not merely a
forget-record functor. It transfers a *global adjunction* to `Chan`; it does not establish pointwise
non-representability for every target `B`. Indeed, for `B=ℂ`, both `Chan(A⊗E,ℂ)` and `Chan(A,ℂ)` are
singletons for every `A`, so that pointwise functor is represented by `ℂ`. In `Instr_0`, `Instr_cg`,
`Instr_D`, `Instr_Q`, and `D^ω`, zero dropping, proportional merging, or splitting destroys the rigid
grade. The total-map functor to
`Chan` is surjective but not injective there (e.g. a channel may have a nontrivial CP instrument
decomposition); its surjectivity alone does **not** restrict an adjunction to `Chan`. No such
implication is used for those categories: see the separate pointwise proofs in C.8, C.10–C.12 and
C.23.

*Remark 4.10.* In either `Instr_lab` or `Instr_perm`, a global Chan no-right-adjoint result implies a
global no-right-adjoint result by Prop. 4.9; this is the direction from deterministic to probabilistic.
Theorem 4.3 is separate and stronger in quantifier scope: it rules out representability at each fixed
`B` in the stated pointwise models. The extension of Prop. 4.9 to coarse quotients such as `Instr_0`
and `Instr_cg` would be invalid; those categories require their own proofs. `Instr_perm` is an allowed
special case because it preserves the multiplicative grade.

> **Corollary 4.11 (no right adjoint; monoidal scope).** If `d_E≥2`, `F_E` has no right adjoint in
> `Instr_lab` or `Instr_perm`. For `d_E=1`, it is naturally isomorphic to the identity and has a
> right adjoint. Since `Instr_perm` is symmetric monoidal, it is not right monoidal closed. This
> corollary does not transfer to `Instr_0`, `Instr_cg`, `Instr_D`, `Instr_Q`, or `D^ω` without their
> category-specific proofs.

### 4.5 No left adjoint; no terminal or initial object

> **Theorem 4.12.** For `d_E ≥ 2`, `F_E` has no left adjoint — in `Chan` and in `Instr`.
>
> *Proof.* (`Chan`) `ℂ` is terminal: the trace is the unique CPTP map `X → ℂ`. Right adjoints preserve
> terminal objects, but `F_E(ℂ) = E` is not terminal, since `Chan(E,E)` contains `id` and the
> depolarising map (two distinct morphisms). (`Instr`) Suppose `G ⊣ F_E` with unit `η`. The mirror of
> Lemma 4.1(2): reading the bijection as `Φ(g) = F_E(g) ∘ η_A`, every morphism `h : A → B⊗E` satisfies
> `O(h) = O(η_A)·O(Φ⁻¹(h))`, and `1`-outcome morphisms exist, so `O(η_A) = 1` for every `A` and the
> bijection respects slices. Take `A = B = ℂ`: then
> `Instr₁(G(ℂ), ℂ) ≅ Instr₁(ℂ, E)`. The left side is `Chan(G(ℂ), ℂ)`, a single point (affine dimension
> `0`); the right side is the state space of `E` (affine dimension `d_E² − 1`). Hence `0 = d_E² − 1`
> and `d_E = 1`. ∎

> **Proposition 4.13.** `Instr` has no terminal object and no initial object.
>
> *Proof.* If `T` were terminal then `Instr(ℂ,T)` would be a single point; but for any object `X` with
> `d_X ≥ 2` there are at least two distinct `1`-outcome instruments `ℂ → X` (two states), so `d_T = 1`
> and `T ≅ ℂ`. Yet `Instr(ℂ,ℂ)` contains the distinct instruments `{1}` and `{½,½}`, contradiction.
> Dually for an initial object. ∎

*Interpretation (the categorical arrow).* The asymmetry standardly associated with causal order is
"`ℂ` is terminal but not initial" — a property of `Chan`, where the discard effect is unique while
states are manifold. Prop. 4.13 shows this asymmetry does **not** survive in `Instr`: with graded
outcomes neither universal property holds. This is the honest categorical location of any "arrow"
(see §5.4); the original draft's "fibre-level arrow" has no anchor in `Instr`.

### 4.6 The causal opfibration, constructed (replacing the original Cor. 4.3 and Figure 1)

The original draft asserted that "the missing right adjoint is the missing cartesian lift". Here is the
construction that makes that sentence precise, together with its exact hypothesis.

**Definition 4.14 (causal opfibration).** Let `(P, ≤)` be a poset of *stage extensions* with least
element `⊥`, and let `u ↦ E_u` assign to each `u : X → Y` in `P` a nonzero finite-dimensional space,
coherently: `E_{⊥} = ℂ` and `E_{v∘u} ≅ E_u ⊗ E_v` for composable `u : X → Y`, `v : Y → Z`. (Example:
`P = (ℕ, ≤)` with `E_m = E^{⊗m}`.) Define `𝒞` by: objects `(X, H)` with `X ∈ P` and `H` a nonzero
finite-dimensional space; a morphism `(X,H) → (Y,K)` is a pair `(u, f)` with `u : X → Y` and `f : H⊗E_u → K`
an instrument; composition is `(v,g) ∘ (u,f) = (v∘u, g ∘ (f ⊗ id_{E_v}))` using the coherence
isomorphism; identities are `(id_X, id_H)`. The projection is `p(X,H) = X`.

> **Theorem 4.15.** (1) `p : 𝒞 → P` is an opfibration, and the cocartesian lift of `u : X → Y` at
> `(X,H)` is `(Y, H⊗E_u)` with the identity instrument. (2) Every fibre is `Instr`: `p⁻¹(X) ≅ Instr`
> for all `X` — literally the same category, since the only data in a fibre is a Hilbert space.
> (3) The reindexing functor is `u_! = (−⊗E_u)`. (4) Therefore (standard; Jacobs, *Categorical Logic
> and Type Theory*, Ch. 9) `p` is a **bifibration** iff every `u_!` has a right adjoint, i.e. **iff
> `E_u ≅ ℂ` for every `u`**; and the cartesian lift of `u` at `(Y,K)` is `(X, u_*(K))` with the missing
> `u_* : Instr → Instr` given by the non-existent internal hom `[E_u, −]`.

*Proof.* (1) Given `(u,f) : (X,H) → (Y,K)`, the morphism `(u,id_{H⊗E_u}) : (X,H) → (Y,H⊗E_u)` is a
lift of `u`, and every `(u,f)` factors as `(id_Y,f) ∘ (u,id_{H⊗E_u})`; uniqueness gives cocartesianity.
(2) A morphism over `id_X` is an instrument `H → K` (with `E_{id} = ℂ`), and vertical composition is
instrument composition. (3) is the defining formula. (4) The standard bifibration criterion plus
Thm 4.3/4.8, since `F_{E_u} = (−⊗E_u)` has a right adjoint iff `d_{E_u} = 1`. ∎

*Remark 4.16 (what the opfibration does and does not say).* (i) All fibres being `Instr`, the
opfibration is `P × Instr` twisted by the environment assignment; "fibre-level dynamics" is therefore
not additional structure, and the original figure's `Instr(A)`, `Instr(A⊗E)` annotations were
ill-typed (there is no fibre `Instr(A)`; a fibre is the whole category). (ii) The bifibration property
is a property of the *environment assignment* `u ↦ E_u`, not of the dynamics: a completely reversible
dynamics with trivial extensions is a bifibration, and a bifibration may contain irreversible
morphisms in its fibres. So the original Cor. 4.3's reading — that the missing cartesian lift is "the formal
signature of irreversibility" — is precisely inverted. (iii) The base direction is the *extension
relation* among stages, not a temporal order; the original "Past/Future" labels have no model here.
(iv) The honest content of the original Cor. 4.3, stated with all hypotheses, is: *if* a poset of stage extensions
is fixed, *then* the associated opfibration is a bifibration iff every extension is trivial
(`E_u ≅ ℂ`) — and by Thm 4.3/4.8 it is never a bifibration over a poset containing a nontrivial
extension. Figure: `figures/causal_opfibration.svg`.

---

## 5. What the obstruction is, and what it is not

### 5.1 It is the normalisation (causality), not irreversibility

**Proposition 5.1 (CPM comparison).** In `CPM(FHilb)` (all completely positive maps, Selinger [7]),
`−⊗E` has right adjoint `E*⊗−`; the compact-closed hom-set bijection is linear, and both ambient CP
hom-spaces have real dimension `d_A²d_E²d_B²`. It does not restrict to a bijection of the
trace-preserving slices. Those `Chan` slices have dimensions

```
Chan(A⊗E,B)          : d_A²d_E²d_B² − d_A²d_E² = d_A²d_E²(d_B² − 1)
Chan(A,E*⊗B)         : d_A²d_E²d_B² − d_A²     = d_A²(d_E²d_B² − 1)
right − left         : d_A²(d_E² − 1)            (= the "intercept")
```

Here trace preservation cuts codimension `d_A²d_E²` from the left ambient CP space and codimension
`d_A²` from the right. Example `(d_A,d_E,d_B) = (2,2,3)`: the two `Chan` dimensions are `128` and
`140`. So the obstruction is precisely the mismatch of causal-normalisation constraints, i.e. the
uniqueness of the discard/unit effect. Two consequences:

* adjointness is **not** a signature of irreversibility (`CPM` has the adjoint and contains the trace);
* a fortiori it cannot be a signature of *time direction* (see Prop. 5.5).

### 5.2 Non-quantum: the classical analogue

**Theorem 5.2 (classical instruments).** Let `Instr^cl` be finite-outcome classical instruments
(families of sub-stochastic matrices summing to a stochastic matrix). Then
`dim_aff Instr^cl_n(X,Y) = |X|(n|Y| − 1)`, and for `|E| ≥ 2` no object represents `Hom(−×E, B)`;
the obstruction is a two-grade normalisation mismatch, with no specifically quantum input.

*Proof.* Let `e=|E|`, `b=|B|`, `r=|R|`, and let the proposed counit have `m` outcomes. At `A=1`,
the inverse representation map sends grade `n` to grade `nm`. Since the whole map is bijective and
the grade is multiplicative, every process instrument of grade `nm` has a preimage of grade `n`;
thus these two strata are bijective without substituting `m=1`. Their affine dimensions are `nr−1`
on the representing side and `e(nmb−1)` on the process side. Equality at `n=1,2` would imply

`r−1=e(mb−1)` and `2r−1=e(2mb−1)`. Subtracting twice the first equation from the second gives
`1=e`, contrary to `|E|≥2`. Separately, the existence of a one-outcome stochastic map and total
surjectivity force `m=1` by the same grade-count argument as Lemma 4.1; the two-slice contradiction
does not depend on substituting it. ∎

**Proposition 5.3 (quantum vs classical threshold — why the grading engine is needed).** In the
quantum case, `n = 1` with `B = E` already suffices (Thm 4.5), because `d_E⁴−d_E²+1` must be a square.
Classically, `n = 1` is *satisfiable*: `|R| = |E||B| − |E| + 1`, e.g. `|E| = |B| = 2 ⇒ |R| = 3`. The
contradiction appears only when the `n = 1` and `n = 2` slices are compared. Hence the graded
intercept engine — the one genuinely load-bearing part of the original draft's machinery — is exactly
what transports the result to the classical (and hence non-quantum) setting. The dimension-general
conclusion is the symbolic two-grade argument in Theorem 5.2; finite examples in the regression suite
are only checks, with their Rev. 2.5 status recorded in the changelog.

### 5.3 Reversible and irreversible tests

**Proposition 5.4.** On the groupoid of Hilbert spaces and unitaries, `−⊗E` has no right adjoint as
soon as `d_E ∤ d_B` (the left hom-set is then empty, while `U(A,R(B)) ⊇ {id}` for all `A`). This is a
purely arithmetic failure in a category where every morphism is invertible.

**Proposition 5.5.** In `Chan`, `ℂ` is terminal but not initial (`Chan(ℂ,X)` = states of `X`, a convex
set of dimension `d_X²−1 ≥ 0`, with `≥ 2` elements for `d_X ≥ 2`). `Chan ≠ Chan^op`: this is the one
categorical asymmetry that survives the tests above, and it is a property of the *category*, not of
`F_E`. It is the Coecke–Lal causality axiom territory; the physical reading is "discarding is unique,
preparation is not".

### 5.4 The defect, quantified (and why the "best" object still fails)

> **Proposition 5.6 (defect).** In the rigidly graded instrument model, any adjunction counit has one
> outcome by Lemma 4.1. Let `d_E ≥ 2`, `e = d_E²`, `v = d_B²`, and let `r = d_R²` be any integer.
> Put `δ_n := e(nv − 1) − (n r − 1)`, the process-side affine dimension minus the representing-side
> dimension at grade `n`. Then
>
> 1. `δ_n = n(ev − r) + (1 − e)` is affine in `n` with constant term `−(e−1)`;
> 2. `δ_n ≡ 0` is impossible for `e ≥ 2` (slope and intercept cannot vanish together — this is
>    Thm 4.3 in other words);
> 3. `min_r max_{n≥1} |δ_n| = e − 1`, attained exactly at `r = ev`, i.e. at `d_R = d_E d_B`, where
>    `δ_n = −(e−1)` **for every `n`**;
> 4. if the `n = 1` count is matched (a Diophantine escape, `r = e(v−1)+1`), then
>    `δ_2 = e − 1`: escaping at `n = 1` costs exactly the intercept at `n = 2`.

*Proof.* (1) is expansion. (2) requires `ev = r` and `1 = e`. (3) If `r ≠ ev` then `|δ_n| → ∞`, so
only `r = ev` is admissible, where `δ_n = 1 − e` for all `n`. (4) Substitute `r = e(v−1)+1`:
`δ_2 = 2(ev − e(v−1) − 1) + 1 − e = 2(e−1) + 1 − e = e − 1`. ∎

The value `d_R = d_E d_B` in (3) is the compact-closed candidate `R(B)=E*⊗B` of Prop. 5.1, and
the number `d_E²−1` also appears as the codimension between a typed channel slice and its ambient
Choi state body. These are related affine-dimension calculations; the numerical match alone does not
establish a unified operational law. Item (4) quantifies only the displayed Pell boundary family
(`j=1`, `n=1` in Prop. 4.7): matching its `n=1` count fails at `n=2` by exactly `e−1`. The
companion's supplementary check 6b [14] records the general `j`-parameter square-escape form;
Prop. 4.7 writes an exact dimension-match criterion and includes `B=ℂ`. No claim is made that all
escapes lie on the Pell boundary. The relation of `δ_n` to general programming cost remains open as
R8; it is not a cost predictor, a Nielsen–Chuang theorem, or a unifying formula for exact, heralded,
and approximate costs.

> **Corollary 5.7 (no state-space or ensemble structure at `B = E`).** For `d_E ≥ 2` and every
> `n ≥ 1`, `Instr_n(E,E)` is not affinely isomorphic to any `n`-outcome ensemble space
> `Instr_n(ℂ, R)`; in particular `Chan(E,E)` is not affinely isomorphic to the state space of any
> system.

*Proof.* Setting affine dimensions equal (take `A = ℂ` in Thm 4.6, i.e. `d_A = 1`) gives
`n d_R² − 1 = d_E²(n d_E² − 1)`, that is

```
d_R² = d_E⁴ − (d_E² − 1)/n .
```

For every `n ≥ 1`, `0 < (d_E²−1)/n ≤ d_E² − 1 < 2d_E² − 1`, so `(d_E²−1)² < d_R² < d_E⁴`: the value
lies strictly between consecutive squares and is never a perfect square. Hence no `R` exists. ∎
This is Theorem 4.6 with `A = ℂ`; it is the precise form of the statement that *channel spaces are not
state spaces*.

*Remark 5.8 (the right fibred picture for outcome dependence).* The forgetful ("total map") functor
`Σ : Instr → Chan`, `Σ({ℰ_i}) = Σ_i ℰ_i`, is functorial, identity-preserving and commutes with
`−⊗E`; its fibres are the instruments refining a given channel, which is where outcome-set dependence
genuinely lives. (The original draft's "base causal poset" was the wrong base: the useful base for
outcome dependence is `Chan` under `Σ`.) The companion's multiset-quotient study [8, groups M and O]
records that the induced comparison on the multiset quotient is a natural split mono which fails to be
surjective and excludes one-outcome units, with the multi-outcome case classified open.

> **Proposition 5.9 (fixed finite outcome multiplier).** Let `d_E,d_B,d_R,m,n` be positive finite
> integers, and put `e=d_E²`, `v=d_B²`, `r=d_R²`. Define the auxiliary affine-dimension defect
> \[
> \Delta_n^{(m)}:=\dim_{\rm aff}\operatorname{Instr}_{nm}(E,B)
> -\dim_{\rm aff}\operatorname{Instr}_{n}(\mathbb C,R).
> \]
> Then
> \[
> \boxed{\Delta_n^{(m)}=n(mev-r)-(e-1).}
> \]
> In particular, `Δ₂⁽ᵐ⁾−2Δ₁⁽ᵐ⁾=e−1`; simultaneous equality of the two slice dimensions is impossible for `d_E≥2`. For fixed `m,r`, `sup_{n≥1}|Δ_n⁽ᵐ⁾|` is infinite unless `r=mev`, in which case it is constantly `e−1`. Minimizing over integer `m,d_R` gives the value `e−1`, attained exactly when `r=mev` (which requires `m` to be a square; `m=1,d_R=d_Ed_B` always attains it).
>
> *Proof.* Proposition 3.1 gives `dim Instr_{nm}(E,B)=e(nmv−1)` and `dim Instr_n(ℂ,R)=nr−1`. Subtraction yields the formula. If `r≠mev`, the affine term in `n` makes the absolute defect unbounded; if `r=mev`, the defect is `1−e` for every grade. Since `m=1` and `r=ev=(d_Ed_B)²` are allowed, the global integer minimum is `e−1`. ∎

**Scope of Proposition 5.9.** At `m=1` this is Proposition 5.6. For `m>1`, it is an auxiliary fixed-grade comparison for a candidate `m`-outcome processor; it does **not** say such a processor is unphysical. Lemma 4.1 forces `m=1` only for an exact adjunction counit in the rigid graded `Instr` category. A complete Bell-basis teleportation instrument with `m=d_E²` outcomes is a physical processor, but not a multi-outcome counit in that category. In the standard protocol, the `d_E²−1` nonidentity Bell outcomes are failures if only the identity-labelled branch is accepted. Their count matches the affine codimension `d_E²−1` of the typed channel slice, but this is a protocol-specific correspondence, not a general operational law. The single-slice inequality `Δ₁⁽ᵐ⁾≤0` is necessary for a surjective processor parameterization; it is not sufficient and does not predict optimal program cost. Exact processors for restricted covariant channel families do not conflict with an obstruction for the full channel set, since the target families differ.

### 5.5 Interpretation (labelled)

*What is proved:* `Hom(−⊗E, B)` is not representable in the stated finite-outcome models; the
would-be internal hom is not an object of the specified first-order quantum-system category.
*What follows (must be argued, not asserted):* `[E,B]` is a higher-order object — a convex set of
combs/supermaps (Chiribella–D'Ariano–Perinotti [13]; Kissinger–Uijlen [12]) — and closure is recovered in those
higher-order completions at the price of fixing a causal structure. Making this precise is Open
Problem 7.4; the closest external framework is the semicartesian monoidal structure of CPTP, whose unit
is terminal (discarding is unique — the Coecke–Lal causality axiom [15]). The monoidal non-closure statement
here refers to `Instr_perm`, the symmetric monoidal outcome-permutation quotient. External priority
for this precise statement has not been established; a full literature search remains to be done.
*What does not follow:* irreversibility of dynamics, an arrow of time, apparatus-dependence of
retrodiction, or non-existence of exact recovery. Proposition 6.1 is the separate full-space recovery
criterion; Sections 5.1–5.3 and §6 make no inference from it to adjoint existence.

*Relation to the cited companion manuscripts (not an external priority assessment).* The
affine-dimension lemma, no-left-adjoint statement, classical analogue and normalization/intercept
principle are also treated in the author's companion articles [8,14]. The companion submission gives
the fixed-outcome instrument dimension formula and pointwise obstruction; its supplementary check 6b
records the general square-escape factorization, not only the `d_B=d_E/2` boundary case. This paragraph
is a version-scope map: Theorem 4.6 states the `B=E` specialization, Proposition 4.7 gives the
affine-dimension matching criterion with divisibility and positivity, Theorem 4.5 isolates the
grade-free `Chan(E,E)` versus state-space consequence, and Theorem 4.3/Proposition 4.9 give the
literal-`Instr` per-`B` theorem and the distinct global grade-dependent reduction. Proposition 5.6
records the `m=1` instrument-slice defect already related to the normalization/intercept calculation
in [14]. This internal comparison does not adjudicate novelty or priority against the broader
literature; the source review is partial, and no external novelty or priority claim is made.

### 5.6 Exact programming costs: finite-family results and scope

For clarity, the heralded cost in Appendices C.30–C.34 uses one fixed instrument
`P_s,P_f:E⊗R→B`, with both maps CP and `P_s+P_f` trace-preserving, and target-dependent (possibly
mixed) program states `ρ_f` satisfying
\[
P_s(X\otimes\rho_f)=q_f f(X)\quad\text{for every input }X,\qquad q_f\ge p>0.
\]
The success probability is input-independent but may vary with `f`; the cost is the infimum of
`log₂ dim R`. This is an exact heralded model, not an approximate channel metric.

The overlap quantity is a **family** `τ(f,f')` indexed by channel pairs. For a deterministic processor,
Proposition C.29 gives its SDP and the finite extreme-target Gram-rank bound. That bound is not the
heralded cost, and the minimum-rank Gram problem is not itself an SDP. For non-extreme targets a mixed
program need not have a pure preimage, so the deterministic extreme-target argument cannot be reused
without a separate proof.

The exact finite-family profiles established here are:

| Target family | Exact result under the stated model |
|---|---|
| `{R_|0⟩, R_|+⟩, Ad_Z}` | `C_F(p)=log₂3` for every `0<p≤1`; C.30 supplies a heralded-specific Choi-support/Kraus-rank proof. |
| Four Pauli unitary channels `{Ad_I,Ad_X,Ad_Y,Ad_Z}` | `C_F(p)=2` bits for every `0<p≤1`; C.31 uses rank-one Choi rays and linear independence of programs. |
| Two distinct qubit depolarizing channels | `C_F(p)=1` bit for every `0<p≤1`; C.32 also gives their closed-form `τ`. The full depolarizing segment is programmable with a qubit. |
| The constructed five full-Choi-rank non-extreme channels of C.33 | `C_F(p)=log₂3` for every `0<p≤1`, by a dimension-square rank bound and an explicit qutrit POVM processor. |
| All qubit channels `Chan(2,2)` | Choi/Bell programming gives `C_F(p)≤2` bits for `0<p≤1/4`; `C_F(1)=∞`. No optimum is claimed for `1/4<p<1`, nor is the four-dimensional construction claimed minimal at `p=1/4`. |

**Separate deterministic dimension bound.** If one finite-dimensional deterministic processor programs every channel `E→B`, with `d_E,d_B≥2`, Proposition C.35 gives the necessary bound `d_R≥d_E²(d_B−1)+1`. For qubit-to-qubit channels this says `d_R≥5`, but the exact-unitary no-go already gives the stronger `C_F(1)=∞`. This bound is only for deterministic exact programming; it supplies no lower bound for heralded thresholds `0<p<1` and is not a sufficiency or cost-prediction theorem.

The `d_E²−1` nonidentity Bell outcomes are failures only for the protocol that accepts the identity-labelled branch and rejects the rest; restricted covariant families may correct and accept other outcomes. Existence of exact processors for such a restricted family does not contradict a no-go for all of `Chan(E,B)`. The appearance of `d_E²−1` as a slice codimension and as this protocol's rejected-outcome count is not a universal cost law. A single formula unifying deterministic exact, heralded exact, and approximate costs remains conjectural.

An asymptotic unitary-gate cost formula `[(d²−1)/2]log₂(1/ε)` qubits is attributed in the working notes to Yang–Renner–Chiribella, together with a Heisenberg-limit metrology argument relating programming, learning, and estimating unitaries. Its source and mechanism have not been independently verified for this revision, so it is not stated as a theorem here and is not extended to general channels. A low-depth brickwork-circuit worst-case claim of order `Θ(N polylog N)` and a quantitative KPP formula are likewise not used pending source/version verification. Structure-sensitive costs may be important, but no such external claim is relied on in this manuscript.

---

## 6. Retrodiction, done properly

### 6.1 The right adjoint is currying, not retrodiction

A right adjoint would give `Instr(A⊗E,B) ≅ Instr(A,[E,B])`: an object representing "B conditioned on
E". Its counit `ε_B : [E,B]⊗E → B` is **evaluation** and points *forward* (into `B`); it cannot be a
map "from a measured outcome on `B` back to a history". The original draft's identification of the
missing adjoint with retrodiction (and with Petz/Bayesian/process-matrix methods) is unsupported;
[4] in particular is about indefinite causal order, not retrodiction. Nor is the theorem a statement
about invertibility of individual channels: unitary channels are invertible *inside* `Instr`
(`U ⊗ id_E` has the one-outcome instrument `U† ⊗ id_E` as an inverse). A prior-dependent Petz
transpose [2] is a candidate Bayesian inverse for a pointed channel; it does not generally recover every
input state, and its scope requires support hypotheses. The missing object is the internal hom, and
nothing else.

### 6.2 Exact retrodiction is a left-inverse theorem

**Proposition 6.1 (full-space Knill–Laflamme criterion; cf. [10]).** Let `N:A→B` be a finite-dimensional
CPTP map with Kraus operators `{K_i}`. There is a CPTP map `R:B→A` satisfying `R∘N=id_A` if and
only if there is a positive semidefinite matrix `C=(c_{ij})` such that

`K_i†K_j = c_{ij} I_A` for all `i,j`.

Equivalently, after a unitary change of Kraus family,
`N(ρ)=Σ_s p_s V_sρV_s†`, where `p_s>0`, `Σ_s p_s=1`, each `V_s:A→B` is an isometry, and the ranges
of the `V_s` are pairwise orthogonal. A single isometry channel is the rank-one special case, not the
general answer.

*Proof.* *(Necessity.)* Let `{L_a}` be Kraus operators for `R`. Then `{L_aK_i}_{a,i}` is a Kraus
family for the identity channel. Its Choi operator has rank one, so every `L_aK_i` is a scalar
multiple `α_{ai}I_A`. Using `Σ_a L_a†L_a=I_B`,

`K_i†K_j = Σ_a K_i†L_a†L_aK_j = (Σ_a ar α_{ai}α_{aj}) I_A`.

The coefficient matrix is a Gram matrix and is positive semidefinite.

*(Sufficiency.)* A unitary rotation of the Kraus family diagonalizes `C`. Thus one may assume
`K_s†K_t=p_sδ_{st}I_A`; trace preservation gives `Σ_s p_s=1`, and the nonzero `V_s=K_s/√p_s`
are isometries with orthogonal ranges. Put `P=Σ_s V_sV_s†`, a projection, and choose any state
`τ_A`. Define

`R(X)=Σ_s V_s†XV_s + tr((I_B−P)X)τ_A`.

This map is CP and trace-preserving. Since `N(ρ)` is supported on `P`,
`R(N(ρ))=Σ_s p_sρ=ρ`. ∎

*Counterexample to the single-isometry-only claim.* Let `B=A⊕A`, let `V_0,V_1` be the two canonical
orthogonal embeddings, and let `0<p<1`. Then

`N(ρ)=pV_0ρV_0†+(1−p)V_1ρV_1†`

has the CPTP left inverse `R(X)=V_0†XV_0+V_1†XV_1`, but it maps every pure input to a rank-two output
and is not a single isometry channel. This is why full-space exact recoverability must be stated by
the Knill–Laflamme condition rather than by isometry alone.

*Corollary.* Irreversibility is graded and quantitative, not a yes/no categorical property: the right
measures are Petz recovery fidelity, approximate-recovery bounds, and the entropy-production
quantity `D(ρ‖σ) − D(Nρ‖Nσ)`. The paper's claim that a missing adjoint is "the formal signature of
open-system irreversibility in all its forms" is replaced by: *the missing adjoint is the failure of
the internal hom to be a system; irreversibility is measured by recoverability.*

### 6.3 Prior-indexed retrodiction is functorial

**Proposition 6.2 (Petz transpose on full-support pointed channels).** Let `A,B` be finite
dimensional and let `σ>0` be a density operator on `A`. For a channel `N:A→B`, put `τ=N(σ)` and
assume `τ>0`. Define

`N^♯_σ(X) = σ^(1/2) N^*(τ^(−1/2) X τ^(−1/2)) σ^(1/2)`,

where `N^*` is the trace adjoint. Then `N^♯_σ:B→A` is CPTP and `N^♯_σ(τ)=σ`. If
`M:B→C`, `υ=M(τ)>0`, and all three priors are full rank, then

`(M∘N)^♯_σ = N^♯_σ ∘ M^♯_τ`.

Thus this construction is a contravariant functor on the category of full-support pointed finite-
dimensional channels `(A,σ)→(B,Nσ)`. For non-faithful priors, support restrictions and extensions
must be specified; no such generalization is claimed here.

*Proof.* Complete positivity follows from composition of CP maps and positive conjugations. Since
`N^*(I_B)=I_A`,
`N^♯_σ(τ)=σ`. For any positive `X`,

`tr N^♯_σ(X)=tr(τ τ^(−1/2)Xτ^(−1/2))=tr X`,

so it is trace-preserving. For composable `N,M`, substitute the definitions and cancel the adjacent
`τ^(−1/2)τ^(1/2)` factors:

`N^♯_σ(M^♯_τ(X)) = σ^(1/2)N^*M^*(υ^(−1/2)Xυ^(−1/2))σ^(1/2) = (M∘N)^♯_σ(X)`.

This proves the contravariant composition law. ∎

*Context.* Prior-indexed Bayesian inversion is a distinct structure from the right adjoint to
`−⊗E`; the Petz and classical/quantum Bayesian treatments [2,3,11] motivate this viewpoint. The
proposition above states and proves only the full-support finite-dimensional Petz-transpose case.

### 6.4 The defensible one-sentence reading

> Channel spaces are not state spaces, and `[E,B]` is a comb-type convex object, not a system; this is
> why currying an environment into a system cannot be represented internally — and it holds for
> classical, quantum, reversible and irreversible dynamics alike.

---

## 7. Scope, limits, and open problems (replacing the "epistemic asymptote")

### 7.1 Hypotheses actually used, and counter-models where they are dropped

| Hypothesis | Used where | Dropped ⇒ |
|---|---|---|
| finite dimension, `d ≥ 1` | Prop. 3.1, all finite-dimensional counts | infinite-dimensional cases require separate dimension and topology arguments; the finite-dimensional comparison does not apply |
| finite outcome sets + multiplicative grade retaining multiplicity | Thm 4.3 (per-`B`), Prop. 4.9, Thm 5.2 | infinite outcome cardinalities can absorb finite products (`|I×M|=|I|`); grade divisibility no longer gives the same obstruction |
| trace-preserving normalisation | everywhere | `CPM`: the right adjoint exists (Prop. 5.1) |
| labelled tuples, or only-permutation quotients retaining zero/repeated multiplicity | Thm 4.3 and Prop. 4.9; Rem. 3.4 handles `Instr_perm` semialgebraically | zero-dropping, merging, or other quotients require category-specific arguments; see §7.2 and Appendix C |
| nonzero objects | Prop. 3.1 and the stated system category | `d = 0` creates degenerate hom-sets (for example, no TP map from a nonzero input to a zero output); the stated affine-dimension argument does not cover it |

### 7.2 Open problems and adjudication status

The claims are handled in this order: **complete** a source proof only after checking it against the
actual definitions; **close** a named case with a category-specific proof; where the full source scope
is not established, **replace with a companion result** carrying an explicit limitation; then **drop**
unsupported or redundant inferences without erasing any still-open case. The detailed source ledger is
`audits/05_OPEN_PROBLEMS_SOURCE_EVAL.md`.

1. **Complete — standalone structural channel results.** C.20 supplies the semialgebraic extreme-set
dimension proof for finite-dimensional `Instr_cg` and its finite-counit consequence; the corrected
argument includes `B=ℂ`. C.21 proves the isometric-channel face invariant for finite `E` and
`dim B≥d_E`: the generated face has dimension `1` for `d_E≥3` and `2` for `d_E=2`. Separately,
C.22 proves a two-dimensional face for every *finite* `d_E,d_B≥2`, including `d_B<d_E`. C.22 is a
block-Kraus structural result, not an extension of the isometric invariant to `d_B<d_E`; neither face
claim by itself settles infinite-dimensional `E`.

2. **Close — pointwise results by category, not by a quotient of Prop. 4.9.** For `Instr_cg`, C.8
closes all `d_E≥2`, arbitrary nonzero `B,R`, and finite or countably supported outcomes. For literal
no-merging `Instr_0`, C.10 gives its own atomic-factorization proof for all Hilbert dimensions and
multiplicities. For the infinite-merge dyadic `D^ω`, C.11 uses its stated orbit-weight model. For
finitary dyadic `Instr_D` and finite-outcome rational `Instr_Q`, C.12 handles arbitrary `E,B,R` when
the counit is finite; C.23 treats finite-dimensional `E` with a countable counit, and C.28 treats
infinite-dimensional `E` with a countable counit, for arbitrary `R` and nonzero `B`. These are
separate category-specific proofs with their own outcome/equivalence hypotheses. In particular,
`Instr_Q` is not silently extended to countably many rational merges; that orbit quotient is not
defined by the finite rule.

3. **Close — deterministic `Chan`; strict graded `Instr` reduction is separate.** For finite
`d_E,d_B≥2`, C.2 rules out affine isomorphism of `Chan(E,B)` to any normal state space; C.3 gives
the stated finite-dimensional direct-sum extension. At `B=ℂ`, `Chan(E,ℂ)` is a point and is
representable by the trivial object. Proposition 4.9 transfers deterministic non-closure globally
to literal `Instr_lab` and to `Instr_perm`, since both retain multiplicative outcome grade. It does
**not** transfer a `Chan` theorem to `Instr_0`, `Instr_cg`, `Instr_D`, `Instr_Q`, `D^ω`, or other
quotients. The preceding item closes those only through their independent, category-specific proofs.
The Pell family is a dimension-count escape, not a representability result.

4. **Close under a register hypothesis — normal no-programming.** C.5 shows that in any normal
instrument model with a well-defined total-map functor, a separable program register cannot represent
`E→B` when `dim E,dim B≥2`, including infinite-dimensional `E` or `B`. It does not exclude a
non-separable register. C.26 constructs a non-separable surjective lookup-table processor and proves
it is non-injective; this is a limitation on the processor route, not a representation or no-go result.

5. **Close constructively, with a typed limitation — higher-order completion.** C.15–C.19 prove the
affine-slice typed category and its weighted-Choi right adjoint for every finite-dimensional typed
input `𝔈`. The Bell counit is CP and trace-preserving **only on its admissible slice**; C.19 states
the generic off-slice trace defect. C.24 proves closedness, flatness and tensor agreement for the
balanced subcategory of `Caus[CPM(FHilb)]`. Flatness excludes unbalanced slices, so no equivalence or
maximality claim for all of `𝒯` is made.

6. **Replace with a companion — measurable outcomes.** C.25 constructs an explicit finite-dimensional
ray-measure category for standard-Borel outcomes and proves its own quadrilateral no-go. It does not
identify every intended quotient of labelled measurable instruments with that model, and it does not
cover non-finite-dimensional objects. That definitional/equivalence question remains open.

7. **Residual ledger — R1 closed; R2–R8 retained.** (R1) Finitary `Instr_D` with infinite-dimensional
`E`, a countable counit, and arbitrary `R` is closed by C.28, for `dim B≥2` and `B=ℂ`; the proof
also covers separable `R`. C.12 covers finite counits and C.23 finite `E`. The analogous countably
supported rational-merge category is not defined by the finite quotient rule. (R2) The intended
measurable labelled-outcome quotient versus C.25's ray-measure model remains open. (R3) Non-normal
C*-algebraic states remain outside the definitions. (R4) The source's infinite-dimensional extension
of the block-face theorem, and its non-separable graded-`Instr` partition proof, are not established
here; C.21/C.22 are finite-input results, while C.5 requires a separable register. (R5) Maximality and
full `𝒯`/`Caus` equivalence beyond the balanced subcategory remain open. (R6) Formal proof-assistant
verification of the analytic and category-level arguments remains future work. (R7) For the
non-degenerate dimension-match locus in Proposition 4.7, whether the fixed-grade bodies admit
`A`-natural affine bijections, and whether any such family can be assembled into a representation,
remain open; dimension equality alone does not answer these questions. (R8) Remains open in the
narrowed form: does `δ_n` yield a family-general operational no-programming principle beyond affine
dimension comparison, and what regularity, metric, or structure assumptions would support an
approximate-cost conclusion? Proposition 5.9 and C.29–C.35 do not settle this question. R1 is closed
by C.28; R8 is not closed.

8. **Finite programming results — closed only for the displayed families.** C.29 proves the
pairwise deterministic `τ`-SDP and the finite extreme-family Gram-rank lower bound; C.30–C.34 prove
exact heralded profiles for the specific finite families listed in §5.6; C.35 adds a necessary
deterministic dimension bound from the dimension of the extreme-channel set. These results do not
imply a general cost formula, do not turn `δ_n` into an operational invariant, and do not unify exact,
heralded, and approximate programming.

9. **Drop — unsupported inferences, not open cases.** The source's unproved generic large-stratum
arguments are not used where C.10/C.12 provide explicit category-specific proofs; its blanket
extension of the isometric face invariant to arbitrary `d_B<d_E` is not adopted; the claim that a
surjective total-map functor alone restricts quotient-category adjunctions to `Chan` is rejected; and
any countable rational-merge extension without an explicit orbit definition is withheld. The named
ledger remains visible: R1 is closed by C.28; R2–R8 remain open.

### 7.3 What this section replaces

The original §6 promised to "formalize" an "epistemic asymptote" without definitions, admitted that
the claim could not be proved, and was then contradicted by §7's "the deductive content is now fully
extracted". The results now listed in §7.2 include the subsequent finite programming addendum, but
those examples do not close R8 or supply a general operational law. The taxonomy of "repetition /
semantic extrapolation / syntactic interpolation" is retained only as an editorial reminder —
applied to this text, it forbids the original §§5–6 as written.

---

## 8. Conclusion

For `d_E≥2`, the pointwise presheaf `Hom(−⊗E,B)` is nonrepresentable for every fixed `B` in the
literal finite-tuple instrument category; the same two-slice argument descends to the outcome-
permutation quotient. Separately, a one-slice square gap at `B=E` rules out a global right adjoint in
`Chan`, and the grade-preserving reduction transfers only that global conclusion to `Instr_lab` and
`Instr_perm`. The monoidal-closedness statement refers to the symmetric monoidal permutation quotient. The mechanism is
the mismatch in trace-preserving normalisation, not an arrow of time, irreversibility, or quantumness.
The missing representing object would be a curried process, not a retrodiction apparatus. Exact
full-channel recovery is governed by the full-space Knill–Laflamme condition, which includes flagged
mixtures of orthogonal isometries; prior-indexed Petz inversion is a separate contravariant structure
on full-support pointed channels. Appendix C.28 separately closes R1 for countable-counit finitary
`Instr_D` at infinite-dimensional `E`, without using the graded reduction. The added finite-family
programming results use a pairwise deterministic overlap SDP, extreme-target Gram bounds, and separate
heralded lower-bound mechanisms; they do not identify `δ_n` with program cost. R8 remains open, and no
single law for exact, heralded, and approximate costs is asserted. The claims are deliberately limited
to the stated models and hypotheses.

---

## References (corrected)

1. A. Abaee, *The Opfibration Ontology: Separating Causal Order from Quantum Irreversibility*,
   earlier unpublished working manuscript (2026; project source copy; no public manuscript DOI or
   repository identifier verified). This entry identifies the historical draft discussed in the
   Introduction; its claims are re-evaluated in the present manuscript. The DOI formerly attached to
   this title (`10.5281/zenodo.20860298`) identifies the separate software record *"MIKEAA2020/opfibration-supplement:
   Initial supplementary simulation"* (Zenodo record 20860299, 2026-06-25, MIT), not the manuscript.
   For the software deposit, see [9].
2. D. Petz, *Sufficiency of channels over von Neumann algebras*, Quart. J. Math. Oxford **39**, 97
   (1988).
3. B. Coecke and R. W. Spekkens, *Picturing classical and quantum Bayesian inference*, Synthese
   **186**(3), 651–696 (2012). DOI 10.1007/s11229-011-9917-5. *(Corrects "194, 3185 (2017)".)*
4. O. Oreshkov, F. Costa, C. Brukner, *Quantum correlations with no causal order*, Nature Commun.
   **3**, 1092 (2012). *(Process matrices / indefinite causal order — not retrodiction.)*
5. E. B. Davies, J. T. Lewis, *An operational approach to quantum probability*, Commun. Math. Phys.
   **17**, 239 (1970). *(Cite at Def. 2.1 and in §5.2.)*
6. M. Ozawa, *Quantum measuring processes of continuous observables*, J. Math. Phys. **25**, 79
   (1984). *(Cite at Def. 2.1: continuous outcomes are outside the finite-outcome scope.)*
7. P. Selinger, *Dagger compact closed categories and completely positive maps*, Electron. Notes
   Theor. Comput. Sci. **170**, 139 (2007). *(Decisive for Prop. 5.1.)*
8. A. Abaee, *No Universal Process Currying: The Intercept Principle, Environmental Currying, and
   Finite-Dimensional Obstructions to Exact Process Storage, Evaluation, and Recovery*, companion
   manuscript with verification suite `verify_abaee_currying.py` (73 checks), repository
   `github.com/MIKEAA2020/opfibration-merged-`. *(Contains, independently: the square-gap
   `e⁴−e²+1`, the intercept engine, the FinStoch vertex mismatch, and the multiset-quotient partial
   results.)*
9. MIKEAA2020, *opfibration-supplement: Initial supplementary simulation*, software, Zenodo record
   20860299, DOI `10.5281/zenodo.20860298` (2026-06-25), MIT; source repository
   `github.com/MIKEAA2020/opfibration-supplement/tree/v1.0`.
10. E. Knill, R. Laflamme, *Theory of quantum error-correcting codes*, Phys. Rev. A **55**, 900 (1997).
   *(Exact-recovery characterisation of Prop. 6.1.)*
11. K. Cho and B. Jacobs, *Disintegration and Bayesian inversion via string diagrams*,
    Math. Structures Comput. Sci. **29**(7), 938–971 (2019), DOI 10.1017/S0960129518000488;
    M. S. Leifer and R. W. Spekkens, *Towards a formulation of quantum theory as a causally neutral
    theory of Bayesian inference*, Phys. Rev. A **88**, 052130 (2013), DOI 10.1103/PhysRevA.88.052130;
    A. J. Parzygnat and B. P. Russo, *A non-commutative Bayes’ theorem*, Linear Algebra Appl. **644**,
    28–94 (2022), DOI 10.1016/j.laa.2022.02.030. *(Context for prior-dependent inversion; Prop. 6.2
    proves the full-support Petz-transpose statement used here.)*
12. B. Coecke and R. Lal, *Categorical quantum mechanics* (Handbook of Quantum Logic, 2012);
    A. Kissinger and S. Uijlen, *A categorical semantics for causal structure*, Logical Methods in
    Computer Science **15**(3), 15:1–15:48 (2019), arXiv:1701.04732.
    *(Causality axioms; §5.4, Prop. 5.5, and C.24.)*
13. G. Chiribella, G. M. D'Ariano, P. Perinotti, *Quantum circuit architecture*, PRL **101**, 060401
    (2008). *(Combs; §5.4.)*
14. A. Abaee, *Quantum Combs, Higher-Order Processes, and the Normalization-Defect (Intercept)
    Principle*, with numerical supplement `verification_checks.py` (checks 1a–6b), repository
    `github.com/MIKEAA2020/Quantum-combs`. *(Contains, independently: the affine-dimension lemma
    under affine bijection, no-right- and no-left-adjoint theorems for environment decoration, the
    classical `FinStoch` proposition (dimension + vertex count), the "parallel tensor is not closed"
    corollary, the pointwise obstruction at fixed outcome number and the general outside-hypothesis
    square-escape factorization in supplementary check 6b, and the e²−e+1 sandwich.)*
15. M. Huot, S. Staton, *Universal properties in quantum theory*, QPL 2018; B. Coecke, R. Lal,
    *Categorical quantum mechanics* (Handbook of Quantum Logic, 2012). *(CPTP is semicartesian
    monoidal with terminal unit — the causal/discard asymmetry used in §5.5.)*
16. *Working note on the four open problems of §7.2* (unpublished; supplied with this revision as
    `uploads/sonnet time open problems.txt`, machine-generated and human-edited). Its results are
    adjudicated in `audits/05_OPEN_PROBLEMS_SOURCE_EVAL.md` and re-proved, with the hypotheses and the
    residual gaps made explicit, in Appendix C of this revision; nothing is cited from it as authority.
    Related literature used there: W. Arveson, *Subalgebras of C\*-algebras*, Acta Math. **123**, 141
    (1969) (extremality criterion, recorded as unchecked here); M. A. Nielsen, I. L. Chuang, *Programmable
    quantum gates*, Phys. Rev. Lett. **79**, 321 (1997) (no-programming, the model for Theorem C.5);
    A. Kissinger and S. Uijlen, *A categorical semantics for causal structure* (2019; arXiv:1701.04732;
    Caus[CPM], Definition 4.2 and §C.24).

---

## Appendix A — Computational certificates

The unchanged regression suite `verification/verify_claims.py` was independently rerun on
2026-10-05. Its 197-check console transcript, source hash, environment, and exit status are recorded in
`paper/REVISION_CHANGELOG_v2.5.md`; the pre-existing `verification/verification_log.txt` remains the
Rev. 2.4 transcript and was not overwritten. The suite is a finite regression battery, not a parser or
formal proof of this manuscript. Separate Rev. 2.5 spot checks cover the corrected quantum and
classical two-slice intercepts with symbolic `m,b`, the CPM dimension example, a non-isometric exactly
recoverable channel, and full-support Petz composition; their commands/results are summarized in the
changelog. These are finite exact-arithmetic or numerical certificates for stated instances, not
formal verification of analytic or category-level arguments. Main-text checks include the
instrument-slice ranks, affine-dimension and square-gap calculations, finite escape searches, classical
threshold contrast, CPM bookkeeping, and outcome-index strictification.

Appendix C's section **L** checks include: L1's exact quadrilateral and decompositions; L2/L18's literal
`Instr_0` multiset identity; L3/L4's Kraus strata, overlap, and block-family examples; L14/L17/L24's
typed-Choi and Bell-slice identities; L15's independent-marginal criterion; L16/L25's `D^ω` orbit
arithmetic; L20's finite-stratum witnesses and square-gap instances; L21's exact isometric-face ranks;
L22's exact block-channel face ranks for `d_E=2,…,7` and `d_B∈{2,3,5}`; L23's finite scalar overlap
identity used in C.23; L26's controlled lookup processor; and L27's explicit distinction between the
fixed-grade convex slice and `Instr_0` recorded-union mixing. The full prior suite output is reproduced
in the Rev. 2.5 changelog, alongside its limits.

For Rev. 2.8, the unchanged `verification/verify_claims.py` was rerun on 2026-10-08: 197 checks
passed, 0 failed. This regression suite predates C.29–C.35 and does not test their new analytic
proofs, including Proposition C.35. Its Section J also retains a legacy, non-assertive note that
references [5] and [6] were uncited in an earlier snapshot; Rev. 2.8 now cites them at Definition 2.1.
The script has no citation parser, so that printed note is not a current citation check. The separate
`verification/verify_nonextreme_qutrit_family.py`
was also rerun during Rev. 2.8 preparation on 2026-10-08. It checks the five-outcome qutrit POVM,
program-state spectra, the rational probability matrix (`det Π=2⁻¹⁸`), linear independence of the
five base and target Choi matrices, and positive target Choi eigenvalues. This is a numerical arithmetic/rank check; the exact entries, determinant,
dimension-square lower bound, and processor construction are given analytically in C.33. No SDP
solver was run for the closed-form overlap calculations, and no finite check proves the
analytic/category-level theorems.

## Appendix B — Map from the original draft

See `REVISION_CHANGELOG_v2.8.md` for the Rev. 2.7 → Rev. 2.8 changes, and
`REVISION_CHANGELOG_v2.7.md` for the preceding Rev. 2.6 → Rev. 2.7 changes; earlier proof and scope
corrections are preserved in `REVISION_CHANGELOG_v2.6.md`, `REVISION_CHANGELOG_v2.5.md`, and the
original-to-Rev. 2.4 map `REVISION_CHANGELOG.md`.

---

## Appendix C — Open-problem proofs, residual gaps, and finite programming benchmarks

This appendix adjudicates and closes several, but not all, of the open problems in §7.2, and in
C.29–C.35 records a separate programming addendum. The supplied unpublished working note [16] is
treated as a source to check, not as authority: each adopted claim is re-derived against the
manuscript's definitions, and unsupported generalizations remain open. C.29 concerns exact
deterministic overlaps; C.30–C.34 specify their own heralded model and finite target families or bounds;
C.35 is a deterministic extreme-boundary dimension bound. None reopens R1, which remains closed by
C.28, or closes R8. The inherited finite checks L1–L27 and the qutrit-family rank/arithmetic check
are numerical certificates only, not formal proofs of analytic or category-level results. The claim-by-claim dispositions and source line references for the earlier
open-problem audit are in `audits/05_OPEN_PROBLEMS_SOURCE_EVAL.md`; the δₙ scope audit and pairwise
programming calculations are preserved in `audits/06_DELTA_N_AUDIT_AND_PROOFS.md` and
`audits/07_PAIRWISE_OVERLAP_SDP_AND_HERALDED_COST.md`.

**Conventions.** `E, B, A, R` are nonzero Hilbert spaces, `d_X = dim X`; unless a statement says
otherwise, `E`, `B`, `A` are finite-dimensional (statements allowing infinite-dimensional `B` or `R` say
so explicitly); `Chan`,
`Instr_n`, `State` as in §2–§3. `Chan(E,B)` is identified with the set of Choi operators
`{J ≥ 0 : Tr_B J = 1_E}` of dimension `d_E²(d_B²−1)` (Prop. 3.1 at `n = 1`). `M_r ⊂ Chan(E,B)` is the
subset of Choi rank `≤ r`. "Representable" means: there is an object `R` and a counit
`ε_B ∈ Instr(R⊗B, B)` (per `B`) such that `g ↦ ε_B ∘ (g ⊗ id_E)` is a bijection
`Instr(A⊗E,B) → Instr(A, R(B))` for every `A` — the slicing form of `F_E ⊣ R` (Def. 4.6, Lemma 4.1).
Dimension of a semialgebraic set means the maximum of its local (real) dimensions; it is a
homeomorphism invariant, which is all that is used below.

### C.1 The overlap identity

> **Lemma C.1 (overlap identity; complete environments).** Let `W:R⊗E→B⊗G` be an isometry and
> let `ψ,ψ'∈R` be unit vectors. Write `W_ψ x = W(ψ⊗x)`. Then
> `W_ψ†W_ψ' = ⟨ψ|ψ'⟩ I_E`.
> If `{e_i}` and `{e'_l}` are **complete orthonormal bases of the same environment `G`**, and
> `K_i=(I_B⊗⟨e_i|)W_ψ`, `K'_l=(I_B⊗⟨e'_l|)W_ψ'`, then
> `⟨ψ|ψ'⟩I_E = Σ_{i,l}⟨e_i|e'_l⟩ K_i†K'_l`, with the sum understood in the weak-operator sense
> (equivalently as the limit of finite compressions). In particular, if the left coefficient is
> nonzero, `I_E` lies in the weak-operator closed linear span of these cross-products.

*Proof.* Since `W` is an isometry,
`⟨W(ψ⊗x),W(ψ'⊗y)⟩=⟨ψ|ψ'⟩⟨x|y⟩` for all `x,y∈E`, which is the first identity.
For complete bases of the common `G`, the resolution-of-identity operator is
`Σ_{i,l}⟨e_i|e'_l⟩ |e_i⟩⟨e'_l|=I_G`; for infinite bases this holds as a weak-operator limit of
finite partial sums. Inserting it between `W_ψ†` and `W_ψ'` gives the displayed expansion.
When two minimal Stinespring dilations are used, their embeddings into `G` must be the embeddings
induced by the *same common dilation* `W`; the associated cross-Gram coefficients are not chosen
independently. Completing each family by zero Kraus operators is harmless. An arbitrary incomplete
family does **not** resolve `I_G`; it gives a support projection instead, so the formula with `I_E`
cannot be asserted for such a family. ∎

*Remark.* The source's finite-dimensional use takes complete bases, as does check L4c. The no-programming
argument below uses the same identity in the common Stinespring environment; no equality of unrelated,
incomplete Kraus lists is assumed.

### C.2 The Kraus-rank theorem: finite-dimensional `Chan(E,B)` is not a state space

> **Theorem C.2.** Let `E,B` be finite-dimensional with `d_E,d_B≥2`. Then `Chan(E,B)` is not
> affinely isomorphic to the normal state space of `B(H_R)` for any Hilbert space `R`.

*Proof.* Put `N=d_Ed_B`.
**(0) The state-space dimension.** If `R` is infinite-dimensional, its normal state space has infinite
affine dimension: it contains simplices on arbitrarily many orthogonal rank-one projections. The
channel body has finite affine dimension `d_E²(d_B²−1)`, so an affine isomorphism forces `R` finite.

**(1) Rank strata and their tangent dimensions.** A Choi matrix of rank `r` has a factorization
`J=KK†`, with `K∈C^{N×r}` full column rank. The rank-`r` positive-semidefinite stratum is a smooth
real manifold: `K` contributes `2Nr` real parameters, and the free right action of `U(r)` removes `r²`.
Thus its dimension is `2Nr−r²`; its tangent vectors at `J=KK†` are
`δJ=KX†+XK†`.

**(2) The trace-preserving slice is transverse.** Consider `T(J)=Tr_B J` on this rank stratum. If a
Hermitian `H∈Herm(E)` annihilates the image of `dT_J`, then for every `X`
`0=Tr[(H⊗I_B)(KX†+XK†)]=2 Re Tr[X†(H⊗I_B)K]`; hence `(H⊗I_B)K=0`. Writing the columns of `K`
as vectorized Kraus operators `K_i:E→B`, this says `K_i H^T=0` for every `i`. Since
`Σ_i K_i†K_i=I_E`, the `K_i` have no common kernel, so `H=0`. The adjoint of `dT_J` is therefore
injective and `dT_J` has full real rank `d_E²`. On every nonempty rank-`r` trace-preserving stratum,

dim = `2Nr−r²−d_E²`.

**(3) Extreme ranks and attainment.** Choi's extremality criterion says that a channel with a minimal
Kraus family `{K_i}_{i=1}^r` is extreme exactly when `{K_i†K_j}_{i,j}` is linearly independent.
Therefore `r²≤d_E²`, so an extreme channel has `r≤d_E`. Rank `d_E` is attained: with an orthonormal
basis `{e_i}` of `E` and a unit `u∈B`, put `K_i=|u⟩⟨e_i|`. Then `Σ_iK_i†K_i=I_E` and
`K_i†K_j=|e_i⟩⟨e_j|` are independent. Independence is an open condition on the rank-`d_E` stratum,
so its extreme subset has the full stratum dimension. For `r<d_E`, the stratum dimension is strictly
smaller because
`[2N(r+1)−(r+1)²]−[2Nr−r²]=2N−2r−1>0` when `d_B≥2`. Hence

`dim Ext Chan(E,B)=2d_E²(d_B−1)`.

**(4) Compare with a state space.** The pure states of an `R`-dimensional quantum system form
`CP^{R−1}`, of real dimension `2(R−1)`, and the whole state body has affine dimension `R²−1`.
An affine bijection of finite-dimensional convex bodies maps extreme points bijectively and
homeomorphically, so it would force
`R=d_E²(d_B−1)+1` and `R²−1=d_E²(d_B²−1)`. Substitution gives
`(d_E²−1)(d_B−1)=0`, contrary to `d_E,d_B≥2`. ∎

The extreme-boundary dimensions at three count-matched escapes are:

| `(d_B,d_E,d_R)` | `dim Ext Chan(E,B)` | `dim Ext State(C^{d_R})` |
|---|---:|---:|
| `(2,4,7)` | `32` | `12` |
| `(4,8,31)` | `384` | `60` |
| `(3,35,99)` | `4900` | `196` |

*(Exact arithmetic certificates: L3a–L3f.)*

> **Corollary C.3.** (i) In the finite-dimensional range of Theorem C.2, the normal state space of
> no Hilbert space is affinely isomorphic to `Chan(E,B)`. This rules out isomorphism, not affine
> embeddings. (ii) The same conclusion holds for the state space of any finite-dimensional
> C*-algebra `⊕_{i=1}^s M_{r_i}`. (iii) At `B=ℂ`, the whole presheaf `A ↦ Chan(A⊗E,ℂ)` is singleton-valued
> and is naturally represented by `R=ℂ`; this does not give a right adjoint for all targets `B`.
> (iv) Proposition 4.9 transfers global non-adjunction only in the literal graded category
> `Instr_lab` of Definition 2.2 and the outcome-permutation quotient `Instr_perm`. It does not
> propagate to `Instr_0`, `Instr_cg`, `Instr_D`, `Instr_Q`, or `D^ω`; their pointwise theorems are
> independent.

*Proof of (ii).* Let `q=max_i r_i`. The state space has affine dimension `Σ_i r_i²−1`; its extreme set is
a finite disjoint union of projective spaces, of maximal real dimension `2(q−1)`. If it matched
`Chan(E,B)`, the extreme dimensions would force `q=d_E²(d_B−1)+1`. But then
`Σ_i r_i²−1 ≥ q²−1 > d_E²(d_B²−1)`, since
`q²−1=d_E²(d_B−1)[d_E²(d_B−1)+2]` and
`d_E²(d_B−1)+2>d_B+1` for `d_E≥2`. This contradicts the affine-dimension equality. ∎

*A class not excluded:* affine embeddings of `Chan(E,B)` into state spaces, or affine isomorphisms to
convex bodies that are not quantum state spaces. For finite-dimensional `E` and infinite-dimensional
`B`, the separate face argument in Proposition C.21 supplies the state-space obstruction; Theorem C.2
itself is the finite-dimensional Kraus-stratum calculation.

### C.4 Why `B = ℂ` is the genuinely instrument-specific case

For `d_B = 1`, `Chan(E,ℂ)` is a single point and `State(ℂ^R) ≅ Chan(E,ℂ)` for `R = 1`: Theorem C.2 is
vacuous there. It is exactly the `B = ℂ` fibre that requires the instrument-level (recorded-mixing)
arguments of C.8, C.10, C.12. This is the precise sense in which the *instruments* add content beyond
the deterministic category.

### C.5 Record forgetting: the no-programming theorem (with the register hypothesis)

Let `C` be an instrument category equipped with a functor `Σ:C→Chan` that forgets the record by
summing the outcome maps, is the identity on one-outcome channels, and commutes with `−⊗E`.
This includes the literal finite-outcome `Instr` and the quotient models whenever their stated outcome
sums are defined. The functor `Σ` is **surjective but not injective**: every channel is a singleton
instrument, while, for example, the two-outcome dephasing instrument and its total dephasing channel
are distinct morphisms in the instrument category. Surjectivity is enough for the processor below;
it is not the restriction argument of Proposition 4.9.

> **Theorem C.5 (separable-program no-go, pointwise).** Let `E,B` be Hilbert spaces with
> `dim E,dim B≥2`, and use normal channels/instruments. If a representability
> `Hom_C(A⊗E,B)≅Hom_C(A,R(B))` is supplied by a counit and `R(B)` is separable, then a contradiction
> follows. In particular, no such pointwise representation exists with a separable program register.

*Proof.* Applying `Σ` to the counit gives a normal channel `\bar ε:R(B)⊗E→B`. At `A=ℂ`, the
one-outcome channel `f:E→B` has a preimage instrument `g`; after forgetting its record,
`f=\bar ε(ρ⊗−)` for the normal program state `ρ=Σ(g)`. Thus
`T(ρ)=\bar ε(ρ⊗−)` maps normal states of `R(B)` onto all normal channels `E→B`.

We build a continuum of extreme channels whose exact programs must be orthogonal. Fix a two-dimensional
subspace `B_0⊂B` with orthonormal basis `u_0,u_1`, and decompose
`E=E_1⊕\bigoplus_{j∈J}ℂe_j`, where `E_1` has orthonormal basis `e_0,e_1` and `J` indexes the
remaining basis vectors. Let `V_1:E_1→B_0` send `e_a↦u_a`, and let
`v=(u_0+u_1)/√2`. Define Kraus operators
`K_1^θ=V_1D_θP_1`, `D_θ=diag(e^{iθ},1)`, and `K_j=|v⟩⟨e_j|` for `j∈J`. Their initial spaces are
orthogonal and `Σ_i(K_i^θ)†K_i^θ=I_E`, so they define a normal channel `f_θ`. Every product
`(K_i^θ)†K_j^θ` is nonzero and occupies its own input block `(E_j→E_i)`; the family is linearly
independent. More explicitly, for `i,j∈J` it is `|e_i⟩⟨e_j|`, for `(1,j)` it has the two nonzero
coordinates inherited from `V_1†v`, and `(1,1)` is `P_1`.

For completeness, this product independence proves extremality also for the possibly infinite Kraus
family. The Stinespring isometry `V_θx=Σ_iK_i^θx⊗|i⟩` is minimal: a vector in the environment
orthogonal to its minimal span would give a square-summable linear relation `Σ_i c_iK_i^θ=0`, and
compression to each initial block forces every `c_i=0`. By the normal CP Radon–Nikodym theorem,
if `f_θ=p f_1+(1−p)f_2` with `0<p<1`, then the dominated map `p f_1` is represented by a positive
contraction `D` on the common minimal environment. Trace preservation of `f_1` gives
`V_θ†(I_B⊗D)V_θ=pI_E`, or
`V_θ†(I_B⊗(D−pI))V_θ=0`. In a complete environment basis this compression expands in the products
`(K_i^θ)†K_j^θ`. Their block supports are pairwise disjoint and every product is nonzero, so each
matrix coefficient of `D−pI` vanishes (for infinite bases, read the equality weakly on basis-vector
compressions). Thus `D=pI`, hence `f_1=f_θ`; similarly `f_2=f_θ`. Therefore `f_θ` is extreme.

Let `W:R(B)⊗E→B⊗G` be a Stinespring isometry for `\bar ε`. For each `θ`, surjectivity of `T`
provides a normal state program; its spectral decomposition is a countable convex combination of
pure normal states. Since `f_θ` is extreme and `T` is affine, every nonzero spectral component also
programs `f_θ`; choose a unit vector `ψ_θ` with `T(|ψ_θ⟩⟨ψ_θ|)=f_θ`. The compressed isometry
`W_{ψ_θ}:x↦W(ψ_θ⊗x)` dilates `f_θ`. By Stinespring uniqueness it factors through the minimal
dilation as `(I_B⊗J_θ)V_θ`, with `J_θ` an isometry into `G`. Therefore

`⟨ψ_θ|ψ_{θ'}⟩I_E = Σ_{i,j} Γ_{ij}(K_i^θ)†K_j^{θ'}`,

where `Γ=J_θ†J_{θ'}` is a contraction. To apply C.1, complete the two embedded minimal
Stinespring bases to complete orthonormal bases of the same `G`; the Kraus operators on the
orthogonal complements are zero, so the displayed sum is unchanged, and the nonzero-support
cross-Gram block is precisely `Γ`. The embeddings `J_θ,J_{θ'}` are induced by the same dilation `W`,
not independently selected. Compress the equality to `E_1`. Only the `(1,1)` block contributes, so
`c I_{E_1}=Γ_{11}diag(e^{i(θ'−θ)},1)`, where `c=⟨ψ_θ|ψ_{θ'}⟩`. For distinct angles modulo `2π`,
comparison of the two diagonal entries gives `Γ_{11}=c=0`. Thus the continuum `{ψ_θ}` is an
orthonormal family, impossible in a separable `R(B)`. ∎

*Scope.* This theorem is a pointwise obstruction when the candidate program register is separable.
For finite-dimensional `E,B`, C.2 and C.21 remove that register restriction in `Chan`; the direct
instrument results C.8, C.10, C.12 and C.22 have their own proofs. A non-separable lookup-table
processor exists (C.26), so the surjective-processor argument by itself cannot settle non-separable
registers.

### C.6 The coarse-graining category `Instr_cg`

**Definition C.6 (cg instruments).** For objects `A, B`, let `Hom_cg(A,B)` be the set of those finitely
supported (or countably supported) measures `μ = Σ_{i∈I} c_i δ_{r_i}` on the set of rays `r` of nonzero
CP maps `A → B`, such that `Σ_i c_i e(r_i)†(1_B) = 1_A`, where `e(r)` is a fixed representative of the
ray `r` and `I` is finite (resp. countable). Composition and identity are componentwise,
`(T∘S) = reduce{F∘E}` where `reduce` merges components in the same ray and drops zero composites; the
zero composites are dropped, so `reduce` is a congruence: `E ∝ E'` implies `F∘E ∝ F∘E'`. Recorded
mixing is `pμ + (1−p)μ'`. Two elementary facts, both immediate: (i) `reduce` is linear in the measure
`μ`, so composition is bi-affine and `F_E = (−⊗id_E)` preserves rays and weights; (ii) hence for any
representation `(R, ε)`, the map `Φ_A(g) = ε_B ∘ F(g)` is **affine** for recorded mixing and, being a
bijection, an isomorphism of convex sets — so it maps extreme points onto extreme points and preserves
supports of finitely supported measures.

### C.7 Extreme points of the cg hom-sets

> **Lemma C.7.** *In `Hom_cg(A,B)`, `μ = Σ_{i∈I}c_iδ_{r_i}` is extreme (for recorded mixing) iff the
> marginals `v_i := e(r_i)†(1_B) ∈ Herm(A)`, `i ∈ supp μ`, are linearly independent. Consequently every
> extreme point has `|supp μ| ≤ d_A²`, and in particular is **finitely supported** — also in the
> countably supported model.*

*Proof.* (⇐, "independent ⇒ extreme") A decomposition `μ = pμ' + (1−p)μ''` has
`supp μ' ∪ supp μ'' = supp μ` and, writing `w_i` for the difference of the weights, `Σ_i w_i v_i = 0`;
independence forces `w = 0`, i.e. `μ' = μ'' = μ`. (⇒, "dependent ⇒ not extreme") Let
`Σ_{i∈J}w_iv_i = 0`, `w ≠ 0`, `J` a finite subset of `supp μ`. For small `ε > 0` the perturbed weights
`c_i ± εw_i` (`i ∈ J`) stay positive and still satisfy the constraint, so
`μ = ½(μ + εW) + ½(μ − εW)` is a non-trivial decomposition. The bound `|supp μ| ≤ d_A²` follows since
`Herm(A)` has dimension `d_A²`; for a countably supported `μ` pick any dependent finite subset (one
exists as soon as `|supp μ| > d_A²`), which the same perturbation argument uses without touching the
other, infinitely many, weights. ∎

*Machine checks:* L15a (independent ⇒ extreme), L15b (dependent ⇒ not extreme, explicit perturbation),
L15c (Carathéodory bound).

### C.8 The quadrilateral: `Instr_cg` is not representable

> **Theorem C.8.** Let `d_E ≥ 2`, let `B` be arbitrary (including `B = ℂ`) and let `R` be arbitrary.
> Then `Hom_cg(−⊗E, B)` is not representable, for finite **or countably supported** outcome sets.
> *(§7.2(2) for `Instr_cg`: resolved.)*

*Proof.* Suppose `(R, ε)` represents. Take `A = ℂ`; by C.6(ii) and C.7, `Φ: Hom_cg(ℂ,R) → Hom_cg(E,B)`
is an affine isomorphism of convex sets, and `Hom_cg(ℂ,R) ≅ {finitely supported probability measures
on State(R)}` (allowed rays with trace-one representatives; recorded mixing = convex combination).
**Step 1 (a quadrilateral face in the target).** Let `a` be a non-scalar Hermitian on `E` and
`δ > 0` small; set `v_l = ¼·1_E + δβ_l a` with `β = (1,−1,2,−2)`, so that every `v_l` is positive.
Since `Σ_l v_l = 1_E` automatically (because `Σβ_l = 0` and the scalar part is `4·¼ = 1`), the four
classes `v_l` are effects with `Σ_l v_l = 1_E`. Let `σ` be a state of `B` and put
`f_l := tr(v_l · )σ`; these are pairwise non-proportional, nonzero CP maps `E → B` with marginals `v_l`,
and `f := {f_1,f_2,f_3,f_4}` is a four-outcome instrument of `Hom_cg(E,B)`. Its two decompositions into
extreme instruments are
> `f = ½e₁₂ ⊕ ½e₃₄ = ¼e₃₄ ⊕ ⅜e₁₄ ⊕ ⅜e₂₃`,  with
> `e₁₂ = {2f_1,2f_2}`, `e₃₄ = {2f_3,2f_4}`, `e₁₄ = {(8/3)f_1,(4/3)f_4}`, `e₂₃ = {(8/3)f_2,(4/3)f_3}`,
where a scalar prefactor multiplies every component. The weights `(½,½)` and `(¼,⅜,⅜)` sum to `1`, and
both sides reproduce the multiset `{f_1,f_2,f_3,f_4}` — verified in exact rational arithmetic (L1e).

**Step 2 (the face is a quadrilateral, not a simplex).** The face of the target carried by `f` is
`P_T = {c ≥ 0 : Σ_l c_l v_l = 1_E}`. Because `Σ_l v_l = 1_E` and `a` is non-scalar,
`Σ_l c_l v_l = (Σ_l c_l)/4·1_E + δ(Σ_l β_l c_l)a`, so
> `P_T = {c ≥ 0 : Σ_l c_l = 4, Σ_l β_l c_l = 0}`,
a polygon in a 2-plane. Its vertex set (all basic feasible solutions, enumerated in exact arithmetic,
L1b) is exactly `{(2,2,0,0), (0,0,2,2), (8/3,0,0,4/3), (0,8/3,4/3,0)}`, and the corresponding
instruments `e₁₂, e₃₄, e₁₄, e₂₃` are trace-preserving with linearly independent marginals, hence extreme
in `Hom_cg(E,B)` (L1c, L1d). Four vertices in a 2-plane: a quadrilateral, not a simplex.

**Step 3 (source-side contradiction).** `Φ⁻¹` maps the four extreme points `e₁₂, e₃₄, e₁₄, e₂₃` to
extreme points of `Hom_cg(ℂ,R)`, i.e. (C.7) to four pairwise **distinct** states `ρ₁₂, ρ₃₄, ρ₁₄, ρ₂₃`,
and the equality of Step 1 to an equality of probability measures on `State(R)`:
`½δ_{ρ₁₂} + ½δ_{ρ₃₄} = ¼δ_{ρ₃₄} + ⅜δ_{ρ₁₄} + ⅜δ_{ρ₂₃}`.
The left side is supported on `{ρ₁₂,ρ₃₄}`, the right side on `{ρ₃₄,ρ₁₄,ρ₂₃}`; with `ρ₁₄,ρ₂₃ ∉ {ρ₁₂,ρ₃₄}`
the supports differ, and two positive measures with different supports are different. Contradiction. ∎

> **Remark C.9 (the arithmetic of this section).**
> (i) *Top stratum.* Since `k = d_A²` extreme instruments exist generically and their stratum is open in
> the `n = d_A²` slice of Prop. 3.1, the extreme set of `Instr_cg(A,B)` has dimension
> `d_A²(d_A²d_B²−1)` (L10).
> (ii) *Simplex vs quadrilateral.* Preparation-type hom-sets `Hom_cg(ℂ,R)` are simplices whose extreme
> points are single states; measurement-type hom-sets carry the quadrilateral above. That is the whole
> obstruction.
> (iii) *Scales.* Over `ℚ`-convexity the same quadrilateral reappears (weights `τ_t = ¼+β_t√2/20`), so
> the ℚ-simplex test fails; the source note retracts its earlier ℚ-simplex remark, and this is verified
> (L7a–L7c). The ℚ-quotient is closed instead by Theorem C.12.
> (iv) *Independent dimension route.* Proposition C.20 completes the semialgebraic bookkeeping for
> the extreme-set dimension and proves the finite-counit consequence. It **does** see `B=ℂ`: the
> one-slice equation lies between consecutive squares for every finite `d_B≥1`. The quadrilateral
> remains the stronger proof because it also handles arbitrary `R` and countably supported outcomes.

### C.10 `Instr_0`: atomic factorization (no merging at all)

Let `Hom_0(A,B)` be the set of finite or countably supported multisets of nonzero normal CP maps
`A→B` whose sum is trace-preserving; composition is componentwise and drops zero composites, but
never merges nonzero components. Equality is literal multiset equality. Recorded mixing is
`pS ⊕ (1−p)S' := {pE}_{E∈S} ⊎ {(1−p)F}_{F∈S'}`; composition is linear in each argument, so the
universal map is affine. The proof below uses only finite-support target instruments.

> **Theorem C.10.** Let `d_E ≥ 2`, `B` arbitrary, `R` arbitrary, and let the outcome multiplicity be
> arbitrary. Then `Hom_0(−⊗E, B)` is not representable. *(§7.2(2) for `Instr_0`: resolved.)*

*Proof.* Call `f` **irreducible** if no proper non-empty sub-multiset of `f` has marginals summing to a
scalar multiple of `1_E`. Two elementary facts.
(a) *Irreducible ⇒ atom.* If `f = pS ⊕ (1−p)S'` with both summands non-empty, then the components of
`pS` form a proper non-empty sub-multiset whose marginals sum to `p·1_E`.
(b) *Atoms of `Hom_0(ℂ,R)` are single states.* A multiset `{c_1ρ_1,…}` with `k ≥ 2` components splits as
`p·{c_1ρ_1/p} ⊕ (1−p)·{c_2ρ_2/(1−p),…}`; and a one-component element cannot be a non-trivial mix, since
a union of two non-empty multisets has at least two elements.

Now take the **pair-sum example** (a different one from the quadrilateral of C.8): a bounded non-scalar
Hermitian `x` with `‖x‖` small and the four positive effects
> `A = 1/5·1_E + x`, `B' = 3/10·1_E − x`, `C = 1/4·1_E + x`, `D = 1/4·1_E − x`,
so that `A+B' = C+D = ½·1_E`, `A+D = 9/20·1_E`, `C+B' = 11/20·1_E` (all *scalar* pair sums: the
`S`-shaped parameter choice is what makes the identity below literal), and let
`f_l = tr(v_l ·)σ` for `v = (A,B',C,D)` with any state `σ ∈ State(B)`. The four atoms
> `a_{AB'} = {2f_1,2f_2}`, `a_{CD} = {2f_3,2f_4}`, `a_{AD} = {(20/9)f_1,(20/9)f_4}`,
> `a_{CB'} = {(20/11)f_3,(20/11)f_2}`
are irreducible — each has two components with non-scalar marginals (a proper non-empty sub-multiset is
a single component, whose marginal is `2A`, `2B'`, … , not a scalar multiple of `1_E`) — hence atoms,
and they are pairwise distinct. In `Instr_0` there is no merging, and the identity
> `½a_{AB'} ⊕ ½a_{CD} = 9/20·a_{AD} ⊕ 11/20·a_{CB'} = f`
holds **literally, component by component**: `½·(2f_1) = f_1`, `(9/20)·(20/9)f_1 = f_1`, and so on for
all four components, both sides giving the multiset `{f_1,f_2,f_3,f_4}` (exact arithmetic: L2a–L2c,
L18). A representation would pull this back, along the affine bijection of C.6(ii), to
> `{½ρ̂₁, ½ρ̂₂} = {9/20·ρ̂₃, 11/20·ρ̂₄}`
with four pairwise distinct states; but the two sides are multisets of CP maps `ℂ → R` whose components
have different traces (`½ ≠ 9/20`, `½ ≠ 11/20`), so the multisets differ. Contradiction. ∎

*Finite checks:* L2 and L18 verify the exact pair-sum identity; L27 separately checks that the fixed
grade-2 componentwise convex slice is not the recorded-union operation used by `Instr_0`.

### C.11 The infinite-merge dyadic quotient `D^ω`

In `D^ω`, a morphism is a countably supported nonnegative weight vector on the `2^ℤ`-orbits of
nonzero CP maps, with `Σ_O w_O r_O` trace-preserving for chosen representatives `r_O`; real weights
are allowed, as they arise from countably infinite dyadic multisets. Mixing is midpoint averaging.
Composition is componentwise followed by the orbit-weight pushforward; dyadic rescaling is a
congruence for composition.

> **Proposition C.11.** For `d_E≥2` and nonzero `B`, `Hom_{D^ω}(−⊗E,B)` is not representable, for
> any program Hilbert space `R`.

*Proof.* Choose a bounded nonscalar Hermitian `H` on `E`, a normal state `σ` on `B`, and small
`δ>0`. Put `v_l=I_E/4+δβ_lH`, `β=(1,−1,2,−2)`, and `f_l(X)=tr(v_lX)σ`. These are positive
nonzero CP maps in four distinct proportionality rays, and `Σ_l v_l=I_E`. Choose `f_l` themselves
as representatives of their `2^ℤ`-orbits. The four orbit-weight vectors

`e₁₂=(2,2,0,0)`, `e₃₄=(0,0,2,2)`,
`e₁₄=(8/3,0,0,4/3)`, `e₂₃=(0,8/3,4/3,0)`

are trace-preserving: their weights satisfy `Σ_l c_l=4`, `Σ_l β_lc_l=0`. Each is extreme for
midpoint mixing. Indeed, any midpoint decomposition has support within its two orbit coordinates;
those two marginal effects are linearly independent, so the normalization equation uniquely fixes the
weights. The four are distinct, and orbit-by-orbit arithmetic gives

`(1,1,1,1)=½e₁₂+½e₃₄=¼e₃₄+⅜e₁₄+⅜e₂₃`.

Suppose a representation existed and take `A=ℂ`. A counit-composition bijection commutes with
midpoint mixing, so it and its inverse preserve midpoint-extreme points. On the source,
`Hom_{D^ω}(ℂ,R)` is a countably supported probability vector on the orbit set of nonzero positive
trace-class maps `ℂ→R`: the probability at `O` is `w_O tr(r_O)`. Its midpoint-extreme points are
exactly the one-orbit vectors. Thus the four distinct target extremes pull back to four distinct
source orbit-atoms. Pulling back the displayed equality would identify two probability vectors with
different finite supports, impossible. ∎

*Finite checks:* L16 and L25 check the exact orbit-weight decompositions, distinct ray labels, supported
marginal independence, and the source midpoint-simplex witness. They do not replace the extremality proof.

*Scope.* This proves the `D^ω` case from its stated orbit-weight definition, separately from the
finitary `Instr_D` theorem C.12/C.23. It does not define a countably supported rational-merge analogue.

### C.12 Dyadic and rational merging: finite-counit rigidity

**Definitions for this result.** `Instr_D` identifies finite or countably supported multisets by the
finitary congruence generated by splitting/merging a proportional pair `F,F ↔ 2F`; each equivalence
uses finitely many such moves. `Instr_Q` is the finite-outcome quotient allowing rational proportional
splits/merges. A countably supported rational-merge quotient is not defined by this rule: an infinite
sum of rational weights can be irrational, changing the rational orbit. The theorem only assumes the
counit has finitely many nonzero components, say `m`.

> **Theorem C.12.** Let `E,B` be Hilbert spaces with `dim E≥2`, use normal maps, and let a proposed
> pointwise representation in `Instr_D` or `Instr_Q` have a counit with `m<∞` outcomes. Then no
> representing object exists, for any program Hilbert space `R`; in particular the result includes
> `B=ℂ` and non-separable `R`.

*Proof (genericity and rigidity).* Choose a bounded nonscalar Hermitian `H` on `E`, and choose positive
real numbers `α_1,…,α_{k−1}` linearly independent over `ℚ`, where `k=m+1`; put
`α_k=−Σ_{l<k}α_l`. For sufficiently small `δ>0`,
`v_l=I_E/k+δα_lH` are positive effects with `Σ_l v_l=I_E`. In the quotient
`B_sa(E)/ℝI`, the only rational relation among their classes
`\bar v_l=δα_l\bar H` is a multiple of the forced relation `Σ_l\bar v_l=0`: indeed
`Σ_l q_l\bar v_l=0` is equivalent to
`Σ_{l<k}(q_l−q_k)α_l=0`, so all rational coefficients `q_l` equal `q_k`.

Fix a normal state `σ` of `B` and let `f_l(X)=tr(v_lX)σ`. These are nonzero, pairwise distinct CP
rays and `f={f_1,…,f_k}` is an instrument. Let `g={ρ_i}` be a preimage at `A=ℂ`, and write
`τ_i=tr ρ_i>0`. Each counit outcome `j` contributes at most one CP map, so after reduction each
nonzero composite `ε_j(ρ_i⊗−)` lies on exactly one target ray `f_l`. Starting from the coefficient `1`
of `f_l`, every finite `D` split/merge keeps each component coefficient dyadic; every finite `Q`
split/merge keeps it rational. Since the whole composite class is equivalent to the target, each
nonzero composite coefficient is therefore dyadic (in `D`) or rational (in `Q`). Let `a_{i,l}≥0`
be the total coefficient of ray `l` from the fixed program component `ρ_i`. There are at most `m`
terms in each such sum, so every `a_{i,l}` is rational.
The total-map constraint for this component is
`Σ_l a_{i,l}v_l=τ_i I_E`. Passing to `B_sa(E)/ℝI` and using the rational-relation property forces
`a_{i,1}=···=a_{i,k}=c_i`. Since `Σ_l v_l=I_E`, the full equation gives `c_i=τ_i>0`. Thus every one
of the `k=m+1` distinct target rays must be supplied by at least one of the `m` counit outcomes for
this single program component, impossible. ∎

*Definition boundary.* The finite rational-merge rule does not define a countable-merge quotient.
Indeed, the nonzero decimal-place contributions in the expansion of `√2` are positive rationals whose
sum is irrational; a countable merge could therefore leave the rational-proportionality orbit. One
cannot extend the finite quotient by simply replacing “finite” with “countable”. This is a
category-definition limitation, not an unproved no-go theorem.

### C.13 Scope in infinite dimensions, measurable outcomes, and non-normal states

> **Proposition C.13 (scope ledger).**
> (a) For finite-dimensional `E,B` with `d_E,d_B≥2`, `Chan(E,B)` is not a normal state space for any
> register dimension (C.2). If `E` is finite and `dim B≥d_E`, C.21 gives the isometric face obstruction
> for arbitrary Hilbert `B`; C.22 gives a separate two-dimensional face for every finite pair
> `d_E,d_B≥2`.
> (b) `Instr_0` is pointwise non-representable for arbitrary Hilbert dimensions (C.10). `Instr_cg` is
> closed for finite-dimensional `E` and arbitrary `B,R` with finite or countably supported outcomes
> (C.8). `Instr_D` is closed for arbitrary `E,B,R` when its counit is finite (C.12), for finite
> `E` with a countable counit (C.23), and for infinite-dimensional `E` with a countable counit
> (C.28). `Instr_Q` is treated only with finite outcomes/counit (C.12); a countable rational-merge
> extension is not defined by the stated quotient.
> (c) In any normal instrument model admitting the total-map functor, a separable program register
> cannot represent `E→B` when `dim E,dim B≥2`, even if `E` or `B` is infinite (C.5). In particular,
> this rederives the source note's separable infinite-dimensional `B≥2` result. At `B=ℂ`, C.12 covers
> finite counit outcomes in all dimensions; C.23 covers finite-dimensional `E` with countable
> finitary-`D` counit, and C.28 covers infinite-dimensional `E` with countable counit.
> (d) The source note's non-separable `Instr_0` face-partition proof (Thm 7) is not needed: C.10 is
> stronger and uses no compactness or separability. For the separate source `Chan` face claims, C.21
> treats isometric channels with finite `E` and `dim B≥d_E`; C.22 treats every finite pair
> `d_E,d_B≥2`. Neither is an infinite-dimensional-`E` face theorem. The finitary-`D` R1 gap is
> instead closed by C.28.
> (e) A non-separable lookup-table processor is constructed in C.26. It proves that the surjective
> processor route alone cannot exclude a non-separable register; it does not give an adjunction.
> (f) R1, the finitary dyadic quotient with infinite-dimensional `E`, non-separable `R`, and a
> countable counit, is closed by C.28. Remaining open cases include identifying the intended
> measurable-outcome quotient with the explicit ray-measure category (C.25), the non-normal
> C*-algebraic setting, and full `𝒯`/`Caus` scope outside C.24's balanced companion.

### C.14 The finitary-D support and response lemmas

> **Lemma C.14.** Let `D` be the finitary dyadic quotient, with countable outcome sets.
> (a) If a finite class `f` is equivalent to the composite `ε∘F(g)`, then the nonzero composite
> multiset is finite. Every source outcome of `g`, and every pure spectral component of it, is supported
> on a finite set `J` of counit outcomes.
> (b) For any finite set `J` of counit outcomes, the response map on Hermitian trace-class program
> operators supported in `V_J` is injective, where
> `V_J={ψ: ε_j(|ψ⟩⟨ψ|⊗−)=0 for all j∉J}`. If `E,B` are finite-dimensional, this implies
> `(dim V_J)²≤|J|d_E²d_B²`; for `B=ℂ` the bound is `|J|d_E²`. If all responses on a subspace `W`
> have output supported in a fixed finite-dimensional `B_0⊂B`, the same bound holds with `d_B` replaced
> by `dim B_0`.

*Proof.* Each elementary dyadic split or merge changes the number of nonzero components by exactly
one. A finite sequence of moves cannot turn a countably infinite multiset into a finite one. Every
nonzero program outcome has at least one nonzero counit composite: otherwise the total counit would
send that positive program and every input state to zero, contradicting trace preservation. Hence a
finite composite class uses finitely many program outcomes and finitely many counit indices. Positivity
shows that if `ε_j(ρ_i⊗−)=0`, then the same is true for every vector in a spectral decomposition of
`ρ_i`; this proves the support assertion.

The set `V_J` is a linear subspace: a Kraus representation of each `ε_j`, `j∉J`, shows that all of
its Kraus operators annihilate `V_J⊗E`; polarization gives the same for off-diagonal program terms.
Let `h=h†` be trace class supported on `V_J` and suppose
`ε_j(h⊗−)=0` for every `j∈J`. The responses for `j∉J` also vanish, so the total response vanishes.
Trace preservation gives `tr h=0`. If `h≠0`, its positive and negative parts have the same nonzero
trace; normalizing them gives two distinct normal program states whose full counit instruments agree
componentwise. They therefore have the same image in `D`, contradicting injectivity of the representing
bijection. Thus the response map is injective. Its codomain is the finite product of Hermitian Choi
spaces, of real dimension `|J|d_E²d_B²` (or `|J|d_E²` for scalar output); an injective linear map
from Hermitian operators on `V_J` gives the stated bound. If all vectors in `W` have responses
supported in `B_0`, the same argument applies on `W` with the smaller codomain. ∎

### C.15–C.19 A typed affine-slice completion `𝒯`

The obstruction of §4 says that the ordinary channel category is not closed under `−⊗E`. The
following finite-dimensional affine-slice category is a concrete typed completion; no universal
minimality assertion is made.

**C.15 (typed systems and `𝒯`).** A **typed system** `𝔸=(H_A,L_A)` consists of a finite-dimensional
Hilbert space and an affine subspace `L_A` of trace-one Hermitian operators containing a
positive-definite density operator. Its admissible states are `S_A=L_A∩Pos_1(H_A)`. Morphisms
`𝔸→𝔹` are CP maps `f:A→B` with `f(L_A)⊂L_B`. The first-order system is
`𝔄=(H_A,{X=X†:tr X=1})`.

> **Lemma C.15.** (i) `aff(S_A)=L_A`. (ii) A CP map is a typed morphism iff it maps `S_A` into
> `S_B`. (iii) The typed systems form a category and the full first-order subcategory is `Chan`.
> (iv) With `L_A⊠L_B=aff{a⊗b:a∈L_A,b∈L_B}`, they form a symmetric monoidal category, and the
> first-order inclusion is strong monoidal.

*Proof.* A positive-definite point of `L_A` has a relative neighborhood in `L_A` consisting of
positive operators, so `S_A` affinely spans `L_A`. If `f(S_A)⊂S_B`, affinity gives
`f(L_A)=f(aff S_A)⊂aff S_B=L_B`; the converse is immediate. Identities and composition preserve
the slices. On first-order objects, preserving all trace-one positive states is equivalent to being
trace-preserving, since they linearly span the Hermitian operators. Products of admissible states
span the tensor affine slice; their product contains a positive-definite state. For two first-order
objects, product states affinely span the full trace-one Hermitian space on the tensor product, proving
strong monoidality. ∎

**C.16 (typed internal hom, weighted Choi slice, and adjunction).** Fix a typed input
`𝔈=(H_E,L_E)` and choose a positive-definite `τ_0∈S_E`. For every typed `𝔹=(H_B,L_B)`, put
`S= (τ_0^T)^{1/2}` on `H_{E^*}`. With the standard Choi operator `C(f)` on `E^*⊗B`, define
`C_{τ_0}(f)=(S⊗I_B)C(f)(S⊗I_B)` and

`L_[E,𝔹]=aff{C_{τ_0}(f): f:E→B is CP and f(L_E)⊂L_B}`,

`[𝔈,𝔹]=(H_{E^*}⊗H_B,L_[E,𝔹])`.

> **Theorem C.16.** The positive slice of `[𝔈,𝔹]` consists exactly of the weighted Choi operators
> `C_{τ_0}(f)` of typed channels `f:E→B`; the counit is CP and typed, and naturally
> `Hom_𝒯(𝔸,[𝔈,𝔹])≅Hom_𝒯(𝔸⊗𝔈,𝔹)`. Thus `−⊗𝔈 ⊣ [𝔈,−]` for every finite-dimensional typed input
> `𝔈`.

*Proof.* The typed-channel constraint is affine in `f`, and the invertible weighted Choi map is
linear. Hence every element of `L_[E,𝔹]` decodes to a Hermiticity-preserving map satisfying the typed
affine constraints. A positive operator in this slice decodes to a CP map, hence to a typed channel;
conversely every typed channel gives a positive weighted Choi operator. Its trace is
`tr C_{τ_0}(f)=tr f(τ_0)=1`. The replacement channel `f_0(X)=tr(X)b_0`, for any positive-definite
`b_0∈S_B`, is typed and has positive-definite weighted Choi operator, so `[𝔈,𝔹]` is an object of
`𝒯`.

Let `ev(Z⊗Y)=Tr_{E^*}[(Y^T⊗I_B)Z]` be standard Bell evaluation and set
`ev_{τ_0}(Z⊗Y)=ev(((S^{-1}⊗I_B)Z(S^{-1}⊗I_B))⊗Y)`. This is CP, and the Choi identity gives
`ev_{τ_0}(C_{τ_0}(f)⊗Y)=f(Y)`. For admissible `C_{τ_0}(f)` and `Y∈S_E`, the output lies in `S_B`;
by Lemma C.15 this is the typed counit.

For `F:A⊗E→B`, define its curry by
`Ψ(F)(X)=C_{τ_0}(Y↦F(X⊗Y))`. To check complete positivity, write
`F(Z)=Σ_s K_s ZK_s†`; the ordinary Choi curry has Kraus operators
`V_s|a⟩=Σ_i |i⟩⊗K_s(|a⟩⊗|i⟩)`. The weighted curry replaces `V_s` by
`(S⊗I_B)V_s`, so `Ψ(F)` is CP. The Choi reshuffling and its inverse are inverse linear operations.
Moreover, `Ψ(F)` maps `S_A` into `S_[E,𝔹]` exactly when each slice
`Y↦F(a⊗Y)` is a typed channel for every `a∈S_A`; by affine spanning of product states, this is
equivalent to `F` being a typed morphism on `𝔸⊗𝔈`. Thus curry/uncurry give inverse hom-set maps.
The evaluation identity gives both round trips and naturality in `𝔸,𝔹`. ∎

**C.17 (codimension for a first-order input).** If `𝔈` is first-order and `𝔹` is first-order, then
`S_[E,𝔹]` is an affine copy of `Chan(E,B)` and

`dim S_[E,𝔹]=d_E²(d_B²−1)=dim State(E^*⊗B)−(d_E²−1)`.

Thus the intercept in Proposition 3.1 is exactly the codimension of this typed slice. For `d_B≥2`,
C.2 shows it is not a first-order state space; the adjunction is in `𝒯`, not in `Chan`.

**C.18 (graded instruments).** For first-order `𝔄` and
`𝔹_n=(H_B⊗ℂ^n,L^bd)`, where
`L^bd={Σ_i b_i⊗|i⟩⟨i|: Σ_i tr b_i=1}`,

`Hom_𝒯(𝔄,𝔹_n)=Instr_n(A,B)`,

and `Instr_n(A⊗E,B)≅Hom_𝒯(𝔄,[E,𝔹_n])`. The internal-slice dimension is
`n d_E²d_B²−d_E²`, the block-diagonal state-space dimension minus `d_E²−1`, independent of `n`.

**C.19 (Bell counit: conditional trace preservation and the generic defect).** For first-order
`E=ℂ^d`, take `τ_0=I_E/d`; then `C_{τ_0}(f)=C(f)/d` and the typed counit is `d·ev`. It is CP and
trace-preserving on the admissible slice: for a channel `f` and any state `τ`,
`tr[d·ev((C(f)/d)⊗τ)]=tr f(τ)=1`. It is not trace-preserving on the full tensor-product state
space.

> **Proposition C.19 (generic off-slice trace defect).** For any nonzero finite-dimensional `B`, any
> trace-one positive `X` on `E^*⊗B`, and any state `τ` on `E`,
> `tr[d·ev(X⊗τ)]=d·tr[(Tr_B X)^T τ]`. This equals `1` for every such `X` iff `τ=I_E/d`.
> If `τ≠I_E/d`, the trace-preserving `X` lie in a proper affine hyperplane; the defect is generic
> relative to the full trace-one state space.

*Proof.* The Bell contraction formula gives the equality. If its affine functional were constant on
all trace-one Hermitian `X`, duality would force
`d(τ^T⊗I_B)=I_{E^*⊗B}`, hence `τ=I_E/d`; the converse is immediate. Otherwise its level set at `1`
is a proper affine hyperplane. Positive-definite trace-one operators form a relative open set, so the
complement of that hyperplane is generic. ∎

*Exact instance.* For `d=2`, `B=ℂ`, `τ=diag(3/5,2/5)`, and
`X=diag(17/40,23/40)`, the output trace is
`2[(17/40)(3/5)+(23/40)(2/5)]=97/100`. The defect is therefore not merely a boundary effect.

*Finite checks:* L17 checks admissible-slice traces and random off-slice examples; L24 independently checks
the displayed trace functional on exact product-state witnesses for `d=2,…,7`.

*Relation to `Caus`.* C.24 proves a balanced affine-slice companion inside `Caus[CPM(FHilb)]` and
states the flatness limitation explicitly; maximality and equivalence beyond that balanced subcategory
remain open.

### C.20 The completed extreme-set dimension route for `Instr_cg` (A4)

> **Proposition C.20.** Let `A,B` be finite-dimensional, with dimensions `a,b≥1`. In the
> finite- or countably-supported `Instr_cg` model, the set of extreme instruments in `Hom_cg(A,B)` is
> semialgebraic and has real dimension
> `a²(a²b²−1)`.

*Proof.* By C.7, an extreme instrument has support on `k≤a²` distinct rays with linearly independent
marginals. Lift the `k` components to an ordered tuple of Choi matrices. The normalization affine
space
`\mathcal A_k={ (J_1,…,J_k) : Σ_i Tr_B J_i=I_A }`
has dimension `k a²b²−a²`, because the partial-trace map onto `Herm(A)` is surjective. Positivity and
marginal independence are semialgebraic conditions; the distinct-ray condition is also semialgebraic.
Passing from ordered tuples to the unordered instrument is a quotient by the finite permutation group
`S_k`, which preserves semialgebraic dimension. Thus the `k`-component extreme stratum has dimension
at most `k a²b²−a²`.

For `k=a²`, this upper bound is attained on a relatively open subset. Choose a real basis
`H_1,…,H_{a²−1}` of traceless Hermitian operators on `A`, and for sufficiently small `δ>0` put
`v_i=I_A/a²+δH_i` for `i<a²` and
`v_{a²}=I_A/a²−δΣ_{i<a²}H_i`. These effects are positive definite and sum to `I_A`. They are linearly
independent: taking traces in `Σ_i c_i v_i=0` gives `Σ_i c_i=0`, and the traceless part then gives
`c_i=c_{a²}` for all `i<a²`, hence every coefficient is zero. With a full-rank state `σ` on `B`, the
Choi matrices `J_i=v_i^T⊗σ` are positive definite, have these independent marginals, and satisfy the
normalization equation. Positivity and independence persist in a neighborhood inside `\mathcal A_{a²}`.
The top stratum therefore has dimension
`a²·a²b²−a²=a²(a²b²−1)`. Since this increases with `k`, no lower stratum is larger. A finite-to-one
semialgebraic map preserves dimension (cell decomposition: its generic fibre has dimension zero),
so the unordered extreme set has the same dimension. ∎

*Finite checks:* L20a gives explicit positive definite TP tuples with independent marginals for small
`a,b`; L20b checks the dimension formula and monotonicity; L20c checks the finite-counit square gap and
two-slice incompatibility on a finite integer range. The general conclusions follow from the proof above.

> **Corollary (A4, finite-counit consequence).** Suppose `E,B,R` are finite-dimensional and a
> pointwise `Instr_cg` representation at `B` has a finite-outcome counit. Then no such representation
> exists for `d_E≥2`.

*Proof.* On extreme sets, the inverse adjunction map is piecewise semialgebraic: an extreme input at
`A` has at most `a²` support rays by C.7, and composing those with the finitely many counit components
produces finitely many zero/proportionality patterns; on each pattern, composition and ray
normalization are semialgebraic. It is bijective, so it preserves semialgebraic dimension. Taking
`A=ℂ` gives
`r²−1=d_E²(d_E²d_B²−1)`, hence
`r²=d_E⁴d_B²−d_E²+1`. For `e=d_E≥2,b=d_B≥1`,
`(e²b−1)² < e⁴b²−e²+1 < (e²b)²`, with gaps `e²(2b−1)>0` and `e²−1>0`. This is not a square.

Alternatively, use `A=ℂ` and `A=ℂ²`: equating the dimensions from C.20 gives
`a²r²−1=a²e⁴b²−e²` for `a=1,2`; subtracting four times the first equation from the second forces
`e²=1`. ∎

*Adjudication of the source route.* The first `Instr_cg` dimension proof (source A4, lines 29–38) was an
unfinished semialgebraic argument, not a false theorem. Its missing strata/quotient bookkeeping is
now supplied above. The one-slice square gap **does apply at `B=ℂ`**; the source explicitly notes this
at line 37, so the earlier audit's claim that A4 was blind at `B=ℂ` was incorrect and is corrected
here. This route is a finite-dimensional, finite-counit companion; it is not used for countably
infinite counits or infinite-dimensional `R`. The quadrilateral C.8 remains the stronger proof and
covers arbitrary `R` and countably supported outcomes.

---

### C.21 The dimension-1/2 face invariant for isometric channels

> **Proposition C.21.** Let `E` be finite-dimensional with `d_E≥2` and `B` a Hilbert space with
> `dim B≥d_E`. There are two isometric channels `Ad_U,Ad_V:E→B` whose minimal common channel face
> has affine dimension `1` if `d_E≥3`, and dimension `2` if `d_E=2`. Consequently `Chan(E,B)` is not
> affinely isomorphic to the normal state space of any Hilbert space.

*Proof.* Fix an isometric embedding `U:E→B` and a unitary `W` on `E` with `V=UW`. If `d_E=2`,
choose `W` nonscalar with two distinct eigenvalues. If `d_E≥3`, choose `W` with at least three
distinct eigenvalues. The channels have rank-one Choi operators `|U⟩⟩⟨⟨U|` and
`|V⟩⟩⟨⟨V|`. Let `S=span{|U⟩⟩,|V⟩⟩`. The set
`F_S={J≥0: Tr_B J=I_E, ran J⊂S}` is a face: if a convex combination of positive Choi matrices is
supported in `S`, each summand is supported in `S`. The midpoint of the two channel Choi matrices is
positive definite on `S`, so `F_S` is the minimal face containing both. (Indeed, for any `J∈F_S`, a
small `t>0` makes `J_0−tJ≥0` on `S`; then `J_0=tJ+(1−t)(J_0−tJ)/(1−t)` with both summands in
`F_S`.)

Every Hermitian Choi matrix supported in `S` is uniquely represented by
`C=[[a,z],[z̄,b]]`. After transposing the trace-preserving equation if needed to match the vectorization
convention, it is
`(a+b)I_E+zW+z̄W†=I_E`.
For an eigenvalue `λ` of `W`, this requires `2 Re(zλ)` to have the same value for every eigenvalue.
A line intersects the unit circle in at most two points, so if `W` has at least three distinct
eigenvalues then `z=0`, `a+b=1`; positivity leaves a line segment, of dimension `1`.
If `W` has exactly two distinct eigenvalues, equality at those two points is one nontrivial real
linear constraint on `z∈ℂ`; then `a+b` is determined and one independent real parameter remains in
`a,b`. At `C=diag(1/2,1/2)` positivity is strict, so the positive face has full affine dimension `2`.

Finally, every finite-dimensional face of the normal state space of `B(H_R)` has dimension `k²−1`
for some finite rank `k`. Let `ρ` be a relative-interior state of such a face. If `ρ` had infinitely
many nonzero eigenvalues, each corresponding rank-one spectral state would belong to the face, giving
arbitrarily large affinely independent subsets; hence `ρ` has finite rank `k`. Relative interior then
implies every state in the face is supported on `supp ρ`: for any `σ` in the face, a small `t>0`
allows `ρ=tσ+(1−t)τ` with `τ` in the face, so positivity forces `supp σ⊂supp ρ`. Conversely, since
`ρ` is positive definite on its finite-dimensional support, every state supported there occurs with
positive weight in a convex decomposition of `ρ`; faciality places it in the face. The face is exactly
the full state space on `supp ρ`, of dimension `k²−1`. Thus no such face has dimension `1` or `2`.
An affine bijection preserves faces and their affine dimensions, proving the non-isomorphism. ∎

*Exact finite checks:* L21a computes the support-slice ranks for `d_E=2,…,7` using exact arithmetic;
L21b checks the missing `1`-/`2`-dimensional face values against the finite-rank state-face formula.
The all-dimension conclusion uses the analytic eigenvalue and face arguments above.

*Scope note.* The isometric-channel construction requires `dim B≥d_E`; it does not address `d_B<d_E`.
For finite `E,B` in that complementary range, C.2 already proves the no-state-space theorem. The
block-family calculation below strengthens the face-dimension statement to every finite `d_E,d_B≥2`.

### C.22 A two-dimensional face for every finite `d_E,d_B≥2`

> **Proposition C.22.** Let `E,B` be finite-dimensional with `d_E,d_B≥2`. The channel set `Chan(E,B)`
> has a face of affine dimension exactly `2`. This assertion is independent of separability of a
> candidate state-space register and is a standalone structural fact about channel faces.

*Proof.* Choose a two-dimensional output subspace with orthonormal basis `u_0,u_1`. Split
`E=E_1⊕\bigoplus_{j=2}^{d_E−1}ℂe_j`, where `E_1=span(e_0,e_1)`, and let `v=(u_0+u_1)/√2`.
Consider the Kraus operators
`L_0=V_1P_1`, `L'_0=V_1D P_1`, `L_j=|v⟩⟨e_j|`, where `V_1e_a=u_a` and `D=diag(i,1)`.
For `d_E=2` the singleton family is absent. The two channels defined by `{L_0,L_j}` and
`{L'_0,L_j}` are trace-preserving. The combined Kraus family
`Q=(L_0,L'_0,L_2,…,L_{d_E−1})` is linearly independent, so the midpoint Choi matrix has support
`S=span Q` and is positive definite on `S`.

Let `F_S` be the face of channels whose Choi matrices are supported in `S`; it is a face because a
positive sum supported in `S` has each positive summand supported in `S`. The midpoint `J_0` is
positive definite on `S`. For every `J∈F_S`, a sufficiently small `t>0` gives `J_0−tJ≥0`, and
`J_0=tJ+(1−t)(J_0−tJ)/(1−t)` with both terms in `F_S`. Thus `J_0` is in the relative interior of
`F_S`; any face containing the two endpoint channels contains `J_0` and, by faciality, every such
`J`. Hence `F_S` is their minimal face. In coefficient coordinates its affine hull is `T(C)=I_E`, where
`T:Herm_{d_E}(ℂ)→Herm(E)`, `C↦Σ_{p,q}C_{pq}Q_q†Q_p`; therefore its dimension is the real nullity
of `T`.

Write `n=d_E−2`. On the `E_1` diagonal block, the four real entries of the Hermitian coefficient
block map to a diagonal matrix with entries `a+b+2 Re(i z)` and `a+b+2 Re(z)`. This map has rank
`2`, so its kernel has dimension `2`. For each singleton `E_j`, the cross-block coefficient pair
with `L_0,L'_0` maps to the two complex row vectors proportional to `(1,1)` and `(−i,1)`; these are
linearly independent, so the real map onto the `E_1↔E_j` block is an isomorphism and has no kernel.
For two distinct singleton blocks, the unique nonzero product is the corresponding matrix unit, so
those off-diagonal coefficient blocks are also injective; each singleton diagonal coefficient maps to
its own diagonal matrix unit. These blocks occupy disjoint matrix positions, so their ranks add:
`rank T=2+4n+n²=d_E²−2`. Since `dim_ℝ Herm_{d_E}=d_E²`, it follows that `dim ker T=2`.
The midpoint coefficient matrix is positive definite on `S`, so the positive trace-preserving slice
has this full affine dimension. ∎

*Exact finite checks:* L22a verifies trace preservation of both endpoints and full rank of the combined
Kraus family; L22b computes the real rank of `T` exactly for `d_E=2,…,7` and `d_B∈{2,3,5}`, including
pairs with `d_B<d_E`. These examples corroborate, but do not replace, the blockwise rank proof.

*Consequence.* Together, C.2 and C.22 rederive the non-separable finite-dimensional `Chan` result
(source note Thm 6) without relying on its numerical face-dimension claim: C.22 gives the face invariant;
C.2 supplies a separate full affine-isomorphism obstruction. The source's alternative face counts for
infinite-dimensional `E` are not asserted here.

### C.23 Finitary dyadic merging with countably many counit outcomes

> **Theorem C.23.** In the finitary dyadic quotient `D` of C.12, with countably supported outcomes,
> no pointwise representing object exists if `E` is finite-dimensional with `d_E≥2`, for any Hilbert
> spaces `B,R` and any countable counit. *(§7.2(2), the finite-input part of the `Instr_D` countable-
> counit gap: closed.)*

*Proof for `dim B≥2`.* Suppose there is a representation and apply record forgetting to its counit.
The induced processor `T:State(R)→Chan(E,B)` is onto. Use the continuum of extreme channels `f_θ`
from C.5, all with output in a fixed two-dimensional `B_0⊂B`. For each `θ`, choose a preimage
`g_θ={ρ_i}` of the target singleton instrument. Since its total output `f_θ` is extreme, every
normalized nonzero source outcome `ρ_i/trρ_i` also programs `f_θ`; choose one such outcome and a pure
spectral component `ψ_θ` of it. Extremality makes `ψ_θ` program `f_θ` as well. The target singleton
instrument has finite support, so Lemma C.14(a) says this source outcome and its pure spectral
components, including `ψ_θ`, are supported on a finite set `J_θ` of counit outcomes. There are only countably many finite subsets of a countable outcome set;
therefore an uncountable subfamily has a common `J`. The overlap calculation in C.5, which is valid for
any program Hilbert space, makes these `ψ_θ` pairwise orthogonal.

Let `W` be their closed linear span. Each individual counit response to `ψ_θ` is a positive CP
summand of `f_θ`, hence has output in `B_0`; the same holds for all Hermitian cross terms by
polarization. Lemma C.14(b), restricted to `W` and the common `J`, gives
`(dim W)²≤|J|d_E²(dim B_0)²<∞`. This contradicts the uncountable orthonormal family.

*Proof for `B=ℂ`.* Identify a finite-outcome scalar instrument with its effects. Let `E_1` be a
2-dimensional subspace of `E`; for `θ∈(0,π/2)` set
`p_θ=cosθ e_0+sinθ e_1`, `q_θ=−sinθ e_0+cosθ e_1`, and
`P_θ=|p_θ⟩⟨p_θ|`, `Q_θ=|q_θ⟩⟨q_θ|`. If `d_E>2`, put `R_0=I_E-P_{E_1}`. The recorded measurement
`f_θ` has effects `P_θ,Q_θ` (and `R_0` when `d_E>2`). Their marginals are linearly independent, so
`f_θ` is extreme in the real coarse-graining category by C.7. Forgetting dyadic labels sends a
countably-supported `D` instrument to its measure on CP rays; this map is compatible with composition
and sums proportional components, and its image lies in `Instr_cg`.

Let `g_θ` be a `D`-preimage, represented by source outcomes `{ρ_a}` with
`τ_a=tr ρ_a` and `Σ_a τ_a=1`. After the ray-measure map, the output is the countable convex
combination `Σ_a τ_a ν_{θ,a}`, where `ν_{θ,a}` is the response to the normalized (possibly mixed)
program state `ω_{θ,a}=ρ_a/τ_a`; this is affine over the separate source outcomes because composition
is componentwise and the ray measure is homogeneous under positive scaling. Since `f_θ` is extreme in
`Instr_cg`, every positive-weight `ν_{θ,a}` equals `f_θ` (otherwise isolating a positive-weight term
gives a nontrivial binary convex decomposition). Choose one such state and call it `ω_θ`; write `ν_θ` for its response, so
`ν_θ=f_θ`. Lemma C.14(a) gives a finite counit-outcome support
`J_θ` for the underlying source component; normalization by its positive trace does not change which
counit outcomes vanish. For each `j∈J_θ`, its scalar response effect is zero or lies on one
of the target rays `P_θ,Q_θ` (and `R_0` when present). Record this type assignment. By countability,
pass to an uncountable subfamily with common `J` and the same assignment; there are only finitely
many assignments for each finite `J`.

For each counit outcome let `M_j=ε_j^*(1)` be its effect on `R⊗E`. Let `J_P⊆J` be the fixed
outcomes assigned to the `P` ray and set `M=Σ_{j∈J_P}M_j`. This is a single effect, `0≤M≤I`,
independent of `θ`; it is used only as an operator effect, without asserting an arbitrary outcome
merge in `D`. For a state `ω` on `R`, write `M[ω]` for the effect on `E` determined by
`tr(σ M[ω])=tr[(ω⊗σ)M]`. The ray-measure equality `ν_θ=f_θ` gives
`M[ω_θ]=P_θ`.

Write a spectral decomposition `ω_θ=Σ_n p_n|ψ_{θ,n}⟩⟨ψ_{θ,n}|`. Then
`P_θ=Σ_n p_n M[|ψ_{θ,n}⟩⟨ψ_{θ,n}|]`, a convex combination of effects. A projection is an extreme
point of the effect interval: if `P=Σ_n p_n A_n` with `0≤A_n≤I`, then the positive operators
`P(I-A_n)P` and `(I-P)A_n(I-P)` have weighted sum zero, so each is zero. Positivity then gives
`A_nP=P` and `A_n(I-P)=0`, hence `A_n=P`. Thus every spectral vector `ψ_{θ,n}`
has the same sharp-effect compression `P_θ`; choose one and call it `ψ_θ`.

For a fixed effect `M` and program embeddings `V_ψx=ψ⊗x`, a sharp compression
`V_ψ^*MV_ψ=P` implies `MV_ψ=V_ψP`. If another program `φ` has sharp compression `Q`, then
`⟨ψ,φ⟩P=V_ψ^*MV_φ=⟨ψ,φ⟩Q`; hence distinct projections force orthogonal program vectors. The
selected `P_θ` are distinct, so the `ψ_θ` are pairwise orthogonal. Lemma C.14(a) also puts every
selected spectral vector in the common support subspace `V_J`; because `V_J` is linear, their span
`W_0` lies in `V_J`. Lemma C.14(b), with scalar output, gives
`(dim W_0)²≤|J|d_E²`, contradicting the uncountable orthogonal family. ∎

*Finite algebra check:* L23 verifies the earlier scalar overlap-matrix identity for distinct exact
angle differences (and checks that the rank drops at equal angles). It is retained as an auxiliary
finite identity check; the proof above instead uses projection extremality and the sharp-effect
argument, and L23 does not support any infinite-dimensional conclusion.

*Scope boundary.* C.23 proves the finite-dimensional-input case and uses C.14(b) only in that finite
response setting. The infinite-dimensional-input/countable-counit case is closed separately by C.28;
no finite-dimensional response bound from C.14(b) is extended to infinite `E`.

### C.24 The balanced-slice comparison with `Caus[CPM(FHilb)]`

Work in finite-dimensional `FHilb`. For a set `S` of normalized positive states, write
`S^⊥={F≥0:tr(Fρ)=1 for every ρ∈S}` and
`S^{⊥⊥}={ρ≥0,trρ=1:tr(Fρ)=1 for every F∈S^⊥}`. The `Caus[CPM(FHilb)]` construction of [12]
uses closed state sets `S=S^{⊥⊥}` and flatness: invertible scalar multiples of the identity must lie
in the effect polar and the state set. For normalized finite-dimensional slices, this means
`I∈S^⊥` and `I/d∈S`. Call a typed slice **balanced** when `I_A/d_A∈S_A`.

> **Proposition C.24.** (a) Every balanced typed slice is closed and flat: `S_A=S_A^{⊥⊥}` and
> `I_A∈S_A^⊥`, `I_A/d_A∈S_A`. (b) If `S_A,S_B` are balanced, the `Caus` tensor state space
> `(S_A⊗S_B)^{⊥⊥}` equals `L_{AB}∩Pos_1(A⊗B)`, where
> `L_{AB}=aff{a⊗b:a∈L_A,b∈L_B}`. Thus the balanced typed subcategory is a symmetric monoidal full
> subcategory of `Caus[CPM(FHilb)]`. (c) An unbalanced affine slice is excluded by flatness: it
> contains no normalized scalar identity.

*Proof.* Let `ρ` be a trace-one positive operator outside `L_A`. Affine separation in the finite-
dimensional trace-one Hermitian space gives a Hermitian `H` and a real `c` such that
`tr(Hx)=c` for every `x∈L_A`, while `tr(Hρ)≠c`. For sufficiently small real `ε`,
`F=I_A+ε(H−cI_A)≥0`. Balance gives `tr(Fx)=1` for every `x∈S_A`, so `F∈S_A^⊥`, but
`tr(Fρ)≠1`. Thus `ρ∉S_A^{⊥⊥}`; the reverse inclusion `S_A⊂S_A^{⊥⊥}` is immediate. Also
`tr(I_Ax)=1` for every normalized `x`, and balance supplies `I_A/d_A∈S_A`, proving the stated
closedness and flatness conditions.

For the tensor statement, product states affinely span `L_{AB}`, and the product slice contains
`I_{AB}/(d_Ad_B)`. If `X∈L_{AB}∩Pos_1`, every effect in `(S_A⊗S_B)^⊥` has expectation one on
all product states and therefore, by affine linearity, on `L_{AB}`; hence
`X∈(S_A⊗S_B)^{⊥⊥}`. Conversely, if `X` lies outside `L_{AB}`, separate it by
`tr(Hx)=c` on `L_{AB}` with `tr(HX)≠c`. Then `I_{AB}+ε(H−cI_{AB})` is positive for small `ε`,
has expectation one on every product state, and excludes `X` from the double polar. This proves the
equality. Typed morphisms are exactly the CP maps preserving these state sets by C.15, so the balanced
slice category is full in the corresponding `Caus` subcategory and tensor-compatible. Finally,
flatness requires a scalar identity state; on a trace-one finite-dimensional slice this must be
`I_A/d_A`, which an unbalanced slice omits. ∎

*Structural limitation and companion result.* The flatness requirement excludes all unbalanced slices;
so C.24 is not an equivalence of the full typed category `𝒯` of C.15–C.16 with all of `Caus`. The
balanced tensor comparison is proved beyond first-order slices, including proper affine slices
containing `I/d`. Whether this balanced subcategory is maximal among all admissible typed slices, and
the full `𝒯`/`Caus` equivalence beyond it, remain open.

### C.25 Measurable outcomes: the ray-measure companion and remaining quotient issue

For finite-dimensional objects `A,B`, let `K(A,B)` be the compact set of positive Choi operators of
trace one. A **ray-measure instrument** is a finite positive Borel measure `μ` on `K(A,B)` satisfying
`∫ Tr_B(J)dμ(J)=I_A`. It forgets outcome labels but retains the distribution of normalized CP rays;
its total mass is `d_A`.

> **Proposition C.25.** (a) Every normal instrument with a standard-Borel outcome space determines a
> ray-measure instrument. Conversely every ray-measure instrument defines a standard-Borel
> measure-valued instrument. (b) These ray-measure instruments form a category under weighted
> pushforward composition. (c) In this category `Hom(ℂ,R)` is the set of Borel probability measures
> on `State(R)`, and the C.8 quadrilateral persists; hence `−⊗E` is not representable for
> `d_E≥2` (with objects, including `R`, finite-dimensional).

*Proof.* For a standard-Borel instrument `I`, its Choi-valued measure `M(S)=C(I(S))` takes values in
the finite-dimensional positive cone. Put `λ(S)=tr M(S)`; then `λ` is finite, and entrywise
Radon–Nikodym gives a measurable density `J(ω)≥0`, `tr J(ω)=1` for `λ`-almost every `ω`. The
pushforward `μ=J_*λ` satisfies the normalization equation and has mass
`tr I_A=d_A`. Conversely, given `μ`, define `M(S)=∫_S Jdμ`; the inverse Choi map is a CP-valued
measure and the displayed constraint makes its total map trace-preserving.

For composition, if normalized Choi rays `J,K` represent component maps `f_J,g_K`, form
`L=C(g_K∘f_J)` and omit pairs with `L=0`. Push the product measure forward under
`(J,K)↦L/tr L`, weighted by `tr L`. Bilinearity of composition shows that the resulting Choi
measure is the integral of `C(g_K∘f_J)`; the two normalization equations make its total map a
channel. Associativity follows from associativity of CP-map composition and Fubini. The identity at
`A` is the measure `d_A·δ_{C(id_A)/d_A}` (not a unit-mass Dirac measure), which acts as an identity
because the normalized Choi representative corresponds to the subchannel `id_A/d_A`.

At `A=ℂ`, the normalization equation says precisely that `μ` is a probability measure on `State(B)`.
The four finite ray-measures and their two distinct decompositions in C.8 remain valid. If one of the
four were decomposable using arbitrary Borel measures, the summands would be absolutely continuous
with respect to its finite-support measure and hence supported on the same finite set; the independent
marginals of C.7 force the decomposition to be trivial. Thus those four target instruments remain
extreme. In the source, the extreme points of the full Borel probability-measure set on `State(R)` are
exactly the Dirac measures: any non-Dirac measure splits over a Borel set of mass strictly between
zero and one. A representing hom-set bijection is affine because composition is bi-affine, so it would
pull the C.8 equality back to an equality of probability measures on `State(R)` with different finite
supports, a contradiction. ∎

*Residual.* C.25 proves a precise finite-dimensional measurable-ray companion. It does **not** prove
that every intended quotient of arbitrary labelled standard-Borel instruments is equivalent to this
ray-measure category; that identification, including the chosen label-isomorphisms and measurable
disintegration, remains open. The result also does not cover non-finite-dimensional objects in this
measure model.

### C.26 A non-separable lookup-table processor (not a representation)

> **Proposition C.26.** For any fixed nonzero Hilbert spaces `E,B` and their set `Chan(E,B)` of normal
> channels, there is a (possibly non-separable) Hilbert register `R` and a normal channel
> `ε:R⊗E→B` such that every channel in the hom-set is a program slice
> `ε(|f⟩⟨f|⊗−)`. The processor is not injective on normal program states whenever the hom-set
> contains two distinct channels.

*Proof.* Let `\mathcal C=Chan(E,B)` and take `R=ℓ²(\mathcal C)` with orthonormal basis `|f⟩`. Define
`ε(X)=Σ_{f∈\mathcal C} f(⟨f|X|f⟩)`. For positive trace-class `X`, only countably many diagonal
blocks are nonzero and their traces sum to `tr X`; the series converges in trace norm. Its
Heisenberg adjoint is the block-diagonal map `ε^*(Y)=⊕_{f∈\mathcal C} f^*(Y)`, a normal unital CP
map, so `ε` is normal CP. Also
`tr ε(X)=Σ_f tr⟨f|X|f⟩=tr X`: it is a channel. Its basis program `|f⟩⟨f|` yields `f`.

If `f≠g`, the pure superposition
`|+⟩=(|f⟩+|g⟩)/√2` and the mixed program
`ρ=(|f⟩⟨f|+|g⟩⟨g|)/2` have the same diagonal blocks, hence the same processor output
`(f+g)/2`, while `|+⟩⟨+|≠ρ`. Thus the processor is not injective. ∎

*Limitation.* This is only a surjective processor. It supplies neither injectivity nor a natural
hom-set bijection, so it does not establish representability for a non-separable register. L26 checks a
finite-dimensional controlled-channel instance and its non-injectivity; the proof above is the general
normal-channel construction.

### C.27 Residual-gap ledger (R1 closed by C.28; remaining gaps kept visible in §7.2)

* **R1 — closed by C.28.** Finitary dyadic `D` with `dim E=∞`, a countable counit, and arbitrary
  `R` is now non-representable for every nonzero `B`, including `B=ℂ` and `dim B≥2`. The earlier
  finite-response/retract routes did not settle this case; C.28 uses a coefficient-algebra collision
  and does not extend C.14(b) or assume split idempotents.
* **R2** The intended quotient for arbitrary standard-Borel labelled outcomes has not been identified
  with the explicit ray-measure category C.25. C.25 proves the companion no-go but does not settle that
  definitional/equivalence gap; non-finite-dimensional objects remain outside its construction.
* **R3** Non-normal states: the current category definitions are normal/trace-class; C.10 and the other
  finite-input theorems do not define or settle the non-normal C*-algebraic setting.
* **R4** The non-separable infinite-dimensional overlap sketch in the source note (lines 618–629) is
  conditional on separability or finite dimension of the program register; the orthogonal-family
  contradiction alone does not exclude non-separable registers. C.26 shows why surjective processors
  do not repair this gap.
* **R5** `𝒯` versus `Caus[CPM(FHilb)]`: C.24 proves the balanced typed-slice companion and identifies
  the flatness limitation; maximality/equivalence outside that subcategory remain open.
* **R6** Formal proof-assistant verification of the analytic/category-level results remains future work;
  the finite arithmetic, exact examples, and linear-algebra checks are recorded in `verification/`.

### C.28 R1 closure: infinite input and countable counit in finitary `Instr_D`

> **Theorem C.28.** Let `E` be infinite-dimensional with `λ=dim E`, let `B` be nonzero, and use
> normal maps in the finitary dyadic instrument category `D` with finite or countably supported
> outcomes. For every Hilbert space `R`, no pointwise representation of
> `Hom_D(−⊗E,B)` exists in this countably supported model (every proposed counit has at most
> countably many nonzero outcomes). This covers `B=ℂ` and every `dim B≥2`, with separable or
> non-separable `R`. *(§7.2 R1: closed.)*

*Proof.* If `R=0`, no trace-preserving counit to nonzero `B` exists, so assume `R≠0`. Suppose a
representation exists, and choose a representative of its counit
`ε={ε_j}_{j∈J}:R⊗E→B` with `|J|≤ℵ₀`. Its total map `\bar ε=Σ_j ε_j` is a normal channel. We
construct a closed subspace `K⊂R` with `dim K>λ` such that every counit outcome, when restricted
to `K⊗E`, has output supported in one fixed finite-dimensional space `B_0` (take `B_0=ℂ` if
`B=ℂ`, and `dim B_0=2` otherwise). We then show that the coefficient algebra of this restricted
counit has a nontrivial commutant, producing two distinct arrows in
`Hom_D(R,R)` with the same image under the representing map at `A=R`.

**Case 1: `dim B≥2`.** Fix `B_0⊂B` with dimension two and orthonormal basis `(b_0,b_1)`, and
choose a set `I` of cardinality `λ`. Write `E=⊕_{i∈I}E_i` with `dim E_i=2`, choose bases
`(e_{i,0},e_{i,1})` for the blocks, and let `P_i` be the block projections. Fix unitary maps
`u_i:E_i→B_0` with `u_ie_{i,k}=b_k`. For `s=(s_i)_{i∈I}∈{−1,+1}^I`, let
`D_{i,s}=diag(s_i,1)` in these bases. Define
`K_i^s=u_iD_{i,s}P_i` and the Stinespring isometry
`V_sx=Σ_i K_i^sx⊗δ_i:E→B_0⊗ℓ²(I)`, with the complete orthonormal environment basis
`{δ_i}`. The vector sum is well-defined for all `x`, since `Σ_i||P_ix||²=||x||²`. Set
`f_s(X)=Tr_{ℓ²(I)}(V_sXV_s^*)=Σ_{i∈I}K_i^sXK_i^{s*}`. Thus `f_s` is a normal channel with
output supported in `B_0`. The dilation is minimal: for each `i`, the map `K_i^s`
onto `B_0` shows that the environment vector `δ_i` lies in the Stinespring span.

These channels are distinct because, for basis vectors `e_{i,0},e_{i,1}` of `E_i`,
`f_s(|e_{i,0}⟩⟨e_{i,1}|)=s_i|b_0⟩⟨b_1|`. They are extreme in `Chan(E,B_0)`. Indeed, if
`f_s=t Φ_1+(1−t)Φ_2`, `0<t<1`, the normal CP Radon–Nikodym theorem on the minimal dilation
`V_s` gives `0≤D≤I` on `ℓ²(I)` with
`V_s^*(I_{B_0}⊗D)V_s=tI_E`. The `(i,j)` block of this equation is the matrix entry `D_{ij}`
times `K_i^{s*}K_j^s`. For `i≠j`, this product is a nonzero map supported only from `E_j` to
`E_i`, so `D_{ij}=0`; for `i=j`, `K_i^{s*}K_i^s=P_i`, so `D_{ii}=t`. Since `{δ_i}` is a
complete basis, `D=tI`; the decomposition is trivial. A positive summand of a channel whose output
is supported in `B_0` also has output supported in `B_0`, so extremality holds in `Chan(E,B)` as
well as `Chan(E,B_0)`.

At `A=ℂ`, surjectivity supplies a `D`-preimage `g_s={ρ_a}` for every singleton target `f_s`. Its
total program state `ρ_s=Σ_aρ_a` is a normal density operator with trace one, and total-map
preservation gives `\bar ε(ρ_s⊗−)=f_s`. Because `\bar ε` is affine in that state and `f_s` is
extreme, every pure spectral component also programs `f_s`. Choose one unit vector `ψ_s` for each
`s`. Let `W:R⊗E→B⊗G` be a Stinespring isometry of `\bar ε`. The restriction
`W_sx=W(ψ_s⊗x)` is a dilation of `f_s`, with range in `B_0⊗G`. By minimality and Stinespring
uniqueness, `W_s=(I_{B_0}⊗J_s)V_s` for an isometry `J_s:ℓ²(I)→G`. For `s,t`, put
`Γ_{st}=J_s^*J_t`, a contraction. The common isometry gives the cross-dilation identity

`⟨ψ_s,ψ_t⟩I_E = V_s^*(I_{B_0}⊗Γ_{st})V_t`.

If `s_i≠t_i`, compression to `E_i` is
`⟨ψ_s,ψ_t⟩I_{E_i}=⟨δ_i,Γ_{st}δ_i⟩diag(−1,1)`, which forces
`⟨ψ_s,ψ_t⟩=0`. Hence the `2^λ` programs are orthogonal. This use of Stinespring theory compares
minimal dilations embedded in one processor environment through the cross-Gram contraction; it
does not apply a Kraus identity to arbitrary incomplete families.

For each counit component `ε_j`, choose a Stinespring contraction
`W_j:R⊗E→B⊗G_j`. For every selected `ψ_s` and `x∈E`, the positive output
`ε_j(|ψ_s⊗x⟩⟨ψ_s⊗x|)` is a positive summand of `f_s(|x⟩⟨x|)`, whose support lies in `B_0`.
Thus `W_j(ψ_s⊗x)∈B_0⊗G_j` (a vector whose partial trace is supported in `B_0` lies in
`B_0⊗G_j`). By linearity, boundedness, and closedness of `B_0⊗G_j`,
`W_j(K⊗E)⊂B_0⊗G_j` for `K=\overline{span}{ψ_s}`. So every restricted counit outcome has
output in this same two-dimensional `B_0`, and `dim K≥2^λ>λ`.

**Case 2: `B=ℂ`.** Fix an orthonormal basis `(e_i)_{i∈I}` of `E`, where `|I|=λ`. For each
nonempty proper subset `S⊂I`, let `P_S` be the diagonal projection onto `ℓ²(S)` and
`Q_S=I_E−P_S`. The two-outcome PVM `f_S={P_S,Q_S}` is a finite `D` instrument. Choose one `S`
from each complementary pair; this gives `2^λ` distinct unordered instruments, because their ray
supports agree only when the subsets agree or are complements. Apply the ray-measure map described
in C.23, which is well-defined under the finitary dyadic splits/merges and compatible with
composition. The ray-measure image of `f_S` is extreme in `Instr_cg(E,ℂ)`: positivity restricts any
convex decomposition to its two rays. Writing `a,b` for their effective coefficients as effects, the
normalization equation `aP_S+bQ_S=I_E` forces `a=b=1`. Thus every normalized component has the same
two-atom ray measure.

Let `g_S={ρ_a}` be a `D`-preimage at `A=ℂ`, and set `τ_a=trρ_a`. The ray-measure image of the
composite is the countable convex combination `Σ_a τ_a ν_{S,a}`, where `ν_{S,a}` is the response
to the normalized (possibly mixed) source state `ω_{S,a}=ρ_a/τ_a`; this decomposition is over the
separate source outcomes, using componentwise composition and homogeneous ray weights. Extremality
forces every
positive-weight `ν_{S,a}` to equal `f_S` (otherwise isolating one positive-weight term gives a
nontrivial binary convex decomposition); choose one and call its normalized state `ω_S`.
Lemma C.14(a) gives a finite counit support `J_S` for the underlying source component; dividing
by its positive trace leaves the zero outcomes unchanged. For each `j∈J_S`,
the scalar response is zero or lies on the `P_S` or `Q_S` ray. There are only countably many
finite counit subsets and finitely many such assignments for each subset. Since there are `2^λ`
targets and `2^λ>λ`, one cell of this countable partition contains a subfamily of size greater
than `λ` (otherwise the countable union would have size at most `λ`). On that cell, the set
`J_P⊂J` of outcomes assigned to the `P` ray is fixed.

Write `M_j=ε_j^*(1)` for the counit effects on `R⊗E`, and set
`M=Σ_{j∈J_P}M_j`. This is one fixed effect, `0≤M≤I`; it is used only as an operator effect, not
as an asserted `D`-outcome merge. For a program state `ω`, let `M[ω]` be the effect on `E` defined by
`tr(σM[ω])=tr[(ω⊗σ)M]`. The ray-measure response of `ω_S` is exactly `f_S`; under the
total-effect map,
its P-ray components sum to `P_S`, hence `M[ω_S]=P_S`. If `ω_S=Σ_n p_n|ψ_{S,n}⟩⟨ψ_{S,n}|`, then
`P_S=Σ_n p_n M[|ψ_{S,n}⟩⟨ψ_{S,n}|]`, a convex combination of effects. A projection is extreme
in `[0,I]`: if `P=Σ_n p_n A_n`, `0≤A_n≤I`, then `P(I−A_n)P` and `(I−P)A_n(I−P)` are
positive with weighted sum zero. Each vanishes, so positivity gives `A_nP=P` and `A_n(I−P)=0`,
hence `A_n=P`. Choose one spectral vector and denote it `ψ_S`.

For one fixed effect `M`, if program embeddings `V_ψx=ψ⊗x` and `V_φx=φ⊗x` have sharp
compressions `V_ψ^*MV_ψ=P` and `V_φ^*MV_φ=Q`, then, because `0≤M≤I`,
`MV_ψ=V_ψP` and `MV_φ=V_φQ`: the complementary effect has zero expectation on `ran P`, and `M`
has zero expectation on `ker P` (and likewise for `Q`). Therefore
`⟨ψ,φ⟩P=V_ψ^*MV_φ=⟨ψ,φ⟩Q`. Distinct projections force orthogonal programs. The selected
`P_S` are distinct, so this subfamily yields more than `λ` orthogonal vectors. Let `K` be their
closed span; `dim K>λ`. The scalar-output counit is already supported in `B_0=ℂ` on this `K`.

**Common coefficient-algebra collision.** In either case let `i:K↪R` be inclusion and write
`η_j=ε_j∘(i⊗id_E):K⊗E→B_0`. Fix an orthonormal basis `(e_α)_{α∈I}` of `E`, and a basis
`(b_r)_{r=1}^{d_0}` of `B_0`, where `d_0≤2`. For every outcome `j`, output matrix unit
`|b_r⟩⟨b_s|`, and input-basis pair `(α,β)`, form the slice

`X_{j,rs,αβ}=(I_K⊗⟨e_α|)η_j^*(|b_r⟩⟨b_s|)(I_K⊗|e_β⟩)∈B(K)`.

There are at most `ℵ₀ d_0² λ²=λ` such operators, since `λ` is infinite and `λ²=λ`. The unital
C*-algebra `𝒜⊂B(K)` they generate
has norm density at most `λ` (rational complex polynomials in a generating set of size `λ` are
dense). It cannot act irreducibly on `K`: if it did, any nonzero `ξ∈K` would be cyclic, and a
dense subset of `𝒜` of size at most `λ` would make `𝒜ξ` dense in `K`, contradicting
`dim K>λ` (the density character of an infinite-dimensional Hilbert space equals its Hilbert
dimension). Thus `𝒜` has a nontrivial reducing subspace, with projection `Q_K∈𝒜'`. Put
`U=I_K−2Q_K`, a nonscalar unitary. Since `U` commutes with every slice, every E-basis matrix
coefficient of `[U⊗I_E,η_j^*(Y)]` is zero; the complete input basis and finite output matrix units
therefore give `[U⊗I_E,η_j^*(Y)]=0` for every `j` and `Y∈B(B_0)`. Hence
`η_j∘(Ad_U⊗id_E)=η_j` for every counit outcome.

Choose a normal state `τ` on `K`, and define the normal channel `p:R→K` by
`p(ρ)=P_KρP_K+tr(P_{K^⊥}ρ)τ`. Let `h=i∘p` and `g=i∘Ad_U∘p`, both one-outcome normal channels
`R→R`. They are distinct: `p` is the identity on states supported in `K`, and the nonscalar `U` changes
some such state. The dyadic split/merge relation preserves the total map and cannot identify distinct
one-outcome channels. But for every `j`,

`ε_j∘(g⊗id_E)=η_j∘(Ad_U⊗id_E)∘(p⊗id_E)
=η_j∘(p⊗id_E)=ε_j∘(h⊗id_E)`.

Thus their composite counit instruments are componentwise equal, so the representing map at `A=R`
identifies `g` and `h`. This contradicts its injectivity. The contradiction is pointwise at the
fixed target `B`; no global categorical reduction or split-idempotent assumption is used. ∎

*Scope and verification boundary.* C.28 uses only C.14(a) in the scalar branch, not the finite-response
bound C.14(b). Its cardinal and C*-algebra arguments are analytic; the finite regression suite does
not constitute a formal proof of them.

### C.29 Pairwise deterministic overlap SDP and Gram-rank bound

Let `E,B,R` be finite-dimensional, let `P:B(E⊗R)→B(B)` be a fixed CPTP processor, and let `f,f'`
be channels `E→B` with minimal Kraus families `{K_i}_{i=1}^r` and `{K'_l}_{l=1}^{r'}`. Define
\[
\tau(f,f')=\max\left\{t\ge0:\ tI_E=\sum_{i,l}\Gamma_{il}K_i^\dagger K'_l,
\quad\|\Gamma\|_{\rm op}\le1\right\}.
\]

> **Proposition C.29.** The maximum is attained, `0≤τ(f,f')≤1`, and is invariant under unitary
> changes of the minimal Kraus bases. If pure unit program states `ψ,ψ'` implement `f,f'` under the
> same deterministic processor, then
> \[
> |\langle\psi|\psi'\rangle|\le\tau(f,f').
> \]
> If a target channel is extreme and is initially implemented by a mixed deterministic program, it
> has a pure-program preimage. Consequently, for a finite family `F` of extreme channels define
> \[
> r_\tau(F)=\min\{\operatorname{rank}G:\ G\succeq0,\ G_{ff}=1,
> |G_{ff'}|\le\tau(f,f')\ (f\ne f')\}.
> \]
> Every deterministic exact processor for `F` satisfies `dim R≥r_τ(F)`. For an infinite family,
> `dim R≥sup_{F_0⊂F, finite}r_τ(F_0)`.

*Proof.* Let `W:E⊗R→B⊗G` be a Stinespring isometry for `P`, and let `W_ψx=W(x⊗ψ)`. For a
program implementing `f`, minimality and Stinespring uniqueness give
`W_ψ=(I_B⊗J_ψ)V_f`, where `V_f:E→B⊗H_f` is the minimal Stinespring isometry and
`J_ψ:H_f→G` is an isometry; similarly for `f'`. The embeddings use the **same** processor
environment. Since `W` is an isometry,
\[
W_\psi^\dagger W_{\psi'}=\langle\psi|\psi'\rangle I_E.
\]
Put `Γ=J_ψ†J_ψ'`, a contraction. Expanding the left side using the minimal Kraus families yields
\[
\langle\psi|\psi'\rangle I_E=\sum_{i,l}\Gamma_{il}K_i^\dagger K'_l,
\]
so the program overlap (up to a phase) is feasible for `τ`.

The SDP is
\[
\begin{array}{ll}
\text{maximize}_{t\in\mathbb R,\Gamma\in\mathbb C^{r\times r'}}&t\\
\text{subject to}&\sum_{i,l}\Gamma_{il}K_i^\dagger K'_l=tI_E,\\
&\begin{pmatrix}I_r&\Gamma\\\Gamma^\dagger&I_{r'}\end{pmatrix}\succeq0,\qquad 0\le t\le1.
\end{array}
\]
The block LMI is equivalent to `||Γ||op≤1`; the complex matrix equality is a finite set of complex
linear equalities (or real/imaginary linear equalities after realification). Feasibility at `t=0`
and compactness of the contraction ball give attainment. The `t≤1` cap follows from
`||V_f†(I_B⊗Γ)V_f'||≤1`. Unitary changes of minimal Kraus coordinates are absorbed into `Γ`, so
`τ` is basis-independent. Also, `τ>0` iff `I_E` belongs to the complex linear span of the cross
products: if a coefficient matrix represents `I_E`, scale it down to a contraction to obtain a
positive feasible `t`.

For an extreme channel `f`, a mixed program `ρ=Σ_kp_k|ψ_k⟩⟨ψ_k|` gives
`f=Σ_kp_k P(·⊗|ψ_k⟩⟨ψ_k|)`, a convex decomposition into channels; every positive-weight component
therefore equals `f`. For a finite extreme family choose one such pure program per target. Its Gram
matrix is feasible in the definition of `r_τ`, and its rank is at most `dim R`. The infinite-family
statement follows by restriction to finite subfamilies. ∎

**Nonconvexity and scope.** The pairwise `τ` problem is an SDP. The minimum-rank Gram problem is
not: the entry bounds admit LMIs, but minimizing rank is nonconvex. The lower bound applies to
extreme target families because pure preimages then exist; it is not asserted for arbitrary
non-extreme targets or heralded processors. The condition `τ>0` is `I_E∈span{K_i†K'_l}`; a
universal count `rr'≥d_E²` is not necessary (identical unitary channels have `r=r'=1` and `τ=1`).
The matrix equality has `d_E²` complex coefficient constraints in a chosen basis. This count is
distinct from the affine codimension `d_E²−1` and is not a scalar cost invariant.

### C.30 Three extreme qubit targets: deterministic and heralded profile

Let `R_σ(X)=tr(X)|σ⟩⟨σ|`, `|0⟩=(1,0)^T`, and `|+⟩=(|0⟩+|1⟩)/√2`. Set
`F_mix={R_|0⟩,R_|+⟩,Ad_Z}`. The pure replacement channels are extreme: for
`K_i=|σ⟩⟨i|`, the products `K_i†K_j=|i⟩⟨j|` are linearly independent. `Ad_Z` is extreme as a
unitary channel.

The minimal Kraus products give
\[
\tau(R_\sigma,R_{\sigma'})=|\langle\sigma|\sigma'\rangle|,
\quad \tau(R_{|0\rangle},\operatorname{Ad}_Z)
=\tau(R_{|+\rangle},\operatorname{Ad}_Z)=0.
\]
For the replacer/unitary pair, each cross product is `|i⟩⟨σ|Z`, so their span consists of
rank-at-most-one matrices with a common row space and cannot contain a nonzero multiple of `I_2`.
Thus a feasible Gram matrix has the block form
\[
G=\begin{pmatrix}1&z&0\\\bar z&1&0\\0&0&1\end{pmatrix},\qquad |z|\le1/\sqrt2.
\]
The upper block has determinant at least `1/2`, hence rank two; `r_τ(F_mix)=3`. A qutrit program
with three orthogonal labels, measured before applying `Ad_Z`, `R_|0⟩`, or `R_|+⟩`, achieves the
deterministic bound. The related measure-and-prepare family of all pure qubit replacement channels
is programmable with a qubit: store `|σ⟩` and use a processor that discards the input and returns the
program state. Any family containing two distinct pure replacers needs dimension at least two, since
a one-dimensional program has only one state. The pure-replacer extremality check above is what
licenses deterministic pure-program arguments; mixed-output replacers are not covered by it.

For the heralded profile, use the model of §5.6. The three target Choi supports are
\[
S_{R_\sigma}=|\sigma\rangle\otimes E^*,\qquad
S_{\operatorname{Ad}_Z}=\operatorname{span}\{|Z\rangle\rangle\}.
\]
They have pairwise zero intersection: the output vectors `|0⟩,|+⟩` are not parallel, and the
unitary Choi vector is entangled whereas vectors in either fixed-output subspace are product. Suppose
a two-dimensional program register were sufficient with positive success on all three targets.
If any target program `ρ_f` had full rank, then any pure program vector could be peeled off with a
small positive weight; positivity and `L_s(ρ_f)=q_fJ_f` would force its success Choi support into
`S_f`. A nonzero pure component from another target's program would then have support in two
trivially intersecting Choi supports, impossible. Therefore all three program states must be pure.
Their rays are distinct. In dimension two, write
`|ψ_Z⟩=α|ψ_0⟩+β|ψ_+⟩` with `αβ≠0`.

Let `A_μ:E⊗R→B` be success Kraus operators. The restricted operators satisfy
`A_{μ,0}=|0⟩⟨v_{μ,0}|`, `A_{μ,+}=|+⟩⟨v_{μ,+}|`, and `A_{μ,Z}=c_μZ`, since each target success
Choi support constrains every Kraus vector. Linearity in the program gives
\[
c_\mu Z=\alpha|0\rangle\langle v_{\mu,0}|+\beta|+\rangle\langle v_{\mu,+}|.
\]
Use
\[
Z=|0\rangle(\langle0|+\langle1|)-\sqrt2|+\rangle\langle1|.
\]
Comparing coefficients in the output basis shows every `A_{μ,0}` is proportional to the same
rank-one operator. The success Choi matrix at `ψ_0` then has rank at most one, contradicting
`q_0J_{R_0}` having rank two. Dimension one is also impossible because it supplies the same success
map for distinct targets. The qutrit construction attains the lower bound, hence
\[
\boxed{\mathcal C_{F_{\rm mix}}(p)=\log_2 3\quad(0<p\le1).}
\]

**Warnings against invalid heralded reductions.** Channel extremality alone does not force the pure
components of a mixed heralded program to be scalar multiples of the target channel: the components
are only CP maps, not channels. For example, success Kraus operators
`A_0=|σ⟩⟨0_E,0_R|`, `A_1=|σ⟩⟨1_E,1_R|` yield `(1/2)R_σ` from program `I_R/2`, while the
pure program components yield non-scalar CP submaps. Also, the bound
`|⟨ψ|ψ'⟩|≤√(q_fq_f')τ(f,f')` is false in general: for `Id` and
`Ad_{exp(−iπZ/6)}`, `τ=0` but normalized Choi programs overlap by `√3/2`; the identity Bell branch
implements both with success `1/4`. A full heralded dilation retains the failure cross-term as in
§5.6. The Pauli-unitary special case in C.31 permits pure reduction for the stronger reason that
its target Choi matrices have rank one.

### C.31 Four Pauli unitary channels: heralded profile

Let `F_P={Ad_I,Ad_X,Ad_Y,Ad_Z}`. Distinct Pauli channels have `τ=0`, so the deterministic Gram
bound gives `dim R≥4`; a four-label controlled-Pauli processor attains equality at success one.
For heralded processors the lower bound requires a separate argument. If
`P_s(·⊗ρ_P)=q_PAd_P`, `q_P>0`, decompose `ρ_P=Σ_kp_k|ψ_k⟩⟨ψ_k|`. The Choi matrix of the
success map is a positive sum equal to the rank-one matrix `q_P|P⟩⟩⟨⟨P|`; every summand lies on
that same positive ray. Choose a component with nonzero success. For success Kraus operators `M_j`,
\[
M_j(I_E\otimes|\psi_P\rangle)=\alpha_{jP}P,
\]
with some `α_{jP}≠0` for each target. If the four selected program vectors had a nontrivial linear
relation `Σ_Pc_P|ψ_P⟩=0`, applying each `M_j(I_E⊗·)` would give
`Σ_Pc_Pα_{jP}P=0`. Linear independence of `I,X,Y,Z` forces `c_Pα_{jP}=0` for every `P,j`; choosing
one nonzero `α_{jP}` for each target forces all `c_P=0`. Thus four linearly independent program
vectors are necessary, so `dim R≥4` at every positive threshold. The deterministic construction
attains it:
\[
\boxed{\mathcal C_{F_P}(p)=2\text{ bits}\quad(0<p\le1).}
\]
This pure-component step is valid because each unitary Choi matrix is rank one, an extreme ray of
the CP cone; it is not valid for every extreme channel.

### C.32 Depolarizing pair: closed-form τ and profile

For `0<λ,μ<1`, use minimal Pauli Kraus families with weights
\[
a=(1+3\lambda)/4,\quad b=(1-\lambda)/4,\qquad
c=(1+3\mu)/4,\quad d=(1-\mu)/4,
\]
so the Kraus operators are `(√a I,√b X,√b Y,√b Z)` and `(√c I,√d X,√d Y,√d Z)`. Only
matching Pauli labels contribute to the identity coefficient. For any feasible contraction,
`|t|≤√(ac)+3√(bd)`, using `|Γ_ii|≤1`; `Γ=I_4` attains this bound and cancels the nonidentity
Pauli terms. Hence
\[
\boxed{\tau(D_\lambda,D_\mu)=\sqrt{ac}+3\sqrt{bd}
=\frac{\sqrt{(1+3\lambda)(1+3\mu)}+3\sqrt{(1-\lambda)(1-\mu)}}4.}
\]
This is the nuclear-norm upper bound from `M=diag(√ac,√bd,√bd,√bd)`, attained because the
identity contraction satisfies the full matrix equality in this case; nuclear-norm equality is not
a general channel-pair rule. The value is the Bhattacharyya overlap of the two Pauli probability
vectors, e.g. `τ(D_0,D_{1/2})≈0.92561479`; by continuity it is `1` for equal parameters and lies
in `[1/2,1)` for distinct parameters in `[0,1]` (strictly above `1/2` for distinct interior
parameters).

For any two distinct channels, a two-dimensional orthogonal program label implements both
deterministically, while dimension one cannot produce positive multiples of two distinct channels.
Thus `C_{ {D_{λ_1},D_{λ_2}} }(p)=1` bit for all `0<p≤1`. More strongly,
`D_λ=λId+(1−λ)D_0`; the mixed program
`ρ_λ=λ|1⟩⟨1|+(1−λ)|0⟩⟨0|` and a fixed processor measuring this label program the entire depolarizing
segment with one qubit. These non-extreme channels therefore calibrate `τ` but do not yield a
nontrivial two-target cost profile.

### C.33 Five full-rank non-extreme targets: qutrit-tight profile

On a qutrit program space define
\[
|+_{01}\rangle=(|0\rangle+|1\rangle)/\sqrt2,\quad
|+_{02}\rangle=(|0\rangle+|2\rangle)/\sqrt2,
\]
with projectors `Q_1=|0⟩⟨0|`, `Q_2=|1⟩⟨1|`, `Q_3=|+_{01}⟩⟨+_{01}|`,
`Q_4=|+_{02}⟩⟨+_{02}|`. Put `E_j=Q_j/8` for `j≤4` and
`E_5=I−Σ_{j≤4}E_j`. Since `||ΣQ_j||≤4`, `E_5⪰I/2`; these effects form a POVM. Define pure
projectors
\[
\sigma_1=Q_1,\quad\sigma_2=Q_2,\quad\sigma_3=|2\rangle\langle2|,
\quad\sigma_4=Q_3,\quad\sigma_5=Q_4,
\qquad \rho_i=\tfrac12\sigma_i+\tfrac16I.
\]
Each `ρ_i` has eigenvalues `(2/3,1/6,1/6)`. The probability matrix `Π_ij=Tr(E_jρ_i)` is
\[
\Pi=\begin{pmatrix}
1/12&1/48&5/96&5/96&19/24\\
1/48&1/12&5/96&1/48&79/96\\
1/48&1/48&1/48&5/96&85/96\\
5/96&5/96&1/12&7/192&149/192\\
5/96&1/48&7/192&1/12&155/192
\end{pmatrix},\qquad \det\Pi=2^{-18}.
\]
All entries are strictly positive.

Let `U_1=I,U_2=X,U_3=Y,U_4=Z,U_5=H=(X+Z)/√2`, and
`Φ_j=Ad_{U_j}`. Their five Choi matrices are linearly independent: the four Pauli Choi projectors
are orthogonal, and `J_{Ad_H}` has off-diagonal `X,Z` terms. Define
`f_i=Σ_jΠ_ijΦ_j`. Invertibility of `Π` implies the five `J_{f_i}` are linearly independent; strict
positive weights on the four Pauli Choi basis projectors make each `J_{f_i}` positive definite.
Thus all five target channels are non-extreme and have full Choi rank.

A deterministic processor measures the qutrit program with `{E_j}` and applies `Φ_j` on outcome
`j`; program `ρ_i` implements `f_i` exactly. For a general heralded processor, the map
`L_s:L(R)→B(B⊗E^*)` sending a program operator to the Choi matrix of its success map is linear.
The five outputs `q_iJ_{f_i}`, with `q_i≥p>0`, are linearly independent. Hence
`rank L_s≥5`, while `dim L(R)=d_R²`; so `d_R²≥5` and `d_R≥3`. This lower bound requires no
extremality or pure programs, and matches the qutrit construction:
\[
\boxed{\mathcal C_{\{f_1,\ldots,f_5\}}(p)=\log_2 3\quad(0<p\le1).}
\]
More generally, `N` linearly independent exact target Choi matrices with positive success require
`d_R²≥N` for any fixed heralded processor.

### C.34 Universal qubit-channel Bell bounds and two Bell constructions

For `E=B=ℂ²`, normalized Choi programs have register dimension `d_Ed_B=4`. In standard gate
teleportation, the identity-labelled Bell outcome implements
\[
P_s(X\otimes J_\Phi/d_E)=\tfrac1{d_E^2}\Phi(X),
\]
so `C_{Chan(2,2)}(p)≤2` bits for `0<p≤1/4`. At `p=1`, the target contains all qubit unitaries, so the exact deterministic universal cost is infinite. These facts do not prove optimality of the four-dimensional construction at `p=1/4` or determine the profile for `1/4<p<1`.

For a complete orthonormal Bell basis `{|Φ_j⟩}` on `E^*⊗E`, set
`W_j=(⟨Φ_j|⊗I_B)`. Completeness gives the uncorrected outcome-summed map
`Σ_j W_jYW_j†=Tr_{E^*E}Y`. On a product program/data input `Y=ρ_{E^*B}⊗X_E`, this is
`tr(X)Tr_{E^*}ρ`. The branch instrument is physical with `d_E²` outcomes. If only the identity
branch is called success, the other `d_E²−1` outcomes are failures of that chosen processor; other
families may allow corrections/acceptance. The summed partial-trace map is not the corrected
teleportation channel. This raw Bell processor, the typed Bell-slice evaluation of C.19, and an
adjunction counit are distinct constructions: Lemma 4.1 forces a counit in rigid graded `Instr` to
have one outcome, whereas the Bell instrument is an ordinary multi-outcome processor. C.19 remains
trace-preserving only on its admissible slice and retains its generic off-slice defect. No claim that
all programmed information is contained in the classical outcome record is made; outcome-resolved
quantum outputs can also depend on the program.

### C.35 Deterministic universal programming: extreme-boundary dimension bound

> **Proposition C.35.** Let `E,B,R` be finite-dimensional with `d_E,d_B≥2`. Suppose one fixed
> deterministic processor `P:E⊗R→B` exactly programs every channel `f:E→B`, so that for each `f`
> there is a program state `ρ_f` with `P(X⊗ρ_f)=f(X)` for all inputs `X`. Then
> \[
> \boxed{d_R\ge d_E^2(d_B-1)+1.}
> \]

*Proof.* If `f` is extreme and `ρ_f=Σ_k p_k|ψ_k⟩⟨ψ_k|` is a spectral decomposition, then
`f=Σ_kp_kP(·⊗|ψ_k⟩⟨ψ_k|)` is a convex decomposition into channels. Extremality implies that
every positive-weight pure component also programs `f`. Thus the map from pure program rays to output
channels has an image containing `Ext Chan(E,B)`. In fixed bases this map is polynomial in the real
and imaginary parts of a normalized program vector, is phase-invariant, and therefore induces a
semialgebraic map from `CP^{d_R−1}`. Its image has real dimension at most `2(d_R−1)`. By Theorem C.2,
`dim Ext Chan(E,B)=2d_E^2(d_B−1)`. Comparing dimensions gives the inequality. ∎

**Scope.** This is a necessary lower bound for deterministic exact universal programming, not a
sufficiency result or a heralded lower bound at `0<p<1`; the pure-program decomposition step relies on
a convex decomposition into channels. For qubit-to-qubit universal programming it gives `d_R≥5`,
which is weaker than the exact-unitary no-go used in C.34 (`C_F(1)=∞`). It is included as a dimension
benchmark derived from C.2, not as a cost law or a novelty claim.

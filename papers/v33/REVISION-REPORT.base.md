# v33: assessment, verification, and implemented revision

> **Historical v33 delivery report.** The later method choice, additional computations and authorized GitHub publication are documented in `research/transition-order/PLAN.md` and `RESULTS.md`. The original outcome/totals below are retained as a dated record, not asserted as the latest execution status.


**Adjudication A-1 · Revision 2 · 16 October 2026 (Asia/Tehran)**

**Deliverable status: author-review draft, not a submission-ready or peer-reviewed paper.** The uploaded v32 is preserved. A full revised LaTeX manuscript, a reproducible source-revision script, a unified diff, numerical code and results accompany this report. This report supersedes `adj-01-paper-improvement-plan.md` and the unfinished earlier revision-2 note. The user's assessment is archived as `adjudications/adj-01-c-v33-assessment.md`.

## Executive decision

Implement **retraction at the headline, analysis in the body**. The three-state-Potts assignment at n = 3, four-state-Potts-plus-logs assignment at n = 4, and q = n inference are withdrawn from the abstract, introduction, phase sections, interpretation and conclusion. The new abstract retains CTD/CPD PostBQP-completeness, record statistics, the operator theory, and proper credit to Bao–Choi–Altman for the n = 2 Ising mapping.

The numerical reading remains: **one n = 3 transition near p_c = 0.3049(2); weak first order favored, continuity unresolved.** Completed χ = 96 data do not settle the order. The new tilted-Clifford SMC is implemented, independently validated and run through L = 128; it does not settle the order either because its large-system genealogies collapse and a population ladder shows drift. A successful computation is not merely a computation that finishes.

The structural upgrade survives, but in a stricter form: **n! is the permutation-label/orbit count, not a universality theorem.** It was already present in the cited literature and, as a bimodule decomposition, in v32 itself. The new contribution is its use to correct this paper's inference and organize new numerical tests—not the discovery of the count.

One important implementation correction: the fourth Clifford commutant of the **two-qubit** gates in this paper has dimension **29**, independently checked by exact rational Gram rank. The 30-label Gross–Nezami–Walter count is independent in the stable regime, requiring at least three qubits at fourth replica order. A redundant 30-label construction on two qubits needs a pseudoinverse; a solved fourth-rung critical point is not supplied here.

## 1. Evaluation of your assessment

| Assessment item | Verdict | Implemented treatment |
|---|---|---|
| Retract the headline class claims; retain the retrospective | Accept | Explicit dated withdrawal, corrected abstract and conclusion, extended crossing table in the body |
| Preserve exact mechanics and credit the n = 2 Ising result | Accept | Main operator statements retained; Bao–Choi–Altman credited in abstract and discussion |
| Promote q = n! and the regular bimodule | Accept with limits | Promoted as a structural comparison, with conditional symmetry-breaking orbit count, finite-dimension quotient caveat and prior-work credit |
| Make n* ∈ (2,3) conditional | Accept and sharpen | Requires first order at n = 3 **and** a regular connecting real-moment phase boundary with appropriate stable neighborhoods. No unique n* is proved |
| If n = 3 is continuous, changeover is higher | Not yet a result | The bracket fails; n = 4,5 short-size data do not prove a new bracket, or even a unique order change |
| Withdraw n = 4 “q = 4 + logs” unqualified | Accept | No “pending another log fit” qualification; location around 0.38–0.39 remains tentative, not a confidence interval |
| Smaller rings imply stronger n = 4 crossover contamination | Qualify | The n = 4 correlation length is unknown; smaller L alone does not order crossover errors across models. It certainly does not justify the old class assignment |
| Operators survive, limiting method changes | Accept | Exact diagonalization computes correct finite-size values; the failed step was their asymptotic interpretation, not diagonalization itself |
| n → 1 fit is suggestive, not a quantitative check | Accept | Fit forms and input sensitivity shown; “first quantitative consistency check” removed |
| The coexistence SMC will settle the question if it runs | Reject the sufficiency | Exact identity and positive weights are valuable, but population bias, rare phases, genealogies, temporal boundaries and mixing must also be controlled |
| CTD/CPD stay in the abstract | Accept | Primary promised completeness results and reductions retained. An optional amplified-promise threshold domain is clarified; see §5 |
| Record results have independent standing | Accept as a dependency statement | Exact LDP, interpolation and dyadic statements retained. This is not a blanket recertification of all earlier proofs; §5 records additional problems found |
| Section VII needs a pass | Accept; more than a numerical substitution | The “modal character” paragraph explicitly retained Potts classes and marginal logs, contrary to the earlier draft assessment. Those clauses are removed; operational and metaphysical claims are separated |

### 1.1 What q = n! does and does not establish

The formal permutation space has the standard decomposition

`C[S_n] = ⊕_(λ ⊢ n) V_λ ⊗ V_λ*`, with `Σ dim(V_λ)² = n!`.

The nonuniform components have dimensions 1 + 4 at n = 3 and 1 + 9 + 9 + 4 at n = 4. If the infinite system breaks S_n × S_n to its diagonal subgroup, the symmetry orbit has n! states. These are different statements:

- The decomposition and conditional orbit count are exact algebra.
- Existence of that symmetry-broken phase at a specified p requires analysis.
- Simultaneous loss of its sectors, transition order and exponents require measurement or proof.
- Reduced symmetry and signed Weingarten coordinates prevent importing the ordinary Potts q > 4 result solely by counting labels.

There is also a local-dimension qualification. At qubit n = 3, the one-wire permutation span has rank 5 while the two-qubit bond span has rank 6. At n = 5, the two-qubit bond Gram has rank 119, not 120; the formal group algebra is then represented through a quotient. The globally aligned p = 0 manifold can nevertheless have all n! independent vectors when the full chain dimension is sufficient. These qualifications prevent replacing one false q = n universality argument with a false q = n! universality argument.

The connection to permutation-Potts limits is verified in Vasseur–Potter–You–Ludwig, already cited by v32. Its setting and limiting assumptions must not be silently identified with this finite-d monitored-circuit operator. [1](https://par.nsf.gov/servlets/purl/10138499)

### 1.2 Continuation and the two ends of the ladder

The illustrative fits, not error estimates, are:

| Fit and input | Extrapolated p at q = 1 |
|---|---:|
| Line through n = 2,3 | 0.16272 |
| Quadratic adding p(4) = 0.380 / 0.383 | 0.16673 / 0.16973 |
| Cubic also adding p(5) = 0.470 | 0.15584 / 0.16784 |

Those few choices give the quoted 0.156–0.170 spread. A wider drift of the uncertain n = 4,5 inputs broadens it further. It is not a bracket on the physical Born transition and does not discriminate Clifford from Haar. Although finite-circuit record moments exist canonically for real q, a few integer critical points do not determine their singular set or normalized entanglement.

Also withdrawn from the plan as delivered results:

- `Z_1 = 1` does not by itself prove a singular amplitude **proportional** to q − 1 or a record-entropy exponent 2ν. Differentiation and thermodynamic limits need control; a nonzero linear amplitude and hyperscaling are additional assumptions.
- The exact n = 2 formula has p_c(d) → 1. It does not prove the same endpoint at every fixed n, the n → ∞ endpoint at d = 2, or noncommuting (q → 1, d → ∞) limits.
- Short-size gap ordering does not measure ξ_coex(5) < ξ_coex(4) < ξ_coex(3). It is compatible with that hypothesis, not an extraction of those lengths.

## 2. Completed computation and its limits

RESULTS_TABLES

### 2.1 What χ = 96 adds

The previously unfinished disordered point completed: at p = 0.305, χ = 96, f_b = 0.99350654, m_species ≈ 0.00065, abs(m_parity) ≈ 0.00006, ξ_χ ≈ 45.4, with 286 iterations. Together with the ordered points at 0.3047 and 0.3048, it preserves the numerical locator rather than changing the verdict.

Three earlier overstatements are corrected in the manuscript and the assessment addendum:

1. A state surviving at a variational local optimum is not a rigorous bound on p_c. The approximate bracket and branch crossing are numerical estimates.
2. ξ_χ ≈ 40–60 is a finite-bond-dimension length, **not** a measured coexistence length, and no lower bound on ξ_coex is inferred from it alone.
3. Effective exponents obtained by changing χ at fixed p slightly below p_c are off-critical diagnostics, not asymptotic β/ν or ν bounds. They cannot by themselves exclude a specified continuous universality class.

What is secure is the withdrawal of the previous evidence-based class assignment, not a proof that every conceivable long-crossover realization of that class is mathematically impossible.

### 2.2 How the new SMC works

The exact identity is `Zbar_3 = E[4^(−N_rand)]` for the Clifford ensemble, equal to the Haar third moment by the gate 3-design. The ensemble conventions match the manuscript: periodic qubit chain, computational product input, period [measurement][odd gates][measurement][even gates], independent schedule coins and uniform two-qubit Clifford gates.

The code tracks unsigned stabilizer generators and uses all 720 elements of Sp(4,2). The tilt is absorbed into the measurement proposal. At a site with a potentially random Z outcome, use

`c = 1 − p + p 2^(−β)` and `p_proposal = p 2^(−β) / c`.

Both proposed branches then have the same residual importance weight c. Deterministic-outcome sites remain weight-neutral. At β = 2, p = 0.305 this avoids the disastrous spread of raw 4^(−r) weights. In the initial timing test, naive weighting gave ESS about 8/2000 at L = 32; the adapted proposal gave roughly 1100/2000 over the short test. The long-run incremental ESS is reported in the tables. This is an exact importance-weight identity, not a proof of efficient rare-event estimation.

The normalizer is accumulated across systematic resampling, with an adaptive half-period resampling step. Genealogy reconstruction explicitly distinguishes entering, mid-period and resampled labels; a deterministic synthetic genealogy test checks this indexing. The normalizer estimator can be unbiased while its logarithm and normalized observable estimates are biased at finite population.

The implementation now records count histograms, entropy histograms, distinct ancestors and descendant ESS for future runs. Existing pilot JSONs predate the expanded diagnostic schema but retain the distinct-lineage counts used here. Descendants in a histogram are not independent samples.

### 2.3 What was actually run

- **30 β = 2 pilot runs** across L = 32,64,128, plus **one β = 0 control**. The L = 32/64 pilot file contains 24 β = 2 runs plus that control; the L = 128 file adds six β = 2 runs.
- **10 β = 1 Ising-control runs** at L = 32,64.
- **6 population-control runs** at L = 32, M = 1000,4000,16000, two independent seeds each.
- **29 small-system validation runs** across seven configurations, including exact targets near p = 0.305, not only far from the transition.

That is 76 SMC/control/validation runs in total. The initial pilot plus the population and β = 1 controls comprise 47 stored large/pilot runs; the 29 validation seed results are stored separately.

The pilot establishes a workable implementation and small-system agreement. It does **not** establish first order, a volume-to-area-law boundary of the tilted ensemble, or a critical density jump. The large entropy changes in poorly sampled genealogies are not used as evidence.

### 2.4 The discriminating production test, revised after the pilot

The highest-value next computation remains the tilted-Clifford route, but the acceptance criteria are now explicit:

1. Verify finite-time normalizers near p_c at small L against exact contraction; this is already done at L = 8,12.
2. At each larger L use a population ladder, several independent populations and both phase-biased starts or a mixing/tempering method. Two seeds are only a pilot. Show that population changes are below the precision needed for the proposed signal.
3. Double the temporal buffer/aspect ratio and record both filtering and interior-time statistics. The L = 128 pilot has T = L, not the proposed production T = 4L or 8L.
4. Use blocked **additive** measurement/random-outcome densities and their response functions as principal thermodynamic diagnostics. Track independent ancestry and autocorrelation; a large incremental ESS is insufficient.
5. Look for stable two-phase weights, peak separation and an interface-barrier scaling across sizes. An absent peak can mean non-mixing, not continuity; a duplicated ancestral path can fake a peak. Entanglement histograms are complementary, not an automatic first-order certificate.
6. Compare with same-p two-branch MPS free energies and residuals; a larger χ target is helpful but not guaranteed to settle the question.

The density response fixes the scale of the required precision. With V = 2LT and ρ_β = E_β[M]/V,

`ρ_β = p + p(1 − p) ∂_p Λ_L(β;p)`.

At β = 2, Λ_∞ = −f_b/4. The approximate branch slopes suggest a possible measured-density separation of order 0.005–0.006 **if** a latent heat survives. It is not an observed jump. Random-outcome density is instead `−∂_β Λ / ln 2`; the two derivatives are not interchangeable.

## 3. Fourth moment: the 30-to-29 correction

The Gross–Nezami–Walter theorem's independent stable-regime basis at fourth moment needs at least three qubits. Its 30 stochastic-Lagrangian labels are therefore not an independent basis for the two-qubit gates used here. [3](https://arxiv.org/pdf/1712.08628)

The independent calculation constructs the span of the 24 replica permutations and their products with

`P = (1/16) Σ_(two-qubit Pauli W) W^(⊗4)`.

The resulting redundant 48-generator Gram matrix has **exact rational rank 29** (SymPy DomainMatrix); P² = P exactly in dyadic arithmetic. An independent exact binary orbit count of balanced four-Pauli tuples also gives 29, checking the full commutant dimension rather than only the rank of a proposed span. This is a verification of the relevant dimension, not a newly discovered general commutant theorem. The all-size theory of Bittel–Eisert–Leone–Mele–Oliviero is also available as Quantum 10, 2171 (2026). [2](https://quantum-journal.org/papers/q-2026-07-22-2171/)

Implementation consequence: use an independent 29-dimensional bond basis, or an explicitly quotiented/redundant construction. Deriving its local twirl/measurement overlap and solving its transfer problem remains work to do. A fourth-moment twirl difference need not shift a critical point; “first appearance of magic” is an interpretation, not an operational resource theorem or a demonstrated new transition.

## 4. Exact, numerical, conditional, and still open

| Claim | Revised status |
|---|---|
| Exact channel/rank/closure statements in their stated scope | Retained; selected statements checked for unchanged source, with previously independent operator tests |
| n = 2 Ising mapping and critical point | Established result, credited to Bao–Choi–Altman |
| n = 3 location near 0.3049(2) | Numerical estimate with finite-χ/optimizer systematics, not a certificate |
| Simultaneous loss of species and parity order | Found within the scanned resolution; no intermediate state found, not a theorem excluding all such phases |
| Weak first order at n = 3 | Preferred numerical interpretation; unresolved |
| Three- and four-state-Potts assignments | Withdrawn unconditionally |
| Regular bimodule and n! orbit count conditional on full ordering | Exact standard algebra; not a universality proof or new literature claim |
| n* ∈ (2,3) | Conditional on order and phase-boundary regularity; no replacement bracket established if n = 3 is continuous |
| n = 4 location around 0.38–0.39 | Tentative finite-size summary, not a rigorous interval |
| n = 5 first-order reading | Plausible from author-reported small-size diagnostics; not asymptotically certified |
| n → 1 critical-point fit | Conjectural extrapolation, not a check or derivation |
| SMC small-system implementation and benchmarks | Verified in the stated cases |
| SMC coexistence verdict | Not obtained; genealogy/population controls fail at pilot scale |
| Fourth Clifford commutant dimension on two qubits | 29, independently checked by exact Gram rank |
| Fourth Clifford critical point or Haar–Clifford p_c split | Not computed |
| Large-d contour/Pirogov–Sinai proof | Program with unknown feasibility; prerequisites unverified |
| Real-replica cluster/loop representation | Open frontier |

The analytic outlook retains Borgs–Imbrie as a possible framework, not a ready-made theorem: stable phases and contour/Peierls bounds have to be supplied for this model. The bibliographic record is verified. [1](https://link.springer.com/article/10.1007/BF01238860)

## 5. Additional corrections found while verifying “unaffected” content

The phase dispute does not logically invalidate the independent record or complexity results. But independence is not a blanket proof audit. Verification found several separate overstatements; leaving them untouched would not improve the paper.

### 5.1 Exact interpolation retained; the limiting sufficient condition corrected

The exact identity is unchanged:

`g(m) − m E[Y] = ∫_0^m (m − s) Var_s(Y) ds`, where `g(m) = log E[e^(mY)]`.

The source's merely bounded `Var(Y_V / V)` is not sufficient to interchange replica and volume limits. Counterexample: Y_V = −VB with a fair Bernoulli B. That intensive variance is 1/4, but for each fixed m > 0 the normalized annealed expression tends to zero, whereas E[Y_V]/V = −1/2.

A sufficient uniform condition is `sup_V sup_(0≤s≤m0) Var_s(Y_V)/V ≤ C`. The normalized annealed–quenched gap is then at most Cm/2. Also, g(m) − mE[Y] is quadratic in m, but g(m)/m − E[Y] is **linear**, as v32's displayed expansion itself shows. The prose is corrected without changing the exact proposition.

### 5.2 No-freezing: analytic branches versus all finite-state processes

An analytic non-affine irreducible branch cannot acquire an affine interval. That argument is retained with explicit sufficient analytic-cocycle assumptions (uniform projective contraction after scalar normalization and local analytic domination). Positivity and integrable entry logarithms alone are not simply relabeled as a completed analyticity proof on the full Haar support.

A reducible finite-state process can expose an affine branch: an initial conserved sector coin selecting either deterministic bits or fair independent bits has `ψ(k) = max(0, k ln 2)`. Therefore the blanket prose “finite reachable implies no affine branch” and “freezing requires an unbounded reachable set” must be narrowed. This does not refute the irreducible analytic-branch argument or establish REM-type smooth freezing in that example.

The p = 1 Haar-refreshed existence statement remains; its unconditional analyticity claim is downgraded pending verification of the additional cocycle hypotheses. **This is a verification gap, not a proof that Haar analyticity is false.** These changes are explicit in the theorem/corollary and abstract rather than hidden in a footnote. Specialist review of the analytic assumptions is still required.

### 5.3 Clifford simulability is not a relative-error SCGF algorithm

Gottesman–Knill gives efficient Born trajectories and score evaluation. It does not make every exponentially tilted disorder expectation efficiently estimable to relative error. The v32 complexity-trichotomy remark claimed too much on this point. The adapted SMC, its ancestry collapse and the earlier exact ESS law all illustrate the distinction. The remark is corrected; no polynomial-cost theorem for the new coexistence experiment is claimed.

### 5.4 Complexity results retained, with a promise-domain clarification

The primary CTD result and the fixed CPD purity thresholds 13/18 versus 5/9 remain intact. The whole complexity appendix is preserved apart from explicitly requiring **integer n ≥ 3** for its optional amplified thresholds `1 − 2^(−n)` versus `1/2 + 2^(−n)`. At n = 2 these thresholds coincide, and at n = 1 they overlap. This clarification does not affect either fixed-gap PostBQP-completeness result. A source-contract test checks the exact scope of the change.

### 5.5 Design order and interpretive claims

The source's claim that the Clifford design stops at the same replica order as Gram invertibility is false: the two-qubit Haar Gram is still invertible at n = 4, but Clifford is only a 3-design. Corrected.

Section VII formerly repeated marginal-log and specific-Potts claims and asserted overly broad interpretive equivalences. Its operational “record-stream” reading is retained, but no theorem here derives the Born rule, an ontology, time, or equivalence with a changed-collapse instrument. The non-dual working premise is not imported, consistently with the governing framework of this conversation; no alternative theology is encoded into the circuit mechanics.

## 6. What is implemented, and what is not

### Delivered

- Full `manuscript_revised_v33.tex` with corrected abstract, introduction, phase sections, retrospective, SMC method/results, analytic outlook, Section VII and conclusion.
- `v32-to-v33.diff`, reproducible `revise_manuscript.py`, source SHA-256 provenance, and the section fragments used by that script.
- Completed χ = 96 JSONs and logs, SMC code, pilot/control/validation data, exact finite-time contraction and exact commutant Gram-rank code.
- CSV tables and `make_revision_tables.py` generating them directly from stored runs.
- A counted verification suite, regression log and integrated runner.
- An amendment to v2.2 confined to adjudication provenance and verification accounting; no Qur'anic reading or Part I–II commitment is changed.

### Not delivered as completed science

- Controlled n = 3 coexistence, a converged ξ_coex, latent heat or interface tension.
- New χ ≥ 128 production scans, n = 3,d = 3 production data, or an n = 4 VUMPS solution.
- A solved fourth Clifford transfer operator or a measured Haar–Clifford critical-point split.
- A real-replica continuation theorem, unique n*, or a contour/cluster proof.
- A re-creation of the missing original supplementary deposit, raw Haar SCGF samples, n = 5 orbit-block production or the original figure.

### Verification and publication readiness

VERIFICATION_SUMMARY

Selected original operator, LDP, exact interpolation and dyadic proposition statements are checked for verbatim preservation. Those source checks are not new formal proofs. The numerical suite checks implementation, finite-size agreement, counterexamples and document contracts; its pass count is not a count of independently proved paper theorems.

The source has no unresolved label references or bibliography keys and its environments balance. The original `fig_final_fss_v16.pdf` and v32 Supplemental Material are absent from the upload. A submission-layout PDF has **not** been certified or fabricated with replacement scientific figures. Restore those author artifacts, review the new assumptions, and compile under REVTeX before submission. This is why the deliverable is marked **author-review draft**.

## 7. Reproduction and next action

From the review-package root (same relative layout as this workspace):

```bash
python3 -m pip install numpy scipy sympy python-docx z3-solver
python3 papers/v33/revise_manuscript.py
python3 papers/v33/make_revision_tables.py
bash papers/v33/run_review_checks.sh
```

The paper-only package reruns 17 + 35 = 52 checks; the full workspace additionally contains the other framework suites and its updated `v2.2/verify/run_all.sh`. The standalone extension is `python3 v2.2/verify/v33_checks.py`. It reruns the small-system statistical regressions with fixed seeds. The long pilot is not automatically rerun. For a new SMC case:

```bash
cd v2.2/verify/replica
python3 clifford_tilt_smc.py 32 0.305 2 4000 128 4 101 new_run.json
```

The next scientifically decisive step is **population- and mixing-controlled coexistence sampling**, or a genuinely converged same-p two-branch MPS study. Increasing raw L, particle count or χ without those controls is not the acceptance criterion.

**Bottom line:** your assessment improves the plan, and the plan is now implemented as a corrected paper draft and reproducible numerical extension. It is stronger because its conclusions have become narrower and testable—not because q = n! or a completed SMC run has been promoted into a phase-order theorem.

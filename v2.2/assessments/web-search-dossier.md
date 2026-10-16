# Web-search dossier — 15 October 2026

**Instruction.** "Conduct deep web search for additional clues and useful or needed material." Three things were done: (A) the author trail behind clues 5 and 8 was followed to its source (Zenodo, ORCID 0000-0002-0019-1842) and every record triaged; (B) the material the plan still needed was searched for (2025–26 results on gravitational algebras, relational clocks, the thermal-time hypothesis, collapse tests, Wigner's-friend tests, the open mathematical items); (C) every arXiv identifier in §22.2 that had been cited "from memory" was machine-checked against the arXiv API. Raw material is in `/home/user/search/`. Nothing in this dossier is a source of claims for Part I; its effects on v2.2 are listed at the end and logged in §23.2 (items 83–89).

---

## A. The author trail (Zenodo; 23 records; `search/zenodo_abaee_records.json`)

Query `creators.name:"Abaee"` returns 23 records, all by Amin Abaee. No record carries the titles of clues 1–4, 6a or 6b (Master Synthesis, Lighthouse, Maturidi, prime-spectral); those exist only as the user's uploads. Rev. 2.8 of the opfibration manuscript (clue 5, October 2026) is newer than every Zenodo version.

| Date | Zenodo id | Title (short) | Triage |
|---|---|---|---|
| 2026-02-08 | 18523783 | *From ornament to algorithm* (Energy and Buildings; architecture) | out of scope |
| 2026-06-30 | 21053301 | *Overcoming Autoregressive Myopia: Parallels from Computer Chess for Multi-Agent LLM Architectures* | the chess analogy of §10.1 has an earlier home here; no claim about time |
| 2026-07-06 | 21228121 | *Comment on "Axioms for retrodiction…"* (2 pp.) | **examined — see A.1** |
| 2026-08-04 | 21792637 | *Quantum Combs, Higher-Order Processes, and the Normalization-Defect (Intercept) Principle* | ancestor of Rev. 2.8 |
| 2026-08-04 | 21795780 | *No Universal Process Currying* (`opfibration manuscript.tex`) | ancestor of Rev. 2.8 (adjoint iff one-dimensional environment; no-programming; Borsuk–Ulam bound) — all already covered by `opfibration_checks.py` |
| 2026-08-05 | 21808030 | *No-Go Theorem for Additive Dynamics on Decorated Quantum Channels* (paper B) | composition-additive valuations are boundary terms ∝ log d_E; nothing new for §10 |
| 2026-08-05 | 21808587 | *Geometry of the Normalization Obstruction: Choi Faces…* | its headline is the R7 "never a perfect square" statement; R7 was closed negatively in v2.2 (§10.4; `r7_check.py` 15/15) and nothing here reopens it |
| 2026-08-12 | 21895581 | *Environmental Currying and Causal Internal Homs* | dimension-profile method; classical channels = products of simplices; covered |
| 2026-08-12 | 21895686 | *Normalization Obstructions in Decorated Quantum Processes* (paper C) | all-order no-go; non-normalized two-sided adjunction; covered |
| 2026-09-02 | 22260638 | *Rate–Distortion Theory of Bounded Sequential Transduction* | = clue 8 (§22.8) |
| 2026-09-06/07 | 22545740, 22552060, 22552616, 22552680, 22553311, 22553609, 22554177, 22554217, 22554297, 22554480, 22588570 | sustainability / viability / fisheries / aquifer papers | out of scope; 22552616 (*An Obstruction Calculus for Viability under Incomplete Observation*) reuses the obstruction vocabulary of §10 in ecology |
| 2026-09-24 | 22940820, 22941018 | datasets: category-theoretic viability (holonomy; "projected CPTP contraction settles the Zeno self-reference"); FBA curvature (E. coli) | out of scope; the Zeno remark is a slogan in a dataset description, not a result |

**What the trail adds.** It confirms the chronology the plan had inferred (the opfibration theorems, August 2026 → Rev. 2.8, October 2026 → the BST paper, September 2026) and shows the author's output is wide (architecture, LLM architecture, ecology, quantum process theory). It yields one new technical document, the Comment.

### A.1 The Comment on "Axioms for retrodiction" (Zenodo 21228121) — finding

*What the Comment says.* It attributes to Parzygnat and Buscemi (*Quantum* 7, 1013 (2023); arXiv:2210.13531) a "retrodiction opfibration over prepared processes", a theorem ("Theorem 4.3") that this opfibration admits a *flat physical section iff all channels are unital*, and a remark that in the classical limit the tensor product "becomes Cartesian" so that Bayesian inversion is flat. It then argues that FinStoch is affine rather than Cartesian (the unit is not terminal; unital = doubly stochastic), gives the counterexample X = {1}, Y = {1,2}, f = (p, 1−p), k = discard, for which f ∘ R_σ(f) ∘ k† = 2(p, 1−p) ≠ (p, 1−p), and concludes that the obstruction to state-independent reversal is *affine, not non-commutative*; the classical copy map makes the Bayesian inverse canonical but not flat.

*Check.* The full text of arXiv:2210.13531v2 (31 pp., 16,556 words; `search/pb2023.txt`) — which is the published text, *Quantum* being an arXiv overlay journal — contains **no** occurrence of "opfibration", "flat", "Cartesian", "prepared process", "FinStoch", "terminal", "classical limit", "state-independent" or a "Theorem 4.3" of the stated content. Parzygnat–Buscemi define retrodiction as a functor **R : States → States^op** on a category whose *objects are (algebra, prior) pairs*; retrodiction is prior-indexed *by construction*, and their Proposition 2.3 already exhibits the discard-and-prepare assignment (the Comment's own counterexample) as a "non-example that comes quite close" and fails. The Comment's arithmetic is correct and its conclusion is true, but it is a conclusion Parzygnat–Buscemi's framework presupposes rather than denies: the claim it refutes could not be located in the paper.

*Verdict.* **[F] as a comment** (misattributed target); **[C] as mathematics** (trivial). *Bearing on the plan:* none that was not already there — §10.7 and §17.2 state that exact reversal is prior-indexed and that the arrow comes from the state, and they cite Parzygnat–Buscemi for exactly that. The finding is recorded for calibration: it is the first document in the author trail that fails on scholarship rather than on register, and it should raise, slightly, the weight given to the plan's policy of re-deriving every claim of clues 5 and 8 rather than trusting their citations (§22.3, §22.8).

---

## B. Needed material found (2025–26), with bearing

All identifiers below were resolved against the arXiv API or Crossref on 15 October 2026.

### B.1 Clocks, relational dynamics, the clock ambiguity (§9.3, P15, G17)

- **Stoica, "The clock ambiguity problem: extended or extinguished?", arXiv:2604.21805 (Apr 2026).** Claims: (i) under a purely relational stance the ambiguity (Albrecht 1995) extends from histories to *evolution laws* — the spectrum of any ideal clock uniformizes the world's evolution operators, leaving only Hilbert-space dimension as invariant information; (ii) the non-interaction condition of Marletto–Vedral (2017) does not remove it, because after uniformization unitary equivalence is too coarse; (iii) fixing the clock–world split removes it but "blocks spacetime symmetries"; (iv) not all decompositions can be equally valid perspectives, else records would not correlate with events; (v) the resolution is the *physical meaning of the operators*, which a bare Page–Wootters structure omits. **Bearing:** strengthens §9.3 items 1–2 and P15/G17 in the plan's direction — the split and the clock are not supplied by the state or by relational conditions; something external to the bare structure (the plan's M2 measure; the operators' physical meaning) must be added. Unrefereed; register "preprint".
- **Chataignier, Höhn, Lock, Mele, "Relational dynamics with periodic clocks", New J. Phys. 28 (2026) 034504, arXiv:2409.06479.** Relational observables relative to periodic clocks are gauge-invariant only for periodic quantities, otherwise only transiently; a systematic treatment of winding. **Bearing:** §9.3 item 3 (non-ideal clocks); the L-tick clock lemma of §9.4 concerns the same object at the finite-state level.
- **De Vuyst, Höhn, Tsobanjan, "On the relation between perspective-neutral, algebraic, and effective quantum reference frames", Quantum 10 (2026) 2196, arXiv:2507.14131.** Three QRF approaches related. **Bearing:** background to §11.4 (DEHK) and P15.
- **Aguilar-Gutierrez, Ferrero, Höhn, Marchetti, "Relational path integral, effective actions and quantum frame covariance in gravity", arXiv:2607.21463 (Jul 2026).** Frame-dressed gravitational path integral. **Bearing:** WP0/RQ-9 context.
- **Diaz, Perez, "The problem of time: a path integral view", arXiv:2605.17935 (May 2026).** Schrödinger evolution emerges in the path integral once a clock degree of freedom is identified and put in a semiclassical "good-clock state"; the e^{iS}+e^{−iS} form of covariant amplitudes is tied to the clock's state. **Bearing:** §9.4 ledger row 1 (order is output of constraint *given a split and a good clock*) and §17.1 (orientation from the state, not the action).
- **Coppo, Cuccoli, Verrucchi, "A magnetic clock for a harmonic oscillator", PRA 109 (2024) 052212, arXiv:2310.13386** (the paper behind the June 2026 press pieces quoting Vedral); **Coppo, Pranzini, Verrucchi, arXiv:2601.07437 (Jan 2026).** A finite spin clock labels only part of an oscillator's states: "not every quantum clock is good enough". **Bearing:** §9.3 item 3; consistent with the §9.4 lemma.

### B.2 Gravitational algebras and the clock inside the algebra (§11.4, P15, D-12)

- **Chen, Xu, "An algebra for covariant observers in de Sitter space", arXiv:2511.00622 (Nov 2025; v3 Aug 2026).** Imposing the full SO(1,d) constraints (a fluctuating geodesic) gives an *averaged* modular crossed product over static patches; type II with a faithful normal trace; type II₁ with a lower-bounded clock Hamiltonian; entropy observer-dependent; agrees with generalized entropy for semiclassical states. **Bearing:** §11.4 — the observer/clock remains the condition of existence of the algebra; now with the clock's worldline itself quantum.
- **Klinger, Kudler-Flam, Satishchandran, "Generalized entropy is von Neumann entropy II: the complete symmetry group and edge modes", arXiv:2601.07910 (Jan 2026); PRD 2026.** Angle-dependent horizon-area fluctuations ("boost supertranslation" charges) impose infinitely many constraints; the dressed algebra is still type II; black holes: II_∞ with no maximum-entropy state; de Sitter with a realistic observer (rotational and binding energy): II₁. **Bearing:** §11.4 and D-12 unchanged in direction, strengthened in detail.

### B.3 Thermal time — the standing objections (§11.2, §9.4)

- **Swanson, "Can quantum thermodynamics save time?", Philosophy of Science 88 (2021) 281–302, DOI 10.1086/711569.** Objections to the TTH: the thermal-time/proper-time relation; the classical implementation.
- **Chua, "The time in thermal time", J. Gen. Philos. Sci. (2025), DOI 10.1007/s10838-024-09691-8.** The circularity worry: interpreting the modular parameter as physical time requires dynamical assumptions the hypothesis was meant to supply; not every one-parameter automorphism group deserves to be read as time translation.
**Bearing:** the plan already registers the TTH as a conjecture (§11.2) and the ledger (§9.4) says the modular flow is "parametrized, not oriented" and is output of (algebra, state). The objections do not touch the theorem (Tomita–Takesaki needs no dynamics) and do touch the *identification*; they are now cited at §11.2 so the conjecture carries its critics.

### B.4 Laboratory analogue — entropic time in cold atoms (§17.3a)

- **Barontini et al., "Testing the problem of time with cold atoms", Phys. Rev. Research 8 (2026) L022047, arXiv:2509.07745.** An isolated BEC with a time-independent Hamiltonian partitioned by optical potentials into a "dark" and a "bright" sector; the bright sector's effective Hamiltonian is minisuperspace-like; a scalar "clock field" φ is *not* monotonic across recollapse, while an operationally defined *entropic time* (coarse-grained entropy exchange between sectors) orders the data monotonically and yields an effective Schrödinger equation reproducing the measurements; at the "heat death" the entropic time stops. **Bearing:** a third scoped analogue for §17.3a. It illustrates exactly the ledger's division — an internal clock gives order (and fails where it is non-monotonic); the arrow in the analogue is read off a coarse-grained entropy of a *particular state* (Prop. 11.1's pattern), not off the structure. Analogue, not instance.

### B.5 Collapse models (D-7 register; landscape row "Modify QM")

- **XENONnT Collaboration, "Challenging spontaneous quantum collapse with the XENONnT dark matter detector", PRL 136 (2026) 120201, arXiv:2506.05507.** Search for collapse-induced X-rays, 1–140 keV, first science run; world-leading limits: CSL improved by two orders of magnitude, Diósi–Penrose by a factor of five, with a spectral model that for the first time includes electron–proton cancellation. **Bearing:** the D-7 evidence row is updated (Donadi et al. 2021 → XENONnT 2026). D-7's bet against the family is unchanged.

### B.6 Extended Wigner's friend (G20; §4.2 informational layer)

- **Zeng, Labib, Russo, "Towards violations of Local Friendliness with quantum computers", Quantum 9 (2025) 1851, arXiv:2409.15302** — LF violations with friends of increasing "branch factor" on superconducting processors (loopholes open).
- **Laux, Cavalcanti, "Extended Wigner's Friend Scenarios with Agent-like Observers on Quantum Computers", arXiv:2609.12527 (Sep 2026)** — friends implemented as reversible circuits with memory, conditional action and Born-rule betting; LF violations on ibm_marrakesh; freedom-of-choice loophole open. **Bearing:** G20's cost (nonlocal actualization under absoluteness) now has an experimental programme behind it that moves the "friend" toward an agent; nothing in the plan's position changes, but the entry is no longer resting on Bong et al. 2020 alone.

### B.7 Open mathematical items — status unchanged

- **Multi-letter AAK (clue 8, N-1 register):** arXiv still has only Lacroce–Panangaden–Rabusseau 2022 (arXiv:2206.00172); the multi-letter case remains open. The BST paper's "Sudo 2026" is real: **A. Sudo, "Thermodynamics of Learning: A Typed Four-Component Accounting of Memory, Fit, and Value", arXiv:2608.12791** (Aug 2026) — the typed-budget idea has a published antecedent; §22.8's "unverified" flag on that citation is lifted.
- **Primon gas (§11.9/§11.10):** no 2026 follow-up to Hartnoll–Yang beyond De Clerck–Hartnoll–Yang arXiv:2507.08788 (already cited).
- **Causal irreversibility (item 76):** Ellison, Mahoney, Crutchfield, "Prediction, retrodiction, and the amount of information stored in the present", J. Stat. Phys. 136 (2009) 1005, arXiv:0905.3587 — identifier now verified.

---

## C. Identifier audit of §22.2 (arXiv API, 15 October 2026)

All **47** arXiv identifiers appearing in §22.2 resolve, and their titles and authors match the cited works (`search/arxiv_meta.json`, `search/arxiv_meta2.xml`). One row was wrong and is corrected:

- *Leutheusser–Liu.* "Causal connectability between quantum systems and the black hole interior in holographic duality" is **arXiv:2110.05497**, not 2112.12156; **2112.12156** is "Emergent times in holographic duality"; **2212.13266** is "Subregion-subalgebra duality: emergence of space and time in holography". The row now lists all three.

Journal references in §22.2 that the arXiv record carries were confirmed in passing (e.g. Castro-Ruiz et al. Nat. Commun. 11 (2020) 2672; Höhn–Smith–Lock PRD 104 (2021) 066001 and Front. Phys. 9 (2021) 587083; Moreva PRA 89 (2014) 052122; Carroll–Singh PRA 103 (2021) 022213; Giovannetti–Lloyd–Maccone PRD 92 (2015) 045033; Fewster et al. CMP 406 (2025) 19; Furuya et al. JHEP 08 (2023) 111; JSS JHEP 2023 20; Bong et al. Nat. Phys. 16 (2020) 1199; Reeb–Wolf NJP 16 (2014) 103011; Barbour–Koslowski–Mercati PRL 113 (2014) 181101; Gomes–Gryb–Koslowski CQG 28 (2011) 045005; Jacobson PRL 75 (1995) 1260 and PRL 116 (2016) 201101; Casini CQG 25 (2008) 205021; Bousso JHEP 07 (1999) 004; Ryu–Takayanagi PRL 96 (2006) 181602). Rows whose journal details are not in the arXiv record (pre-arXiv classics; Witten 2022's JHEP reference; García-Pintos et al. PRX 16 (2026) 011028) keep the "verify journal reference" status. The §22.2 header is changed accordingly.

---

## D. Changes made to v2.2 (seventh amendment)

1. §22.2 header and Leutheusser–Liu row corrected; protocol line updated (arXiv identifiers machine-verified).
2. §22.10 added: this dossier's sources, with status (refereed / preprint / Zenodo), and the Comment finding.
3. §9.3 item 1–2: one sentence each on Stoica 2026.
4. §11.2: the TTH's critics (Swanson 2021; Chua 2025) attached to the conjecture register.
5. §11.4: a "2025–26" bullet (Chen–Xu; Klinger–Kudler-Flam–Satishchandran; De Vuyst–Höhn–Tsobanjan).
6. §17.3a: Barontini et al. 2026 added as a third scoped analogue.
7. Landscape row "Modify QM" (§7) and D-7 evidence: XENONnT 2026.
8. §16/G20 cross-reference: LF tests on quantum computers (Zeng et al. 2025; Laux–Cavalcanti 2026).
9. §22.8: Sudo 2026 verified.
10. §23.2 items 83–89; §24 provenance.

No grade in Part I or Part II changes. No work package changes. The Comment finding alters nothing in §10.7/§17.2 beyond a footnote-level caveat in §22.10.

# Branch continuation: corrected assessment and proposed next gate

16 October 2026 · A-1 continuation · **Proposal only: no new production allocation yet.**

## What the completed scan actually measured

The six-rate scan recorded both `f_half` and `f_full_rayleigh` for every accepted preparation. It was not solely a record of final order parameters or optimizer basins. Examples of the recorded full-period trial-state values are:

| p | Ordered-start history | Disordered-start history |
|---:|---:|---:|
| .30470 | .992545675311388 | .992545675311591 |
| .30486 | .993062083928551 | .993062080171600 |
| .30500 | .993505848064407 | .993505850138863 |

Last digits describe individual numerical contractions, not certified global errors. At .30470 both states have large order diagnostics and align as nearly equivalent symmetry orientations. At .30486 and .30500 both have small order diagnostics. Thus the initialization labels do **not** identify an ordered and a disordered phase branch over these rates.

The missing object is **two separately identified, stationary, symmetry-inequivalent branch families retained through a common rate interval**, with a controlled comparison of their free-energy functionals. The existing values cannot simply be renamed `f_ordered(p)` and `f_disordered(p)` because of the starting labels.

Numerical stationarity was tested for the Hermitian half-row objective. Full-period values are evaluations on those states, not independent full-period optimizer convergence. Their finite-chi discrepancies and optimizer/truncation errors are not global free-energy error bounds.

The scan samples two numerical histories and their functionals. It does not map whole basins, certify a global minimum, identify physical spinodals, or prove that the sampled change is a basin boundary rather than a physical or finite-chi effect. Agreement from two starts is not a global-minimum certificate.

## Thermodynamic distinctions

- First-order coexistence requires equality of the competing bulk free-energy densities, not a finite gap. Distinct branches may remain metastable on either side before a spinodal. Their identity and stability must be checked rather than inferred from initialization.
- A kink in f normally denotes a jump of f', a first-order signature for a generic tuning direction. At an ordinary continuous transition f' is continuous while higher derivatives can be singular; not every continuous transition has a simple power-law scenario.
- Sharpening as chi increases is not by itself a first-order discriminator: reduced finite-entanglement rounding can sharpen a continuous transition too. Likewise a merger of numerical branches at one rate does not establish continuity.
- Finding distinct minima or a crossing at one finite chi can be a variational artifact. A non-vanishing jump requires chi/size-systematic control; no finite sandbox run is promised to force a binary verdict.

## Selected next protocol: unbiased branch-following continuation at chi128

This is not another independent-start grid. Warm-continue **actual accepted states** from opposite sides, with no residual phase constraint or pinning field in the final objective.

A bounded branch-retention pilot would use:

1. Large-order anchor: ordered-start chi128 state at p=.30470.
2. Small-order anchor: disordered-start chi128 state at p=.30486.
3. Large-order history: .30470 → .30475 → **.30480**.
4. Small-order history: .30486 → .30483 → **.30480**.

Each continuation step must pass the unchanged 1e-7 numerical gates before being called a stationary branch observation. Save all tensors and provenance. Record symmetry-invariant order, symmetry-aligned overlap, correlation diagnostics, and both energy functionals. Do not force a family to remain ordered/disordered; a jump, merger or convergence failure is an outcome, not a manufactured branch or a certified physical spinodal.

At the common target, compare the **same** stationary objective on both states; retain full-period evaluations as a separate diagnostic. Do not mix half-row and full-period numbers into one crossing. A tiny energy sign change between nearly equivalent states is not a coexistence crossing.

If distinct stationary families survive, the next gate is a second common rate forming a genuine branch-pressure bracket, then smaller steps/root bracketing and unbiased perturb-and-return stability tests. Merely restarting an exact fixed point does not demonstrate local stability. Perturbation recovery is a numerical variational-landscape test, not by itself a thermodynamic metastability certificate. If a bias is ever used for preparation, remove it and reconverge before using an unbiased branch value.

## Runtime gate

The proposed pilot has two sequential stages with at most two single-thread CPU workers. At the earlier per-stage ceiling it can require **up to 3 hours walltime** (90 minutes per stage), and may still fail to retain two branches. It is not the full crossing/stability/chi-extrapolation campaign. No chi192 run, extra rate bracket or perturbation production is automatically authorized. Fresh authorization is needed; the completed six-rate allocation is not silently extended.

The earlier scan, exact operator checks and source records remain intact. The v34 Qur'anic/Lighthouse interpretation and real creator–creation distinction are unchanged by this numerical protocol proposal.

# χ128 same-point convergence-safety refinement

16 October 2026 · A-1 · a separately recorded numerical amendment, not a new rate.

**Refinement status:** accepted under unchanged external gates. **Original pilot status remains:** stopped: stage 2 acceptance gate not passed for both histories. The original failed record and checkpoint are not overwritten or retroactively accepted.

## Why refinement was authorized

At p=.30480, the original small-order history passed the primary stopping test (9.995603787e-08) but its right compatibility defect was 1.000165013e-07, above the strict 1e-7 ceiling. It was rejected, not rounded into acceptance.

The user separately authorized up to 30 minutes at the same p=.30480, χ128 and unbiased operator. Only the internal convergence-driving goal is tightened to 5e-8. External acceptance is unchanged: primary and BOTH compatibility residuals <1e-7, canonical defects <1e-9, positive full-period contraction and relative defect <1e-8. No phase constraint, new p, perturbation stability production, crossing bracket or χ192 is added.

An internal goal is not a new external threshold. If an internal driving budget ends, the saved state can be accepted only after all original external gates and period validation are actually checked within the reserved time. Its internal-target and budget status remain explicit. A changed order character is an outcome, not prevented.

## Refinement geometry and acceptance

| Diagnostic | Refined small-order history |
|---|---:|
| Primary optimizer residual | 4.988270901e-08 |
| Left compatibility | 4.989559384e-08 |
| Right compatibility | 4.996652741e-08 |
| Left canonical defect | 4.007662612e-14 |
| Right canonical defect | 4.085127235e-14 |
| Internal 5e-8 goal met | True |
| Period contraction defect | 3.523379389e-13 |
| Total refinement seconds | 883.48 |

## Augmented comparison at the same p=.30480

The large-order result is the already accepted original-pilot state. The other column is the separately validated refinement. These are finite-χ numerical states; history labels are not automatically thermodynamic phases.

| Diagnostic | Accepted large-order history | Refined small-order history |
|---|---:|---:|
| f_half (stationary objective estimate) | 0.992869885471 | 0.992871751622 |
| f_period_Rayleigh (separate trial evaluation) | 0.992869864438 | 0.992871518919 |
| m_species | 0.51753748 | 0.00967019 |
| abs(m_parity) | 0.34709416 | 0.00577977 |
| Invariant color L2 | 0.48823244 | 0.00902724 |
| xi_chi | 72.8757 | 73.2547 |

Ordered-history minus refined-history: **Δf_half=-1.86615050e-06** and **Δf_period,trial=-1.65448091e-06**. These are different finite-χ functionals, not one mixed crossing or global error bounds.

Symmetry-aligned comparison: all 36 symmetry orientations evaluated; largest evaluated fidelity/site 0.997585340183. This is a constructed-state diagnostic, not a phase-order classifier.

## What is still missing

A nonzero energy difference at one common p is not coexistence. Competing bulk branch free energies must agree at a properly bracketed crossing of distinct phases. This amendment provides neither a second common rate nor an independently tested local/thermodynamic stability certificate. The half-row objective and full-period trial evaluation differ at finite χ; no global variational/truncation error bound or χ→infinity control is obtained here.

**Physical transition order remains unresolved.** The earlier pressure values were already measured; the missing work concerns identification/retention, crossing, stability and systematic errors of phase branches. No numerical result is forced by the governing creator–creation interpretation.

# Resource feasibility and stopping decisions

Two CPU cores, approximately 2 GB RAM, one BLAS thread per worker. These estimates explain triage; they are not impossibility theorems about better algorithms.

| Object | Float64 storage before solver work arrays | Decision |
|---|---:|---|
| n=4 full-period dense local MPO, bond 24² | 24⁶ × 8 = 1.529 GB | Do not materialize in this sandbox |
| n=4 Hermitian half-row dense local MPO, bond 48 | 48² × 24² × 8 = 10.62 MB | Feasible; exact ring/endpoint controls precede pilot |
| n=5 L=8 permutation-label vector | 120⁴ × 8 = 1.659 GB per vector | A conventional multi-vector Krylov solve is infeasible here |
| n=5 L=8, 16 Krylov vectors alone | 26.54 GB | Needs orbit/symmetry reduction and rank-119 quotient, not naive full space |
| n=5 Hermitian half-row dense MPO | 240² × 120² × 8 = 6.636 GB | Needs further factorization; current low-bond n≤4 implementation is not a valid n=5 implementation |
| n=3 L=20, 16 Krylov vectors alone | 6¹⁰ × 8 × 16 = 7.740 GB | Existing exact L≤18 data are not extended blindly |

For n=5,d=2 the two-qubit bond Gram rank is **119 of 120**. The legacy inverse-Gram implementation is explicitly for d²≥n and must not be reused at n=5 by accepting a numerically ill-conditioned inverse. The original n=5 L=8 orbit-block assembler and its validation deposit were not supplied. Independent large-size n=5 reproduction remains deferred until a quotient-aware symmetry-reduced assembler exists. A tiny L=4 pilot alone would not certify the claimed order, so it does not outrank the n=3 matched-branch computation.

The measured n=3 chi=128 iteration cost is about 15 seconds in the initial implementation on this machine. A naive cubic extrapolation to chi=192 is roughly 50 seconds/iteration; 30 iterations would exceed the 900-second production-stage ceiling. Warm starts and exact contraction improvements may help, but chi=192 is conditional on measured feasibility, not promised just because it appears in a target list.

Two exact optimizations were implemented and checked without changing the operator: block-diagonal direct-sum contractions, and reducing paired environment eigenproblems to one component B while reconstructing (B,Bᵀ). **Both global summands are still present in the center problem.** This is not the rejected non-Hermitian H-only optimizer. At small chi block dispatch is not necessarily faster; the data record actual timings instead of assuming a speedup factor.

Partial states checkpoint every five iterations for chi≥96 and every twenty below that, plus at convergence/budget stop. A stopped optimizer state is usable as an approximate initialization, not an accepted phase result. Planned performance-upgrade and plateau stops are recorded separately in `optimizer-segments.json`; per-segment times are not silently represented as total end-to-end cost.

L=8 fourth-Clifford work is benchmark-gated. The actual matvec runtime, memory high-water mark, per-sector time budgets and any partial cases are recorded in `clifford4_L8_budgeted.json`. Smaller-system timings do not authorize an unbounded larger ladder.

## Final resource-limited outcome

Chi=128 did not produce an accepted phase: ordered p=.3048 stopped after its resumed 900-second segment (saved iteration 63, residual 1.15e-6); disordered p=.305 was triaged at saved iteration 15 (residual 2.34e-5). These are not converged high-chi results. Chi=192 is **deferred and was never launched**, not merely an implied next automatic queue entry.

Both opposite-start chi=96 attempts at p=.30486 then hit their prospective 750-second ceilings: ordered 153 saved iterations/residual 8.75e-7, disordered 154/residual 8.30e-7, versus tolerance 1e-7. Disordered p=.30490 converged first; the ordered queue did not reach .30490. Explicit missing cases are in `deferred-computations.json`. The six cheap full-period frozen-trial contractions completed afterward, but their tiny contraction residuals do not replace optimizer, chi or thermodynamic convergence. No campaign numerical workers remain running.

## Authorized chi128 stage — completed outcome

ordered: accepted-stationary-at-finite-chi, eps=9.991478996514631e-08, iterations=186, total stage 2507.1s; disordered: accepted-stationary-at-finite-chi, eps=9.56534706713505e-08, iterations=79, total stage 1022.8s.

2/2 preparations passed the prospective acceptance gates at p=.30486. This does not decide first order versus continuous. Chi192 was not launched; no campaign numerical production remains running. The earlier chi96 failures do not establish two stationary phases. See `CHI128-STAGE.md` for the interpretation contract and logical counterexamples.

### New measured iteration cost

The completed common-rate chi128 loops averaged 12.71 to 13.38 seconds per iteration. Holding iteration complexity fixed, a naive cubic chi192 forecast is 42.9–45.2 seconds/iteration, or roughly 3.6–3.8 hours for 300 iterations per preparation. This is not a measured chi192 benchmark or a convergence promise, and no such allocation was authorized. The present chi128 convergence bottleneck was overcome; a rate bracket and chi/size-systematic controls, not a binary one-point inference, remain necessary.

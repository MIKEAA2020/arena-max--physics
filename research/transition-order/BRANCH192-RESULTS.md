# χ192 branch-retention continuation at p=.30480

17 October 2026 · A-1 continuation · finite-χ numerical test, not a thermodynamic verdict.

**Campaign status:** both accepted finite-chi states. **Two of two χ192 states passed the unchanged external gates.**

## Scope and resource gate

The authorization was limited to enlarging the exact accepted χ128 p=.30480 ordered-history and refined low-order-history checkpoints to χ=192, with at most two single-thread workers and one five-hour absolute wall-clock cap. No extra p, perturbation, stability run, or additional preparation was authorized.

The immutable first resource gate used a deliberately broad 200-iteration forecast and stopped before production: its one-step wall timings (which include operator construction) projected beyond five hours. That STOP record is retained. The follow-up feasibility addendum then separated the VUMPS-internal iteration time from the one-time build: measured benchmark steps were 82 s and 87 s; the two accepted same-p χ128 warm steps had taken 23 and 55 iterations. A transparent 2× allowance on the larger observed count (110 iterations per preparation), a 90 s/iteration forecast, a 120 s setup reserve and a 45-minute validation reserve gave 12,720 s, within the 17,745 s then remaining. The measured simultaneous benchmark RSS passed the frozen memory rule. Only after that addendum were the two production workers launched.

One first production attempt stopped at its first five-iteration checkpoint callback because the adapter used the wrong argument signature; it wrote no χ192 checkpoint and yielded no scientific state. Its logs and JSON are preserved. A corrected serializer was used for one same-source retry, under the *original* deadline, unchanged thresholds, and same two-worker cap. This was a code-execution correction, not an added preparation. The retry and error details are in the campaign record/addenda.

Elapsed from the initial benchmark through this report: **12.28 h** of the authorized five hours; approximate time remaining at report generation: **0.00 h**. Both accepted states and their checks completed within the cap.

Frozen and amended protocol records:

`research/transition-order/branch192-protocol.json` · SHA-256 `8e83b8ff572a9265f2771f54594b493d3918368d640fd19438fd23d9475f7a66`
`research/transition-order/branch192-execution-addendum.json` · SHA-256 `c82b822c0d86131469adb2f7319c086ee40964467c4cb6aa29e8aa9324278ac2`
`research/transition-order/branch192-retry-addendum.json` · SHA-256 `4be205213ce39ba39c80486193c9690d1fe95ac531be91532e1452911f1d0180`

Frozen model, optimizer, source-worker and comparison-helper hashes were checked: all 7/8 launch-time entries match except the final report formatter, which was changed only after computation to include the amended feasibility record and independent audit. The launch-time report-helper SHA was `d1658017c88184d6ec3c90ace7aed27c3624d00b73e6db2210c16413273b6b57`; the post-run formatter SHA is `a621738bd968f3f5a3b6ccd7d098276e7dead58e68dd6b04d9a2c26e5746043d`.
Corrected retry worker SHA-256: `e42700815197566423027c21de9078eaf655beed718e1019e0d49123b270796f`. Physics kernels and optimizer hashes remain the unchanged frozen values above.

Acceptance was not relaxed: optimizer and left/right compatibility residuals <1e−7, canonical defects <1e−9, positive full-period Rayleigh contraction with relative residual <1e−8. The internal 5e−8 target drove convergence but did not replace the external tests.

## Disposable χ192 benchmark

| Start history | VUMPS iterations | Wall time including operator setup | VUMPS-reported step time | Peak RSS | Output finite |
|---|---:|---:|---:|---:|---|
| ordered | 1 | 155.08s | 82s | 172436 KiB | True |
| disordered | 1 | 149.86s | 87s | 172308 KiB | True |

The disposable iterates were not checkpointed or used as scientific observations. The benchmark memory gate used both simultaneous peaks: 344,744 KiB combined; 1.25× this was below 0.75× available memory at the decision point. During production each process peaked near 605 MiB RSS; no memory limit was exceeded.

## Accepted χ192 results

| Start history | Iterations | Optimizer seconds | ε | Right compatibility | Color L2 | m_species | ξχ | f_half | f_period,trial |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ordered | 116 | 9355.66 | 4.806926e-08 | 4.806517e-08 | 0.4791267 | 0.5080769 | 103.26 | 0.992869795739 | 0.992869787976 |
| low-order | 72 | 6021.90 | 4.855261e-08 | 4.855856e-08 | 0.4790272 | 0.5079527 | 103.20 | 0.992869795769 | 0.992869788133 |

Independent saved-tensor audit passed for both 192×6×192 physical MPS tensors: exact checkpoint hashes and metadata; finite arrays; both mixed-canonical compatibility residuals and canonical defects recomputed; half-row objective, color diagnostic and positive full-period Rayleigh contraction recomputed. Maximum audited ε = 4.855261e-08; maximum compatibility residual = 4.856402e-08; maximum canonical defect = 6.034423e-14. This is a state-integrity/acceptance audit, not an energy-error estimate.

## Did the χ128 branch-retention behavior persist?

The operational answer for this single warm-enlargement test is **no for the low-order continuation**. At χ128 its accepted source had invariant color L2 ≈0.009027. Starting from that exact low-order source, the unconstrained χ192 warm continuation converged to color L2 = 0.4790272, similar to the ordered-source χ192 result (0.4791267). The χ128 ordered-source value had been ≈0.488232; its χ192 value remains large, ≈0.479127.

All 36 symmetry orientations were compared at χ192. The largest evaluated normalized fidelity per site was **0.999999996013**. Thus these two independently initialized-and-optimized χ192 records are numerically almost the same symmetry orbit, rather than a retained ordered/low-order pair. This supports a finite-χ optimizer-basin merger/loss of the low-order continuation under this precise enlargement path. It does **not** establish that no low-order χ192 stationary state exists: no constrained search, alternative restart ensemble, or stability campaign was authorized.

For the two accepted states, Δf_half (ordered-start minus low-order-start) = **-3.06121795e-11**; the separately retained full-period trial difference is **-1.57154734e-10**. These differences are tiny between near-identical MPS constructions. Do not interpret their arithmetic sign as a coexistence crossing, pressure bracket, or ranking with quantified uncertainty.

## Limits and interpretation

An accepted VUMPS state is a finite-χ variational construction, not a global-minimum certificate. Optimizer residuals, canonical defects and contraction residuals are not free-energy error bars. Similarity at one rate and χ does not prove uniqueness. Loss of this continuation at χ=192 does not prove a continuous transition or physical instability; likewise, its χ=128 persistence did not prove a thermodynamic metastable phase. There is still no same-objective finite-χ crossing bracket, perturbation stability result, χ→∞ extrapolation or thermodynamic order verdict.

**Transition order remains unresolved.** This test used one p only; no more rates or stability tests are included. The governing Qur’anic/Lighthouse interpretation remains separate from physics: real dependent creation is distinct from the uncreated Creator; no quantum state or algebra is identified with God.

### Durable artifacts

- `v2.2/verify/replica/n3_branch192.json` — campaign aggregate, gate history, accepted pair and symmetry comparison.
- `v2.2/verify/replica/branch192_state_audit.json` — independent tensor/gate audit.
- `v2.2/verify/replica/checkpoints/branch192_retry1_ordered_p0.3048000.npz` and `...branch192_retry1_disordered_p0.3048000.npz` — retained real χ192 state tensors.
- `v2.2/verify/replica/n3_branch192_attempt1.json` and `branch192_retry1_*.log` — retained failed serializer attempt and corrected-run logs.
- `research/transition-order/branch192.csv` — compact result data.

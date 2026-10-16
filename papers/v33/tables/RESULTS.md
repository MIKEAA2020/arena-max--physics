## Completed χ = 96 extension

| p | χ | f_b | m_species | abs(m_parity) | ξ_χ |
|---|---:|---:|---:|---:|---:|
| 0.3047 | 48 | 0.99254674 | 0.57473 | 0.39649 | 22.8 |
| 0.3047 | 72 | 0.99254592 | 0.56439 | 0.38740 | 33.6 |
| 0.3047 | 96 | 0.99254575 | 0.56065 | 0.38425 | 41.2 |
| 0.3048 | 48 | 0.99287146 | 0.55689 | 0.38005 | 25.6 |
| 0.3048 | 72 | 0.99287032 | 0.53636 | 0.36261 | 41.6 |
| 0.3048 | 96 | 0.99287002 | 0.52503 | 0.35331 | 56.8 |
| 0.3050 | 48 | 0.99351843 | 0.47110 | 0.30617 | 38.2 |
| 0.3050 | 72 | 0.99350864 | 0.00460 | 0.00626 | 39.1 |
| 0.3050 | 96 | 0.99350654 | 0.00065 | 0.00006 | 45.4 |

A **linear branch-model** crossing using slopes 3.2427 and 3.152 gives p* ≈ 0.30487; this is not a direct coexistence measurement. The retained numerical locator is p_c ≈ 0.3049(2).

## Tilted-SMC pilot at p = 0.305, β = 2

| L | particles | periods | seeds | mean Λ_L | incremental ESS / M | distinct mid-time ancestors / run |
|---:|---:|---:|---:|---:|---:|---:|
| 32 | 2000 | 128 | 2 | -0.246421 | 0.69 | 22–28 |
| 64 | 1200 | 192 | 2 | -0.247334 | 0.52 | 4–5 |
| 128 | 600 | 128 | 2 | -0.246897 | 0.35 | 1–2 |

**Read this as a sampling diagnostic, not as a coexistence result.** The normalizers have finite-L, finite-T and finite-population effects. The ancestor counts, not the number of duplicated descendants, indicate how little independent history remains in the interior.

## Population control at L = 32, p = 0.305, β = 2, T = 128

| particles | independent seeds | mean Λ_L | between-seed SEM | mean distinct mid-time ancestors |
|---:|---:|---:|---:|---:|
| 1000 | 2 | -0.246584 | 0.000140 | 19.0 |
| 4000 | 2 | -0.246485 | 0.000004 | 64.5 |
| 16000 | 2 | -0.246325 | 0.000029 | 176.0 |

Two seeds do not provide reliable systematic error bars. The population-dependent drift and the poor L = 64–128 genealogies prevent a phase-order claim.

## Fixed-seed small-system validation

| L | p | β | T | estimate | between-run SEM | exact finite-time target |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 0.160 | 1 | 2 | 0.032957345 | 0.000015283 | 0.032961721 |
| 8 | 0.160 | 2 | 32 | -0.121920260 | 0.000019444 | -0.121924372 |
| 8 | 0.220 | 2 | 32 | -0.169636443 | 0.000017709 | -0.169612662 |
| 12 | 0.160 | 2 | 48 | -0.123862789 | 0.000004770 | -0.123856677 |
| 16 | 0.220 | 2 | 64 | -0.173888665 | 0.000010031 | -0.173901000 |
| 8 | 0.305 | 2 | 32 | -0.237179973 | 0.000058435 | -0.237048017 |
| 12 | 0.305 | 2 | 48 | -0.241684496 | 0.000062325 | -0.241720161 |

The first row is E[2^(−N_rand)], not Λ. Other rows are Λ = log E[2^(−β N_rand)] / (2LT). All targets except the rounded L = 16, β = 2 v32 anchor are independently contracted with the physical product-state temporal boundary. Errors use the sample standard deviation (ddof = 1). Passing stochastic regressions validates these cases; it is not an exact-arithmetic certificate or a proof of efficient rare-event estimation.

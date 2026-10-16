#!/usr/bin/env python3
"""Build review tables directly from stored runs; no numerical solver is rerun."""
from pathlib import Path
import json,csv,statistics,math
R=Path(__file__).resolve().parents[2]/'v2.2/verify/replica'
O=Path(__file__).resolve().parent/'tables';O.mkdir(exist_ok=True)

def csvwrite(name,rows):
 with (O/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

chi=[]
for name in ['ord','mid','dis']:
 d=json.loads((R/f'vumps_n3_chi96_{name}.json').read_text())
 for r in sorted(d.values(),key=lambda x:x['chi']):
  chi.append(dict(p=r['p'],chi=r['chi'],f_b=r['f'],m_species=r['m_species'],abs_m_parity=abs(r['m_parity']),
                  xi_chi=r['xi_chi'],S_MPS=r['S_ent'],iterations=r['iters'],seconds=r['seconds']))
csvwrite('chi96.csv',chi)
md=['## Completed χ = 96 extension','', '| p | χ | f_b | m_species | abs(m_parity) | ξ_χ |', '|---|---:|---:|---:|---:|---:|']
for r in chi:
 md.append(f"| {r['p']:.4f} | {r['chi']} | {r['f_b']:.8f} | {r['m_species']:.5f} | {r['abs_m_parity']:.5f} | {r['xi_chi']:.1f} |")
ord96=next(r for r in chi if r['chi']==96 and r['p']==.3048)
dis96=next(r for r in chi if r['chi']==96 and r['p']==.305)
a=3.2427;b=3.152
pc=.3048+(dis96['f_b']-b*.0002-ord96['f_b'])/(a-b)
md+=['',f"A **linear branch-model** crossing using slopes {a} and {b} gives p* ≈ {pc:.5f}; this is not a direct coexistence measurement. The retained numerical locator is p_c ≈ 0.3049(2).",'']

pilot=[]
recs=[]
for fn in ['smc_pilot_L32_64.json','smc_pilot_L128.json']:
 recs+=json.loads((R/fn).read_text())
for L in [32,64,128]:
 rs=[r for r in recs if r['L']==L and r['beta']==2 and abs(r['p']-.305)<1e-9]
 pilot.append(dict(L=L,M=rs[0]['M'],T=rs[0]['T'],seeds=len(rs),Lambda_mean=statistics.mean(r['Lambda'] for r in rs),
                   ESS_fraction=statistics.mean(r['ess_mean']/r['M'] for r in rs),
                   midpoint_ancestors_min=min(r['n_distinct_lineages'][r['T']//2] for r in rs),
                   midpoint_ancestors_max=max(r['n_distinct_lineages'][r['T']//2] for r in rs)))
csvwrite('smc-pilot.csv',pilot)
md+=['## Tilted-SMC pilot at p = 0.305, β = 2','', '| L | particles | periods | seeds | mean Λ_L | incremental ESS / M | distinct mid-time ancestors / run |', '|---:|---:|---:|---:|---:|---:|---:|']
for r in pilot:
 md.append(f"| {r['L']} | {r['M']} | {r['T']} | {r['seeds']} | {r['Lambda_mean']:.6f} | {r['ESS_fraction']:.2f} | {r['midpoint_ancestors_min']}–{r['midpoint_ancestors_max']} |")
md+=['', '**Read this as a sampling diagnostic, not as a coexistence result.** The normalizers have finite-L, finite-T and finite-population effects. The ancestor counts, not the number of duplicated descendants, indicate how little independent history remains in the interior.','']

pop=[];d=json.loads((R/'smc_population.json').read_text())
for M in sorted(set(r['M'] for r in d)):
 rs=[r for r in d if r['M']==M];vals=[r['Lambda'] for r in rs]
 pop.append(dict(L=32,p=.305,M=M,T=128,seeds=len(rs),Lambda_mean=statistics.mean(vals),
                 Lambda_sem=statistics.stdev(vals)/math.sqrt(len(vals)),
                 midpoint_ancestors_mean=statistics.mean(r['n_distinct_lineages'][r['T']//2] for r in rs),
                 bulk_random_density_mean=statistics.mean(r['bulk_rand_mid'] for r in rs)))
csvwrite('smc-population.csv',pop)
md+=['## Population control at L = 32, p = 0.305, β = 2, T = 128','', '| particles | independent seeds | mean Λ_L | between-seed SEM | mean distinct mid-time ancestors |','|---:|---:|---:|---:|---:|']
for r in pop:
 md.append(f"| {r['M']} | {r['seeds']} | {r['Lambda_mean']:.6f} | {r['Lambda_sem']:.6f} | {r['midpoint_ancestors_mean']:.1f} |")
md+=['', 'Two seeds do not provide reliable systematic error bars. The population-dependent drift and the poor L = 64–128 genealogies prevent a phase-order claim.','']

v=json.loads((R/'smc_validation_v33.json').read_text())
vs=[{k:r[k] for k in ['L','p','beta','M','T','nseed','mean','sem','exact','exact_source']} for r in v]
csvwrite('smc-validation.csv',vs)
md+=['## Fixed-seed small-system validation','', '| L | p | β | T | estimate | between-run SEM | exact finite-time target |','|---:|---:|---:|---:|---:|---:|---:|']
for r in v:
 md.append(f"| {r['L']} | {r['p']:.3f} | {r['beta']} | {r['T']} | {r['mean']:.9f} | {r['sem']:.9f} | {r['exact']:.9f} |")
md+=['', 'The first row is E[2^(−N_rand)], not Λ. Other rows are Λ = log E[2^(−β N_rand)] / (2LT). All targets except the rounded L = 16, β = 2 v32 anchor are independently contracted with the physical product-state temporal boundary. Errors use the sample standard deviation (ddof = 1). Passing stochastic regressions validates these cases; it is not an exact-arithmetic certificate or a proof of efficient rare-event estimation.']
(O/'RESULTS.md').write_text('\n'.join(md)+'\n')
print(O/'RESULTS.md')

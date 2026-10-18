#!/usr/bin/env python3
"""Report the χ192 p=.304825 paired-history retention test."""
from pathlib import Path
import json,csv,importlib.util
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
p=json.loads((HERE/'branch192-mid-pair-protocol.json').read_text());db=json.loads((R/'n3_branch192_mid_pair.json').read_text())
bench=db.get('benchmarks',{});g=db.get('feasibility_gate',{});results=db.get('results',{});audits=db.get('audits',{})
fmt=lambda x,n=9:'—' if x is None else f'{float(x):.{n}f}'
lines=['# χ192 paired-history test at p=.304825','',
'17 October 2026 · separately authorized paired one-rate test · finite-χ branch-retention evidence only.','',
f"**Status:** {db.get('status')}.",'',
'## Authorization and protocol','',
'The user authorized one rate with two ordered histories, run sequentially by one single-thread worker under a fresh 12-hour absolute cap. The ordered preparation starts from the accepted χ192 p=.30480 state; the small-order preparation starts from the accepted χ192 p=.30485 state. Both target p=.304825 with identical gates and objective. No other rate, gap/excited-state, perturbation or stability calculation is included.','',
'These histories test whether both numerical characters are retained at the same finite χ and same p. A two-state result at one p does not itself locate a coexistence crossing or determine transition order.','',
f"Ordered source: `{p['sources']['ordered']['checkpoint']}` (SHA-256 `{p['sources']['ordered']['sha256']}`, source color L2 {p['sources']['ordered']['color_l2_order']:.8f}).",
f"Small-order source: `{p['sources']['small']['checkpoint']}` (SHA-256 `{p['sources']['small']['sha256']}`, source color L2 {p['sources']['small']['color_l2_order']:.8f}).",
'Execution provenance: the accepted small-order state resumes from the verified p=.304825 iteration-40 checkpoint. Its reported 199 cumulative iterations are for that accepted checkpoint lineage; the separate earlier no-checkpoint 65-iteration attempt is not added to these counts. The resume used the same preparation and rate, not an extra branch or rate.','',
'Acceptance gates remain unchanged: optimizer and both compatibility residuals <1e−7, canonical defects <1e−9, positive full-period trial contraction with relative defect <1e−8.','',
'## Disposable benchmarks and feasibility gate','']
for name in ['ordered','small']:
 b=bench.get(name,{})
 lines.append(f"- **{name}:** {b.get('iterations','—')} step(s), {fmt(b.get('seconds_per_iteration'),2)} s/step, wall {fmt(b.get('wall_seconds'),2)} s, peak RSS {b.get('peak_rss_kib','—')} KiB; no state checkpoint written.")
lines += [f"\nForecast for both preparations including setup and validation reserves: {fmt(g.get('forecast_seconds'),2)} s versus {fmt(g.get('remaining_seconds'),2)} s remaining; headroom {fmt(g.get('headroom_seconds'),2)} s. Memory gate passed={g.get('memory_passed','—')} (forecast peak {g.get('forecast_peak_rss_kib','—')} KiB; available {g.get('mem_available_kib','—')} KiB). Decision: **{g.get('decision','pending')}**.",'']
if results:
 lines += ['## Same-rate state outcomes','', '| Preparation | Reported status | Iterations | eps | Max compatibility | Max canonical defect | Color L2 | m_species | ξχ | f_half | f_period,trial | Audit record / current tensor |','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
 for name in ['ordered','small']:
  r=results.get(name,{})
  lines.append(f"| {name} | accepted finite-chi state reported | {r.get('iters','—')} | {fmt(r.get('eps'),8)} | {fmt(max(r.get('gauge_left_residual',0),r.get('gauge_right_residual',0)),8) if r else '—'} | {fmt(max(r.get('left_canonical_residual',0),r.get('right_canonical_residual',0)),3) if r else '—'} | {fmt(r.get('color_l2_order'),8)} | {fmt(r.get('m_species'),8)} | {fmt(r.get('xi_chi'),3)} | {fmt(r.get('f_half'),12)} | {fmt(r.get('f_full_rayleigh'),12)} | historical audit pass; final file missing |")
 if all(results.get(n,{}).get('converged') for n in ['ordered','small']):
  ro,rs=results['ordered'],results['small'];dc=abs(ro['color_l2_order']-rs['color_l2_order']);df=ro['f_half']-rs['f_half']
  lines += ['',f"Same-p invariant-order separation |Δcolor L2| = {dc:.8g}. Same-objective half-row difference Δf_half (ordered−small) = {df:.12g}. These are finite-χ numerical state diagnostics, not calibrated uncertainty or a thermodynamic crossing. Full-period Rayleigh trial values remain a separate objective.",'']
else:
 lines += ['', 'No production result is available; a disposable benchmark is not a numerical state.','']
lines += ['## Cross-rate χ192 context','',
'The accepted χ192 p=.30480 pair converged to nearly the same large-order state; the low-order-start path was not retained as a distinct low-order state. At p=.304825, the two authorized histories produced clearly separated accepted states (color L2 0.42451 versus 0.000624). At p=.30485, the ordered-start retry ended in the small-order state. Thus, among these sampled warm-history outcomes, p=.304825 is the first χ192 point with a retained pair, between the sampled .30480 and .30485 outcomes.','',
'A useful shorthand is a **coarse sampled finite-χ warm-history change zone** of approximately (.30480, .30485), with distinct-state retention demonstrated at .304825. The spacing from .304825 to either sampled endpoint is 2.5×10⁻⁵. This is not a measured two-branch stability interval: the endpoints are path outcomes, not mapped boundaries, and no local stability or thermodynamic coexistence test was done. The actual retention limits could differ.','',
'At χ128 and p=.304825, Δf_half (ordered−disordered) = −4.359393×10⁻⁷; at χ192, Δf_half (ordered−small) = +3.590992×10⁻⁷. The magnitudes are of the same order but the sign changes with χ. These are not calibrated errors or a crossing bracket.','',
'## Interpretation','',
'This pattern strengthens a **first-order-like finite-χ reading** relative to the earlier χ192 .30480 result alone: two distinguishable states are now retained at one common rate, while the sampled warm paths change character at neighboring rates. It is compatible with a narrow metastable-branch picture if the transition is first-order. A continuous transition with a small exponent β, together with finite-χ crossover or long-lived numerical configurations, remains possible. The current data cannot distinguish these explanations or place the thermodynamic critical point inside the sampled interval.','',
'Optimizer residuals are not free-energy error bars. A VUMPS state is not a global-minimum certificate. The evidence is finite-χ warm-history retention at one sampled rate, not thermodynamic metastability, global optimality, or transition order.','',
'> **Ledger:** χ192 at p=.304825: two distinct warm-history numerical states reported (color L2 0.4245 vs. 0.0006; Δf_half, ordered−small = +3.59×10⁻⁷). Both final accepted checkpoint files are missing; historical audit records say “passed,” but the final tensors cannot now be independently reopened. Coarse sampled warm-history change zone: .30480–.30485, with pair retention at .304825; not a thermodynamic window or coexistence bracket. First-order-like narrow-window reading strengthened; continuous transition with small β remains live. **Transition order unresolved.**','',
'## Follow-up status','',
'One additional lower-side probe was authorized and selected at χ192 p=.30481 (closer to .30480 than .304815). Disposable benchmarks measured 101.90 s/step for the ordered source and 99.23 s/step for the small-order source; the memory gate passed. The first ordered process ended before its first saved checkpoint, with no iteration or residual recorded. Its restart reached iteration 5 (ε=4.7849577×10⁻⁶; 354.871 optimizer seconds) and wrote a valid p=.30481 checkpoint (SHA-256 `816854bdd9b8c5824ef39d0b4a687836cd45d83a8e8d76a605d4dbecd959c786`), but the process was later unavailable; the exact termination cause is unknown. The same ordered preparation is resuming from that saved p=.30481 state, preserving cumulative iterations and optimizer time, then the small-order history will run sequentially. The original 14-hour deadline is retained, not reset; a recovery worker now checkpoints every iteration. No converged result is available yet. Provenance is in `chi192-p30481/ordered-attempt1-interruption.json`, `ordered-attempt2-interruption.json`, and `ordered-attempt3-resume.json`. This run cannot restore the missing p=.304825 tensors. The alternative .304815 and χ256 campaign have not been run.','',
'Artifacts: `v2.2/verify/replica/n3_branch192_mid_pair.json`, surviving source checkpoints, audit records, disposable benchmarks/logs, and `branch192-mid-pair-protocol.json`.','']
if db.get('artifact_integrity_note'):
 lines += ['## Artifact availability note','',db['artifact_integrity_note'],'']
(HERE/'BRANCH192-MID-PAIR-RESULTS.md').write_text('\n'.join(lines))
fields=['campaign','status','p','chi','preparation','iters','eps','color_l2_order','m_species','xi_chi','f_half','f_full_rayleigh','audit_record_status','final_checkpoint_present','checkpoint_sha256']
with (HERE/'branch192-mid-pair.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
 for name in ['ordered','small']:
  r=results.get(name,{})
  w.writerow({'campaign':p['campaign'],'status':'reported accepted finite-chi numerical state','p':p['p'],'chi':p['chi'],'preparation':name,'iters':r.get('iters'),'eps':r.get('eps'),
   'color_l2_order':r.get('color_l2_order'),'m_species':r.get('m_species'),'xi_chi':r.get('xi_chi'),'f_half':r.get('f_half'),'f_full_rayleigh':r.get('f_full_rayleigh'),
   'audit_record_status':'historical audit record passed','final_checkpoint_present':False,'checkpoint_sha256':r.get('checkpoint_sha256')})
spec=importlib.util.spec_from_file_location('md2docx',ROOT/'v2.2/md2docx.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);out=HERE/'branch192-mid-pair-report.docx';m.convert(str(HERE/'BRANCH192-MID-PAIR-RESULTS.md'),str(out))
from docx import Document
from docx.shared import Cm
D=Document(out)
for sec in D.sections:sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
D.core_properties.title='χ192 paired histories at p=.304825';D.save(out)
print(json.dumps(dict(status=db.get('status'),preparations=list(results),audits=audits,report=str(HERE/'BRANCH192-MID-PAIR-RESULTS.md'))))

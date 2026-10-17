#!/usr/bin/env python3
"""Report the fresh six-hour χ192 ordered-history p=.30485 retry."""
from pathlib import Path
import json,csv,importlib.util
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
p=json.loads((HERE/'branch192-upper-retry1-protocol.json').read_text());db=json.loads((R/'n3_branch192_upper_retry1.json').read_text())
b=db.get('benchmark',{});g=db.get('feasibility_gate',{});r=db.get('result') or {}
fmt=lambda x,n=9:'—' if x is None else f'{float(x):.{n}f}'
lines=['# Fresh χ192 ordered-history continuation at p=.30485','',
'17 October 2026 · separately authorized fresh six-hour attempt · one rate, one preparation, finite-χ only.','',
f"**Status:** {db.get('status')}.",'',
'## Authorization, source and cap','',
'The prior six-hour attempt ended without a final record or target checkpoint. The user then explicitly authorized one fresh attempt under a new six-hour absolute cap, starting with a new disposable benchmark. This attempt reuses only the accepted ordered χ192 p=.30480 checkpoint; it does not resume or overwrite the interrupted attempt. No other rate, preparation, gap/excited-state calculation, perturbation or stability test is authorized.','',
f"Source checkpoint: `{p['source']['checkpoint']}`; SHA-256 `{p['source']['sha256']}`; source color L2 {p['source']['source_color_l2']:.8f}.",
f"Same-rate iteration reference: accepted χ128 ordered p=.30485 in {p['chi128_same_p_upper_reference']['iterations']} iterations; used only for conservative runtime forecasting.",'',
'Acceptance gates remain unchanged: optimizer and both compatibility residuals <1e−7, canonical defects <1e−9, positive full-period trial contraction with relative defect <1e−8.','',
'## Disposable benchmark and feasibility gate','',
f"Benchmark: {b.get('iterations','—')} step(s), {fmt(b.get('seconds_per_iteration'),2)} s/iteration, wall {fmt(b.get('wall_seconds'),2)} s, peak RSS {b.get('peak_rss_kib','—')} KiB, finite={b.get('finite_output','—')}; no benchmark checkpoint was written.",
f"Forecast: {g.get('forecast_iterations','—')} × {fmt(g.get('per_iteration_seconds'),2)} s + {g.get('setup_reserve_seconds',p['setup_reserve_seconds'])} s setup + {g.get('validation_reserve_seconds',p['validation_reserve_seconds'])} s validation = {fmt(g.get('forecast_seconds'),2)} s versus {fmt(g.get('remaining_seconds'),2)} s remaining; headroom {fmt(g.get('headroom_seconds'),2)} s. Memory passed={g.get('memory_passed','—')}. Decision: **{g.get('decision','pending')}**.",'']
if r:
 lines += ['## Production result','',
 '| Status | Iterations | eps | Right compatibility | Color L2 | m_species | ξχ | f_half | f_period,trial |','|---|---:|---:|---:|---:|---:|---:|---:|---:|',
 f"| {r.get('status')} | {r.get('iters','—')} | {fmt(r.get('eps'),8)} | {fmt(r.get('gauge_right_residual'),8)} | {fmt(r.get('color_l2_order'),8)} | {fmt(r.get('m_species'),8)} | {fmt(r.get('xi_chi'),3)} | {fmt(r.get('f_half'),12)} | {fmt(r.get('f_full_rayleigh'),12)} |",'']
 if db.get('audit_status')=='passed':
  a=json.loads((R/'branch192_upper_retry1_state_audit.json').read_text())
  lines += [f"Independent saved-state audit passed: ε={a['eps']:.3e}, max compatibility={max(a['gauge_left_residual'],a['gauge_right_residual']):.3e}, max canonical={max(a['left_canonical_residual'],a['right_canonical_residual']):.3e}, period residual={a['period_contraction_relative_residual']:.3e}.",'']
else:
 lines += ['No final production state is recorded. A benchmark or incomplete worker record is not a scientific observation.','']
lines += ['## Interpretation','',
'This is a one-point, one-history finite-χ continuation, not a global-minimum certificate or transition verdict. Numerical residuals and contraction residuals are acceptance diagnostics, not free-energy error bars. A single rate cannot locate a spinodal or determine transition order. No follow-up rate or stability/gap calculation is inferred.','',
'Artifacts: `v2.2/verify/replica/n3_branch192_upper_retry1.json`, `branch192_upper_retry1_benchmark.json`, worker logs, and—only if a production state is saved—the retry1 checkpoint and independent audit.','']
(HERE/'BRANCH192-UPPER-RETRY1-RESULTS.md').write_text('\n'.join(lines))
fields=['campaign','status','p','chi','source_checkpoint','benchmark_seconds_per_iteration','forecast_seconds','remaining_seconds','production_authorized','production_status','converged','iters','eps','color_l2_order','f_half','f_full_rayleigh']
with (HERE/'branch192-upper-retry1.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerow({'campaign':p['campaign'],'status':db.get('status'),'p':p['p'],'chi':p['chi'],'source_checkpoint':p['source']['checkpoint'],
 'benchmark_seconds_per_iteration':b.get('seconds_per_iteration'),'forecast_seconds':g.get('forecast_seconds'),'remaining_seconds':g.get('remaining_seconds'),
 'production_authorized':g.get('production_authorized'),'production_status':r.get('status'),'converged':r.get('converged'),'iters':r.get('iters'),'eps':r.get('eps'),
 'color_l2_order':r.get('color_l2_order'),'f_half':r.get('f_half'),'f_full_rayleigh':r.get('f_full_rayleigh')})
spec=importlib.util.spec_from_file_location('md2docx',ROOT/'v2.2/md2docx.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);out=HERE/'branch192-upper-retry1-report.docx';m.convert(str(HERE/'BRANCH192-UPPER-RETRY1-RESULTS.md'),str(out))
from docx import Document
from docx.shared import Cm
D=Document(out)
for sec in D.sections:sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
D.core_properties.title='Fresh χ192 p=.30485 ordered-history continuation';D.save(out)
print(json.dumps(dict(status=db.get('status'),production_authorized=g.get('production_authorized'),report=str(HERE/'BRANCH192-UPPER-RETRY1-RESULTS.md'))))

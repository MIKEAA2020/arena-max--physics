#!/usr/bin/env python3
"""Human-readable record of the single-rate χ192 .30485 feasibility test."""
from pathlib import Path
import json,hashlib,math,importlib.util
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
db=json.loads((R/'n3_branch192_upper.json').read_text());p=json.loads((HERE/'branch192-upper-protocol.json').read_text())
def fmt(x,d=10):return '—' if x is None else f'{float(x):.{d}f}'
def sha(x):return hashlib.sha256(Path(x).read_bytes()).hexdigest()
b=db.get('benchmark',{});gate=db.get('feasibility_gate',{});r=db.get('result') or {}
lines=['# χ192 single ordered-history step at p=.30485','',
'17 October 2026 · separately authorized one-rate continuation · finite-χ test, not a transition verdict.','',
f"**Status:** {db.get('status')}.",'',
'## Scope and cap','',
'The user authorized exactly one ordered-history χ192 continuation at p=.30485, warm-started from the accepted ordered χ192 state at p=.30480. This is a fresh five-hour absolute cap. The disposable enlargement benchmark and runtime/memory gate precede production; if the projected optimizer plus setup and validation reserve does not fit, production is not launched. No other p, second preparation, excited-state/gap computation, perturbation or stability test is in scope.', '',
'Acceptance remains unchanged: primary and both compatibility residuals <1e−7, canonical defects <1e−9, positive full-period trial contraction with relative defect <1e−8.','',
'## Frozen references','',
f"Accepted χ192 source: `{p['source']['checkpoint']}`, SHA-256 `{p['source']['sha256']}`; source order diagnostic L2 = {p['source']['source_color_l2']:.8f}.",
f"Same-p χ128 upper-rate reference: `{p['chi128_same_p_upper_reference']['checkpoint']}`, accepted in {p['chi128_same_p_upper_reference']['iterations']} iterations at p=.30485, terminal color L2 {p['chi128_same_p_upper_reference']['final_color_l2']:.8f}. This is the prior upper-rate warm-history reference, not a χ192 result.",'',
'## Disposable one-step benchmark','',
f"Iterations: {b.get('iterations','—')}; VUMPS time per step: {fmt(b.get('seconds_per_iteration'),2)}s; total wall time including operator construction: {fmt(b.get('wall_seconds'),2)}s; peak RSS: {b.get('peak_rss_kib','—')} KiB; finite output: {b.get('finite_output','—')}. No state checkpoint was written.",'',
'## Feasibility decision','',
f"Projection: {gate.get('forecast_iterations','—')} iterations × {fmt(gate.get('per_iteration_seconds'),2)}s/step + {gate.get('setup_reserve_seconds',p['setup_reserve_seconds'])}s setup + {gate.get('validation_reserve_seconds',p['validation_reserve_seconds'])}s validation = {fmt(gate.get('forecast_seconds'),2)}s, versus {fmt(gate.get('remaining_seconds'),2)}s remaining after benchmark.",
f"Memory forecast: measured peak {gate.get('peak_rss_kib','—')} KiB; available memory {gate.get('mem_available_kib','—')} KiB. Gate decision: **{gate.get('decision','pending')}**.",'']
if r:
 lines+=['## Production result','',
 '| Status | Iterations | Optimizer residual | Right compatibility | Color L2 | m_species | ξχ | f_half | f_period,trial |','|---|---:|---:|---:|---:|---:|---:|---:|---:|',
 f"| {r.get('status')} | {r.get('iters','—')} | {fmt(r.get('eps'),8)} | {fmt(r.get('gauge_right_residual'),8)} | {fmt(r.get('color_l2_order'),8)} | {fmt(r.get('m_species'),8)} | {fmt(r.get('xi_chi'),3)} | {fmt(r.get('f_half'),12)} | {fmt(r.get('f_full_rayleigh'),12)} |",'']
 if db.get('audit_status')=='passed':
  au=json.loads((R/'branch192_upper_state_audit.json').read_text())
  lines += [f"Independent saved-state audit passed: ε={au['eps']:.3e}, max compatibility={max(au['gauge_left_residual'],au['gauge_right_residual']):.3e}, max canonical={max(au['left_canonical_residual'],au['right_canonical_residual']):.3e}, period residual={au['period_contraction_relative_residual']:.3e}.",'']
 lines += ['This is a single unconstrained warm continuation. Its order diagnostic is not a ground-state certificate. A change or persistence at one p does not locate a spinodal, prove a stationary branch absent, determine a collapse point, or classify the thermodynamic transition. No next rate or gap/stability measurement is inferred.']
else:
 lines += ['**No optimizer state at p=.30485 was produced.** Only the disposable one-step benchmark ran. The feasibility gate stopped before production; therefore there is no p=.30485 order diagnostic or phase inference.']
lines += ['',
'## Interpretation','',
'Comparison to χ128 is only a one-point, one-history finite-χ retention check. If a production optimizer was launched and retained high order, that would show this warm path remains ordered at .30485; if it lost order, that would show only that this unconstrained optimizer path changed character. Neither case identifies the thermodynamic transition point or order.', '',
'All optimizer residuals and transfer-contraction residuals are numerical acceptance diagnostics, not free-energy error bars. A VUMPS state is not certified globally minimal. Transition order remains unresolved.', '',
'Artifacts: `v2.2/verify/replica/n3_branch192_upper.json`, `branch192_upper_benchmark.json`, its log, and (only if production passed the gate) the named `.30485` result/checkpoint plus `branch192_upper_state_audit.json`.','']
(HERE/'BRANCH192-UPPER-RESULTS.md').write_text('\n'.join(lines))
with (HERE/'branch192-upper.csv').open('w',newline='') as f:
 import csv
 fields=['campaign','status','p','chi','source_checkpoint','benchmark_seconds_per_iteration','forecast_seconds','remaining_seconds','production_launched','converged','iters','eps','color_l2_order','f_half','f_full_rayleigh']
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
 row={'campaign':p['campaign'],'status':db.get('status'),'p':p['p'],'chi':p['chi'],'source_checkpoint':p['source']['checkpoint'],
  'benchmark_seconds_per_iteration':b.get('seconds_per_iteration'),'forecast_seconds':gate.get('forecast_seconds'),'remaining_seconds':gate.get('remaining_seconds'),
  'production_launched':bool(r),'converged':r.get('converged'),'iters':r.get('iters'),'eps':r.get('eps'),'color_l2_order':r.get('color_l2_order'),'f_half':r.get('f_half'),'f_full_rayleigh':r.get('f_full_rayleigh')};w.writerow(row)
spec=importlib.util.spec_from_file_location('md2docx',ROOT/'v2.2/md2docx.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);out=HERE/'branch192-upper-report.docx';m.convert(str(HERE/'BRANCH192-UPPER-RESULTS.md'),str(out))
from docx import Document
from docx.shared import Cm,Pt
D=Document(out)
for sec in D.sections:sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
D.core_properties.title='χ192 single upper-rate step at p=.30485';D.save(out)
print(json.dumps(dict(status=db.get('status'),production_launched=bool(r),report=str(HERE/'BRANCH192-UPPER-RESULTS.md'))))

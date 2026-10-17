#!/usr/bin/env python3
"""Supersede the initial feasibility-only report with the post-extension interruption record."""
from pathlib import Path
import runpy,json,csv,importlib.util,hashlib,re
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
runpy.run_path(str(HERE/'branch192_upper_report.py'),run_name='__main__')
p=json.loads((HERE/'branch192-upper-protocol.json').read_text());e=json.loads((HERE/'branch192-upper-extension-addendum.json').read_text());i=json.loads((HERE/'branch192-upper-interruption.json').read_text());db=json.loads((R/'n3_branch192_upper.json').read_text());g=e['extended_gate']
md=HERE/'BRANCH192-UPPER-RESULTS.md';text=md.read_text()
text=text.replace('**Status:** production interrupted without final record; no target checkpoint.','**Current status:** the original five-hour gate failed; a later authorized one-hour extension passed and launched production. The worker then disappeared without a final result or saved target checkpoint. The six-hour absolute cap has now expired; there is no accepted p=.30485 χ192 observation.')
text=text.replace('This is a fresh five-hour absolute cap. The disposable enlargement benchmark and runtime/memory gate precede production; if the projected optimizer plus setup and validation reserve does not fit, production is not launched.','The initial authorization set a fresh five-hour cap. A later addendum extended the absolute cap to six hours from the original start. The disposable enlargement benchmark and runtime/memory gate preceded production; the original gate failed, then the extension gate passed.')
text=text.replace('Artifacts: `v2.2/verify/replica/n3_branch192_upper.json`, `branch192_upper_benchmark.json`, its log, and (only if production passed the gate) the named `.30485` result/checkpoint plus `branch192_upper_state_audit.json`.','Artifacts: `v2.2/verify/replica/n3_branch192_upper.json`, the worker execution record and log, and `research/transition-order/branch192-upper-interruption.json`. No accepted target checkpoint, final optimizer record, or independent state audit exists.')
text=text.replace('## Feasibility decision','## Original five-hour feasibility decision (preserved)')
text=text.replace('**No optimizer state at p=.30485 was produced.** Only the disposable one-step benchmark ran. The feasibility gate stopped before production; therefore there is no p=.30485 order diagnostic or phase inference.','**Historical note:** at the original five-hour gate, no optimizer state had been produced and production had not launched. A later cap-extension decision superseded that stop; see the execution update below. No accepted or audited p=.30485 state is available.')
section=(
'## One-hour extension and subsequent execution interruption\n\n'
'The user authorized one additional hour, changing the absolute cap from five to six hours measured from the original campaign start. The original frozen protocol and failed five-hour gate remain unchanged. The extension gate reused the disposable benchmark and unchanged forecast: '
+f"{g['forecast_iterations']} iterations × {g['per_iteration_seconds']:.2f}s plus setup and validation = {g['forecast_seconds']:.2f}s. At the extension decision, {g['remaining_seconds']:.2f}s remained; forecast headroom was {g['headroom_seconds']:.2f}s. Runtime and memory gates passed, and the single production worker was launched.\n\n"
+f"Afterward, the worker no longer appeared in the process table. Its durable result record remains at status `{i['last_worker_record_state']}`; its log is {i['worker_log_bytes']} bytes, and the named p=.30485 checkpoint exists: {i['target_checkpoint_exists']}. The actual number of optimizer iterations completed is unknown; no final result or independent state audit exists. The six-hour deadline expired at Unix time {e['extended_deadline_unix']:.0f} before this interruption was documented. **No restart is authorized by the expired cap.** A renewed explicit cap is required before another attempt.\n\n"
+f"Interruption evidence: `research/transition-order/branch192-upper-interruption.json`; extension authorization/gate: `branch192-upper-extension-addendum.json`.\n\n")
anchor='## Interpretation'
if '## One-hour extension and subsequent execution interruption' not in text:
 if anchor not in text:raise SystemExit('Report insertion anchor missing')
 text=text.replace(anchor,section+anchor,1)
md.write_text(text)
# Keep the compact data record consistent with the post-extension execution state.
fields=['campaign','status','p','chi','source_checkpoint','benchmark_seconds_per_iteration','forecast_seconds','remaining_seconds','production_launched','converged','iters','eps','color_l2_order','f_half','f_full_rayleigh','extended_cap_seconds','extension_gate_passed','execution_status','target_checkpoint_exists']
with (HERE/'branch192-upper.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerow({
 'campaign':p['campaign'],'status':db['status'],'p':p['p'],'chi':p['chi'],'source_checkpoint':p['source']['checkpoint'],
 'benchmark_seconds_per_iteration':e['benchmark_seconds_per_iteration'],'forecast_seconds':g['forecast_seconds'],'remaining_seconds':g['remaining_seconds'],
 'production_launched':True,'converged':'','iters':'','eps':'','color_l2_order':'','f_half':'','f_full_rayleigh':'',
 'extended_cap_seconds':e['total_wall_cap_seconds'],'extension_gate_passed':g['production_authorized'],'execution_status':i['last_worker_record_state'],'target_checkpoint_exists':i['target_checkpoint_exists']})
spec=importlib.util.spec_from_file_location('md2docx',ROOT/'v2.2/md2docx.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);out=HERE/'branch192-upper-report.docx';m.convert(str(md),str(out))
from docx import Document
from docx.shared import Cm
D=Document(out)
for sec in D.sections:sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
D.core_properties.title='χ192 p=.30485 extension and interrupted run';D.save(out)
# Bind this report implementation to the interruption note without modifying the frozen extension addendum.
i['interruption_report_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();(HERE/'branch192-upper-interruption.json').write_text(json.dumps(i,indent=2)+'\n')
print(json.dumps(dict(report=str(md.relative_to(ROOT)),status=db['status'],production_launched=True,result_available=False)))

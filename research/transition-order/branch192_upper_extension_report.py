#!/usr/bin/env python3
"""Regenerate the .30485 report with the later one-hour cap-extension addendum."""
from pathlib import Path
import json,runpy,importlib.util
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica'
runpy.run_path(str(HERE/'branch192_upper_report.py'),run_name='__main__')
md=HERE/'BRANCH192-UPPER-RESULTS.md';text=md.read_text();ext=json.loads((HERE/'branch192-upper-extension-addendum.json').read_text());g=ext['extended_gate']
section=(
"## Later one-hour cap extension\n\n"
"After the original five-hour benchmark gate stopped production, the user authorized a one-hour extension, making the absolute campaign cap six hours from the original start time. The original gate and its result remain preserved above; the protocol and first benchmark were not rerun or overwritten.\n\n"
+f"The extension gate used the already completed disposable benchmark ({ext['benchmark_seconds_per_iteration']:.2f}s/iteration), the same 205-iteration hard-case reference, and the original setup/validation reserves. At the extension decision, {g['remaining_seconds']:.2f}s remained to the extended deadline versus a {g['forecast_seconds']:.2f}s forecast (headroom {g['headroom_seconds']:.2f}s); memory {g['memory_passed']}. Decision: **{g['decision']}**.\n\n"
"This amendment changes only the wall-clock cap for the already authorized single ordered χ192 p=.30485 continuation from the accepted p=.30480 source. It authorizes no other rate, preparation, gap/excited-state, perturbation, or stability calculation. The unchanged acceptance gates and all scientific caveats remain in force.\n\n"
+f"Extension addendum: `branch192-upper-extension-addendum.json`; production worker: `v2.2/verify/replica/branch192_upper_extension_worker.py`.\n\n")
anchor='## Interpretation'
if '## Later one-hour cap extension' not in text:
 if anchor not in text:raise SystemExit('Interpretation section anchor missing')
 text=text.replace(anchor,section+anchor,1)
md.write_text(text)
spec=importlib.util.spec_from_file_location('md2docx',ROOT/'v2.2/md2docx.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);out=HERE/'branch192-upper-report.docx';m.convert(str(md),str(out))
from docx import Document
from docx.shared import Cm
D=Document(out)
for sec in D.sections:sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
D.core_properties.title='χ192 single upper-rate continuation at p=.30485';D.save(out)
print(json.dumps(dict(report=str(md.relative_to(ROOT)),production_launched=bool(json.loads((R/'n3_branch192_upper.json').read_text()).get('result')),extension_decision=g['decision'])))

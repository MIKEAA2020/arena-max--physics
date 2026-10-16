#!/usr/bin/env python3
"""Refresh the physics-only review archive; the full Git repo is the complete record.
Keep accepted/control state anchors; omit duplicate rolling, seed and partial
states from this compact ZIP (all are available in the repository).
"""
from pathlib import Path
import hashlib,zipfile,json,io
import numpy as np
ROOT=Path(__file__).resolve().parents[2];files={}
def add(p):
    if p.is_file() and p.suffix not in ['.pyc','.tmp'] and '__pycache__' not in p.parts:
        files[str(p.relative_to(ROOT))]=p.read_bytes()
for folder in ['v33','v34']:
    for p in (ROOT/'papers'/folder).rglob('*'):add(p)
for p in (ROOT/'adjudications').glob('adj-01-*'):add(p)
for p in (ROOT/'v2.2/verify/replica').glob('*'):
    if p.suffix in ['.py','.json','.log']:add(p)
for p in (ROOT/'v2.2/verify/replica/checkpoints').glob('*.npz'):
    if p.name.startswith(('scan128_','branch128_')) or any(x in p.name for x in ['latest','partial','seed_']):continue
    with np.load(p,allow_pickle=False) as z:m=json.loads(str(z['metadata']))
    if p.name.startswith('control_') or m.get('eps',1)>0 and m.get('eps',1)<m.get('tol',1e-7):add(p)
for name in ['replica_checks.py','replica_checks.log','v33_checks.py','v33_checks.log','transfer_checks.py','transfer_checks.log','run_all_transition_2026-10-16-final.log','run_all_chi128_2026-10-16.log','run_all_scan128_2026-10-16.log','run_all_branch128_2026-10-16.log']:
    add(ROOT/'v2.2/verify'/name)
add(ROOT/'v2.2/md2docx.py')
for p in (ROOT/'research/transition-order').rglob('*'):add(p)
for name in ['requirements.txt','PUBLICATION-SCOPE.md']:add(ROOT/name)
files['README.md']=b'''# Physics-only author-review and transition-order package

Start with papers/v33/REVISION-REPORT.md (historical v33 delivery), then
research/transition-order/RESULTS.md or transition-order-report.docx (continuation).
The paper remains an author-review draft; original figure/SM and specialist review
are still required. No transition-order or submission certification is implied.

From this extracted v33-review/ root:
  python3 -m pip install -r papers/v33/requirements.txt
  bash papers/v33/run_review_checks.sh

The current paper runner has 17+35+49=101 counted implementation/regression checks.
The full framework driver, unrelated theological/time-framework content and its
inputs are not needed or bundled. Full integrated-run logs may be included solely
as provenance; that full driver is available in the GitHub repository.

The bundle retains supplied A-1 manuscript/reviewer/credential-free assessment
inputs for source/hash reproduction; these are not claimed as agent creations.
The original v33 TeX and its historical tables are distinguished from the later
half-row data. Different finite-chi functionals must not be mixed silently.

Real MPS NPZ states are included selectively: controls and accepted immutable
anchors from the earlier matched-point experiment. Bulk scan128/branch128 states and
rolling/partial/warm-seed states are omitted here to avoid duplication;
the full repository snapshot / owner-push Git bundle retains those records.
The publication-status receipt says whether the new continuation was actually
pushed; this archive by itself does not establish a new GitHub publication.
Inspect metadata and optimizer tolerances: a checkpoint is not a phase verdict.

Optional workspace/amendment/publication helpers under research/ require the full
repository when their documented framework/Git inputs are referenced. They are
not part of the minimal physics verification command above.

SHA256SUMS hashes the supplied files. Source attributions/rights are retained.
'''
manifest=''.join(f'{hashlib.sha256(data).hexdigest()}  {name}\n' for name,data in sorted(files.items()))
files['SHA256SUMS']=manifest.encode()
path=ROOT/'papers/v33-review-package.zip';tmp=path.with_suffix('.tmp')
with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,data in sorted(files.items()):z.writestr('v33-review/'+name,data)
with zipfile.ZipFile(tmp) as z:
    bad=z.testzip()
    if bad:raise RuntimeError('Archive CRC failed: '+bad)
    for line in manifest.splitlines():
        sha,name=line.split('  ',1)
        assert hashlib.sha256(z.read('v33-review/'+name)).hexdigest()==sha
    if any('/.git/' in x or '/.arena/' in x or 'credentials' in x.lower() for x in z.namelist()):raise RuntimeError('Forbidden archive member')
tmp.replace(path)
path.with_name(path.name+'.sha256').write_text(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n')
print(json.dumps(dict(path=str(path),files=len(files),bytes=path.stat().st_size,crc='passed',sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2))

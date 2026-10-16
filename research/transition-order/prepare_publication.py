#!/usr/bin/env python3
"""Prepare (not push) the allowlisted generated-work snapshot for GitHub.
The destination must be an existing Git clone. Credentials stay in its excluded
.git metadata. Scan actual secrets without ever printing them. ZIP/OOXML/NPZ
members are scanned too; a suspicious file aborts before staging.
"""
from pathlib import Path
import os,sys,shutil,json,hashlib,zipfile,io,re
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[2]
DEST=Path(os.environ.get('PUBLISH_CLONE',ROOT/'.arena/publish')).resolve()
if not (DEST/'.git').is_dir():raise SystemExit('Destination is not an existing Git clone')
if DEST==ROOT:raise SystemExit('Refusing workspace root as publication clone')
SKIP={'.git','.arena','.cache','.local','.npm','.pytest_cache','.venv','__pycache__','node_modules','build','dist','target','out','.next','.vite','Unselected files'}
ALLOW=['v2.1','v2.2','papers','clues','research']
# These supplied inputs are included solely for the reproducible A-1 record.
INPUTS=['adjudications/adj-01-a-manuscript_revised_v32.txt',
        'adjudications/adj-01-b-engine-contradicts-paper.txt',
        'adjudications/adj-01-c-v33-assessment.md',
        'adjudications/adj-01-d-method-assessment.md','quran/q.py','quran/download_corpus.py','quran/README.md']
TOP=['README.md','PUBLICATION-SCOPE.md','.gitignore','requirements.txt']
secrets=[];cred=DEST/'.git/credentials'
if cred.exists():
    for line in cred.read_text().splitlines():
        u=urlsplit(line)
        if u.password:
            raw=unquote(u.password).encode();secrets.extend([raw,u.password.encode()])
patterns=[re.compile(rb'github_pat_[A-Za-z0-9_]{20,}'),re.compile(rb'gh[pousr]_[A-Za-z0-9]{20,}'),re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
def scan(data,label,depth=0):
    if any(s and s in data for s in secrets) or any(p.search(data) for p in patterns):
        raise SystemExit('Credential scan blocked a file; no content was printed: '+label)
    if depth<3 and data.startswith(b'PK\x03\x04'):
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for n in z.namelist():
                    if not n.endswith('/'):scan(z.read(n),label+'!'+n,depth+1)
        except zipfile.BadZipFile:raise SystemExit('Invalid archive: '+label)
files=[]
for root in ALLOW:
    for p in sorted((ROOT/root).rglob('*')):
        if (p.is_file() and not p.is_symlink()
                and not any(x in SKIP for x in p.relative_to(ROOT).parts)
                and not (p.parent.name=='quran' and p.suffix=='.json')):files.append(p)
for rel in INPUTS+TOP:
    p=ROOT/rel
    if p.is_file():files.append(p)
# Prune only the four corpus copies previously introduced by this publication
# script; raw worktree inputs are not otherwise deleted or history-rewritten.
for rel in ['v2.2/verify/quran/'+x+'.json' for x in ['quran-simple','en.sahih','en.arberry','en.pickthall']]:
    old=DEST/rel
    if old.is_file():old.unlink()
records=[]
for src in sorted(set(files)):
    rel=src.relative_to(ROOT)
    if src.suffix in ['.pyc','.tmp'] or src.name.endswith('.tmp.npz'):continue
    # Atomic read: the optimizer writes checkpoints by rename, not in-place.
    data=src.read_bytes();scan(data,str(rel))
    dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
    if os.access(src,os.X_OK):dst.chmod(dst.stat().st_mode|0o111)
    records.append(dict(path=str(rel),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
# Scan the entire non-Git worktree too, not only newly copied files.
for p in DEST.rglob('*'):
    if p.is_file() and not any(x in SKIP for x in p.relative_to(DEST).parts):scan(p.read_bytes(),str(p.relative_to(DEST)))
manifest=dict(scope='generated work plus specifically identified A-1 reproduction inputs',
              credential_scan='passed (contents and nested archives; no secret values printed)',
              omitted=['raw uploads directory','bulk third-party search downloads','third-party Quran JSON corpora','dependency caches','all Git metadata/credentials'],
              files=records)
(DEST/'PUBLICATION-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(files=len(records),bytes=sum(x['bytes'] for x in records),credential_scan='passed',destination=str(DEST)),indent=2))

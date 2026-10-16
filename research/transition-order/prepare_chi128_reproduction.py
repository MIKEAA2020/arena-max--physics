#!/usr/bin/env python3
"""Prepare, but NEVER launch, an isolated reproduction of the chi128 stage.
An archived authorization deadline must not be silently extended in place.
Use a new, explicitly allocated directory and runtime; historical files survive.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse, hashlib, json, platform, shlex, shutil, time
import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('destination', type=Path, help='new directory; must not exist')
parser.add_argument('--seconds', type=int, default=5400, help='180..5400 seconds; preparation only')
args = parser.parse_args()
if not 180 <= args.seconds <= 5400:
    parser.error('Runtime must be 180..5400 seconds; no larger allocation is implicit')
dest = args.destination.expanduser().resolve()
if dest.exists():
    parser.error('Destination already exists; refusing overwrite')
original = ROOT / 'research/transition-order/chi128-90m-protocol.json'
protocol = json.loads(original.read_text())
paths = dict(protocol['source_sha256'])
paths.update({s['checkpoint']: s['sha256'] for s in protocol['preparations'].values()})
for name, digest in paths.items():
    if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
        raise SystemExit('Archived source/hash mismatch: ' + name)
for name in paths:
    target = dest / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / name, target)
protocol['reproduces_protocol_sha256'] = hashlib.sha256(original.read_bytes()).hexdigest()
protocol['campaign'] = 'isolated-chi128-reproduction-' + str(int(time.time()))
protocol['task_local_date'] = datetime.now(ZoneInfo('Asia/Tehran')).date().isoformat()
protocol['authorization'] = 'Operator allocation for an isolated reproduction; this helper does not launch workers.'
protocol['total_wall_seconds'] = args.seconds
protocol['optimizer_seconds'] = args.seconds - 120
protocol['global_deadline_unix'] = time.time() + args.seconds
protocol['software'] = dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)
p = dest / 'research/transition-order/chi128-90m-protocol.json'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(protocol, indent=2) + '\n')
print('Prepared only; NO production worker launched. Original archive untouched.')
print('The shared deadline starts now; launch in two terminals promptly, or prepare another new directory.')
print('cd ' + shlex.quote(str(dest / 'v2.2/verify/replica')))
for side in ['ordered', 'disordered']:
    print(f'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout --signal=TERM --kill-after=5s {args.seconds}s python3 -u bounded_chi128.py {side}')

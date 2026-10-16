#!/usr/bin/env python3
"""Record the completed authorized stage; refuse running or unverifiable rows.
No optimizer is launched, no tolerance is relaxed, no order verdict is inferred.
"""
from pathlib import Path
import hashlib, json, math
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
R = ROOT / 'v2.2/verify/replica'
protocol_path = HERE / 'chi128-90m-protocol.json'
protocol = json.loads(protocol_path.read_text())
protocol_digest = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
for name, digest in protocol['source_sha256'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
rows = {}
for side in ['ordered', 'disordered']:
    r = json.loads((R / f'n3_chi128_bounded_{side}.json').read_text())
    terminal = {'accepted-stationary-at-finite-chi', 'budget-stopped',
                'iteration-cap-or-stationarity-check-failed', 'period-contraction-check-failed',
                'optimizer-or-validation-failed', 'unexpected-error'}
    assert r['status'] in terminal, 'A preparation or its validation is still running'
    assert r['protocol_sha256'] == protocol_digest
    assert r['p'] == protocol['p'] and r['chi'] == 128 and r['tol'] == 1e-7
    source = ROOT / r['warm_source']['checkpoint']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == r['warm_source']['sha256']
    checkpoint = R / r['checkpoint']
    if checkpoint.exists():
        with np.load(checkpoint, allow_pickle=False) as z:
            metadata = json.loads(str(z['metadata']))
            assert metadata['p'] == r['p'] and metadata['chi'] == 128
    else:
        metadata = {}
    if r['converged']:
        assert r['status'] == 'accepted-stationary-at-finite-chi'
        assert r['eps'] < 1e-7
        assert max(r['gauge_left_residual'], r['gauge_right_residual']) < 1e-7
        assert max(r['left_canonical_residual'], r['right_canonical_residual']) < protocol['canonical_ceiling']
        assert r['period_contraction_relative_residual'] < protocol['period_contraction_ceiling']
        assert math.isfinite(r['f_full_rayleigh'])
        assert hashlib.sha256(checkpoint.read_bytes()).hexdigest() == r['checkpoint_sha256']
        assert metadata['eps'] == r['eps']
        with np.load(checkpoint, allow_pickle=False) as z:
            AL, AR, AC, C = [z[k] for k in ['AL','AR','AC','C']]
        assert metadata['n']==3 and metadata['d']==2 and metadata['operator']=='hermitian-halfrow'
        assert AL.shape==AR.shape==AC.shape==(128,6,128) and C.shape==(128,128)
        assert all(np.isfinite(x).all() for x in [AL,AR,AC,C])
        # Independent matrix-reshape expressions, not the driver's tensordot/einsum.
        direct_left=np.linalg.norm(AC.reshape(768,128)-AL.reshape(768,128)@C)
        direct_right=np.linalg.norm(AC.reshape(128,768)-C@AR.reshape(128,768))
        assert max(direct_left,direct_right)<1e-7
        assert np.linalg.norm(AL.reshape(768,128).T@AL.reshape(768,128)-np.eye(128))<1e-9
        assert np.linalg.norm(AR.reshape(128,768)@AR.reshape(128,768).T-np.eye(128))<1e-9
    assert r['total_stage_seconds'] < protocol['total_wall_seconds'] + 30
    rows[side] = (r, metadata)

segments_path = HERE / 'optimizer-segments.json'
segments = json.loads(segments_path.read_text())
for side, (r, metadata) in rows.items():
    output = R / f'order_{side}.json'
    db = json.loads(output.read_text())
    key = f"p{r['p']:.7f}:chi128"
    if key in db:
        assert db[key].get('campaign') == protocol['campaign'], 'A distinct earlier observation would be overwritten'
    db[key] = r
    temporary = output.with_suffix('.tmp')
    temporary.write_text(json.dumps(db, indent=2) + '\n')
    temporary.replace(output)
    if not any(s.get('campaign') == protocol['campaign'] and s.get('branch') == side for s in segments):
        segments.append(dict(campaign=protocol['campaign'], branch=side,
                             checkpoint_metadata=metadata, total_stage_seconds=r['total_stage_seconds'],
                             outcome=r['status'], source_checkpoint=r['warm_source']['checkpoint'],
                             note='One newly authorized stage; warm-source iterations/time are separate. No chi192 automatically scheduled.'))
segments_path.write_text(json.dumps(segments, indent=2) + '\n')

accepted = sum(r['converged'] for r, metadata in rows.values())
summary = dict(campaign=protocol['campaign'], p=protocol['p'], chi=128,
               completed_preparations=2, accepted_preparations=accepted,
               accepted_same_rate_comparisons=int(accepted == 2),
               maximum_preparation_wall_seconds=max(r['total_stage_seconds'] for r, m in rows.values()),
               chi192_launched=False, phase_order_verdict='unresolved',
               qualification='Numerical stationarity is for the half-row objective; period values are evaluations, not independent period-optimizer convergence.',
               outcomes={side: {k: r.get(k) for k in ['status','converged','eps','iters','total_stage_seconds','f_half','f_full_rayleigh','m_species','m_parity','xi_chi']} for side, (r, m) in rows.items()})
(HERE / 'chi128-stage-summary.json').write_text(json.dumps(summary, indent=2) + '\n')

p = HERE / 'deferred-computations.json'
deferred = json.loads(p.read_text())
deferred = [r for r in deferred if not (r.get('chi') == 128 and r.get('p') == protocol['p'])]
for r in deferred:
    if r.get('chi') == 192:
        r['status'] = 'not-authorized-for-automatic-launch; new-convergence-and-runtime-decision-required'
    if r.get('chi') == 96:
        r['status'] = 'unrun-archived-queue; superseded-by-authorized-higher-chi-stage'
p.write_text(json.dumps(deferred, indent=2) + '\n')

outcome = '; '.join(f"{side}: {r['status']}, eps={r.get('eps')}, iterations={r.get('iters')}, total stage {r['total_stage_seconds']:.1f}s" for side, (r, m) in rows.items())
for name in ['FEASIBILITY.md', 'NUMERICAL-NOTES.md']:
    p = HERE / name
    text = p.read_text()
    marker = '## Authorized chi128 stage — completed outcome'
    if marker not in text:
        text += '\n' + marker + '\n\n' + outcome + '.\n\n'
        text += f'{accepted}/2 preparations passed the prospective acceptance gates at p=.30486. This does not decide first order versus continuous. Chi192 was not launched; no campaign numerical production remains running. The earlier chi96 failures do not establish two stationary phases. See `CHI128-STAGE.md` for the interpretation contract and logical counterexamples.\n'
        p.write_text(text)
print(json.dumps(summary, indent=2))

#!/usr/bin/env python3
"""Independently recheck the saved scan tensors and declared numerical gates.
This is a release-data audit, not an extra part of the counted 246 suite and
not a phase-order, global-error, or local-minimum-stability certificate.
"""
from pathlib import Path
import hashlib,json,math,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(R))
import replica_halfrow as H
import scan128_worker as W

p=HERE/'chi128-scan-protocol.json';protocol=json.loads(p.read_text())
for name,digest in protocol['source_sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
for side,spec in protocol['preparations'].items():
    assert hashlib.sha256((ROOT/spec['checkpoint']).read_bytes()).hexdigest()==spec['sha256']
db=json.loads((R/'n3_chi128_scan.json').read_text())
assert len(db['cases'])==6,'The full requested grid has not been attempted'
checks=[];accepted=0
for rate in protocol['grid']:
    case=db['cases'][f'{rate:.7f}']
    for side in ['ordered','disordered']:
        r=case[side]
        assert r['p']==rate and r['chi']==128 and r['tol']==1e-7
        record=dict(p=rate,preparation=side,status=r['status'],accepted=r.get('converged') is True)
        path=R/r['checkpoint']
        assert path.exists(),'No real MPS checkpoint for recorded result'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==r['checkpoint_sha256']
        state,meta=H.load_state(path,operator='hermitian-halfrow')
        assert meta['n']==3 and meta['d']==2 and meta['chi']==128 and meta['p']==rate
        assert meta['operator']=='hermitian-halfrow'
        AL,AR,AC,C=[state[k] for k in ['AL','AR','AC','C']]
        assert AL.shape==AR.shape==AC.shape==(128,6,128) and C.shape==(128,128)
        assert all(np.isfinite(x).all() for x in [AL,AR,AC,C])
        if record['accepted']:
            accepted+=1
            left=float(np.linalg.norm(AC.reshape(768,128)-AL.reshape(768,128)@C))
            right=float(np.linalg.norm(AC.reshape(128,768)-C@AR.reshape(128,768)))
            lc=float(np.linalg.norm(AL.reshape(768,128).T@AL.reshape(768,128)-np.eye(128)))
            rc=float(np.linalg.norm(AR.reshape(128,768)@AR.reshape(128,768).T-np.eye(128)))
            assert max(left,right)<1e-7 and max(lc,rc)<1e-9
            assert r['eps']<1e-7 and meta['eps']==r['eps']
            assert r['period_contraction_relative_residual']<1e-8
            assert math.isfinite(r['f_full_rayleigh']) and math.isfinite(r['f_half'])
            assert abs(r['f_half']+2*math.log(meta['eta']))<1e-10
            colors=W.color_diagnostics(state,rate)
            assert abs(colors['color_sum']-1)<1e-9
            assert abs(colors['color_l2_order']-r['color_l2_order'])<1e-10
            record.update(left_compatibility=left,right_compatibility=right,left_canonical=lc,right_canonical=rc,
                          color_l2_order=colors['color_l2_order'],period_relative_residual=r['period_contraction_relative_residual'])
        checks.append(record)
    if case['ordered'].get('converged') and case['disordered'].get('converged'):
        comp=case['comparison']
        assert len(comp.get('orientations',[]))<=36
        assert comp.get('largest_evaluated_fidelity_per_site',0)<=1+1e-7
protected=json.loads((HERE/'governance-protection.json').read_text())
for name,digest in protected.items():
    assert hashlib.sha256((ROOT/'v2.2/parts'/name).read_bytes()).hexdigest()==digest
v34=json.loads((ROOT/'papers/v34/source-provenance.json').read_text())
assert v34['unchanged_statement_and_proof_blocks']==65 and v34['references_resolve'] and v34['citations_resolve']
result=dict(status='passed',recorded_preparations=len(checks),accepted_preparations=accepted,
            reused_preparations=2,new_targets=10,core_and_initializer_hashes_match=True,
            protected_framework_sources_unchanged=len(protected),v34_preserved_mathematical_blocks=65,
            counted_in_246=False,phase_order_verdict='unresolved',preparations=checks)
(HERE/'scan128-data-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='preparations'},indent=2))

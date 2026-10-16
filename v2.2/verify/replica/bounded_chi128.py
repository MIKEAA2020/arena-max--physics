#!/usr/bin/env python3
"""One explicitly authorized, wall-bounded chi=128 two-preparation stage.

No change to the validated optimizer, no chi=96 production and no automatic
chi=192. This wrapper preserves the earlier rolling states and observations.
The prospective protocol specifies immutable warm sources, tolerance and gates.
"""
from pathlib import Path
import hashlib, json, os, signal, sys, time, shutil
import numpy as np
import replica_halfrow as H
import replica_vumps as V

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
PROTOCOL = ROOT / 'research/transition-order/chi128-90m-protocol.json'


def atomic_json(path, value):
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, indent=2) + '\n')
    os.replace(temp, path)


def deadline(signum, frame):
    raise TimeoutError('authorized total wall-clock deadline reached')


def main():
    side = sys.argv[1]
    if side not in ('ordered', 'disordered'):
        raise SystemExit('ordered or disordered')
    protocol = json.loads(PROTOCOL.read_text())
    for name, digest in protocol['source_sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    spec = protocol['preparations'][side]
    source = ROOT / spec['checkpoint']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == spec['sha256']
    initial, metadata = H.load_state(source, operator='hermitian-halfrow')
    assert metadata['n'] == 3 and metadata['d'] == 2 and metadata['chi'] == 128
    p, chi, tol = protocol['p'], protocol['chi'], protocol['tol']
    assert chi == 128 and tol == 1e-7
    out = R / f'n3_chi128_bounded_{side}.json'
    checkpoint = R / 'checkpoints' / f'n3_{side}_chi128_bounded_latest.npz'
    if out.exists():
        raise SystemExit('Refusing accidental repeat/overwrite of the named authorized stage')
    started = time.monotonic()
    remaining = protocol['global_deadline_unix'] - time.time()
    if remaining < 180:
        raise SystemExit('Insufficient authorized time remains to launch')
    os.environ['STAGE_SECONDS'] = str(min(protocol['optimizer_seconds'], remaining - 120))
    os.environ['CORR_RMAX'] = str(protocol['correlation_rmax'])
    result = dict(campaign=protocol['campaign'], preparation=side, n=3, d=2,
                  p=p, chi=chi, tol=tol, status='running', converged=False,
                  protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                  warm_source=spec, warm_source_metadata=metadata,
                  warm_source_is_accepted_observation=False,
                  checkpoint=str(checkpoint.relative_to(R)),
                  qualification='preparation labels are histories, not proven phases; no binary order inference')
    atomic_json(out, result)
    signal.signal(signal.SIGALRM, deadline)
    signal.signal(signal.SIGTERM, deadline)
    signal.setitimer(signal.ITIMER_REAL, remaining)
    print('AUTHORIZED_STAGE', json.dumps(result), flush=True)
    try:
        state, obs = H.solve(3, 2, p, chi, init=initial, tol=tol,
                             maxiter=protocol['maxiter'], checkpoint_path=checkpoint,
                             tag=f'{side}-chi128-bounded', verbose=True)
        # These validate the same requested tolerance, rather than relaxing it.
        AL, AR, AC, C = (state[k] for k in ('AL', 'AR', 'AC', 'C'))
        left = float(np.linalg.norm(AC - np.tensordot(AL, C, axes=([2], [0]))))
        right = float(np.linalg.norm(AC - np.tensordot(C, AR, axes=([1], [0]))))
        lc = float(np.linalg.norm(np.einsum('asb,asc->bc', AL, AL) - np.eye(chi)))
        rc = float(np.linalg.norm(np.einsum('asb,csb->ac', AR, AR) - np.eye(chi)))
        result.update(obs)
        result.update(gauge_left_residual=left, gauge_right_residual=right,
                      left_canonical_residual=lc, right_canonical_residual=rc,
                      optimizer_tolerance_passed=bool(obs['eps'] < tol))
        numerical_stationarity = (obs['eps'] < tol and max(left, right) < tol
                                   and max(lc, rc) < protocol['canonical_ceiling'])
        if not numerical_stationarity:
            result.update(status='iteration-cap-or-stationarity-check-failed', converged=False)
        else:
            result.update(status='stationarity-passed-period-contraction-pending')
            atomic_json(out, result)
            print('PERIOD_RAYLEIGH_START', side, flush=True)
            W, _, _, _ = V.build_mpo(3, 2, p)
            lam, F = V.dominant(lambda x: V.apply_TL(x, AL, W),
                                (chi, W.shape[0], chi), tol=1e-10)
            relative = float(np.linalg.norm(V.apply_TL(F, AL, W) - lam * F) / abs(lam))
            if lam <= 0 or not np.isfinite(relative):
                raise RuntimeError('Non-positive or invalid period contraction')
            result.update(f_full_rayleigh=float(-np.log(lam)),
                          period_contraction_relative_residual=relative)
            accepted = relative < protocol['period_contraction_ceiling']
            result.update(converged=bool(accepted),
                          status='accepted-stationary-at-finite-chi' if accepted
                                 else 'period-contraction-check-failed')
            if accepted:
                saved = R / 'checkpoints' / f'n3_{side}_chi128_p{p:.7f}.npz'
                if saved.exists():
                    raise RuntimeError('Refusing overwrite of an existing immutable anchor')
                shutil.copyfile(checkpoint, saved)
                result['checkpoint'] = str(saved.relative_to(R))
                result['checkpoint_sha256'] = hashlib.sha256(saved.read_bytes()).hexdigest()
    except (RuntimeError, TimeoutError) as exc:
        result['status'] = ('budget-stopped' if isinstance(exc, TimeoutError)
                            or 'budget' in str(exc).lower() else 'optimizer-or-validation-failed')
        result['reason'] = str(exc)
        result['converged'] = False
        if checkpoint.exists():
            _, latest = H.load_state(checkpoint, operator='hermitian-halfrow')
            result['last_state_metadata'] = latest
            result['eps'] = latest.get('eps')
            result['iters'] = latest.get('iters')
    except Exception as exc:
        result.update(status='unexpected-error', converged=False,
                      reason=f'{type(exc).__name__}: {exc}')
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        result['total_stage_seconds'] = time.monotonic() - started
        if checkpoint.exists():
            result['latest_checkpoint_sha256'] = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
        atomic_json(out, result)
        print('BOUNDED_RESULT', json.dumps(result), flush=True)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Supplementary gauge/symmetry-aware comparison of ACCEPTED chi128 states.
Not an order classifier. Mixed-transfer eigenvalues may be complex: their
modulus is used deliberately for fidelity per site, with phase/residual retained.
Self/product/gauge/symmetry tests are separate smoke checks, not added to 246.
"""
from pathlib import Path
import json, sys, time, signal
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigs
import replica_halfrow as H
from replica_tm import make_group

R = Path(__file__).resolve().parent


def radius(A, B):
    ka, d, _ = A.shape
    kb = B.shape[0]
    dim = ka * kb
    def apply(X):
        temp = np.einsum('asg,gd->asd', A, X, optimize=True)
        return np.einsum('asd,bsd->ab', temp, B.conj(), optimize=True)
    def mv(x):
        return apply(x.reshape(ka, kb)).reshape(-1)
    if dim <= 36:
        matrix = np.column_stack([mv(np.eye(dim)[:, j]) for j in range(dim)])
        values, vectors = np.linalg.eig(matrix)
        i = np.argmax(abs(values))
        value, vector = values[i], vectors[:, i]
    else:
        dtype = np.result_type(A.dtype, B.dtype)
        operator = LinearOperator((dim, dim), matvec=mv, dtype=dtype)
        v0 = np.random.default_rng(911).standard_normal(dim)
        values, vectors = eigs(operator, k=1, which='LM', v0=v0, tol=1e-10,
                               maxiter=3000, ncv=32)
        value, vector = values[0], vectors[:, 0]
    residual = np.linalg.norm(mv(vector) - value * vector) / (abs(value) * np.linalg.norm(vector))
    return dict(radius=float(abs(value)), eigenvalue=[float(value.real), float(value.imag)],
                relative_residual=float(residual))


def transform(A, G, left, right):
    # tau -> left * tau * right^-1; the bond Gram commutes with this action,
    # so the action is also this orthogonal permutation in the symmetric basis.
    destinations = G['mul'][left, G['mul'][np.arange(G['N']), G['inv'][right]]]
    return A[:, np.argsort(destinations), :]


def smoke():
    A = np.array([1., 0., 0., 0., 0., 0.]).reshape(1, 6, 1)
    B = np.array([.6, .8, 0., 0., 0., 0.]).reshape(1, 6, 1)
    assert abs(radius(A, A)['radius'] - 1) < 1e-12
    assert abs(radius(A, B)['radius'] - .6) < 1e-12
    rng = np.random.default_rng(25)
    Q, _ = np.linalg.qr(rng.standard_normal((18, 3)))
    A = Q.reshape(3, 6, 3)
    U, _ = np.linalg.qr(rng.standard_normal((3, 3)))
    B = np.einsum('ai,isb,bj->asj', U.T, A, U, optimize=True)
    assert abs(radius(A, B)['radius'] - 1) < 1e-12
    G = make_group(3)
    B = transform(A, G, 1, 2)
    best = max(radius(A, transform(B, G, l, r))['radius'] for l in range(6) for r in range(6))
    assert abs(best - 1) < 1e-12
    print('4/4 supplementary product/self/gauge/symmetry smoke checks passed; not counted in 246')


def main():
    rows = {s: json.loads((R / f'n3_chi128_bounded_{s}.json').read_text())
            for s in ['ordered', 'disordered']}
    if not all(r.get('converged') is True for r in rows.values()):
        raise SystemExit('Not applicable: no two accepted stationary chi128 states')
    assert rows['ordered']['p'] == rows['disordered']['p']
    states = {s: H.load_state(R / r['checkpoint'], operator='hermitian-halfrow')[0]
              for s, r in rows.items()}
    A, B = states['ordered']['AL'], states['disordered']['AL']
    norm_a, norm_b = radius(A, A), radius(B, B)
    denominator = np.sqrt(norm_a['radius'] * norm_b['radius'])
    result = dict(kind='finite-chi stationary-state comparison, NOT phase-order classifier',
                  p=rows['ordered']['p'], chi=128, normalization_A=norm_a,
                  normalization_B=norm_b, orientations=[], status='partial')
    G = make_group(3)
    t0 = time.monotonic()
    def alarm(signum, frame):
        raise TimeoutError('Supplementary fidelity comparison budget reached')
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(90)
    try:
        for left in range(6):
            for right in range(6):
                record = radius(A, transform(B, G, left, right))
                record.update(left=left, right=right,
                              normalized_fidelity_per_site=record['radius'] / denominator)
                result['orientations'].append(record)
        result['status'] = 'all 36 symmetry orientations evaluated'
    except TimeoutError as exc:
        result['status'] = 'budget-stopped partial orientation search'
        result['reason'] = str(exc)
    finally:
        signal.alarm(0)
    if result['orientations']:
        result['largest_evaluated_fidelity_per_site'] = max(r['normalized_fidelity_per_site'] for r in result['orientations'])
    result['seconds'] = time.monotonic() - t0
    result['qualification'] = 'Similarity or difference at one p and chi does not decide transition order; no thermodynamic jump or crossing is inferred.'
    path = R / 'n3_chi128_stationary_comparison.json'
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(result, indent=2) + '\n')
    temp.replace(path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    smoke() if len(sys.argv) > 1 and sys.argv[1] == '--smoke' else main()

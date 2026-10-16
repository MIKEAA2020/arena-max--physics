#!/usr/bin/env python3
"""
replica_vumps.py — thermodynamic-limit fixed point of the n-replica transfer operator by VUMPS
(uniform matrix-product states; Zauner-Stauber et al. PRB 97, 045145 (2018), MPO-fixed-point variant;
Fishman et al. PRB 98, 235148 (2018) for 2D classical transfer matrices).

The one-period operator C = M1 T M1 of replica_tm.py is written as a uniform MPO of bond dimension N^2
(N = n! bond labels; N^2 = 36 for n = 3):
    W[(a2,a1),(b2,b1); sigma, tau] = delta(a1,tau) * Wb[sigma, a2, b2] * Wb[b2, tau, b1],
and conjugated site-wise by g^{1/2} (g[s,t] = (d^2)^{c(s^-1 t)}) into the symmetric form S = G^{1/2} C G^{-1/2},
whose dominant left and right eigenvectors coincide, so a single uniform MPS |psi(A)> serves as bra and ket.
Checked against the dense operator for m = 3 (python3 replica_vumps.py check).

Outputs per (p, chi): free energy per bond site f = -log eta, entanglement entropy, the stat-mech
order parameters <(-1)^a> (parity, sgn x sgn sector) and |<omega^k>| (Potts species, std x std sector),
correlation lengths in the parity and species channels (from connected correlators to r = 2000), and the
overall MPS correlation length xi_chi.  Scans use warm starts (previous p's MPS and environments).
"""
import json, os, sys, time
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigs
from replica_tm import make_group, weingarten, bond_weights

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------- MPO
def build_mpo(n, d, p, symmetric=True):
    G = make_group(n); N = G['N']
    Wb, T, Wg = bond_weights(G, d, p)                 # Wb[x, t, u] = W_p(x | t, u)
    _, gram = weingarten(G, d * d)
    w, V = np.linalg.eigh(gram)
    gh = (V * np.sqrt(w)) @ V.T; gmh = (V / np.sqrt(w)) @ V.T
    # W[a2,a1,b2,b1,sigma,tau] = delta(a1,tau) Wb[sigma,a2,b2] Wb[b2,tau,b1]
    W = np.einsum('xab,btc,ut->aubcxt', Wb, Wb, np.eye(N))   # (a2, a1, b2, b1, sigma, tau)
    W = W.reshape(N * N, N * N, N, N)
    if symmetric:
        W = np.einsum('xy,abyz,zt->abxt', gh, W, gmh)
    return W, G, gh, gmh

def mpo_dense_periodic(W, m):
    """tr prod_k W as a dense N^m x N^m operator (small m only)."""
    D, _, N, _ = W.shape
    # Close the virtual ring before building the two-site physical matrix.
    # The generic open-virtual intermediate would use D^2*N^4 doubles
    # (over 6 GB for the Hermitian n=4 half row). This is the identical sum.
    if m == 1:
        return np.trace(W, axis1=0, axis2=1)
    if m == 2:
        return np.einsum('abst,bauv->sutv', W, W, optimize=True).reshape(N*N, N*N)
    M = W.transpose(0, 2, 3, 1).reshape(D, N, N, D)        # (a, s, t, b)
    cur = M
    for k in range(1, m):
        cur = np.tensordot(cur, M, axes=([-1], [0]))       # (a, s1,t1,...,sk,tk, b)
    cur = np.trace(cur, axis1=0, axis2=-1)                 # (s1,t1,...,sm,tm)
    perm = list(range(0, 2 * m, 2)) + list(range(1, 2 * m, 2))
    return cur.transpose(perm).reshape(N ** m, N ** m)

# ----------------------------------------------------------------------------- contractions
def apply_TL(F, A, W):
    T1 = np.tensordot(F, A, axes=([0], [0]))               # (a, g, s, b)
    T2 = np.tensordot(T1, W, axes=([0, 2], [0, 2]))        # (g, b, b', t)
    return np.tensordot(T2, A, axes=([0, 3], [0, 1]))      # (b, b', d)

def apply_TR(F, A, W):
    T1 = np.tensordot(A, F, axes=([2], [0]))               # (al, s, b, dl)
    T2 = np.tensordot(W, T1, axes=([1, 2], [2, 1]))        # (a, t, al, dl)
    F2 = np.tensordot(T2, A, axes=([1, 3], [1, 2]))        # (a, al, g)
    return F2.transpose(1, 0, 2)

def apply_HAC(X, FL, FR, W):
    T1 = np.tensordot(FL, X, axes=([2], [0]))              # (al, a, t, dl)
    T2 = np.tensordot(T1, W, axes=([1, 2], [0, 3]))        # (al, dl, b, s)
    return np.tensordot(T2, FR, axes=([1, 2], [2, 1]))     # (al, s, be)

def apply_HC(Y, FL, FR):
    T1 = np.tensordot(FL, Y, axes=([2], [0]))              # (al, a, dl)
    return np.tensordot(T1, FR, axes=([1, 2], [1, 2]))     # (al, be)

def dominant(opfun, shape, v0=None, tol=1e-10, which='LM', ncv=None):
    """dominant eigenpair (real) of a real linear map given by opfun on arrays of `shape`."""
    dim = int(np.prod(shape))
    mv = lambda x: opfun(np.asarray(x, float).reshape(shape)).reshape(-1)
    A = LinearOperator((dim, dim), matvec=mv, dtype=float)
    v0v = None if v0 is None else np.asarray(v0, float).reshape(-1)
    if dim <= 300:
        M = np.column_stack([mv(np.eye(dim)[:, j]) for j in range(dim)])
        w, V = np.linalg.eig(M)
        i = np.argmax(w.real) if which == 'LR' else np.argmax(np.abs(w))
        lam, vec = w[i], V[:, i]
    else:
        w, V = eigs(A, k=1, which=which, v0=v0v, tol=tol, ncv=ncv or min(dim - 1, 24), maxiter=5000)
        lam, vec = w[0], V[:, 0]
    if abs(lam.imag) > 1e-8 * abs(lam):
        raise RuntimeError(f"complex dominant eigenvalue {lam}")
    vec = vec.real if np.linalg.norm(vec.real) > np.linalg.norm(vec.imag) else vec.imag
    vec = vec / np.linalg.norm(vec)
    if v0v is not None and np.dot(vec, v0v) < 0:
        vec = -vec
    return float(lam.real), vec.reshape(shape)

def polar(M):
    U, s, Vt = np.linalg.svd(M, full_matrices=False)
    return U @ Vt

# ----------------------------------------------------------------------------- canonical forms
def left_orth(A, tol=1e-12, maxit=2000):
    chi, d, _ = A.shape
    L = np.eye(chi)
    # start from the dominant left fixed point of the transfer matrix for speed
    for it in range(maxit):
        B = np.tensordot(L, A, axes=([1], [0])).reshape(chi * d, chi)
        Q, R = np.linalg.qr(B)
        sg = np.sign(np.diag(R)); sg[sg == 0] = 1
        Q = Q * sg; R = (R.T * sg).T
        R /= np.linalg.norm(R)
        if np.linalg.norm(R - L) < tol:
            L = R; break
        L = R
    return Q.reshape(chi, d, chi), L

def right_orth(A, tol=1e-12, maxit=2000):
    chi, d, _ = A.shape
    AR, Rt = left_orth(A.transpose(2, 1, 0), tol, maxit)
    return AR.transpose(2, 1, 0), Rt.T

def mixed_canonical(A):
    AL, L = left_orth(A); AR, R = right_orth(A)
    C = L @ R; C /= np.linalg.norm(C)
    AC = np.tensordot(AL, C, axes=([2], [0]))
    return AL, AR, AC, C

# ----------------------------------------------------------------------------- VUMPS
def vumps(W, chi, init=None, tol=1e-7, maxiter=400, verbose=False, seed=0, kick=0.0, callback=None, env_project=None):
    D, _, d, _ = W.shape
    if init is not None and kick > 0 and init['AL'].shape[0] == chi:
        rng = np.random.default_rng(seed + 1)
        A = init['AL'] + kick * rng.standard_normal(init['AL'].shape) * np.abs(init['AL']).max()
        AL, AR, AC, C = mixed_canonical(A)
        init = dict(AL=AL, AR=AR, AC=AC, C=C, FL=None, FR=None)
    if init is None:
        rng = np.random.default_rng(seed)
        A = rng.standard_normal((chi, d, chi))
        AL, AR, AC, C = mixed_canonical(A)
        FL = FR = None
    else:
        AL, AR, AC, C, FL, FR = (init[k] for k in ('AL', 'AR', 'AC', 'C', 'FL', 'FR'))
        if AL.shape[0] != chi:   # grow bond dimension by padding
            old = AL.shape[0]
            def pad3(X):
                Y = np.zeros((chi, d, chi)); Y[:old, :, :old] = X; return Y
            def pad2(X):
                Y = np.zeros((chi, chi)); Y[:old, :old] = X; return Y
            rng = np.random.default_rng(seed)
            A = pad3(AL) + 1e-3 * rng.standard_normal((chi, d, chi))
            AL, AR, AC, C = mixed_canonical(A); FL = FR = None
    eps = 1.0; eta = None
    t0 = time.time()
    for it in range(maxiter):
        etol = max(min(eps / 100, 1e-6), 1e-13)
        if env_project is not None:
            rng_env = np.random.default_rng(seed+1729)
            FL = env_project(FL if FL is not None else rng_env.standard_normal((chi,D,chi)))
            FR = env_project(FR if FR is not None else rng_env.standard_normal((chi,D,chi)))
        etaL, FL = dominant(lambda F: apply_TL(F, AL, W), (chi, D, chi), v0=FL, tol=etol)
        etaR, FR = dominant(lambda F: apply_TR(F, AR, W), (chi, D, chi), v0=FR, tol=etol)
        if env_project is not None:
            FL=env_project(FL);FR=env_project(FR)
        # normalise  <FL| C (x) C |FR> = 1
        nrm = np.einsum('aig,ab,gd,bid->', FL, C, C, FR)
        if nrm < 0:
            FR = -FR; nrm = -nrm
        FL = FL / np.sqrt(nrm); FR = FR / np.sqrt(nrm)
        lamAC, AC_new = dominant(lambda X: apply_HAC(X, FL, FR, W), (chi, d, chi), v0=AC, tol=etol, which='LR')
        lamC, C_new = dominant(lambda Y: apply_HC(Y, FL, FR), (chi, chi), v0=C, tol=etol, which='LR')
        AC, C = AC_new, C_new
        AL = (polar(AC.reshape(chi * d, chi)) @ polar(C).T).reshape(chi, d, chi)
        AR = (polar(C).T @ polar(AC.reshape(chi, d * chi))).reshape(chi, d, chi)
        HAC = apply_HAC(AC, FL, FR, W); HC = apply_HC(C, FL, FR)
        # fixed point: H_AC(A_C) = lamAC A_C, H_C(C) = lamC C with lamAC/lamC = eta (one more MPO site in H_AC)
        eps = np.linalg.norm(HAC / lamAC - np.tensordot(AL, HC, axes=([2], [0])) / lamC)
        eta = lamAC / lamC
        if verbose and (it % 10 == 0 or eps < tol):
            print(f"    it={it:3d} eta={eta:.10f} lamC={lamC:.10f} etaL={etaL:.10f} eps={eps:.2e} [{time.time()-t0:.0f}s]", flush=True)
        if callback is not None:
            callback(dict(AL=AL, AR=AR, AC=AC, C=C, FL=FL, FR=FR, eta=eta, eps=eps,
                          iters=it+1, chi=chi, seconds=time.time()-t0))
        if eps < tol:
            break
    return dict(AL=AL, AR=AR, AC=AC, C=C, FL=FL, FR=FR, eta=eta, eps=eps, iters=it + 1, chi=chi, seconds=time.time() - t0)

# ----------------------------------------------------------------------------- observables
def ka_labels(G):
    """(k, a) with sigma = c^k s^a, c = 3-cycle (0->1->2), s = transposition (01); S_3 only."""
    elems, idx, mul = G['elems'], G['idx'], G['mul']
    c = idx[(1, 2, 0)]; s = idx[(1, 0, 2)]; e = idx[(0, 1, 2)]
    lab = {}
    for k in range(3):
        for a in range(2):
            g = e
            for _ in range(k): g = mul[c, g]
            if a: g = mul[g, s]
            lab[g] = (k, a)
    return [lab[i] for i in range(G['N'])]

def local_expect(AC, O):
    return float(np.einsum('asb,st,atb->', AC, O, AC) / np.einsum('asb,asb->', AC, AC))

def correlators(st, ops, rmax, floor=1e-10):
    """connected <O_0 O_r>, r = 1..rmax, for several operators at once (same O at both ends); stops early
    once every correlator has fallen below `floor` x its r = 1 value."""
    AL, AR, C = st['AL'], st['AR'], st['C']
    AC = np.tensordot(AL, C, axes=([2], [0]))
    AC = AC / np.sqrt(np.einsum('asb,asb->', AC, AC))
    ms = [local_expect(AC, O) for O in ops]
    vs = [np.einsum('asg,st,atd->gd', AC, O, AC) for O in ops]
    ARO = [np.tensordot(AR, O, axes=([1], [1])).transpose(0, 2, 1) for O in ops]   # (g, t, b) = sum_s AR[g,s,b] O[s,t]... (bra index)
    out = [np.zeros(rmax) for _ in ops]
    ref = [None] * len(ops)
    for r in range(1, rmax + 1):
        done = True
        for i, O in enumerate(ops):
            # close: sum v[g,d] AR[g,s,b] O[s,t] AR[d,t,b]
            tmp = np.tensordot(vs[i], AR, axes=([0], [0]))            # (d, s, b)
            val = np.einsum('dsb,st,dtb->', tmp, O, AR)
            out[i][r - 1] = val - ms[i] ** 2
            if ref[i] is None:
                ref[i] = abs(out[i][0]) + 1e-300
            if abs(out[i][r - 1]) > floor * ref[i]:
                done = False
            # propagate one site
            tmp = np.tensordot(vs[i], AR, axes=([0], [0]))            # (d, s, b)
            vs[i] = np.tensordot(tmp, AR, axes=([0, 1], [0, 1]))      # (b, c)
        if done and r > 20:
            for i in range(len(ops)):
                out[i] = out[i][:r]
            break
    return out, ms

def xi_from_corr(c):
    """correlation length from the tail of |c(r)|: log-linear fit between the first r at which |c| has
    dropped below 1e-2 |c(1)| (or r = len/4 if it never does) and the last r at which |c| > 1e-7 |c(1)|."""
    a = np.abs(c); a0 = a[0]
    if not np.isfinite(a0) or a0 == 0:
        return float('nan')
    below = np.where(a < 1e-2 * a0)[0]
    r1 = int(below[0]) if len(below) else len(a) // 4
    above = np.where(a > 1e-7 * a0)[0]
    r2 = int(above[-1])
    if r2 - r1 < 10:
        r1 = max(0, r2 - 40)
    if r2 - r1 < 10:
        return float('nan')
    r = np.arange(r1, r2 + 1); y = np.log(a[r1:r2 + 1] + 1e-300)
    sl = np.polyfit(r, y, 1)[0]
    return float(-1 / sl) if sl < 0 else float('inf')

def transfer_second(st, k=6):
    """subleading eigenvalues of the MPS transfer matrix (overall xi_chi)."""
    AL = st['AL']; chi = AL.shape[0]
    def mv(x):
        v = x.reshape(chi, chi)
        tmp = np.einsum('asg,gd->asd', AL, v, optimize=True)
        return np.einsum('asd,bsd->ab', tmp, AL, optimize=True).reshape(-1)
    Aop = LinearOperator((chi * chi, chi * chi), matvec=mv, dtype=float)
    w = eigs(Aop, k=k, which='LM', return_eigenvectors=False, tol=1e-10, ncv=min(chi * chi - 1, 40))
    w = sorted(w, key=lambda z: -abs(z))
    return [complex(z) for z in w]

def observables(st, G, gh, gmh, rmax=2000):
    N = G['N']; AC = st['AC']
    lab = ka_labels(G) if G['n'] == 3 else None
    S_par = np.diag(G['sgn'].astype(float))
    res = dict(f=-np.log(st['eta']), eta=st['eta'], eps=st['eps'], iters=st['iters'], chi=st['chi'], seconds=st['seconds'])
    s = np.linalg.svd(st['C'], compute_uv=False); s2 = s ** 2 / np.sum(s ** 2)
    res['S_ent'] = float(-np.sum(s2 * np.log(s2 + 1e-300)))
    # stat-mech expectation values use g^{1/2} O g^{-1/2}
    Opar_sm = gh @ S_par @ gmh
    res['m_parity'] = local_expect(AC, Opar_sm); res['m_parity_sym'] = local_expect(AC, S_par)
    S_par_sm = gh @ S_par @ gmh
    if lab is not None:
        ck = np.diag([np.cos(2 * np.pi * k / 3) for k, a in lab]); sk = np.diag([np.sin(2 * np.pi * k / 3) for k, a in lab])
        mx = local_expect(AC, gh @ ck @ gmh); my = local_expect(AC, gh @ sk @ gmh)
        res['m_species'] = float(np.hypot(mx, my))
        res['m_species_sym'] = float(np.hypot(local_expect(AC, ck), local_expect(AC, sk)))
        Pe = np.diag([1.0 if a == 0 else 0.0 for k, a in lab])
        mxe = local_expect(AC, gh @ (Pe @ ck) @ gmh); mye = local_expect(AC, gh @ (Pe @ sk) @ gmh)
        res['m_species_even'] = float(np.hypot(mxe, mye))
        (c_sp, c_par), _ = correlators(st, [ck, S_par], rmax)
        res['xi_species'] = xi_from_corr(c_sp)
        res['corr_species_tail'] = [float(c_sp[i]) for i in (0, min(9, len(c_sp) - 1), min(49, len(c_sp) - 1), len(c_sp) - 1)]
    else:
        (c_par,), _ = correlators(st, [S_par], rmax)
    res['xi_parity'] = xi_from_corr(c_par)
    res['corr_parity_tail'] = [float(c_par[i]) for i in (0, min(9, len(c_par) - 1), min(49, len(c_par) - 1), len(c_par) - 1)]
    res['corr_len'] = int(len(c_par))
    w = transfer_second(st); res['xi_chi'] = float(-1 / np.log(abs(w[1]))) if len(w) > 1 else float('nan')
    res['transfer_eigs'] = [abs(z) for z in w[:6]]
    return res

# ----------------------------------------------------------------------------- drivers
def _store(out, key, ob):
    db = json.load(open(out)) if os.path.exists(out) else {}
    db[key] = ob
    tmp = out + '.tmp'
    json.dump(db, open(tmp, 'w'), indent=1, sort_keys=True)
    os.replace(tmp, out)
    return db

def run_scan(n, ps, chis, out, tol=1e-7, maxiter=300, verbose=True, sweep='up', kick=0.0):
    db = json.load(open(out)) if os.path.exists(out) else {}
    ps = list(ps) if sweep == 'up' else list(ps)[::-1]
    for chi in chis:
        init = None
        for p in ps:
            key = f"n{n}:chi{chi}:p{p:.5f}:{sweep}" + (f":kick{kick:g}" if kick else "")
            if key in db:
                if verbose: print("cached", key); continue
            W, G, gh, gmh = build_mpo(n, 2, p)
            st = vumps(W, chi, init=init, tol=tol, maxiter=maxiter, verbose=False, kick=kick)
            init = st
            ob = observables(st, G, gh, gmh)
            ob.update(p=p, n=n, sweep=sweep, kick=kick)
            db = _store(out, key, ob)
            if verbose:
                print(f"n={n} chi={chi} p={p:.5f} [{sweep}] f={ob['f']:.8f} S={ob['S_ent']:.4f} m_par={ob['m_parity']:+.5f} "
                      + (f"m_sp={ob['m_species']:.5f} m_sp_even={ob['m_species_even']:.5f} xi_sp={ob['xi_species']:.2f} " if n == 3 else "")
                      + f"xi_par={ob['xi_parity']:.2f} xi_chi={ob['xi_chi']:.2f} eps={ob['eps']:.1e} it={ob['iters']} [{ob['seconds']:.0f}s]", flush=True)
    return db

def run_chiscan(n, p, chis, out, tol=1e-7, maxiter=400, verbose=True, tag='chi', seed=0):
    """finite-entanglement scaling at fixed p: increasing chi with padded warm starts."""
    db = json.load(open(out)) if os.path.exists(out) else {}
    W, G, gh, gmh = build_mpo(n, 2, p)
    init = None
    for chi in chis:
        key = f"n{n}:chi{chi}:p{p:.5f}:{tag}"
        if key in db:
            if verbose: print("cached", key)
            continue
        st = vumps(W, chi, init=init, tol=tol, maxiter=maxiter, verbose=False, seed=seed)
        init = st
        ob = observables(st, G, gh, gmh)
        ob.update(p=p, n=n, sweep=tag, kick=0.0)
        db = _store(out, key, ob)
        if verbose:
            print(f"n={n} chi={chi} p={p:.5f} [{tag}] f={ob['f']:.8f} S={ob['S_ent']:.4f} m_par={ob['m_parity']:+.5f} "
                  + (f"m_sp={ob['m_species']:.5f} xi_sp={ob['xi_species']:.2f} " if n == 3 else "")
                  + f"xi_par={ob['xi_parity']:.2f} xi_chi={ob['xi_chi']:.2f} eps={ob['eps']:.1e} it={ob['iters']} [{ob['seconds']:.0f}s]", flush=True)
    return db

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'chiscan':
        n = int(sys.argv[2]); p = float(sys.argv[3]); chis = [int(x) for x in sys.argv[4].split(',')]
        tag = sys.argv[5] if len(sys.argv) > 5 else 'chi'
        maxiter = int(sys.argv[6]) if len(sys.argv) > 6 else 400
        run_chiscan(n, p, chis, os.environ.get('VUMPS_OUT', os.path.join(HERE, f'vumps_n{n}.json')), tag=tag, maxiter=maxiter)
        sys.exit(0)
    if cmd == 'check':
        from replica_tm import ReplicaTM
        for n, m, p in ((2, 4, 0.3), (3, 3, 0.305)):
            tm = ReplicaTM(n, 2, 2 * m, p)
            Cd = tm.dense_C()
            W, G, gh, gmh = build_mpo(n, 2, p, symmetric=False)
            Cm = mpo_dense_periodic(W, m)
            print(f"n={n} m={m}: |C_mpo - C_dense| = {np.abs(Cm - Cd).max():.2e}  (|C| max {np.abs(Cd).max():.3f})")
            Ws, _, _, _ = build_mpo(n, 2, p, symmetric=True)
            Sm = mpo_dense_periodic(Ws, m)
            Gh = tm.g_half
            for _ in range(m - 1): Gh = np.kron(Gh, tm.g_half)
            Sd = Gh @ Cd @ np.linalg.inv(Gh)
            print(f"        |S_mpo - S_dense| = {np.abs(Sm - Sd).max():.2e}; S symmetric to {np.abs(Sm - Sm.T).max():.1e}")
            ev = np.sort(np.linalg.eigvals(Sm).real)[::-1]
            print(f"        top eigenvalues: {ev[:4]}")
        # small VUMPS test: n=2 at p=0.20 (ordered) and p=0.27 (disordered), chi=16
        for p in (0.20, 0.233810, 0.27):
            W, G, gh, gmh = build_mpo(2, 2, p)
            st = vumps(W, 16, tol=1e-7, maxiter=200, verbose=False)
            ob = observables(st, G, gh, gmh, rmax=600)
            print(f"n=2 p={p}: f={ob['f']:.8f} m_par={ob['m_parity']:+.5f} (sym {ob['m_parity_sym']:+.5f}) xi_par={ob['xi_parity']:.2f} xi_chi={ob['xi_chi']:.2f} eps={ob['eps']:.1e} it={ob['iters']} [{ob['seconds']:.0f}s]")
    elif cmd == 'scan':
        n = int(sys.argv[2]); chis = [int(x) for x in sys.argv[3].split(',')]
        ps = [float(x) for x in sys.argv[4].split(',')]
        sweep = sys.argv[5] if len(sys.argv) > 5 else 'up'
        kick = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
        out = os.environ.get('VUMPS_OUT', os.path.join(HERE, f'vumps_n{n}.json'))
        run_scan(n, ps, chis, out, sweep=sweep, kick=kick)

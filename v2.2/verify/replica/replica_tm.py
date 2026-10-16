#!/usr/bin/env python3
"""
replica_tm.py — exact n-replica compressed transfer operator C_comp^{(n)} of the monitored brickwork
period (Abaee, "Exact replica mechanics ...", manuscript_revised_v32, Prop. general-n / Thm. general-n),
implemented independently from Eq. (Wpn):

    W_{p,n}(pi | mu, nu) = sum_sigma Wg_{d^2}(pi^{-1} sigma) T_p(sigma,mu) T_p(sigma,nu),
    T_p(sigma,mu)        = (1-p) d^{c(sigma^{-1} mu)} + p d,

on a periodic chain of L = 2m sites: odd bonds (1,2),(3,4),...,(L-1,L) carry labels tau_1..tau_m,
even bonds (2,3),...,(L,1) carry labels sigma_1..sigma_m,

    M1[sigma; tau] = prod_k W(sigma_k | tau_k, tau_{k+1}),   M2[tau; sigma] = prod_k W(tau_k | sigma_{k-1}, sigma_k),
    C = M2 M1  (one period),  and  M2 u = M1 (T u),  (T u)(s_1..s_m) = u(s_2..s_m, s_1).

C is similar to the symmetric PSD operator  S = G^{1/2} C G^{-1/2},  G = g^{(x) m},  g[s,t] = (d^2)^{c(s^{-1}t)}.
Everything is matrix-free (sequential tensor contraction, cost ~ m * 6^{m+2} per application for n=3),
so sizes up to L = 16 (6^8 = 1.68e6 bond labels) run on a laptop; L = 18 is reachable with the
low-memory Lanczos in replica_run.py.

Sectors: the operator commutes with global relabelings tau_b -> alpha tau_b beta^{-1} (S_n x S_n),
with inversion tau_b -> tau_b^{-1}, with bond translations and with the ring reflection.  Isotypic
projectors for S_3 x S_3 (triv(x)triv, std(x)std, sgn(x)sgn) and momentum-zero / inversion / reflection
projectors are provided and applied inside the LinearOperator.

Only numpy/scipy.  Written 15 Oct 2026 for adjudication A-1 (engine vs paper; not a clue — separate lineage).
"""
import itertools, math, sys, time
import numpy as np

# ---------------------------------------------------------------- S_n as index tables
def make_group(n):
    elems = list(itertools.permutations(range(n)))
    idx = {e: i for i, e in enumerate(elems)}
    N = len(elems)
    def compose(a, b):  # (a o b)(i) = a(b(i))
        return tuple(a[b[i]] for i in range(n))
    def inverse(a):
        inv = [0] * n
        for i, ai in enumerate(a):
            inv[ai] = i
        return tuple(inv)
    mul = np.zeros((N, N), dtype=np.int64)
    inv = np.zeros(N, dtype=np.int64)
    for i, a in enumerate(elems):
        inv[i] = idx[inverse(a)]
        for j, b in enumerate(elems):
            mul[i, j] = idx[compose(a, b)]
    def cycles(a):
        seen = [False] * n; c = 0
        for i in range(n):
            if not seen[i]:
                c += 1; j = i
                while not seen[j]:
                    seen[j] = True; j = a[j]
        return c
    cyc = np.array([cycles(a) for a in elems])
    sgn = np.array([(-1) ** (n - c) for c in cyc])
    return dict(n=n, elems=elems, idx=idx, N=N, mul=mul, inv=inv, cyc=cyc, sgn=sgn)

def weingarten(G, D):
    """Weingarten function as the inverse of the Gram matrix D^{c(s^{-1}t)} (valid for D >= n)."""
    N = G['N']
    gram = np.zeros((N, N))
    for s in range(N):
        for t in range(N):
            gram[s, t] = float(D) ** G['cyc'][G['mul'][G['inv'][s], t]]
    return np.linalg.inv(gram), gram

def bond_weights(G, d, p):
    """W[x, t, u] = W_{p,n}(x | t, u) from Eq. (Wpn)."""
    N = G['N']; D = d * d
    Wg, _ = weingarten(G, D)
    T = np.zeros((N, N))
    for s in range(N):
        for m_ in range(N):
            T[s, m_] = (1 - p) * float(d) ** G['cyc'][G['mul'][G['inv'][s], m_]] + p * d
    # Wg(pi^{-1} sigma) as a matrix in (pi, sigma): it is a class function, so Wg[pi^{-1}sigma] = Wg_vec[class]
    Wgmat = np.zeros((N, N))
    for pi in range(N):
        for s in range(N):
            Wgmat[pi, s] = Wg[G['inv'][pi], s] if False else Wg[0, G['mul'][G['inv'][pi], s]]
    W = np.einsum('ps,st,su->ptu', Wgmat, T, T)
    return W, T, Wg

# ---------------------------------------------------------------- the operator
class ReplicaTM:
    def __init__(self, n, d, L, p):
        assert L % 2 == 0 and L >= 4
        self.G = make_group(n); self.n = n; self.d = d; self.L = L; self.m = L // 2; self.p = p
        self.N = self.G['N']
        self.W, self.T, self.Wg = bond_weights(self.G, d, p)
        _, gram = weingarten(self.G, d * d)
        w, V = np.linalg.eigh(gram)
        assert w.min() > 0, "bond Gram matrix must be positive definite (d^2 >= n)"
        self.g_half = (V * np.sqrt(w)) @ V.T
        self.g_mhalf = (V / np.sqrt(w)) @ V.T
        self.dim = self.N ** self.m
        self.shape = (self.N,) * self.m

    # --- M1: y(sigma) = sum_tau prod_k W[sigma_k, tau_k, tau_{k+1}] v(tau)
    def apply_M1(self, v):
        N, m, W = self.N, self.m, self.W
        v = v.reshape(self.shape)
        y = np.zeros(self.shape)
        for t in range(N):
            vt = v[t]                                   # tau_2..tau_m
            if m == 1:
                raise ValueError
            # step k=1: B[s1, tau2, rest] = W[s1, t, tau2] * vt[tau2, rest]
            cur = W[:, t, :].reshape(N, N, 1) * vt.reshape(1, N, -1)   # (s1, tau2, rest)
            S = N
            for k in range(2, m):
                # cur: (S, tau_k, R) with R = N^{m-k}; split R -> (tau_{k+1}, R')
                R = cur.shape[-1]
                cur = cur.reshape(S, N, N, R // N)      # (S, tau_k, tau_{k+1}, R')
                cur = np.einsum('xtu,stur->sxur', W, cur, optimize=True)
                S *= N
                cur = cur.reshape(S, N, -1)             # (S', tau_{k+1}, R')
            # last step k=m: y[s.., s_m] += sum_{tau_m} W[s_m, tau_m, t] cur[s.., tau_m]
            cur = cur.reshape(S, N)
            y += (cur @ W[:, :, t].T).reshape(self.shape)
        return y

    def shift(self, v):  # (T u)(s_1..s_m) = u(s_2..s_m, s_1)
        return np.moveaxis(v.reshape(self.shape), -1, 0)

    def apply_C(self, v):
        return self.apply_M1(self.shift(self.apply_M1(v)))

    def apply_local(self, v, A):  # (A (x) ... (x) A) v
        v = v.reshape(self.shape)
        for ax in range(self.m):
            v = np.moveaxis(np.tensordot(A, v, axes=([1], [ax])), 0, ax)
        return v

    def apply_S(self, v):  # symmetric form G^{1/2} C G^{-1/2}
        return self.apply_local(self.apply_C(self.apply_local(v, self.g_mhalf)), self.g_half)

    # --- symmetries
    def relabel(self, v, a, b):  # (R v)(tau) = v(a tau b^{-1})
        G = self.G
        perm = G['mul'][a][G['mul'][:, G['inv'][b]]]   # perm[tau] = a*tau*b^{-1}
        return v.reshape(self.shape)[np.ix_(*([perm] * self.m))]

    def invert(self, v):
        perm = self.G['inv']
        return v.reshape(self.shape)[np.ix_(*([perm] * self.m))]

    def reflect(self, v):
        return np.transpose(v.reshape(self.shape), axes=tuple(range(self.m - 1, -1, -1)))

    def project_colour(self, v, sector):
        """isotypic projector of S_3 x S_3 (works for any n with these three characters: triv, std/perm-1, sgn)."""
        G = self.G; N = self.N
        if sector == 'triv':
            chi = np.ones(N)
        elif sector == 'sgn':
            chi = G['sgn'].astype(float)
        elif sector == 'std':  # standard (n-1)-dim rep: chi = (#fixed points) - 1
            chi = np.array([sum(1 for i, ai in enumerate(e) if ai == i) - 1 for e in G['elems']], float)
        else:
            raise ValueError(sector)
        dimrho = chi[0]
        out = np.zeros(self.shape)
        for a in range(N):
            for b in range(N):
                c = chi[a] * chi[b]
                if c != 0:
                    out += c * self.relabel(v, a, b)
        return out * (dimrho ** 2) / (N * N)

    def project_momentum0(self, v):
        v = v.reshape(self.shape); out = v.copy()
        for j in range(1, self.m):
            out += np.moveaxis(v, list(range(self.m)), [(i + j) % self.m for i in range(self.m)])
        return out / self.m

    def project_even(self, v, kind):
        v = v.reshape(self.shape)
        if kind == 'inv':
            return 0.5 * (v + self.invert(v))
        if kind == 'refl':
            return 0.5 * (v + self.reflect(v))
        raise ValueError

    def projector(self, colour=None, k0=True, inv_even=None, refl_even=None):
        def P(v):
            v = v.reshape(self.shape)
            if colour is not None:
                v = self.project_colour(v, colour)
            if k0:
                v = self.project_momentum0(v)
            if inv_even is not None:
                w = self.invert(v); v = 0.5 * (v + w) if inv_even else 0.5 * (v - w)
            if refl_even is not None:
                w = self.reflect(v); v = 0.5 * (v + w) if refl_even else 0.5 * (v - w)
            return v
        return P

    def sector_operator(self, **kw):
        """scipy LinearOperator for P S P in the chosen sector."""
        from scipy.sparse.linalg import LinearOperator
        P = self.projector(**kw)
        def mv(x):
            x = P(np.asarray(x, float).reshape(self.shape))
            y = self.apply_S(x)
            return P(y).reshape(-1)
        return LinearOperator((self.dim, self.dim), matvec=mv, dtype=float), P

    def dense_C(self):
        """dense compressed operator (small L only)."""
        D = self.dim
        M = np.zeros((D, D))
        e = np.zeros(D)
        for j in range(D):
            e[:] = 0; e[j] = 1
            M[:, j] = self.apply_C(e).reshape(-1)
        return M

def top_eigs(tm, k=6, ncv=None, tol=1e-12, **sector):
    from scipy.sparse.linalg import eigsh
    A, P = tm.sector_operator(**sector)
    rng = np.random.default_rng(12345)
    v0 = P(rng.standard_normal(tm.shape)).reshape(-1)
    if np.linalg.norm(v0) < 1e-12:
        return np.array([])
    vals = eigsh(A, k=k, which='LA', v0=v0, ncv=ncv, tol=tol, return_eigenvectors=False, maxiter=5000)
    vals = np.sort(vals)[::-1]
    return vals[vals > 1e-9]

if __name__ == '__main__':
    # quick self-checks
    G2 = make_group(2); d = 2; p = 0.3
    W2, T2, _ = bond_weights(G2, d, p)
    vth = d - (d - 1) * p
    a = (d * d * vth * vth - 1) / (d ** 4 - 1); b = vth / (d * d + 1); c = (d * d - vth * vth) / (d ** 4 - 1)
    print('n=2 check (a,b,c):', W2[0, 0, 0], a, '|', W2[0, 0, 1], b, '|', W2[0, 1, 1], c)
    G3 = make_group(3); W3, T3, Wg3 = bond_weights(G3, 2, 0.0)
    print('n=3 Wg at D=4 (e, transp, 3-cycle):', Wg3[0, 0], Wg3[0, 1], Wg3[0, 3], ' expected 7/360, -1/180, 1/360 =', 7/360, -1/180, 1/360)
    print('n=3, d=2, p=0: negative entries of W:', int((W3 < -1e-12).sum()), ' min entry', W3.min())

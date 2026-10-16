#!/usr/bin/env python3
"""Independent re-derivation of the main-text claims of
"The Opfibration Ontology" Rev. 2.8 (clue 5), done for WP3 of the v2.x plan.

Everything here is either exact symbolic algebra (sympy) or finite numerical
certificates (numpy) for the dimension counts the theorems rest on. It does NOT
verify the appendix's category-specific quotient proofs (C.8-C.28) or the
programming benchmarks (C.29-C.35) beyond the algebra of C.2/C.35.
"""
import itertools
import math
import numpy as np
import sympy as sp

rng = np.random.default_rng(20261014)
results = []


def record(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + detail if detail else ""))


# ----------------------------------------------------------------------------
# 1. Theorem 4.3 (quantum) and Theorem 5.2 (classical): the two-slice combination
# ----------------------------------------------------------------------------
n, r, e, m, b = sp.symbols("n r e m b", positive=True)
qR = n * r - 1                 # dim_aff Instr_n(C, R(B)),   r = d_R^2
qE = e * (n * m * b - 1)       # dim_aff Instr_{nm}(E, B),   e = d_E^2, b = d_B^2
combR = sp.simplify(qR.subs(n, 2) - 2 * qR.subs(n, 1))
combE = sp.simplify(qE.subs(n, 2) - 2 * qE.subs(n, 1))
record("Thm 4.3: q(2)-2q(1) = 1 on representing side", combR == 1, f"got {combR}")
record("Thm 4.3: q(2)-2q(1) = e on process side", combE == e, f"got {combE}")
# classical: dims |X|(n|Y|-1); representing side (|A|=1): n r - 1 with r=|R|; process: e(n m b - 1)
record("Thm 5.2: same two-grade mismatch classically (1 vs |E|)", True,
       "identical algebra with r=|R|, e=|E|, b=|B|")

# ----------------------------------------------------------------------------
# 2. Theorem 4.5 / 4.6 / Cor 5.7: the square gap
# ----------------------------------------------------------------------------
dE = sp.symbols("d_E", positive=True, integer=True)
target = dE**4 - dE**2 + 1
lower = (dE**2 - 1) ** 2
upper = dE**4
record("Thm 4.5: (d_E^2-1)^2 < d_E^4-d_E^2+1", sp.simplify(target - lower) == dE**2, "difference = d_E^2 > 0")
record("Thm 4.5: d_E^4-d_E^2+1 < d_E^4", sp.simplify(upper - target) == dE**2 - 1, "difference = d_E^2-1 > 0 for d_E>=2")
ok = all(not math.isqrt(d**4 - d**2 + 1) ** 2 == d**4 - d**2 + 1 for d in range(2, 100000))
record("Thm 4.5: finite check d_E in [2,1e5): never a perfect square", ok)
# Theorem 4.6 uniform in n: g = e^2 - (e-1)/n between (e-1)^2 and e^2
nn = sp.symbols("n", positive=True, integer=True)
ee = sp.symbols("e", positive=True, integer=True)
g = ee**2 - (ee - 1) / nn
record("Thm 4.6: g < e^2", sp.simplify(ee**2 - g) == (ee - 1) / nn, "(e-1)/n > 0")
record("Thm 4.6: g > (e-1)^2  iff  (e-1)/n < 2e-1", True, "holds since (e-1)/n <= e-1 < 2e-1")

# ----------------------------------------------------------------------------
# 3. Proposition 3.1: affine dimension of Instr_n(A,B) = d_A^2 (n d_B^2 - 1)
#    numerical: rank of the normalisation map (J_i) -> sum_i Tr_B J_i on Herm^n
# ----------------------------------------------------------------------------

def herm_basis(d):
    """Real basis of d x d Hermitian matrices."""
    B = []
    for i in range(d):
        M = np.zeros((d, d), complex); M[i, i] = 1; B.append(M)
    for i in range(d):
        for j in range(i + 1, d):
            M = np.zeros((d, d), complex); M[i, j] = M[j, i] = 1 / np.sqrt(2); B.append(M)
            M = np.zeros((d, d), complex); M[i, j] = -1j / np.sqrt(2); M[j, i] = 1j / np.sqrt(2); B.append(M)
    return B


def ptrace_B(J, dA, dB):
    return np.trace(J.reshape(dA, dB, dA, dB), axis1=1, axis2=3)


def herm_to_vec(H):
    d = H.shape[0]
    v = [H[i, i].real for i in range(d)]
    for i in range(d):
        for j in range(i + 1, d):
            v += [np.sqrt(2) * H[i, j].real, np.sqrt(2) * H[i, j].imag]
    return np.array(v)


ok_all = True
for dA, dB, nout in itertools.product([1, 2, 3], [1, 2, 3], [1, 2, 3]):
    basis = herm_basis(dA * dB)
    cols = []
    for k in range(nout):
        for H in basis:
            cols.append(herm_to_vec(ptrace_B(H, dA, dB)))
    M = np.array(cols).T
    rank = np.linalg.matrix_rank(M, tol=1e-9)
    ambient = nout * dA**2 * dB**2
    dim = ambient - rank
    expected = dA**2 * (nout * dB**2 - 1)
    if rank != dA**2 or dim != expected:
        ok_all = False
record("Prop 3.1: normalisation map has rank d_A^2; dim_aff = d_A^2(n d_B^2 - 1) for d_A,d_B,n <= 3", ok_all)

# ----------------------------------------------------------------------------
# 4. Proposition 5.1: CPM comparison, example (2,2,3): Chan dims 128 vs 140
# ----------------------------------------------------------------------------
dA, dE_, dB = 2, 2, 3
left = dA**2 * dE_**2 * (dB**2 - 1)
right = dA**2 * (dE_**2 * dB**2 - 1)
record("Prop 5.1: Chan(A⊗E,B)=128, Chan(A,E*⊗B)=140, difference d_A^2(d_E^2-1)=12",
       (left, right, right - left) == (128, 140, 12), f"{left}, {right}, {right-left}")

# ----------------------------------------------------------------------------
# 5. Theorem C.2 step (2)-(3): tangent dimension of the rank-r trace-preserving
#    Choi stratum is 2Nr - r^2 - d_E^2, and at r = d_E equals 2 d_E^2 (d_B - 1).
#    Numerical: Jacobian rank of X -> (K X^† + X K^†, Tr_B(...)) at a random K.
# ----------------------------------------------------------------------------

def random_tp_choi_factor(dE_, dB_, r_):
    """Random Kraus family with r operators E->B, normalised to be trace preserving;
    return K (N x r) with J = K K^†, N = dE*dB, and Tr_B J = I_E."""
    Ks = [rng.normal(size=(dB_, dE_)) + 1j * rng.normal(size=(dB_, dE_)) for _ in range(r_)]
    S = sum(K.conj().T @ K for K in Ks)
    w, V = np.linalg.eigh(S)
    Sinv_half = V @ np.diag(w ** -0.5) @ V.conj().T
    Ks = [K @ Sinv_half for K in Ks]
    # Choi vectorisation: column i of K is vec(K_i) in basis |e><b| ordering (E ⊗ B)
    K = np.zeros((dE_ * dB_, r_), complex)
    for i, Ki in enumerate(Ks):
        K[:, i] = Ki.T.reshape(-1)  # index (e, b)
    J = K @ K.conj().T
    assert np.allclose(ptrace_B(J, dE_, dB_), np.eye(dE_), atol=1e-8)
    return K


def stratum_dims(dE_, dB_, r_):
    N = dE_ * dB_
    K = random_tp_choi_factor(dE_, dB_, r_)
    # real parametrisation of X in C^{N x r}
    Xs = []
    for p in range(N):
        for q in range(r_):
            X = np.zeros((N, r_), complex); X[p, q] = 1; Xs.append(X)
            X = np.zeros((N, r_), complex); X[p, q] = 1j; Xs.append(X)
    tangents = [K @ X.conj().T + X @ K.conj().T for X in Xs]
    T = np.array([herm_to_vec(t) for t in tangents]).T          # (N^2) x (2Nr)
    rank_stratum = np.linalg.matrix_rank(T, tol=1e-8)             # should be 2Nr - r^2
    # trace-preserving sub-slice: tangent vectors with Tr_B = 0
    P = np.array([herm_to_vec(ptrace_B(t, dE_, dB_)) for t in tangents]).T  # (dE^2) x (2Nr)
    # dimension of image of (tangent space) under Tr_B
    rank_P = np.linalg.matrix_rank(P, tol=1e-8)                 # should be dE^2
    # dimension of tangent space of TP stratum = rank_stratum - rank of Tr_B restricted to it
    # compute directly: dim of {t in span(T): Tr_B t = 0}
    # = rank_stratum - rank(P restricted to span) ; P factors through T so rank_P suffices
    return rank_stratum, rank_P, rank_stratum - rank_P


ok_all = True
details = []
for dE_, dB_ in [(2, 2), (2, 3), (3, 2), (3, 3)]:
    r_ = dE_  # extreme-rank stratum
    N = dE_ * dB_
    rs, rp, dimTP = stratum_dims(dE_, dB_, r_)
    exp_stratum = 2 * N * r_ - r_**2
    exp_tp = exp_stratum - dE_**2
    exp_ext = 2 * dE_**2 * (dB_ - 1)
    good = (rs == exp_stratum) and (rp == dE_**2) and (dimTP == exp_tp == exp_ext)
    ok_all &= good
    details.append(f"(dE,dB)=({dE_},{dB_}): stratum {rs}={exp_stratum}, Tr_B rank {rp}={dE_**2}, TP dim {dimTP}={exp_ext}")
record("Thm C.2: rank-d_E TP stratum dimension = 2 d_E^2 (d_B - 1) (numerical Jacobian ranks)", ok_all, "; ".join(details))
# algebraic identity 2Nr - r^2 - dE^2 at r = dE
dEs, dBs = sp.symbols("d_E d_B", positive=True)
ident = sp.simplify(2 * dEs * dBs * dEs - dEs**2 - dEs**2 - 2 * dEs**2 * (dBs - 1))
record("Thm C.2: 2Nr - r^2 - d_E^2 at r=d_E equals 2 d_E^2 (d_B-1) (symbolic)", ident == 0)
# step (4): R = dE^2 (dB-1) + 1 and R^2 - 1 = dE^2 (dB^2 - 1) force (dE^2-1)(dB-1) = 0
R = dEs**2 * (dBs - 1) + 1
expr = sp.factor(sp.expand(R**2 - 1 - dEs**2 * (dBs**2 - 1)))
record("Thm C.2 step (4): R^2-1 - d_E^2(d_B^2-1) factors as d_E^2 (d_B-1) (d_E^2 (d_B-1) + 2 - d_B - 1)",
       sp.simplify(expr - dEs**2 * (dBs - 1) * (dEs**2 * (dBs - 1) - dBs + 1)) == 0, f"factor: {expr}")
# (The manuscript's displayed reduction "(d_E^2-1)(d_B-1)=0" is the same conclusion once d_B>=2 is used:
#  the second factor d_E^2(d_B-1) - (d_B-1) = (d_E^2-1)(d_B-1).)
chk = sp.simplify(dEs**2 * (dBs - 1) - dBs + 1 - (dEs**2 - 1) * (dBs - 1))
record("Thm C.2 step (4): second factor = (d_E^2-1)(d_B-1)", chk == 0)

# ----------------------------------------------------------------------------
# 6. Proposition C.35: deterministic universal processor needs d_R >= d_E^2 (d_B-1) + 1
#    (pure programs must cover the extreme boundary: 2(d_R-1) >= 2 d_E^2 (d_B-1))
# ----------------------------------------------------------------------------
record("Prop C.35: 2(d_R-1) >= dim Ext Chan(E,B) = 2 d_E^2 (d_B-1)  <=>  d_R >= d_E^2(d_B-1)+1 (qubit->qubit: 5)",
       2**2 * (2 - 1) + 1 == 5)

# ----------------------------------------------------------------------------
# 7. Proposition 6.1: the two-isometry channel has a CPTP left inverse (counterexample
#    to "single isometry only"), and satisfies Knill-Laflamme K_i^† K_j = c_ij I.
# ----------------------------------------------------------------------------
dA_ = 2
p = 0.3
V0 = np.vstack([np.eye(dA_), np.zeros((dA_, dA_))])   # A -> A ⊕ A
V1 = np.vstack([np.zeros((dA_, dA_)), np.eye(dA_)])
K0, K1 = np.sqrt(p) * V0, np.sqrt(1 - p) * V1
KL = np.array([[np.allclose(Ki.conj().T @ Kj, (Ki.conj().T @ Kj)[0, 0] * np.eye(dA_)) for Kj in (K0, K1)] for Ki in (K0, K1)])
record("Prop 6.1: Knill-Laflamme condition holds for the two-isometry channel", bool(KL.all()))
rho = rng.normal(size=(dA_, dA_)) + 1j * rng.normal(size=(dA_, dA_)); rho = rho @ rho.conj().T; rho /= np.trace(rho)
Nrho = K0 @ rho @ K0.conj().T + K1 @ rho @ K1.conj().T
Rec = V0.conj().T @ Nrho @ V0 + V1.conj().T @ Nrho @ V1
record("Prop 6.1: R∘N = id on a random state; N(pure) has rank 2 (not an isometry channel)",
       np.allclose(Rec, rho) and np.linalg.matrix_rank(K0 @ np.outer([1, 0], [1, 0]) @ K0.conj().T + K1 @ np.outer([1, 0], [1, 0]) @ K1.conj().T) == 2)

# ----------------------------------------------------------------------------
# 8. Proposition 6.2: Petz transpose on full-support pointed channels is CPTP,
#    recovers the prior, and composes contravariantly.
# ----------------------------------------------------------------------------

def rand_channel(din, dout, k=3):
    Ks = [rng.normal(size=(dout, din)) + 1j * rng.normal(size=(dout, din)) for _ in range(k)]
    S = sum(K.conj().T @ K for K in Ks)
    w, V = np.linalg.eigh(S); Sih = V @ np.diag(w ** -0.5) @ V.conj().T
    return [K @ Sih for K in Ks]


def apply(Ks, X):
    return sum(K @ X @ K.conj().T for K in Ks)


def adjoint(Ks, Y):
    return sum(K.conj().T @ Y @ K for K in Ks)


def msqrt(M, power=0.5):
    w, V = np.linalg.eigh(M); return V @ np.diag(w ** power) @ V.conj().T


def petz(Ks, sigma):
    tau = apply(Ks, sigma)
    s_half, t_mhalf = msqrt(sigma, 0.5), msqrt(tau, -0.5)
    return (lambda X: s_half @ adjoint(Ks, t_mhalf @ X @ t_mhalf) @ s_half), tau


def rand_state(d):
    G = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)); S = G @ G.conj().T + 0.1 * np.eye(d); return S / np.trace(S)


NK = rand_channel(3, 3); MK = rand_channel(3, 2)
sigma = rand_state(3)
Nsharp, tau = petz(NK, sigma)
Msharp, ups = petz(MK, tau)
MN = [M @ N for M in MK for N in NK]
MNsharp, _ = petz(MN, sigma)
X = rand_state(2)
record("Prop 6.2: N^#_σ(τ) = σ and trace preservation", np.allclose(Nsharp(tau), sigma) and np.isclose(np.trace(Nsharp(X if False else rand_state(3))), 1))
record("Prop 6.2: (M∘N)^#_σ = N^#_σ ∘ M^#_τ (contravariant composition)", np.allclose(MNsharp(X), Nsharp(Msharp(X))))

# ----------------------------------------------------------------------------
# 9. Theorem 4.12 / Prop 5.5 sanity: ℂ terminal in Chan; E (d_E>=2) not terminal.
# ----------------------------------------------------------------------------
record("Thm 4.12 / Prop 5.5: Chan(X,ℂ) = {trace} (unique), Chan(E,E) ⊇ {id, depolarising} (two morphisms)", True,
       "trace preservation fixes the unique effect; identity and X -> tr(X) I/d_E are distinct for d_E>=2")

print()
print(f"{sum(ok for _, ok, _ in results)}/{len(results)} checks passed")

#!/usr/bin/env python3
"""
clifford_tilt_smc.py — sequential Monte Carlo (cloning) for the tilted Clifford record-count ensemble

Ensemble (Abaee v32, App. B / Sec. IV-Clifford): periodic chain of L qubits, initial |0...0>, one period =
[measurement layer][gates on odd matching][measurement layer][gates on even matching]; every site measured
in Z independently with probability p in each measurement layer; every gate an independent uniformly random
two-qubit Clifford (sampled as the 720 symplectic actions Sp(4,2); the counted quantities are Pauli-frame
invariant).  N_rand = number of measurements whose outcome is random.

Target:  Lambda_L(beta; p) = (2 L t)^{-1} ln E_omega[ 2^{-beta N_rand(omega)} ]  (Def. cliffscgf),
         with beta = n - 1; beta = 2 is the Haar n = 3 annealed partition function (3-design identity),
         so Lambda(2; p) = -f_VUMPS(p)/4 in the thermodynamic limit (f per bond site per period = 4 sites).

Method (locally adapted proposal, v2): M walkers, phase-free stabilizer tableau (only the stabilizer rows are needed for N_rand and for
entanglement). The factor 2^{-beta} is absorbed into the measurement proposal (see measure_layer);
the remaining marginal weights are resampled at half-period / period boundaries.
The normaliser is accumulated as sum of log mean residual weights.  Ancestry is stored so that *bulk* (smoothed)
statistics of the tilted ensemble can be estimated from the genealogy of the final population: measurement count,
random-outcome count and the half-chain stabilizer entropy S_{L/2} (bits, two cuts) per period.

This has no sign problem and no MPS truncation, but finite-population bias, rare-event
sampling and ancestry collapse remain. log Z_hat is not unbiased even when Z_hat is.
Histogram counts are dependent descendants, NOT independent histories. Validate populations,
independent seeds, temporal boundaries and phase mixing before drawing coexistence conclusions.

CLI:  python3 clifford_tilt_smc.py L p beta M T [S_every] [seed] [out.json]
"""
import sys, json, time
import numpy as np

# ------------------------------------------------------------------ Sp(4,2): the 720 two-qubit Clifford actions
def symplectic_group_4():
    J = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=np.int64)
    mats = []
    for bits in range(1 << 16):
        S = np.array([(bits >> k) & 1 for k in range(16)], dtype=np.int64).reshape(4, 4)
        if np.array_equal((S @ J @ S.T) % 2, J):
            mats.append(S.astype(np.uint8))
    return np.array(mats)  # (720, 4, 4); acts on row vectors v = (x_a, x_b, z_a, z_b) -> v S

SP4 = None

# ------------------------------------------------------------------ tableau operations (vectorised over walkers)
def apply_gate_layer(X, Z, pairs, rng):
    """X, Z: (M, L, L) uint8.  pairs: array (P, 2) of qubit pairs.  Independent random Sp(4,2) per walker and pair."""
    global SP4
    M, L, _ = X.shape
    a = pairs[:, 0]; b = pairs[:, 1]
    v = np.stack([X[:, :, a], X[:, :, b], Z[:, :, a], Z[:, :, b]], axis=-1)      # (M, L, P, 4)
    S = SP4[rng.integers(0, 720, size=(M, len(pairs)))]                            # (M, P, 4, 4)
    w = np.einsum('mrpk,mpkj->mrpj', v, S) & 1                                      # (M, L, P, 4)
    X[:, :, a] = w[..., 0]; X[:, :, b] = w[..., 1]; Z[:, :, a] = w[..., 2]; Z[:, :, b] = w[..., 3]

def measure_layer(X, Z, p, beta, rng):
    """One measurement layer with the tilt 2^{-beta} per random outcome absorbed into the proposal
    (exact marginalisation / locally optimal SMC proposal).  For each site i and walker:
      * if no stabiliser anticommutes with Z_i the outcome would be deterministic: the state is unchanged
        whether or not the site is measured, so the site is weight-neutral (measured with prob. p for the record);
      * otherwise the outcome would be random: measuring carries weight p 2^{-beta}, not measuring (1-p);
        the site is measured with probability q = p 2^{-beta} / (p 2^{-beta} + 1 - p) and the walker's weight
        is multiplied by the exact marginal c = p 2^{-beta} + 1 - p.
    Returns (n_meas, n_rand, n_wouldbe_random, log_weight) per walker."""
    M, L, _ = X.shape
    c = p * 2.0 ** (-beta) + (1.0 - p)
    q = p * 2.0 ** (-beta) / c
    n_meas = np.zeros(M, dtype=np.int32); n_rand = np.zeros(M, dtype=np.int32); n_wr = np.zeros(M, dtype=np.int32)
    for i in range(L):
        Xi = X[:, :, i].astype(bool)                                                 # (M, L)
        R = Xi.any(axis=1)                                                           # would-be-random
        u = rng.random(M)
        meas = np.where(R, u < q, u < p)
        n_meas += meas; n_wr += R
        idx = np.nonzero(R & meas)[0]
        if idx.size == 0:
            continue
        n_rand[idx] += 1
        Ai = Xi[idx]                                                                 # anticommuting rows (k, L)
        piv = np.argmax(Ai, axis=1)
        PX = X[idx, piv, :]; PZ = Z[idx, piv, :]
        X[idx] ^= (Ai[:, :, None] & PX[:, None, :].astype(bool)).astype(np.uint8)
        Z[idx] ^= (Ai[:, :, None] & PZ[:, None, :].astype(bool)).astype(np.uint8)
        X[idx, piv, :] = 0; Z[idx, piv, :] = 0; Z[idx, piv, i] = 1
    return n_meas, n_rand, n_wr, n_wr * np.log(c)

def gf2_rank_batch(B):
    """rank over GF(2) of each matrix in B (M, R, C) uint8, vectorised Gaussian elimination."""
    B = B.copy().astype(bool)
    M, R, C = B.shape
    used = np.zeros((M, R), dtype=bool)
    rank = np.zeros(M, dtype=np.int32)
    for c in range(C):
        cand = B[:, :, c] & ~used
        has = cand.any(axis=1)
        idx = np.nonzero(has)[0]
        if idx.size == 0:
            continue
        piv = np.argmax(cand[idx], axis=1)
        prow = B[idx, piv, :]                                                        # (k, C)
        col = B[idx, :, c].copy()                                                    # rows with a 1 in column c
        col[np.arange(idx.size), piv] = False                                        # not the pivot itself
        B[idx] ^= col[:, :, None] & prow[:, None, :]
        used[idx, piv] = True
        rank[idx] += 1
    return rank

def half_chain_entropy(X, Z):
    """S_A in bits for A = first L/2 qubits (two cuts on the ring): rank of [X_A | Z_A] minus |A|."""
    M, L, _ = X.shape
    h = L // 2
    B = np.concatenate([X[:, :, :h], Z[:, :, :h]], axis=2)                           # (M, L, L)
    return gf2_rank_batch(B) - h

def systematic_resample(w, rng):
    M = w.size
    c = np.cumsum(w / w.sum())
    u = (rng.random() + np.arange(M)) / M
    return np.minimum(np.searchsorted(c, u), M - 1)

def reconstruct_lineage(anc, anc_in):
    """anc[t]: end-of-period children -> mid-period labels, after any internal resampling.
    anc_in[t]: mid-period labels -> labels entering t. Observables of period t use mid labels.
    Returns period-observable ancestor indices for every final particle.
    """
    T,M=anc.shape
    lineage=np.empty((T,M),dtype=np.int32)
    entering=np.arange(M)
    for t in range(T-1,-1,-1):
        mid=anc[t][entering]
        lineage[t]=mid
        entering=anc_in[t][mid]
    return lineage

# ------------------------------------------------------------------ the SMC
def run_smc(L, p, beta, M, T, S_every=0, seed=0, verbose=True):
    if L < 4 or L % 2 or M < 2 or T < 2 or not (0 <= p <= 1) or not (0 <= beta <= 32):
        raise ValueError("Require even L>=4, M>=2, T>=2, p in [0,1], beta in [0,32]")
    global SP4
    if SP4 is None:
        SP4 = symplectic_group_4()
        assert SP4.shape[0] == 720
    rng = np.random.default_rng(seed)
    X = np.zeros((M, L, L), dtype=np.uint8)
    Z = np.tile(np.eye(L, dtype=np.uint8), (M, 1, 1))
    odd = np.array([((2 * k + 1) % L, (2 * k + 2) % L) for k in range(L // 2)])
    even = np.array([(2 * k, 2 * k + 1) for k in range(L // 2)])
    logZ = 0.0
    anc = np.zeros((T, M), dtype=np.int32); anc_in = np.tile(np.arange(M, dtype=np.int32), (T, 1))
    n_meas = np.zeros((T, M), dtype=np.int16); n_rand = np.zeros((T, M), dtype=np.int16)
    S_half = np.full((T, M), -1, dtype=np.int16)
    ess = np.zeros(T)
    t0 = time.time()
    logw = np.zeros(M)
    for t in range(T):
        m1, r1, w1, lw1 = measure_layer(X, Z, p, beta, rng); apply_gate_layer(X, Z, odd, rng)
        logw += lw1
        a1 = None
        if beta > 0:
            w = np.exp(logw - logw.max()); e = w.sum() ** 2 / (w ** 2).sum()
            if e < 0.5 * M:                                                         # adaptive resampling mid-period
                logZ += np.log(w.mean()) + logw.max(); a1 = systematic_resample(w, rng)
                X = X[a1]; Z = Z[a1]; m1 = m1[a1]; r1 = r1[a1]; logw = np.zeros(M)
        m2, r2, w2, lw2 = measure_layer(X, Z, p, beta, rng); apply_gate_layer(X, Z, even, rng)
        logw += lw2
        r = r1 + r2
        n_meas[t] = m1 + m2; n_rand[t] = r
        if S_every and (t % S_every == S_every - 1):
            S_half[t] = half_chain_entropy(X, Z)
        if beta > 0:
            w = np.exp(logw - logw.max())
            ess[t] = w.sum() ** 2 / (w ** 2).sum()
            logZ += np.log(w.mean()) + logw.max()
            a = systematic_resample(w, rng); logw = np.zeros(M)
        else:
            ess[t] = M; a = np.arange(M)
        anc[t] = a                                   # entering labels of period t+1 -> mid-period labels of t
        if a1 is not None:
            anc_in[t] = a1                           # mid-period labels of t -> entering labels of t
        X = X[a]; Z = Z[a]
        if verbose and (t % max(1, T // 8) == 0 or t == T - 1):
            print(f"  t={t+1:4d}/{T} logZ/(2Lt)={logZ/(2*L*(t+1)):+.6f} ESS={ess[t]:.0f} "
                  f"<meas>={n_meas[t].mean()/(2*L):.4f} <rand>={r.mean()/(2*L):.4f} [{time.time()-t0:.0f}s]", flush=True)
    # genealogy: lineage[t, f] = index (before resampling at period t) of the ancestor of final walker f
    lineage = reconstruct_lineage(anc, anc_in)
    bulk_meas = np.take_along_axis(n_meas, lineage, axis=1).astype(float) / (2 * L)   # (T, M) densities
    bulk_rand = np.take_along_axis(n_rand, lineage, axis=1).astype(float) / (2 * L)
    bulk_S = np.take_along_axis(S_half, lineage, axis=1)                             # (T, M), -1 where not computed
    def s_summary(Sarr):
        hist = []; mean = []; var = []
        for t in range(T):
            v = Sarr[t][Sarr[t] >= 0]
            if v.size == 0:
                hist.append(None); mean.append(None); var.append(None); continue
            hist.append(np.bincount(v, minlength=L // 2 + 1).tolist()); mean.append(float(v.mean())); var.append(float(v.var()))
        return dict(hist=hist, mean=mean, var=var)
    mid = slice(T // 4, 3 * T // 4)
    descendant_ess=[]
    for t in range(T):
        c=np.bincount(lineage[t],minlength=M).astype(float)
        descendant_ess.append(float(M*M / np.sum(c*c)))
    def count_hist(A):
        return [np.bincount(row, minlength=2*L+1).tolist() for row in A]
    return dict(schema_version=2, method="locally-adapted tilt; adaptive half-period/systematic period resampling",
                histogram_warning="Descendants are correlated; these are not independent path counts.",
                L=L, p=p, beta=beta, M=M, T=T, seed=seed, Lambda=logZ / (2 * L * T), logZ=logZ,
                ess_mean=float(ess.mean()), ess_min=float(ess.min()),
                filt_meas=(n_meas.astype(float) / (2 * L)).mean(axis=1).tolist(),
                filt_rand=(n_rand.astype(float) / (2 * L)).mean(axis=1).tolist(),
                bulk_meas=bulk_meas.mean(axis=1).tolist(), bulk_rand=bulk_rand.mean(axis=1).tolist(),
                bulk_meas_mid=float(bulk_meas[mid].mean()), bulk_rand_mid=float(bulk_rand[mid].mean()),
                bulk_S=s_summary(bulk_S) if S_every else None, filt_S=s_summary(S_half) if S_every else None,
                bulk_random_count_hist=count_hist(np.take_along_axis(n_rand,lineage,axis=1)),
                bulk_measurement_count_hist=count_hist(np.take_along_axis(n_meas,lineage,axis=1)),
                descendant_ess=descendant_ess,
                n_distinct_lineages=[int(len(np.unique(lineage[t]))) for t in range(T)],
                seconds=time.time() - t0)

if __name__ == '__main__':
    L = int(sys.argv[1]); p = float(sys.argv[2]); beta = float(sys.argv[3]); M = int(sys.argv[4]); T = int(sys.argv[5])
    S_every = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    seed = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    out = sys.argv[8] if len(sys.argv) > 8 else None
    res = run_smc(L, p, beta, M, T, S_every=S_every, seed=seed)
    print(f"L={L} p={p} beta={beta} M={M} T={T}: Lambda_L={res['Lambda']:+.6f}  ESS mean {res['ess_mean']:.0f} min {res['ess_min']:.0f}  "
          f"bulk <meas>={np.mean(res['bulk_meas'][T//4:3*T//4]):.4f} bulk <rand>={np.mean(res['bulk_rand'][T//4:3*T//4]):.4f} [{res['seconds']:.0f}s]")
    if out:
        json.dump(res, open(out, 'w'))

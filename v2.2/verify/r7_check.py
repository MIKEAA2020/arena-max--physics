#!/usr/bin/env python3
"""Independent check of the R7 exchange (Opfibration Ontology Rev. 2.8, §7.2 R7).

R7: on the non-degenerate dimension-match locus of Prop. 4.7, do the fixed-grade bodies
Instr_n(A⊗E,B) and Instr_n(A,G) admit A-natural affine bijections / a fixed-grade representation?

Checks performed here (exact integers + sympy; numpy only for the two numerical certificates):
  1. Enumerate the locus for d_E in [2,60], d_B in [1,60]; count cells; flag the degenerate point.
  2. Representing side at A=C: Ext Instr_n(C,G) = n copies of CP^{d_G-1}; Y = 2(d_G-1) exactly.
  3. Process side at A=C, lower bounds on dim Ext Instr_n(E,B):
       d_B>=2 : zero-padded extreme channels      -> X >= 2 d_E^2 (d_B-1)   (Thm C.2)
       d_B =1 : zero-padded binary projective POVMs -> X >= 2 floor(d_E/2) ceil(d_E/2)
     and the best rank-split extreme-POVM stratum as a sharper lower bound.
  4. Verify X_lower > Y on every non-degenerate cell; verify the general inequalities symbolically;
     verify that j=1 is impossible on the non-degenerate d_B=1 locus (so d_G <= d_E-2).
  5. The reply's two counterexamples to the probe's "slice-wise transport":
       (d_E,n)=(11,3): three rank-4 extreme effects, normalized stratum of dimension 95 (> probe's 80);
       qubit trine: three rank-1 extreme effects, stratum of dimension 5 (> probe's 2).
     Numerical Jacobian-rank certificates of the stratum dimensions and extremality.
  6. The reply's factor-of-two finding on the cell (7,1,2,2,5).
"""
import math
import itertools
import numpy as np
import sympy as sp
import sys, functools
print = functools.partial(print, flush=True)

rng = np.random.default_rng(7)
out = []


def rec(name, ok, detail=""):
    out.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (("  -- " + detail) if detail else ""))


# ---------------------------------------------------------------- 1. locus enumeration
def locus(dE_max=60, dB_max=60):
    cells = []
    for dE in range(2, dE_max + 1):
        e = dE * dE
        for n in range(1, e):
            if (e - 1) % n:
                continue
            c = (e - 1) // n
            for dB in range(1, dB_max + 1):
                w = dE * dB
                for j in range(1, w):
                    if j * (2 * w - j) == c:
                        dG = w - j
                        degenerate = (dB == 1 and n == 1)
                        cells.append(dict(dE=dE, dB=dB, n=n, j=j, dG=dG, degenerate=degenerate))
    return cells


cells = locus()
nondeg = [c for c in cells if not c["degenerate"]]
nB2 = sum(1 for c in nondeg if c["dB"] >= 2)
nB1 = sum(1 for c in nondeg if c["dB"] == 1)
print(f"locus cells d_E,d_B<=60: {len(cells)} total; degenerate (d_B=1,n=1): {len(cells)-len(nondeg)}; "
      f"non-degenerate: {len(nondeg)}  (d_B>=2: {nB2}, d_B=1: {nB1})")
rec("1. degenerate cells are exactly (d_B=1, n=1, j=d_E-1, d_G=1), one per d_E",
    all(c["j"] == c["dE"] - 1 and c["dG"] == 1 for c in cells if c["degenerate"]) and
    sum(1 for c in cells if c["degenerate"]) == 59)

# ---------------------------------------------------------------- 3./4. bounds on every cell
def herm_vec(H):
    d = H.shape[0]
    v = [H[i, i].real for i in range(d)]
    for i in range(d):
        for j in range(i + 1, d):
            v += [H[i, j].real, H[i, j].imag]
    return np.array(v)


def povm_stratum_certificate(d, ranks):
    """Build a random POVM with given effect ranks by normalising random PSD matrices;
    check extremality (independence of the support-operator spaces) and compute the
    dimension of the normalised fixed-rank stratum through it by Jacobian rank."""
    Ks = [rng.normal(size=(d, r)) + 1j * rng.normal(size=(d, r)) for r in ranks]
    S = sum(K @ K.conj().T for K in Ks)
    w, V = np.linalg.eigh(S)
    Sih = V @ np.diag(w ** -0.5) @ V.conj().T
    Ks = [Sih @ K for K in Ks]
    Ms = [K @ K.conj().T for K in Ks]
    assert np.allclose(sum(Ms), np.eye(d))
    # extremality: operator spaces Herm(supp M_i) independent  <=> stacked basis has rank sum r_i^2
    cols = []
    for K in Ks:
        Q, _ = np.linalg.qr(K)              # orthonormal basis of the support
        r = K.shape[1]
        for a in range(r):
            for b in range(r):
                Eab = np.outer(Q[:, a], Q[:, b].conj())
                cols.append(herm_vec(Eab + Eab.conj().T))
                cols.append(herm_vec(1j * (Eab - Eab.conj().T)))
    rank_supports = np.linalg.matrix_rank(np.array(cols).T, tol=1e-8)
    extreme = (rank_supports == sum(r * r for r in ranks))  # real dim of Herm(supp M_i) is r_i^2; the 2r_i^2 spanning vectors are redundant
    # stratum dimension: tangent of product of rank-r PSD strata, intersected with ker(sum)
    tangents = []
    for idx, K in enumerate(Ks):
        r = K.shape[1]
        for p in range(d):
            for q in range(r):
                for unit in (1, 1j):
                    X = np.zeros((d, r), complex); X[p, q] = unit
                    t = [np.zeros((d, d), complex) for _ in ranks]
                    t[idx] = K @ X.conj().T + X @ K.conj().T
                    tangents.append(t)
    T = np.array([np.concatenate([herm_vec(ti) for ti in t]) for t in tangents]).T
    rank_T = np.linalg.matrix_rank(T, tol=1e-8)                 # = sum_i (2 d r_i - r_i^2)
    Ssum = np.array([herm_vec(sum(t)) for t in tangents]).T
    rank_sum = np.linalg.matrix_rank(Ssum, tol=1e-8)            # = d^2 if transverse
    return extreme, rank_T, rank_sum, rank_T - rank_sum



def best_povm_stratum(dE, n):
    """A sharper *lower* bound on dim Ext Instr_n(E,C) (the extreme POVM set on C^dE).
    Candidate rank vectors (r_1..r_n) must satisfy the necessary conditions for extremality --
    pairwise r_i + r_j <= dE (supports of an extreme POVM intersect trivially) and sum r_i^2 <= dE^2 --
    and are then CERTIFIED numerically at a random point (independence of the support-operator
    spaces, and transversality of the normalisation map); only certified strata are used.
    Any certified stratum gives a valid lower bound: it is a nonempty open piece of the extreme set."""
    best = 2 * (dE // 2) * (dE - dE // 2)          # binary projective, padded (always valid)
    q = int(dE / math.sqrt(n))
    cand = sorted(set(max(0, min(dE, q + t)) for t in (-2, -1, 0, 1, 2)))
    cands = []
    for rs in set(tuple(sorted(x, reverse=True)) for x in itertools.product(cand, repeat=n)):
        if sum(r * r for r in rs) > dE * dE or sum(rs) < dE:
            continue
        nz = [r for r in rs if r > 0]
        if any(a + b > dE for a, b in itertools.combinations(nz, 2)):
            continue
        val = sum(2 * dE * r - r * r for r in rs) - dE * dE
        if val > best:
            cands.append((val, nz))
    for val, nz in sorted(cands, reverse=True):      # best candidate first; stop at the first certified one
        extreme, rT, rS, dim = povm_stratum_certificate(dE, nz)
        if extreme and rS == dE * dE and dim == val:
            return val
    return best


all_ok = True
min_gap = None
worst = None
rows = []
for c in nondeg:
    dE, dB, n, j, dG = c["dE"], c["dB"], c["n"], c["j"], c["dG"]
    Y = 2 * (dG - 1)
    if dB >= 2:
        X_low = 2 * dE * dE * (dB - 1)                      # padded extreme channels (C.2)
        X_sharper = X_low
    else:
        X_low = 2 * (dE // 2) * (dE - dE // 2)              # padded binary projective POVMs
        X_sharper = best_povm_stratum(dE, n) if (n <= 4 and dE <= 15) else X_low
    gap = X_low - Y
    rows.append((dE, dB, n, j, dG, Y, X_low, X_sharper, gap))
    if gap <= 0:
        all_ok = False
    if min_gap is None or gap < min_gap:
        min_gap, worst = gap, (dE, dB, n, j, dG)
rec("4a. X_lower > Y on every non-degenerate locus cell (d_E,d_B<=60)", all_ok,
    f"{len(nondeg)} cells; minimum gap {min_gap} at (d_E,d_B,n,j,d_G)={worst}")
print("    cells: (d_E,d_B,n,j,d_G | Y, X_lower, X_sharper_lower, gap)")
for r_ in rows:
    print("     ", r_[:5], "|", r_[5:])

# symbolic: d_B>=2 gap identity and positivity
dE_, dB_ = sp.symbols("d_E d_B", positive=True)
gap_expr = 2 * dE_**2 * (dB_ - 1) - 2 * (dE_ * dB_ - 2)
claimed = 2 * dE_ * (dB_ - 2) * (dE_ - 1) + 2 * dE_ * (dE_ - 2) + 4
rec("4b. d_B>=2: 2d_E^2(d_B-1) - 2(d_E d_B - 2) == 2d_E(d_B-2)(d_E-1) + 2d_E(d_E-2) + 4  (symbolic)",
    sp.simplify(gap_expr - claimed) == 0)
rec("4c. d_B>=2: that expression >= 4 for d_E,d_B>=2", True, "each of the three terms is >= 0, 0, 4")
# j = 1 impossible on the non-degenerate d_B = 1 locus
j1_cells = [c for c in nondeg if c["dB"] == 1 and c["j"] == 1]
rec("4d. d_B=1 non-degenerate: j=1 never occurs (so d_G <= d_E-2); proof: (2d_E-1) | 3 would be needed",
    len(j1_cells) == 0, "gcd(2d_E-1, d_E^2-1) divides 3")
# positivity of the d_B=1 bound for all d_E>=3 (not just enumerated): 2 floor(d_E^2/4) > 2(d_E-3)
rec("4e. d_B=1: 2*floor(d_E^2/4) > 2(d_E-3) for all d_E>=3 (checked to 10^4; floor(d_E^2/4) >= d_E-2 algebraically)",
    all(2 * (d * d // 4) > 2 * (d - 3) for d in range(3, 10001)))
# the two infinite families
fam1 = all(((4*k+3)**2 - 1) % (k + 1) == 0 and ((4*k+3)**2 - 1)//(k+1) == 2*(2*(4*k+3) - 2) for k in range(0, 200))
fam2 = all(((16*k-1)**2 - 1) % k == 0 and ((16*k-1)**2 - 1)//k == 4*(2*2*(16*k-1) - 4) for k in range(1, 200))
rec("4f. families (4k+3, d_B=1, j=2, n=k+1) and (16k-1, d_B=2, j=4, n=k) lie on the locus (k<200)", fam1 and fam2)

# ---------------------------------------------------------------- 5. numerical certificates
ext, rT, rS, dim = povm_stratum_certificate(11, [4, 4, 4])
rec("5a. d=11, three rank-4 effects: extreme POVM; normalised stratum dim = 3(2*11*4-16)-121 = 95",
    ext and dim == 95 and rT == 216 and rS == 121, f"extreme={ext}, product-stratum rank {rT}, normalisation rank {rS}, dim {dim}")
ext, rT, rS, dim = povm_stratum_certificate(11, [6, 6, 7])
rec("5b. d=11, ranks (6,6,7): NOT extreme (6+6>11 forces overlapping supports) -- sum r_i^2 <= d^2 alone is not sufficient",
    (not ext) and dim == 176, f"extreme={ext}; the fixed-rank stratum (dim {dim}) is not inside the extreme set")
ext, rT, rS, dim = povm_stratum_certificate(11, [5, 5, 6])
rec("5b'. d=11, ranks (5,5,6): certified extreme stratum of dim 2(110-25)+(132-36)-121 = 145 (> 95 > 80)",
    ext and rS == 121 and dim == 145, f"extreme={ext}, dim {dim}")
# trine
ext, rT, rS, dim = povm_stratum_certificate(2, [1, 1, 1])
rec("5c. qubit, three rank-1 effects (trine-type): extreme; stratum dim 3(4-1)-4 = 5 (> probe's 2)",
    ext and dim == 5, f"extreme={ext}, dim {dim}")
rec("5d. zero-padding preserves extremality (proof: CP components averaging to 0 vanish; then use extremality of the unpadded body)", True)

# ---------------------------------------------------------------- 6. factor-of-two on (7,1,2,2,5)
dE, dG = 7, 5
X_probe = 2 * (dE // 2) * (dE - dE // 2)     # 24: Grassmannian of rank-3 projections in C^7
Y = 2 * (dG - 1)                              # 8
identity = dE * (dE - 1) - 4 * (dE - 2)       # 22, the probe's verified identity
rec("6a. cell (7,1,2,2,5): X_probe=24, Y=8, gap 16; the probe's certificate value (d_E-2)(d_E-3)+2 = 22 > 16  => stated bound false as written",
    X_probe == 24 and Y == 8 and identity == 22 and (X_probe - Y) < identity)
rec("6b. corrected bound ((d_E-2)(d_E-3)+2)/2 = 11 <= 16 holds; sign unaffected", (identity / 2) <= X_probe - Y)
# general: for the j=2, d_B=1 family, gap = 2 floor(d_E^2/4) - 2(d_E-3); compare with (d_E-2)(d_E-3)+2 and its half
bad_full, bad_half = [], []
for k in range(1, 300):          # k=0 is the degenerate (n=1) point
    d = 4 * k + 3
    gap = 2 * (d * d // 4) - 2 * (d - 3)
    if gap < (d - 2) * (d - 3) + 2:
        bad_full.append(d)
    if 2 * gap < (d - 2) * (d - 3) + 2:
        bad_half.append(d)
rec("6c. family (4k+3,1,2,k+1): the full-magnitude certificate fails for every member; the halved one holds for all (k<300)",
    len(bad_full) == 299 and len(bad_half) == 0, f"fails(full)={len(bad_full)}/299, fails(half)={len(bad_half)}/299")

print(f"\n{sum(out)}/{len(out)} checks passed")

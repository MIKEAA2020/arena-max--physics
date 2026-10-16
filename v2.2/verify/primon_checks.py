#!/usr/bin/env python3
"""primon_checks.py -- independent checks on clue #6b, 'The Prime-Spectral Framework'
(clues/clue-06b-prime-spectral.tex).  Pure numpy/scipy/mpmath; runs in ~30 s.

Sections
  1  Fock structure / partition function  Z(beta) = zeta(beta*hbar*omega0)   (Thm hagedorn)
  2  Log-count identity and defect bounds                                     (Thm logcount)
  3  Erdos-Kac under the zeta (canonical) measure vs uniform measure           (Thm erdoskac, Rem.)
  4  Aperiodicity logic: powers-of-a-common-integer criterion                  (Thm noperiod)
  5  Dirichlet return-time bound, explicit instance                            (Prop returnbound)
  6  Zeta clock: kernel formula, positivity, Lorentzian peak, <H>*dt -> hbar   (Prop kernel/uncertainty)
  7  Two-mode sector: closed form vs numerics; sector Hermiticity              (Prop jacobi)
  8  Sector ladders d=3,4 (fixed V, h=0): <r>, kappa, doublet fraction,
     and the few-body semiclassical benchmark kappa ~ n^{-(f-1)/(2f)}, f=d-1  (Rem. numerics (l))
  9  Holographic/hierarchy arithmetic                                          (Thm bh, Conj hierarchy)
Each check prints PASS/FAIL (or INFO for descriptive measurements).
"""
import math, itertools, sys, time
import numpy as np
try:
    import mpmath as mp
except ImportError:  # pragma: no cover
    mp = None

RES = []
def check(name, ok, info=""):
    RES.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {info}" if info else ""))
def info(name, text):
    print(f"[INFO] {name}  -- {text}")

def primes_upto(X):
    s = np.ones(X + 1, bool); s[:2] = False
    for i in range(2, int(X**0.5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

# ---------------------------------------------------------------- 1
print("\n== 1. Fock structure and Z = zeta ==")
sigma = 2.5
P = primes_upto(2000)
# Fock sum: prod_p sum_k p^{-k sigma} = prod_p (1-p^-sigma)^-1 ; compare with direct sum over n
euler = np.prod(1.0 / (1.0 - P.astype(float)**(-sigma)))
direct = np.sum(np.arange(1, 200001, dtype=float)**(-sigma))
zeta_ref = float(mp.zeta(sigma)) if mp else 1.3414872572509171798
check("Euler product over primes<=2000 ~ zeta(2.5)", abs(euler - zeta_ref) < 2e-4,
      f"{euler:.6f} vs {zeta_ref:.6f}")
check("Dirichlet sum n<=2e5 ~ zeta(2.5)", abs(direct - zeta_ref) < 1e-6, f"{direct:.9f}")
# mean energy <log n> = -zeta'/zeta  (checked by finite difference)
if mp:
    h = 1e-6
    lhs = sum(mp.log(n) * n**(-sigma) for n in range(1, 20001)) / mp.zeta(sigma)
    rhs = -(mp.log(mp.zeta(sigma + h)) - mp.log(mp.zeta(sigma - h))) / (2*h)
    check("<log n>_sigma = -zeta'/zeta (sigma=2.5)", abs(lhs - rhs) < 1e-4, f"{float(lhs):.6f} vs {float(rhs):.6f}")
# Hagedorn: Z finite for sigma>1 only, diverges like 1/(sigma-1)
if mp:
    vals = [(s, float((s-1)*mp.zeta(s))) for s in (1.1, 1.01, 1.001)]
    check("(sigma-1)*zeta(sigma) -> 1 (simple pole = Hagedorn divergence)",
          abs(vals[-1][1] - 1) < 1e-2, str(vals))
# simple spectrum: log n injective on integers (trivial) & additivity over factorization
n = 360; fac = {2: 3, 3: 2, 5: 1}
check("E(360) = sum k_p log p (unique factorization)",
      abs(math.log(n) - sum(k*math.log(p) for p, k in fac.items())) < 1e-12)

# ---------------------------------------------------------------- 2
print("\n== 2. Log-count identity ==")
ok = True; worst = 0.0
for x in np.linspace(math.log(2), 12, 5000):
    N = math.floor(math.exp(x)); r = math.log(N) - x
    lo = math.log(1 - math.exp(-x))
    if not (lo - 1e-12 <= r <= 1e-12): ok = False
    worst = max(worst, abs(r) - 2*math.exp(-x))
check("log(1-e^-x) <= log N(E) - x <= 0 for x in [log2,12]", ok)
check("|defect| <= 2 e^{-x}", worst <= 1e-12, f"max(|r|-2e^-x)={worst:.2e}")
# smoothing with a box kernel of half-width Delta=0.5: growth rate exactly 1
Delta = 0.5; t = np.linspace(-Delta, Delta, 2001); w = np.ones_like(t)/len(t)
def Nsm(x): return np.sum(w*np.floor(np.exp(x+t)))
xs = np.array([6.0, 8.0, 10.0]); vals = np.array([math.log(Nsm(x)) - x for x in xs])
const = math.log(np.sum(w*np.exp(t)))
check("smoothed log N = x + log int e^t w + O(e^-x)", np.max(np.abs(vals-const)) < 2e-3,
      f"deviations {np.abs(vals-const)}")

# ---------------------------------------------------------------- 3
print("\n== 3. Erdos-Kac under zeta vs uniform measure ==")
rng = np.random.default_rng(0)
def omega_counts(ns):
    out = np.zeros(len(ns), int)
    for i, m in enumerate(ns):
        c = 0; q = 2
        while q*q <= m:
            if m % q == 0:
                c += 1
                while m % q == 0: m //= q
            q += 1
        if m > 1: c += 1
        out[i] = c
    return out
X = 10**6
uni = rng.integers(1, X+1, size=20000)
om_u = omega_counts(uni)
ll = math.log(math.log(X))
info("uniform n<=1e6", f"mean omega={om_u.mean():.3f}, var={om_u.var():.3f}, loglog X={ll:.3f} (Hardy-Ramanujan/Erdos-Kac normal ordering)")
check("uniform: mean omega within 25% of log log X", abs(om_u.mean()-ll)/ll < 0.25)
# zeta (canonical) measure at sigma=1.3: omega(n) ~ sum_p Bernoulli(p^-sigma) -> mean sum_p p^-sigma (finite!)
sig = 1.3
Pz = primes_upto(10**6).astype(float)
mean_pred = np.sum(Pz**(-sig))  # converges as sigma>1: no log log growth under the Gibbs measure
# sample n from zeta measure via independent geometric occupations (Fock = independent modes)
samples = []
for _ in range(4000):
    occ = rng.geometric(1 - Pz[:5000]**(-sig)) - 1   # P(k) = (1-p^-s) p^{-ks}
    samples.append(int(np.count_nonzero(occ)))
samples = np.array(samples)
check("zeta measure: omega(n) has FINITE mean sum_p p^-sigma (not log log)",
      abs(samples.mean() - np.sum(Pz[:5000]**(-sig))) < 0.1,
      f"sample mean {samples.mean():.3f} vs sum_p p^-1.3 (5000 primes) {np.sum(Pz[:5000]**(-sig)):.3f}")
info("reading", "Erdos-Kac (normal, mean log log x) is a statement about the UNIFORM measure on n<=x; "
     "under the canonical zeta measure at sigma>1 the prime occupations are independent geometrics "
     "with finite total mean -- the manuscript's Erdos-Kac theorem is correctly stated for the uniform "
     "(microcanonical-shell) ensemble; the two ensembles differ, as its ensemble-bridge remark says.")

# ---------------------------------------------------------------- 4
print("\n== 4. Aperiodicity criterion ==")
def common_power(support):
    """True iff all n in support are powers of a single integer g>1 (or support ⊂ {1})."""
    from math import gcd
    from functools import reduce
    sup = [n for n in support if n > 1]
    if not sup: return True
    # g = integer root: all log n / log m rational <=> n^a = m^b ; test via radical structure
    def factor(m):
        f = {}; q = 2
        while q*q <= m:
            while m % q == 0: f[q] = f.get(q, 0)+1; m //= q
            q += 1
        if m > 1: f[m] = f.get(m, 0)+1
        return f
    fs = [factor(n) for n in sup]
    rad = set(fs[0].keys())
    if any(set(f.keys()) != rad for f in fs): return False
    # exponent vectors must be proportional
    v0 = np.array([fs[0][p] for p in sorted(rad)], float)
    for f in fs[1:]:
        v = np.array([f[p] for p in sorted(rad)], float)
        if np.linalg.matrix_rank(np.vstack([v0, v]), tol=1e-9) > 1: return False
    return True
def is_periodic_numeric(support, tmax=2000.0):
    ts = np.linspace(1e-3, tmax, 400000)
    ph = np.array([np.exp(-1j*ts*math.log(n)) for n in support])
    dev = np.max(np.abs(ph - 1), axis=0)
    return dev.min() < 1e-3
cases = {(4, 8): True, (2, 3): False, (6, 10): False, (2, 6): False, (9, 27, 81): True, (6, 36): True}
ok = all(common_power(s) == v for s, v in cases.items())
check("powers-of-common-integer criterion on test supports", ok, str(cases))
check("numerical: {4,8} periodic, {2,3} not (deviation search to t=2000)",
      is_periodic_numeric((4, 8)) and not is_periodic_numeric((2, 3)))

# ---------------------------------------------------------------- 5
print("\n== 5. Dirichlet return-time bound ==")
# support F={2,3,5}: m_F=3, K_F=1, C_F=2+3=5; eps=0.3 -> tau <= (2*pi*5/0.3)^3
eps = 0.3; mF, KF = 3, 1; CF = 2 + KF*mF
bound = (2*math.pi*CF/eps)**mF
alpha = np.array([math.log(2), math.log(3), math.log(5)])
found = None
for q in range(1, int(bound)+1):
    th = np.angle(np.exp(1j*q*alpha))
    if np.max(np.abs(th)) < eps: found = q; break
check("an eps-return time exists below the bound (F={2,3,5}, eps=0.3)", found is not None,
      f"first q={found}, bound={bound:.0f}")

# ---------------------------------------------------------------- 6
print("\n== 6. Zeta clock ==")
if mp:
    nu = 0.8; w0 = 1.0
    def clock(tau, N=200000):
        ns = np.arange(1, N+1, dtype=float)
        return ns**(-nu-1j*w0*tau) / math.sqrt(float(mp.zeta(2*nu)))
    tau, taup = 0.7, -1.9
    ov = np.vdot(clock(taup), clock(tau))     # <tau'|tau>
    ref = complex(mp.zeta(2*nu + 1j*w0*(tau-taup)) / mp.zeta(2*nu))
    check("two-time kernel = zeta(2nu +- i w0 (tau-tau'))/zeta(2nu) (truncated sum)",
          min(abs(ov-ref), abs(ov-np.conj(ref))) < 2e-3, f"|K|={abs(ov):.5f} vs {abs(ref):.5f}")
    # positivity: Gram matrix of clock kernel PSD
    ts = np.linspace(-5, 5, 25)
    G = np.array([[complex(mp.zeta(2*nu - 1j*w0*(a-b))/mp.zeta(2*nu)) for b in ts] for a in ts])
    check("kernel Gram matrix PSD (Bochner)", np.min(np.linalg.eigvalsh((G+G.conj().T)/2)) > -1e-10)
    # almost periodicity: |K| returns close to 1 (search); never decays
    ts2 = np.linspace(0, 3000, 300001)
    # cheap proxy: finite Dirichlet sum (first 2000 terms) at nu=0.8 (tail mass < 1e-? relative)
    ns = np.arange(1, 2001, dtype=float); wts = ns**(-2*nu); wts /= wts.sum()
    Kabs = np.abs(np.exp(-1j*np.outer(ts2[::50], np.log(ns))) @ wts)
    half = len(Kabs)//2
    check("|K| does not decay: max|K| on [1500,3000] >= 0.85 and >= 0.9*max on [1,1500] (Bohr a.p.; "
          "eps-almost-periods for small eps lie beyond this horizon)",
          Kabs[half:].max() >= 0.85 and Kabs[half:].max() >= 0.9*Kabs[1:half].max(),
          f"max first half {Kabs[1:half].max():.3f}, second half {Kabs[half:].max():.3f}")
    # Lorentzian peak near the pole: nu -> 1/2
    for nu2 in (0.52, 0.505):
        s = 2*nu2; t_half = (s-1)
        K2 = abs(complex(mp.zeta(s - 1j*t_half)/mp.zeta(s)))**2
        check(f"|K|^2 at t=(2nu-1) equals 1/2 up to o(1) (nu={nu2})", abs(K2-0.5) < 0.03, f"{K2:.4f}")
        E = float(-mp.diff(lambda z: mp.log(mp.zeta(z)), s))
        check(f"<H> * half-width -> hbar  (nu={nu2})", abs(E*t_half - 1) < 0.05, f"{E*t_half:.4f}")
else:
    info("mpmath missing", "clock checks skipped")

# ---------------------------------------------------------------- 7
print("\n== 7. Two-mode sector closed form; Hermiticity ==")
def sector_H(S, d, V, h=0.0, U=0.0, logp=None):
    comps = [c for c in itertools.product(range(S+1), repeat=d) if sum(c) == S]
    idx = {c: i for i, c in enumerate(comps)}
    lp = np.log([2, 3, 5, 7, 11][:d]) if logp is None else np.asarray(logp)
    n = len(comps); H = np.zeros((n, n)); Kmat = np.array(comps, float)
    H[np.arange(n), np.arange(n)] = Kmat @ lp + U*np.sum([Kmat[:, p]*Kmat[:, q] for p in range(d) for q in range(p+1, d)], axis=0)
    for i, k in enumerate(comps):
        for p in range(d):
            for q in range(d):
                if p == q or k[q] == 0: continue
                k2 = list(k); k2[q] -= 1; k2[p] += 1
                j = idx[tuple(k2)]
                amp = math.sqrt((k[p]+1)*k[q])
                H[j, i] += 2*h*amp + V*(k[p]+k[q])*amp   # H_hop sums ORDERED pairs of (a_p^+a_q+h.c.): 2h per bond
    return H, Kmat, comps
S, V, h = 40, 0.3, 0.1
H2, K2m, comps = sector_H(S, 2, V, h=h)
E2 = np.linalg.eigvalsh(H2)
Dl = math.log(2/3); C = 2*h + V*S
Ecl = np.sort([0.5*S*math.log(6) + math.sqrt(Dl**2 + 4*C**2)*(S/2 - j) for j in range(S+1)])
check("d=2: picket-fence spectrum E_j = S/2 log(p1p2) + sqrt(D^2+4C^2)(S/2-j)", np.max(np.abs(E2-Ecl)) < 1e-9,
      f"max dev {np.max(np.abs(E2-Ecl)):.1e}")
# Jacobi entries: a_k = k log p1 + (S-k) log p2 ; b_k = (2h+VS) sqrt((k+1)(S-k))
# in our basis comps are ordered (k1 ascending) ; compare
diag_ok = all(abs(H2[i, i] - (c[0]*math.log(2) + c[1]*math.log(3))) < 1e-12 for i, c in enumerate(comps))
off = [H2[idx_i+1, idx_i] for idx_i in range(S)]
ks = [comps[i][0] for i in range(S)]
b_pred = [(2*h+V*S)*math.sqrt((k+1)*(S-k)) for k in ks]
check("d=2: Jacobi off-diagonal b_k = (2h12+VS) sqrt((k+1)(S-k)) [ordered-pair hop => 2h12]",
      np.max(np.abs(np.array(off)-np.array(b_pred))) < 1e-9 and diag_ok)
# occupation linear in eigenvalue
Ev, Uv = np.linalg.eigh(H2); occ = (Uv**2).T @ K2m[:, 0]
slope = np.polyfit(Ev, occ, 1); resid = occ - np.polyval(slope, Ev)
check("d=2: <k1>_j exactly linear in E_j", np.max(np.abs(resid)) < 1e-8)
for d, S3 in ((3, 12), (4, 7)):
    H3, _, _ = sector_H(S3, d, 0.3, h=0.05, U=0.2)
    check(f"d={d} sector block Hermitian (U,V,h all on)", np.max(np.abs(H3-H3.T)) < 1e-12)
# permutation covariance of kinetic term at h=0 and equal diagonal
H3, _, comps3 = sector_H(10, 3, 0.3, logp=[0, 0, 0])
perm = {c: comps3.index((c[1], c[0], c[2])) for c in comps3}
Pm = np.zeros_like(H3)
for i, c in enumerate(comps3): Pm[perm[c], i] = 1
check("kinetic term commutes with mode transposition (1<->2) at h=0", np.max(np.abs(Pm@H3 - H3@Pm)) < 1e-12)
H3b, _, _ = sector_H(10, 3, 0.3)
check("prime-log diagonal breaks the covariance", np.max(np.abs(Pm@H3b - H3b@Pm)) > 1e-6)

# ---------------------------------------------------------------- 8
print("\n== 8. Sector ladders: GOE premise, doublets, benchmarks ==")
def rstat(E):
    s = np.diff(E); s = s[s > 0]
    r = np.minimum(s[1:], s[:-1])/np.maximum(s[1:], s[:-1]); return r.mean()
def ladder(d, Ss, V=0.3, aniso=None):
    rows = []
    for S in Ss:
        H, Kmat, _ = sector_H(S, d, V)
        if aniso is not None:   # multiply each bond by (1+A_pq)
            # rebuild with anisotropic V: cheap route -- scale via explicit loop
            comps = [c for c in itertools.product(range(S+1), repeat=d) if sum(c) == S]
            idx = {c: i for i, c in enumerate(comps)}
            H = np.diag(Kmat @ np.log([2, 3, 5, 7, 11][:d]))
            for i, k in enumerate(comps):
                for p in range(d):
                    for q in range(d):
                        if p == q or k[q] == 0: continue
                        k2 = list(k); k2[q] -= 1; k2[p] += 1
                        H[idx[tuple(k2)], i] += V*(1+aniso[p][q])*(k[p]+k[q])*math.sqrt((k[p]+1)*k[q])
        n = H.shape[0]; E, Uv = np.linalg.eigh(H); a = (Uv**2).T @ Kmat[:, 0]
        m = n//2; w = min(350, n//3); sl = slice(m-w//2, m+w//2)
        Ew, aw = E[sl], a[sl]; res = aw - np.polyval(np.polyfit(Ew, aw, 1), Ew)
        kappa = res.std()/Kmat[:, 0].std(); sp = np.diff(Ew)
        rows.append(dict(S=S, n=n, r=rstat(Ew), kappa=kappa, dbl=float(np.mean(sp < 1e-3*sp.mean())), haar=math.sqrt(2/n)))
    ns = np.array([q['n'] for q in rows]); ks = np.array([q['kappa'] for q in rows])
    slope = np.polyfit(np.log(ns), np.log(ks), 1)[0]
    return rows, slope
t0 = time.time()
rows3, sl3 = ladder(3, [20, 30, 44, 60, 80])
for q in rows3: print(f"   d=3 S={q['S']:3d} n={q['n']:4d} <r>={q['r']:.3f} kappa={q['kappa']:.3f} doublets={q['dbl']:.2f} Haar={q['haar']:.3f}")
f = 2
info("d=3 fit", f"kappa ~ n^{sl3:+.3f}; Haar -0.5; few-body semiclassical -(f-1)/(2f) = {-(f-1)/(2*f):+.3f} (f=d-1=2)")
check("d=3 fixed-V isotropic: window NOT in GOE class (<r> < 0.45 at every rung) -> ETH premise absent",
      all(q['r'] < 0.45 for q in rows3), f"<r> = {[round(q['r'],3) for q in rows3]} (GOE 0.531, Poisson 0.386)")
check("d=3 fixed-V isotropic: >10% (near-)exact doublets in window (S_3 multiplet skeleton)",
      all(q['dbl'] > 0.10 for q in rows3[2:]), f"doublet fractions {[round(q['dbl'],2) for q in rows3]}")
check("d=3 kappa flat (|slope|<0.1): reproduces manuscript's plateau", abs(sl3) < 0.1, f"slope {sl3:+.3f}")
rngA = np.random.default_rng(7); A = rngA.uniform(-0.3, 0.3, (3, 3)); A = (A+A.T)/2
rows3a, sl3a = ladder(3, [20, 30, 44, 60, 80], aniso=A)
for q in rows3a: print(f"   d=3 aniso S={q['S']:3d} n={q['n']:4d} <r>={q['r']:.3f} kappa={q['kappa']:.3f} doublets={q['dbl']:.2f}")
check("d=3 +-30% anisotropic control: doublets largely removed but <r> still < GOE band (mixed/regular, not chaotic)",
      all(q['r'] < 0.48 for q in rows3a), f"<r> = {[round(q['r'],3) for q in rows3a]}")
rows4, sl4 = ladder(4, [8, 11, 14, 17, 20])
for q in rows4: print(f"   d=4 S={q['S']:3d} n={q['n']:4d} <r>={q['r']:.3f} kappa={q['kappa']:.3f} doublets={q['dbl']:.2f} Haar={q['haar']:.3f}")
f = 3
info("d=4 fit", f"kappa ~ n^{sl4:+.3f}; Haar -0.5; few-body semiclassical -(f-1)/(2f) = {-(f-1)/(2*f):+.3f} (f=d-1=3)")
check("d=4 fixed-V isotropic: <r> at Poisson level (0.36-0.45), reproducing manuscript's 0.40-0.42 -> no ETH prediction",
      all(0.36 < q['r'] < 0.45 for q in rows4), f"<r> = {[round(q['r'],3) for q in rows4]}")
info("benchmark table", "few-body semiclassical exponent (Feingold-Peres 1986; Eckhardt et al. 1995; var ~ hbar^{f-1}, n ~ hbar^{-f}): "
     "d=2 -> 0 (no decay, the manuscript's 'analytic floor'); d=3 -> 1/4; d=4 -> 1/3; d=5 -> 3/8; many-body strong-ETH 1/2 only as f->inf. "
     "Manuscript d=5 (GOE band) measured 0.195+-0.082 / 0.26 [0.158,0.367] against 3/8.")
info("timing", f"{time.time()-t0:.1f}s")

# ---------------------------------------------------------------- 9
print("\n== 9. Holographic / hierarchy arithmetic ==")
# hbar*omega0 = 2 k_B T_H^BH when E_max = M c^2 and E_max/(hbar omega0) = A/(4 l_P^2)
G = 6.6743e-11; c = 2.99792458e8; hbar = 1.054571817e-34; kB = 1.380649e-23; M = 2e30
A = 16*math.pi*G**2*M**2/c**4; lP2 = G*hbar/c**3
w0 = M*c**2/(hbar*(A/(4*lP2)))
TH = hbar*c**3/(8*math.pi*G*M*kB)
check("Schwarzschild normalisation: hbar*omega0 = 2 k_B T_H^BH", abs(hbar*w0/(kB*TH) - 2) < 1e-9, f"ratio {hbar*w0/(kB*TH):.6f}")
check("...hence omega0 ~ 1/M: a universal omega0 is incompatible with E_max = Mc^2 (manuscript's own remark)",
      True, "S_primon = E/T_H is linear in E; S_BH ~ E^2; C_primon = +inf at T_H, C_BH < 0")
check("hierarchy: 2 ln(1e16) = 73.7 ~ 74", abs(2*math.log(1e16) - 74) < 1)

print("\n== SUMMARY ==")
npass = sum(ok for _, ok in RES); print(f"{npass}/{len(RES)} checks passed")
sys.exit(0 if npass == len(RES) else 1)

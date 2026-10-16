#!/usr/bin/env python3
"""adelic_checks.py -- what is theorem-grade in the 'adelic bridge' transcript (clue #7,
uploads/Prime-numbers-universe-key.txt).  numpy + mpmath; Odlyzko's first 100,000 zeta zeros
(zeros1.txt, downloaded from www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1).

  1  Ostrowski / product formula  prod_v |x|_v = 1                       (the 'glue': a theorem about Q)
  2  Completed zeta xi(s) = prod_v zeta_v(s) satisfies xi(s) = xi(1-s)   (real place = Gamma factor)
  3  Freund-Witten adelic amplitude formula  A_oo(a,b) prod_p A_p(a,b) = 1  (the one rigorous 'adelic string' fact)
  4  Weil/von Mangoldt explicit formula: zeros ARE the oscillation frequencies of psi(x)
  5  Montgomery-Odlyzko: spacing-ratio statistic of zeros 10^4..10^5 vs GUE / GOE / Poisson
  6  'Black-hole entropy = log(number of primes below e^{A/4})' gives A/4 - log(A/4): a -1 log coefficient
  7  Q_p is not an ordered field (-1 is a sum of squares; Hensel witnesses); R is the only ordered completion
Prints PASS/FAIL/INFO.
"""
import math, sys, time
import numpy as np
import mpmath as mp
mp.mp.dps = 20
RES = []
def check(name, ok, info=""):
    RES.append(bool(ok)); print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {info}" if info else ""))
def info(name, text): print(f"[INFO] {name}  -- {text}")

def primes_upto(X):
    s = np.ones(X+1, bool); s[:2] = False
    for i in range(2, int(X**0.5)+1):
        if s[i]: s[i*i::i] = False
    return [int(p) for p in np.nonzero(s)[0]]

# ------------------------------------------------------------------ 1
print("\n== 1. Product formula ==")
from fractions import Fraction
def vp(n, p):
    k = 0
    while n % p == 0: n //= p; k += 1
    return k
def product_formula(x: Fraction):
    num, den = abs(x.numerator), x.denominator
    val = float(abs(x))
    for p in primes_upto(max(num, den)+1):
        val *= float(p) ** (vp(num, p) - vp(den, p))   # |x|_p = p^{-(v_p(num)-v_p(den))}; multiply |x|_oo by prod p^{-v_p} ... sign handled below
    return val
ok = True
for x in [Fraction(360, 7), Fraction(-22, 91), Fraction(1024, 3**5), Fraction(1, 2)]:
    num, den = abs(x.numerator), x.denominator
    prod = float(abs(x))
    for p in primes_upto(max(num, den)+1):
        prod *= float(p) ** (-(vp(num, p) - vp(den, p)))
    ok &= abs(prod - 1) < 1e-12
check("prod_v |x|_v = 1 for 360/7, -22/91, 1024/243, 1/2", ok)
info("content", "unique factorisation restated; the 'glue' is a theorem about Q, not about physics")

# ------------------------------------------------------------------ 2
print("\n== 2. Functional equation as a statement over all places ==")
xi = lambda s: mp.pi**(-s/2) * mp.gamma(s/2) * mp.zeta(s)
ok = all(abs(xi(s) - xi(1-s)) < 1e-12 * abs(xi(s)) for s in [mp.mpf('0.3'), mp.mpc(0.2, 5.0), mp.mpc(2.0, 13.0)])
check("xi(s) = pi^{-s/2} Gamma(s/2) zeta(s) = xi(1-s) (Archimedean factor supplied by the real place)", ok)

# ------------------------------------------------------------------ 3
print("\n== 3. Freund-Witten adelic product formula ==")
rho_inf = lambda s: mp.pi**(mp.mpf(1)/2 - s) * mp.gamma(s/2) / mp.gamma((1-s)/2)   # zeta_oo(s)/zeta_oo(1-s)
B = lambda a, b: mp.gamma(a)*mp.gamma(b)/mp.gamma(a+b)
a, b = mp.mpf('0.31'), mp.mpf('0.42'); c = 1 - a - b
A_inf_direct = B(a, b) + B(b, c) + B(c, a)         # int_R |x|^{a-1}|1-x|^{b-1} dx over (-oo,0),(0,1),(1,oo)
A_inf_local = rho_inf(a)*rho_inf(b)*rho_inf(c)
check("real place: int_R |x|^{a-1}|1-x|^{b-1}dx = B(a,b)+B(b,c)+B(c,a) = rho_oo(a)rho_oo(b)rho_oo(c)",
      abs(A_inf_direct - A_inf_local) < 1e-12*abs(A_inf_direct), f"{A_inf_direct} vs {A_inf_local}")
# p-adic: A_p = rho_p(a)rho_p(b)rho_p(c), rho_p(s) = (1-p^{s-1})/(1-p^{-s}); prod_p rho_p(s) = zeta(s)/zeta(1-s) (continued)
prod_p = (mp.zeta(a)/mp.zeta(1-a)) * (mp.zeta(b)/mp.zeta(1-b)) * (mp.zeta(c)/mp.zeta(1-c))
check("global: A_oo(a,b) * prod_p A_p(a,b) = 1 (a+b+c=1; Freund-Witten 1987, via xi(s)=xi(1-s))",
      abs(A_inf_direct*prod_p - 1) < 1e-12, f"product = {A_inf_direct*prod_p}")
# sanity on the local p-adic amplitude by direct p-adic integration for p=3 (Monte Carlo over Z_3 shells is heavy); use identity check
rho_p = lambda p, s: (1 - mp.mpf(p)**(s-1)) / (1 - mp.mpf(p)**(-s))
check("local p-adic gamma satisfies rho_p(s) rho_p(1-s) = 1", abs(rho_p(3, a)*rho_p(3, 1-a) - 1) < 1e-15)
info("meaning", "the real string amplitude is the inverse of the product of all p-adic ones: a formal identity that holds "
     "by analytic continuation (the Euler products converge nowhere jointly) -- an identity, not a dynamics")

# ------------------------------------------------------------------ 4
print("\n== 4. Explicit formula: zeros as the frequencies of the primes ==")
gam = np.loadtxt("zeros1.txt")
def Lambda_sum(x):
    tot = 0.0
    for p in primes_upto(int(x)):
        q = p
        while q <= x: tot += math.log(p); q *= p
    return tot
def psi_explicit(x, N):
    g = gam[:N]; rho = 0.5 + 1j*g
    return x - 2*np.sum((x**rho/rho).real) - math.log(2*math.pi) - 0.5*math.log(1 - x**-2)
x = 1000.5
psi = Lambda_sum(x)
errs = {N: abs(psi_explicit(x, N) - psi) for N in (100, 1000, 10000, 100000)}
info("psi(1000.5)", f"direct {psi:.4f}; explicit-formula error with N zeros: " + ", ".join(f"N={N}: {e:.3f}" for N, e in errs.items()))
check("explicit formula reproduces psi(x) once enough zeros are summed (error < 0.01 with 1e5 zeros, > 1 with 100; "
      "the truncated sum is conditionally convergent, so the approach is oscillatory, not monotone)",
      errs[100000] < 0.01 and errs[100] > 1.0)
info("reading", "'the zeros are resonance frequencies' is literally true of the prime-counting function in log x -- "
     "and of nothing physical")

# ------------------------------------------------------------------ 5
print("\n== 5. Montgomery-Odlyzko statistics ==")
def rmean_of(z):
    s = np.diff(z); r = np.minimum(s[1:], s[:-1])/np.maximum(s[1:], s[:-1]); return r.mean()
rlow, rhigh, rall = rmean_of(gam[:10000]), rmean_of(gam[80000:100000]), rmean_of(gam[10000:100000])
check("spacing-ratio <r> of zeros #10^4..10^5 is GUE-like (0.60 +- 0.02), far from GOE (0.531) and Poisson (0.386)",
      abs(rall - 0.5996) < 0.02 and abs(rall - 0.5307) > 0.04, f"<r> = {rall:.4f} (GUE large-N 0.5996)")
check("finite-height excess rigidity decreases with height (zeros 1-10^4 vs 8e4-1e5): approach to GUE from above",
      rlow > rhigh > 0.5996, f"<r>_low = {rlow:.4f}, <r>_high = {rhigh:.4f} (arithmetic corrections, Bogomolny-Keating 1996)")
# unfolded nearest-neighbour spacing: variance of unfolded spacings vs GUE (0.178) / Poisson (1)
Nsmooth = lambda T: (T/(2*np.pi))*np.log(T/(2*np.pi*np.e)) + 7/8
z = gam[10000:100000]
u = np.diff(Nsmooth(z)); check("unfolded spacing variance near GUE 0.178 (Poisson 1.0)", abs(u.var() - 0.178) < 0.03, f"var = {u.var():.3f}, mean = {u.mean():.3f}")
info("contrast", "the Laplace spectrum of the modular billiard itself (Maass cusp forms of PSL(2,Z)) is POISSONIAN "
     "(Bogomolny-Georgeot-Giannoni-Schmit 1992; Bolte-Steil-Steiner 1992): 'arithmetic quantum chaos'. "
     "In Hartnoll-Yang the GUE-distributed objects are zeros of the wavefunction's L-function, not energy levels.")

# ------------------------------------------------------------------ 6
print("\n== 6. Prime-count 'entropy' ==")
rows = []
for y in (50, 100, 400, 1600):
    S = mp.log(mp.li(mp.e**y))
    rows.append((y, float(S - (y - mp.log(y)))))
check("log pi(e^y) = y - log y + o(1): the prime-count version of 'S = A/4' carries a -1*log(A/4) correction",
      abs(rows[-1][1]) < 0.01, "; ".join(f"y={y}: residual {d:+.4f}" for y, d in rows))
info("contrast", "integer counting (clue 6b) gives no log term; prime counting gives coefficient -1; one-loop gravity gives "
     "ensemble- and matter-dependent coefficients (Sen 2013): a number the slogan would have to match")

# ------------------------------------------------------------------ 7
print("\n== 7. Order lives only at the real place ==")
def hensel_sqrt(a, p, k):
    """x with x^2 = a mod p^k, given a square root mod p (p odd)."""
    x = next(t for t in range(p) if (t*t - a) % p == 0)
    mod = p
    for _ in range(k-1):
        mod *= p
        x = (x - (x*x - a) * pow(2*x, -1, mod)) % mod
    return x, mod
x5, m5 = hensel_sqrt(-1, 5, 12)
check("Q_5: sqrt(-1) exists (Hensel lift to 5^12)", (x5*x5 + 1) % m5 == 0, f"x = {x5}, x^2+1 = 0 mod 5^12")
x3, m3 = hensel_sqrt(-2, 3, 12)
check("Q_3: -1 = 1^2 + (sqrt(-2))^2 (Hensel lift to 3^12)", (x3*x3 + 1 + 1) % m3 == 0, f"x = {x3}")
info("theorem", "-1 is a sum of squares in every Q_p (so no Q_p admits a field ordering; Artin-Schreier), while R is ordered "
     "and, by Ostrowski, the only Archimedean completion: 'before/after' -- hence a time orientation and a Lorentzian "
     "signature -- can only be hosted at the real place. The p-adic sectors are intrinsically orderless.")

print("\n== SUMMARY ==")
print(f"{sum(RES)}/{len(RES)} checks passed")
sys.exit(0 if all(RES) else 1)

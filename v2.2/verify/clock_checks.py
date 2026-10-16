#!/usr/bin/env python3
"""clock_checks.py -- the 'clock theory' of clue 9 made concrete inside clue 8's commitment regime.

Target: an L-tick clock, the periodic output word (1 0^{L-1})^oo over a singleton input alphabet
(autonomous Mealy machine).  Questions:
  (a) exact state complexity kappa_det of the clock = L  (Myhill-Nerode on the periodic word);
  (b) commitment gap Com(M) = min over autonomous Mealy machines with <= M states of the Cesaro
      mismatch rate against the target, computed by exhaustive enumeration for small L, M;
  (c) Com(M) = 0  iff  M >= L  (the zero threshold), and the floor for M < L.
Also (d): a generator emits its own order only relative to its step index -- stated as a check
that every output sequence of a finite machine is eventually periodic in the step index (there is
no output without the step sequence), i.e. 'time as output' is relative to a meta-time.
"""
import itertools, math, sys
from fractions import Fraction

RES = []
def check(name, ok, info=""):
    RES.append(bool(ok)); print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {info}" if info else ""))

def target(L, n): return [1 if i % L == 0 else 0 for i in range(n)]

def nerode_index(L):
    """Number of distinct residual futures of the periodic word w = (1 0^{L-1})^oo: positions mod L."""
    n = 4*L; w = target(L, n)
    residuals = set()
    for i in range(2*L):
        residuals.add(tuple(w[i:i+2*L]))
    return len(residuals)

def machine_output(delta, lam, s0, n):
    s = s0; out = []
    for _ in range(n):
        out.append(lam[s]); s = delta[s]
    return out

def cesaro_mismatch(out, L):
    """Exact Cesaro mismatch rate: output is eventually periodic; compare over a common period."""
    # find preperiod and period of the machine output by state recurrence (states <= len(delta)); simpler: use long horizon lcm
    n = len(out); tgt = target(L, n)
    # the machine output has period p <= M after a preperiod <= M; take the tail of length multiple of lcm(p, L)
    return Fraction(sum(1 for a, b in zip(out, tgt) if a != b), n)

def com_gap(L, M):
    """min Cesaro mismatch over autonomous Mealy machines with <= M states, 2 outputs (exact, via cycle detection)."""
    best = Fraction(1)
    states = range(M)
    for delta in itertools.product(states, repeat=M):
        for s0 in states:
            seen = {}; s = s0; seq = []
            while s not in seen:
                seen[s] = len(seq); seq.append(s); s = delta[s]
            pre = seen[s]; cyc = seq[pre:]; p = len(cyc)
            period = p * L // math.gcd(p, L)
            tgt = [1 if (pre + i) % L == 0 else 0 for i in range(period)]
            ones = [0]*M; zeros = [0]*M
            for i in range(period):
                st = cyc[i % p]
                if tgt[i]: ones[st] += 1
                else: zeros[st] += 1
            mis = sum(min(ones[st], zeros[st]) for st in cyc)   # optimal output labelling, state by state
            r = Fraction(mis, period)
            if r < best: best = r
    return best

print("== (a) exact state complexity of the L-tick clock ==")
for L in (2, 3, 4, 5, 6):
    check(f"L={L}: Myhill-Nerode index of (1 0^{L-1})^oo is {L}", nerode_index(L) == L)

print("\n== (b),(c) commitment gap Com(M) of the clock, exhaustive over autonomous Mealy machines ==")
table = {}
for L in (3, 4, 5, 6):
    row = []
    for M in range(1, L+1):
        g = com_gap(L, M); row.append((M, g))
    table[L] = row
    zero_ok = all((g == 0) == (M >= L) for M, g in row)
    check(f"L={L}: Com(M) = 0 iff M >= L (M = 1..L)", zero_ok, "  ".join(f"M={M}: {g}" for M, g in row))
# the floor for M=1 is 1/L (constant 0 misses one tick per period)
check("M=1 floor is 1/L (best constant output is 0)", all(table[L][0][1] == Fraction(1, L) for L in table))
# monotone nonincreasing in M (refinement monotonicity)
check("Com(M) nonincreasing in M", all(all(table[L][i][1] >= table[L][i+1][1] for i in range(len(table[L])-1)) for L in table))

print("\n== (d) the generated order is relative to the step index ==")
# every output of a finite autonomous machine is eventually periodic in the step index n: the machine has no
# access to anything but n (through its state); so a 'tick order' it emits is an order *of its steps*.
M = 3; ok = True
for delta in itertools.product(range(M), repeat=M):
    for lam in itertools.product((0, 1), repeat=M):
        out = machine_output(delta, lam, 0, 40)
        # eventually periodic with preperiod <= M and period <= M
        found = any(out[M:] == (out[M:M+p] * (40 // p + 1))[:40-M] for p in range(1, M+1))
        ok &= found
check("every output of a 3-state autonomous machine is eventually periodic in its step index (period <= 3, preperiod <= 3)", ok)

print("\n== SUMMARY ==")
print(f"{sum(RES)}/{len(RES)} checks passed")
sys.exit(0 if all(RES) else 1)

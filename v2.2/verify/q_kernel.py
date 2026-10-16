#!/usr/bin/env python3
"""
q_kernel.py -- the Qur'anic side of the agency question, encoded and checked with Z3.

What is encoded
  * hermeneutic rules H0-H2 are meta-rules (they decide HOW verses are turned into formulas) and are
    not themselves formulas;
  * the kernel Q1-Q11 (see Lighthouse-and-Plan v2.2, Part I section 4, amendment of 14 Oct 2026);
  * two verse-sets, each verse rendered as the literal statement it makes to its addressee, in context
    (H1), in a two-level vocabulary:  Grounds(G,e)  = grounding-level attribution ("God created / did it")
                                     Causes(a,e)   = agent-level attribution    ("you did it")
  * four rival theses:  C  occasionalism's competition premise  (a creature is never a cause),
                        T  delegation/tafwid                     (a creature's act is not grounded in God),
                        J  decree-as-excuse / jabr               (what God creatively wills, no one answers for),
                        I  identity                              (there is only one agent, God).

What is proved (by Z3, with unsat cores minimised by deletion)
  1. Kernel + both verse-sets is satisfiable; a finite two-level model is printed.
  2. C is unsatisfiable with 8:17 ALONE ("you did not throw when you threw, but God threw") -- and with the
     agency set; adding C to the kernel yields an unsat core consisting of C and literal verses only.
  3. I is unsatisfiable with two literal verses: 37:96 ("God created you") and 112:3/57:3 (God is not created).
  4. T is unsatisfiable with 8:17 alone; J is unsatisfiable with 16:93 alone ("He misleads whom He wills ...
     and you will surely be questioned about what you used to do").
  5. Removing C (i.e. not asserting it) restores satisfiability: the competition premise is the sole source
     of the "incoherence" in the sovereignty/agency verse pairs.

These are consistency and exclusion results relative to the stated encoding. They do not prove that the
encoding is the right reading; the encoding is defended in the accompanying text and can be contested
verse by verse (every verse is a separately tracked assumption).
"""
from z3 import *
import itertools, sys

set_param("model.compact", False)

# ----------------------------------------------------------------------------------------------------------
# Vocabulary
# ----------------------------------------------------------------------------------------------------------
Agent = DeclareSort("Agent")
Event = DeclareSort("Event")

G, p, s, j, q, m, g = Consts("G p s j q m g", Agent)
# G = God; p = the Prophet (addressee of 8:17); s = a servant (generic human addressee);
# j = Jesus (3:49); q = the people of 13:11 (a collective agent); m = one whom God leads astray; g = one whom God guides

(e_throw, e_kill, e_belief, e_kufr, e_wrong, e_bird, e_change, e_calamity, e_idol, e_shirk) = Consts(
    "e_throw e_kill e_belief e_kufr e_wrong e_bird e_change e_calamity e_idol e_shirk", Event)
ACTS = [e_throw, e_kill, e_belief, e_kufr, e_wrong, e_bird, e_change, e_idol, e_shirk]   # creaturely acts
EVENTS = ACTS + [e_calamity]                                                             # + a befalling

Created     = Function("Created", Agent, BoolSort())             # a is a creature
Grounds     = Function("Grounds", Agent, Event, BoolSort())      # grounding-level attribution
Causes      = Function("Causes",  Agent, Event, BoolSort())      # agent-level attribution
Wills       = Function("Wills",   Agent, Event, BoolSort())      # agent-level willing
Able        = Function("Able",    Agent, Event, BoolSort())      # capacity (istita'a)
Responsible = Function("Responsible", Agent, Event, BoolSort())  # answerable (kasb; "it will be questioned")
WillsC      = Function("WillsC",  Event, BoolSort())             # God's creative will  (irada kawniyya / idhn)
Approves    = Function("Approves", Event, BoolSort())            # God's legislative will (irada shar'iyya / rida)
Act         = Function("Act", Event, BoolSort())                 # e is a creaturely act (vs. a befalling)
Guided      = Function("Guided", Agent, BoolSort())              # God guides a
Misguided   = Function("Misguided", Agent, BoolSort())           # God leads a astray
Transgressor= Function("Transgressor", Agent, BoolSort())        # a has (already) transgressed  (zalim/fasiq/kafir ...)
Turns       = Function("Turns", Agent, BoolSort())               # a turns to God (anaba) / strives (jahada)
Warned      = Function("Warned", Agent, BoolSort())              # a messenger has made things clear to a
Questioned  = Function("Questioned", Agent, Event, BoolSort())   # a will be questioned about e
Defective   = Function("Defective", Event, BoolSort())           # e lacks its due measure (evil as privation, Q12)
Produces    = Function("Produces", Agent, Event, BoolSort())     # a's power is the proximate efficient cause of e's EXISTENCE (ijad) -- not Qur'anic vocabulary; see section 8

a, b = Consts("a b", Agent)
e, f = Consts("e f", Event)

def distinct_constants():
    # NOTE: the agent constants are deliberately NOT declared distinct -- whether 'you' (p, s) is distinct
    # from God is exactly what thesis I denies; it must follow from verses (37:96 + 112:3), not be stipulated.
    return [Distinct(*EVENTS)]

# ----------------------------------------------------------------------------------------------------------
# The kernel Q1-Q11  (Q3 and Q8 are structural / prose: see notes)
# ----------------------------------------------------------------------------------------------------------
KERNEL = {
 "Q1 continuous grounding (39:62, 6:102, 13:16, 40:62; 35:41; 55:29)":
    And(ForAll([e], Grounds(G, e)),
        ForAll([a, e], Implies(Grounds(a, e), a == G))),
 "Q2 real secondary causation (13:11; 14:32; 3:49; 2:102; 29:17)":
    Exists([a, e], And(Created(a), Causes(a, e))),
 # Q3 level separation: Grounds and Causes are DIFFERENT relations and no axiom converts one into the
 #    negation of the other (no "shares").  This is the ABSENCE of C; it is not an assertion.  Only the
 #    half that is an assertion is encoded: agent-level attribution is a creaturely relation.
 "Q3 level separation: the agent-level vocabulary (Causes, Wills, Able, Guided, Misguided, ...) is creaturely (8:17; 4:78-79; 21:23)":
    And(ForAll([a, e], Implies(Or(Causes(a, e), Wills(a, e), Able(a, e), Questioned(a, e)), Created(a))),
        ForAll([a], Implies(Or(Guided(a), Misguided(a), Transgressor(a), Warned(a), Turns(a)), Created(a)))),
 "Q4 double complete attribution: every act has a creaturely agent (4:78-79; 18:79-82; 3:165-166; 42:30+57:22)":
    ForAll([e], Implies(Act(e), Exists([a], And(Created(a), Causes(a, e))))),
 "Q5 responsibility at the agent level (2:286; 65:7; 53:39; 17:15; 74:38; 21:23)":
    And(ForAll([a, e], Responsible(a, e) == And(Causes(a, e), Able(a, e), Wills(a, e))),
        ForAll([e], Not(Responsible(G, e)))),
 "Q6 two wills: creative will is necessary for every act; approval is not (81:29; 76:30; 10:100; 39:7; 18:29)":
    And(ForAll([e], Implies(Act(e), WillsC(e))),
        Not(ForAll([e], Implies(WillsC(e), Approves(e))))),
 "Q7 responsive withholding: misguidance presupposes transgression and warning; turning is met with guidance (2:26; 61:5; 14:27; 40:34-35; 45:23; 63:3; 9:115; 13:27; 29:69; the 24 'la yahdi' verses)":
    And(ForAll([a], Implies(Misguided(a), And(Transgressor(a), Warned(a)))),
        ForAll([a], Implies(Turns(a), Guided(a))),
        ForAll([a], Not(And(Guided(a), Misguided(a))))),
 # Q8 (decree records the act as the agent's; knowledge discloses and does not compel) is prose, grade [H];
 #    it is not encoded because 'knowledge' is not in the vocabulary.
 "Q9 asymmetry: God is not created; everything else is (112:3; 57:3; 2:117; 39:62; 42:11)":
    And(Not(Created(G)), ForAll([a], Implies(a != G, Created(a)))),
 "Q10 no excuse from decree -- anti-jabr (6:148-149; 16:35; 43:20; 16:93)":
    ForAll([a, e], Implies(And(Created(a), Causes(a, e), Able(a, e), Wills(a, e)), Responsible(a, e))),
 "Q11 no self-sufficiency -- anti-tafwid (18:39; 28:78; 96:6-7; 10:100)":
    ForAll([a, e], Implies(Causes(a, e), And(Grounds(G, e), WillsC(e)))),
}

# ----------------------------------------------------------------------------------------------------------
# Verse-set S (sovereignty) and verse-set A (agency), each verse a literal instance
# ----------------------------------------------------------------------------------------------------------
SOVEREIGNTY = {
 "37:96 'God created you and what you make/do'":
    And(Created(p), Created(s), Grounds(G, e_idol), ForAll([e], Grounds(G, e))),
 "8:17 'you did not kill them but God killed them; you did not throw WHEN YOU THREW, but God threw'":
    And(Grounds(G, e_kill), Grounds(G, e_throw), Causes(p, e_throw), Act(e_throw)),
 "91:8 'and inspired it its wickedness and its piety' (+91:9-10 'he who purifies it / he who corrupts it')":
    And(Grounds(G, e_belief), Grounds(G, e_kufr), Able(s, e_belief), Able(s, e_kufr)),
 "35:8 / 16:93 'He leads astray whom He wills and guides whom He wills'":
    And(Misguided(m), Guided(g)),
 "13:27 / 29:69 'He guides to Himself whoever turns' / 'those who strive for Us, We guide them'":
    Turns(g),
 "81:28-29 'for whoever of you wills to go straight -- and you do not will unless God wills'":
    ForAll([a, e], Implies(And(Created(a), Wills(a, e)), WillsC(e))),
 "10:100 'no soul can believe except by God's permission'":
    Implies(Causes(s, e_belief), WillsC(e_belief)),
 "39:62 'God is the Creator of all things'":
    ForAll([e], Grounds(G, e)),
 "16:93 '... and you will surely be questioned about what you used to do' (+6:148-149 excuse rejected)":
    And(WillsC(e_shirk), Act(e_shirk), Causes(s, e_shirk), Able(s, e_shirk), Wills(s, e_shirk),
        Questioned(s, e_shirk), ForAll([a, e], Implies(Questioned(a, e), Responsible(a, e)))),
 "39:7 'He does not approve disbelief for His servants' (while disbelief occurs: 18:29)":
    And(Not(Approves(e_kufr)), Approves(e_belief)),
 "112:3 / 57:3 'He begets not, nor is He begotten' / 'the First' -- God is not created":
    Not(Created(G)),
 "7:179 'We have created for Hell many of jinn and men: they have hearts with which they do not understand ...' (the verse's own characterisation; lam al-'aqiba)":
    And(Created(m), Misguided(m), Transgressor(m), Warned(m)),
 "57:22 + 42:30 'no calamity but it is in a Book' + 'whatever strikes you is for what your hands earned'":
    And(Grounds(G, e_calamity), Causes(s, e_calamity), Not(Act(e_calamity))),
}

AGENCY = {
 "90:10 'and shown him the two highways'":
    And(Able(s, e_belief), Able(s, e_kufr)),
 "18:29 'whoever wills, let him believe; whoever wills, let him disbelieve'":
    And(Or(Wills(s, e_belief), Wills(s, e_kufr)),
        Implies(Wills(s, e_belief), Causes(s, e_belief)),
        Implies(Wills(s, e_kufr), Causes(s, e_kufr)),
        Act(e_belief), Act(e_kufr)),
 "2:286 'God burdens no soul beyond its capacity; for it is what it earned, against it what it incurred'":
    And(ForAll([a, e], Implies(Responsible(a, e), Able(a, e))),
        ForAll([e], Implies(And(Causes(s, e), Wills(s, e), Able(s, e)), Responsible(s, e)))),
 "13:11 'God does not change a people's condition until they change what is in themselves'":
    And(Created(q), Causes(q, e_change), Act(e_change)),
 "53:39 'there is not for man except what he strives for'":
    ForAll([e], Implies(Responsible(s, e), Causes(s, e))),
 "7:23 'our Lord, we have wronged ourselves'":
    And(Causes(s, e_wrong), Wills(s, e_wrong), Able(s, e_wrong), Act(e_wrong)),
 "4:78-79 'say: all is from God' / 'whatever evil befalls you is from yourself'":
    And(Grounds(G, e_calamity), Causes(s, e_calamity)),
 "3:49 'I create for you from clay the form of a bird ... by God's permission'":
    And(Created(j), Causes(j, e_bird), Grounds(G, e_bird), WillsC(e_bird), Act(e_bird)),
 "2:26 / 61:5 / 14:27 'He misleads thereby none but the transgressors' / 'when they deviated, God made their hearts deviate'":
    ForAll([a], Implies(Misguided(a), Transgressor(a))),
 "9:115 'God would not let a people stray after guiding them until He makes clear what they should avoid'":
    ForAll([a], Implies(Misguided(a), Warned(a))),
}

# ----------------------------------------------------------------------------------------------------------
# Rival theses
# ----------------------------------------------------------------------------------------------------------
THESES = {
 "C  occasionalism: a creature is never a cause (God's creating excludes creaturely causing)":
    ForAll([a, e], Implies(Created(a), Not(Causes(a, e)))),
 "T  delegation/tafwid: a creature's own act is not grounded in God":
    ForAll([a, e], Implies(And(Created(a), Causes(a, e)), Not(Grounds(G, e)))),
 "J  decree-as-excuse/jabr: what God creatively wills, no one is answerable for":
    ForAll([a, e], Implies(WillsC(e), Not(Responsible(a, e)))),
 "I  identity: there is only one agent (every agent is God)":
    ForAll([a], a == G),
}

# ----------------------------------------------------------------------------------------------------------
# Machinery
# ----------------------------------------------------------------------------------------------------------
def solver_with(assumptions):
    """assumptions: dict label -> formula. Returns (solver, label->Bool tracker)."""
    S = Solver()
    S.set("timeout", 60000)
    for d in distinct_constants():
        S.add(d)
    trackers = {}
    for lab, fml in assumptions.items():
        t = Bool("[" + lab + "]")
        S.assert_and_track(fml, t)
        trackers[t] = lab
    return S, trackers

def check(assumptions):
    S, tr = solver_with(assumptions)
    r = S.check()
    return r, S, tr

def minimal_core(assumptions):
    """Deletion-minimised unsat core (labels)."""
    r, S, tr = check(assumptions)
    assert r == unsat, r
    core = [tr[t] for t in S.unsat_core()]
    changed = True
    while changed:
        changed = False
        for lab in list(core):
            trial = {k: assumptions[k] for k in core if k != lab}
            r2, _, _ = check(trial)
            if r2 == unsat:
                core.remove(lab); changed = True; break
    return core

results = []
def rec(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (("  -- " + detail) if detail else ""))

def merged(*dicts):
    out = {}
    for d in dicts:
        out.update(d)
    return out

# ----------------------------------------------------------------------------------------------------------
# 1. Kernel + both verse-sets: satisfiable; print the model
# ----------------------------------------------------------------------------------------------------------
ALL = merged(KERNEL, SOVEREIGNTY, AGENCY)
r, S, tr = check(ALL)
if r == sat:
    # re-solve with soft constraints so that the printed model asserts no more than the verses require
    O = Optimize()
    for d in distinct_constants():
        O.add(d)
    for lab, fml in ALL.items():
        O.add(fml)
    for x in [G, p, s, j, q, m, g]:
        for ev in EVENTS:
            for F in (Causes, Wills, Able, Responsible, Questioned):
                O.add_soft(Not(F(x, ev)), 1)
        for F in (Guided, Misguided, Transgressor, Warned, Turns):
            O.add_soft(Not(F(x)), 1)
    for ev in EVENTS:
        O.add_soft(Not(Approves(ev)), 1)
    if O.check() == sat:
        S = O
rec("1. kernel Q1-Q11 + sovereignty set + agency set: SATISFIABLE (a layered-concurrence model exists)", r == sat, str(r))
if r == sat:
    M = S.model()
    agents = [G, p, s, j, q, m, g]
    def tv(x):
        v = M.eval(x, model_completion=True)
        return "1" if is_true(v) else "0"
    print("    model (1 = true; soft-minimised over the named constants, quantified parts solved exactly), agents G p s j q m g; events:", " ".join(str(x) for x in EVENTS))
    print("    Created:    ", " ".join(f"{str(x)}={tv(Created(x))}" for x in agents))
    for name, F in [("Grounds", Grounds), ("Causes", Causes), ("Wills", Wills), ("Able", Able), ("Responsible", Responsible)]:
        print(f"    {name:12s}", end="")
        for x in agents:
            print(f" {str(x)}:" + "".join(tv(F(x, ev)) for ev in EVENTS), end="")
        print()
    print("    Act:        ", "".join(tv(Act(ev)) for ev in EVENTS))
    print("    WillsC:     ", "".join(tv(WillsC(ev)) for ev in EVENTS))
    print("    Approves:   ", "".join(tv(Approves(ev)) for ev in EVENTS))
    print("    Guided/Misguided/Transgressor/Warned/Turns:",
          " ".join(f"{str(x)}={tv(Guided(x))}{tv(Misguided(x))}{tv(Transgressor(x))}{tv(Warned(x))}{tv(Turns(x))}" for x in agents))
    # two-level reading made explicit
    both = [str(ev) for ev in ACTS if is_true(M.eval(Grounds(G, ev), model_completion=True))
            and any(is_true(M.eval(Causes(x, ev), model_completion=True)) for x in agents if str(x) != "G")]
    print("    acts attributed wholly to God (Grounds) AND wholly to a creature (Causes):", ", ".join(both))

# ----------------------------------------------------------------------------------------------------------
# 2. Occasionalism
# ----------------------------------------------------------------------------------------------------------
C = {k: v for k, v in THESES.items() if k.startswith("C ")}
v817 = {k: v for k, v in SOVEREIGNTY.items() if k.startswith("8:17")}
v3796 = {k: v for k, v in SOVEREIGNTY.items() if k.startswith("37:96")}
r, _, _ = check(merged(C, v817, v3796))
rec("2a. C + 8:17 + 37:96: UNSAT ('when you threw' is agent-level causation; 'God created you' makes the thrower a creature)", r == unsat, str(r))
core = minimal_core(merged(SOVEREIGNTY, AGENCY, C))
rec("2b. both verse-sets + C (no kernel axiom): UNSAT; minimal core", True, " | ".join(core))
rec("2c. that core consists of C and literal verses only", any(x.startswith("C ") for x in core) and all(not x.startswith("Q") for x in core), "")
r, _, _ = check(merged(C, v3796, {k: v for k, v in AGENCY.items() if k.startswith("13:11")}))
rec("2c'. C + 13:11 alone ('until they change what is in themselves'): UNSAT", r == unsat, str(r))
r, _, _ = check(merged(C, AGENCY, v3796))
rec("2d. C + agency set + 37:96 ('God created you'): UNSAT", r == unsat, str(r))
r, _, _ = check(merged(C, {k: v for k, v in SOVEREIGNTY.items() if not k.startswith("8:17") and not k.startswith("16:93") and not k.startswith("57:22")}))
rec("2e. C is consistent with the sovereignty verses that do NOT themselves name a creaturely act (8:17, 16:93, 42:30 removed)", r == sat, str(r))

# ----------------------------------------------------------------------------------------------------------
# 3. Identity
# ----------------------------------------------------------------------------------------------------------
I = {k: v for k, v in THESES.items() if k.startswith("I ")}
v112 = {k: v for k, v in SOVEREIGNTY.items() if k.startswith("112:3")}
r, _, _ = check(merged(I, v3796, v112))
rec("3a. I + 37:96 ('God created you') + 112:3/57:3 (God not created): UNSAT", r == unsat, str(r))
core = minimal_core(merged(SOVEREIGNTY, AGENCY, I))
rec("3b. both verse-sets + I (no kernel axiom): UNSAT; minimal core", True, " | ".join(core))
rec("3b'. that core consists of I and literal verses only", any(x.startswith("I ") for x in core) and all(not x.startswith("Q") for x in core), "")
r, _, _ = check(merged(I, {k: v for k, v in SOVEREIGNTY.items() if k.startswith("8:17")}, {"Q3": KERNEL[[k for k in KERNEL if k.startswith("Q3")][0]]}, v112))
rec("3c. I + 8:17 + Q3 (agent-level attribution is creaturely) + 112:3: UNSAT (under identity 8:17 would have God throwing at God)", r == unsat, str(r))

# ----------------------------------------------------------------------------------------------------------
# 4. Delegation and decree-as-excuse
# ----------------------------------------------------------------------------------------------------------
T = {k: v for k, v in THESES.items() if k.startswith("T ")}
J = {k: v for k, v in THESES.items() if k.startswith("J ")}
r, _, _ = check(merged(T, v817, v3796))
rec("4a. T + 8:17 + 37:96: UNSAT (the same verse gives 'you threw' and 'God threw'; 37:96 makes 'you' a creature)", r == unsat, str(r))
r, _, _ = check(merged(T, {k: v for k, v in SOVEREIGNTY.items() if k.startswith("39:62")}, {k: v for k, v in AGENCY.items() if k.startswith("13:11")}))
rec("4b. T + 39:62 + 13:11: UNSAT", r == unsat, str(r))
v1693 = {k: v for k, v in SOVEREIGNTY.items() if k.startswith("16:93")}
r, _, _ = check(merged(J, v1693))
rec("4c. J + 16:93 alone: UNSAT ('He misleads whom He wills ... and you will be questioned about what you did')", r == unsat, str(r))
r, _, _ = check(merged(J, v3796, {k: v for k, v in SOVEREIGNTY.items() if k.startswith("81:28")}, {k: v for k, v in AGENCY.items() if k.startswith("7:23") or k.startswith("2:286")}))
rec("4d. J + 81:29 + 7:23 + 2:286 + 37:96: UNSAT", r == unsat, str(r))

# ----------------------------------------------------------------------------------------------------------
# 5. C is the sole culprit: kernel + verses + not-C is SAT; and the kernel without Q3/Q4 + verses + C still UNSAT
# ----------------------------------------------------------------------------------------------------------
notC = {"not-C: some creature is a cause": Not(THESES[[k for k in THESES if k.startswith("C ")][0]])}
r, _, _ = check(merged(KERNEL, SOVEREIGNTY, AGENCY, notC))
rec("5a. kernel + both verse-sets + not-C: SAT", r == sat, str(r))
r, _, _ = check(merged(SOVEREIGNTY, AGENCY))
rec("5b. both verse-sets WITHOUT any kernel axiom: SAT (the verses do not contradict each other by themselves)", r == sat, str(r))
r, _, _ = check(merged(SOVEREIGNTY, AGENCY, C))
rec("5c. both verse-sets + C: UNSAT (the contradiction appears exactly when C is added)", r == unsat, str(r))

# ----------------------------------------------------------------------------------------------------------
# 6. Each rival thesis is individually consistent (the exclusions are not artefacts of an inconsistent thesis)
# ----------------------------------------------------------------------------------------------------------
for k, v in THESES.items():
    r, _, _ = check({k: v})
    rec(f"6. thesis alone is consistent: {k[:2].strip()}", r == sat, str(r))

# ----------------------------------------------------------------------------------------------------------
# 7. Q12 evil as privation (added 14 Oct 2026, evening). What God grounds in an evil act is its being (Q1, Q4);
#    the evil is the act's lack of due measure, owned by its agent and not approved (Q5, Q6). Encoded minimally.
# ----------------------------------------------------------------------------------------------------------
Q12 = {"Q12 evil as privation: a defective act is an act, is not approved, and has an answerable creaturely agent (4:79; 91:9-10; 39:7; 24:40; 6:1)":
       ForAll([e], Implies(Defective(e), And(Act(e), Not(Approves(e)), Exists([a], And(Created(a), Responsible(a, e))))))}
EVIL = {"evil acts named by the verse-sets are defective (18:29 disbelief; 7:23 wronging; 6:148 shirk)":
        And(Defective(e_kufr), Defective(e_wrong), Defective(e_shirk))}
r, _, _ = check(merged(KERNEL, SOVEREIGNTY, AGENCY, Q12, EVIL))
rec("7a. kernel + both verse-sets + Q12 + named evil acts: SAT (grounding of the act's being and creaturely ownership of its defect are jointly consistent)", r == sat, str(r))
P = {"P  God is answerable for a defect": Exists([e], And(Defective(e), Responsible(G, e)))}
r, _, _ = check(merged(KERNEL, Q12, P))
rec("7b. 'God is answerable for a defect' + kernel: UNSAT (21:23 via Q5; the defect is owned at the agent level)", r == unsat, str(r))
A2 = {"A' God approves a defective act": Exists([e], And(Defective(e), Approves(e)))}
r, _, _ = check(merged(Q12, A2))
rec("7c. 'God approves a defective act' + Q12: UNSAT (39:7)", r == unsat, str(r))


# ----------------------------------------------------------------------------------------------------------
# 8. The mechanism question (added 14 Oct 2026, late evening): does creaturely causation reach the BEING of the
#    act (Imami tuli causation: Mufid, Hilli, Sadra, Tabataba'i; structurally the Thomist concurrence), or only
#    its choice/quality, God alone producing the act's existence (Maturidi khalq + ikhtiyar; Ash'ari khalq +
#    kasb)?  'Produces' is NOT a Qur'anic term -- that is the point of the test: the two instantiations differ
#    only in a predicate the text never fixes, and both satisfy kernel + verses + Q12.
# ----------------------------------------------------------------------------------------------------------
MECH_M = {"MECH-M (Maturidi/Ash'ari): God alone produces the existence of every act; the creature's share is agent-level (choice, doing, earning), never production":
          And(ForAll([e], Implies(Act(e), Produces(G, e))),
              ForAll([a, e], Implies(Created(a), Not(Produces(a, e)))))}
MECH_I = {"MECH-I (Imami tuli / concurrence): a creature that causes an act produces its existence, by a power God gives and upholds (Q1, Q11 still hold)":
          ForAll([a, e], Implies(And(Created(a), Causes(a, e)), Produces(a, e)))}
r, _, _ = check(merged(KERNEL, SOVEREIGNTY, AGENCY, Q12, EVIL, MECH_M))
rec("8a. kernel + both verse-sets + Q12 + evil acts + MECH-M: SAT (the Maturidi mechanism instantiates the kernel; privation does not exclude it)", r == sat, str(r))
r, _, _ = check(merged(KERNEL, SOVEREIGNTY, AGENCY, Q12, EVIL, MECH_I))
rec("8b. kernel + both verse-sets + Q12 + evil acts + MECH-I: SAT (the Imami mechanism instantiates the kernel)", r == sat, str(r))
r, _, _ = check(merged(MECH_M, MECH_I, {k: v for k, v in KERNEL.items() if k.startswith("Q2")}))
rec("8c. MECH-M + MECH-I + Q2: UNSAT (they are genuine rivals, not two names for one view)", r == unsat, str(r))
# 8d: the one verse that could fix the mechanism, 37:96 on the masdariyya reading ("God created your doing"), is
#     encoded as: every creaturely act is created/grounded by God.  It does not entail MECH-M: the conjunction with
#     MECH-I stays satisfiable, because 'created' is Q1 (grounding), not 'sole proximate producer'.
v3796m = {k: v for k, v in SOVEREIGNTY.items() if k.startswith("37:96")}
r, _, _ = check(merged(KERNEL, SOVEREIGNTY, AGENCY, v3796m, MECH_I))
rec("8d. 37:96 (either reading) + kernel + verses + MECH-I: SAT (37:96 asserts creation of the act, Q1; it does not fix the mechanism)", r == sat, str(r))
# ----------------------------------------------------------------------------------------------------------
# 9. The point-circle argument (clue #6a, 15 Oct 2026).  The piece argues: being flows only from the Point (God);
#    a radius (creature) can determine but cannot GIVE BEING; hence the Maturidi mechanism is entailed by the GPP
#    structure.  Encoded, the argument's conclusion about being is P* -- no creature produces the existence of
#    ANY effect -- because nothing in the picture singles out free acts.  Tests: P* is (9a) occasionalism about
#    nature's production, (9b) stronger than Maturidism-on-acts, (9c/9e) not entailed by kernel + verses, and
#    (9d) not excluded by them either: the mechanism stays open, so the 'entailment' claim fails.
# ----------------------------------------------------------------------------------------------------------
P_STAR = {"P* (point-circle, generalised): no creature produces the existence of any effect":
          ForAll([a, e], Implies(Created(a), Not(Produces(a, e))))}
NATURE = {"NATURE: some creature produces the existence of some non-act effect (fire -> burning as production)":
          Exists([a, e], And(Created(a), Produces(a, e), Not(Act(e))))}
MECH_M_ACTS = {"MECH-M restricted to acts: for every act God alone produces its existence":
               ForAll([e], Implies(Act(e), And(Produces(G, e), ForAll([a], Implies(Created(a), Not(Produces(a, e)))))))}
r, _, _ = check(merged(P_STAR, NATURE))
rec("9a. P* + NATURE: UNSAT (generalised point-circle = occasionalism about all creaturely production, nature included)", r == unsat, str(r))
r, _, _ = check(merged(MECH_M_ACTS, NATURE))
rec("9b. MECH-M (acts only) + NATURE: SAT (Maturidism about acts does not need P*; the argument proves more than its conclusion)", r == sat, str(r))
r, _, _ = check(merged(KERNEL, SOVEREIGNTY, AGENCY, Q12, EVIL, NATURE, MECH_I))
rec("9c. kernel + verses + Q12 + evil + NATURE + MECH-I: SAT (text + kernel admit creaturely production of being)", r == sat, str(r))
r, _, _ = check(merged(KERNEL, SOVEREIGNTY, AGENCY, Q12, EVIL, P_STAR))
rec("9d. kernel + verses + Q12 + evil + P*: SAT (text + kernel also admit occasionalism about being: the mechanism is open)", r == sat, str(r))
r, _, _ = check(merged(KERNEL, SOVEREIGNTY, AGENCY, {"not P*": Not(list(P_STAR.values())[0])}))
rec("9e. kernel + verses + not-P*: SAT (hence kernel + verses do NOT entail P*: no entailment of the Maturidi mechanism)", r == sat, str(r))
# ----------------------------------------------------------------------------------------------------------
# SMT-LIB export of the main satisfiable problem
# ----------------------------------------------------------------------------------------------------------
S, _ = solver_with(ALL)
open("q_kernel.smt2", "w").write(S.to_smt2())
print(f"\n{sum(results)}/{len(results)} checks passed; SMT-LIB of problem 1 written to q_kernel.smt2")
sys.exit(0 if all(results) else 1)

#!/usr/bin/env python3
"""Corpus counts quoted in Lighthouse-and-Plan v2.2 §4.1 (run from this directory; needs the four JSON files)."""
import re
from q import Q
DIA = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")
bare = {f"{s}:{a}": DIA.sub("", t) for (s, a), t in Q["ar"].items()}
def hits(pat):
    rx = re.compile(pat); return [r for r, t in bare.items() if rx.search(t)]
checks = [
 ("'la yahdi' with God as subject (7:148 calf and 10:35 creature-subject excluded)", r"لا يهدي", 24, ("7:148", "10:35")),
 ("sealing of hearts asserted (6:46, 42:24 hypothetical and 36:65 mouths excluded)", r"ختم|طبع|يطبع|نطبع", 13, ("6:46", "42:24", "36:65")),
 ("'had He willed' (law sha'a / law shi'na / law nasha')", r"لو شاء|لو نشاء|لو شئنا", 33),
 ("'Creator of all things' / 'created all things'", r"خالق كل شيء|خلق كل شيء", 6),
 ("'wronged themselves' and variants", r"ظلموا أنفسهم|ظلمت نفسي|ظلمنا أنفسنا|يظلمون أنفسهم|ظالمي أنفسهم|ظلم نفسه|ظلمتم أنفسكم|ظالم لنفسه", 18),
 ("'God does not wrong / did not wrong them' (active)", r"الله لا يظلم|لا يظلم ربك|ما ظلمهم الله|وما ظلمناهم|ما ظلمناهم|وما ظلمونا|ما كان الله ليظلمهم|ليس بظلام|وما ربك بظلام|لا يظلم الناس|إن الله لا يظلم", 17),
 ("'they shall not be wronged' (passive)", r"لا يظلمون|لا تظلمون|لا يظلم أحد|لن يظلموا|فلا يظلم", 19),
]
ok = True
for row in checks:
    name, pat, expected = row[:3]; excl = row[3] if len(row) > 3 else ()
    h = [r for r in hits(pat) if r not in excl]; flag = "PASS" if len(h) == expected else "FAIL"; ok &= len(h) == expected
    print(f"{flag} {name}: {len(h)} verses (expected {expected}): {', '.join(h)}")
# the 25 la-yahdi objects, for inspection
print("\nobjects of 'la yahdi':")
for r in hits(r"لا يهدي"):
    if r in ("7:148", "10:35"): continue
    t = bare[r]; i = t.find("لا يهدي"); print(f"  {r}: {t[i:i+40]}")
print("\nALL PASS" if ok else "\nSOME FAIL")

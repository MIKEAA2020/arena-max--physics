import json, re, sys
EDS = {"ar":"quran-simple","sahih":"en.sahih","arberry":"en.arberry","pickthall":"en.pickthall"}
Q = {}
for k, ed in EDS.items():
    d = json.load(open(f"/home/user/v2.2/verify/quran/{ed}.json"))
    Q[k] = {}
    for s in d["data"]["surahs"]:
        for a in s["ayahs"]:
            Q[k][(s["number"], a["numberInSurah"])] = a["text"]
def v(ref, eds=("ar","sahih","arberry")):
    s, a = map(int, ref.split(":"))
    return {k: Q[k][(s,a)] for k in eds}
def show(ref, eds=("ar","sahih","arberry")):
    x = v(ref, eds)
    print(f"--- {ref}")
    for k in eds:
        print(f"  [{k}] {x[k]}")
def grep(pattern, ed="ar", flags=0):
    rx = re.compile(pattern, flags)
    return [(f"{s}:{a}", t) for (s,a), t in Q[ed].items() if rx.search(t)]
if __name__ == "__main__":
    for ref in sys.argv[1:]:
        show(ref)

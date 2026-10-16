import json, os, math
rows=[]
for fn in ["vumps_n3_chi96_ord.json","vumps_n3_chi96_mid.json","vumps_n3_chi96_dis.json"]:
    if not os.path.exists(fn): continue
    for k,v in json.load(open(fn)).items():
        rows.append((v['p'], int(k.split(':')[1][3:]), v))
rows.sort()
print(f"{'p':>7} {'chi':>4} {'f':>11} {'S':>7} {'m_par':>8} {'m_sp':>7} {'xi_sp':>6} {'xi_par':>6} {'xi_chi':>6} {'it':>4}")
for p,chi,v in rows:
    print(f"{p:7.4f} {chi:4d} {v['f']:11.8f} {v['S_ent']:7.4f} {v['m_parity']:+8.4f} {v['m_species']:7.4f} {v['xi_species']:6.1f} {v['xi_parity']:6.1f} {v['xi_chi']:6.1f} {v['iters']:4d}")
# effective exponents along each p
from collections import defaultdict
byp=defaultdict(list)
for p,chi,v in rows: byp[p].append((chi,v))
for p,lst in byp.items():
    lst.sort()
    for (c1,v1),(c2,v2) in zip(lst,lst[1:]):
        x1,x2=v1['xi_chi'],v2['xi_chi']
        kap=math.log(x2/x1)/math.log(c2/c1)
        s=f"p={p:.4f} chi {c1}->{c2}: kappa_eff(xi_chi)={kap:.2f}"
        if v1['m_species']>0.1 and v2['m_species']>0.1:
            bn=-math.log(v2['m_species']/v1['m_species'])/math.log(x2/x1)
            bp=-math.log(abs(v2['m_parity']/v1['m_parity']))/math.log(x2/x1)
            s+=f"  beta/nu_eff: species {bn:.3f}, parity {bp:.3f}"
        print(s)

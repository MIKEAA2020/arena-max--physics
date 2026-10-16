#!/usr/bin/env python3
"""print the VUMPS scan database as tables (one block per (chi, sweep))."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
db = json.load(open(os.path.join(HERE, f'vumps_n{n}.json')))
blocks = {}
for k, v in db.items():
    blocks.setdefault((v['chi'], v['sweep'], v.get('kick', 0)), []).append(v)
for (chi, sweep, kick), rows in sorted(blocks.items()):
    rows.sort(key=lambda r: r['p'])
    print(f"\n== n={n} chi={chi} sweep={sweep} kick={kick} ==")
    print("   p       f            S_ent   |m_par|  m_spec   xi_spec  xi_par   xi_chi   it   sec")
    for r in rows:
        print(f" {r['p']:.5f}  {r['f']:.8f}  {r['S_ent']:.4f}  {abs(r['m_parity']):.5f}  {r.get('m_species', float('nan')):.5f}  "
              f"{r.get('xi_species', float('nan')):7.2f}  {r['xi_parity']:7.2f}  {r['xi_chi']:7.2f}  {r['iters']:3d}  {r['seconds']:5.0f}")

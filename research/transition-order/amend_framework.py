#!/usr/bin/env python3
"""Apply the thirteenth v2.2 amendment only after a verified full fresh run.
Changes are restricted to front matter and A-1/provenance/consolidation records;
Parts I–II (and other existing substantive parts) are hash-protected.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
receipt=json.loads((HERE/'verification-receipt.json').read_text())
assert receipt['exit_code']==0 and receipt['passed']==receipt['total'] and receipt['suites']==10
count=receipt['total'];extension=receipt['transfer_checks'];assert count==197+extension
parts=ROOT/'v2.2/parts'
protected={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(parts.glob('0[1-8]-*.md'))}
hp=HERE/'governance-protection.json'
if hp.exists():assert protected==json.loads(hp.read_text()),'Protected framework sources changed'
else:hp.write_text(json.dumps(protected,indent=2)+'\n')

p=parts/'00-front.md';s=p.read_text()
if 'thirteenth time on 16 October 2026' not in s:
 s=s.replace('Status: working draft, audited.', 'And amended a thirteenth time on 16 October 2026 by the A-1 method-selection and repository follow-up: validated Hermitian half-row transfer-MPS selected, resumable higher-chi states and explicit convergence/budget statuses; fourth Clifford rank-29 transfer and finite-size ladder, d=3 and n=4 pilots; feasibility gates; credential-free ordinary GitHub publication; '+str(extension)+' new transfer-extension checks, '+str(count)+' total across ten suites — §22.14 continuation, §23.2 items 113–116. Status: working draft, audited.',1)
 lines=s.splitlines()
 for i,l in enumerate(lines):
  if l.startswith('| Verification suite |'):
   lines[i]=f'| Verification suite | 10 counted suites, {count} checks | 16 Oct 2026: fresh integrated driver passed {count}/{count}, exit 0; log `{receipt["log"]}`. Opfibration 20, R7 15, Q-kernel 34, primon 35, adelic 12, BST 17, clock 12, replica 17, v33 35, transfer extension {extension}. Long production data are stored, not rerun by the suite. Counts validate stated finite identities, implementation contracts and regressions, not all manuscript theorems, thermodynamic convergence or a transition-order verdict |'
  if l.startswith('| Consolidation |'):
   lines[i]='| Consolidation | 15 source lineages, 116 audit items | Grades changed in Part I or II by the clues, searches or A-1 follow-up: none. A-1 remains an adjudication; clue 13 remains unassigned |'
 s='\n'.join(lines)+'\n';p.write_text(s)

p=parts/'09-part-IV-b.md';s=p.read_text()
marker='**A-1 continuation, 16 October 2026 (thirteenth amendment; items 113–116).**'
if marker not in s:
 note=marker+''' The user requested a concrete next method, publication to `MIKEAA2020/arena-max--physics`, and dependency-ordered computation. The chosen primary method is deterministic transfer-MPS/DMRG on the exact six-label n=3 operator. Existing VUMPS is already in that family; it is not advertised as an independent alternative. A globally Hermitian half-row direct sum H+H† with paired environments reduces the MPO bond dimension from 36 to 12, with normalization f_b=−2 log eta_half. The naive nonsymmetric optimizer failed a complex-eigenvalue check and was rejected. Exact finite-ring identities, Ising scaling, period-Rayleigh cross-checks, checkpoint round trips and exact contraction reductions are verified. Half- and full-period finite-chi functionals are not identical, and local residuals are not global free-energy error certificates.

The actual campaign, including converged, unconverged, planned-stop and budget-stop states, is recorded in `research/transition-order/RESULTS.md`, `NUMERICAL-NOTES.md`, `optimizer-segments.json` and the raw JSON/logs. NPZ files contain real AL/AR/AC/C/environment tensors, not merely observations. Some disordered warm stages did not meet tolerance; their states may initialize a later solve but are not promoted to accepted phase observations. Higher-chi and same-p branch comparisons remain subject to their own convergence and feasibility gates. No new order theorem or measured latent heat is asserted.

The fourth Clifford local transfer is now derived on 30 closed labels with Gram rank 29 and a pseudoinverse quotient. Physical gate-generator checks, endpoints and Haar controls pass. All 52 requested Haar/Clifford L=4,6 cases in five diagonal colour sectors completed with small residuals; they resolve a finite-size difference, not a thermodynamic critical-point split. The L=8 Clifford matvec benchmark exceeded the adopted runtime gate and the larger ladder was deferred. Exact n=3,d=3 crossings and bidirectional small-chi pilots, and a low-chi n=4 Haar pilot with exact fully monitored control, were also executed. A dense n=4 full-period MPO and naive n=5 L=8 solve violate the resource policy; the higher-replica quotient/symmetry-reduction requirements are logged. Finite-cylinder interfaces/gaps, guided/resample-move SMC and full-Haar analytic hypotheses remain separate gated tasks. The previous SMC pilot's failure is not a no-go theorem for the entire method class. The regular-bimodule algebra is not conditional on n=3 being first order.

A fresh integrated regression passed '''+f'{count}/{count} across ten suites (including {extension} transfer-extension checks), exit 0'+'''. Original v32 and the historical v33 delivery report are preserved. Generated work and narrowly identified reproduction inputs were pushed with ordinary non-force commits, preserving the existing history/license; exact secret values and archive contents were scanned before staging. Credentials remain outside committed files, in excluded private Git metadata; that transient storage is not a durable vault. The initial nested corpus-copy inclusion is corrected in the current tree without rewriting history. Publication scope and the first verified commit are recorded in the repository. The draft still needs its original figure/SM, author review and proof-hypothesis audit before any submission certification. No Qur’anic reading, ontological commitment or statement of Parts I–II is altered; protected source hashes are stored.

'''
 s=s.replace('## §23 Consolidation record',note+'## §23 Consolidation record',1)
 rows=f'''| 113 | A-1 method selected: validated Hermitian half-row transfer-MPS/DMRG, real NPZ checkpoints and explicit same-p/convergence/stopping rules | `research/transition-order/PLAN.md`, `NUMERICAL-NOTES.md`; `verify/replica/replica_halfrow.py`, `order_campaign.py`; rejected raw nonsymmetric optimizer recorded |
| 114 | Remaining feasible computations executed in dependency order: higher-chi campaign; n=3,d=3 exact/coarse-MPS scans; fourth Clifford rank-29 transfer and 52-case finite ladder; n=4 Haar pilot; larger jobs benchmark/budget gated | `research/transition-order/RESULTS.md`, `FEASIBILITY.md`, raw JSON/logs and checkpoint states; finite-size differences and finite-chi stationary states do not certify order or a critical-point split |
| 115 | Fresh integrated verification after solver changes: {count}/{count} across ten suites; {extension} transfer-extension identities/checkpoint/physical-twirl checks | `verify/run_all.sh`, `{receipt['log']}`, `verify/transfer_checks.py`; counts are implementation/regression evidence, not a count of all paper theorems |
| 116 | Authorized non-force GitHub publication and reproducibility scope; preserve inputs/history/license, exclude credentials/caches and bulk downloads; protect Parts I–II and retain A-1 as distinct lineage | `PUBLICATION-SCOPE.md`, publication manifest, `research/transition-order/publication-receipt.json`, `governance-protection.json`; no clue 13 assignment; no submission-readiness claim |
'''
 i=s.index('| 112 |');j=s.index('\n',i)+1;s=s[:j]+rows+s[j:]
 s=s.replace('**Provenance.** ', '**Provenance.** v2.2 was amended a thirteenth time on 16 October 2026 by the A-1 method-selection, feasibility-ordered numerical continuation and authorized GitHub publication (§22.14 continuation; items 113–116; '+f'{count}/{count} fresh integrated checks across ten suites'+'). No part of the governing commitments or Parts I–II was changed. ',1)
 p.write_text(s)
assert protected=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(parts.glob('0[1-8]-*.md'))}
assembled='\n\n'.join(p.read_text().rstrip() for p in sorted(parts.glob('*.md')))+'\n'
(ROOT/'v2.2/Lighthouse-and-Plan-v2.2.md').write_text(assembled)
print('Thirteenth amendment assembled; protected sources unchanged; checks',count)

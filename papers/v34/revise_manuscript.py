#!/usr/bin/env python3
"""v34 author-review continuation from preserved v33, not a submission PDF.
Apply explicit Qur'anic/Lighthouse interpretive governance without identifying
creation with God or changing any theorem/proof block. Numerical updates are
labeled finite-chi observations, not a phase-order or publication certificate.
"""
from pathlib import Path
import hashlib,json,re,difflib,importlib.util,os
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
source=ROOT/'papers/v33/manuscript_revised_v33.tex';original=source.read_text();s=original

def replace_once(old,new):
    global s
    assert s.count(old)==1,(old[:90],s.count(old))
    s=s.replace(old,new,1)

def region(start,end,new):
    global s
    i=s.index(start);j=s.index(end,i);s=s[:i]+new.rstrip()+'\n\n'+s[j:]

def atomic(path,text):
    tmp=path.with_name(path.name+'.tmp');tmp.write_text(text);os.replace(tmp,path)

s='% manuscript_revised_v34.tex -- author-review continuation; 16 October 2026\n% Source: preserved v33; numerical and interpretation changes recorded separately.\n'+s
replace_once('Weak first order is favored, but a continuous transition is not excluded.',
             'Transition order remains unresolved. A later $\\chi=128$ shared-rate test yields two accepted small-order solutions at $p=.30486$; this does not establish continuity or coexistence.')
region('The persistence of sizable order near the edge',r'\emph{Retrospective:',r'''These earlier finite-$\chi$ observations motivated a weak-first-order preference, but did not establish a non-vanishing thermodynamic discontinuity. The later accepted $\chi=128$ two-preparation calculation at $p=.30486$ gives small order diagnostics for both histories, rather than a persistent large ordered/disordered separation at that point. It does not prove continuity, nor establish that this rate is on the thermodynamic disordered side: both finite-$\chi$ approximations could lie on one side of a shifted first-order crossing. Earlier unconverged $\chi=96$ states and the later run also differ in runtime and continuation details; the change is not a one-variable $\chi$ scaling experiment.

No nonzero latent heat, limiting exponent, or converged coexistence length is quoted. In particular, the earlier approximate slope proxy near $.11$ and $\xi_{\rm coex}\simeq40$--$60$ are not validated physical coexistence measurements. The reported $\xi_\chi$ is an MPS transfer length. The three-state-Potts assignment remains withdrawn, and a continuous non-Potts transition and weak first order both remain live alternatives.''')
replace_once('At $n=3$ these give $p_c^{(3)}=0.3049(2)$ and simultaneous loss of sign and standard order; weak first order is the preferred reading, with a continuous alternative still open.',
             'At $n=3$ the earlier scans provide a working locator $p_c^{(3)}=0.3049(2)$ and simultaneous loss of sign and standard order within their sampled resolution. Later $\\chi=128$ two-preparation observations and the rate scan are reported below; weak first order and continuity remain live alternatives, not established classes.')
# Discussion: preserve its analytic/complexity qualifications, update only the execution narrative.
replace_once('At $n=3$ the completed $\\chi=96$ points support a single transition near $.3049$; weak first order is favored but not established.',
             'At $n=3$ the earlier $\\chi\\le96$ data supply a working locator near $.3049$; the later accepted $\\chi=128$ shared-rate comparison does not settle order. Weak first order and continuity both remain live.')
region('The next computation is population-controlled tilted SMC,', 'The analytic program also has explicit gates.',r'''The independent-start $\chi=128$ coarse grid is complete. It evaluated both the half-row objective and full-period trial-state functionals, but did not retain an ordered and a disordered branch through a common rate interval. Initialization labels must not be relabeled as phases, and agreement from two starts is not a global-minimum certificate. The selected next protocol is unbiased branch-following continuation from the accepted large-order $.30470$ and small-order $.30486$ states, with the original $10^{-7}$ criterion. A branch-retention pilot is separately allocated from the completed grid, not another independent-start grid or an automatically authorized expansion; its actual execution status is recorded below when available. This is the same replica operator, not an independent disorder tilt. It is accompanied by exact small-ring identities, Ising and gapped controls, and same-period expectation contractions. Guided or resample-move SMC remains gated behind separate population, genealogy and mixing controls; the earlier pilot is not a no-go for every SMC method. The $n=3,d=3$ finite-size/coarse-MPS tests and the rank-29 two-qubit fourth-Clifford transfer operator with an $L=4,6$ ladder have also been implemented. Their finite-size observations do not establish a thermodynamic order or critical-point split. Larger ladders, a fine fourth-moment MPS scan and the $n=5$ quotient/orbit assembler remain open.''')
region(r'\section{Interpretive status of the record formalism}',r'\section{Conclusion}',(HERE/'sections/interpretation.tex').read_text())
s=s.replace('Weak first order is favored; continuity remains open.',
            'Weak first order and continuity remain open; the later $\\chi=128$ comparison and rate scan are finite-$\\chi$ observations, not a binary order test.')
s=s.replace('its transfer operator and possible critical-point split are future computations.',
            'its transfer operator and finite $L=4,6$ Haar/Clifford comparison have since been implemented, while any thermodynamic critical-point split remains open.')
# Add the completed/preregistered scan record without rewriting old numerical tables as new data.
path=ROOT/'v2.2/verify/replica/n3_chi128_scan.json'
db=json.loads(path.read_text()) if path.exists() else {'status':'not launched','cases':{}}
grid=[.3040,.3045,.3047,.30486,.3050,.3055]
lines=[r'\subsection{Later $\chi=128$ two-preparation rate scan}',r'\label{sec:chi128-scan}',
       r'The following is a later author-review continuation, separate from the historical full-period $\chi\le96$ table above. It uses the same two immutable warm sources independently at every target rate; it is not a bidirectional hysteresis continuation. The $p=.30486$ source-matched accepted pair is reused rather than reoptimized. Acceptance requires the original $10^{-7}$ residual, both canonical compatibility checks, and a checked full-period expectation contraction. Half-row stationarity does not imply independent full-period optimizer convergence. Real canonical/physical tensors are saved; omitted environments are recomputable caches.',
       '\nCampaign status at source generation: '+db.get('status','unknown').replace('_',r'\_')+'.',
       r'\begin{table*}[t]',r'\caption{Fixed-$\chi=128$ two-start rate scan. O/D label initialization histories, not phases. Only accepted rows carry observables; pending or failed rows are not zero. $m_{\rm color}$ is the invariant norm of the six one-point amplitudes about uniformity. $\xi_\chi$ is an MPS length, not a certified physical coexistence length.}',r'\label{tab:chi128-scan}',r'\begin{ruledtabular}',r'\begin{tabular}{cclrrrr}',r'$p$ & prep. & status & $f_{\rm period}$ & $m_{\rm sp}$ & $m_{\rm color}$ & $\xi_\chi$\\',r'\colrule']
accepted=0
for p in grid:
 c=db.get('cases',{}).get(f'{p:.7f}',{})
 for side,label in [('ordered','O'),('disordered','D')]:
  r=c.get(side,{})
  if r.get('converged'):
   accepted+=1
   color='---' if r.get('color_l2_order') is None else f"{r['color_l2_order']:.6f}"
   lines.append(f"{p:.5f} & {label} & accepted & {r['f_full_rayleigh']:.10f} & {r['m_species']:.6f} & {color} & {r['xi_chi']:.2f}"+r'\\')
  else:
   status='pending' if not r or r.get('status')=='running' else 'not accepted'
   lines.append(f'{p:.5f} & {label} & {status} & --- & --- & --- & ---'+r'\\')
lines += [r'\end{tabular}',r'\end{ruledtabular}',r'\end{table*}',
          r'At first-order coexistence, the competing bulk free-energy densities agree. A finite bulk gap at a sampled rate is not coexistence; a persistent observable/slope discontinuity or interface cost is a different diagnostic. Distinct finite-$\chi$ minima may persist away from a crossing, and a coarse grid may miss a narrow window. Neither branch separation at one $\chi$ nor its absence on these six points supplies a thermodynamic order verdict. A controlled branch crossing and $\chi$/size-systematic analysis remain necessary. For an ordinary continuous transition, the first derivative of the thermodynamic free energy is continuous while higher derivatives can be singular. A kink in the free energy normally denotes a first-derivative jump, instead a first-order signature for a generic tuning direction. Sharpening as $\chi$ grows also occurs when finite-entanglement rounding recedes at a continuous transition; neither sharpening nor merger alone is a binary test.']
pilot_path=ROOT/'v2.2/verify/replica/n3_branch128_pilot.json'
pilot=json.loads(pilot_path.read_text()) if pilot_path.exists() else {}
if pilot:
    lines.append(r'\paragraph{Separately allocated branch-retention pilot.} The zero-bias warm-continuation protocol uses the accepted large-order state at $.30470$ and small-order state at $.30486$, advancing via $.30475$ and $.30483$ respectively to a common $.30480$. Its current status is '+pilot.get('status','unknown').replace('_',r'\_')+'. These initialization histories are not certified thermodynamic phases; a merger or loss of order is not prevented by a constraint.')
    common=pilot.get('stages',{}).get('2',{})
    if common.get('ordered',{}).get('converged') and common.get('disordered',{}).get('converged'):
        pa,pb=common['ordered'],common['disordered']
        lines.append(r'At the common pilot rate $.30480$, invariant one-point order is '+f"{pa['color_l2_order']:.6f} / {pb['color_l2_order']:.6f}"+r'. Half-row trial-objective difference is '+f"{pa['f_half']-pb['f_half']:.5e}"+r', while the separately evaluated full-period trial difference is '+f"{pa['f_full_rayleigh']-pb['f_full_rayleigh']:.5e}"+r'. They are different finite-$\chi$ functionals, not a root bracket or a global error estimate. This allocation does not perform perturbation stability tests, a second common-rate crossing bracket, or $\chi\to\infty$ extrapolation; it does not certify transition order.')
if accepted==12:
    left=[db['cases'][f'{p:.7f}'][side]['color_l2_order'] for p in grid if p<=.3047 for side in ['ordered','disordered']]
    right=[db['cases'][f'{p:.7f}'][side]['color_l2_order'] for p in grid if p>=.30486 for side in ['ordered','disordered']]
    if min(left)>.1 and max(right)<.01:
        lines.append(r'The completed six-rate experiment gives large order diagnostics for both histories at $.3040,.3045,.3047$ and small diagnostics for both at $.30486,.3050,.3055$. No persistent ordered/disordered branch separation was demonstrated at these sampled rates after symmetry alignment. The large-to-small change is sampled between $.3047$ and $.30486$ at this fixed $\chi$; this is not a thermodynamic critical-point confidence interval or a measured jump. A narrower stationary-branch bracket and $\chi$/size-systematic control remain necessary, so first order and continuity both remain live.')
marker=r'\subsection{Four- and five-replica finite-size diagnostics}'
assert s.count(marker)==1;s=s.replace(marker,'\n\n'.join(lines)+'\n\n'+marker,1)
# Structural source checks: all numbered statements and all proof blocks remain verbatim.
pat=re.compile(r'\\begin\{(theorem|proposition|lemma|corollary|definition|assumption|remark|proof|structuralproposition)\}.*?\\end\{\1\}',re.S)
a=[m.group(0) for m in pat.finditer(original)];b=[m.group(0) for m in pat.finditer(s)]
assert len(a)>10 and a==b,'A theorem/proof block changed'
labels=re.findall(r'\\label\{([^}]+)\}',s);assert len(labels)==len(set(labels))
refs=re.findall(r'\\(?:eqref|ref|autoref)\{([^}]+)\}',s);assert set(refs)<=set(labels)
keys=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',s))
cites={k.strip() for v in re.findall(r'\\cite\{([^}]+)\}',s) for k in v.split(',')};assert cites<=keys
out=HERE/'manuscript_revised_v34.tex';atomic(out,s)
atomic(HERE/'v33-to-v34.diff',''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='manuscript_revised_v33.tex',tofile='manuscript_revised_v34.tex')))
provenance=dict(source_v33_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),output_v34_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),unchanged_statement_and_proof_blocks=len(a),labels=len(labels),references_resolve=True,citations_resolve=True,scan_status=db.get('status'),scan_accepted_preparations=accepted,branch_pilot_status=pilot.get('status','not launched'),phase_order='unresolved',status='author-review; not submission certified',interpretation='Quranic/Lighthouse: real dependent creation distinct from uncreated Creator; not a physics theorem')
atomic(HERE/'source-provenance.json',json.dumps(provenance,indent=2)+'\n')
report=f'''# v34 author-review continuation

16 October 2026. Source: preserved v33, SHA256 `{provenance['source_v33_sha256']}`.

## Governing interpretive correction

The governing reading is **real creation, dependent on and distinct from the uncreated Creator**. Dependence is not identity; creation is neither an unreal appearance of God nor a second independent absolute. The interpretation explicitly rejects the “only the Absolute exists” premise. God is not a physical clock, field, quantum state, algebra or instrument.

This follows the independently argued Qur’anic/Lighthouse framework, including its text/context/tafsir discipline. A user override is not itself interpretive authority. The interpretation is not inferred from quantum spectra, a transition order, or the Born-record formalism. The physics retains its separate mathematical and empirical warrant.

## Numerical and scientific scope

The accepted χ128 p=.30486 pair has small order diagnostics; it does not establish continuity or coexistence. The six-rate scan status is **{db.get('status')}**, with **{accepted}/12** accepted preparation records at generation time. Its table marks pending/failed entries explicitly. A finite bulk free-energy gap is not coexistence. The earlier latent-heat proxy and claimed physical coexistence length remain unvalidated/withdrawn.

The source explicitly distinguishes measured half-row/full-period trial-state functionals from unresolved phase branches. The energies were recorded; initialization labels are not phase identities, and agreement from two starts does not certify a global minimum. It corrects the claim that a continuous transition generically has a kink in f, and warns that χ-dependent sharpening is not a binary order test. Unbiased branch continuation is the selected next protocol, with its separately allocated bounded pilot tracked independently from the completed grid.

The completed finite fourth-Clifford/d=3 pilots remain finite observations. Old v33 tables remain historical observations, not relabeled χ128 data.

## Preservation and verification

- Original v33 is not edited.
- **{len(a)} theorem/statement/proof blocks are unchanged verbatim** by a source-contract comparison.
- Labels are unique; references and citation keys resolve.
- The source/provenance JSON and unified diff record this continuation.
- This source-contract audit is not a proof of every retained theorem or a new addition to the 246-check suite.

## Submission status

Still an **author-review draft**: original `fig_final_fss_v16.pdf`, original SM/numerical deposits, author approval, and specialist analytic-hypothesis audit remain required. No submission PDF or visual layout certificate was produced. New interpretation does not supply missing scientific hypotheses or assets.
'''
atomic(HERE/'REVISION-REPORT.md',report)
spec=importlib.util.spec_from_file_location('md2docx',ROOT/'v2.2/md2docx.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.convert(str(HERE/'REVISION-REPORT.md'),str(HERE/'v34-revision-report.docx'))
print(json.dumps(provenance,indent=2))

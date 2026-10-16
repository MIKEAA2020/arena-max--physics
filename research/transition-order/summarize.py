#!/usr/bin/env python3
"""Generate a status-honest report/tables from saved observations, not process exit.
Does not fit critical exponents, infer latent heat or promote checkpoint-only states.
"""
from pathlib import Path
import json,csv,math,re,html
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
R=ROOT/'v2.2/verify/replica'
def load(p,default=None):
    p=Path(p);return json.loads(p.read_text()) if p.exists() else ({} if default is None else default)
def fmt(x,d=6):
    try:
        if not math.isfinite(float(x)):return 'undefined'
        return f'{float(x):.{d}f}'
    except (ValueError,TypeError):return '—'
def status(r):
    if r.get('converged') is True:return 'optimizer converged'
    if r.get('status'):return r['status']
    return 'unconverged' if r.get('converged') is False else 'recorded (see tolerance)'
def writecsv(path,rows,fields):
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)

controls=load(R/'half_controls.json',[])
bounded={b:load(R/f'n3_chi128_bounded_{b}.json') for b in ['ordered','disordered']}
branches={b:load(R/f'order_{b}.json') for b in ['ordered','disordered']}
prod=[]
for b,db in branches.items():
    for key,r in db.items():
        view=dict(r);last=r.get('last_state_metadata',{})
        for k in ['eps','iters','seconds']:
            if k in last:view.setdefault(k,last[k])
        if 'eta' in last:view.setdefault('f_half',-2*math.log(last['eta']))
        prod.append(dict(view,preparation=b,key=key,status_label=status(r)))
prod.sort(key=lambda r:(r['preparation'],r.get('p',0),r.get('chi',0)))
accepted=[r for r in prod if r.get('converged') is True]
writecsv(HERE/'n3-production.csv',prod,['preparation','p','chi','status_label','tol','eps','iters','seconds','f','f_half','f_full_rayleigh','m_species','m_parity','xi_chi','S_ent','checkpoint'])
matched=[]
for a in branches['ordered'].values():
    for b in branches['disordered'].values():
        if a.get('converged') and b.get('converged') and a.get('p')==b.get('p') and a.get('chi')==b.get('chi'):
            matched.append(dict(p=a['p'],chi=a['chi'],f_ordered_start=a['f'],f_disordered_start=b['f'],delta_f=a['f']-b['f'],m_species_O=a['m_species'],m_species_D=b['m_species'],m_parity_O=abs(a['m_parity']),m_parity_D=abs(b['m_parity']),xi_O=a['xi_chi'],xi_D=b['xi_chi'],f_period_O=a.get('f_full_rayleigh'),f_period_D=b.get('f_full_rayleigh'),delta_f_period=(a['f_full_rayleigh']-b['f_full_rayleigh']) if 'f_full_rayleigh' in a and 'f_full_rayleigh' in b else None))
writecsv(HERE/'n3-matched.csv',matched,['p','chi','f_ordered_start','f_disordered_start','delta_f','m_species_O','m_species_D','m_parity_O','m_parity_D','xi_O','xi_D','f_period_O','f_period_D','delta_f_period'])
lad=load(R/'clifford4_ladder.json');cross=[]
for ens in ['haar','clifford']:
    for s in ['std','sgn','two','stdsgn']:
        rows=[]
        for p in [.32,.34,.355,.36,.37,.38,.39,.40,.42,.44,.46,.48,.50]:
            a=lad.get(f'{ens}:L4:p{p:.5f}');b=lad.get(f'{ens}:L6:p{p:.5f}')
            if a and b:rows.append((p,a['X_'+s]-b['X_'+s]))
        for (p,a),(q,b) in zip(rows,rows[1:]):
            if a*b<0:cross.append(dict(ensemble=ens,sector=s,L1=4,L2=6,p_linear=p+(q-p)*a/(a-b),bracket_low=p,bracket_high=q))
writecsv(HERE/'fourth-moment-crossings.csv',cross,['ensemble','sector','L1','L2','p_linear','bracket_low','bracket_high'])
ex=load(R/'n3_d3_exact.json');d3=load(R/'n3_d3_mps_pilot.json');n4=load(R/'n4_haar_half_pilot.json');l8=load(R/'clifford4_L8_budgeted.json');trial=load(R/'n3_trial_period_rayleigh.json')
vr=load(HERE/'verification-receipt.json');pub=load(HERE/'publication-receipt.json');publication_hold=load(HERE/'chi128-publication-status.json');comparison=load(R/'n3_chi128_stationary_comparison.json')
maxchi=max([r['chi'] for r in accepted],default=96)
ledger=[
 dict(id='T0',status='complete',outcome='immutable inputs and credential-free method-request log preserved'),
 dict(id='T1',status='complete',outcome='exact half-row, direct-sum, paired-environment, checkpoint and contraction checks passed'),
 dict(id='T2',status='complete-with-stated-control-exceptions',outcome='Ising ladder; n=3 gapped functional controls; lower-chi requested-tolerance misses retained'),
 dict(id='T3',status='partial-order-unresolved',outcome=f'accepted new half-row observations through chi={maxchi}; {len(matched)} accepted same-rate/same-chi pair(s); inspect nonconverged and partial states'),
 dict(id='T4',status='finite-and-coarse-pilots-complete-fine-order-open',outcome=f'{len(ex.get("cases",{}))} exact cases, {len(ex.get("crossings",[]))} finite crossings, {len(d3)} MPS pilot cases'),
 dict(id='T5',status='complete',outcome='fourth Clifford physical twirl on rank-29 quotient'),
 dict(id='T6',status='L4-L6-complete-L8-runtime-deferred',outcome=f'{len(lad)} cases in five diagonal colour sectors; L8 benchmark {fmt(l8.get("benchmark",{}).get("one_projected_matvec_seconds"),3)} s/matvec'),
 dict(id='T7',status='endpoint-and-low-chi-pilot-complete',outcome=f'{len(n4)} n=4 Haar cases; no converged chi-to-infinity phase result'),
 dict(id='T8',status='deferred-not-implemented',outcome='finite-cylinder gaps/interfaces need an exact boundary/operator contract and convergence controls'),
 dict(id='T9',status='gated-deferred',outcome='guided/resample-move SMC needs separate exact/mixing/population validation; pilot failure is not a no-go'),
 dict(id='T10',status='audit-partial-proof-open',outcome='conditional implication and counterexamples checked; full-Haar analytic hypotheses, contour/real-replica constructions open'),
 dict(id='T11',status='deferred-feasibility-gated',outcome='n=5 rank-119 quotient/orbit-block assembler required; naive L8 Krylov memory exceeds sandbox')]
latest_grid=load(R/'n3_chi128_scan.json')
if latest_grid:
    paired=sum(c.get('ordered',{}).get('converged') is True and c.get('disordered',{}).get('converged') is True for c in latest_grid.get('cases',{}).values())
    ledger[3]['status']='coarse-chi128-grid-complete-order-unresolved' if paired==6 else 'coarse-chi128-grid-incomplete-order-unresolved'
    ledger[3]['outcome']=f'earlier campaign through chi={maxchi}; separate fixed-source chi128 grid {paired}/6 paired rates accepted (reference included), not a coexistence or transition-order certificate'
(HERE/'task-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')

text=['# Transition-order continuation — executed work and status','',
'16 October 2026 · A-1 continuation · Reproducible observations and explicit stopping rules, not a phase-order certificate.','',
'## 1. Decision and outcome','',
'**Chosen primary method:** deterministic transfer-MPS/DMRG on the exact n=3 replica operator. The implemented upgrade is a validated Hermitian half-row MPO, real resumable NPZ states, higher chi and matched-rate independently prepared states. Existing VUMPS is already in this method family. Finite-cylinder gaps/interfaces are the next independent discriminant if this remains ambiguous; unvalidated large SMC is not the next production run.','',
'**Scientific conclusion:** the previous locator **p_c approximately .3049(2)** remains the working numerical estimate; **transition order remains unresolved**. The earlier weak-first-order preference is not a verdict and is not strengthened by the chi=96 optimizer failures. No latent heat, interface tension or asymptotic exponent is certified by this campaign. The standard n! algebra does not depend on n=3 being first order.','',
'See [PLAN.md](PLAN.md), [NUMERICAL-NOTES.md](NUMERICAL-NOTES.md), [FEASIBILITY.md](FEASIBILITY.md) and the machine-readable [task ledger](task-ledger.json).','',
'## 2. Primary n=3,d=2 computation','',
'All rows below retain their own requested tolerance/status. Local optimizer residuals are not global free-energy error bounds. Preparations named ordered/disordered identify the continuation history, not a guaranteed physical phase. For stopped rows, any listed f_half is an intermediate center-eigenvalue estimate, not an accepted stationary Ritz/free energy.','',
('**Earlier resource-limited stages:** the ordered chi=128 anchor exhausted its resumed optimizer budget without convergence; the disordered chi=128 anchor was triaged before convergence. Both partial states are retained. A separately authorized 90-minute common-rate chi=128 stage is recorded below. Chi=192 was not launched and is not automatic.' if any(bounded.values()) else '**Higher-chi ceiling:** the ordered chi=128 stage exhausted its resumed optimizer budget without convergence; the disordered chi=128 expansion was triaged before convergence. Both partial states are retained. Chi=192 was not launched. Compute was redirected to the more feasible matched-rate chi=96 test without relaxing its tolerance.'),'',
'| Preparation | p | chi | f_half | m_sp / abs(m_par) | xi_chi | residual | Status |',
'|---|---:|---:|---:|---:|---:|---:|---|']
if all(r.get('converged') is True for r in bounded.values()):
    a,b=bounded['ordered'],bounded['disordered']
    finding=f"**New accepted chi=128 comparison:** both preparations passed the prospective gates at p={a['p']:.5f}. m_species is {a['m_species']:.6f} / {b['m_species']:.6f}, with xi_chi {a['xi_chi']:.2f} / {b['xi_chi']:.2f}. "
    if max(a['m_species'],b['m_species'],abs(a['m_parity']),abs(b['m_parity']))<.01:
        finding+='Both solutions have small order diagnostics; a persistent large ordered/disordered branch separation was **not** demonstrated at this probed point. '
    finding+='This does not establish continuity: the point could lie on the same side of a first-order transition. The earlier common-rate chi=96 states were unconverged and had a shorter budget, so this comparison does not isolate a pure chi effect.'
    i=text.index('## 2. Primary n=3,d=2 computation')
    text[i:i]=[finding,'']
for r in prod:
    text.append(f"| {r['preparation']} | {fmt(r.get('p'),7)} | {r.get('chi','—')} | {fmt(r.get('f',r.get('f_half')),10)} | {fmt(r.get('m_species'),5)} / {fmt(abs(r['m_parity']) if 'm_parity' in r else None,5)} | {fmt(r.get('xi_chi'),2)} | {float(r['eps']):.2e} | {status(r)} |" if 'eps' in r else f"| {r['preparation']} | {fmt(r.get('p'),7)} | {r.get('chi','—')} | — | — | — | see saved metadata | {status(r)} |")
text+=['','[Full production CSV](n3-production.csv). A row pointing to a rolling `latest.npz` describes that path at the time of recording; it may since have been superseded. Immutable high-chi anchor copies are separately named. Always read checkpoint metadata rather than inferring its state from an old JSON pointer. Partial states contain actual tensors but are not accepted stationary observations.','',
'### Matched-rate comparisons','']
if matched:
    text+=['| p | chi | f_half,O − f_half,D | m_species O / D | abs(m_parity) O / D | xi O / D |','|---|---:|---:|---:|---:|---:|']
    for r in matched:text.append(f"| {fmt(r['p'],7)} | {r['chi']} | {r['delta_f']:.3e} | {r['m_species_O']:.5f} / {r['m_species_D']:.5f} | {r['m_parity_O']:.5f} / {r['m_parity_D']:.5f} | {r['xi_O']:.2f} / {r['xi_D']:.2f} |")
    text+=['','These are finite-chi variational comparisons. Agreement/merger at a single p does not establish continuity; different stationary states at one chi do not establish first order. Rate tuning, free-energy systematics, slope/jump convergence and correlation-length behavior remain necessary.']
else:text+=['No pair has yet passed both optimizer tolerances at exactly the same p and chi. A partial checkpoint is not substituted into that comparison.']
if any(bounded.values()):
    text+=['','### Authorized 90-minute chi=128 stage','',
    'The user authorized one bounded two-preparation chi=128 stage at p=.30486, not another chi=96 campaign. The original 1e-7 tolerance and optimizer are unchanged. Left/right compatibility, canonical identities and a same-period contraction are additionally validated. See [prospective protocol](chi128-90m-protocol.json) and [interpretation contract](CHI128-STAGE.md). No chi=192 is automatically scheduled.','',
    '| Preparation | Status | Optimizer residual | Left / right compatibility | Iterations | Stage seconds | f_period_Rayleigh |','|---|---|---:|---:|---:|---:|---:|']
    for side,r in bounded.items():
        if not r:continue
        eps=r.get('eps',r.get('last_state_metadata',{}).get('eps'))
        eps_text=f'{eps:.2e}' if eps is not None else 'pending'
        left=r.get('gauge_left_residual');right=r.get('gauge_right_residual')
        compatibility=f'{left:.2e} / {right:.2e}' if left is not None and right is not None else 'not evaluated'
        text.append(f"| {side} | {r.get('status','pending')} | {eps_text} | {compatibility} | {r.get('iters','pending')} | {fmt(r.get('total_stage_seconds'),1)} | {fmt(r.get('f_full_rayleigh'),10)} |")
    text+=['','Neither agreement nor disagreement at one rate and chi is a binary order test. The earlier chi=96 optimizer failures do not establish two stationary phases and are not assigned additional phase-order evidence. A controlled stationary-branch rate bracket and chi/size-systematic checks remain necessary. Non-converged partial states are not substituted for an accepted pair.']
if comparison:
    text+=['',f"Supplementary symmetry/gauge-aware comparison: **{comparison.get('status')}**, {len(comparison.get('orientations',[]))} orientations. Largest evaluated normalized mixed-transfer fidelity per site: **{fmt(comparison.get('largest_evaluated_fidelity_per_site'),10)}**. This is a per-site similarity diagnostic, not proof of exact state identity or phase order. Raw complex eigenvalues and contraction residuals are retained in `n3_chi128_stationary_comparison.json`."]
ritz=[r for r in accepted if 'f_full_rayleigh' in r]
if ritz:
    text+=['','### Independent period-Rayleigh functional checks','','| Preparation | p | chi | f_half | f_period_Rayleigh | difference |','|---|---:|---:|---:|---:|---:|']
    for r in ritz:text.append(f"| {r['preparation']} | {fmt(r['p'],7)} | {r['chi']} | {r['f']:.10f} | {r['f_full_rayleigh']:.10f} | {r['f']-r['f_full_rayleigh']:.3e} |")
if trial:
    text+=['','### Frozen-trial period-Rayleigh comparison — not coexistence','',
    'This evaluates the **same full-period operator at the same p** on two saved normalized MPS trial states, even when their source optimizers failed to converge. The right fixed point and spin diagnostics are recomputed for the actual frozen AL tensors. Small contraction residuals control only the MPS expectation contraction; they do **not** bound the distance to the true transfer eigenstate, optimizer error or finite-chi bias. No crossing of these trial curves is promoted to p_c or latent heat.','',
    '| p | Preparation | f_period_Rayleigh | Contraction residual |','|---|---|---:|---:|']
    for r in trial.get('evaluations',[]):text.append(f"| {r['p']:.7f} | {r['preparation']} | {r['f_period_Rayleigh']:.10f} | {r['contraction_relative_residual']:.2e} |")
    text+=['','| Frozen preparation | Source p | Source residual | m_species | abs(m_parity) | xi_chi |','|---|---:|---:|---:|---:|---:|']
    for side,r in trial.get('states',{}).items():
        meta=r['source_metadata']
        text.append(f"| {side} | {meta['p']:.7f} | {meta.get('eps',float('nan')):.2e} | {r['m_species']:.5f} | {abs(r['m_parity']):.5f} | {r['xi_chi']:.2f} |")
    text+=['',f"Frozen-state evaluation status: {trial.get('status','partial')}. The distinct trial order diagnostics are **not** a converged jump. This is a valid trial-state comparison, **not** the missing pair of stationary phases."]
text+=['','### Normalization, controls and exact optimization changes','',
'The raw nonsymmetric half-row optimizer produced a complex effective eigenvalue and was rejected. Production uses the global direct sum H+H† with paired/transposed environments. Both summands remain in the effective-center problem, even when the redundant environment eigenproblem is reduced to one component. Exact block/map identities and independent finite-ring tests guard these optimizations.','',
'The n=3 MPO bond is 12 rather than full-period 36; **f_half = −2 log eta_half**. Half- and full-period finite-chi functionals differ, so their agreement is checked rather than assumed.','',
'The Ising p=.233810 chi=8,16,32,64 ladder converged at requested 1e-8; xi_chi = **39.2048, 165.8538, 681.2273, 2546.748**. For n=3,p=.300 the half/full discrepancy falls from 2.09e-7 at chi=24 to 5.79e-9 at chi=48; at p=.310 it falls from 3.97e-6 to 4.12e-7. The final p=.310 residual 1.17e-8 missed its nominal 1e-8 but passed the separately stated 3e-8 calibration ceiling. Other capped lower-chi stages are not retrospectively called converged.','',
'Warm-stage failures, planned checkpoint resumes and per-segment times are in `optimizer-segments.json`. A later solve may use an unconverged state solely as an initialization; that does not validate the earlier observation. Production stopping/tolerance rules are recorded prospectively, not relaxed after seeing the desired phase.','',
'## 3. Fourth Clifford versus Haar','',
'An exact local fourth-Clifford transfer operator is now implemented on **30 closed generators with Gram rank 29**, using a Moore–Penrose quotient. Physical gate-generator commutators, Haar weights, projectors and p=1 controls pass. Independent two-qubit support-rank counts are [48,288,384], giving moments **2/5, 1/5, 1/8** at replicas 2,3,4. Haar fourth moment is **4/35**.','',
f'**{len(lad)} finite cases completed**: 13 rates × L=4,6 × two ensembles, five diagonal S4-left/right sectors per case. These are not a claim to exhaust every off-diagonal representation sector or the entire spectrum.','',
'| Diagonal sector | Haar L4/L6 crossing | Clifford L4/L6 crossing |','|---|---:|---:|']
for s in ['std','sgn','two','stdsgn']:
    vals={r['ensemble']:r['p_linear'] for r in cross if r['sector']==s}
    text.append(f"| {s} | {fmt(vals.get('haar'),4)} | {fmt(vals.get('clifford'),4)} |")
res=max([e for r in lad.values() for k,x in r.items() if k.endswith('_residuals') for e in x],default=float('nan'))
text+=['',f'These are **linear-grid finite-size crossing estimates**, not finely root-solved values and not thermodynamic critical points. The maximum absolute stored eigenpair residual is {res:.2e}. The finite-size Haar/Clifford difference is resolved; a thermodynamic critical-point split is not established. See [crossing CSV](fourth-moment-crossings.csv) and [finite-size gap plot](fourth-moment-gaps.svg).','',
f'L=8 benchmark: **{fmt(l8.get("benchmark",{}).get("one_projected_matvec_seconds"),3)} seconds per projected matvec**, versus an adopted 1-second gate; status **{l8.get("status","not recorded")}**. A larger ladder was not launched merely because the L=4,6 cases were cheap.','',
'## 4. n=3,d=3 and n=4 Haar pilots','',
'### d=3 exact finite-size crossings','','| Sector | Sizes | p_star |','|---|---:|---:|']
for r in ex.get('crossings',[]):text.append(f"| {r['sector']} | {r['L']},{r['M']} | {r['p_star']:.7f} |")
text+=['',f'The d=3 exact cache contains {len(ex.get("cases",{}))} cases, with root tolerance 3e-6. These are finite-size locators, not p_c-infinity error bars. The bidirectional MPS pilot has {len(d3)} recorded cases, including chi=12 edge controls and chi=24 continuation.','',
'| d=3 preparation | p | chi | f_half | m_species | abs(m_parity) | Status |','|---|---:|---:|---:|---:|---:|---|']
for key,r in d3.items():
    text.append(f"| {key.split(':')[0]} | {fmt(r.get('p'),7)} | {r.get('chi','—')} | {fmt(r.get('f'),9)} | {fmt(r.get('m_species'),5)} | {fmt(abs(r['m_parity']) if 'm_parity' in r else None,5)} | {status(r)} |")
text+=['','The d=3 pilot supplies a controlled implementation/continuation check and coarse location information. It is not a fine phase-order scan or a universality assignment.','',
'### Fourth Haar thermodynamic-MPS pilot','']
for key,r in n4.items():
    if key.startswith('p1'):
        text.append(f"- Fully monitored endpoint: chi={r.get('chi')}, f_half={fmt(r.get('f'),10)}, exact −2 log(4/35)={fmt(r.get('f_exact'),10)}, error={float(r.get('endpoint_error',0)):.2e}; {status(r)}.")
    else:text.append(f"- p={r.get('p',key)}, chi={r.get('chi','—')}: f_half={fmt(r.get('f'),10)}, abs(m_parity)={fmt(abs(r['m_parity']) if 'm_parity' in r else None,5)}, xi_chi={fmt(r.get('xi_chi'),3)}; {status(r)}.")
text+=['','The exact endpoint precedes the pilot. A low-chi optimizer solution is not a chi-converged thermodynamic phase determination. The approximately 1.5 GB full-period n=4 local tensor was not materialized.','',
'## 5. Dependency and stopping ledger','','| Task | Status | Outcome |','|---|---|---|']
for r in ledger:text.append(f"| {r['id']} | {r['status']} | {r['outcome']} |")
text+=['','The chosen method has been implemented and feasible computations executed, but unfinished mathematical and large-size jobs are not represented as complete. Missing boundary-contract, mixing or analytic-hypothesis prerequisites remain explicit. See [proof audit](PROOF-AUDIT.md) and [resource feasibility](FEASIBILITY.md).','',
'## 6. Verification, artifacts and GitHub','']
if vr:
    text.append(f"Fresh integrated regression: **{vr.get('passed')}/{vr.get('total')} across {vr.get('suites')} suites**, exit {vr.get('exit_code')}; transfer extension {vr.get('transfer_checks')}. Log: `{vr.get('log')}`. The current paper-only runner performs 17+35+49=101 checks. These totals validate specified finite identities and implementation contracts, not every paper theorem or a phase-order verdict.")
else:text.append('The earlier integrated run passed 241/241 with a 44-check transfer extension; after exact map optimizations the expanded transfer extension passed 49/49 freshly. The final integrated regression receipt is not yet recorded; it is not assumed from process startup.')
publication_text=(f"The previous verified remote commit is `{publication_hold.get('last_verified_remote_commit')}` on `MIKEAA2020/arena-max--physics`. The new chi=128 continuation is **not claimed pushed**: the earlier excluded credential metadata was not retained in the restored workspace. A credential-free Git bundle provides an owner-push handoff if authenticated publication remains unavailable. Existing history/license are preserved; credentials are excluded and nested archives are scanned before staging. This is a publication-status receipt, not a numerical qualification. See `PUBLICATION-SCOPE.md` at the project root."
    if publication_hold and publication_hold.get('new_stage_pushed') is False else
    f"The first ordinary GitHub push was verified at commit `{pub.get('first_published_commit','not recorded')}` on `MIKEAA2020/arena-max--physics`. The final delivery includes this report as a non-force follow-up snapshot; the exact verified final commit is supplied in the completion message. Existing history/license are preserved. Credentials are excluded and nested archive contents are scanned before staging. See `PUBLICATION-SCOPE.md` at the project root.")
text+=['',publication_text,'',
'The v33 manuscript remains an **author-review draft**, not a certified submission: the original figure/SM, author approval and specialist analytic-hypothesis audit are still required. This continuation does not rewrite the original v33 numerical claims silently. A-1 stays separate from the Lighthouse source lineage, and Parts I–II commitments are unchanged.','']
(HERE/'RESULTS.md').write_text('\n'.join(text))

# The separate fixed-source grid must not be silently folded into older campaign counts.
scan=load(R/'n3_chi128_scan.json')
if scan:
    target=HERE/'RESULTS.md'
    existing=target.read_text()
    existing+='\n## Later six-rate chi128 continuation\n\nThe separate fixed-source scan is **'+scan.get('status','not recorded')+'**. Its per-rate/preparation statuses, actual checkpoints, symmetry alignment and coexistence criteria are in [SCAN128-RESULTS.md](SCAN128-RESULTS.md). The production table above is the earlier campaign, not an exhaustive or duplicate-counted merge of this new grid. The v34 author-review continuation also makes the governing real creator–creation distinction explicit while preserving v33.\n'
    target.write_text(existing)

# Standalone offline SVG chart using only the actual finite-size data.
W,Hh=920,510;left,right,top,bottom=76,890,58,430
xmin,xmax=.315,.405;ymin,ymax=0,2.5
sx=lambda p:left+(p-xmin)/(xmax-xmin)*(right-left)
sy=lambda y:bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}">','<rect width="100%" height="100%" fill="#fff"/>','<g font-family="Arial,sans-serif" fill="#182334">', '<text x="28" y="27" font-size="20" font-weight="bold">Fourth moment: finite-size standard-sector gaps</text>']
for p in [.32,.33,.34,.35,.36,.37,.38,.39,.4]:
    x=sx(p);svg += [f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="#e5eaf0"/>',f'<text x="{x}" y="453" font-size="12" text-anchor="middle">{p:.2f}</text>']
for y in [0,.5,1,1.5,2,2.5]:
    yy=sy(y);svg += [f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#e5eaf0"/>',f'<text x="62" y="{yy+4}" font-size="12" text-anchor="end">{y:g}</text>']
for i,(ens,L,color,dash) in enumerate([('haar',4,'#176a9e',''),('haar',6,'#176a9e','7,5'),('clifford',4,'#b44f2d',''),('clifford',6,'#b44f2d','7,5')]):
    pts=sorted((r['p'],r['X_std']) for r in lad.values() if r['ensemble']==ens and r['L']==L and xmin<=r['p']<=xmax)
    poly=' '.join(f'{sx(x):.2f},{sy(y):.2f}' for x,y in pts)
    svg.append(f'<polyline points="{poly}" fill="none" stroke="{color}" stroke-width="2.8" stroke-dasharray="{dash}"/>')
    for x,y in pts:svg.append(f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="3" fill="{color}"/>')
    ly=75+i*22;svg += [f'<line x1="92" y1="{ly}" x2="128" y2="{ly}" stroke="{color}" stroke-width="3" stroke-dasharray="{dash}"/>',f'<text x="138" y="{ly+4}" font-size="13">{ens.capitalize()}, L={L}</text>']
svg+=['<text x="480" y="478" font-size="14" text-anchor="middle">Measurement probability p</text>','<text x="21" y="250" transform="rotate(-90 21 250)" font-size="14" text-anchor="middle">L log(lambda_triv / lambda_std)</text>','<text x="76" y="501" font-size="12">L=4,6 crossings only. Finite-size separation is not a thermodynamic critical-point split.</text>','</g></svg>']
(HERE/'fourth-moment-gaps.svg').write_text('\n'.join(svg))
print(json.dumps(dict(production_rows=len(prod),accepted=len(accepted),matched=len(matched),fourth_cases=len(lad),d3_exact=len(ex.get('cases',{})),d3_mps=len(d3),n4_pilots=len(n4)),indent=2))

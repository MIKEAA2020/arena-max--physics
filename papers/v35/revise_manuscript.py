#!/usr/bin/env python3
"""Create the v35 author-review manuscript from preserved v34.

This adds the χ192 finite-χ evidence and a cautious χ256 follow-up plan only.
It does not run or claim a χ256 calculation, alter v33/v34, or modify proofs.
"""
from pathlib import Path
import hashlib, re, difflib, json, os

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'papers/v34/manuscript_revised_v34.tex'
OUT = HERE / 'manuscript_revised_v35.tex'
original = SOURCE.read_text()
s = original

def replace_once(old, new):
    global s
    n = s.count(old)
    if n != 1:
        raise ValueError(f'Expected one occurrence, found {n}: {old[:120]!r}')
    s = s.replace(old, new, 1)

# Update the revision header without touching v34.
s = s.replace('% manuscript_revised_v34.tex -- author-review continuation; 16 October 2026',
              '% manuscript_revised_v35.tex -- author-review continuation; 19 October 2026', 1)
s = s.replace('% Source: preserved v33; numerical and interpretation changes recorded separately.',
              '% Source: preserved v34 (itself derived from preserved v33); χ192 evidence added separately.', 1)

replace_once(
    'A later $\\chi=128$ shared-rate test yields two accepted small-order solutions at $p=.30486$; this does not establish continuity or coexistence.',
    'Later $\\chi=128$ and $\\chi=192$ paired-history calculations add finite-bond-dimension evidence but do not settle transition order. At $\\chi=192$, two distinct warm-history states were reported at $p=.304825$ within a coarse sampled change zone $p\\simeq.30480$--$.30485$; the final tensors for that pair are unavailable for reopening, and the $p=.30481$ follow-up did not converge. A controlled $\\chi=256$ paired-history study with same-objective comparisons and bond-dimension extrapolation is the next discriminating computation; it was not performed here.'
)
replace_once(
    'Later $\\chi=128$ two-preparation observations and the rate scan are reported below; weak first order and continuity remain live alternatives, not established classes.',
    'Later $\\chi=128$ observations and a $\\chi=192$ paired-history test are reported below. They characterize a coarse finite-$\\chi$ warm-history change zone, not a thermodynamic coexistence window; weak first order and continuity remain live alternatives, not established classes. A controlled $\\chi=256$ paired-history study is identified as the next discriminating computation, but is not part of the present results.'
)

chi192_section = r'''\subsection{Later $\chi=192$ paired-history evidence}
\label{sec:chi192-window}

A separately authorized author-review calculation tested two warm histories at the common rate $p=.304825$, using the same Hermitian half-row objective and the existing convergence and gauge gates. The ordered preparation was continued from the accepted $\chi=192$, $p=.30480$ state; the small-order preparation was continued from the accepted $p=.30485$ source. The two runs were reported accepted by their historical audit records, although the final $p=.304825$ MPS checkpoint blobs are no longer available for tensor-level reopening. Their values below are therefore historical audited observations, not newly re-audited tensors.

\begin{table}[t]
\caption{Reported $\chi=192$ paired observations at $p=.304825$. The final checkpoint files are missing; historical audit records report passing gates.}
\label{tab:chi192-mid-pair}
\begin{ruledtabular}
\begin{tabular}{lrrrr}
preparation & iterations & $\epsilon$ & color $L_2$ & $f_{\rm half}$\\
\colrule
ordered & 146 & $4.8394\times10^{-8}$ & 0.424511 & 0.992950567266\\
small-order & 199 & $4.9159\times10^{-8}$ & 0.000624 & 0.992950208167\\
\end{tabular}
\end{ruledtabular}
\end{table}

The reported same-rate color separation is 0.423887 and $\Delta f_{\rm half}$ (ordered minus small-order) is $+3.59099\times10^{-7}$. At $\chi=128$ and the same rate, the recorded ordered-minus-disordered $\Delta f_{\rm half}$ is $-4.359393\times10^{-7}$. This sign reversal is a finite-$\chi$ comparison, not an objective error bar, coexistence crossing, or controlled $\chi$-scaling result. Optimizer residuals are not free-energy error bars, and an accepted MPS state is not a global-minimum certificate.

Across the sampled $\chi=192$ warm histories, the low-order-start state was not retained as distinct at $p=.30480$; a distinct pair was reported at $p=.304825$; and the ordered-start retry at $p=.30485$ ended in the small-order state. These observations characterize an \emph{coarse finite-$\chi$ warm-history change zone of approximately $p=.30480$--$.30485$}, with pair retention demonstrated at the sampled midpoint. The endpoints are path outcomes, not mapped branch-stability limits, a thermodynamic coexistence interval, or a physical transition bracket.

A lower-side continuation at $p=.30481$ was not accepted. Its latest saved ordered checkpoint is cumulative iteration 19 with $\epsilon=1.30854\times10^{-6}$, above the external $10^{-7}$ tolerance and the internal $5\times10^{-8}$ goal; the paired small-order history was not completed. It does not refine the sampled change zone and is not evidence of accepted branch retention. The partial checkpoint is archived at \texttt{research/transition-order/chi192-p30481/} with SHA-256 \texttt{a8097162c27ca104556edd5c789bcf36e5c9c89ef5af7eb92ad3811248319cee}; it remains a non-accepted state.

The $\chi=192$ observations strengthen a first-order-like finite-$\chi$ reading relative to the earlier single-rate evidence, but they do not determine transition order. A continuous transition with small $\beta$, finite-entanglement crossover, or long-lived numerical configurations remain possible explanations. The final $p=.304825$ checkpoint loss and incomplete $p=.30481$ continuation also limit reproducibility.

The next discriminating computation is a \emph{controlled $\chi=256$ paired-history study}: converge ordered and small-order preparations at common rates bracketing this sampled zone, retain and independently audit reopenable final checkpoints, compare the same objective and observables, and assess the result together with $\chi=128$ and $\chi=192$ through controlled bond-dimension extrapolation and a direct coexistence or branch-stability test. A single $\chi=256$ point alone would not settle thermodynamic order. No $\chi=256$ calculation is reported here.'''
marker = r'\subsection{Four- and five-replica finite-size diagnostics}'
if s.count(marker) != 1:
    raise ValueError('Expected one insertion marker for χ192 subsection')
s = s.replace(marker, chi192_section + '\n\n' + marker, 1)

old_conclusion = ('Weak first order and continuity remain open; the later $\\chi=128$ comparison and rate scan are finite-$\\chi$ observations, not a binary order test. '
                  'We retract the three- and four-state-Potts assignments and the argument from the dimension of one standard irrep. '
                  'The regular bimodule and the conditional $n!$ ordered-state orbit supply the appropriate structural comparison without proving transition order. '
                  'Four- and five-replica small-system spectra are retained as such; the $n=5$ first-order reading is plausible but not asymptotically certified. '
                  'No converged coexistence length, nonzero latent heat, real-replica changeover, or $q\\to1$ continuation is claimed.')
new_conclusion = ('Weak first order and continuity remain open; the later $\\chi=128$ and $\\chi=192$ observations are finite-$\\chi$ evidence, not a binary order test. '
                  'At $\\chi=192$, a coarse sampled warm-history change zone spans approximately $.30480$--$.30485$, with a reported distinct pair at $.304825$; the endpoints are path outcomes and the final pair tensors are unavailable for reopening. '
                  'The $.30481$ follow-up did not converge and does not refine that zone. A controlled $\\chi=256$ paired-history study, with same-objective comparisons and $\\chi$-extrapolation/coexistence checks, is the next computation needed to determine whether the finite-$\\chi$ pattern survives; it was not run here. '
                  'Transition order remains unresolved. We retract the three- and four-state-Potts assignments and the argument from the dimension of one standard irrep. '
                  'The regular bimodule and the conditional $n!$ ordered-state orbit supply the appropriate structural comparison without proving transition order. '
                  'Four- and five-replica small-system spectra are retained as such; the $n=5$ first-order reading is plausible but not asymptotically certified. '
                  'No converged coexistence length, nonzero latent heat, real-replica changeover, or $q\\to1$ continuation is claimed.')
replace_once(old_conclusion, new_conclusion)

replace_once(
    r'\noindent\textbf{Revision status:} This v33 is an author-review draft prepared with Arena.ai assistance. The author must review the new text, numerical artifacts, narrowed theorem hypotheses, and publication claims before release. No peer review or author approval of this revision is implied.',
    r'\noindent\textbf{Revision status:} This v35 continuation is an author-review draft prepared with Arena.ai assistance. The author must review the new text, numerical artifacts, narrowed theorem hypotheses, and publication claims before release. No peer review or author approval of this revision is implied.'
)
replace_once(
    r'\noindent\textbf{v33 numerical artifacts:} The accompanying review package supplies independent transfer-matrix and uniform-MPS scripts, tilted-Clifford SMC scripts, JSON data, validation logs and a source diff. It does not include the v32 supplementary deposit or original figure files; their quoted results are author-reported unless explicitly rechecked in the revision report. The new MPS values have finite-bond-dimension and optimizer systematics; SMC histograms have finite-population and genealogy systematics. No new coexistence result is claimed.',
    r'\noindent\textbf{Numerical artifacts and limitations:} The accompanying review package supplies independent transfer-matrix and uniform-MPS scripts, tilted-Clifford SMC scripts, JSON data, validation logs and source diffs. It does not include the v32 supplementary deposit or original figure files; their quoted results are author-reported unless explicitly rechecked. The historical $\chi=192$, $p=.304825$ audit records report accepted states, but the final MPS checkpoint blobs are unavailable for reopening; the $p=.30481$ follow-up is incomplete. The surviving partial checkpoint and campaign records are identified in the author-review data package. The $\chi=256$ study is a proposed future computation, not a result of this manuscript. No new thermodynamic coexistence result is claimed.'
)

# Contract checks: preserve all mathematical statement/proof environments, labels and citations.
pattern = re.compile(r'\\begin\{(theorem|proposition|lemma|corollary|definition|assumption|remark|proof|structuralproposition)\}.*?\\end\{\1\}', re.S)
source_blocks = [m.group(0) for m in pattern.finditer(original)]
output_blocks = [m.group(0) for m in pattern.finditer(s)]
if not source_blocks or source_blocks != output_blocks:
    raise AssertionError('A theorem/proof/statement block changed')
labels = re.findall(r'\\label\{([^}]+)\}', s)
if len(labels) != len(set(labels)):
    raise AssertionError('Duplicate LaTeX labels')
refs = re.findall(r'\\(?:eqref|ref|autoref)\{([^}]+)\}', s)
if not set(refs) <= set(labels):
    raise AssertionError('Unresolved internal references')
bibkeys = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', s))
cites = {k.strip() for v in re.findall(r'\\cite\{([^}]+)\}', s) for k in v.split(',')}
if not cites <= bibkeys:
    raise AssertionError('Unresolved citation keys')

def atomic(path, text):
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(text)
    os.replace(tmp, path)

atomic(OUT, s)
diff = ''.join(difflib.unified_diff(original.splitlines(True), s.splitlines(True),
                                   fromfile='papers/v34/manuscript_revised_v34.tex',
                                   tofile='papers/v35/manuscript_revised_v35.tex'))
atomic(HERE / 'v34-to-v35.diff', diff)
prov = {
    'revision': 'v35 author-review continuation',
    'source_v34_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'source_v33_sha256': hashlib.sha256((ROOT/'papers/v33/manuscript_revised_v33.tex').read_bytes()).hexdigest(),
    'output_v35_sha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
    'unchanged_math_statement_and_proof_blocks': len(source_blocks),
    'labels_unique': True,
    'internal_references_resolve': True,
    'citation_keys_resolve': True,
    'chi192_p304825_status': 'historically reported accepted; audits marked passed; final checkpoint blobs unavailable for reopening',
    'chi192_p30481_status': 'incomplete at cumulative iteration 19; not accepted',
    'transition_order': 'unresolved',
    'finite_chi_window': 'coarse sampled warm-history change zone p=.30480--.30485; not thermodynamic coexistence interval',
    'chi256': 'proposed future paired-history/extrapolation study; not run',
    'submission_status': 'author-review; not submission certified'
}
atomic(HERE/'source-provenance.json', json.dumps(prov, indent=2)+'\n')
atomic(HERE/'source-contract-check.log',
       f"PASS\nunchanged mathematical statement/proof blocks: {len(source_blocks)}\nunique labels: {len(labels)}\nreferences resolved: {len(refs)}\ncitation keys resolved: {len(cites)}\nPDF compile/layout: not run\nscientific status: chi192 order unresolved; chi256 not run\n")
print(json.dumps(prov, indent=2))

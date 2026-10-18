#!/usr/bin/env python3
"""Create v36 main text and supplementary run details from preserved v35."""
from pathlib import Path
import hashlib, re, difflib, json, os

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'papers/v35/manuscript_revised_v35.tex'
OUT = HERE / 'manuscript_revised_v36.tex'
SUPP = HERE / 'supplementary_v36.tex'
BS = chr(92)
original = SOURCE.read_text()
s = original

def replace_once(old, new):
    global s
    n = s.count(old)
    if n != 1:
        raise ValueError(f'Expected one occurrence, found {n}: {old[:120]!r}')
    s = s.replace(old, new, 1)

s = s.replace('% manuscript_revised_v35.tex -- author-review continuation; 19 October 2026',
              '% manuscript_revised_v36.tex -- author-review continuation; 19 October 2026', 1)
s = s.replace('% Source: preserved v34 (itself derived from preserved v33); χ192 evidence added separately.',
              '% Source: preserved v35; χ192 run-level details moved to supplementary_v36.tex.', 1)

old_abs = (r'At $\chi=192$, two distinct warm-history states were reported at $p=.304825$ within a coarse sampled change zone '
           r'$p\simeq.30480$--$.30485$; the final tensors for that pair are unavailable for reopening, and the $p=.30481$ follow-up did not converge.')
new_abs = (r'At $\chi=192$, a distinct warm-history pair was reported at $p=.304825$ within a coarse sampled finite-$\chi$ change zone '
           r'$p\simeq.30480$--$.30485$.')
replace_once(old_abs, new_abs)

start = BS + 'subsection{Later $' + BS + 'chi=192$ paired-history evidence}'
end = BS + 'subsection{Four- and five-replica finite-size diagnostics}'
if s.count(start) != 1 or s.count(end) != 1:
    raise ValueError('Could not locate χ192 main-text section boundaries')
a = s.index(start); b = s.index(end, a)
main_section = r'''\subsection{Finite-$\chi$ warm-history change zone at $\chi=192$}
\label{sec:chi192-window}

A later paired-history probe at $\chi=192$ reports distinct ordered- and small-order-history states at $p=.304825$. In the neighboring sampled outcomes, the small-order history was not retained as distinct at $p=.30480$, whereas an ordered-start retry at $p=.30485$ ended in the small-order state. Taken together, these outcomes characterize a \emph{coarse sampled finite-$\chi$ warm-history change zone of approximately $p=.30480$--$.30485$}. The reported interval is a description of sampled history dependence, not a thermodynamic coexistence window, a pair of branch-stability boundaries, a spinodal, or a physical transition bracket. Additional run-level values and audit/provenance notes are provided in Supplementary Material, Sec.~S1.

These observations strengthen a first-order-like finite-$\chi$ reading but do not determine transition order. A continuous transition with small $\beta$, finite-entanglement crossover, or long-lived numerical configurations remain possible. \textbf{Transition order remains unresolved.} The next discriminating computation is a controlled $\chi=256$ paired-history study at common rates, with same-objective comparisons, reopenable independently audited checkpoints, and controlled $\chi$ extrapolation plus a direct coexistence or branch-stability test. A single $\chi=256$ point alone would not settle the thermodynamic order; no $\chi=256$ calculation is reported here.'''
s = s[:a] + main_section + '\n\n' + s[b:]

# Replace only the corresponding conclusion paragraph, after the conclusion heading.
conclusion_heading = BS + 'section{Conclusion}'
cpos = s.index(conclusion_heading)
para_start = s.index('The corrected annealed phase diagram has a numerically located three-replica transition', cpos)
para_end = s.index('\n\nConditional-trajectory', para_start)
new_conclusion = ('The corrected annealed phase diagram has a numerically located three-replica transition near $p_c^{(3)}=.3049(2)$, with simultaneous loss of sign and standard order in the sampled uniform-MPS scans through $\\chi=96$. '
                  'Weak first order and continuity remain open; the later $\\chi=128$ and $\\chi=192$ observations are finite-$\\chi$ evidence, not a binary order test. '
                  'At $\\chi=192$, a coarse sampled warm-history change zone spans approximately $.30480$--$.30485$, with a reported distinct pair at $.304825$; these are finite-$\\chi$ history outcomes, not physical stability or coexistence boundaries. '
                  'A controlled $\\chi=256$ paired-history study, with same-objective comparisons and $\\chi$ extrapolation/coexistence checks, is the next computation needed to determine whether the finite-$\\chi$ pattern survives; it was not run here. '
                  'Transition order remains unresolved. We retract the three- and four-state-Potts assignments and the argument from the dimension of one standard irrep. '
                  'The regular bimodule and the conditional $n!$ ordered-state orbit supply the appropriate structural comparison without proving transition order. '
                  'Four- and five-replica small-system spectra are retained as such; the $n=5$ first-order reading is plausible but not asymptotically certified. '
                  'No converged coexistence length, nonzero latent heat, real-replica changeover, or $q\\to1$ continuation is claimed.')
s = s[:para_start] + new_conclusion + s[para_end:]

replace_once('This v35 continuation is an author-review draft prepared with Arena.ai assistance.',
             'This v36 continuation is an author-review draft prepared with Arena.ai assistance.')
# Keep detailed status in the supplement, not in main-text declarations.
art_start = BS + 'noindent' + BS + 'textbf{Numerical artifacts and limitations:}'
ack_start = BS + 'noindent' + BS + 'textbf{Acknowledgements:}'
if s.count(art_start) != 1 or s.count(ack_start) != 1:
    raise ValueError('Could not locate numerical-artifact declaration')
art_a=s.index(art_start); art_b=s.index(ack_start,art_a)
new_art = (r'\noindent\textbf{Numerical artifacts and limitations:} The accompanying review package supplies independent transfer-matrix and uniform-MPS scripts, tilted-Clifford SMC scripts, JSON data, validation logs and source diffs. It does not include the v32 supplementary deposit or original figure files; their quoted results are author-reported unless explicitly rechecked. The $\chi=192$ numerical values and audit/provenance notes are provided in Supplementary Material, Sec.~S1. The $\chi=256$ study is a proposed future computation, not a result of this manuscript. No new thermodynamic coexistence result is claimed.' + '\n\n')
s = s[:art_a] + new_art + s[art_b:]

supp = r'''\documentclass[aps,prx,onecolumn,nofootinbib]{revtex4-2}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{hyperref}
\begin{document}
\title{Supplementary Material for: Exact Replica Mechanics and Born-Record Large Deviations in Monitored Quantum Circuits}
\author{Amin Abaee}
\date{\today}
\maketitle

\section*{S1. $\chi=192$ paired-history run details and incomplete continuation}
\label{sec:supp-chi192}

This section records the run-level details underlying the concise main-text characterization. These are finite-$\chi$ warm-history observations, not measurements of a thermodynamic coexistence interval, spinodal, physical transition bracket, or transition order.

\paragraph{Reported $p=.304825$ pair.} A separately authorized author-review calculation tested two warm histories at the common rate $p=.304825$, using the same Hermitian half-row objective and the established convergence and gauge gates. The ordered preparation was continued from the accepted $\chi=192$, $p=.30480$ state; the small-order preparation was continued from the accepted $p=.30485$ source. Historical audit records report that both runs passed acceptance gates. The final $p=.304825$ MPS checkpoint blobs are unavailable for tensor-level reopening, so these remain historical audited observations rather than newly re-audited tensors.

\begin{table}[h]
\caption{Historical $\chi=192$ paired observations at $p=.304825$. The final checkpoint files are unavailable for reopening.}
\begin{ruledtabular}
\begin{tabular}{lrrrr}
preparation & iterations & $\epsilon$ & color $L_2$ & $f_{\rm half}$\\
\colrule
ordered & 146 & $4.8394074016\times10^{-8}$ & 0.424511350240 & 0.992950567266133\\
small-order & 199 & $4.9158883629\times10^{-8}$ & 0.000624328653 & 0.992950208166968\\
\end{tabular}
\end{ruledtabular}
\end{table}

The recorded same-rate color separation is 0.4238870216. The reported same-objective difference $\Delta f_{\rm half}$ (ordered minus small-order) is $+3.5909916507\times10^{-7}$. At $\chi=128$ and the same rate, the recorded ordered-minus-disordered $\Delta f_{\rm half}$ is $-4.359393\times10^{-7}$. The sign reversal is a finite-$\chi$ comparison; it is not an objective error bar, a calibrated crossing, or a controlled $\chi$-scaling result. Optimizer residuals are not free-energy error bars, and accepted MPS states are not global-minimum certificates.

\paragraph{Sampled neighboring outcomes.} The low-order-start state was not retained as distinct at $p=.30480$. A distinct pair was reported at $p=.304825$. An ordered-start retry at $p=.30485$ ended in the small-order state. These path outcomes support the main-text description of a coarse sampled finite-$\chi$ warm-history change zone of approximately $.30480$--$.30485$; they do not map branch-stability boundaries.

\paragraph{Incomplete $p=.30481$ continuation.} The lower-side ordered continuation was not accepted. Its latest saved checkpoint was cumulative iteration 19, with $\epsilon=1.308536380704902\times10^{-6}$, above the external $10^{-7}$ tolerance and internal $5\times10^{-8}$ goal. The recorded optimizer time was 3222.734782934189 seconds. The paired small-order history was not completed. The run manager and worker became unavailable; the termination source was not identified. The surviving finite-tensor checkpoint is archived at \texttt{research/transition-order/chi192-p30481/} with SHA-256 \texttt{a8097162c27ca104556edd5c789bcf36e5c9c89ef5af7eb92ad3811248319cee}. It is a partial, non-accepted state and does not refine the sampled zone.

No $\chi=256$ calculation was run for this manuscript. The proposed controlled paired-history study and extrapolation are future work only.
\end{document}
'''

# Contract checks: preserve all mathematical statement/proof blocks in the main paper.
pattern = re.compile(r'\\begin\{(theorem|proposition|lemma|corollary|definition|assumption|remark|proof|structuralproposition)\}.*?\\end\{\1\}', re.S)
source_blocks = [m.group(0) for m in pattern.finditer(original)]
output_blocks = [m.group(0) for m in pattern.finditer(s)]
if not source_blocks or source_blocks != output_blocks:
    raise AssertionError('Mathematical statement/proof blocks changed')
labels = re.findall(r'\\label\{([^}]+)\}', s)
if len(labels) != len(set(labels)):
    raise AssertionError('Duplicate main-text labels')
refs = re.findall(r'\\(?:eqref|ref|autoref)\{([^}]+)\}', s)
if not set(refs) <= set(labels):
    raise AssertionError('Unresolved main-text references')
bibkeys = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', s))
cites = {k.strip() for v in re.findall(r'\\cite\{([^}]+)\}', s) for k in v.split(',')}
if not cites <= bibkeys:
    raise AssertionError('Unresolved citation keys')
# Ensure the detailed run identifiers live only in the supplement.
for fragment in ['p=.30481','1.308536380704902','a8097162c27ca104','4.8394074016','3.5909916507']:
    if fragment in s:
        raise AssertionError('Run-level detail remains in main text: '+fragment)
    if fragment not in supp:
        raise AssertionError('Run-level detail missing from supplement: '+fragment)

def atomic(path, text):
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(text)
    os.replace(tmp, path)

atomic(OUT, s)
atomic(SUPP, supp)
diff = ''.join(difflib.unified_diff(original.splitlines(True), s.splitlines(True),
                                   fromfile='papers/v35/manuscript_revised_v35.tex',
                                   tofile='papers/v36/manuscript_revised_v36.tex'))
atomic(HERE / 'v35-to-v36.diff', diff)
prov = {
    'revision': 'v36 author-review continuation',
    'source_v35_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'output_v36_sha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
    'supplementary_sha256': hashlib.sha256(SUPP.read_bytes()).hexdigest(),
    'unchanged_math_statement_and_proof_blocks': len(source_blocks),
    'unique_main_labels': len(labels),
    'internal_main_references_resolve': True,
    'main_citation_keys_resolve': True,
    'chi192_run_details': 'moved to supplementary_v36.tex, S1',
    'p30481_status': 'partial at cumulative iteration 19; not accepted; details supplementary only',
    'main_text_window': 'coarse sampled finite-chi warm-history change zone p=.30480--.30485',
    'transition_order': 'unresolved in main text',
    'chi256': 'future work only; not run',
    'pdf_compile': 'not run; no TeX engine available',
    'submission_status': 'author-review'
}
atomic(HERE / 'source-provenance.json', json.dumps(prov, indent=2) + '\n')
atomic(HERE / 'source-contract-check.log',
       f"PASS\nunchanged mathematical statement/proof blocks: {len(source_blocks)}\nunique main labels: {len(labels)}\ninternal references: {len(refs)} resolved\ncitation keys: {len(cites)} resolved\nrun-level χ192 values/checkpoint details/p=.30481 attempt: supplementary only\nPDF compile/layout: not run\ntransition order: unresolved; χ256 not run\n")
print(json.dumps(prov, indent=2))

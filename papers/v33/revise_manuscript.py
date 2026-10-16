#!/usr/bin/env python3
"""Reproduce the v33 author-review draft from the unmodified uploaded v32 source.
No missing supplemental result or new production computation is invented. New sections
are unnumbered theorem-like statements so all original theorem/proposition labels and
numbering are preserved. The change log records narrowed statements outside the class audit.
"""
from pathlib import Path
import hashlib, json, difflib
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
src=ROOT/'adjudications/adj-01-a-manuscript_revised_v32.txt'
s=src.read_text(); original=s

def replace_region(start,end,new):
    global s
    i=s.index(start); j=s.index(end,i)
    s=s[:i]+new.rstrip()+'\n\n'+s[j:]

def fragment(name): return (HERE/'sections'/name).read_text()

s=s.replace('% manuscript_revised_v32.tex -- claims-alignment +','% manuscript_revised_v33.tex -- author-review draft; 16 October 2026\n% Reproduction: papers/v33/revise_manuscript.py; see REVISION-REPORT.md.\n% The v32 provenance ledger below is historical, not a certificate of the new numerics.')
s=s.replace('\\newtheorem{conjecture}{Conjecture}', '\\newtheorem{conjecture}{Conjecture}\n\\newtheorem*{structuralproposition}{Structural proposition}')
replace_region('\\begin{abstract}','\\end{abstract}',fragment('abstract.tex'))
s=s.replace('Potts universality classes;', 'permutation symmetry; finite-entanglement scaling;')
replace_region('The second contribution is the annealed replica ladder','A local wire has Hilbert space',fragment('introduction.tex'))
# Local factual corrections, separate from withdrawal of class claims.
s=s.replace('which locate the annealed three-replica critical point numerically and find it continuous, with three-state-Potts scaling amplitudes.',
            'which locate the annealed three-replica transition numerically and document why finite-size amplitudes did not establish its class.')
s=s.replace('independently Haar-averaged gates (or exact 2-designs).', 'independently Haar-averaged gates (or exact $n$-designs at replica number $n$).')
replace_region('\\subsection{The annealed three-replica critical point}', '\\section{Born normalization, replica data, and complexity}',fragment('replica-phase-diagram.tex'))
# Correct a false design/Gram coincidence: the fourth Gram is invertible but Clifford is not a 4-design.
s=s.replace('design property stops at exactly the replica number at which the\npermutation Gram matrix is still invertible, $d^2\\ge n$---consistent with',
            'design property stops at order three, independently of the\ninvertibility of the Haar permutation Gram matrix (which remains invertible at $n=4$, $d^2=4$)---consistent with')
# Insert new SMC subsection without changing numbered propositions.
i=s.index('\\begin{remark}[Born-average complexity trichotomy]')
s=s[:i]+fragment('tilted-smc.tex')+'\n\n'+s[i:]
s=s.replace('sampling and every tilted average $\\E_{\\rm Born}[P^\\beta f]$ are\npoly-time by the Gottesman--Knill theorem~\\cite{Gottesman1998};',
'''sampling and the evaluation of a per-trajectory score are polynomial-time by the
Gottesman--Knill theorem~\\cite{Gottesman1998}. This does not bound the sample cost of
relative-error estimation of an exponentially small tilted average or of its logarithm;
rare-event and finite-population errors must be controlled separately. In particular,''')
s=s.replace('The Clifford testbed is the maximal exactly-solvable window of the general\nmonitored problem, and $\\Lambda_L$ is well defined precisely because of\nlevel (i).',
'''The Clifford testbed supplies efficient trajectories, not a general polynomial-time
relative-error algorithm for its disorder SCGF. The definition of $\\Lambda_L$ does not
depend on the existence of an efficient estimator.''')
s=s.replace('almost\nsurely entrywise strictly positive (some finite product in the support of\nthe disorder law is strictly positive, in the sense of Ruelle and\nPeres~\\cite{Ruelle1979,Peres1992}) and strongly irreducible.',
            'almost\nsurely entrywise strictly positive and strongly irreducible.')
# Exact interpolation identity retained; its claimed sufficient condition is corrected.
s=s.replace('approached\nquadratically as $m\\downarrow0$', 'approached\nlinearly as $m\\downarrow0$')
old='''a sufficient condition is the
self-averaging bound $\\sup_{T}\\operatorname{Var}\\!\\big(T^{-1}\\log Z_{q,\\omega}(T)\\big)
<\\infty$, a measurable quantity for the sequential Monte Carlo machinery
of the next subsection,'''
new=r'''a sufficient uniform condition, with $V=2LT$ and $Y_V=\log Z_{q,\omega}(T)$,
is $\sup_V\sup_{0\le s\le m_0}\operatorname{Var}_s(Y_V)/V\le C$ for some
$m_0>0$. Indeed the normalized gap is bounded by $Cm/2$ directly from
Eq.~\eqref{eq:repint}. A merely bounded variance of $Y_V/V$ is insufficient:
$Y_V=-VB$ with a fair Bernoulli variable $B$ has normalized variance $1/4$,
but $\lim_{V\to\infty}(mV)^{-1}\log\E e^{mY_V}=0$ at every $m>0$,
whereas $\E Y_V/V=-1/2$. This correction concerns limit interchange, not
the exact finite-volume identity,'''
assert old in s
s=s.replace(old,new)
s=s.replace('the quadratic small-$m$ rate', 'the linear small-$m$ rate for $f_m$')
# Narrow no-freezing to the analytic-cocycle hypotheses actually needed; finite reachability alone is not a proof.
s=s.replace("and strongly irreducible.  Clifford", "and strongly irreducible. Clifford")
s=s.replace("and strongly irreducible. Clifford", r"""and strongly irreducible. For analyticity we use the following additional,
concrete sufficient regularity condition on each real compact interval $I$. After
factoring a positive analytic scalar $a_\omega(k)$, the entries of
$\widehat{\mathcal Q}_{k,\omega}=\mathcal Q_{k,\omega}/a_\omega(k)$
extend holomorphically to a common complex neighborhood of $I$, are uniformly
bounded there, and obey
$\delta_I\le(\widehat{\mathcal Q}_{k,\omega})_{ij}\le\delta_I^{-1}$
for real $k\in I$ and some $\delta_I>0$. The analytic logarithm of
$a_\omega$ is integrably dominated on that neighborhood. These assumptions
supply uniform projective contraction and analytic domination for the top-Lyapunov
theorem~\cite{Ruelle1979,Peres1992}; positivity and logarithmic integrability alone
are not asserted to imply them. Uniformly positive finite-support analytic families
are a sufficient subclass. Clifford""")
s=s.replace('''Then:
(i) for almost every $\\omega$''', '''Assume also the analytic-cocycle regularity specified above on every compact interval.
Then:
(i) for almost every $\\omega$''',1)
s=s.replace('''(ii) $k\\mapsto\\gamma(k)$ is real-analytic on all of $\\mathbb R$ under the
stated allowability''', '''(ii) $k\\mapsto\\gamma(k)$ is real-analytic on the connected domain covered by the
stated analytic-cocycle hypotheses (on all of $\\mathbb R$ when they hold on every compact interval)''')
start='''If the reachable set decomposes into $r\\ge2$ invariant
communicating classes with allowable restrictions, then'''
end='''Freezing requires an \\emph{unbounded} reachable set, as in the
random-energy sequence of Theorem~\\ref{thm:rem}.'''
if start in s:
    i=s.index(start); j=s.index(end,i)+len(end)
    s=s[:i]+r'''For finitely many accessible invariant communicating classes, the growth rate is
the maximum of the corresponding branch exponents. Corners may occur at branch exchanges.
A branch that is analytic and non-affine cannot develop a new affine interval; however an
already affine (deterministic or zero-variance) component can dominate beyond a crossing.
For example, a conserved fair sector label selecting either deterministic bits or fair
independent bits gives $\psi(k)=\max\{0,k\log2\}$, a finite-state example with affine
branches. Thus the no-affine-onset conclusion is restricted to irreducible nondegenerate
analytic branches; finite reachability alone does not imply that freezing requires an
unbounded reachable set.''' + s[j:]
replace_region('\\begin{corollary}[The fully monitored point, unconditional]', '\\begin{proposition}[Replica interpolation identity]',r'''\begin{corollary}[The fully monitored point: existence and conditional analyticity]
\label{cor:p1closure}
At $p=1$ with Haar-refreshed gates the finite-state tilted matrices are almost surely
strictly positive and have integrable entry logarithms on real compact $k$ intervals.
The quenched growth rate therefore exists and is deterministic. Its real-analyticity
and the no-affine-onset conclusion require, in addition, the analytic-cocycle regularity
of Theorem~\ref{thm:nofreeze}. The full Haar-support verification of that extra hypothesis
is not supplied here; numerical smoothness is not a substitute. For a uniformly positive
finite-support analytic gate family the sufficient subclass above applies.
\end{corollary}''')
s=s.replace('''Its analyticity in $k$ is no longer conditional: Theorem~\\ref{thm:nofreeze} and Corollary~\\ref{cor:p1closure} below close it for exactly this family, since almost-surely entrywise strictly positive tilted matrices are allowable.''',
'''Its analyticity requires the additional analytic-cocycle hypotheses of Theorem~\\ref{thm:nofreeze}; positivity and integrable logarithms establish existence, not by themselves the full analyticity claim (Corollary~\\ref{cor:p1closure}).''')
replace_region('\\begin{remark}[Corners versus affine branches---the physical dichotomy]', '\\subsection{Sequential Monte Carlo contract}',r'''\begin{remark}[Corners, nondegeneracy, and affine branches]
\label{rem:dichotomy}
Theorem~\ref{thm:nofreeze} rules out a new affine interval within an irreducible,
nondegenerate analytic branch. A maximum of distinct analytic branches may instead have
corners. If one accessible branch is already affine, a branch exchange can expose an
affine tail even on a finite reachable set. The random-energy sequence of
Theorem~\ref{thm:rem} illustrates another mechanism, but is not a classification theorem
for every finite-state reducible process. All claims here distinguish quenched record
statistics, annealed disorder tilts, and the subsequent spatial thermodynamic limit.
\end{remark}''')
replace_region('\\section{Discussion and open problems}', '\\section*{Declarations}',fragment('discussion-interpretation-conclusion.tex'))
# Preserve author declarations as historical, but do not certify author review of the generated revision.
s=s.replace('\\noindent\\textbf{AI declaration:}', '\\noindent\\textbf{Revision status:} This v33 is an author-review draft prepared with Arena.ai assistance. The author must review the new text, numerical artifacts, narrowed theorem hypotheses, and publication claims before release. No peer review or author approval of this revision is implied.\n\n\\noindent\\textbf{AI declaration (v32):}')
# Add reproducibility disclosure rather than pretending the earlier SM/figures are supplied.
key='\\noindent\\textbf{Acknowledgements:}'
s=s.replace(key,r'''\noindent\textbf{v33 numerical artifacts:} The accompanying review package supplies independent transfer-matrix and uniform-MPS scripts, tilted-Clifford SMC scripts, JSON data, validation logs and a source diff. It does not include the v32 supplementary deposit or original figure files; their quoted results are author-reported unless explicitly rechecked in the revision report. The new MPS values have finite-bond-dimension and optimizer systematics; SMC histograms have finite-population and genealogy systematics. No new coexistence result is claimed.

'''+key)
# Keep the fixed CPD promise and proof; make the optional amplified promise non-overlapping.
s=s.replace('the same holds for any pair of thresholds $1-2^{-n}$ (YES) versus $1/2+2^{-n}$ (NO).',
            'the same holds for the threshold pair $1-2^{-n}$ (YES) versus $1/2+2^{-n}$ (NO) for every integer $n\\ge3$.')
# New bibliography entries (the v32 BCA / Vasseur citations remain and are credited).
refs=r'''
\bibitem{ZaunerStauber2018} V. Zauner-Stauber, L. Vanderstraeten, M. T. Fishman, F. Verstraete, and J. Haegeman, Phys. Rev. B \textbf{97}, 045145 (2018).
\bibitem{Fishman2018} M. T. Fishman, L. Vanderstraeten, V. Zauner-Stauber, J. Haegeman, and F. Verstraete, Phys. Rev. B \textbf{98}, 235148 (2018).
\bibitem{GrossNezamiWalter2021} D. Gross, S. Nezami, and M. Walter, Commun. Math. Phys. \textbf{385}, 1325--1393 (2021), arXiv:1712.08628.
\bibitem{Bittel2026} L. Bittel, J. Eisert, L. Leone, A. A. Mele, and S. F. E. Oliviero, Quantum \textbf{10}, 2171 (2026), arXiv:2504.12263.
\bibitem{Giardina2006} C. Giardin\`a, J. Kurchan, and L. Peliti, Phys. Rev. Lett. \textbf{96}, 120603 (2006).
\bibitem{BorgsImbrie1989} C. Borgs and J. Z. Imbrie, Commun. Math. Phys. \textbf{123}, 305--328 (1989).
'''
s=s.replace('\\end{thebibliography}',refs+'\n\\end{thebibliography}')
out=HERE/'manuscript_revised_v33.tex'; out.write_text(s)
(HERE/'v32-to-v33.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='manuscript_revised_v32.tex',tofile='manuscript_revised_v33.tex')))
(HERE/'source-provenance.json').write_text(json.dumps(dict(input=str(src.relative_to(ROOT)), input_sha256=hashlib.sha256(original.encode()).hexdigest(), output_sha256=hashlib.sha256(s.encode()).hexdigest(), revision='33', status='author-review draft', local_date='2026-10-16'),indent=2))
print(out, len(s.split()), 'whitespace-separated words')

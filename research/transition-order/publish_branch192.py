#!/usr/bin/env python3
"""Secret-scanned, ordinary non-force publication of the chi192 test only via mirror.
Uses authorized public repository main, preserves history and LICENSE.
"""
from pathlib import Path
import os,sys,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;R=ROOT/'v2.2/verify/replica';C=ROOT/'.arena/publish'
def run(args,env=None,capture=False):
 if capture:return subprocess.check_output(args,cwd=ROOT,text=True,env=env)
 return subprocess.run(args,cwd=ROOT,check=True,env=env)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
# Refresh human-readable and compact artifacts before the credential-scanned mirror pass.
run([sys.executable,str(HERE/'branch192_report.py')])
run([sys.executable,str(HERE/'bundle_review.py')])
run([sys.executable,str(HERE/'prepare_publication.py')])
if not (C/'.git').is_dir():raise SystemExit('Publication mirror missing')
remote=run(['git','-C',str(C),'remote','get-url','origin'],capture=True).strip()
if remote not in ['https://github.com/MIKEAA2020/arena-max--physics.git','https://github.com/MIKEAA2020/arena-max--physics']:
 raise SystemExit('Refusing any repository other than the explicitly authorized main remote')
# No physics kernels or optimizer were changed; independently audit accepted files and exact source hashes.
protocol=json.loads((HERE/'branch192-protocol.json').read_text());campaign=json.loads((R/'n3_branch192.json').read_text());audit=json.loads((R/'branch192_state_audit.json').read_text())
if campaign.get('status')!='both accepted finite-chi states' or len(campaign.get('results',{}))!=2:raise SystemExit('Campaign pair not accepted; refuse result publication')
if not audit.get('gates_recomputed'):raise SystemExit('Independent saved-state audit incomplete')
for side in ['ordered','disordered']:
 row=campaign['results'][side];cp=R/row['checkpoint']
 if not row.get('converged') or digest(cp)!=row.get('checkpoint_sha256'):raise SystemExit('State record/checkpoint hash mismatch')
for name,expected in protocol['source_sha256'].items():
 if name.endswith('branch192_report.py'):continue # post-run report-only formatter update is explicitly recorded in the report.
 if digest(ROOT/name)!=expected:raise SystemExit('Frozen calculation source mismatch: '+name)
if digest(R/'branch192_worker_v2.py')!=json.loads((HERE/'branch192-retry-addendum.json').read_text())['corrected_worker_sha256']:
 raise SystemExit('Corrected production worker hash mismatch')
# At most two single-thread workers and no campaign jobs remain.
ps=run(['ps','-eo','args='],capture=True)
active=[line for line in ps.splitlines() if 'branch192_worker_v2.py' in line or 'branch192_retry_execution.py' in line]
if active:raise SystemExit('Active chi192 process remains; refuse publication snapshot')
env=os.environ.copy();env.update(GIT_ASKPASS=str(ROOT/'.private/github-askpass.py'),GIT_TERMINAL_PROMPT='0')
for k in ['GIT_TRACE','GIT_TRACE_PACKET','GIT_TRACE_CURL','GIT_CURL_VERBOSE']:env.pop(k,None)
def git(*args,capture=False):return run(['git','-c','credential.helper=','-C',str(C),*args],env=env,capture=capture)
# Refresh remote refs before staging; only a clean exact-base ordinary main push is permitted.
git('fetch','--quiet','origin','main')
head=git('rev-parse','HEAD',capture=True).strip();origin=git('rev-parse','origin/main',capture=True).strip()
if head!=origin:raise SystemExit('Remote main changed since mirror checkout; stop without rebase or force-push')
if git('diff','--','LICENSE',capture=True).strip():raise SystemExit('LICENSE differs; refuse commit')
git('add','--all')
names=git('diff','--cached','--name-only',capture=True).splitlines()
for name in names:
 if name.startswith(('.private/','.arena/')) or 'github-repository.pat' in name or name.endswith('.tmp'):
  raise SystemExit('Credential/cache/temp path unexpectedly staged; refused')
if not names:raise SystemExit('No publication diff')
git('diff','--cached','--check')
print('CHI192_STAGED',json.dumps(dict(files=len(names),license_unchanged=True,credential_scan='passed by prepare_publication.py',ordinary_push_only=True)),flush=True)
git('-c','user.name=Arena Research Assistant','-c','user.email=assistant@arena.invalid','-c','commit.gpgsign=false','commit','-m','Record chi192 p=.30480 branch-retention test')
new=git('rev-parse','HEAD',capture=True).strip()
# Refuse a race and never force; a normal push will fail if main moved.
git('push','origin','main')
remote_commit=git('ls-remote','origin','refs/heads/main',capture=True).split()[0]
if remote_commit!=new:raise SystemExit('Remote verification did not match the ordinary push')
receipt=dict(commit=new,remote_commit=remote_commit,remote_equals_local=True,ordinary_non_force_push=True,
 repository='MIKEAA2020/arena-max--physics',parent_commit=head,campaign=protocol['campaign'],status=campaign['status'],
 accepted_states=2,p=.3048,chi=192,full_state_checkpoints_retained=True,independent_audit=True,
 transition_order='unresolved',initial_serializer_attempt_preserved=True,
 protocol_sha256=digest(HERE/'branch192-protocol.json'),execution_addendum_sha256=digest(HERE/'branch192-execution-addendum.json'),
 retry_addendum_sha256=digest(HERE/'branch192-retry-addendum.json'),report_sha256=digest(HERE/'BRANCH192-RESULTS.md'),
 review_package_sha256=digest(ROOT/'papers/v33-review-package.zip'),license_unchanged=True,credential_scan='passed')
(ROOT/'handoff').mkdir(exist_ok=True)
(ROOT/'handoff/chi192-publication-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('CHI192_PUSH_VERIFIED',json.dumps(receipt),flush=True)
if __name__=='__main__':pass

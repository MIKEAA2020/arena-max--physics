#!/usr/bin/env python3
"""Publish authorized branch-pilot artifacts with existing history/license intact.
The persistent private credential is never copied; preparation scans exact
secrets and nested archives. No force-push or unreviewed remote overwrite.
"""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
R=ROOT/'v2.2/verify/replica';db=json.loads((R/'n3_branch128_pilot.json').read_text())
def run(args):subprocess.run(args,check=True,cwd=ROOT)
run([sys.executable,str(HERE/'branch128_pilot_report.py')])
run([sys.executable,str(ROOT/'papers/v34/revise_manuscript.py')])
run([sys.executable,str(HERE/'bundle_review.py')])
run([sys.executable,str(HERE/'prepare_publication.py')])
C=ROOT/'.arena/publish';env=os.environ.copy();env.update(GIT_ASKPASS=str(ROOT/'.private/github-askpass.py'),GIT_TERMINAL_PROMPT='0')
for k in ['GIT_TRACE','GIT_TRACE_PACKET','GIT_TRACE_CURL','GIT_CURL_VERBOSE']:env.pop(k,None)
def git(*args,capture=False):
 cmd=['git','-c','credential.helper=','-C',str(C),*args]
 return subprocess.check_output(cmd,text=True,env=env) if capture else subprocess.run(cmd,check=True,env=env)
git('fetch','--quiet','origin','main')
head=git('rev-parse','HEAD',capture=True).strip();remote=git('rev-parse','origin/main',capture=True).strip()
if head!=remote:
 check=subprocess.run(['git','-C',str(C),'merge-base','--is-ancestor',remote,head])
 if check.returncode:raise SystemExit('Remote changed; refuse automatic overwrite/rebase/force-push')
 git('push','origin','main')
assert not git('diff','--','LICENSE',capture=True)
git('add','--all')
if git('diff','--cached','--name-only',capture=True).strip():
 git('-c','user.name=Arena Research Assistant','-c','user.email=assistant@arena.invalid','-c','commit.gpgsign=false','commit','-m','Record unbiased chi128 branch-pilot progress: '+db['status'])
 git('push','origin','main')
a=git('rev-parse','HEAD',capture=True).strip();b=git('ls-remote','origin','refs/heads/main',capture=True).split()[0];assert a==b
receipt=dict(commit=a,remote_equals_local=True,ordinary_push=True,status=db['status'],stage_count=len(db.get('stages',{})),thermodynamic_order='unresolved')
(ROOT/'handoff').mkdir(exist_ok=True)
(ROOT/'handoff/branch128-publication-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('BRANCH_PUSH_VERIFIED',json.dumps(receipt),flush=True)

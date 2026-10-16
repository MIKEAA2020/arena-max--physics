#!/usr/bin/env python3
"""Recover an interrupted scan from real physical MPS checkpoints.
Original math/worker/protocol files stay unchanged. Calendar downtime is logged;
no tolerance relaxation, no fresh rerun of completed targets, no global extension.
"""
from pathlib import Path
import hashlib,json,os,subprocess,sys,threading,time,math,fcntl,shutil
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
R=ROOT/'v2.2/verify/replica';sys.path.insert(0,str(HERE))
import chi128_scan_campaign as base
H=base.H
TERMINAL={'accepted-finite-chi','accepted-stationary-at-finite-chi','budget-stopped',
          'iteration-cap-or-stationarity-check-failed','period-contraction-check-failed',
          'optimizer-or-validation-failed','unexpected-error','worker-exited-without-record',
          'worker-terminated-before-final-record'}


def main():
    (ROOT/'.arena').mkdir(exist_ok=True)
    lock=(ROOT/'.arena/scan128.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    master_path=HERE/'chi128-scan-protocol.json';master=json.loads(master_path.read_text())
    for name,digest in master['source_sha256'].items():assert base.digest(ROOT/name)==digest,name
    data_path=R/'n3_chi128_scan.json';db=json.loads(data_path.read_text())
    if db.get('status','').startswith(('complete','grid attempted')):raise SystemExit('Campaign already terminal; no rerun')
    if time.time()>master['campaign_deadline_unix']-180:raise SystemExit('Original campaign deadline leaves insufficient time; need a new allocation')
    db['status']='running: recovered after session interruption'
    if db.get('publication_error'):
        db.setdefault('publication_error_history',[]).append(db.pop('publication_error'))
    events=db.setdefault('recovery_events',[])
    recovery_index=len(events)+1
    event=dict(index=recovery_index,detected_at_unix=time.time(),reason='User requested continue; registered process absent and no campaign/worker PID active in restored workspace',global_deadline_unchanged=master['campaign_deadline_unix'],qualification='Checkpoint iteration/seconds are segment lower bounds; lost uncheckpointed work and session downtime are not disguised as converged results.')
    events.append(event);base.save(data_path,db)
    for p in master['priority_new_rates']:
        key=f'{p:.7f}';case=db.get('cases',{}).get(key,{})
        if case and all(case.get(s,{}).get('status') in TERMINAL for s in ['ordered','disordered']):
            for side in ['ordered','disordered']:base.verify_accepted(case[side])
            continue
        if time.time()>master['campaign_deadline_unix']-180:
            db['status']='remaining rates deferred at original authorized campaign deadline';break
        local_rows={};pending=[];interrupted=[]
        for side in ['ordered','disordered']:
            out=R/f'scan128_{side}_p{p:.7f}.json'
            r=json.loads(out.read_text()) if out.exists() else None
            if r and r.get('status') in TERMINAL:
                base.verify_accepted(r);local_rows[side]=r
            else:
                pending.append(side)
                if r:interrupted.append((side,r,out))
        point_master_path=master_path
        if interrupted:
            # Archive actual starting tensors and old segment records before overwrite.
            recovery_master=dict(master)
            recovery_master['campaign']=master['campaign']+f'-recovery-{recovery_index}-p{p:.7f}'
            recovery_master['original_master_sha256']=base.digest(master_path)
            recovery_master['original_preparations']=master['preparations']
            recovery_master['preparations']=dict(master['preparations'])
            recovery_master['recovery_qualification']='Continuation from saved physical MPS states; FL/FR caches recomputed as already documented. Prior segment times are not a total end-to-end cost.'
            history={}
            for side,r,out in interrupted:
                cp=R/r['checkpoint'];assert cp.exists(),'No physical checkpoint: do not substitute scalar JSON'
                state,meta=H.load_state(cp,operator='hermitian-halfrow')
                assert meta['p']==p and meta['chi']==128
                archived=R/'checkpoints'/f'scan128_{side}_p{p:.7f}_resume-source{recovery_index}.npz'
                if archived.exists():raise RuntimeError('Refusing overwrite of an immutable recovery source')
                shutil.copyfile(cp,archived)
                record=HERE/'scan128'/f'segment-{p:.7f}-{side}-before-recovery{recovery_index}.json'
                r['interruption_status']='interrupted before validation, not a converged observation'
                r['saved_checkpoint_metadata']=meta;r['saved_checkpoint_sha256']=base.digest(archived)
                base.save(record,r);out.unlink()
                recovery_master['preparations'][side]=dict(checkpoint=str(archived.relative_to(ROOT)),sha256=base.digest(archived),qualification='real partial state continuing the original fixed-source preparation, not a new independent phase')
                history[side]=dict(record=str(record.relative_to(ROOT)),saved_iters=meta.get('iters'),saved_seconds=meta.get('seconds'),saved_eps=meta.get('eps'))
            recovery_master['prior_segments']=history
            point_master_path=HERE/'scan128'/f'recovery-master-p{p:.7f}-{recovery_index}.json'
            base.save(point_master_path,recovery_master)
        # At most 80 min for recovery of a paused target; fresh targets retain 90.
        window=4800 if interrupted else 5400
        point=dict(p=p,master_protocol=str(point_master_path.relative_to(ROOT)),master_sha256=base.digest(point_master_path),deadline_unix=min(time.time()+window,master['campaign_deadline_unix']),recovery_event=recovery_index,original_global_deadline_unchanged=True)
        point_path=HERE/'scan128'/f'point-{p:.7f}-recovery{recovery_index}.json'
        base.save(point_path,point);print('RECOVERED_PAIR_START',p,'preparations',pending,'window_seconds',window,flush=True)
        children=[];threads=[]
        def relay(pipe,path,side):
            with path.open('w') as f:
                for line in pipe:
                    f.write(line);f.flush();print(f'[{p:.7f} {side}] '+line.rstrip(),flush=True)
        env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
        for side in pending:
            seconds=max(1,math.ceil(point['deadline_unix']-time.time()))
            args=['timeout','--signal=TERM','--kill-after=5s',str(seconds)+'s',sys.executable,'-u',str(R/'scan128_worker.py'),str(point_path),side]
            child=subprocess.Popen(args,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
            thread=threading.Thread(target=relay,args=(child.stdout,R/f'scan128_{side}_p{p:.7f}_recovery{recovery_index}.log',side),daemon=True)
            thread.start();threads.append(thread);children.append((side,child))
        for side,child in children:
            code=child.wait();out=R/f'scan128_{side}_p{p:.7f}.json'
            r=json.loads(out.read_text()) if out.exists() else dict(p=p,chi=128,preparation=side,status='worker-exited-without-record',converged=False)
            if r.get('status') not in TERMINAL:r.update(status='worker-terminated-before-final-record',converged=False)
            r['process_exit_code']=code;r['recovery_event']=recovery_index
            if interrupted:r['prior_segment_history']=str(point_master_path.relative_to(ROOT))
            base.verify_accepted(r);base.save(out,r);local_rows[side]=r
        for thread in threads:thread.join()
        local_rows['comparison']=base.fidelity(local_rows['ordered'],local_rows['disordered'],point['deadline_unix'])
        local_rows['reused_verified_reference']=False;local_rows['recovery_event']=recovery_index
        db['cases'][key]=local_rows
        base.save(R/f'scan128_comparison_p{p:.7f}.json',local_rows['comparison']);base.save(data_path,db)
        print('RECOVERED_PAIR_DONE',p,json.dumps({s:local_rows[s]['status'] for s in ['ordered','disordered']}),flush=True)
        try:base.publish(db)
        except Exception as exc:
            db['publication_error']=f'{type(exc).__name__}: {exc}';base.save(data_path,db);print('PUBLICATION_PENDING',db['publication_error'],flush=True)
    else:
        good=sum(c.get(s,{}).get('converged') is True for c in db['cases'].values() for s in ['ordered','disordered'])
        db['status']='complete: all 12 preparation results accepted' if good==12 else 'grid attempted: some preparations not accepted'
    db['completed_at_unix']=time.time();base.save(data_path,db)
    try:base.publish(db)
    except Exception as exc:
        db['publication_error']=f'{type(exc).__name__}: {exc}';base.save(data_path,db);print('PUBLICATION_PENDING',db['publication_error'],flush=True)
    print('SCAN_DONE',json.dumps(dict(status=db['status'],rates=len(db['cases']),phase_order='unresolved')),flush=True)


if __name__=='__main__':main()

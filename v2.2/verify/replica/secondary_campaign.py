#!/usr/bin/env python3
"""Feasibility-first secondary queue; one BLAS thread, one worker.
Modes: d3-exact, d3-mps, n4-mps, clifford8. Each completed case is atomic.
Pilots/finite-size crossings are not thermodynamic transition-order certificates.
"""
from pathlib import Path
import os,sys,time,json,signal,resource
import numpy as np
from scipy.sparse.linalg import eigsh,LinearOperator
from scipy.optimize import brentq
from replica_tm import ReplicaTM
import replica_halfrow as H
import clifford4_transfer as F

def save(path,db):
    path=Path(path);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(db,indent=2));tmp.replace(path)
def read(path,default):return json.loads(Path(path).read_text()) if Path(path).exists() else default


def d3exact():
    path='n3_d3_exact.json';db=read(path,dict(cases={},crossings=[]));cases=db['cases']
    def levels(L,p):
        key=f'L{L}:p{p:.9f}'
        if key in cases:return cases[key]
        t0=time.time();tm=ReplicaTM(3,3,L,p);out=dict(n=3,d=3,L=L,p=p)
        for s in ['triv','std','sgn']:
            P=tm.projector(colour=s,k0=True)
            mv=lambda x:P(tm.apply_S(P(x))).ravel()
            op=LinearOperator((tm.dim,tm.dim),matvec=mv,dtype=float)
            x=P(np.random.default_rng(81+L).normal(size=tm.shape)).ravel();x/=np.linalg.norm(x)
            w,v=eigsh(op,k=2 if s=='triv' else 1,which='LA',v0=x,ncv=12,tol=1e-10,maxiter=2000)
            ix=np.argsort(w)[::-1];w=w[ix];v=v[:,ix]
            out[s]=w.tolist();out[s+'_residuals']=[float(np.linalg.norm(mv(v[:,j])-w[j]*v[:,j])) for j in range(len(w))]
        out['X_std']=float(L*np.log(out['triv'][0]/out['std'][0]));out['X_sgn']=float(L*np.log(out['triv'][0]/out['sgn'][0]))
        out['f_b_finite']=float(-np.log(out['triv'][0])/(L/2));out['seconds']=time.time()-t0
        cases[key]=out;save(path,db);print('EXACT',key,'Xs',out['X_std'],'Xg',out['X_sgn'],'seconds',out['seconds'],flush=True)
        return out
    ps=[.2,.3,.4,.5,.6,.7,.8]
    for L in [4,6,8]:
        for p in ps:levels(L,p)
    for s in ['std','sgn']:
        field='X_'+s
        for L,M in [(4,6),(6,8)]:
            ds=[levels(L,p)[field]-levels(M,p)[field] for p in ps]
            found=False
            for p,q,a,b in zip(ps,ps[1:],ds,ds[1:]):
                if a*b<0:
                    root=brentq(lambda p:levels(L,p)[field]-levels(M,p)[field],p,q,xtol=3e-6)
                    row=dict(sector=s,L=L,M=M,p_star=float(root),root_xtol=3e-6,interpretation='finite-size crossing; not asymptotic pc')
                    if not any(r['sector']==s and r['L']==L and r['M']==M for r in db['crossings']):db['crossings'].append(row)
                    save(path,db);print('CROSSING',json.dumps(row),flush=True);found=True;break
            if not found:print('NO BRACKET',s,L,M,ds,flush=True)
    return db


def d3mps():
    ex=read('n3_d3_exact.json',{})
    roots=[r['p_star'] for r in ex.get('crossings',[]) if r['sector']=='std' and r['M']==8]
    if not roots:raise RuntimeError('Exact-location prerequisite absent')
    center=roots[-1];lo=max(.01,center-.04);hi=min(.99,center+.06)
    path='n3_d3_mps_pilot.json';db=read(path,{})
    # Deliberately a pilot: two opposite preparations and small-chi checks.
    for side,ps in [('up',[lo,center,hi]),('down',[hi,center,lo])]:
        st=None
        for ip,p in enumerate(ps):
            failed=False
            for chi in ([12,24] if ip==0 else [24]):
                key=f'{side}:p{p:.8f}:chi{chi}';cp=f'checkpoints/n3_d3_{side}_latest.npz'
                try:
                    st,r=H.solve(3,3,p,chi,init=st,tol=1e-7,maxiter=200,checkpoint_path=cp,tag='d3-'+side,verbose=False)
                    r['tol']=1e-7;r['converged']=bool(r['eps']<1e-7);r['status']='pilot-converged' if r['converged'] else 'pilot-maxiter-unconverged'
                    db[key]=r;save(path,db);print('D3_MPS',key,json.dumps(r),flush=True)
                    if not r['converged']:failed=True;break
                except RuntimeError as e:
                    db[key]=dict(status='budget-stopped',reason=str(e),checkpoint=cp);save(path,db);print('D3_STOP',key,str(e),flush=True);failed=True;break
            if failed:break
            # Only accepted stages advance the continued pilot branch.
    return db


def n4mps():
    path='n4_haar_half_pilot.json';db=read(path,{})
    st,r=H.solve(4,2,1.,4,tol=1e-8,maxiter=80,checkpoint_path='checkpoints/n4_haar_p1.npz',tag='endpoint',verbose=False)
    r['f_exact']=-2*np.log(4/35);r['converged']=bool(r['eps']<1e-8);r['endpoint_error']=r['f']-r['f_exact']
    db['p1:chi4']=r;save(path,db);print('N4_ENDPOINT',json.dumps(r),flush=True)
    if not r['converged'] or abs(r['endpoint_error'])>1e-7:raise RuntimeError('n4 endpoint prerequisite failed')
    try:
        st,r=H.solve(4,2,.38,4,init=None,tol=1e-7,maxiter=120,checkpoint_path='checkpoints/n4_haar_p038.npz',tag='pilot',verbose=True)
        r['converged']=bool(r['eps']<1e-7);r['tol']=1e-7;db['p.38:chi4']=r;save(path,db);print('N4_PILOT',json.dumps(r),flush=True)
    except RuntimeError as e:
        db['p.38:chi4']=dict(status='budget-stopped',reason=str(e),checkpoint='checkpoints/n4_haar_p038.npz');save(path,db);print('N4_STOP',str(e),flush=True)
    return db


def clifford8():
    path='clifford4_L8_budgeted.json';db=read(path,dict(cases={}))
    tm=F.MomentTM(8,.36);rng=np.random.default_rng(418)
    def P(x,s='triv'):return tm.project_momentum0(tm.project_colour(x,s))
    v=P(rng.normal(size=tm.shape));v/=np.linalg.norm(v)
    t0=time.time();y=P(tm.apply_S(P(v)));seconds=time.time()-t0
    db['benchmark']=dict(L=8,ensemble='clifford',one_projected_matvec_seconds=seconds,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save(path,db);print('L8_BENCHMARK',json.dumps(db['benchmark']),flush=True)
    del tm,v,y
    # Do not blindly launch an entire expensive ladder from one small-L timing.
    ceiling=float(os.environ.get('L8_MATVEC_CEILING','1.0'))
    if seconds>ceiling:
        db['status']='deferred-after-runtime-benchmark';save(path,db);return db
    def alarm(signum,frame):raise TimeoutError('finite-case wall budget exhausted')
    signal.signal(signal.SIGALRM,alarm)
    for p in [.35,.36,.37]:
        key=f'{p:.6f}';row=db['cases'].get(key,dict(L=8,p=p,ensemble='clifford'))
        for s in ['triv','std']:
            if s in row:continue
            try:
                signal.alarm(int(os.environ.get('L8_SECTOR_SECONDS','180')))
                t0=time.time();r=F.levels(8,p,'clifford',sectors=(s,),tol=2e-9)
                row.update(r);row[s+'_seconds']=time.time()-t0
                row['maxrss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            except TimeoutError as e:
                row['status']='budget-stopped';row['reason']=str(e);db['cases'][key]=row;save(path,db);print('L8_STOP',key,s,flush=True);return db
            finally:signal.alarm(0)
            if 'triv' in row:
                row['f_b_finite']=float(-np.log(row['triv'][0])/4)
                if 'std' in row:row['X_std']=float(8*np.log(row['triv'][0]/row['std'][0]))
            db['cases'][key]=row;save(path,db);print('L8_CASE',key,s,json.dumps(row),flush=True)
    db['status']='requested-three-point-pilot-complete';save(path,db);return db

if __name__=='__main__':
    mode=sys.argv[1]
    {'d3-exact':d3exact,'d3-mps':d3mps,'n4-mps':n4mps,'clifford8':clifford8}[mode]()

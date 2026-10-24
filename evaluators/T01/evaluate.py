#!/usr/bin/env python3
"""Independent T01 evaluator. Trusted infrastructure only; no model calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import uuid

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from t01_harness_smoke import project_candidate

TAGS={k:'guild-ledger-t01-'+k+':local' for k in ('guild','armory','web')}
TAGS['judge']='guild-ledger-t01-acceptance:local'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def version():
    files=[HERE/'criteria.json',Path(__file__),ROOT/'scripts/t01_harness_smoke.py',ROOT/'scripts/package_benchmark.py',*sorted((HERE/'runner').glob('*'))]
    return hashlib.sha256(json.dumps({p.relative_to(ROOT).as_posix():sha(p) for p in files if p.is_file()},sort_keys=True).encode()).hexdigest()

def command(args,log,timeout=180):
    log.parent.mkdir(parents=True,exist_ok=True)
    try:
        with log.open('w') as stream:
            p=subprocess.run(args,stdout=stream,stderr=subprocess.STDOUT,text=True,timeout=timeout)
        return p.returncode
    except subprocess.TimeoutExpired:
        with log.open('a') as stream:stream.write('\nSUPERVISOR_TIMEOUT\n')
        raise

def build(output):
    output.mkdir(parents=True,exist_ok=True)
    commands=[('guild',['-f',str(ROOT/'benchmarks/T01/starter/services/guild/Dockerfile'),str(ROOT/'benchmarks/T01/starter')]),('armory',[str(ROOT/'benchmarks/T01/starter/services/armory')]),('web',[str(ROOT/'benchmarks/T01/starter/web')]),('judge',['--build-arg','EVALUATOR_SHA256='+version(),str(HERE/'runner')])]
    for name,args in commands:
        if command(['docker','build','-t',TAGS[name],*args],output/(name+'.log'),900):raise RuntimeError('Image build failed: '+name)

def aggregate(observations,only):
    inventory=json.loads((HERE/'criteria.json').read_text())
    expected={c['id']:c for c in inventory['criteria'] if not only or c['id'] in only}
    results=observations.get('results',[])
    if observations.get('status')!='completed' or len(results)!=len(expected) or {r.get('id') for r in results}!=set(expected):raise ValueError('Incomplete or invalid evaluator observations')
    for result in results:
        if result.get('status') not in ('pass','fail') or result.get('requirements')!=expected[result['id']]['requirements']:raise ValueError('Invalid criterion outcome')
    return {'evaluation_complete':not only,'full_target_acceptance':all(r['status']=='pass' for r in results) if not only else None,'diagnostic_passed':all(r['status']=='pass' for r in results),'passed_criteria':sum(r['status']=='pass' for r in results),'evaluated_criteria':len(results),'full_target_denominator':len(inventory['criteria']),'communicated_conformance':None,'exposure_audit_status':'draft; independent audit required','results':results}

def evaluate(candidate,output,only=()):
    candidate=Path(candidate).absolute();output=Path(output).absolute()
    if output.exists():raise ValueError('Evidence output must be new')
    if output.is_relative_to(candidate):raise ValueError('Evidence must be outside candidate')
    inventory=json.loads((HERE/'criteria.json').read_text());known={c['id'] for c in inventory['criteria']}
    if len(set(only))!=len(only) or set(only)-known:raise ValueError('Unknown or repeated criteria')
    output.mkdir(parents=True)
    report={'schema':'guild-ledger.t01-acceptance/v1','task':'T01','evaluator_sha256':version(),'status':'running','full_target_acceptance':None,'model_calls':0,'model_usage':None,'cost_usd':None,'live_model_calls_enabled':False,'selected_criteria':list(only),'coverage_limits':inventory['coverage_limits']}
    token='t01-accept-'+uuid.uuid4().hex;network=token+'-net';created_network=False;services=[]
    started=time.monotonic()
    try:
        with tempfile.TemporaryDirectory(prefix='t01-accept-') as temp:
            temp=Path(temp);application=temp/'application'
            try:report['application_sha256']=project_candidate(candidate,ROOT/'benchmarks/T01/starter',application)
            except ValueError as exc:
                report.update(status='invalid_candidate',full_target_acceptance=False,required_input_gate_passed=False,input_error=str(exc));return report
            report['required_input_gate_passed']=True
            images={name:json.loads(subprocess.check_output(['docker','image','inspect',tag],text=True))[0] for name,tag in TAGS.items()}
            if images['judge']['Config'].get('Labels',{}).get('io.guild-ledger.evaluator-sha256')!=version():raise ValueError('Evaluator image/source digest mismatch; rebuild required')
            report['images']={name:{'id':info['Id'],'platform':info['Os']+'/'+info['Architecture']} for name,info in images.items()}
            inputs=temp/'inputs';inputs.mkdir();fixture=ROOT/'benchmarks/T01/starter/fixtures/quests.json'
            (inputs/'quests.json').write_bytes(fixture.read_bytes());report['fixture_sha256']=sha(fixture)
            common=['--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','256','--memory','2g','--cpus','2','--user','10001:10001','--tmpfs','/tmp:rw,nosuid,nodev,mode=1777']
            def mount(path,target):return ['--mount',f'type=bind,src={path},dst={target},readonly']
            build_args=['docker','run','--rm','--label','io.guild-ledger.acceptance='+token,'--network','none',*common,*mount(application/'web/src','/app/src'),'--tmpfs','/app/dist:rw,uid=10001,gid=10001','--tmpfs','/app/node_modules/.vite:rw,uid=10001,gid=10001','--tmpfs','/app/node_modules/.vite-temp:rw,uid=10001,gid=10001',images['web']['Id'],'npm','run','build']
            build_exit=command(build_args,output/'candidate-build.log',90)
            if build_exit in (125,126,127):raise RuntimeError('Build checker failed to launch')
            report['required_build_gate_passed']=build_exit==0
            if build_exit:
                report.update(status='candidate_build_failure',full_target_acceptance=False);return report
            if command(['docker','network','create','--internal',network],output/'network.log'):raise RuntimeError('Network setup failed')
            created_network=True
            if not json.loads(subprocess.check_output(['docker','network','inspect',network],text=True))[0]['Internal']:raise RuntimeError('Private network required')
            for name in ('guild','armory','web'):
                container=token+'-'+name;services.append(container)
                args=['docker','run','-d','--name',container,'--network',network,'--network-alias',name,*common]
                if name=='guild':args+=mount(application/'services/guild/app.py','/app/app.py')
                if name=='web':args+=mount(application/'web/src','/app/src')+['--tmpfs','/app/node_modules/.vite:rw,uid=10001,gid=10001','--tmpfs','/app/node_modules/.vite-temp:rw,uid=10001,gid=10001','-e','GUILD_PROXY_TARGET=http://guild:8000','-e','__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS=web']
                if command(args+[images[name]['Id']],output/(name+'-start.log')):raise RuntimeError('Service launch failed: '+name)
            # Readiness tests only server transport; /health behavior is a scored criterion.
            ready_script="import socket,urllib.request; urllib.request.urlopen('http://web:5173',timeout=2); socket.create_connection(('guild',8000),2).close()"
            for attempt in range(30):
                code=command(['docker','run','--rm','--label','io.guild-ledger.acceptance='+token,'--network',network,*common,'--entrypoint','python',images['guild']['Id'],'-c',ready_script],output/'readiness.log',20)
                if code in (125,126,127):raise RuntimeError('Readiness probe failed to launch')
                if not code:break
                time.sleep(.25)
            else:
                report.update(status='candidate_unavailable',full_target_acceptance=False);return report
            judge=token+'-judge';services.append(judge)
            args=['docker','create','--name',judge,'--network',network,*common,*mount(inputs,'/inputs'),'-e','CRITERIA='+json.dumps(list(only)),images['judge']['Id']]
            if command(args,output/'judge-create.log'):raise RuntimeError('Evaluator container launch failed')
            code=command(['docker','start','--attach',judge],output/'observations.log',240)
            state=json.loads(subprocess.check_output(['docker','inspect',judge],text=True))[0]['State']
            if code or state['ExitCode']:raise RuntimeError('Evaluator process failed; see observations.log')
            lines=(output/'observations.log').read_text().splitlines()
            records=[json.loads(line) for line in lines if line.startswith('{')]
            if len(records)!=1:raise ValueError('Expected one evaluator observation record')
            report.update(aggregate(records[0],only),status='completed',browser=records[0].get('browser'))
    except Exception as exc:
        report.update(status='evaluator_error',full_target_acceptance=None,error=repr(exc))
    finally:
        cleanup=[]
        for name in services:
            command(['docker','logs',name],output/(name.removeprefix(token+'-')+'-service.log'))
            cleanup.append(command(['docker','rm','--force',name],output/(name.removeprefix(token+'-')+'-cleanup.log'))==0)
        residual=subprocess.check_output(['docker','ps','--all','--quiet','--filter','label=io.guild-ledger.acceptance='+token],text=True).split()
        if residual:cleanup.append(command(['docker','rm','--force',*residual],output/'probe-cleanup.log')==0)
        if created_network:cleanup.append(command(['docker','network','rm',network],output/'network-cleanup.log')==0)
        report['cleanup_passed']=all(cleanup)
        if not all(cleanup):report.update(status='evaluator_error',full_target_acceptance=None,error='Container/network cleanup failed')
        report['seconds']=round(time.monotonic()-started,3)
        (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--candidate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--only',nargs='+',default=[]);p.add_argument('--build',action='store_true');args=p.parse_args()
    if args.build:build(args.output.absolute().parent/(args.output.name+'-build'))
    r=evaluate(args.candidate,args.output,args.only);print(json.dumps(r,indent=2))
    sys.exit(2 if r['status']=='evaluator_error' else 0 if r.get('diagnostic_passed') else 1)

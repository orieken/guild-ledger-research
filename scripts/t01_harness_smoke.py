#!/usr/bin/env python3
"""Trusted T01 no-model harness/test supervisor. No Docker access in workers."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import uuid
from package_benchmark import ROOT, package

IMAGES={name:'guild-ledger-t01-'+name+':local' for name in ('guild','armory','web','probe','harness2','claude','loom')}
EDITABLE=('web/src/','services/guild/app.py')
REGISTRY={r['harness_id']:r for r in json.loads((ROOT/'harness-packages.json').read_text())['entries']}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def execute(args,log,timeout=180,check=True):
    log=Path(log);log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('w') as stream:
        p=subprocess.run(args,stdout=stream,stderr=subprocess.STDOUT,text=True,timeout=timeout)
    if check and p.returncode:raise RuntimeError(f'Command failed ({p.returncode}); see {log}')
    return p.returncode,log.read_text()

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def identity(image):return json.loads(subprocess.check_output(['docker','image','inspect',image],text=True))[0]

def worker(image,task,prompt,output):
    """Dedicated H4 T01 adapter; native core in a non-root/no-network worker."""
    info=identity(image)
    if 'RUNNER_KIND=harness2-deterministic' not in info['Config'].get('Env',[]) or info['Config'].get('Labels',{}).get('io.guild-ledger.profile-sha256')!=REGISTRY['H4']['manifest_sha256']:
        raise ValueError('Pinned deterministic H4 image required')
    output.mkdir();name='t01-h4-'+uuid.uuid4().hex
    uid=os.getuid() if sys.platform.startswith('linux') and os.getuid()>0 else 10001
    gid=os.getgid() if sys.platform.startswith('linux') and os.getgid()>0 else 10001
    record={'synthetic':True,'model_calls':0,'image_id':info['Id'],'network':'none','worker_uid':uid,'worker_gid':gid,'prompt_sha256':sha(prompt),'stop_reason':'running'}
    try:
        with tempfile.TemporaryDirectory(prefix='t01-h4-') as temp:
            temp=Path(temp);work=temp/'workspace';work.mkdir();work.chmod(0o777)
            inputs=temp/'inputs';inputs.mkdir();shutil.copyfile(prompt,inputs/'prompt.txt')
            args=['docker','create','--name',name,'--init','--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','256','--memory','1g','--cpus','2','--user',f'{uid}:{gid}','--tmpfs',f'/home/runner:rw,uid={uid},gid={gid},mode=0700','--tmpfs','/tmp:rw,nosuid,nodev,mode=1777','--mount',f'type=bind,src={task},dst=/task,readonly','--mount',f'type=bind,src={inputs},dst=/inputs,readonly','--mount',f'type=bind,src={work},dst=/workspace',info['Id']]
            if 'T01_OFFLINE_TOOLS=1' in info['Config'].get('Env',[]):
                args[-1:-1]=['--tmpfs',f'/opt/t01-run:rw,exec,nosuid,nodev,uid={uid},gid={gid},mode=0700']
            execute(args,output/'create.log')
            execute(['docker','start','--attach',name],output/'runtime.log',120)
            state=json.loads(subprocess.check_output(['docker','inspect',name],text=True))[0]['State']
            if state['ExitCode']!=0:raise RuntimeError('H4 worker failed')
            shutil.copytree(work,output/'workspace',symlinks=True)
            report=json.loads((work/'report.json').read_text())
            if not report['source_unchanged'] or report['task_prompt_sha256']!=sha(prompt):raise ValueError('H4 transport mismatch')
            record.update(stop_reason='completed',native=report)
    finally:
        subprocess.run(['docker','rm','--force',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
        (output/'attempt.json').write_text(json.dumps(record,indent=2)+'\n')
    return output/'workspace/candidate',record

def project_candidate(source,canonical,target):
    """Export application bytes only; never execute candidate test/infra changes."""
    if source.is_symlink():raise ValueError('Candidate root must be regular')
    frontend=source/'web/src'
    if frontend.is_symlink() or not frontend.is_dir():raise ValueError('Regular frontend source directory required')
    target.mkdir()
    files={p.relative_to(canonical).as_posix() for p in canonical.rglob('*') if p.is_file()}
    def read(relative):
        path=source/relative
        if any(p.is_symlink() for p in [path,*path.parents] if p==source or source in p.parents):raise ValueError('Candidate symlink rejected')
        if not path.is_file():raise ValueError('Missing canonical input: '+relative)
        return path.read_bytes()
    for relative in sorted(files):
        path=source/relative
        if relative.startswith('web/src/') and not path.exists() and not path.is_symlink():continue
        data=read(relative)
        editable=any(relative==p or relative.startswith(p) for p in EDITABLE)
        if not editable and data!=(canonical/relative).read_bytes():raise ValueError('Protected input changed: '+relative)
        destination=target/relative;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data)
    (target/'web/src').mkdir(parents=True,exist_ok=True)
    for path in (source/'web/src').rglob('*'):
        if path.is_symlink() or (not path.is_dir() and not path.is_file()):raise ValueError('Unsafe new source path')
        if path.is_file():
            destination=target/path.relative_to(source);destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(path.read_bytes())
    return {p.relative_to(target).as_posix():sha(p) for p in sorted(target.rglob('*')) if p.is_file()}

def validate_acceptance(report,evaluator,files):
    """Fail closed on judge errors, missing criteria, or a different candidate.

    These no-op fixtures must reject the unfinished product while completing all
    acceptance observations. This expectation is not a live-run scoring rule.
    """
    if report.get('schema')!='guild-ledger.t01-acceptance/v1' or report.get('status')!='completed':
        raise ValueError('Independent acceptance evaluation did not complete')
    if report.get('evaluator_sha256')!=evaluator.version() or report.get('application_sha256')!=files:
        raise ValueError('Acceptance evaluator/candidate identity mismatch')
    if (report.get('model_calls')!=0 or report.get('live_model_calls_enabled') is not False
            or report.get('cleanup_passed') is not True or report.get('selected_criteria')!=[]
            or report.get('required_input_gate_passed') is not True
            or report.get('required_build_gate_passed') is not True):
        raise ValueError('Acceptance isolation, gates, or cleanup not verified')
    score=evaluator.aggregate({'status':'completed','results':report.get('results',[])},[])
    for key,value in score.items():
        if report.get(key)!=value:raise ValueError('Acceptance score mismatch: '+key)
    failed={item['id'] for item in score['results'] if item['status']=='fail'}
    if score['full_target_acceptance'] is not False or not {'A01','U01'}<=failed:
        raise ValueError('Expected unfinished mock candidate acceptance rejection')
    return True

def test_candidate(candidate,output,expect_features):
    """Only trusted fixed images/tests, source read-only; private internal network."""
    output.mkdir();token='t01-test-'+uuid.uuid4().hex;network=token+'-net';containers=[];checks=[]
    common=['--label','io.guild-ledger.t01-test='+token,'--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','256','--memory','1g','--cpus','2','--user','10001:10001','--tmpfs','/tmp:rw,nosuid,nodev,mode=1777']
    webtmp=['--tmpfs','/app/dist:rw,uid=10001,gid=10001','--tmpfs','/app/node_modules/.vite:rw,uid=10001,gid=10001','--tmpfs','/app/node_modules/.vite-temp:rw,uid=10001,gid=10001']
    def mount(path,dst):return ['--mount',f'type=bind,src={path},dst={dst},readonly']
    source_mounts={'guild':mount(candidate/'services/guild/app.py','/app/app.py'),'web':mount(candidate/'web/src','/app/src'),'armory':[]}
    env=['-e','GUILD_URL=http://guild:8000','-e','ARMORY_URL=http://armory:8001','-e','WEB_URL=http://web:5173']
    def probe(label,pattern,expected=0):
        args=['docker','run','--rm','--network',network,*common,*env,IMAGES['probe'],'-p',pattern,'-v']
        code,text=execute(args,output/(label+'.log'),check=False)
        return code,text
    try:
        execute(['docker','network','create','--internal',network],output/'network.log')
        net=json.loads(subprocess.check_output(['docker','network','inspect',network],text=True))[0]
        if not net['Internal']:raise ValueError('Private test network required')
        for service in ('guild','armory','web'):
            name=token+'-'+service;containers.append(name)
            args=['docker','run','-d','--name',name,'--network',network,'--network-alias',service,*common,*source_mounts[service]]
            if service=='web':args += webtmp+['-e','GUILD_PROXY_TARGET=http://guild:8000','-e','__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS=web']
            execute(args+[IMAGES[service]],output/(service+'-start.log'))
        for attempt in range(30):
            code,text=probe('startup', 'test_startup.py')
            if code==0:break
            time.sleep(1)
        checks.append({'check':'startup','passed':code==0,'exit_code':code})
        if code:raise RuntimeError('Application startup failed')
        code,text=probe('api','test_quests.py')
        passed=code==0 if expect_features else code!=0 and bool(re.search(r'FAILED \(failures=4\)',text))
        checks.append({'check':'visible-api','passed':passed,'exit_code':code,'expected':'green' if expect_features else '4 assertion failures'})
        for label,command in [('ui',['npm','test','--','--run']),('build',['npm','run','build'])]:
            code,text=execute(['docker','run','--rm','--network','none',*common,*webtmp,*source_mounts['web'],'-e','NO_COLOR=1',IMAGES['web'],*command],output/(label+'.log'),check=False)
            passed=code==0 if label=='build' or expect_features else code!=0 and bool(re.search(r'Tests\s+2 failed',text))
            checks.append({'check':label,'passed':passed,'exit_code':code,'expected':'green' if label=='build' or expect_features else '2 assertion failures'})
    finally:
        for name in containers:
            execute(['docker','logs',name],output/(name.split(token+'-')[-1]+'-service.log'),check=False)
            execute(['docker','rm','--force',name],output/(name.split(token+'-')[-1]+'-cleanup.log'),check=False)
        # A timed-out Docker client can leave its probe container running.
        residual=subprocess.check_output(['docker','ps','--all','--quiet','--filter','label=io.guild-ledger.t01-test='+token],text=True).split()
        if residual:execute(['docker','rm','--force',*residual],output/'probe-cleanup.log',check=False)
        cleanup,_=execute(['docker','network','rm',network],output/'network-cleanup.log',check=False)
        result={'checks':checks,'passed':len(checks)==4 and all(c['passed'] for c in checks) and cleanup==0,'agent_network':'none','test_network_internal':True,'ports_published':False,'test_inputs':'fixed image tests and infrastructure; candidate source only'}
        (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def worker_positive(candidate,output):
    """Green control for the same common in-worker tool/dependencies."""
    output.mkdir();name='t01-worker-positive-'+uuid.uuid4().hex
    args=['docker','create','--name',name,'--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','256','--memory','2g','--cpus','2','--user','10001:10001','--tmpfs','/home/runner:rw,uid=10001,gid=10001,mode=0700','--tmpfs','/tmp:rw,nosuid,nodev,mode=1777','--tmpfs','/opt/t01-run:rw,exec,nosuid,nodev,uid=10001,gid=10001,mode=0700','--mount',f'type=bind,src={candidate},dst=/workspace,readonly','--entrypoint','python3',IMAGES['claude'],'/opt/t01/visible_checks.py']
    try:
        execute(args,output/'create.log')
        code,text=execute(['docker','start','--attach',name],output/'tool.log',120,check=False)
        state=json.loads(subprocess.check_output(['docker','inspect',name],text=True))[0]['State']
        events=[json.loads(line) for line in text.splitlines() if line.startswith('{')]
        passed=code==0 and state['ExitCode']==0 and len(events)==1 and events[0].get('all_visible_passed') is True
        result={'passed':passed,'checks':events[0]['checks'] if events else [],'network':'none','image_id':IMAGES['claude']}
        (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
        return result
    finally:
        subprocess.run(['docker','rm','--force',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)

def build(output):
    commands=[('claude',['--target','smoke','-t','guild-ledger-claude-smoke:local','containers/claude']),('loom',['-t','guild-ledger-loom-mock:local','containers/loom']),('harness2',['-t','guild-ledger-harness2-demo:local','containers/harness2']),('guild',['-t',IMAGES['guild'],'-f','benchmarks/T01/starter/services/guild/Dockerfile','benchmarks/T01/starter']),('armory',['-t',IMAGES['armory'],'benchmarks/T01/starter/services/armory']),('web',['-t',IMAGES['web'],'benchmarks/T01/starter/web']),('probe',['-t',IMAGES['probe'],'-f','containers/t01/Dockerfile.probe','benchmarks/T01/starter']),('tools-claude',['--target','claude','-t',IMAGES['claude'],'-f','containers/t01/Dockerfile.worker','.']),('tools-loom',['--target','loom','-t',IMAGES['loom'],'-f','containers/t01/Dockerfile.worker','.']),('tools-h4',['--target','harness2','-t',IMAGES['harness2'],'-f','containers/t01/Dockerfile.worker','.'])]
    for name,args in commands:
        if name.startswith('tools-'):args=['--build-arg','T01_PROFILE_SHA256='+sha(ROOT/'containers/t01/profile.json'),*args]
        print('Build '+name,flush=True);execute(['docker','build',*args],output/(name+'.log'),600)
    module('t01_acceptance_build',ROOT/'evaluators/T01/evaluate.py').build(output/'acceptance')

def run(output,levels,build_images=False):
    if output.exists():raise ValueError('Output directory must be new')
    output.mkdir(parents=True)
    if build_images:build(output/'build')
    sys.path.insert(0,str(ROOT/'containers/claude'))
    claude=module('t01_claude',ROOT/'containers/claude/run.py');h2=module('t01_h2',ROOT/'containers/claude/h2.py');loom=module('t01_loom',ROOT/'containers/loom/run.py')
    images={name:identity(image)['Id'] for name,image in IMAGES.items()}
    overlay_digest=sha(ROOT/'containers/t01/profile.json')
    for role in ('claude','loom','harness2'):
        if identity(IMAGES[role])['Config'].get('Labels',{}).get('io.guild-ledger.t01-profile-sha256')!=overlay_digest:
            raise ValueError('T01 overlay profile/image mismatch: '+role)
    IMAGES.update(images)  # Resolve tags once; every worker/service uses recorded image IDs.
    evaluator=module('t01_acceptance',ROOT/'evaluators/T01/evaluate.py')
    cells=[];controls={};starter_hashes=set()
    try:
        for level in levels:
            bundle=output/('bundle-'+level);manifest=package(level,bundle);starter_hashes.add(manifest['starter_sha256'])
            task=bundle/'workspace';prompt=bundle/'prompt.txt'
            if level==levels[0]:
                positive=output/'positive-source';project_candidate(task,task,positive)
                shutil.copyfile(ROOT/'benchmarks/T01/validation/visible-reference.py',positive/'services/guild/app.py')
                shutil.copyfile(ROOT/'benchmarks/T01/validation/visible-reference.vue',positive/'web/src/App.vue')
                controls['positive']=test_candidate(positive,output/'positive-tests',True)
                controls['worker-positive']=worker_positive(positive,output/'positive-worker')
                for label,path in [('protected-test','tests/test_quests.py'),('source-symlink','web/src/App.vue')]:
                    with tempfile.TemporaryDirectory() as temp:
                        temp=Path(temp);bad=temp/'bad';shutil.copytree(task,bad)
                        if label=='protected-test':(bad/path).write_text('tampered')
                        else:(bad/path).unlink();(bad/path).symlink_to('/etc/passwd')
                        try:project_candidate(bad,task,temp/'projected')
                        except ValueError:controls[label]={'passed':True}
                        else:controls[label]={'passed':False}
            for hid in ('H0','H1','H2','H3','H4'):
                started=time.monotonic()
                print(level+' '+hid,flush=True);cell=output/level/hid;cell.mkdir(parents=True)
                record={'level':level,'harness':hid,'starter_sha256':manifest['starter_sha256'],'prompt_sha256':manifest['prompt_sha256'],'synthetic':True,'model_calls':0,'passed':False}
                try:
                    if hid in ('H0','H1'):
                        entry=REGISTRY.get(hid)
                        runtime=claude.run(IMAGES['claude'],task,prompt,cell/'runtime',harness=ROOT/entry['local_package'] if entry else None,harness_digest=entry['manifest_sha256'] if entry else None,harness_id=hid,timeout=120)
                        if runtime.get('exit_code')!=0 or runtime.get('timed_out'):raise RuntimeError('Mock worker failed')
                        candidate=cell/'runtime/workspace'
                    elif hid=='H2':
                        entry=REGISTRY[hid];runtime=h2.execute(image=IMAGES['claude'],task=task,prompt=prompt,output=cell/'runtime',harness=ROOT/entry['local_package'],harness_digest=entry['manifest_sha256'],fixture='repair',wall_seconds=120)
                        if runtime['stop_reason']!='completed' or [s['stage_id'] for s in runtime['stages']]!=['implementation','review','repair']:raise RuntimeError('H2 mock flow failed')
                        candidate=cell/'runtime/candidate'
                    elif hid=='H3':
                        entry=REGISTRY[hid];runtime=loom.execute(IMAGES['loom'],task,ROOT/entry['local_package'],entry['manifest_sha256'],cell/'runtime',fixture_approvals=True,prompt=prompt,wall_seconds=120)
                        if runtime['stop_reason']!='completed' or runtime.get('task_prompt_sha256')!=sha(prompt) or len(runtime['synthetic_approvals'])!=3:raise RuntimeError('Loom mock flow failed')
                        events=[json.loads(line) for log in (cell/'runtime/invocations').glob('*/stdout.log') for line in log.read_text().splitlines() if line.startswith('{')]
                        if not any(e.get('type')=='loom_task_input' and e['sha256']==sha(prompt) for e in events):raise ValueError('Loom task prompt not observed')
                        candidate=cell/'runtime/workspace'
                    else:candidate,runtime=worker(IMAGES['harness2'],task,prompt,cell/'runtime')
                    worker_events=[]
                    for log in (cell/'runtime').rglob('*'):
                        if log.is_file() and (log.name=='stdout.jsonl' or log.name=='stdout.log' or log.name=='runtime.log'):
                            for line in log.read_text().splitlines():
                                if line.startswith('{'):
                                    event=json.loads(line)
                                    if event.get('type')=='t01_visible_checks':worker_events.append(event)
                    expected_events=3 if hid=='H2' else 1
                    if len(worker_events)!=expected_events or not all(e['expected_starter_red'] for e in worker_events):raise ValueError('In-worker visible checks were not verified')
                    record['worker_visible_checks']=[{k:v for k,v in e.items() if k!='logs'} for e in worker_events]
                    projected=cell/'application';files=project_candidate(candidate,task,projected)
                    if files!=manifest['files']:raise ValueError('Expected no-op mock changed application source')
                    record['tests']=test_candidate(projected,cell/'tests',False)
                    record['application_unchanged']=True
                    # Worker has exited. Judge inputs/evidence are never mounted into it.
                    record['acceptance']=evaluator.evaluate(projected,cell/'acceptance')
                    record['acceptance_artifact']={'path':'acceptance/report.json','sha256':sha(cell/'acceptance/report.json')}
                    record['mock_acceptance_expectation_passed']=validate_acceptance(record['acceptance'],evaluator,files)
                    record['passed']=record['tests']['passed'] and record['mock_acceptance_expectation_passed']
                except Exception as exc:
                    record['error']=str(exc);(cell/'error.log').write_text(traceback.format_exc())
                record['elapsed_seconds']=round(time.monotonic()-started,2)
                cells.append(record);(cell/'summary.json').write_text(json.dumps(record,indent=2)+'\n')
    finally:
        passed=len(cells)==len(levels)*5 and len(starter_hashes)==1 and all(c['passed'] for c in cells) and len(controls)==4 and all(c['passed'] for c in controls.values())
        acceptance_summary={'evaluator_sha256':evaluator.version(),'expected_cells':len(levels)*5,
            'completed':sum(c.get('acceptance',{}).get('status')=='completed' for c in cells),
            'accepted':sum(c.get('acceptance',{}).get('full_target_acceptance') is True for c in cells),
            'rejected':sum(c.get('acceptance',{}).get('full_target_acceptance') is False for c in cells),
            'unknown':sum(c.get('acceptance',{}).get('full_target_acceptance') is None for c in cells),
            'cells':[{'level':c['level'],'harness':c['harness'],
                'status':c.get('acceptance',{}).get('status','not_run'),
                'full_target_acceptance':c.get('acceptance',{}).get('full_target_acceptance'),
                'passed_criteria':c.get('acceptance',{}).get('passed_criteria'),
                'full_target_denominator':c.get('acceptance',{}).get('full_target_denominator'),
                'report_path':c['level']+'/'+c['harness']+'/acceptance/report.json',
                'report_sha256':c.get('acceptance_artifact',{}).get('sha256')} for c in cells]}
        report={'schema':'guild-ledger.t01-harness-smoke/v2','independent_acceptance':acceptance_summary,'verification_passed':passed,'model_calls':0,'model_usage':None,'cost_usd':None,'live_model_calls_enabled':False,'levels':levels,'overlay_profile_sha256':overlay_digest,'images':images,'controls':controls,'cells':cells,'scope':'Infrastructure and input transport plus independent full-target observations; unchanged mock candidates must be rejected. Synthetic acceptance observations are not model/harness quality measurements or live admission.'}
        (output/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    if not passed:raise RuntimeError('T01 harness smoke failed; see '+str(output/'summary.json'))
    print(json.dumps({'verification_passed':passed,'cells':len(cells),'model_calls':0}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);parser.add_argument('--levels',nargs='+',choices=['P1','P2','P3'],default=['P1','P2','P3']);parser.add_argument('--build',action='store_true')
    args=parser.parse_args()
    if len(set(args.levels))!=len(args.levels):parser.error('Levels must be unique')
    os.chdir(ROOT);run(args.output.absolute(),args.levels,args.build)

#!/usr/bin/env python3
"""Run the native Loom pipeline with mock provider only, never infer or auto-ship."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

# Reuse strict task auditing, without exposing the research checkout to the worker.
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'claude'))
from entrypoint import audit_tree
from run import digest_tree

STATE=Path('.claude/feature-workspace/mock-spec/run-state.json')


def save(path,value):
    temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(value,indent=2)+'\n');temporary.replace(path)


def execute(image,task,package,manifest_digest,output,fixture_approvals=False,
            hang=False,resume_after_interrupt=False,wall_seconds=60):
    if not 1<=wall_seconds<=120:raise ValueError('Wall limit must be 1–120 seconds')
    if task.is_symlink() or not task.is_dir() or output.exists() or output.resolve().is_relative_to(task.resolve()):
        raise ValueError('New output and standalone regular task directory required')
    audit_tree(task);audit_tree(package)
    raw=(package/'manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=manifest_digest:raise ValueError('Profile manifest digest mismatch')
    profile=json.loads(raw)
    if profile.get('provider')!='mock' or profile.get('real_provider_enabled') is not False:
        raise ValueError('Only mock supported')
    if {p.name for p in package.iterdir()}!={'manifest.json','mock-spec.md'}:
        raise ValueError('Unexpected package file set')
    for name,digest in profile['assets'].items():
        if name!='mock-spec.md' or hashlib.sha256((package/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Profile asset digest mismatch')
    info=json.loads(subprocess.check_output(['docker','image','inspect',image],text=True))[0]
    if 'RUNNER_KIND=loom-mock' not in info['Config'].get('Env',[]):raise ValueError('Mock Loom image required')
    image=info['Id'];started=time.monotonic();deadline=started+wall_seconds
    output.mkdir(parents=True)
    record={'schema_version':'guild-ledger.loom-mock-attempt/v1','synthetic':True,'profile':'H3-native-mock',
            'source_commit':profile['source']['commit'],'profile_manifest_sha256':manifest_digest,'image_id':image,
            'network':'none','model_calls':0,'cost_usd':None,'model_usage':None,'evaluation_performed':False,
            'fixture_approvals_enabled':fixture_approvals,'synthetic_approvals':[], 'invocations':[],
            'wall_seconds':wall_seconds,'stop_reason':'running'}
    save(output/'attempt.json',record)
    with tempfile.TemporaryDirectory(prefix='guild-ledger-loom-') as temp:
        staging=Path(temp);workspace=staging/'workspace';shutil.copytree(task,workspace)
        for p in [workspace,*workspace.rglob('*')]:p.chmod(0o777 if p.is_dir() else 0o666)
        inputs=staging/'inputs';shutil.copytree(package,inputs)
        shutil.copytree(package,output/'profile')
        request={'resume':False,'approve':None,'fixture_approval':False,'hang':'context-engineer' if hang else None}
        try:
            for index in range(5): # Initial call, optional interrupt-resume, at most three fixture gates.
                if time.monotonic()>=deadline:record['stop_reason']='timeout';break
                (inputs/'request.json').write_text(json.dumps(request)+'\n')
                call_dir=output/'invocations'/f'{index+1:02}';call_dir.mkdir(parents=True)
                shutil.copyfile(inputs/'request.json',call_dir/'request.json')
                name='guild-ledger-loom-'+uuid.uuid4().hex
                item={'session_id':name,'provider':'mock','request':dict(request),'timed_out':False}
                record['invocations'].append(item)
                create=['docker','create','--name',name,'--network','none','--read-only','--cap-drop','ALL',
                        '--security-opt','no-new-privileges','--pids-limit','128','--memory','2g','--cpus','2',
                        '--user','10001:10001','--tmpfs','/home/runner:rw,nosuid,nodev,uid=10001,gid=10001,mode=0700',
                        '--tmpfs','/tmp:rw,nosuid,nodev,mode=1777',
                        '--mount',f'type=bind,src={workspace},dst=/workspace',
                        '--mount',f'type=bind,src={inputs},dst=/inputs,readonly',image]
                try:
                    subprocess.run(create,check=True,stdout=subprocess.DEVNULL,timeout=max(.001,deadline-time.monotonic()))
                    with (call_dir/'stdout.log').open('wb') as stdout,(call_dir/'stderr.log').open('wb') as stderr:
                        process=subprocess.Popen(['docker','start','--attach',name],stdout=stdout,stderr=stderr)
                        try:process.wait(timeout=max(.001,min(2 if request['hang'] else wall_seconds,deadline-time.monotonic())))
                        except subprocess.TimeoutExpired:
                            item['timed_out']=True
                            subprocess.run(['docker','stop','--signal','SIGINT','--timeout','3',name],
                                           check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                            process.wait(timeout=10)
                    state_info=json.loads(subprocess.check_output(['docker','inspect',name],text=True,timeout=10))[0]['State']
                    item['exit_code']=state_info['ExitCode'];item['oom_killed']=state_info['OOMKilled']
                    state=json.loads((workspace/STATE).read_text()) if (workspace/STATE).exists() else None
                    if state is not None:save(call_dir/'state.json',state)
                    if state is not None and state.get('provider')!='mock':raise ValueError('Unexpected recorded provider')
                    save(output/'attempt.json',record)
                    if item['timed_out']:
                        if resume_after_interrupt and index==0 and state is not None:
                            request.update(resume=True,hang=None);continue
                        record['stop_reason']='timeout';break
                    if item['exit_code']==3:
                        gates=[v['gate'] for v in state['stages'].values() if v['status']=='WAITING_APPROVAL'] if state else []
                        if len(gates)!=1:raise ValueError('Expected exactly one pending gate')
                        item['waiting_gate']=gates[0]
                        if not fixture_approvals:record['stop_reason']='needs-human';break
                        expected=profile['gates'][len(record['synthetic_approvals'])] if len(record['synthetic_approvals'])<3 else None
                        if gates[0]!=expected:raise ValueError('Unexpected native gate sequence')
                        record['synthetic_approvals'].append({'gate':gates[0],'synthetic':True,'not_human_authorization':True})
                        request.update(resume=True,approve=gates[0],fixture_approval=True,hang=None)
                        continue
                    record['stop_reason']='completed' if item['exit_code']==0 else 'runtime-error'
                    break
                finally:
                    subprocess.run(['docker','rm','--force',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=False,timeout=10)
            else:record['stop_reason']='invocation-limit'
        except subprocess.TimeoutExpired:
            record['stop_reason']='timeout'
        except (ValueError,OSError,subprocess.CalledProcessError) as exc:
            record['stop_reason']='runtime-error';record['error']=str(exc)
        finally:
            shutil.copytree(workspace,output/'workspace',symlinks=True)
            record['output_sha256']=digest_tree(output/'workspace')
            record['elapsed_seconds']=time.monotonic()-started
            save(output/'attempt.json',record)
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--image',default='guild-ledger-loom-mock:local')
    for name in ('task','package','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--manifest-digest',required=True);p.add_argument('--fixture-approvals',action='store_true')
    p.add_argument('--hang',action='store_true');p.add_argument('--resume-after-interrupt',action='store_true')
    p.add_argument('--wall-seconds',type=float,default=60)
    result=execute(**vars(p.parse_args()))
    print(json.dumps({'stop_reason':result['stop_reason'],'provider':'mock'}))
    raise SystemExit(0 if result['stop_reason']=='completed' else 1)

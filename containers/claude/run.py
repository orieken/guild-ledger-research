#!/usr/bin/env python3
"""Host-side no-model supervisor. Never mounts host home or evidence output."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid


def digest_tree(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}


def run(image, task, prompt, output, mode='fake', timeout=30):
    # Imported without running the container entrypoint.
    import runpy
    audit = runpy.run_path(str(Path(__file__).with_name('entrypoint.py')))['audit_tree']
    if task.is_symlink() or prompt.is_symlink():
        raise ValueError('Task and prompt must not be symlinks')
    task=task.resolve(strict=True); prompt=prompt.resolve(strict=True)
    if output.resolve().is_relative_to(task):
        raise ValueError('Output must be outside task inputs')
    if not task.is_dir() or not prompt.is_file():
        raise ValueError('Task directory and prompt file required')
    audit(task)
    if prompt.is_symlink():
        raise ValueError('Prompt must not be a symlink')
    if output.exists():
        raise ValueError('Output must be a new directory')
    image_info=json.loads(subprocess.check_output(['docker','image','inspect',image],text=True))[0]
    image_id=image_info['Id']
    name='guild-ledger-'+uuid.uuid4().hex
    output.mkdir(parents=True)
    manifest={'schema_version':'guild-ledger.container-smoke/v1','synthetic':mode=='fake',
              'mode':mode,'image_id':image_id,'image_repo_digests':image_info.get('RepoDigests',[]),
              'task_sha256':digest_tree(task),'prompt_sha256':hashlib.sha256(prompt.read_bytes()).hexdigest(),
              'network':'none','timeout_seconds':timeout,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    created=False
    try:
        with tempfile.TemporaryDirectory(prefix='guild-ledger-attempt-') as temp:
            staging=Path(temp); workspace=staging/'workspace'; inputs=staging/'inputs'
            shutil.copytree(task,workspace);inputs.mkdir();shutil.copyfile(prompt,inputs/'prompt.txt')
            # The isolated UID must be able to edit copied files on Linux too.
            for p in [workspace,*workspace.rglob('*')]:
                p.chmod(0o777 if p.is_dir() else (0o777 if p.stat().st_mode & 0o111 else 0o666))
            create=['docker','create','--name',name,'--network','none','--read-only',
                    '--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','128',
                    '--memory','2g','--cpus','2','--user','10001:10001',
                    '--tmpfs','/home/runner:rw,nosuid,nodev,uid=10001,gid=10001,mode=0700',
                    '--tmpfs','/tmp:rw,nosuid,nodev,mode=1777',
                    '--mount',f'type=bind,src={workspace},dst=/workspace',
                    '--mount',f'type=bind,src={inputs},dst=/inputs,readonly',image_id,mode]
            subprocess.run(create,check=True,stdout=subprocess.DEVNULL);created=True
            with (output/'stdout.jsonl').open('wb') as stdout,(output/'stderr.log').open('wb') as stderr:
                process=subprocess.Popen(['docker','start','--attach',name],stdout=stdout,stderr=stderr)
                try:
                    process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    manifest['timed_out']=True
                    subprocess.run(['docker','kill',name],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    process.wait(timeout=10)
            state=json.loads(subprocess.check_output(['docker','inspect',name],text=True))[0]['State']
            manifest.update(exit_code=state['ExitCode'],oom_killed=state['OOMKilled'])
            shutil.copytree(workspace,output/'workspace',symlinks=True)
            manifest['output_symlinks']={str(p.relative_to(output/'workspace')):os.readlink(p)
                                         for p in (output/'workspace').rglob('*') if p.is_symlink()}
            manifest['output_sha256']=digest_tree(output/'workspace')
    finally:
        if created:
            subprocess.run(['docker','rm','--force',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=False)
        manifest['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--image',required=True);p.add_argument('--task',type=Path,required=True)
    p.add_argument('--prompt',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--mode',choices=['fake','preflight','cli-info'],default='fake')
    p.add_argument('--timeout',type=int,default=30)
    a=p.parse_args()
    if not 1<=a.timeout<=120: p.error('timeout must be between 1 and 120 seconds')
    result=run(a.image,a.task,a.prompt,a.output,a.mode,a.timeout)
    raise SystemExit(0 if result.get('exit_code')==0 and not result.get('timed_out') else 1)

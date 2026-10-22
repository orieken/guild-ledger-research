"""Run only the baked upstream deterministic Harness² demo, offline."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

DIGEST='98ea2f392df4140dd18cceeecc6b09c442aafa090b50ef62ceba43b5f71f0af0'


def execute(image,output,timeout=30,profile_digest=DIGEST):
    uid=os.getuid() if sys.platform.startswith('linux') and os.getuid()>0 else 10001
    gid=os.getgid() if sys.platform.startswith('linux') and os.getgid()>0 else 10001
    if output.exists() or not 0<timeout<=120:raise ValueError('New output and bounded timeout required')
    info=json.loads(subprocess.check_output(['docker','image','inspect',image],text=True))[0]
    if ('RUNNER_KIND=harness2-deterministic' not in info['Config'].get('Env',[]) or
        info['Config'].get('Labels',{}).get('io.guild-ledger.profile-sha256')!=profile_digest):
        raise ValueError('Only the pinned deterministic profile image is permitted')
    output.mkdir(parents=True);name='guild-ledger-harness2-'+uuid.uuid4().hex
    started=time.monotonic()
    record={'schema_version':'guild-ledger.harness2-demo-attempt/v1','harness_id':'H4','synthetic':True,
            'worker_uid':uid,'worker_gid':gid,'image_id':info['Id'],'profile_manifest_sha256':profile_digest,'session_id':name,
            'network':'none','model_calls':0,'model_usage':None,'cost_usd':None,'timeout_seconds':timeout,
            'stop_reason':'running','benchmark_evaluation_performed':False}
    created=False
    try:
        with tempfile.TemporaryDirectory(prefix='guild-ledger-harness2-') as temp:
            workspace=Path(temp)/'workspace';workspace.mkdir(mode=0o777);workspace.chmod(0o777)
            create=['docker','create','--name',name,'--init','--network','none','--read-only',
                    '--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','128',
                    '--memory','1g','--cpus','1','--user',f'{uid}:{gid}',
                    '--tmpfs',f'/home/runner:rw,nosuid,nodev,uid={uid},gid={gid},mode=0700',
                    '--tmpfs','/tmp:rw,nosuid,nodev,mode=1777',
                    '--mount',f'type=bind,src={workspace},dst=/workspace',info['Id']]
            subprocess.run(create,check=True,stdout=subprocess.DEVNULL,timeout=10);created=True
            with (output/'stdout.log').open('wb') as out,(output/'stderr.log').open('wb') as err:
                process=subprocess.Popen(['docker','start','--attach',name],stdout=out,stderr=err)
                try:process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    record['stop_reason']='timeout'
                    subprocess.run(['docker','kill',name],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                    process.wait(timeout=10)
            state=json.loads(subprocess.check_output(['docker','inspect',name],text=True,timeout=10))[0]['State']
            record['exit_code']=state['ExitCode']
            shutil.copytree(workspace,output/'workspace',symlinks=True)
            report=workspace/'demo/demo.json'
            if report.exists():record['demo_summary']=json.loads(report.read_text())
            if record['stop_reason']=='running':
                record['stop_reason']='completed' if state['ExitCode']==0 and report.exists() and record['demo_summary']['failed']==0 else 'runtime-error'
    except subprocess.TimeoutExpired:
        record['stop_reason']='timeout'
    except (OSError,subprocess.CalledProcessError,ValueError) as exc:
        record['stop_reason']='runtime-error';record['error']=str(exc)
    finally:
        subprocess.run(['docker','rm','--force',name],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
        record['elapsed_seconds']=time.monotonic()-started
        (output/'attempt.json').write_text(json.dumps(record,indent=2)+'\n')
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--image',default='guild-ledger-harness2-demo:local');p.add_argument('--output',type=Path,required=True)
    p.add_argument('--timeout',type=float,default=30)
    result=execute(**vars(p.parse_args()));print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['stop_reason']=='completed' else 1)

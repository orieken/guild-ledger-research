"""Shared agent-visible, offline T01 test command; only public tests/fixtures.

Runs ephemeral localhost services inside the worker's --network=none namespace.
The independent supervisor still retests exported source using trusted inputs.
"""
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

ROOT=Path('/opt/t01')
def run():
    servers=[];results=[];logs={}
    with tempfile.TemporaryDirectory(prefix='t01-visible-',dir='/opt/t01-run') as temporary:
        temp=Path(temporary);web=temp/'web';shutil.copytree(ROOT/'web',web,symlinks=True)
        shutil.rmtree(web/'src');shutil.copytree(Path('/workspace/web/src'),web/'src',symlinks=False)
        env={**os.environ,'NO_COLOR':'1','PYTHONDONTWRITEBYTECODE':'1','GUILD_PROXY_TARGET':'http://127.0.0.1:18000','GUILD_URL':'http://127.0.0.1:18000','ARMORY_URL':'http://127.0.0.1:8001','WEB_URL':'http://127.0.0.1:5173'}
        def check(label,args,cwd=None):
            p=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=60)
            logs[label]=p.stdout;return p.returncode
        try:
            commands=[('guild',[str(ROOT/'venv/bin/python'),'-m','uvicorn','app:app','--app-dir','/workspace/services/guild','--host','127.0.0.1','--port','18000'],None),('armory',[str(ROOT/'armory')],None),('web',['npm','run','dev'],web)]
            for label,args,cwd in commands:
                stream=(temp/(label+'.log')).open('w')
                process=subprocess.Popen(args,cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
                servers.append((label,process,stream))
            startup=1
            for attempt in range(20):
                startup=check('startup',['python3','-m','unittest','discover','-s',str(ROOT/'tests'),'-p','test_startup.py','-v'])
                if startup==0:break
                if any(p.poll() is not None for _,p,_ in servers):break
                time.sleep(.25)
            results.append({'check':'startup','exit_code':startup})
            if startup==0:
                results.append({'check':'api','exit_code':check('api',['python3','-m','unittest','discover','-s',str(ROOT/'tests'),'-p','test_quests.py','-v'])})
                results.append({'check':'ui','exit_code':check('ui',['npm','test','--','--run'],web)})
                results.append({'check':'build','exit_code':check('build',['npm','run','build'],web)})
        finally:
            for label,p,stream in servers:
                if p.poll() is None:
                    os.killpg(p.pid,signal.SIGTERM)
                    try:p.wait(timeout=5)
                    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
                stream.close();logs[label+'-service']=(temp/(label+'.log')).read_text()
        expected_red=len(results)==4 and results[0]['exit_code']==0 and results[1]['exit_code']!=0 and results[2]['exit_code']!=0 and results[3]['exit_code']==0 and bool(re.search(r'FAILED \(failures=4\)',logs['api'])) and bool(re.search(r'Tests\s+2 failed',logs['ui']))
        event={'type':'t01_visible_checks','schema':'guild-ledger.worker-visible/v1','synthetic_attempt':True,'model_calls':0,'checks':results,'all_visible_passed':len(results)==4 and all(r['exit_code']==0 for r in results),'expected_starter_red':expected_red,'network':'none; ephemeral localhost only','logs':logs}
        print(json.dumps(event),flush=True)
        return event
if __name__=='__main__':
    event=run()
    if sys.argv[1:]==['--expect-starter-red']:sys.exit(0 if event['expected_starter_red'] else 2)
    if sys.argv[1:]:raise ValueError('Only optional --expect-starter-red is accepted')
    sys.exit(0 if event['all_visible_passed'] else 1)

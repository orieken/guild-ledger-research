#!/usr/bin/env python3
"""No-model startup/red/green/mutation check of T01's visible checks only."""
import argparse
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import uuid
from package_benchmark import ROOT, package

def verify(output):
    output=Path(output).absolute()
    if output.exists(): raise ValueError('Evidence output must be new')
    output.mkdir(parents=True)
    results=[]
    env={**os.environ,'NO_COLOR':'1','COMPOSE_PROJECT_NAME':'t01-verify-'+uuid.uuid4().hex[:10]}
    with tempfile.TemporaryDirectory(prefix='guild-t01-') as temp:
        bundle=Path(temp)/'bundle';manifest=package('P1',bundle);work=bundle/'workspace'
        def run(label,args,expected=0):
            print(label,flush=True)
            start=time.monotonic()
            p=subprocess.run(args,cwd=work,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=600)
            (output/(label+'.log')).write_text(p.stdout)
            passed=p.returncode==0 if expected==0 else p.returncode!=0
            if expected != 0:
                if 'test_quests.py' in args:
                    passed = passed and bool(re.search(r'FAILED \(failures=\d+\)',p.stdout))
                else:
                    passed = passed and bool(re.search(r'Tests\s+\d+ failed',p.stdout))
            results.append({'check':label,'returncode':p.returncode,'expected':'pass' if expected==0 else 'fail','passed':passed,'seconds':round(time.monotonic()-start,2)})
            if not passed: raise AssertionError(f'{label}: unexpected result; see {output}')
        compose=['docker','compose']
        try:
            run('starter-build',compose+['up','--build','-d','--wait'])
            run('starter-startup',['make','test-startup'])
            run('starter-api-red',['python3','-m','unittest','discover','-s','tests','-p','test_quests.py','-v'],1)
            run('starter-ui-red',['make','test-web'],1)
            run('starter-web-build',compose+['run','--rm','--no-deps','web','npm','run','build'])
            # This witness proves the visible checks are satisfiable, not full-target acceptance.
            reference=ROOT/'benchmarks/T01/validation'
            shutil.copyfile(reference/'visible-reference.py',work/'services/guild/app.py')
            shutil.copyfile(reference/'visible-reference.vue',work/'web/src/App.vue')
            run('witness-build',compose+['up','--build','-d','--wait'])
            run('witness-visible',['make','test-visible'])
            run('witness-web-build',compose+['run','--rm','--no-deps','web','npm','run','build'])
            api=work/'services/guild/app.py';original=api.read_text()
            for name,source in [
                ('ordering',original.replace("sorted(data,key=lambda q:(q['title'].casefold(),q['id']))","data")),
                ('filter',original.replace("difficulty is None or q['difficulty']==difficulty","True")),
                ('missing-status',original.replace('status_code=404','status_code=200'))]:
                api.write_text(source)
                run(name+'-build',compose+['up','--build','-d','--wait','guild'])
                run(name+'-detected',['python3','-m','unittest','discover','-s','tests','-p','test_quests.py','-v'],1)
            api.write_text(original)
            ui=work/'web/src/App.vue';ui.write_text(ui.read_text().replace('role="alert"','role="status"'))
            run('alert-build',compose+['build','web'])
            run('alert-detected',['make','test-web'],1)
        finally:
            p=subprocess.run(compose+['down','--volumes','--remove-orphans'],cwd=work,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=60)
            (output/'cleanup.log').write_text(p.stdout)
            report={'schema':'guild-ledger.visible-validation/v1','live_model_calls_enabled':False,'starter_sha256':manifest['starter_sha256'],'checks':results,'verification_passed':len(results)==16 and all(r['passed'] for r in results) and p.returncode==0,'scope':'Visible checks only. Witness intentionally does not implement the full target.'}
            (output/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    if not report['verification_passed']: raise AssertionError('Verification incomplete')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);verify(parser.parse_args().output)

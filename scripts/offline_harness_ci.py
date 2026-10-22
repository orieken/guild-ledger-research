#!/usr/bin/env python3
"""Credential-free setup/build/test orchestration; never dispatch a model runner."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

RESEARCH = Path(__file__).resolve().parents[1]
RESULTS = RESEARCH/'ci-offline-results'
PACKAGES = {'H1':'guild-ledger-guidelines', 'H2':'guild-ledger-harness',
            'H3':'guild-ledger-loom', 'H4':'guild-ledger-harness2'}
UPSTREAM = {'H3':('https://github.com/orieken/loom.git','upstream-loom'),
            'H4':('https://github.com/google-research/harness2.git','upstream-harness2')}
SUITES = [('claude-startup','containers/claude/tests/smoke.py'),
          ('h1-h2-packages','containers/claude/tests/treatments.py'),
          ('h2-controller','containers/claude/tests/h2.py'),
          ('loom-source-snapshot','containers/loom/tests/source_snapshot.py'),
          ('loom-native-mock','containers/loom/tests/pipeline.py'),
          ('harness2-deterministic','containers/harness2/tests/demo.py'),
          ('t01-packaging','scripts/tests/test_benchmark_package.py'),
          ('t01-supervisor-boundaries','scripts/tests/test_t01_supervisor.py')]
IMAGES = ['guild-ledger-claude-smoke:local','guild-ledger-claude:2.1.304',
          'guild-ledger-loom-mock:local','guild-ledger-harness2-demo:local'] + [
          'guild-ledger-t01-'+name+':local' for name in ('guild','armory','web','probe','claude','loom','harness2')]


def write(name,value):
    RESULTS.mkdir(exist_ok=True)
    temp=RESULTS/(name+'.tmp');temp.write_text(json.dumps(value,indent=2)+'\n');temp.replace(RESULTS/name)


def step(name,command,timeout=1200):
    RESULTS.mkdir(exist_ok=True);started=time.monotonic()
    with (RESULTS/(name+'.log')).open('w') as log:
        try:
            result=subprocess.run(command,cwd=RESEARCH,stdout=log,stderr=subprocess.STDOUT,
                                  timeout=timeout,check=False)
            status={'name':name,'exit_code':result.returncode,'status':'passed' if result.returncode==0 else 'failed'}
        except subprocess.TimeoutExpired:
            status={'name':name,'exit_code':None,'status':'timeout'}
        except OSError as exc:
            log.write(str(exc)+'\n');status={'name':name,'exit_code':None,'status':'failed'}
    status['elapsed_seconds']=time.monotonic()-started
    write(name+'.json',status)
    print(name+': '+status['status'],flush=True)
    return status['status']=='passed'


def git(*args,cwd):
    return subprocess.check_output(['git',*args],cwd=cwd,text=True,timeout=120).strip()


def checkout(url,revision,path):
    if not re.fullmatch('[0-9a-f]{40}',revision or ''):raise ValueError('Immutable commit required')
    if path.is_symlink():raise ValueError('Checkout cannot be a symlink')
    if not path.exists():
        path.mkdir()
        subprocess.run(['git','init','--quiet',str(path)],check=True)
        subprocess.run(['git','-C',str(path),'remote','add','origin',url],check=True)
    head=subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=path,capture_output=True,text=True)
    if head.returncode!=0:
        subprocess.run(['git','-C',str(path),'fetch','--quiet','--depth','1','origin',revision],check=True,timeout=120)
        subprocess.run(['git','-C',str(path),'checkout','--quiet','--detach',revision],check=True)
    if git('rev-parse','HEAD',cwd=path)!=revision:raise ValueError('Checkout revision mismatch: '+str(path))
    if git('status','--porcelain',cwd=path):raise ValueError('Dirty checkout: '+str(path))


def prepare():
    entries=json.loads((RESEARCH/'harness-packages.json').read_text())['entries']
    if {e['harness_id'] for e in entries}!=set(PACKAGES) or len(entries)!=4:
        raise ValueError('Expected H1–H4 registry')
    identities=[]
    source_errors=[]
    for entry in entries:
        hid=entry['harness_id'];name=PACKAGES[hid]
        if entry['repository']!='orieken/'+name or entry['local_package']!='../'+name+'/package':
            raise ValueError('Unexpected repository layout')
        path=RESEARCH.parent/name
        checkout('https://github.com/'+entry['repository']+'.git',entry['source_commit'],path)
        raw=(path/'package/manifest.json').read_bytes()
        if hashlib.sha256(raw).hexdigest()!=entry['manifest_sha256']:raise ValueError('Package digest mismatch: '+hid)
        manifest=json.loads(raw)
        for filename,digest in manifest.get('assets',{}).items():
            asset=path/'package'/filename
            if Path(filename).is_absolute() or '..' in Path(filename).parts or asset.is_symlink():raise ValueError('Invalid asset path')
            if hashlib.sha256(asset.read_bytes()).hexdigest()!=digest:raise ValueError('Asset digest mismatch')
        identities.append({'harness_id':hid,'repository':entry['repository'],'commit':entry['source_commit'],
                           'manifest_sha256':entry['manifest_sha256']})
        if hid in UPSTREAM:
            url,folder=UPSTREAM[hid];source=RESEARCH.parent/folder
            if manifest['source']['repository']!=url:raise ValueError('Unexpected upstream URL')
            if hid=='H3' and entry.get('source_snapshot'):
                snapshot=entry['source_snapshot']
                relative=Path(snapshot['path'])
                if relative.is_absolute() or '..' in relative.parts or relative.parts[:2]!=('vendor','loom'):
                    raise ValueError('Unexpected source snapshot location')
                archive=RESEARCH/relative
                if hashlib.sha256(archive.read_bytes()).hexdigest()!=snapshot['sha256']:
                    raise ValueError('Registry snapshot digest mismatch')
                command=[sys.executable,'-B','containers/loom/prepare.py','--snapshot',str(archive),
                         '--package',str(path/'package'),'--manifest-digest',entry['manifest_sha256']]
                if not step('prepare-h3',command):raise RuntimeError('Snapshot preparation failed')
                identities[-1]['source_snapshot']=snapshot
                continue
            try:
                checkout(url,manifest['source']['commit'],source)
            except (ValueError,subprocess.SubprocessError) as exc:
                source_errors.append(hid)
                write('prepare-'+hid.lower()+'.json',{'name':'prepare-'+hid.lower(),'status':'blocked','exit_code':None,
                       'elapsed_seconds':0,'error':'Pinned upstream commit unavailable: '+str(exc)})
                continue
            if hid=='H3':command=[sys.executable,'-B','containers/loom/prepare.py','--source',str(source),
                                 '--package',str(path/'package'),'--manifest-digest',entry['manifest_sha256']]
            else:command=[sys.executable,'-B','containers/harness2/prepare.py','--source',str(source),
                          '--package',str(path/'package'),'--digest',entry['manifest_sha256']]
            if not step('prepare-'+hid.lower(),command):raise RuntimeError('Upstream export failed: '+hid)
    h1=RESEARCH.parent/PACKAGES['H1']/'package/guidelines.md'
    h2=RESEARCH.parent/PACKAGES['H2']/'package/guidelines.md'
    if h1.read_bytes()!=h2.read_bytes():raise ValueError('H2 must contain identical H1 guideline bytes')
    write('package-identities.json',identities)
    if source_errors:raise RuntimeError('Pinned upstream source unavailable for '+', '.join(source_errors))
    write('prepare.json',{'name':'prepare','status':'passed','exit_code':0,'elapsed_seconds':0})


def build():
    commands=[('build-claude-smoke',['docker','build','--progress=plain','--target','smoke','-t',IMAGES[0],'containers/claude']),
              ('build-claude',['docker','build','--progress=plain','--target','claude','-t',IMAGES[1],'containers/claude']),
              ('build-loom',['docker','build','--progress=plain','-t',IMAGES[2],'containers/loom']),
              ('build-harness2',['docker','build','--progress=plain','-t',IMAGES[3],'containers/harness2'])]
    passed=[step(name,command) for name,command in commands]
    if not all(passed):raise RuntimeError('One or more image builds failed; unaffected images were still attempted')


def test():
    # Deliberately run every suite even after an assertion failure.
    passed=[step(name,[sys.executable,'-B',script],timeout=240) for name,script in SUITES]
    passed.append(step('t01-harness-integration',[sys.executable,'-B','scripts/t01_harness_smoke.py',
                       '--build','--output',str(RESULTS/'t01')],timeout=1200))
    if not all(passed):raise RuntimeError('One or more offline suites failed; see artifacts')


def report():
    identities=[]
    for image in IMAGES:
        result=subprocess.run(['docker','image','inspect',image],capture_output=True,text=True,check=False,timeout=30)
        if result.returncode==0:
            data=json.loads(result.stdout)[0]
            identities.append({'tag':image,'image_id':data['Id'],'architecture':data['Architecture'],
                               'os':data['Os'],'rootfs_layers':data['RootFS']['Layers']})
    write('image-identities.json',identities)
    results=[json.loads(p.read_text()) for p in sorted(RESULTS.glob('*.json'))
             if p.name not in {'image-identities.json','package-identities.json','report.json'}]
    expected={name for name,_ in SUITES}|{'t01-harness-integration'}
    suites={r['name']:r for r in results if r.get('name') in expected}
    suites_passed=set(suites)==expected and all(r['status']=='passed' for r in suites.values())
    required=expected|{'prepare','prepare-h3','prepare-h4','build-claude-smoke','build-claude','build-loom','build-harness2'}
    observed={r['name']:r for r in results}
    complete=(required<=set(observed) and all(r['status']=='passed' for r in results)
              and (RESULTS/'package-identities.json').exists())
    result={'schema_version':'guild-ledger.offline-ci/v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'research_commit':git('rev-parse','HEAD',cwd=RESEARCH),'run_id':os.environ.get('GITHUB_RUN_ID'),
            'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'runner_image':os.environ.get('ImageVersion'),
            'all_suites_passed':suites_passed,'verification_passed':complete,'live_model_calls_enabled':False,'results':results}
    write('report.json',result)
    lines=['## Offline harness setup','', '| Check | Result | Seconds |','|---|---|---|']
    for r in results:lines.append(f"| {r['name']} | {r['status']} | {r['elapsed_seconds']:.1f} |")
    for name in sorted(expected-set(suites)):lines.append(f'| {name} | not run | — |')
    lines+=['','Offline suites passed: **'+str(suites_passed)+'**. Full setup verified: **'+str(complete)+'**.',
            'Tests use fake/mock/deterministic execution only.',
            'Claude is invoked only for version/help. Builds require downloads; agent workers have no external network and service probes use internal-only networks.',
            'Model credentials are not supplied. CI compute and model-call costs are distinct.']
    summary='\n'.join(lines)+'\n';(RESULTS/'summary.md').write_text(summary)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as stream:stream.write(summary)
    print(summary)
    if not complete:raise RuntimeError('Offline verification incomplete or failed')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['prepare','build','test','report'])
    args=parser.parse_args()
    stale=RESULTS/(args.command+'-error.json')
    if stale.exists():stale.unlink()
    try:globals()[args.command]()
    except Exception as exc:
        write(args.command+'-error.json',{'name':args.command,'status':'failed','exit_code':None,
                                        'elapsed_seconds':0,'error':str(exc)})
        raise

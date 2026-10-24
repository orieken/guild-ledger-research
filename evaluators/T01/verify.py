#!/usr/bin/env python3
"""Verify the independent evaluator using full references and seeded defects."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import evaluate as evaluator
from mutations import materialize, EXPECTED

def verify(output,build_images=False):
    output=Path(output).absolute()
    if output.exists():raise ValueError('New verification output required')
    output.mkdir(parents=True)
    if build_images:
        evaluator.build(output/'build')
        if evaluator.command(['docker','build','-t','guild-ledger-t01-probe:local','-f',str(evaluator.ROOT/'containers/t01/Dockerfile.probe'),str(evaluator.ROOT/'benchmarks/T01/starter')],output/'build/probe.log',600):raise RuntimeError('Visible-control image build failed')
    inventory=json.loads((evaluator.HERE/'criteria.json').read_text())
    if set(EXPECTED.values())!={row['id'] for row in inventory['criteria']}:raise ValueError('Every criterion requires a predeclared sensitivity mutant')
    checks=[]
    with tempfile.TemporaryDirectory(prefix='t01-evaluator-proof-') as temp:
        temp=Path(temp);starter=evaluator.ROOT/'benchmarks/T01/starter';reference=temp/'reference'
        materialize(starter,evaluator.HERE/'reference',reference)
        for number in (1,2):
            print('Complete reference '+str(number),flush=True)
            result=evaluator.evaluate(reference,output/('reference-'+str(number)))
            checks.append({'case':'reference-'+str(number),'passed':result.get('full_target_acceptance') is True,'failed':[r['id'] for r in result.get('results',[]) if r['status']=='fail']})
        print('Valid frontend component rename',flush=True)
        renamed=temp/'renamed-component';shutil.copytree(reference,renamed)
        (renamed/'web/src/App.vue').rename(renamed/'web/src/QuestBrowser.vue')
        (renamed/'web/src/App.vue').write_text("<script setup lang=\"ts\">\nimport QuestBrowser from './QuestBrowser.vue';\n</script>\n<template><QuestBrowser /></template>\n")
        path=renamed/'web/src/main.ts';path.write_text(path.read_text().replace('./App.vue','./QuestBrowser.vue'))
        result=evaluator.evaluate(renamed,output/'renamed-component')
        checks.append({'case':'valid-component-rename','passed':result.get('full_target_acceptance') is True})
        print('Valid accessible button labels',flush=True)
        labeled=temp/'accessible-labels';shutil.copytree(reference,labeled)
        path=labeled/'web/src/App.vue';path.write_text(path.read_text().replace('<button @click="open(quest.id)">View {{quest.title}}</button>', '<button @click="open(quest.id)" :aria-label="`View ${quest.title}`">Details</button>'))
        result=evaluator.evaluate(labeled,output/'accessible-labels',only=['U01'])
        checks.append({'case':'valid-accessible-labels','passed':result.get('diagnostic_passed') is True})
        # Valid alternative: serialization instead of generation counters for list requests.
        serialized=temp/'serialized';shutil.copytree(reference,serialized)
        path=serialized/'web/src/App.vue';path.write_text(path.read_text().replace('<button type="submit">','<button type="submit" :disabled="loading">'))
        print('Valid serialized list requests',flush=True)
        result=evaluator.evaluate(serialized,output/'serialized',only=['U09'])
        checks.append({'case':'valid-serialized-list','passed':result.get('diagnostic_passed') is True})
        print('Visible-only witness versus full target',flush=True)
        visible=temp/'visible-witness';shutil.copytree(starter,visible)
        for source,target in [('visible-reference.py','services/guild/app.py'),('visible-reference.vue','web/src/App.vue')]:shutil.copyfile(evaluator.ROOT/'benchmarks/T01/validation'/source,visible/target)
        from t01_harness_smoke import test_candidate
        public=test_candidate(visible,output/'visible-witness-public',True)
        result=evaluator.evaluate(visible,output/'visible-witness-acceptance')
        checks.append({'case':'visible-witness','passed':public['passed'] and result.get('status')=='completed' and result.get('full_target_acceptance') is False})
        print('Build and evaluator-failure controls',flush=True)
        badtypes=temp/'bad-types';shutil.copytree(reference,badtypes);path=badtypes/'web/src/App.vue';path.write_text(path.read_text().replace("const q=ref('')","const number: number = 'wrong';const q=ref('')"))
        result=evaluator.evaluate(badtypes,output/'type-error')
        checks.append({'case':'type-error','passed':result['status']=='candidate_build_failure' and result['full_target_acceptance'] is False})
        empty=temp/'empty-frontend';shutil.copytree(reference,empty);shutil.rmtree(empty/'web/src');(empty/'web/src').mkdir()
        result=evaluator.evaluate(empty,output/'empty-frontend')
        checks.append({'case':'empty-frontend','passed':result['status']=='candidate_build_failure' and result['full_target_acceptance'] is False})
        original=evaluator.TAGS['judge'];evaluator.TAGS['judge']=evaluator.TAGS['guild']
        try:result=evaluator.evaluate(reference,output/'wrong-evaluator-image')
        finally:evaluator.TAGS['judge']=original
        checks.append({'case':'wrong-evaluator-image','passed':result['status']=='evaluator_error' and result['full_target_acceptance'] is None})
        print('Unfinished starter',flush=True)
        result=evaluator.evaluate(starter,output/'starter',only=['A01','U01'])
        checks.append({'case':'unfinished-starter','passed':result.get('status')=='completed' and not result.get('diagnostic_passed')})
        for name,criterion in EXPECTED.items():
            print('Mutation '+name+' -> '+criterion,flush=True)
            candidate=temp/name;materialize(starter,evaluator.HERE/'reference',candidate,name)
            result=evaluator.evaluate(candidate,output/('mutant-'+name),only=[criterion])
            detected=result.get('status')=='completed' and any(r['id']==criterion and r['status']=='fail' for r in result.get('results',[]))
            checks.append({'case':name,'expected_failed_criterion':criterion,'passed':detected,'status':result['status']})
        print('Protected input rejection',flush=True)
        tampered=temp/'tampered';shutil.copytree(reference,tampered);(tampered/'tests/test_quests.py').write_text('pass')
        result=evaluator.evaluate(tampered,output/'tampered')
        checks.append({'case':'protected-test-tamper','passed':result['status']=='invalid_candidate' and result['full_target_acceptance'] is False})
    summary={'schema':'guild-ledger.t01-evaluator-verification/v1','verification_passed':all(c['passed'] for c in checks),'evaluator_sha256':evaluator.version(),'checks':checks,'model_calls':0,'live_model_calls_enabled':False,'scope':'Independent API/Chromium acceptance checks validated against hand-written reference and separate mutation catalog; no model or harness quality measurement.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    if not summary['verification_passed']:raise RuntimeError('Evaluator validation failed')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--build',action='store_true');a=p.parse_args();verify(a.output,a.build)

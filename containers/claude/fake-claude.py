"""Synthetic fixtures, never provider usage or code-quality measurements."""
import json
import time
import sys
from pathlib import Path
prompt=Path('/inputs/assembled-prompt.txt').read_text()
config_path=Path('/inputs/stage.json')
if config_path.exists():
    config=json.loads(config_path.read_text());stage=config['stage_id'];scenario=config['fixture']
    handoff=json.loads(Path('/inputs/handoff.json').read_text())
    marker=Path.home()/'stage-marker'
    if marker.exists():
        raise RuntimeError('Stage home was reused')
    marker.write_text(stage)
    if stage == 'implementation':
        Path('/workspace/candidate.txt').write_text('implemented\n')
        value={'plan':['Make synthetic edit','Run synthetic check'], 'handoff':'Synthetic implementation',
               'visible_checks':[{'command':'synthetic-check','exit_code':0,'synthetic':True}]}
    elif stage == 'review':
        if scenario == 'review-mutation':
            Path('/workspace/candidate.txt').write_text('reviewer changed candidate\n')
        finding={'id':'F1','severity':'medium','file':'candidate.txt','line':1,
                 'issue':'Synthetic issue','evidence':'Synthetic observation','requested_change':'Write repaired'}
        value={'schema_version':'guild-ledger.h2-review/v1','verdict':'pass','findings':[]}
        if scenario in {'repair','repair-failure','repair-needs-human','repair-timeout','repair-malformed'}:
            value.update(verdict='changes_requested',findings=[finding])
        if scenario == 'invalid-review':value={'verdict':'broken'}
        if scenario == 'invalid-path':value.update(verdict='changes_requested',findings=[dict(finding,file='../escape')])
        if scenario == 'missing-file':value.update(verdict='changes_requested',findings=[dict(finding,file='absent.txt')])
    else:
        if handoff.get('review',{}).get('verdict') != 'changes_requested':
            raise RuntimeError('Repair lacks validated review')
        Path('/workspace/candidate.txt').write_text('repaired\n')
        value={'handoff':'Synthetic repair','visible_checks':[{'command':'synthetic-check','exit_code':0,'synthetic':True}],
               'findings_addressed':['F1'],'findings_remaining':[]}
    if scenario == stage+'-failure':sys.exit(9)
    if scenario == stage+'-timeout':time.sleep(60)
    if scenario == stage+'-needs-human':
        print(json.dumps({'type':'result','synthetic':True,'stop_reason':'needs-human','result':None,
                          'usage':{'input_tokens':11,'output_tokens':7},'cost_usd':None}),flush=True)
        sys.exit(0)
    if scenario == stage+'-malformed':print('not JSON',flush=True);sys.exit(0)
    event={'type':'result','synthetic':True,'stop_reason':'completed','result':value,
           'usage':{'input_tokens':11,'output_tokens':7},'cost_usd':None}
    if scenario == 'missing-usage' and stage == 'review':event.pop('usage')
    print(json.dumps(event),flush=True)
else:
    Path('/workspace/synthetic-result.txt').write_text('Synthetic edit: ' + prompt + '\n')
    if prompt == '__fixture_timeout__':time.sleep(60)
    if prompt == '__fixture_failure__':sys.exit(9)
    print(json.dumps({'type':'result','synthetic':True,'result':'fixture complete',
                      'usage':{'input_tokens':11,'output_tokens':7},'cost_usd':None}),flush=True)

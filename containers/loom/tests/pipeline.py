"""Native Loom mock-container integration. No model calls or human approvals."""
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile

root=Path(__file__).resolve().parents[1]
execute=runpy.run_path(str(root/'run.py'))['execute']
package=root.parents[2]/'guild-ledger-loom/package'
digest=hashlib.sha256((package/'manifest.json').read_bytes()).hexdigest()
state_path=Path('.claude/feature-workspace/mock-spec/run-state.json')


def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Invalid profile accepted')


with tempfile.TemporaryDirectory(prefix='guild-ledger-loom-tests-') as temp:
    temp=Path(temp);task=temp/'task';task.mkdir();(task/'starter.txt').write_text('untouched\n')
    halt=execute('guild-ledger-loom-mock:local',task,package,digest,temp/'halt')
    assert halt['stop_reason']=='needs-human' and halt['synthetic_approvals']==[]
    assert len(halt['invocations'])==1 and halt['invocations'][0]['exit_code']==3
    state=json.loads((temp/'halt/workspace'/state_path).read_text())
    assert state['provider']=='mock' and state['stages']['developer']['status']=='WAITING_APPROVAL'
    assert state['approvals']=={}
    complete=execute('guild-ledger-loom-mock:local',task,package,digest,temp/'complete',fixture_approvals=True)
    assert complete['stop_reason']=='completed' and len(complete['invocations'])==4
    assert [g['gate'] for g in complete['synthetic_approvals']]==['confirm-design','confirm-security','confirm-ship']
    assert all(g['not_human_authorization'] for g in complete['synthetic_approvals'])
    assert len({i['session_id'] for i in complete['invocations']})==4
    state=json.loads((temp/'complete/workspace'/state_path).read_text())
    assert state['provider']=='mock' and len(state['stages'])==16
    assert sum(s['status']=='COMPLETED' for s in state['stages'].values())==9
    assert sum(s['status']=='SKIPPED' for s in state['stages'].values())==7
    assert set(state['approvals'])=={'confirm-design','confirm-security','confirm-ship'}
    assert state.get('spend') is None and all(s.get('usage') is None for s in state['stages'].values())
    for stage in state['stages'].values():
        if stage.get('artifactPath'):
            relative=Path(stage['artifactPath']).relative_to('/workspace')
            assert hashlib.sha256((temp/'complete/workspace'/relative).read_bytes()).hexdigest()==stage['artifactSha256']
    assert any(s.get('postureViolation') for s in state['stages'].values())
    assert any(s.get('editedAfterReview') for s in state['stages'].values())
    interrupted=execute('guild-ledger-loom-mock:local',task,package,digest,temp/'interrupted',hang=True)
    assert interrupted['stop_reason']=='timeout'
    s=json.loads((temp/'interrupted/workspace'/state_path).read_text())
    assert s['provider']=='mock' and s['stages']['context-engineer']['status']=='INTERRUPTED'
    resumed=execute('guild-ledger-loom-mock:local',task,package,digest,temp/'resumed',hang=True,resume_after_interrupt=True)
    assert resumed['stop_reason']=='needs-human' and len(resumed['invocations'])==2
    assert resumed['invocations'][1]['request']['resume'] is True
    s=json.loads((temp/'resumed/workspace'/state_path).read_text())
    assert s['provider']=='mock' and s['stages']['context-engineer']['status']=='COMPLETED'
    for result in (halt,complete,interrupted,resumed):
        assert result['model_calls']==0 and result['cost_usd'] is None and result['model_usage'] is None
        assert result['network']=='none' and not result['evaluation_performed']
    assert list(task.iterdir())==[task/'starter.txt']
    reject(lambda:execute('unused',task,package,'0'*64,temp/'bad-digest'))
    bad=temp/'bad-package';shutil.copytree(package,bad);(bad/'mock-spec.md').write_text('tampered')
    reject(lambda:execute('unused',task,bad,digest,temp/'bad-asset'))
    profile=json.loads((bad/'manifest.json').read_text());profile['provider']='claude'
    (bad/'manifest.json').write_text(json.dumps(profile))
    bad_digest=hashlib.sha256((bad/'manifest.json').read_bytes()).hexdigest()
    reject(lambda:execute('unused',task,bad,bad_digest,temp/'bad-provider'))
    reject(lambda:execute('guild-ledger-claude:2.1.304',task,package,digest,temp/'wrong-image'))
    # The container also binds a submitted profile to the binary's source lock.
    changed=temp/'changed-profile';shutil.copytree(package,changed)
    m=json.loads((changed/'manifest.json').read_text());m['source']['commit']='0'*40
    (changed/'manifest.json').write_text(json.dumps(m))
    result=execute('guild-ledger-loom-mock:local',task,changed,hashlib.sha256((changed/'manifest.json').read_bytes()).hexdigest(),temp/'source-mismatch')
    assert result['stop_reason']=='runtime-error' and result['invocations'][0]['exit_code']==2
    assert 'Profile digest' in (temp/'source-mismatch/invocations/01/stderr.log').read_text()
    # A legacy/tampered resume state must never switch from mock to Claude.
    workspace=temp/'unsafe-resume';shutil.copytree(temp/'halt/workspace',workspace)
    state=json.loads((workspace/state_path).read_text());state['provider']='claude';(workspace/state_path).write_text(json.dumps(state))
    inputs=temp/'resume-inputs';shutil.copytree(package,inputs)
    (inputs/'request.json').write_text(json.dumps({'resume':True,'approve':None,'fixture_approval':False,'hang':None}))
    rejected=subprocess.run(['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL',
        '--security-opt','no-new-privileges','--tmpfs','/home/runner:rw,uid=10001,gid=10001,mode=0700',
        '--mount',f'type=bind,src={workspace},dst=/workspace',
        '--mount',f'type=bind,src={inputs},dst=/inputs,readonly','guild-ledger-loom-mock:local'],capture_output=True,text=True)
    assert rejected.returncode==2 and 'non-mock provider' in rejected.stderr
print('PASS: 10 native Loom mock cases: default gate, full fixture-gated pipeline, interruption/checkpoint/resume, input preservation, profile/asset/provider/image/source binding and unsafe-resume rejection; 16 stages settled with 9 completed and 7 routed out; zero model calls')

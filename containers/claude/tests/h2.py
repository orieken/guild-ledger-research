"""Fake-only Docker tests for the complete bounded H2 controller."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from h2 import execute
package=root.parents[2]/'guild-ledger-harness/package'
digest=hashlib.sha256((package/'manifest.json').read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix='guild-ledger-h2-tests-') as temp:
    temp=Path(temp);task=temp/'task';task.mkdir();(task/'starter.txt').write_text('original\n')
    prompt=temp/'prompt.txt';prompt.write_text('Only the assigned prompt.\n')
    scenarios=[
        ('pass','completed',2),('repair','completed',3),
        ('invalid-review','invalid-review',2),('invalid-path','invalid-review',2),
        ('missing-file','invalid-review',2),('review-mutation','reviewer-mutated',2),
        ('missing-usage','missing-usage',2),
        ('implementation-failure','runtime-error',1),('review-failure','runtime-error',2),('repair-failure','runtime-error',3),
        ('implementation-needs-human','needs-human',1),('review-needs-human','needs-human',2),('repair-needs-human','needs-human',3),
        ('implementation-malformed','invalid-result',1),('review-malformed','invalid-review',2),('repair-malformed','invalid-result',3)]
    for scenario,stop,count in scenarios:
        out=temp/scenario
        result=execute('guild-ledger-claude-smoke:local',task,prompt,out,package,digest,fixture=scenario)
        assert result['stop_reason']==stop,(scenario,result)
        assert len(result['stages'])==count,(scenario,result)
        assert len({s['session_id'] for s in result['stages']})==count
        assert result['model_calls']==0 and result['synthetic'] and result['cost_usd'] is None
        assert not result['evaluation_performed']
        if stop=='completed':
            assert result['known_synthetic_tokens']==18*count and result['usage_complete']
        if scenario=='missing-usage':
            assert result['known_synthetic_tokens']==18 and not result['usage_complete']
        expected='repaired\n' if count==3 else 'implemented\n'
        assert (out/'candidate/candidate.txt').read_text()==expected
        if count>=2:
            evidence=json.loads((out/'review/inputs/handoff.json').read_text())
            assert evidence['implementation']['visible_checks'][0]['synthetic']
            assert evidence['changes'] and 'diff' in evidence['changes'][0]
        if count==3:
            handoff=json.loads((out/'repair/inputs/handoff.json').read_text())
            assert handoff['review']['verdict']=='changes_requested'
        for stage in result['stages']:
            folder=out/stage['stage_id']
            assert (folder/'inputs/prompt.txt').read_bytes()==prompt.read_bytes()
            manifest=json.loads((folder/'manifest.json').read_text())
            assert manifest['network']=='none' and manifest['stage_id']==stage['stage_id']
        assert json.loads((out/'attempt.json').read_text())['stop_reason']==stop
    for budget,count in [(0,0),(18,1),(36,2)]:
        result=execute('guild-ledger-claude-smoke:local',task,prompt,temp/f'limit-{budget}',package,digest,
                       fixture='repair',max_synthetic_tokens=budget)
        assert result['stop_reason']=='limit' and len(result['stages'])==count
        assert result['known_synthetic_tokens']==18*count
    result=execute('guild-ledger-claude-smoke:local',task,prompt,temp/'timeout',package,digest,
                   fixture='implementation-timeout',wall_seconds=3)
    assert result['stop_reason']=='timeout' and len(result['stages'])==1
    assert (temp/'timeout/candidate/candidate.txt').exists()
    assert not result['usage_complete']
    result=execute('guild-ledger-claude-smoke:local',task,prompt,temp/'scope',package,digest,
                   fixture='repair',editable_prefixes=['starter.txt'])
    assert result['stop_reason']=='invalid-review' and len(result['stages'])==2
    for stage in ('review','repair'):
        stopped=execute('guild-ledger-claude-smoke:local',task,prompt,temp/(stage+'-timeout'),package,digest,
                        fixture=stage+'-timeout',wall_seconds=4)
        assert stopped['stop_reason']=='timeout'
        assert len(stopped['stages'])==(2 if stage=='review' else 3)
        remaining=[s['remaining_wall_seconds_at_start'] for s in stopped['stages']]
        assert all(a>b for a,b in zip(remaining,remaining[1:])),remaining
        assert not stopped['usage_complete']
    blocked=execute('guild-ledger-claude:2.1.304',task,prompt,temp/'real-blocked',package,digest)
    assert blocked['stop_reason']=='runtime-error' and not blocked['stages']
    assert 'synthetic runtime image' in blocked['error']
    assert not (task/'candidate.txt').exists()
print('PASS: 24 H2 controller cases: pass/repair, fresh stages, immutable review candidate, original prompts, handoffs, invalid reviews, failures, human gates, missing usage, shared limits, timeout and edit scope; zero model calls')

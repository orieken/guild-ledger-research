"""Docker integration checks. No credentials or model calls required."""
import json
import subprocess
from pathlib import Path
import runpy
import tempfile

root=Path(__file__).resolve().parents[1]
run=runpy.run_path(str(root/'run.py'))['run']
audit=runpy.run_path(str(root/'entrypoint.py'))['audit_tree']
with tempfile.TemporaryDirectory(prefix='guild-ledger-tests-') as temp:
    temp=Path(temp);task=temp/'task';task.mkdir()
    (task/'starter.txt').write_text('unchanged starter\n')
    prompt=temp/'prompt.txt';prompt.write_text('fixture task')
    for index in (1,2):
        out=temp/f'out-{index}'
        result=run('guild-ledger-claude-smoke:local',task,prompt,out)
        assert result['exit_code']==0 and result['synthetic']
        assert result['network']=='none'
        assert (out/'workspace/synthetic-result.txt').read_text()=='Synthetic edit: fixture task\n'
        events=[json.loads(line) for line in (out/'stdout.jsonl').read_text().splitlines()]
        assert events[0]['status']=='passed' and events[-1]['synthetic'] is True
    for label,limit,expected in [('__fixture_failure__',30,9),('__fixture_timeout__',2,137)]:
        prompt.write_text(label)
        result=run('guild-ledger-claude-smoke:local',task,prompt,temp/label,timeout=limit)
        assert result['exit_code']==expected,result
        assert (temp/label/'workspace/synthetic-result.txt').exists()
        if label=='__fixture_timeout__':assert result['timed_out']
    prompt.write_text('fixture task')
    assert not (task/'synthetic-result.txt').exists(), 'Host task modified'
    for filename in ('CLAUDE.md','AGENTS.md','.mcp.json'):
        contaminated=task/filename;contaminated.write_text('unapproved')
        try:audit(task)
        except ValueError:pass
        else:raise AssertionError(f'Contamination accepted: {filename}')
        contaminated.unlink()
    (task/'escape').symlink_to('/etc/passwd')
    try:audit(task)
    except ValueError:pass
    else:raise AssertionError('Symlink accepted')
    (task/'escape').unlink()
    result=run('guild-ledger-claude:2.1.304',task,prompt,temp/'cli-info',mode='cli-info',timeout=90)
    assert result['exit_code']==0 and not result['synthetic']
    text=(temp/'cli-info/stdout.jsonl').read_text()
    assert '2.1.304' in text and '--bare' in text
rejected=subprocess.run(['docker','run','--rm','--network','none','--read-only',
                         '--cap-drop','ALL','--security-opt','no-new-privileges',
                         '--env','ANTHROPIC_API_KEY=synthetic-not-a-secret',
                         'guild-ledger-claude-smoke:local','preflight'],capture_output=True,text=True)
assert rejected.returncode==2 and 'Unexpected environment keys' in rejected.stderr
assert 'synthetic-not-a-secret' not in rejected.stderr
print('PASS: two fresh offline synthetic attempts, no source mutation, rule/MCP/symlink rejection, partial artifacts after failure/timeout, real CLI version/help without inference')

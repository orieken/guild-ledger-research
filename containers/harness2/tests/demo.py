"""Offline tests for the real upstream deterministic Harness² workflow."""
import json
from pathlib import Path
import runpy
import subprocess
import tempfile

root=Path(__file__).resolve().parents[1]
execute=runpy.run_path(str(root/'run.py'))['execute']
with tempfile.TemporaryDirectory(prefix='guild-ledger-harness2-tests-') as temp:
    temp=Path(temp)
    for index in range(2):
        out=temp/f'repeat-{index}'
        result=execute('guild-ledger-harness2-demo:local',out)
        assert result['stop_reason']=='completed' and result['model_calls']==0
        assert result['model_usage'] is None and result['cost_usd'] is None
        summary=result['demo_summary']
        assert summary['n_tasks']==2 and summary['done']==2 and summary['failed']==0
        assert summary['execution_count']==28 and summary['editor_calls']==32
        assert summary['tasks'][0]['library_entries_before']=={'agg':0,'seq':0}
        assert summary['tasks'][1]['library_entries_before']=={'agg':1,'seq':1}
        demo=out/'workspace/demo'
        for mode in ('agg','seq'):
            library=demo/'library/k2'/mode/'accounting/INDEX.md'
            assert library.exists() and library.read_text().strip()
            for task,total in [('ledger-1','85.15'),('ledger-2','20.25')]:
                # Both modes' final compositions include signed amounts.
                final='agg2' if mode=='agg' else 'c2'
                answer=demo/f'executions/demo-oc-{mode}2'/task/final/'answer.txt'
                assert answer.read_text().strip()=='Total: '+total
    for image,digest in [('guild-ledger-claude:2.1.304',None),('guild-ledger-harness2-demo:local','0'*64)]:
        try:
            kwargs={} if digest is None else {'profile_digest':digest}
            execute(image,temp/('rejected-'+image.split(':')[0]),**kwargs)
        except ValueError:pass
        else:raise AssertionError('Wrong image/profile accepted')
    for dirty in (False,True):
        workspace=temp/('dirty' if dirty else 'env');workspace.mkdir();workspace.chmod(0o777)
        if dirty:(workspace/'unexpected.txt').write_text('inherited state')
        cmd=['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL',
             '--security-opt','no-new-privileges','--tmpfs','/home/runner:rw,uid=10001,gid=10001,mode=0700',
             '--mount',f'type=bind,src={workspace},dst=/workspace']
        if not dirty:cmd+=['--env','OPENAI_API_KEY=synthetic-not-a-secret']
        result=subprocess.run(cmd+['guild-ledger-harness2-demo:local'],capture_output=True,text=True)
        assert result.returncode!=0
        assert ('Fresh home/workspace' if dirty else 'External configuration') in result.stderr
        assert 'synthetic-not-a-secret' not in result.stderr
    timed=execute('guild-ledger-harness2-demo:local',temp/'timeout',timeout=.01)
    assert timed['stop_reason']=='timeout' and timed['model_calls']==0
    assert (temp/'timeout/attempt.json').exists()
print('PASS: 7 Harness² cases: repeated fresh deterministic demos, native library transfer, final compositions, wrong image/profile, external credentials, dirty workspace and timeout rejection; zero model calls')

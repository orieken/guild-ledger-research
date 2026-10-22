"""Offline package and Docker exposure tests; never execute a model."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from treatment import load_package, assemble, validate_review
run = runpy.run_path(str(root/'run.py'))['run']
p = argparse.ArgumentParser()
p.add_argument('--h1', type=Path, default=root.parents[2]/'guild-ledger-guidelines/package')
p.add_argument('--h2', type=Path, default=root.parents[2]/'guild-ledger-harness/package')
a = p.parse_args()


def rejected(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError('Invalid input accepted')


with tempfile.TemporaryDirectory(prefix='guild-ledger-treatments-') as temp:
    temp = Path(temp)
    task = temp/'task'; task.mkdir(); (task/'starter.txt').write_text('unchanged')
    prompt = temp/'prompt.txt'; prompt.write_bytes(b'Assigned prompt only.\n')
    records = {}
    assert (a.h1/'guidelines.md').read_bytes() == (a.h2/'guidelines.md').read_bytes()
    for hid, source in [('H1', a.h1), ('H2', a.h2)]:
        digest = hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest()
        package = load_package(source, digest, hid)
        records[hid] = package
        rejected(lambda: load_package(source, '0'*64, hid))
        rejected(lambda: load_package(source, digest, 'H2' if hid == 'H1' else 'H1'))
        copied = temp/hid; shutil.copytree(source, copied)
        (copied/'guidelines.md').write_text('tampered')
        rejected(lambda: load_package(copied, digest, hid))
        (copied/'guidelines.md').write_bytes((source/'guidelines.md').read_bytes())
        (copied/'extra.md').write_text('undeclared')
        rejected(lambda: load_package(copied, digest, hid))
        (copied/'extra.md').unlink()
        (copied/'guidelines.md').unlink()
        rejected(lambda: load_package(copied, digest, hid))
        out = temp/(hid+'-attempt')
        result = run('guild-ledger-claude-smoke:local', task, prompt, out,
                     harness=source, harness_digest=digest, harness_id=hid)
        assert result['exit_code'] == 0
        assert result['stage_execution_implemented'] is False
        assert result['harness_id'] == hid and result['harness_manifest_sha256'] == digest
        assert result['network'] == 'none'
        assembled = (out/'inputs/assembled-prompt.txt').read_bytes()
        assert assembled.startswith(prompt.read_bytes())
        assert assembled.count(b'# H1 coding guidelines') == 1
        assert assembled == assemble(prompt.read_bytes(), source, package)
        events = [json.loads(line) for line in (out/'stdout.jsonl').read_text().splitlines()]
        exposed = next(e for e in events if e['type'] == 'runner_treatment')
        assert exposed['harness_id'] == hid
        assert exposed['assembled_prompt_sha256'] == result['assembled_prompt_sha256']
        assert not (out/'workspace/guidelines.md').exists()
        bad_inputs = temp/(hid+'-tampered-inputs')
        shutil.copytree(out/'inputs', bad_inputs)
        (bad_inputs/'treatment/guidelines.md').write_text('changed after host assembly')
        rejected_container = subprocess.run(['docker','run','--rm','--network','none','--read-only',
            '--cap-drop','ALL','--security-opt','no-new-privileges',
            '--mount',f'type=bind,src={bad_inputs},dst=/inputs,readonly',
            'guild-ledger-claude-smoke:local','preflight'],capture_output=True,text=True)
        assert rejected_container.returncode == 2
        assert 'Input exposure digest/file-set mismatch' in rejected_container.stderr
    assert assemble(prompt.read_bytes()) == prompt.read_bytes(), 'H0 gained instructions'
    h2 = records['H2']
    assert b'# Review stage' in assemble(prompt.read_bytes(), a.h2, h2, 'review')
    assert b'# Repair stage' in assemble(prompt.read_bytes(), a.h2, h2, 'repair')
    assert not (task/'synthetic-result.txt').exists()
    # Re-hashing a mutated policy must not bypass the fixed treatment contract.
    bad = temp/'bad-policy'; shutil.copytree(a.h2, bad)
    m = json.loads((bad/'manifest.json').read_text()); m['policy']['max_repair_sessions'] = 99
    (bad/'manifest.json').write_text(json.dumps(m))
    rejected(lambda: load_package(bad, hashlib.sha256((bad/'manifest.json').read_bytes()).hexdigest(), 'H2'))
    rejected(lambda: run('unused', task, prompt, temp/'unpinned', harness=a.h1, harness_id='H1'))
    assert validate_review({'schema_version':'guild-ledger.h2-review/v1','verdict':'pass','findings':[]}) == 'pass'
    finding = {'id':'F1','severity':'medium','file':'src/example.py','line':1,
               'issue':'Synthetic defect','evidence':'Synthetic observation','requested_change':'Synthetic fix'}
    review = {'schema_version':'guild-ledger.h2-review/v1','verdict':'changes_requested','findings':[finding]}
    assert validate_review(review) == 'changes_requested'
    rejected(lambda: validate_review(dict(review, verdict='pass')))
    rejected(lambda: validate_review(dict(review, findings=[dict(finding, file='../escape')])) )
    rejected(lambda: validate_review(dict(review, findings=[finding, finding])))
print('PASS: H1/H2 package hashes, identical guidelines, H0 byte preservation, explicit container exposure, tamper/extra/policy rejection, stage assembly and review contract; no stage orchestration or model calls')

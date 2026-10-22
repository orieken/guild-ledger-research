"""Explicit, pinned H1/H2 package loading; no automatic instruction discovery."""
import hashlib
import json
from pathlib import Path
import re

ASSETS = {'H1': {'guidelines.md'}, 'H2': {'guidelines.md', 'workflow.md', 'implementation.md', 'review.md', 'repair.md'}}
STAGES = {'H1': [('coding', ['guidelines.md'])], 'H2': [
    ('implementation', ['guidelines.md', 'workflow.md', 'implementation.md']),
    ('review', ['guidelines.md', 'workflow.md', 'review.md']),
    ('repair', ['guidelines.md', 'workflow.md', 'repair.md'])]}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_package(root, expected_digest, expected_id):
    if expected_id not in ASSETS or not re.fullmatch('[0-9a-f]{64}', expected_digest or ''):
        raise ValueError('H1/H2 package requires an explicit manifest SHA-256 and harness ID')
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Package must be a real directory')
    expected_files = ASSETS[expected_id] | {'manifest.json'}
    actual = set()
    for p in root.rglob('*'):
        if p.is_symlink() or not p.is_file():
            raise ValueError('Package may contain only regular, declared files')
        actual.add(str(p.relative_to(root)))
    if actual != expected_files:
        raise ValueError('Package file set differs from the treatment contract')
    raw = (root / 'manifest.json').read_bytes()
    if sha(raw) != expected_digest:
        raise ValueError('Package manifest digest mismatch')
    manifest = json.loads(raw)
    if manifest.get('schema_version') != 'guild-ledger.harness-package/v1' or manifest.get('harness_id') != expected_id:
        raise ValueError('Package identity mismatch')
    assets = manifest.get('assets', {})
    if set(assets) != ASSETS[expected_id]:
        raise ValueError('Unexpected assets')
    for name, digest in assets.items():
        data = (root / name).read_bytes()
        if not data or sha(data) != digest:
            raise ValueError(f'Asset digest mismatch: {name}')
        data.decode('utf-8')
    expected_stages = [{'id': sid, 'instructions': names, 'fresh_session': True} for sid, names in STAGES[expected_id]]
    expected_policy = {'review_sessions': int(expected_id == 'H2'), 'max_repair_sessions': int(expected_id == 'H2'),
                       'recursive_agents': False, 'model_and_effort': 'same-as-campaign',
                       'limits': 'shared-aggregate-attempt-allowance', 'private_evaluator_access': False,
                       'product_requirements_added': False}
    if (manifest.get('stages') != expected_stages or manifest.get('initial_stage') != expected_stages[0]['id']
            or manifest.get('policy') != expected_policy or manifest.get('tools_added') != [] or manifest.get('skills_added') != []):
        raise ValueError('Stage, tools or policy contract mismatch')
    return manifest


def assemble(prompt, root=None, manifest=None, stage_id=None):
    """Preserve H0 bytes; append explicit treatment assets for the chosen stage."""
    if manifest is None:
        return prompt
    stage_id = stage_id or manifest['initial_stage']
    stage = next((s for s in manifest['stages'] if s['id'] == stage_id), None)
    if stage is None:
        raise ValueError('Undeclared stage')
    text = prompt.decode('utf-8')
    for name in stage['instructions']:
        text += f'\n\n--- BEGIN TREATMENT ASSET: {name} ---\n'
        text += (root / name).read_text()
        text += f'--- END TREATMENT ASSET: {name} ---\n'
    return text.encode('utf-8')


def validate_review(value):
    """Validate control data only; findings remain untrusted agent claims."""
    if not isinstance(value, dict) or set(value) != {'schema_version', 'verdict', 'findings'}:
        raise ValueError('Invalid review fields')
    if value['schema_version'] != 'guild-ledger.h2-review/v1' or value['verdict'] not in {'pass', 'changes_requested'}:
        raise ValueError('Invalid review identity/verdict')
    findings = value['findings']
    if not isinstance(findings, list) or ((value['verdict'] == 'pass') != (len(findings) == 0)):
        raise ValueError('Review verdict/findings mismatch')
    ids = set()
    for f in findings:
        if not isinstance(f, dict) or set(f) != {'id', 'severity', 'file', 'line', 'issue', 'evidence', 'requested_change'}:
            raise ValueError('Invalid finding fields')
        if any(not isinstance(f[k], str) or not f[k].strip() for k in ('id', 'file', 'issue', 'evidence', 'requested_change')):
            raise ValueError('Finding text required')
        path = Path(f['file'])
        if path.is_absolute() or '..' in path.parts or '\\' in f['file'] or f['file'] == '.':
            raise ValueError('Finding path must be workspace-relative')
        if f['severity'] not in {'high', 'medium', 'low'} or f['id'] in ids:
            raise ValueError('Invalid severity or duplicate finding ID')
        if f['line'] is not None and (type(f['line']) is not int or f['line'] < 1):
            raise ValueError('Invalid finding line')
        ids.add(f['id'])
    return value['verdict']

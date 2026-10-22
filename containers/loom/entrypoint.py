"""Native Loom mock-only command boundary. No arbitrary CLI flags or providers."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import subprocess


def main():
    if os.getuid()==0 or shutil.which('claude') or Path('/var/run/docker.sock').exists():
        raise ValueError('Non-root, no Claude binary, no Docker socket required')
    if any(Path.home().iterdir()):raise ValueError('A fresh empty home is required')
    for key in os.environ:
        if key.startswith(('ANTHROPIC_','AWS_','GOOGLE_','GH_','GITHUB_','OTEL_')):
            raise ValueError('Unexpected external configuration key: '+key)
    inputs=Path('/inputs')
    expected={'manifest.json','mock-spec.md','request.json'}
    if (inputs/'task-prompt.txt').exists():expected.add('task-prompt.txt')
    if {p.name for p in inputs.iterdir()}!=expected:
        raise ValueError('Unexpected input set')
    if any(p.is_symlink() or not p.is_file() for p in inputs.iterdir()):
        raise ValueError('Only regular inputs allowed')
    lock=json.loads(Path('/opt/loom/source-lock.json').read_text())
    raw=(inputs/'manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=lock['profile_manifest_sha256']:
        raise ValueError('Profile digest does not match built binary source lock')
    profile=json.loads(raw)
    if profile['provider']!='mock' or profile['real_provider_enabled'] is not False:
        raise ValueError('Only mock provider allowed')
    for name,digest in profile['assets'].items():
        if name!='mock-spec.md' or hashlib.sha256((inputs/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Profile asset mismatch')
    request=json.loads((inputs/'request.json').read_text())
    if set(request)!={'resume','approve','fixture_approval','hang'} or type(request['resume']) is not bool:
        raise ValueError('Invalid request')
    gate=request['approve']
    if gate and (not request['resume'] or request['fixture_approval'] is not True or gate not in profile['gates']):
        raise ValueError('Approval allowed only as an explicit synthetic resume fixture')
    if request['hang'] not in (None,'context-engineer'):
        raise ValueError('Unknown hang fixture')
    state=Path('/workspace/.claude/feature-workspace/mock-spec/run-state.json')
    if state.exists() and json.loads(state.read_text()).get('provider')!='mock':
        raise ValueError('Refuse resume state with non-mock provider')
    if os.environ.get('T01_OFFLINE_TOOLS')=='1' and not request['resume']:
        subprocess.run(['python3','/opt/t01/visible_checks.py','--expect-starter-red'],check=True)
    # A disposable synthetic baseline lets native posture/diff checks run.
    # No host repository, identity, hooks or Git configuration is copied.
    os.environ.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',
                      GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='safe.directory',GIT_CONFIG_VALUE_0='/workspace')
    if not request['resume'] and not Path('/workspace/.git').exists():
        subprocess.run(['git','init','--quiet','/workspace'],check=True)
        subprocess.run(['git','-C','/workspace','-c','core.hooksPath=/dev/null','add','--all'],check=True)
        subprocess.run(['git','-C','/workspace','-c','core.hooksPath=/dev/null',
                        '-c','user.name=Synthetic fixture','-c','user.email=fixture@example.invalid',
                        'commit','--quiet','--allow-empty','-m','Synthetic mock baseline'],check=True)
    spec='/inputs/mock-spec.md'
    task_prompt=inputs/'task-prompt.txt'
    if task_prompt.exists():
        # Keep the native mock-spec slug and all gates; only carry task data.
        combined=Path('/tmp/mock-spec.md')
        combined.write_bytes((inputs/'mock-spec.md').read_bytes()+b'\n\nAssigned task (mock transport only):\n'+task_prompt.read_bytes())
        spec=str(combined)
        print(json.dumps({'type':'loom_task_input','sha256':hashlib.sha256(task_prompt.read_bytes()).hexdigest(),'mock_ignores_product_requirements':True}),flush=True)
    args=['/usr/local/bin/loom','run','--spec',spec,'--provider','mock']
    if request['resume']:args+=['--resume']
    if gate:args+=['--approve',gate]
    if request['hang']:args+=['--mock-hang-stage',request['hang']]
    print(json.dumps({'type':'loom_mock_launch','provider':'mock','source_commit':lock['commit'],
                      'resume':request['resume'],'synthetic_approval':gate or None}),flush=True)
    os.execv(args[0],args)


if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('Loom mock runner rejected: '+str(exc),file=sys.stderr)
        sys.exit(2)

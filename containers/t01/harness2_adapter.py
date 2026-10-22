"""T01 no-op solver using the pinned native Harness² recursion/selection engine.

No model client, benchmark judge, solution or private criteria is installed.
The scripted proposer changes a synthetic harness note; every solver rollout
returns the supplied starter unchanged. This is plumbing evidence only.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

INITIAL_ENV=tuple(os.environ)

from harness2.core import tree
from harness2.core.proposer import Proposer, Reply
from harness2.core.schedule import run_task
from harness2.core.spec import BenchPrompts, BenchSpec, ChannelSpec
from harness2.substrate.opencode import OpencodeSubstrate

def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}

class Adapter:
    def __init__(self):
        self.root=Path('/workspace/native');self.substrate=OpencodeSubstrate()
        channel=ChannelSpec('opencode','local/deterministic')
        self.spec=BenchSpec(name='guild-t01-mock',runs_root=self.root/'runs',install_mode='workspace_config',prompts=BenchPrompts(work='browse guild quests'),channels={'proposer':channel,'selector':channel})
        base={name:'' for name in self.substrate.surface().always_on}
        base['systemprompt.md']='Mock-only: preserve the supplied source.\n'
        tree.write_tree(self.substrate.surface(),base,self.base_harness(),stubs=False)
    def tasks(self,split='all'):return ['T01']
    def domain_of(self,task_id):return 'guild-ledger'
    def task_prompt(self,task_id):return Path('/inputs/prompt.txt').read_text()
    def task_files(self,task_id):return Path('/task')
    def base_harness(self):return self.root/'base'
    def validate_tree(self,harness):
        if not harness.get('systemprompt.md'):raise ValueError('Mock system prompt required')
    def execute(self,task_id,harness_dir,run_id,*,timeout=None):
        run=self.root/'executions'/run_id;run.mkdir(parents=True,exist_ok=True)
        shutil.copytree(self.task_files(task_id),run/'candidate')
        data={'synthetic':True,'model_calls':0,'task_prompt_sha256':hashlib.sha256(Path('/inputs/prompt.txt').read_bytes()).hexdigest(),'files':hashes(run/'candidate')}
        (run/'delivery.json').write_text(json.dumps(data,indent=2)+'\n')
        (run/'trajectory.md').write_text('[ACTION] Return supplied source unchanged using the deterministic mock solver.\n[OBSERVATION] Candidate source exported; visible tests run separately by the trusted supervisor.\n')
        return run
    def delivered(self,run_dir):return (run_dir/'delivery.json').is_file()
    def trajectory(self,run_dir,*,obs_trunc):return (run_dir/'trajectory.md').read_text()[:obs_trunc]
    def deliverable_text(self,run_dir):return (run_dir/'delivery.json').read_text()
    def deliverable_files(self,run_dir):return {'delivery.json':self.deliverable_text(run_dir)}

class ScriptedProposer(Proposer):
    def call(self,mission,context_dir,label,**kwargs):
        context=Path(context_dir);workspace=None
        if label.startswith('select.'):
            chosen=sorted((context/'candidates').glob('*.md'))[0].stem
            text=f'<why>All mock candidates preserve the supplied input; choose first deterministically.</why>\n```choice\n{chosen}\n```'
        elif label.startswith('experience.'):
            text='NO_ENTRY'
        else:
            workspace=context/'harness';p=workspace/'systemprompt.md'
            p.write_text(p.read_text()+'Synthetic no-op adaptation note.\n')
            text='<notes>Transport-only mock; source remains unchanged.</notes>'
        reply=Reply(label=label,text=text,ok=True,attempts=1,workspace=workspace)
        self._calls.append(reply);return reply

def main():
    if os.getuid()==0 or any(Path.home().iterdir()) or any(Path('/workspace').iterdir()):raise ValueError('Fresh non-root worker required')
    if any(shutil.which(n) for n in ('claude','codex','opencode','gcloud')):raise ValueError('No model binaries allowed')
    if any(n.startswith(('ANTHROPIC_','OPENAI_','GOOGLE_','GEMINI_','AWS_','GH_','GITHUB_','HARNESS2_')) for n in INITIAL_ENV):raise ValueError('External config forbidden')
    if Path('/var/run/docker.sock').exists():raise ValueError('No Docker socket allowed')
    if {p.name for p in Path('/inputs').iterdir()}!={'prompt.txt'}:raise ValueError('Only assigned prompt input allowed')
    profile=json.loads(Path('/opt/profile.json').read_text())
    if profile['model_backed_execution_enabled'] is not False:raise ValueError('Mock profile required')
    if os.environ.get('T01_OFFLINE_TOOLS')=='1':
        # /task is read-only; the common tool reads application source at /workspace.
        shutil.copytree('/task/web', '/workspace/web')
        shutil.copytree('/task/services', '/workspace/services')
        subprocess.run(['python3','/opt/t01/visible_checks.py','--expect-starter-red'],check=True)
        shutil.rmtree('/workspace/web');shutil.rmtree('/workspace/services')
    adapter=Adapter();proposer=ScriptedProposer(adapter.spec.channels['proposer'])
    result=run_task('T01',2,adapter=adapter,prop=proposer,runs_root=adapter.spec.runs_root,modes=('agg','seq'))
    if result.errors:raise ValueError(str(result.errors))
    original=hashes(Path('/task'))
    selected={}
    for mode,selection in result.selections.items():
        candidate=Path(selection['chosen_run_dir'])/'candidate'
        if hashes(candidate)!=original:raise ValueError('No-op mock changed source')
        selected[mode]=selection['chosen_run_dir']
    if set(selected)!={'agg','seq'}:raise ValueError('Both native modes required')
    shutil.copytree(Path(selected['agg'])/'candidate',Path('/workspace/candidate'))
    report={'synthetic':True,'model_calls':0,'model_usage':None,'cost_usd':None,'source_unchanged':True,'task_prompt_sha256':hashlib.sha256(Path('/inputs/prompt.txt').read_bytes()).hexdigest(),'selected':selected,'editor_calls':len(proposer._calls),'execution_count':len(list(adapter.root.glob('executions/**/delivery.json'))),'library_learning_exercised':False,'scope':'Native k=2 parallel/sequential recursion and selection; no-op solver, no experience library learning.'}
    Path('/workspace/report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()

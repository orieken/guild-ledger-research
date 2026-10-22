"""Fixed upstream deterministic demo only. Does not expose benchmark CLIs."""
import json
import os
from pathlib import Path
import shutil


def main():
    if os.getuid()==0:raise ValueError('Non-root runner required')
    if any(Path.home().iterdir()) or any(Path('/workspace').iterdir()):raise ValueError('Fresh home/workspace required')
    if any(shutil.which(name) for name in ('claude','codex','opencode','gcloud')):raise ValueError('No model executor permitted')
    for name in os.environ:
        if name.startswith(('ANTHROPIC_','OPENAI_','GOOGLE_','GEMINI_','AWS_','GH_','GITHUB_','HARNESS2_')):
            raise ValueError('External configuration not permitted: '+name)
    profile=json.loads(Path('/opt/profile.json').read_text())
    if profile['model_backed_execution_enabled'] is not False or profile['entrypoint']!='harness2.cli.demo':
        raise ValueError('Unsupported profile')
    os.execv('/usr/local/bin/python',['python','-m','harness2.cli.demo','--output','/workspace/demo',
                                     '--k',str(profile['k']),'--mode',profile['mode']])


if __name__=='__main__':main()

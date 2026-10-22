"""Export reviewed tracked source only; no installation or model execution."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def prepare(source,package,digest):
    raw=(package/'manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Profile manifest mismatch')
    profile=json.loads(raw)
    if profile.get('schema_version')!='guild-ledger.harness2-profile/v1' or profile.get('model_backed_execution_enabled') is not False:
        raise ValueError('Only deterministic profile supported')
    pin=profile['source']
    tree=subprocess.check_output(['git','rev-parse',pin['commit']+'^{tree}'],cwd=source,text=True).strip()
    if tree!=pin['tree']:raise ValueError('Source tree mismatch')
    build=Path(__file__).resolve().parent/'build';build.mkdir(exist_ok=True)
    archive=build/'source.tar.gz'
    subprocess.run(['git','archive','--format=tar.gz','--output='+str(archive),pin['commit']],cwd=source,check=True)
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=pin['archive_sha256']:raise ValueError('Archive mismatch')
    (build/'manifest.json').write_bytes(raw)
    print('Verified pinned Harness² source export')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','package'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--digest',required=True);a=p.parse_args();prepare(a.source,a.package,a.digest)

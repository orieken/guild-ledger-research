#!/usr/bin/env python3
"""Export only the pinned tracked Loom source; never build from a personal tree."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def prepare(source, package, expected_digest):
    raw=(package/'manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_digest:
        raise ValueError('Loom package digest mismatch')
    manifest=json.loads(raw)
    if (manifest.get('schema_version')!='guild-ledger.loom-profile/v1' or manifest.get('provider')!='mock'
        or manifest.get('plan')!='deliver-feature' or manifest.get('real_provider_enabled') is not False):
        raise ValueError('Only the pinned native/mock profile is supported')
    for name,digest in manifest['assets'].items():
        if name!='mock-spec.md' or (package/name).is_symlink() or hashlib.sha256((package/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Loom asset mismatch')
    pin=manifest['source']
    actual=subprocess.check_output(['git','rev-parse',pin['commit']+'^{tree}'],cwd=source,text=True).strip()
    if actual!=pin['tree']:raise ValueError('Source tree mismatch')
    build=Path(__file__).resolve().parent/'build';build.mkdir(exist_ok=True)
    archive=build/'loom-source.tar.gz'
    subprocess.run(['git','archive','--format=tar.gz','--output='+str(archive),pin['commit']],cwd=source,check=True)
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=pin['archive_sha256']:
        raise ValueError('Source archive digest mismatch')
    lock=dict(pin,profile_manifest_sha256=expected_digest,profile='native-mock',provider='mock')
    (build/'source-lock.json').write_text(json.dumps(lock,indent=2)+'\n')
    return lock


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--package',type=Path,required=True)
    p.add_argument('--manifest-digest',required=True)
    a=p.parse_args();print(json.dumps(prepare(a.source,a.package,a.manifest_digest),indent=2))

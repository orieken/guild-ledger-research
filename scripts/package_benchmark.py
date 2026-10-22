#!/usr/bin/env python3
"""Export only reviewed T01 inputs; deterministic archive, external evidence."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import shutil
ROOT=Path(__file__).resolve().parents[1]
IGNORED={'.git','node_modules','dist','__pycache__','.venv'}
def sha(data): return hashlib.sha256(data).hexdigest()
def package(level,output):
    if level not in ('P1','P2','P3'): raise ValueError('Invalid level')
    source=ROOT/'benchmarks/T01/starter'
    output=Path(output).absolute()
    if output.exists(): raise ValueError('Output must not exist')
    if source.resolve() in output.resolve().parents: raise ValueError('Output cannot be inside starter')
    files=[]
    for path in sorted(source.rglob('*')):
        rel=path.relative_to(source)
        if any(part in IGNORED for part in rel.parts): continue
        if path.is_symlink(): raise ValueError('Symlinks not permitted')
        if path.is_dir(): continue
        if not path.is_file(): raise ValueError('Special files not permitted')
        files.append((rel.as_posix(),path.read_bytes()))
    buffer=io.BytesIO()
    with gzip.GzipFile(fileobj=buffer,mode='wb',mtime=0,filename='') as gz:
        with tarfile.open(fileobj=gz,mode='w',format=tarfile.USTAR_FORMAT) as tar:
            for name,data in files:
                info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;info.mtime=0
                tar.addfile(info,io.BytesIO(data))
    prompt=(ROOT/'benchmarks/T01/prompts/envelope.md').read_bytes()+b'\n'+(ROOT/f'benchmarks/T01/prompts/{level}.md').read_bytes()
    manifest={'schema':'guild-ledger.task-bundle/v1','task':'T01','prompt_level':level,'status':'draft-unfrozen','source_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()),'starter_sha256':sha(buffer.getvalue()),'prompt_sha256':sha(prompt),'files':{name:sha(data) for name,data in files},'live_model_calls_enabled':False}
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temp:
        staging=Path(temp)/'bundle';staging.mkdir();(staging/'workspace').mkdir()
        for name,data in files:
            target=staging/'workspace'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        (staging/'starter.tar.gz').write_bytes(buffer.getvalue());(staging/'prompt.txt').write_bytes(prompt)
        (staging/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        staging.rename(output)
    return manifest
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--level',choices=['P1','P2','P3'],required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();print(json.dumps(package(args.level,args.output),indent=2))

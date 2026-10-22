"""Verify source snapshot identity and safe archive handling without models."""
import hashlib
import io
import json
from pathlib import Path
import runpy
import shutil
import tarfile
import tempfile

root=Path(__file__).resolve().parents[1]
prepare=runpy.run_path(str(root/'prepare.py'))['prepare']
package=root.parents[2]/'guild-ledger-loom/package'
snapshot=root.parents[1]/'vendor/loom/loom-3f2817818c68.tar.gz'
digest=hashlib.sha256((package/'manifest.json').read_bytes()).hexdigest()
lock=prepare(None,package,digest,snapshot)
assert lock['archive_sha256']==hashlib.sha256(snapshot.read_bytes()).hexdigest()


def rejected(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Unsafe snapshot accepted')


with tempfile.TemporaryDirectory() as temp:
    temp=Path(temp)
    bad=temp/'tampered.tar.gz';bad.write_bytes(snapshot.read_bytes()+b'altered')
    rejected(lambda:prepare(None,package,digest,bad))
    for kind in ('traversal','symlink'):
        archive=temp/(kind+'.tar.gz')
        with tarfile.open(archive,'w:gz') as tar:
            entry=tarfile.TarInfo('../../escape' if kind=='traversal' else 'unsafe-link')
            if kind=='symlink':entry.type=tarfile.SYMTYPE;entry.linkname='/outside'
            else:entry.size=1
            tar.addfile(entry,None if kind=='symlink' else io.BytesIO(b'x'))
        fixture=temp/kind;shutil.copytree(package,fixture)
        manifest=json.loads((fixture/'manifest.json').read_text())
        manifest['source']['archive_sha256']=hashlib.sha256(archive.read_bytes()).hexdigest()
        (fixture/'manifest.json').write_text(json.dumps(manifest))
        fixture_digest=hashlib.sha256((fixture/'manifest.json').read_bytes()).hexdigest()
        rejected(lambda:prepare(None,fixture,fixture_digest,archive))
assert lock==json.loads((root/'build/source-lock.json').read_text())
print('PASS: exact source snapshot, tampered digest, path traversal and external symlink checks; no model calls')

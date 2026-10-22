"""Meaningful trust-boundary checks without Docker or model calls."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from package_benchmark import ROOT, package
import t01_harness_smoke as runner
class Boundaries(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  bundle=self.root/'bundle';package('P1',bundle);self.canonical=bundle/'workspace'
  self.source=self.root/'source';shutil.copytree(self.canonical,self.source)
 def project(self):return runner.project_candidate(self.source,self.canonical,self.root/'projected')
 def test_rejects_modified_protected_test(self):
  (self.source/'web/tests/quests.test.ts').write_text('always pass')
  with self.assertRaisesRegex(ValueError,'Protected input'):self.project()
 def test_rejects_modified_fixtures(self):
  (self.source/'fixtures/quests.json').write_text('[]')
  with self.assertRaisesRegex(ValueError,'Protected input'):self.project()
 def test_rejects_missing_lock(self):
  (self.source/'web/package-lock.json').unlink()
  with self.assertRaisesRegex(ValueError,'Missing canonical'):self.project()
 def test_rejects_source_symlink(self):
  path=self.source/'web/src/App.vue';path.unlink();path.symlink_to('/etc/passwd')
  with self.assertRaisesRegex(ValueError,'symlink'):self.project()
 def test_rejects_directory_symlink(self):
  path=self.source/'web/src';shutil.rmtree(path);path.symlink_to(self.canonical/'web/src',target_is_directory=True)
  with self.assertRaisesRegex(ValueError,'symlink'):self.project()
 def test_rejects_workspace_symlink(self):
  path=self.root/'link';path.symlink_to(self.source,target_is_directory=True)
  with self.assertRaisesRegex(ValueError,'root'):runner.project_candidate(path,self.canonical,self.root/'projected')
 def test_preserves_editable_source_but_excludes_native_state(self):
  (self.source/'web/src/App.vue').write_text('<template>changed</template>')
  (self.source/'.claude').mkdir();(self.source/'.claude/private-output').write_text('native metadata')
  (self.source/'web/src/new.ts').write_text('export const x=1')
  files=self.project()
  self.assertEqual((self.root/'projected/web/src/App.vue').read_text(),'<template>changed</template>')
  self.assertIn('web/src/new.ts',files);self.assertFalse((self.root/'projected/.claude').exists())
 def test_h4_model_image_rejected_before_launch(self):
  with patch.object(runner,'identity',return_value={'Config':{'Env':['RUNNER_KIND=claude']}}):
   with self.assertRaisesRegex(ValueError,'deterministic'):runner.worker('model-image',self.source,self.root/'prompt',self.root/'output')
if __name__=='__main__':unittest.main(verbosity=2)

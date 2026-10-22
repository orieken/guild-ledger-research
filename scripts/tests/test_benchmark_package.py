import importlib.util
import sys
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from package_benchmark import package
class Packaging(unittest.TestCase):
 def test_repeatable_and_prompt_separation(self):
  with tempfile.TemporaryDirectory() as temp:
   base=Path(temp)
   a=package('P1',base/'a');b=package('P1',base/'b');c=package('P3',base/'c')
   self.assertEqual((base/'a/starter.tar.gz').read_bytes(),(base/'b/starter.tar.gz').read_bytes())
   self.assertEqual(a['starter_sha256'],c['starter_sha256'])
   self.assertNotEqual(a['prompt_sha256'],c['prompt_sha256'])
   self.assertFalse(any('reference' in f or 'prompts' in f or 'requirements.json' in f for f in a['files']))
   self.assertFalse(a['live_model_calls_enabled'])
   with self.assertRaises(ValueError): package('P1',base/'a')
 def test_container_input_audit(self):
  import runpy
  sys.path.insert(0,str(ROOT/'containers/claude'))
  audit=runpy.run_path(str(ROOT/'containers/claude/entrypoint.py'))['audit_tree']
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'bundle';package('P2',path);audit(path/'workspace')
if __name__=='__main__': unittest.main(verbosity=2)

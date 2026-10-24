"""Evaluator result integrity and leak isolation, not replicas of product logic."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'evaluators/T01'));sys.path.insert(0,str(ROOT/'scripts'))
from evaluate import aggregate, evaluate
from package_benchmark import package
INVENTORY=json.loads((ROOT/'evaluators/T01/criteria.json').read_text())['criteria']
def observations():return {'status':'completed','results':[{'id':r['id'],'requirements':r['requirements'],'status':'pass'} for r in INVENTORY]}
class EvaluatorIntegrity(unittest.TestCase):
 def test_full_pass_requires_every_criterion(self):
  result=observations();self.assertTrue(aggregate(result,[])['full_target_acceptance'])
  result['results'].pop()
  with self.assertRaises(ValueError):aggregate(result,[])
 def test_one_failure_rejects_full_target(self):
  result=observations();result['results'][0]['status']='fail';self.assertFalse(aggregate(result,[])['full_target_acceptance'])
 def test_duplicate_id_cannot_inflate_success(self):
  result=observations();result['results'][-1]=result['results'][0]
  with self.assertRaises(ValueError):aggregate(result,[])
 def test_evaluator_error_is_not_a_candidate_zero(self):
  result=observations();result['status']='evaluator_error'
  with self.assertRaises(ValueError):aggregate(result,[])
 def test_unknown_outcome_and_requirement_mismatch_rejected(self):
  for key,value in [('status','skip'),('requirements',['R999'])]:
   result=observations();result['results'][0][key]=value
   with self.assertRaises(ValueError):aggregate(result,[])
 def test_subset_never_claims_full_acceptance(self):
  result=observations();result['results']=result['results'][:1]
  report=aggregate(result,[INVENTORY[0]['id']]);self.assertIsNone(report['full_target_acceptance']);self.assertTrue(report['diagnostic_passed'])
 def test_unknown_selection_rejected_before_launch(self):
  with tempfile.TemporaryDirectory() as temp:
   with self.assertRaises(ValueError):evaluate(ROOT/'benchmarks/T01/starter',Path(temp)/'output',['unknown'])
 def test_all_prompt_bundles_exclude_private_evaluator_and_reference(self):
  import tarfile
  with tempfile.TemporaryDirectory() as temp:
   for level in ('P1','P2','P3'):
    dest=Path(temp)/level;manifest=package(level,dest)
    with tarfile.open(dest/'starter.tar.gz') as archive:names=archive.getnames()
    self.assertEqual(set(names),set(manifest['files']))
    self.assertFalse(any('evaluat' in n or 'reference' in n or 'mutation' in n for n in names))
    self.assertNotIn('criteria.json',(dest/'prompt.txt').read_text())
if __name__=='__main__':unittest.main(verbosity=2)

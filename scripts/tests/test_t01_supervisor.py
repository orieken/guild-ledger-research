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
  with self.assertRaisesRegex(ValueError,'source directory'):self.project()
 def test_empty_frontend_keeps_mount_directory(self):
  shutil.rmtree(self.source/'web/src');(self.source/'web/src').mkdir()
  self.project();self.assertTrue((self.root/'projected/web/src').is_dir())
 def test_allows_frontend_component_rename(self):
  (self.source/'web/src/App.vue').rename(self.source/'web/src/QuestBrowser.vue')
  p=self.source/'web/src/main.ts';p.write_text(p.read_text().replace('./App.vue','./QuestBrowser.vue'))
  files=self.project();self.assertNotIn('web/src/App.vue',files);self.assertIn('web/src/QuestBrowser.vue',files)
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
class AcceptanceReportBoundaries(unittest.TestCase):
 def setUp(self):
  import json
  self.evaluator=runner.module('t01_report_test_evaluator',ROOT/'evaluators/T01/evaluate.py')
  inventory=json.loads((ROOT/'evaluators/T01/criteria.json').read_text())['criteria']
  results=[{'id':c['id'],'requirements':c['requirements'],'status':'fail' if c['id'] in ('A01','U01') else 'pass'} for c in inventory]
  self.files={'web/src/App.vue':'candidate-digest'}
  self.report={'schema':'guild-ledger.t01-acceptance/v1','status':'completed',
   'evaluator_sha256':self.evaluator.version(),'application_sha256':self.files.copy(),
   'model_calls':0,'live_model_calls_enabled':False,'cleanup_passed':True,'selected_criteria':[],
   'required_input_gate_passed':True,'required_build_gate_passed':True,
   **self.evaluator.aggregate({'status':'completed','results':results},[])}
 def validate(self):return runner.validate_acceptance(self.report,self.evaluator,self.files)
 def test_expected_product_rejection_can_pass_mock_verification(self):
  self.assertTrue(self.validate());self.assertIs(self.report['full_target_acceptance'],False)
 def test_evaluator_error_is_unknown_and_fails_verification(self):
  self.report.update(status='evaluator_error',full_target_acceptance=None)
  with self.assertRaisesRegex(ValueError,'did not complete'):self.validate()
  self.assertIsNone(self.report['full_target_acceptance'])
 def test_different_candidate_or_evaluator_rejected(self):
  import copy
  original=copy.deepcopy(self.report)
  for key in ('application_sha256','evaluator_sha256'):
   self.report=copy.deepcopy(original);self.report[key]='wrong'
   with self.assertRaisesRegex(ValueError,'identity mismatch'):self.validate()
 def test_partial_or_duplicate_criteria_rejected(self):
  import copy
  original=copy.deepcopy(self.report)
  for duplicate in (False,True):
   self.report=copy.deepcopy(original)
   if duplicate:self.report['results'][-1]=self.report['results'][0]
   else:self.report['results'].pop()
   with self.assertRaises(ValueError):self.validate()
 def test_forged_success_count_rejected(self):
  self.report['passed_criteria']=23
  with self.assertRaisesRegex(ValueError,'score mismatch'):self.validate()
 def test_cleanup_failure_and_subset_cannot_pass(self):
  for key,value in [('cleanup_passed',False),('selected_criteria',['A01']),('model_calls',1)]:
   with self.subTest(key=key):
    old=self.report[key];self.report[key]=value
    with self.assertRaises(ValueError):self.validate()
    self.report[key]=old
 def test_unexpected_mock_product_success_rejected(self):
  for item in self.report['results']:item['status']='pass'
  self.report.update(self.evaluator.aggregate({'status':'completed','results':self.report['results']},[]))
  with self.assertRaisesRegex(ValueError,'unfinished mock'):self.validate()

class AcceptanceCICollection(unittest.TestCase):
 def test_ci_report_retains_matrix_results_and_digest_even_if_another_suite_failed(self):
  import hashlib,json,subprocess
  import offline_harness_ci as ci
  with tempfile.TemporaryDirectory() as temp:
   results=Path(temp);matrix=results/'t01/summary.json';matrix.parent.mkdir()
   acceptance={'completed':15,'expected_cells':15,'accepted':0,'rejected':15,'unknown':0,
    'cells':[{'level':'P1','harness':'H0','full_target_acceptance':False}]}
   matrix.write_text(json.dumps({'independent_acceptance':acceptance}))
   with patch.object(ci,'RESULTS',results),patch.object(ci,'git',return_value='test-revision'),patch.object(ci.subprocess,'run',return_value=subprocess.CompletedProcess([],1,stdout='')):
    with self.assertRaisesRegex(RuntimeError,'incomplete'):ci.report()
   report=json.loads((results/'report.json').read_text())
   self.assertFalse(report['verification_passed'])
   self.assertEqual(report['t01_independent_acceptance'],acceptance)
   self.assertEqual(report['t01_report'],{'path':'t01/summary.json','sha256':hashlib.sha256(matrix.read_bytes()).hexdigest()})
   self.assertIn('15/15 completed; 0 accepted, 15 rejected, 0 unknown',(results/'summary.md').read_text())
 def test_missing_matrix_does_not_invent_acceptance_results(self):
  import json,subprocess
  import offline_harness_ci as ci
  with tempfile.TemporaryDirectory() as temp:
   results=Path(temp)
   with patch.object(ci,'RESULTS',results),patch.object(ci,'git',return_value='test-revision'),patch.object(ci.subprocess,'run',return_value=subprocess.CompletedProcess([],1,stdout='')):
    with self.assertRaises(RuntimeError):ci.report()
   report=json.loads((results/'report.json').read_text())
   self.assertNotIn('t01_independent_acceptance',report);self.assertFalse(report['verification_passed'])

if __name__=='__main__':unittest.main(verbosity=2)

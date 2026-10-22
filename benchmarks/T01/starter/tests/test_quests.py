import json, os, unittest
from urllib.request import urlopen
from urllib.error import HTTPError
BASE=os.environ.get('GUILD_URL','http://localhost:18000')
def request(path):
 try:
  with urlopen(BASE+path,timeout=5) as r: return r.status,json.load(r)
 except HTTPError as e: return e.code,json.load(e)
class Quests(unittest.TestCase):
 def test_list_fixture_order(self):
  status,body=request('/api/quests')
  self.assertEqual(status,200)
  self.assertEqual([q['id'] for q in body['quests']],['q-ash','q-beacon','q-cairn','q-delta'])
 def test_detail(self):
  status,body=request('/api/quests/q-ash')
  self.assertEqual(status,200)
  self.assertEqual(body['description'],'Recover the orchard bells.')
 def test_difficulty_filter(self):
  status,body=request('/api/quests?difficulty=easy')
  self.assertEqual(status,200)
  self.assertEqual([q['id'] for q in body['quests']],['q-ash','q-delta'])
 def test_unknown_detail(self):
  status,body=request('/api/quests/not-a-quest')
  self.assertEqual(status,404)
  self.assertEqual(body['error']['code'],'NOT_FOUND')

import json, os, unittest
from urllib.request import urlopen
class Startup(unittest.TestCase):
 def test_guild_health(self):
  with urlopen(os.environ.get('GUILD_URL','http://localhost:18000')+'/health',timeout=5) as r:
   self.assertEqual(json.load(r),{'status':'ok','service':'guild'})
 def test_armory_health(self):
  with urlopen(os.environ.get('ARMORY_URL','http://localhost:18001')+'/health',timeout=5) as r:
   self.assertEqual(json.load(r),{'status':'ok','service':'armory'})
 def test_web_shell(self):
  with urlopen(os.environ.get('WEB_URL','http://localhost:15173'),timeout=5) as r:
   self.assertIn('Guild Ledger',r.read().decode())

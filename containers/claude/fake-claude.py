"""Synthetic fixture only. These token counts are NOT measured model usage."""
import json
import time
import sys
from pathlib import Path
prompt=Path('/inputs/assembled-prompt.txt').read_text()
Path('/workspace/synthetic-result.txt').write_text('Synthetic edit: ' + prompt + '\n')
if prompt == '__fixture_timeout__':
    time.sleep(60)
if prompt == '__fixture_failure__':
    sys.exit(9)
print(json.dumps({'type':'result','synthetic':True,'result':'fixture complete',
                  'usage':{'input_tokens':11,'output_tokens':7},'cost_usd':None}),flush=True)

"""Complete T01 reference. Never exported in an agent task bundle."""
import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title='Guild Ledger')
QUESTS = json.loads(Path('/fixtures/quests.json').read_text())

def error(status, code, message):
    return JSONResponse(status_code=status, content={'error': {'code': code, 'message': message}})

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'guild'}

@app.get('/api/quests')
def quests(request: Request):
    params = request.query_params
    for name in ('q', 'difficulty', 'status'):
        if len(params.getlist(name)) > 1:
            return error(400, 'INVALID_REQUEST', 'Repeated filter')
    for name, values in [('difficulty', ('easy', 'medium', 'hard')), ('status', ('open', 'closed'))]:
        if name in params and params[name] not in values:
            return error(400, 'INVALID_REQUEST', 'Invalid filter')
    query = params.get('q', '').strip().casefold()
    selected = [q for q in QUESTS if query in q['title'].casefold()
                and ('difficulty' not in params or q['difficulty'] == params['difficulty'])
                and ('status' not in params or q['status'] == params['status'])]
    return {'quests': sorted(selected, key=lambda q: (q['title'].casefold(), q['id']))}

@app.get('/api/quests/{quest_id}')
def detail(quest_id: str):
    for quest in QUESTS:
        if quest['id'] == quest_id:
            return quest
    return error(404, 'NOT_FOUND', 'Quest not found')

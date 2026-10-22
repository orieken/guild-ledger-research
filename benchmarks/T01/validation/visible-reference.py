"""Trusted visible-test witness only; not a complete P3 reference or agent input."""
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse
app=FastAPI()
DATA=json.loads(Path('/fixtures/quests.json').read_text())
@app.get('/health')
def health(): return {'status':'ok','service':'guild'}
@app.get('/api/quests')
def quests(difficulty: str | None=None):
    data=[q for q in DATA if difficulty is None or q['difficulty']==difficulty]
    return {'quests': sorted(data,key=lambda q:(q['title'].casefold(),q['id']))}
@app.get('/api/quests/{quest_id}')
def quest(quest_id:str):
    return next((q for q in DATA if q['id']==quest_id),JSONResponse(status_code=404,content={'error':{'code':'NOT_FOUND','message':'Quest not found'}}))

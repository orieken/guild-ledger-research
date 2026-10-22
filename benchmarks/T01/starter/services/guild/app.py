"""T01 starting point. The quest browser endpoints are the assigned work."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI(title="Guild Ledger", version="0.1.0")
@app.get("/health")
def health():
    return {"status": "ok", "service": "guild"}
@app.get("/api/quests")
def quests():
    return JSONResponse(status_code=501, content={"error": {"code": "NOT_IMPLEMENTED", "message": "Quest browsing is not implemented"}})
@app.get("/api/quests/{quest_id}")
def quest(quest_id: str):
    return JSONResponse(status_code=501, content={"error": {"code": "NOT_IMPLEMENTED", "message": "Quest details are not implemented"}})

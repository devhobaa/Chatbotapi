#!/usr/bin/env python3
import os
import time
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from adapters.gemini_mind_adapter import get_bot
from sse_starlette.sse import EventSourceResponse

SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")
if SERVICE_API_KEY is None:
    print("[WARN] SERVICE_API_KEY not set; using 'dev-key' (development only).")
    SERVICE_API_KEY = "dev-key"

app = FastAPI(title="GeminiMindBot API", version="1.0.0")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _check_auth(x_api_key: Optional[str]):
    if SERVICE_API_KEY and x_api_key != SERVICE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

class Msg(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: List[Msg] = Field(default_factory=list)
    user_id: Optional[str] = None
    stream: bool = False
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    reply: str
    usage: Dict[str, Any] = {}
    latency_ms: int

@app.get("/health")
def health():
    return {"status": "ok", "time": int(time.time())}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, request: Request, x_api_key: Optional[str] = Header(None)):
    _check_auth(x_api_key)
    t0 = time.perf_counter()
    bot = get_bot()
    try:
        reply, usage = bot.chat(
            message=req.message,
            history=[m.dict() for m in req.history],
            user_id=req.user_id,
            temperature=req.temperature,
            stream=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    t1 = time.perf_counter()
    return ChatResponse(reply=reply, usage=usage or {}, latency_ms=int((t1 - t0) * 1000))

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest, request: Request, x_api_key: Optional[str] = Header(None)):
    _check_auth(x_api_key)
    bot = get_bot()

    async def event_gen():
        try:
            async for chunk in bot.chat_stream(
                message=req.message,
                history=[m.dict() for m in req.history],
                user_id=req.user_id,
                temperature=req.temperature,
            ):
                yield {"event": "token", "data": chunk}
            yield {"event": "done", "data": "ok"}
        except Exception as e:
            yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_gen())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

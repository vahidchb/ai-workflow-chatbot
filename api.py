"""API برای رابط کاربری Angular — همین کدهای پایتون، پشت HTTP.

اجرا:
    uvicorn api:app --reload --port 8000

بعد Angular از http://localhost:8000/api/chat صدا می‌زند.
"""
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot import config
from chatbot.chat import SYSTEM_PROMPT, chat_one_turn
from chatbot.memory import count_messages_tokens, needs_compaction, compact_messages

app = FastAPI(title="AI Workflow Chatbot")

# Angular روی پورت 4200 اجرا می‌شود؛ اجازه بده به API وصل شود.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# حافظه ساده: هر session_id یک مکالمه دارد.
sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tokens: int
    max_tokens: int
    used_tool: bool


@app.get("/api/health")
def health():
    """سلامتی API را برگردان؛ مدل هم نشان بده."""
    return {"status": "ok", "model": config.LLM_MODEL}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """یک پیام بگیر، با همان منطق chat.py جواب بده."""
    if not config.LLM_API_KEY or not config.LLM_BASE_URL:
        raise HTTPException(
            status_code=400,
            detail="اول TOKEN_HARBOR_API_KEY و LLM_BASE_URL را در فایل .env بگذار.",
        )
    session_id = req.session_id or str(uuid.uuid4())
    messages = sessions.get(session_id)
    if messages is None:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        sessions[session_id] = messages

    messages.append({"role": "user", "content": req.message})

    # مدیریت توکن + compaction، دقیقاً مثل نسخه ترمینالی
    if needs_compaction(messages):
        messages[:] = compact_messages(messages)

    before = len(messages)
    reply = chat_one_turn(messages)
    used_tool = any(m.get("role") == "tool" for m in messages[before:])

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        tokens=count_messages_tokens(messages),
        max_tokens=config.MAX_TOKENS,
        used_tool=used_tool,
    )

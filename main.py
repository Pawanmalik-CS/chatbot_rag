from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import rag_answer

# ─── App Setup ─────────────────────────────────────────────────
app = FastAPI(title="AI Chatbot API")

# ─── CORS ───────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Request & Response Models ──────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    history: list = []

class ChatResponse(BaseModel):
    reply: str

# ─── Health Check ───────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Chatbot API is running 🚀"}

# ─── Chat Endpoint ──────────────────────────────────────────────
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = rag_answer(request.message, request.history)
    return ChatResponse(reply=reply)

from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import openai
import os
import json

from google.cloud import firestore
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
firestore_client = firestore.Client()

app = FastAPI()

# -------------------- Models --------------------
class ChatRequest(BaseModel):
    user_id: str
    prompt: Optional[str] = None
    messages: Optional[List[dict]] = None
    model: str = "gpt-3.5-turbo"
    prompt_key: str = "ai_prompt.chat"

class ChatResponse(BaseModel):
    reply: str
    model_used: str
    token_used: int
    timestamp: str

# -------------------- Utility --------------------
def fetch_prompt_config(key: str):
    doc_ref = firestore_client.collection("configs").document(key)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return data.get("prompt", ""), data.get("max_tokens", 300), data.get("temperature", 0.7)
    return "", 300, 0.7
def cosine_similarity(a, b):
    import numpy as np
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def search_similar_context(query_embedding, top_k=3, threshold=0.75):
    docs = firestore_client.collection("rag_contexts").stream()
    scored = []
    for doc in docs:
        data = doc.to_dict()
        emb = data.get("embedding", [])
        if emb:
            score = cosine_similarity(query_embedding, emb)
            if score >= threshold:
                scored.append((score, data.get("text", "")))
    return [text for score, text in sorted(scored, reverse=True)[:top_k]]

def log_ai_usage(user_id: str, model: str, tokens: int, route: str, payload: dict):
    firestore_client.collection("ai_logs").add({
        "user_id": user_id,
        "model": model,
        "tokens": tokens,
        "route": route,
        "payload": payload,
        "timestamp": datetime.utcnow()
    })

def wrap_content(content, model):
    if model.startswith("gpt-4") or model.startswith("gpt-3.5"):
        return [{"type": "text", "text": content}]
    return content

# -------------------- Routes --------------------
@app.post("/ai/chat", response_model=ChatResponse)
async def ai_chat(req: ChatRequest):
    prompt_text, max_tokens, temperature = fetch_prompt_config(req.prompt_key)
    try:
        messages = req.messages if req.messages else [
            {"role": "system", "content": wrap_content(prompt_text, req.model)},
            {"role": "user", "content": wrap_content(req.prompt, req.model)}
        ]
        response = client.chat.completions.create(
            model=req.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        reply = response.choices[0].message.content.strip()
        token_used = response.usage.total_tokens
    except Exception as e:
        reply = f"ขออภัย ระบบ AI มีปัญหา: {e}"
        token_used = 0

    log_ai_usage(req.user_id, req.model, token_used, "chat", req.dict())
    return ChatResponse(
        reply=reply,
        model_used=req.model,
        token_used=token_used,
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/ai/interpret", response_model=ChatResponse)
async def ai_interpret(req: ChatRequest):
    prompt_text, max_tokens, temperature = fetch_prompt_config(req.prompt_key)
    try:
        messages = req.messages if req.messages else [
            {"role": "system", "content": wrap_content(prompt_text, req.model)},
            {"role": "user", "content": wrap_content(req.prompt, req.model)}
        ]
        response = client.chat.completions.create(
            model=req.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        reply = response.choices[0].message.content.strip()
        token_used = response.usage.total_tokens
    except Exception as e:
        reply = f"ขออภัย ระบบ AI มีปัญหา: {e}"
        token_used = 0

    log_ai_usage(req.user_id, req.model, token_used, "interpret", req.dict())
    return ChatResponse(
        reply=reply,
        model_used=req.model,
        token_used=token_used,
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/ai/summarize", response_model=ChatResponse)
async def ai_summarize(req: ChatRequest):
    prompt_text, max_tokens, temperature = fetch_prompt_config(req.prompt_key)
    try:
        messages = req.messages if req.messages else [
            {"role": "system", "content": wrap_content(prompt_text, req.model)},
            {"role": "user", "content": wrap_content(req.prompt, req.model)}
        ]
        response = client.chat.completions.create(
            model=req.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        reply = response.choices[0].message.content.strip()
        token_used = response.usage.total_tokens
    except Exception as e:
        reply = f"ขออภัย ระบบ AI มีปัญหา: {e}"
        token_used = 0

    log_ai_usage(req.user_id, req.model, token_used, "summarize", req.dict())
    return ChatResponse(
        reply=reply,
        model_used=req.model,
        token_used=token_used,
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/ai/tarot", response_model=ChatResponse)
async def ai_tarot(req: ChatRequest):
    prompt_text, max_tokens, temperature = fetch_prompt_config(req.prompt_key)
    try:
        messages = req.messages if req.messages else [
            {"role": "system", "content": wrap_content(prompt_text, req.model)},
            {"role": "user", "content": wrap_content(req.prompt, req.model)}
        ]
        response = client.chat.completions.create(
            model=req.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        reply = response.choices[0].message.content.strip()
        token_used = response.usage.total_tokens
    except Exception as e:
        reply = f"ขออภัย ระบบ AI มีปัญหา: {e}"
        token_used = 0

    log_ai_usage(req.user_id, req.model, token_used, "tarot", req.dict())
    return ChatResponse(
        reply=reply,
        model_used=req.model,
        token_used=token_used,
        timestamp=datetime.utcnow().isoformat()
    )
@app.post("/ai/rag", response_model=ChatResponse)
async def ai_rag(req: ChatRequest):
    prompt_text, max_tokens, temperature = fetch_prompt_config(req.prompt_key)

    # 👉 (ตัวอย่าง) ดึง context จาก Pinecone (mock หรือจริงก็ได้)
    context_text = "นี่คือบริบทจำลองจาก Pinecone เช่น รายละเอียดไพ่ หรือคำสอนที่เกี่ยวข้อง..."

    full_prompt = f"{context_text}\n\nคำถาม: {req.prompt}"

    try:
        messages = [
            {"role": "system", "content": wrap_content(prompt_text, req.model)},
            {"role": "user", "content": wrap_content(full_prompt, req.model)},
        ]
        response = client.chat.completions.create(
            model=req.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        reply = response.choices[0].message.content.strip()
        token_used = response.usage.total_tokens
    except Exception as e:
        reply = f"ขออภัย ระบบ AI มีปัญหา: {e}"
        token_used = 0

    log_ai_usage(req.user_id, req.model, token_used, "rag", req.dict())
    return ChatResponse(
        reply=reply,
        model_used=req.model,
        token_used=token_used,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/ai/test", response_model=List[ChatResponse])
async def ai_test(req: ChatRequest):
    models_to_test = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
    results = []
    for m in models_to_test:
        prompt_text, max_tokens, temperature = fetch_prompt_config(req.prompt_key)
        try:
            messages = [
                {"role": "system", "content": wrap_content(prompt_text, m)},
                {"role": "user", "content": wrap_content(req.prompt, m)}
            ]
            response = client.chat.completions.create(
                model=m,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            reply = response.choices[0].message.content.strip()
            token_used = response.usage.total_tokens
        except Exception as e:
            reply = f"ERROR: {e}"
            token_used = 0

        log_ai_usage(req.user_id, m, token_used, "test", req.dict())
        results.append(ChatResponse(
            reply=reply,
            model_used=m,
            token_used=token_used,
            timestamp=datetime.utcnow().isoformat()
        ))
    return results
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
@app.get("/ai/monitor")
def ai_monitor():
    logs = firestore_client.collection("ai_logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(10).stream()
    return [{"user_id": l.get("user_id"), "model": l.get("model"), "tokens": l.get("tokens"), "route": l.get("route"), "time": l.get("timestamp")} for l in logs]

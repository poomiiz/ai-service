# ai-service/routes/ai.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# 1) Schema สำหรับ /ai/interpret
class InterpretRequest(BaseModel):
    user_id: str = Field(..., alias="userId")
    conversation_id: str = Field(..., alias="conversationId")
    message: str

class InterpretResponse(BaseModel):
    intent: str
    confidence: float

@app.post("/ai/interpret", response_model=InterpretResponse)
async def interpret(req: InterpretRequest):
    # โค้ดวิเคราะห์ intent/emotion (mockup ตัวอย่าง)
    # ตัวอย่างส่งกลับว่าเป็น “general” ความมั่นใจ 0.9
    return {"intent": "general", "confidence": 0.90}


# 2) Schema สำหรับ /ai/summarize
class SummarizeRequest(BaseModel):
    conversation_id: str = Field(..., alias="conversationId")
    messages: List[str]

class SummarizeResponse(BaseModel):
    summary: str

@app.post("/ai/summarize", response_model=SummarizeResponse)
async def summarize(req: SummarizeRequest):
    # โค้ดสรุปข้อความ (mockup ตัวอย่าง)
    # สมมติสรุปเป็น “user กล่าวคำว่า …”
    joined = " ".join(req.messages)
    return {"summary": f"สรุปบทสนทนาว่า: {joined}"}


# 3) Schema สำหรับ /ai/chat
class ChatRequest(BaseModel):
    user_id: str = Field(..., alias="userId")
    conversation_id: str = Field(..., alias="conversationId")
    message: str
    # ถ้าอยากรับ modelPreference ก็เขียนเพิ่ม (ไม่บังคับ)
    model: str
    # ลบ modelPreference ออก (เพราะ schema นี้คาดว่ามีแต่ model ตัวเดียว)

class ChatResponse(BaseModel):
    response: str
    model_used: str = Field(..., alias="modelUsed")
    confidence_score: float = Field(..., alias="confidenceScore")
    summary: Optional[str] = None

@app.post("/ai/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # โค้ดเรียกโมเดล deep learning จริงๆ
    # mockup: ส่งกลับ echo เสียงตอบ
    reply = f"คุณพิมพ์ว่า: {req.message}"
    return {
        "response": reply,
        "modelUsed": req.model,
        "confidenceScore": 0.85,
        "summary": "สรุปสั้นๆ หลังตอบ"
    }


# 4) Schema สำหรับ /ai/tune_prompt
class TunePromptRequest(BaseModel):
    tune_id: str = Field(..., alias="tuneId")
    model: str
    candidate_prompt: str = Field(..., alias="candidatePrompt")
    test_question: str = Field(..., alias="testQuestion")

class TunePromptResponse(BaseModel):
    generatedResponse: str
    scores: dict

@app.post("/ai/tune_prompt", response_model=TunePromptResponse)
async def tune_prompt(req: TunePromptRequest):
    # โค้ดเรียก GPT-4o เพื่อ generate ตาม candidate_prompt + test_question
    # mockup: สร้างข้อความตอบ “ทดสอบ prompt”
    gen = f"Response for '{req.test_question}' using prompt '{req.candidate_prompt}'"
    return {"generatedResponse": gen, "scores": {req.model: 0.9}}

from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    prompt: str
    model: str = "gpt-3.5-turbo"

class ChatResponse(BaseModel):
    reply: str

@app.post("/ai/chat", response_model=ChatResponse)
async def ai_chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model=req.model,
            messages=[{"role": "user", "content": req.prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception as e:
        reply_text = f"ขออภัย ระบบ AI มีปัญหา: {e}"
    return ChatResponse(reply=reply_text)

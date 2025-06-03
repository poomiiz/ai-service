from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ตัวอย่าง Pydantic model สำหรับ request/response
class HelloRequest(BaseModel):
    name: str

class HelloResponse(BaseModel):
    message: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/ai/chat", response_model=HelloResponse)
async def chat_endpoint(req: HelloRequest):
    # แก้เป็น logic จริงตามต้องการ (ตัวอย่างส่งข้อความทักทายกลับ)
    return {"message": f"Hello, {req.name}! This is ai-service."}

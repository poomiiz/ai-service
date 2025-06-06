# ai-service/ai_services/chat.py

async def generate_chat_response(user_id: str, prompt: str, model: str) -> str:
    # แค่คืนข้อความ echo หรือข้อความตายตัวก่อน
    return f"คุณส่งข้อความว่า: {prompt} (ในโหมด {model})"

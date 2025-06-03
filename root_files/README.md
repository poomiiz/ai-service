# ai-service (FastAPI)

## ภาพรวม
Service นี้เขียนด้วย FastAPI ทำหน้าที่รับคำขอจาก go-backend ผ่าน HTTP (REST) แล้วเลือก route ไปหา GPT/Llama/Together หรือโมดูล AI ต่างๆ (multi-turn chat, วิเคราะห์ไพ่, สรุป, preprocessing ฯลฯ)

## โครงสร้างโฟลเดอร์

- **ai_services/**  
  - `ai_router.py`: รับ prompt มาจาก go-backend แล้วตัดสินใจเลือก AI model (เช่น GPT-4o, LLaMA, Together)  
  - `chat.py`: จัดการ AI Chat แบบ multi-turn (เก็บ context, ส่งต่อ prompt)  
  - `daily_card.py`: วิเคราะห์ความหมายไพ่รายวัน (ใช้ RAG + AI)  
  - `summarize.py`: สรุปข้อความหรือวิเคราะห์รีวิว  
  - `pre_predict.py`: Preprocessing เบื้องต้น เช่น intent detection, token count, NER, OCR ฯลฯ

- **routes/ai.py**  
  FastAPI router สำหรับ endpoint ที่ go-backend จะเรียก  

- **models/**  
  - `request_models.py`: Pydantic models สำหรับรับข้อมูลจาก go-backend  
  - `response_models.py`: Pydantic models สำหรับตอบกลับ (ผลลัพธ์ AI, error structure ฯลฯ)

- **utils/**  
  - `logger.py`: ตั้งค่าส่วนกลางของ logging (เช่น log level)  
  - (ถ้ามี): error handler, helper functions

- **core/**  
  - `config.py`: โหลด config ต่างๆ (เช่น API keys สำหรับ OpenAI, Llama endpoint ฯลฯ)  
  - `dependencies.py`: กำหนด Dependency Injection (เช่น DB session ถ้ามี)

- **scripts/**  
  - `run.sh`: สคริปต์รัน uvicorn, ตั้งค่า environment ก่อนรัน  

- **Dockerfile / requirements.txt**  
  กำหนด dependencies (FastAPI, uvicorn, openai SDK, llama SDK ฯลฯ)

## วิธีติดตั้งและรัน

1. สร้าง virtual environment และติดตั้ง dependencies  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```  
2. ตั้งค่า environment variables  
   ```
   OPENAI_API_KEY=...
   LLAMA_ENDPOINT=...
   REDIS_URL=...
   ```  
3. รัน server  
   ```bash
   ./scripts/run.sh
   ```  
   หรือ  
   ```bash
   uvicorn routes.ai:app --host 0.0.0.0 --port 8000
   ```  

## ตัวอย่าง Endpoints

- `POST /ai/chat`  
  รับ JSON ประมาณ `{ "user_id": "...", "prompt": "...", "model": "gpt-4o" }` แล้วตอบ `{ "reply": "..." }`  
- `POST /ai/daily_card`  
  รับ `{ "user_id": "...", "deck": "tarot", "date": "2025-06-03" }` แล้วตอบผลวิเคราะห์ไพ่  
- `POST /ai/summarize`  
  ฯลฯ  


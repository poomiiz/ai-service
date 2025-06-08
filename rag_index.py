# rag_index.py

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

load_dotenv()

# Load API keys
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME", "moobiker-context")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Init Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Create index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)

# Init OpenAI client
client = OpenAI(api_key=openai_api_key)

# ตัวอย่างข้อมูล
documents = [
    {"id": "deck_001", "text": "ไพ่ The Fool หมายถึงการเริ่มต้นใหม่ด้วยหัวใจที่เปิดกว้าง"},
    {"id": "deck_002", "text": "ไพ่ The Tower สื่อถึงการเปลี่ยนแปลงฉับพลัน หรือความเปลี่ยนที่ไม่คาดฝัน"},
]

# ทำ embedding แล้วใส่ลง Pinecone
for doc in documents:
    embedding = client.embeddings.create(
        input=doc["text"],
        model="text-embedding-3-small"
    ).data[0].embedding

    index.upsert(vectors=[{
        "id": doc["id"],
        "values": embedding,
        "metadata": {"text": doc["text"]}
    }])

print("✅ Upsert สำเร็จ!")

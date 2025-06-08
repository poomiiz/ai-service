import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

# Load env
load_dotenv()

# Firebase
cred = credentials.Certificate("config/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("moobiker-context")

# OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed(text):
    res = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return res.data[0].embedding

def sync_tarot():
    docs = db.collection("tarot").stream()
    for doc in docs:
        data = doc.to_dict()
        card_id = doc.id
        content = data.get("description", "")
        vector = embed(content)
        index.upsert([
            {
                "id": card_id,
                "values": vector,
                "metadata": {
                    "name": data.get("name", ""),
                    "deck": data.get("deck_id", "")
                }
            }
        ])
        print(f"✅ Upserted: {card_id}")

if __name__ == "__main__":
    sync_tarot()

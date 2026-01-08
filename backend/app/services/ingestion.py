# backend/app/services/ingestion.py

import uuid
from datetime import datetime
from app.services.embedding import generate_embedding

def ingest_memory(content: str, source: str):
    return {
        "id": str(uuid.uuid4()),
        "content": content,
        "source": source,
        "embedding": generate_embedding(content),
        "created_at": datetime.utcnow()
    }

# backend/app/services/ingestion.py

import uuid
from datetime import datetime

def ingest_memory(content: str, source: str):
    return {
        "id": str(uuid.uuid4()),
        "content": content,
        "source": source,
        "created_at": datetime.utcnow()
    }

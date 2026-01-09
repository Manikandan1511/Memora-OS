from app.services.embedding import generate_embedding
from app.db.chroma import collection
import uuid
from datetime import datetime

def ingest_memory(content: str, source: str):
    memory_id = str(uuid.uuid4())
    embedding = generate_embedding(content)
    timestamp = datetime.utcnow().isoformat()

    collection.add(
        ids=[memory_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[{
            "source": source,
            "created_at": timestamp
        }]
    )

    return {
        "id": memory_id,
        "content": content,
        "source": source,
        "embedding": embedding,
        "created_at": timestamp
    }

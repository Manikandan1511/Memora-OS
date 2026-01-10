# backend/app/services/ingestion.py

import uuid
from datetime import datetime

from app.services.embedding import create_embedding
from app.db.chroma import get_collection
from app.services.graph import create_memory_node


def ingest_memory(content: str, source: str = "manual"):
    """
    Ingests a memory:
    - creates embedding
    - stores in Chroma
    - creates Neo4j node
    """

    memory_id = str(uuid.uuid4())
    created_at = datetime.utcnow()

    # 1. Create embedding
    embedding = create_embedding(content)

    # 2. Store in ChromaDB
    collection = get_collection()
    collection.add(
        ids=[memory_id],
        documents=[content],
        metadatas=[{
            "source": source,
            "created_at": created_at.isoformat()
        }],
        embeddings=[embedding]
    )

    # 3. Store in Neo4j
    create_memory_node({
        "id": memory_id,
        "content": content,
        "source": source,
        "created_at": created_at.isoformat()
    })

    # 4. Return API-safe response
    return {
        "id": memory_id,
        "content": content,
        "source": source,
        "embedding": embedding,
        "created_at": created_at.isoformat()
    }

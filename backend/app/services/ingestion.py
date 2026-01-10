# backend/app/services/ingestion.py

from uuid import uuid4
from datetime import datetime

from app.services.embedding import create_embedding
from app.db.chroma import get_collection
from app.services.graph import create_memory_node, link_related_memories


def ingest_memory(content: str, source: str):
    memory_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()

    # Create embedding
    embedding = create_embedding(content)

    # Store in ChromaDB
    collection = get_collection()
    collection.add(
        ids=[memory_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[{
            "source": source,
            "created_at": created_at
        }]
    )

    # Unified memory object
    memory = {
        "id": memory_id,
        "content": content,
        "source": source,
        "created_at": created_at
    }

    # Store in Neo4j
    create_memory_node(memory)
    link_related_memories(memory)

    return memory

# backend/app/services/ingestion.py

import uuid
from datetime import datetime
from typing import Dict

from app.services.embedding import create_embedding
from app.services.evolution import evolve_memory
from app.services.graph import create_memory_node
from app.db.chroma import get_collection


def ingest_memory(content: str, source: str = "manual") -> Dict:
    """
    Ingest a new memory into the system.

    Steps:
    1. Generate embedding
    2. Store in vector DB (Chroma)
    3. Create node in Neo4j
    4. Always evolve memory (top-k linking for demo)
    """

    # Create base memory fields

    memory_id = str(uuid.uuid4())
    created_at = datetime.utcnow()

    # Generate embedding

    embedding = create_embedding(content)

    # Store in vector database
    
    collection = get_collection()
    collection.add(
        ids=[memory_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[{
            "id": memory_id,
            "source": source,
            "created_at": created_at.isoformat()
        }]
    )

    # Create Neo4j node
    
    memory_payload = {
        "id": memory_id,
        "content": content,
        "source": source,
        "created_at": created_at.isoformat()
    }

    create_memory_node(memory_payload)

    # Knowledge evolution (ALWAYS)

    evolve_memory(
        new_memory_id=memory_id,
        new_embedding=embedding
    )


    # API response

    return {
        "id": memory_id,
        "content": content,
        "source": source,
        "embedding": embedding,
        "created_at": created_at.isoformat()
    }

# backend/app/services/search.py

from typing import List
from app.services.embedding import generate_embedding
from app.db.chroma import get_collection


def search_memories(query: str, limit: int = 5):
    """
    Semantic search over stored memories using vector similarity.
    """
    collection = get_collection()

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        include=["documents", "metadatas", "ids"]
    )

    memories = []
    for i in range(len(results["ids"][0])):
        memories.append({
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return memories

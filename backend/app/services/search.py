# backend/app/services/search.py

from app.db.chroma import get_collection
from app.services.embedding import create_embedding


def search_memories(query: str, limit: int = 5):
    collection = get_collection()

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit
    )

    memories = []

    for i in range(len(results["ids"][0])):
        memories.append({
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return memories

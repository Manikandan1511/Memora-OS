# backend/app/db/chroma.py

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings

_client = None
_collection = None


def get_collection():
    """
    Returns the persistent ChromaDB collection.
    Used by ingestion, evolution, memory APIs.
    """
    global _client, _collection

    if _client is None:
        _client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.CHROMA_PATH,
                is_persistent=True,
                anonymized_telemetry=False,
            )
        )

    if _collection is None:
        _collection = _client.get_or_create_collection(
            name="memories"
        )

    return _collection


def semantic_search(query: str, k: int = 5):
    """
    Semantic similarity search for AskBrain.
    """
    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=k
    )

    hits = []

    if not results or not results.get("documents"):
        return hits

    documents = results["documents"][0]
    ids = results["ids"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):
        hits.append({
            "id": ids[i],
            "content": documents[i],
            "score": round(float(distances[i]), 4)
        })

    return hits

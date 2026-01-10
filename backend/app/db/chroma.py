# backend/app/db/chroma.py

import chromadb
from chromadb.config import Settings as ChromaSettings

# Persistent storage path
CHROMA_PATH = "vectordb"

_client = None
_collection = None


def get_collection():
    global _client, _collection

    if _client is None:
        _client = chromadb.Client(
            ChromaSettings(
                persist_directory=CHROMA_PATH,
                anonymized_telemetry=False
            )
        )

    if _collection is None:
        _collection = _client.get_or_create_collection(
            name="memories"
        )

    return _collection

# backend/app/db/chroma.py

import os
import chromadb

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

VECTOR_DB_PATH = os.path.join(BASE_DIR, "vectordb")

client = chromadb.PersistentClient(
    path=VECTOR_DB_PATH
)

collection = client.get_or_create_collection(
    name="memora_memories"
)

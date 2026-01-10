# backend/app/services/embedding.py

from sentence_transformers import SentenceTransformer
from functools import lru_cache
from typing import List

# Load model once (VERY important for performance)
@lru_cache(maxsize=1)
def _load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> List[float]:
    """
    Generate vector embedding for a given text.
    This is the SINGLE embedding function used across Memora OS.
    """
    model = _load_model()
    embedding = model.encode(text)
    return embedding.tolist()

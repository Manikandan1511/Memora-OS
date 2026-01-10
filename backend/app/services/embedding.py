# backend/app/services/embedding.py

from sentence_transformers import SentenceTransformer

# Load once (important for performance & stability)
_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str) -> list[float]:
    """
    Create a vector embedding for a given text.
    Always returns a Python list (NOT numpy array).
    """
    embedding = _model.encode(text)
    return embedding.tolist()

# backend/app/services/embedding.py

from sentence_transformers import SentenceTransformer

# Load model once (important)
_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> list[float]:
    """
    Convert text into a semantic vector (embedding)
    """
    embedding = _model.encode(text)
    return embedding.tolist()

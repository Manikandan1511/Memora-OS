# backend/app/services/embedding.py


from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def create_embedding(text: str) -> list[float]:
    """
    Create a vector embedding for a given text.
    Loads the model only on the first request.
    """
    model = get_model()
    embedding = model.encode(text)
    return embedding.tolist()

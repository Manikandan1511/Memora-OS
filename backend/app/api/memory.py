from fastapi import APIRouter
from app.schemas.memory import (
    MemoryCreate,
    MemoryResponse,
    MemorySearchRequest,
    MemorySearchResponse
)
from app.services.ingestion import ingest_memory
from app.services.search import search_memories

router = APIRouter()

@router.post("", response_model=MemoryResponse)
def add_memory(payload: MemoryCreate):
    return ingest_memory(
        content=payload.content,
        source=payload.source
    )

@router.post("/search", response_model=MemorySearchResponse)
def search_memory(payload: MemorySearchRequest):
    results = search_memories(
        query=payload.query,
        limit=payload.limit
    )
    return {"results": results}

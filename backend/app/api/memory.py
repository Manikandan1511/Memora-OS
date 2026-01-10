from fastapi import APIRouter
from app.schemas.memory import (
    MemoryCreate,
    MemoryResponse,
    MemorySearchRequest,
    MemorySearchResponse,
    MemoryTimeRangeRequest,
    MemoryTimeRangeResponse
)
from app.services.ingestion import ingest_memory
from app.services.search import search_memories
from app.services.temporal import get_memories_by_time


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

@router.post("/timeline", response_model=MemoryTimeRangeResponse)
def get_memory_timeline(payload: MemoryTimeRangeRequest):
    memories = get_memories_by_time(
        start_date=payload.start_date,
        end_date=payload.end_date
    )
    return {"results": memories}

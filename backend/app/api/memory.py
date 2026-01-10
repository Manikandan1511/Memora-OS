# backend/app/api/memory.py

from fastapi import APIRouter

from app.schemas.memory import (
    MemoryCreateRequest,
    MemoryResponse,
    MemorySearchRequest,
    MemoryTimelineRequest
)
from app.services.ingestion import ingest_memory
from app.services.search import search_memories
from app.services.temporal import get_memories_by_time

router = APIRouter(prefix="/memory", tags=["Memory"])


# -------- Create Memory --------
@router.post("/", response_model=MemoryResponse)
def add_memory(payload: MemoryCreateRequest):
    return ingest_memory(
        content=payload.content,
        source=payload.source
    )


# -------- Semantic Search --------
@router.post("/search")
def search_memory(payload: MemorySearchRequest):
    return {
        "results": search_memories(
            query=payload.query,
            limit=payload.limit
        )
    }


# -------- Timeline (Temporal Memory) --------
@router.post("/timeline")
def memory_timeline(payload: MemoryTimelineRequest):
    return {
        "results": get_memories_by_time(
            start_date=payload.start_date,
            end_date=payload.end_date
        )
    }

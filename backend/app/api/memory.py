# backend/app/api/memory.py

from fastapi import APIRouter
from app.schemas.memory import MemoryCreate, MemoryResponse
from app.services.ingestion import ingest_memory

router = APIRouter()

@router.post("/memory", response_model=MemoryResponse)
def add_memory(payload: MemoryCreate):
    return ingest_memory(
        content=payload.content,
        source=payload.source
    )

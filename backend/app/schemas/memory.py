# backend/app/schemas/memory.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict


class MemoryCreate(BaseModel):
    content: str
    source: Optional[str] = "manual"


class MemoryResponse(BaseModel):
    id: str
    content: str
    source: str
    embedding: List[float]
    created_at: datetime  # datetime is correct

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()  # THIS FIXES IT
        }


class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 5


class MemorySearchResult(BaseModel):
    id: str
    content: str
    metadata: Dict


class MemorySearchResponse(BaseModel):
    results: List[MemorySearchResult]


class MemoryTimeRangeRequest(BaseModel):
    start_date: str
    end_date: str


class MemoryTimeRangeResponse(BaseModel):
    results: List[MemorySearchResult]

# backend/app/schemas/memory.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MemoryCreate(BaseModel):
    content: str
    source: Optional[str] = "manual"

class MemoryResponse(BaseModel):
    id: str
    content: str
    source: str
    created_at: datetime

# backend/app/models/memory.py

from datetime import datetime
from pydantic import BaseModel, Field


class Memory(BaseModel):
    id: str
    content: str
    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Phase 5
    strength: float = 0.8   # initial confidence

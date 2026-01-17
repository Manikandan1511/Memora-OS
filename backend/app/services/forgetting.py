# backend/app/services/forgetting.py

from datetime import datetime, timezone
from math import exp

DECAY_RATE = 0.00002
MIN_STRENGTH = 0.1


def apply_time_decay(created_at: datetime, current_strength: float) -> float:
    """
    Exponential decay based on time.
    Fully UTC-safe (no naive/aware crashes).
    """

    #  FORCE created_at to UTC-aware
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    #  USE UTC-AWARE now
    now = datetime.now(timezone.utc)

    age_seconds = (now - created_at).total_seconds()

    decayed = current_strength * exp(-DECAY_RATE * age_seconds)

    return max(decayed, MIN_STRENGTH)


def reinforce_memory(current_strength: float, boost: float = 0.1) -> float:
    """
    Reinforce memory when recalled.
    """
    return min(current_strength + boost, 1.0)

def reinforce_strength(current_strength: float, boost: float = 0.1) -> float:
    """
    Increase memory strength when recalled.
    """
    return min(current_strength + boost, 1.0)

ARCHIVE_THRESHOLD = 0.3

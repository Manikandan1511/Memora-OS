# backend/app/services/forgetting.py

from datetime import datetime, timezone
from math import exp

from app.config.memory_config import (
    DECAY_CONSTANT,
    REINFORCEMENT_BOOST,
    ARCHIVE_THRESHOLD
)

# TIME DECAY

def apply_time_decay(created_at: datetime, current_strength: float) -> float:
    """
    Apply exponential time decay to memory strength.

    - Fully UTC-safe
    - No naive/aware datetime crashes
    - Never returns negative values
    """

    if not created_at:
        return current_strength

    # Ensure created_at is UTC-aware
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    age_seconds = (now - created_at).total_seconds()

    # Exponential decay
    decayed = current_strength * exp(-DECAY_CONSTANT * age_seconds)

    # Strength should never go below 0
    return max(decayed, 0.0)


# REINFORCEMENT

def reinforce_memory(current_strength: float) -> float:
    """
    Reinforce memory when recalled.

    Uses configured boost.
    Capped at 1.0
    """

    boosted = current_strength + REINFORCEMENT_BOOST

    return min(boosted, 1.0)


# ARCHIVE CHECK

def should_archive(strength: float) -> bool:
    """
    Check whether a memory should be archived
    based on configured threshold.
    """

    return strength <= ARCHIVE_THRESHOLD

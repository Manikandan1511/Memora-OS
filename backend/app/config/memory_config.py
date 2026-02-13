# backend/app/config/memory_config.py

"""
Central cognitive tuning configuration.
Adjust these values to control memory behavior.
"""

# How fast memories decay (higher = faster forgetting)
DECAY_CONSTANT = 0.000002

# Strength threshold below which memory is archived
ARCHIVE_THRESHOLD = 0.3

# Reinforcement boost when memory is recalled
REINFORCEMENT_BOOST = 0.05

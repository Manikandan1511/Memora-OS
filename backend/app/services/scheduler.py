# backend/app/services/scheduler.py

import threading
import time
from app.services.graph import run_decay_cycle

DECAY_INTERVAL = 30  # seconds


def decay_worker():
    """
    Background worker that runs decay continuously.
    """
    while True:
        try:
            print("🧠 Running automatic decay cycle...")
            run_decay_cycle()
        except Exception as e:
            print(f"❌ Decay error: {e}")

        time.sleep(DECAY_INTERVAL)


def start_decay_scheduler():
    """
    Starts decay worker in background thread.
    Safe: non-blocking
    """
    thread = threading.Thread(target=decay_worker, daemon=True)
    thread.start()
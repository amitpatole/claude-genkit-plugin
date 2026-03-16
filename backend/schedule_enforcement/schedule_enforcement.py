from typing import Any, Dict, Optional
import sqlite3
import logging
from datetime import datetime, timezone

from flask import current_app

logging.basicConfig(level=logging.INFO)

def get_non_dev_hours() -> Dict[str, Any]:
    return {
        "start": "18:00",
        "end": "08:00",
        "timezone": "UTC",
    }

def is_within_non_dev_hours(current_time: datetime) -> bool:
    non_dev_hours = get_non_dev_hours()
    non_dev_start = datetime.strptime(non_dev_hours["start"], "%H:%M").time()
    non_dev_end = datetime.strptime(non_dev_hours["end"], "%H:%M").time()
    non_dev_start_time = datetime.combine(current_time.date(), non_dev_start)
    non_dev_end_time = datetime.combine(current_time.date(), non_dev_end)

    if non_dev_start_time > non_dev_end_time:
        non_dev_end_time += timedelta(days=1)

    return non_dev_start_time <= current_time.time() < non_dev_end_time

async def enforce_schedule() -> None:
    async with current_app.app_context():
        conn = await current_app.db.acquire()
        try:
            current_time = datetime.now(timezone.utc)
            if is_within_non_dev_hours(current_time):
                logging.info("Enforcing schedule: Non-development hours are active.")
                # Add logic to enforce schedule here
            else:
                logging.info("No schedule enforcement needed: Outside non-development hours.")
        finally:
            await current_app.db.release(conn)
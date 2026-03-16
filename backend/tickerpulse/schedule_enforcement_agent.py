from typing import Any
import logging
from datetime import datetime, time
from flask import current_app
from sqlite3 import Row
from .db import get_db

logging.basicConfig(level=logging.INFO)

def is_non_dev_hour() -> bool:
    """Determine if the current hour is outside of typical development hours."""
    current_time = datetime.now().time()
    return current_time < time(9, 0) or current_time > time(17, 0)

def enforce_schedule() -> None:
    """Enforce non-development hour schedule by logging a message."""
    if is_non_dev_hour():
        logging.info("Enforcing schedule: Non-development hour detected.")

async def main() -> None:
    """Main entry point for the schedule enforcement agent."""
    db = await get_db()
    db.row_factory = Row
    try:
        if is_non_dev_hour():
            await enforce_schedule()
    finally:
        db.close()
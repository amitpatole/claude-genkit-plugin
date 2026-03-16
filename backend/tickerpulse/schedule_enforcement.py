from typing import Any
import sqlite3
from sqlite3 import Row
from datetime import datetime, time
from flask import current_app

from backend.tickerpulse.utils import get_db_connection

logging.basicConfig(level=logging.INFO)

def is_non_dev_hour(current_time: time) -> bool:
    """Check if the current time is outside of regular development hours."""
    # Define development hours (e.g., 9 AM to 5 PM)
    dev_start_time = time(9, 0)
    dev_end_time = time(17, 0)
    
    # Check if current time is before start or after end of development hours
    return current_time < dev_start_time or current_time >= dev_end_time

async def enforce_schedule(current_time: time) -> bool:
    """Enforce schedule by checking if the current time is a non-development hour."""
    if is_non_dev_hour(current_time):
        logging.info("Enforcing schedule: Non-development hour detected.")
        return True
    return False

async def main() -> None:
    """Main entry point to enforce the schedule."""
    try:
        # Get the current time
        now = datetime.now().time()
        
        # Check if the current time is a non-development hour
        if await enforce_schedule(now):
            # Perform necessary actions (e.g., log, send notifications)
            logging.info("Scheduled actions executed during non-development hour.")
        else:
            logging.info("No actions needed as it's within development hours.")
    except Exception as e:
        logging.error(f"Error enforcing schedule: {e}")

# Ensure the database connection is properly managed
async with get_db_connection() as conn:
    conn.row_factory = Row
    await main()
from typing import Any, Optional
import sqlite3
from datetime import datetime
from flask import current_app

from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

def get_schedule_enforcement_config() -> dict[str, Any]:
    """Fetches the schedule enforcement config from the environment."""
    return {
        "non_dev_hours": (17, 9),  # 5 PM to 9 AM (local time)
        "timezone": "America/New_York",  # Example timezone
    }

def is_within_non_dev_hours() -> bool:
    """Checks if the current time is within non-development hours."""
    config = get_schedule_enforcement_config()
    non_dev_start, non_dev_end = config["non_dev_hours"]
    timezone = config["timezone"]
    
    now = datetime.now()
    now_local = now.astimezone(timezone)
    current_hour = now_local.hour
    
    return non_dev_start <= current_hour < non_dev_end

async def enforce_schedule() -> None:
    """Enforces the schedule by logging if the current time is within non-dev hours."""
    if is_within_non_dev_hours():
        logging.info("Current time is within non-development hours. Schedule enforcement active.")
    else:
        logging.info("Current time is outside non-development hours. Schedule enforcement inactive.")

async def main() -> None:
    """Main entry point for the schedule enforcement agent."""
    try:
        conn = await get_db_connection()
        cursor = await conn.execute("SELECT * FROM some_table", [])
        rows = await cursor.fetchall()
        logging.info(f"Fetched {len(rows)} rows from some_table.")
        
        await enforce_schedule()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        await conn.close()
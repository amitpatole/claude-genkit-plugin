from typing import Any, Dict, List
import sqlite3
from sqlite3 import Error
from datetime import datetime, time
from flask import current_app

from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

def get_non_dev_hours() -> List[Dict[str, time]]:
    return [
        {"start": time(hour=18), "end": time(hour=8)},
    ]

def is_within_non_dev_hours(current_time: time) -> bool:
    non_dev_hours = get_non_dev_hours()
    for hour_range in non_dev_hours:
        if hour_range["start"] <= current_time < hour_range["end"]:
            return True
    return False

async def enforce_schedule(current_time: time) -> None:
    if is_within_non_dev_hours(current_time):
        logging.info("Enforcing schedule during non-development hours.")
        # Logic to enforce schedule can go here
    else:
        logging.info("Not enforcing schedule during development hours.")

async def main() -> None:
    current_time = time(hour=datetime.now().hour, minute=datetime.now().minute, second=datetime.now().second)
    await enforce_schedule(current_time)

async def setup_db() -> None:
    conn = await get_db_connection()
    try:
        cursor = await conn.execute("PRAGMA journal_mode=WAL")
        cursor = await conn.execute("PRAGMA foreign_keys=ON")
        cursor = await conn.execute("CREATE TABLE IF NOT EXISTS schedule_enforcement_log (id INTEGER PRIMARY KEY, timestamp TEXT, message TEXT)")
        await conn.commit()
    except Error as e:
        logging.error(f"Failed to setup database: {e}")
    finally:
        await conn.close()

async def log_enforcement(action: str) -> None:
    conn = await get_db_connection()
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await conn.execute("INSERT INTO schedule_enforcement_log (timestamp, message) VALUES (?, ?)", (timestamp, action))
        await conn.commit()
    except Error as e:
        logging.error(f"Failed to log enforcement: {e}")
    finally:
        await conn.close()

async def handle_schedule_enforcement() -> None:
    await setup_db()
    while True:
        current_time = time(hour=datetime.now().hour, minute=datetime.now().minute, second=datetime.now().second)
        await enforce_schedule(current_time)
        await log_enforcement(f"Enforced schedule at {current_time}")
        await asyncio.sleep(60)  # Check every minute

# Ensure this script is run as a standalone script
if __name__ == "__main__":
    import asyncio
    asyncio.run(handle_schedule_enforcement())
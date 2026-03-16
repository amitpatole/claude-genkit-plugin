from typing import Any, Dict, Optional
import sqlite3
from sqlite3 import Row
from datetime import datetime, timedelta
from flask import current_app

from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

def get_non_dev_hours() -> Dict[str, datetime]:
    return {
        "Monday": datetime(2023, 10, 2, 18, 0),
        "Tuesday": datetime(2023, 10, 3, 18, 0),
        "Wednesday": datetime(2023, 10, 4, 18, 0),
        "Thursday": datetime(2023, 10, 5, 18, 0),
        "Friday": datetime(2023, 10, 6, 18, 0),
    }

def is_within_non_dev_hours(current_time: datetime) -> bool:
    non_dev_hours = get_non_dev_hours()
    today = current_time.strftime("%A")
    if today in non_dev_hours:
        return current_time >= non_dev_hours[today]
    return False

def enforce_schedule() -> None:
    try:
        current_time = datetime.now()
        if is_within_non_dev_hours(current_time):
            logging.info("Within non-development hours, schedule enforcement active.")
        else:
            logging.info("Outside non-development hours, schedule enforcement inactive.")
    except Exception as e:
        logging.error(f"Error during schedule enforcement: {e}")

async def enforce_schedule_async() -> None:
    try:
        current_time = datetime.now()
        if is_within_non_dev_hours(current_time):
            logging.info("Within non-development hours, schedule enforcement active.")
        else:
            logging.info("Outside non-development hours, schedule enforcement inactive.")
    except Exception as e:
        logging.error(f"Error during schedule enforcement: {e}")

# Ensure the database connection is used properly
async def main() -> None:
    async with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM some_table")  # Example query
        rows = await cursor.fetchall()
        for row in rows:
            print(dict(row))  # Example usage of row_factory

# Run the main function if this script is executed directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
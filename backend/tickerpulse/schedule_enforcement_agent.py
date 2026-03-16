from typing import Any, Dict, List
import sqlite3
from sqlite3 import Error
from datetime import datetime, time
from flask import current_app

from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

def get_non_dev_hours() -> List[Dict[str, time]]:
    """Retrieve non-development hours from the configuration."""
    return current_app.config.get("NON_DEV_HOURS", [])

def is_within_non_dev_hours(current_time: time) -> bool:
    """Check if the current time is within non-development hours."""
    non_dev_hours = get_non_dev_hours()
    for start, end in non_dev_hours:
        if start <= current_time < end:
            return True
    return False

async def enforce_schedule() -> None:
    """Enforce the schedule by logging or taking appropriate actions."""
    current_time = time(datetime.now().hour, datetime.now().minute)
    if is_within_non_dev_hours(current_time):
        logging.warning("Non-development hours detected. Enforcing schedule.")
        # Add logic to enforce the schedule here
    else:
        logging.info("Development hours. No schedule enforcement needed.")

async def main() -> None:
    """Main entry point for the schedule enforcement agent."""
    await enforce_schedule()

# Ensure the database connection is properly managed using async context managers
async def get_connection() -> sqlite3.Connection:
    """Get a database connection with proper row factory and parameterized queries."""
    conn = await get_db_connection()
    conn.row_factory = sqlite3.Row
    return conn

async def close_connection(conn: sqlite3.Connection) -> None:
    """Close the database connection."""
    await conn.close()

# Example of using async context managers for database operations
async def fetch_data() -> Dict[str, Any]:
    """Fetch data from the database safely."""
    async with get_connection() as conn:
        cursor = await conn.execute("SELECT * FROM some_table WHERE condition = ?", (some_value,))
        row = await cursor.fetchone()
        return dict(row) if row else {}

# Ensure the main function is awaited properly
async def run() -> None:
    """Run the main function and handle any exceptions."""
    try:
        await main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Example of running the agent
if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
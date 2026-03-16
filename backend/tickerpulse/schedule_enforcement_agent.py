from typing import Any, Dict, Optional
import logging
from datetime import datetime
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager
import sqlite3

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(current_app.config['DATABASE_PATH'], uri=True, timeout=10, isolation_level=None, check_same_thread=False)
    conn.row_factory = Row
    yield conn
    conn.close()

async def enforce_schedule() -> None:
    async with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT user_id, start_time, end_time FROM work_schedule WHERE status = 'active'"
        cursor.execute(query)
        active_schedules = cursor.fetchall()

        for schedule in active_schedules:
            user_id, start_time, end_time = schedule
            current_time = datetime.now()

            if not start_time or not end_time:
                logging.warning(f"Invalid schedule for user {user_id}: start_time or end_time is missing")
                continue

            if current_time < start_time or current_time > end_time:
                logging.info(f"User {user_id} is not working during their scheduled hours")
                # Implement logic to enforce schedule, e.g., send notifications, log violations, etc.
                # For now, just log the violation
                pass
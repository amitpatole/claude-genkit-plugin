from typing import Any, Dict, Optional
import logging
from datetime import datetime
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager

from backend.tickerpulse.utils import get_db_connection

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_db_conn() -> Row:
    conn = await get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

async def enforce_schedule() -> None:
    async with get_db_conn() as conn:
        cursor = await conn.execute("SELECT * FROM schedule WHERE active = 1", ())
        schedule_items = await cursor.fetchall()
        for item in schedule_items:
            schedule_id = item["id"]
            schedule_time = item["time"]
            current_time = datetime.now()
            if current_time.hour >= schedule_time.hour and current_time.minute >= schedule_time.minute:
                logger.info(f"Enforcing schedule item: {schedule_id}")
                # Add logic to enforce the schedule item here
                # For example, send notifications, update states, etc.

async def main() -> None:
    while True:
        await enforce_schedule()
        await asyncio.sleep(3600)  # Check every hour
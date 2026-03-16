from typing import Any, Dict, List
import logging
from datetime import datetime, time
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager

from .database import get_db_connection

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def db_connection() -> Row:
    conn = await get_db_connection()
    try:
        yield conn
    finally:
        await conn.close()

async def enforce_schedule(user_id: int, current_time: time) -> None:
    async with db_connection() as conn:
        query = """
            SELECT * FROM user_preferences
            WHERE user_id = ?
        """
        user_preferences = await conn.execute(query, (user_id,))
        user_preferences = await user_preferences.fetchone()

        if not user_preferences:
            logging.warning(f"No user preferences found for user_id: {user_id}")
            return

        preferred_start_time = time.fromisoformat(user_preferences['start_time'])
        preferred_end_time = time.fromisoformat(user_preferences['end_time'])

        if not (preferred_start_time <= current_time < preferred_end_time):
            logging.info(f"User {user_id} is not allowed to access during current time: {current_time}")
            raise Exception("Access denied during non-development hours")

        logging.info(f"User {user_id} is allowed to access during current time: {current_time}")

async def main() -> None:
    user_id = 1  # Example user ID, should be passed as a parameter
    current_time = time(15, 30)  # Example current time, should be passed as a parameter
    await enforce_schedule(user_id, current_time)
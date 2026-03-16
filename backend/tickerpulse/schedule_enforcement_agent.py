from typing import Any, Optional
import sqlite3
from sqlite3 import Row
from flask import current_app

from backend.utils.db import get_db_connection
from backend.utils.logging import setup_logger

logger = setup_logger(__name__)

class ScheduleEnforcementAgent:
    def __init__(self):
        self.db_connection = get_db_connection()
        self.db_connection.row_factory = sqlite3.Row

    async def enforce_schedule(self, user_id: int) -> Optional[bool]:
        try:
            async with self.db_connection as conn:
                cursor = await conn.execute(
                    "SELECT is_scheduled FROM user_schedule WHERE user_id = ?", (user_id,)
                )
                row = await cursor.fetchone()
                if row is None:
                    logger.warning(f"No schedule found for user_id: {user_id}")
                    return None

                is_scheduled = row["is_scheduled"]
                if not is_scheduled:
                    logger.info(f"User {user_id} is not scheduled during non-dev hours.")
                    return False

                logger.info(f"User {user_id} is scheduled during non-dev hours.")
                return True
        except Exception as e:
            logger.error(f"Error enforcing schedule for user {user_id}: {e}")
            return None

    async def close_db_connection(self):
        await self.db_connection.close()
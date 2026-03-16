from typing import Any, Dict, Optional
import sqlite3
from contextlib import asynccontextmanager
from flask import current_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_db_connection() -> sqlite3.Connection:
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db, uri=True)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

async def enforce_schedule(user_id: int, current_time: str) -> bool:
    async with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT non_dev_hours FROM user_schedules WHERE user_id = ?"
        cursor.execute(query, (user_id,))
        schedule = cursor.fetchone()
        
        if not schedule:
            logger.warning(f"No schedule found for user_id {user_id}")
            return False
        
        non_dev_hours = schedule['non_dev_hours']
        
        if current_time in non_dev_hours:
            logger.info(f"User {user_id} is in non-dev hours, schedule enforced.")
            return True
        else:
            logger.info(f"User {user_id} is not in non-dev hours, schedule not enforced.")
            return False
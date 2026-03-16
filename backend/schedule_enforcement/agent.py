from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import connect, Row
from contextlib import asynccontextmanager
from config import ALLOWED_DEPLOYMENT_HOURS, DEPLOYMENT_VIOLATION_LOG_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_db_connection() -> Any:
    conn = connect(current_app.config['DATABASE_PATH'], isolation_level=None, journal_mode='WAL')
    conn.row_factory = Row
    yield conn
    conn.close()

async def is_allowed_deployment_time() -> bool:
    now = datetime.now(timezone.utc)
    allowed_start = datetime(now.year, now.month, now.day, 22, 0, 0, tzinfo=timezone.utc)
    allowed_end = datetime(now.year, now.month, now.day, 8, 0, 0, tzinfo=timezone.utc)
    return allowed_start <= now < allowed_end

async def log_deployment_violation(user_id: str, deployment_time: datetime) -> None:
    async with get_db_connection() as conn:
        cursor = conn.cursor()
        await cursor.execute("INSERT INTO deployment_violations (user_id, deployment_time) VALUES (?, ?)",
                             (user_id, deployment_time))
        conn.commit()

async def notify_user_violation(user_id: str, deployment_time: datetime) -> None:
    logger.info(f"Deployment violation detected at {deployment_time} for user {user_id}")
    # Notify via Genkit Explorer sidebar (assuming a function exists for this)
    await notify_genkit_explorer(user_id, deployment_time)

async def notify_genkit_explorer(user_id: str, deployment_time: datetime) -> None:
    # Placeholder for actual notification logic
    pass

async def enforce_schedule(user_id: str, deployment_time: datetime) -> None:
    if not await is_allowed_deployment_time():
        await log_deployment_violation(user_id, deployment_time)
        await notify_user_violation(user_id, deployment_time)

# Example usage
if __name__ == "__main__":
    user_id = "user123"
    deployment_time = datetime(2023, 10, 1, 9, 0, 0, tzinfo=timezone.utc)
    await enforce_schedule(user_id, deployment_time)
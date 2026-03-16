from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager
from backend.database.db import get_db_connection

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def db_connection():
    conn = await get_db_connection()
    try:
        yield conn
    finally:
        await conn.close()

async def is_allowed_time() -> bool:
    """Check if the current time is within the allowed deployment hours."""
    now = datetime.now(timezone.utc)
    allowed_start = datetime.combine(now.date(), datetime.min.time()) + timezone(
        "EST"
    ).utcoffset(now)
    allowed_end = allowed_start + 10  # 10 hours window
    return allowed_start <= now < allowed_end

async def log_violation(user_id: str, deployment_time: datetime) -> None:
    """Log a deployment violation to a file."""
    with (await db_connection()) as conn:
        conn.row_factory = Row
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO deployment_violations (user_id, deployment_time) VALUES (?, ?)",
            (user_id, deployment_time),
        )
        conn.commit()

async def notify_user(user_id: str, deployment_time: datetime) -> None:
    """Notify the user via Genkit Explorer sidebar."""
    # Assuming Genkit Explorer has a method to send notifications
    await current_app.notify_user(user_id, f"Deployment attempt at {deployment_time} was blocked.")

async def enforce_schedule(user_id: str, deployment_time: datetime) -> None:
    """Enforce schedule by checking allowed time and logging violations."""
    if not await is_allowed_time():
        await log_violation(user_id, deployment_time)
        await notify_user(user_id, deployment_time)
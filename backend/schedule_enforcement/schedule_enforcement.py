from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager
from backend.database import get_db

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def get_db_connection() -> Row:
    db = await get_db()
    try:
        yield db
    finally:
        db.close()

async def is_allowed_time() -> bool:
    current_time = datetime.now(timezone.utc).astimezone().hour
    return 22 <= current_time <= 8

async def log_violation(user_id: str, deployment_time: datetime) -> None:
    with (await get_db_connection()) as db:
        db.row_factory = Row
        db.execute(
            "INSERT INTO deployment_violations (user_id, deployment_time) VALUES (?, ?)",
            (user_id, deployment_time)
        )
        db.commit()

async def notify_user(user_id: str, deployment_time: datetime) -> None:
    current_app.logger.info(f"Deployment attempt at {deployment_time} blocked for user {user_id}")

async def enforce_schedule(user_id: str, deployment_time: datetime) -> None:
    if not await is_allowed_time():
        await log_violation(user_id, deployment_time)
        await notify_user(user_id, deployment_time)
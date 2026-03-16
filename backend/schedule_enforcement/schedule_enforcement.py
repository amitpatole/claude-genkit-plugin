from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager
from .db import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_async_db() -> Row:
    db = await get_db()
    try:
        yield db
    finally:
        db.close()

async def is_allowed_time() -> bool:
    now = datetime.now(timezone.utc).astimezone(timezone(offset=-(5, 0)))  # EST is UTC-5
    return 22 <= now.hour < 8

async def log_violation(user_id: int, deployment_time: datetime) -> None:
    with (await get_async_db()) as db:
        db.execute(
            "INSERT INTO deployment_violations (user_id, deployment_time) VALUES (?, ?)",
            (user_id, deployment_time),
        )
        db.commit()

async def notify_user(user_id: int, deployment_time: datetime) -> None:
    current_app.genkit.send_notification(
        user_id,
        f"Deployment attempt at {deployment_time} was blocked due to schedule enforcement.",
    )

async def enforce_schedule(user_id: int, deployment_time: datetime) -> None:
    if not await is_allowed_time():
        await log_violation(user_id, deployment_time)
        await notify_user(user_id, deployment_time)
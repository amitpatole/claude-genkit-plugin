from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row
import os

from .db import get_db, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_allowed_time() -> bool:
    """Check if the current time is within the allowed deployment hours (10 PM - 8 AM EST)."""
    now = datetime.now(timezone('EST'))
    return 22 <= now.hour < 8

async def log_deployment_attempt(user_id: int, time: datetime, success: bool) -> None:
    """Log deployment attempts to a file."""
    db = await get_db()
    await db.execute(
        "INSERT INTO deployment_attempts (user_id, time, success) VALUES (?, ?, ?)",
        (user_id, time, success),
    )
    await db.commit()

async def send_notification(user_id: int, time: datetime, success: bool) -> None:
    """Send a notification to the user via Genkit Explorer sidebar."""
    # Assuming Genkit Explorer has a method to send notifications
    current_app.genkit_explorer.send_notification(
        user_id=user_id,
        message=f"Deployment attempt at {time} {'succeeded' if success else 'failed'}",
    )

async def enforce_schedule(user_id: int) -> None:
    """Enforce deployment schedule by blocking non-allowed deployments and logging violations."""
    if not is_allowed_time():
        logger.info(f"Deployment attempt blocked for user {user_id} at {datetime.now(timezone('EST'))}")
        await log_deployment_attempt(user_id, datetime.now(timezone('EST')), False)
        await send_notification(user_id, datetime.now(timezone('EST')), False)
    else:
        logger.info(f"Deployment allowed for user {user_id} at {datetime.now(timezone('EST'))}")

async def init_schedule_enforcement() -> None:
    """Initialize the schedule enforcement agent."""
    await init_db()
    while True:
        await enforce_schedule(current_app.user_id)
        await asyncio.sleep(60)  # Check every minute
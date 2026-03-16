from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row
import os

from .db import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_off_peak_hour() -> bool:
    """Check if the current hour is outside the allowed deployment window (10 PM - 8 AM EST)."""
    est_tz = timezone(-5, 'EST')
    now = datetime.now(est_tz)
    return now.hour < 20 or now.hour >= 8

def log_violation(deployment_id: int, user_id: int, violation_time: datetime) -> None:
    """Log a violation to a file."""
    log_path = os.path.join(current_app.root_path, 'logs', 'violation_logs.txt')
    with open(log_path, 'a') as log_file:
        log_file.write(f"Deployment {deployment_id} by user {user_id} violated schedule enforcement at {violation_time}\n")

async def notify_user(user_id: int, violation_time: datetime) -> None:
    """Notify the user via the Genkit Explorer sidebar."""
    # Assuming Genkit Explorer has a method to send notifications
    await current_app.notify_user(user_id, f"Your deployment attempt at {violation_time} was blocked due to schedule enforcement.")

async def enforce_schedule(deployment_id: int, user_id: int) -> None:
    """Enforce schedule by checking if the current time is within the allowed deployment window."""
    if is_off_peak_hour():
        logger.info(f"Deployment {deployment_id} by user {user_id} is within the allowed schedule window.")
        return

    violation_time = datetime.now(timezone.utc)
    log_violation(deployment_id, user_id, violation_time)
    await notify_user(user_id, violation_time)

# Example usage in a route
# async def deploy_application(deployment_id: int, user_id: int) -> None:
#     await enforce_schedule(deployment_id, user_id)
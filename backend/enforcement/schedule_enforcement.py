from typing import Any, Optional
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row

from .db import get_db, init_db, row_to_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_within_allowed_hours() -> bool:
    """Check if the current time is within the allowed deployment hours (10 PM - 8 AM EST)."""
    est_timezone = timezone(offset=-5 * 3600)  # EST is UTC-5
    current_time = datetime.now(est_timezone)
    return 22 <= current_time.hour < 8

def log_violation(deployment_id: int, user_id: int, violation_time: datetime) -> None:
    """Log a deployment violation to a file."""
    with open("violation_logs.txt", "a") as log_file:
        log_file.write(f"Deployment {deployment_id} by user {user_id} violated schedule at {violation_time}\n")

async def notify_user_violation(deployment_id: int, user_id: int, violation_time: datetime) -> None:
    """Notify the user via the Genkit Explorer sidebar about a deployment violation."""
    # Assuming Genkit Explorer has a method to notify users
    await current_app.notify_user_violation(deployment_id, user_id, violation_time)

async def enforce_schedule(deployment_id: int, user_id: int) -> Optional[bool]:
    """Enforce schedule by blocking deployments outside allowed hours and logging violations."""
    if not is_within_allowed_hours():
        violation_time = datetime.now(timezone.utc)
        log_violation(deployment_id, user_id, violation_time)
        await notify_user_violation(deployment_id, user_id, violation_time)
        return False
    return True
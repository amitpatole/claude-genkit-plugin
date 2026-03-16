from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row

from .config import ALLOWED_DEPLOYMENT_HOURS, DEPLOYMENT_LOG_FILE, DEPLOYMENT_VIOLATION_EMAIL
from .db import get_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_allowed_deployment_time() -> bool:
    """
    Check if the current time is within the allowed deployment hours (10 PM - 8 AM EST).
    """
    now = datetime.now(timezone('EST'))
    return ALLOWED_DEPLOYMENT_HOURS[0] <= now.hour < ALLOWED_DEPLOYMENT_HOURS[1]

async def log_deployment_violation(deployment_time: datetime, user_id: int) -> None:
    """
    Log a deployment violation to the specified file.
    
    :param deployment_time: Time of the attempted deployment
    :param user_id: ID of the user who attempted the deployment
    """
    try:
        conn = await get_db_connection()
        cursor = conn.cursor(row_factory=Row)
        cursor.execute("INSERT INTO deployment_violations (user_id, deployment_time) VALUES (?, ?)", (user_id, deployment_time))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to log deployment violation: {e}")

async def notify_user_of_violation(user_id: int) -> None:
    """
    Notify the user via the Genkit Explorer sidebar about the deployment violation.
    
    :param user_id: ID of the user who attempted the deployment
    """
    try:
        conn = await get_db_connection()
        cursor = conn.cursor(row_factory=Row)
        cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
        user_email = cursor.fetchone()["email"]
        # Assuming Genkit Explorer has a method to notify users
        current_app.notify_user_of_violation(user_email)
    except Exception as e:
        logger.error(f"Failed to notify user of violation: {e}")

async def enforce_schedule() -> None:
    """
    Enforce the deployment schedule by blocking deployments outside the allowed hours and logging violations.
    """
    if not is_allowed_deployment_time():
        logger.warning("Deployment attempted outside allowed hours. Blocking deployment.")
        user_id = 1  # Placeholder for user ID, should be passed from the caller
        await log_deployment_violation(datetime.now(timezone('EST')), user_id)
        await notify_user_of_violation(user_id)

# Example usage
if __name__ == "__main__":
    enforce_schedule()
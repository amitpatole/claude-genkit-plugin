from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row

from .utils import get_current_time, get_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScheduleEnforcementAgent:
    def __init__(self):
        self.allowed_hours = (22, 8)  # 10 PM - 8 AM EST

    def is_within_allowed_hours(self, current_time: datetime) -> bool:
        """
        Check if the current time is within the allowed deployment hours.

        Args:
            current_time (datetime): The current time to check.

        Returns:
            bool: True if within allowed hours, False otherwise.
        """
        return self.allowed_hours[0] <= current_time.hour < self.allowed_hours[1]

    async def enforce_schedule(self, deployment_time: datetime) -> bool:
        """
        Enforce the schedule by checking if the deployment time is within allowed hours.

        Args:
            deployment_time (datetime): The time at which the deployment is attempted.

        Returns:
            bool: True if the deployment is allowed, False if it's a violation.
        """
        current_time = await get_current_time()
        if not self.is_within_allowed_hours(current_time):
            logger.info(f"Deployment attempt at {deployment_time} is outside allowed hours.")
            await self.log_violation(deployment_time)
            await self.notify_user(deployment_time)
            return False
        return True

    async def log_violation(self, deployment_time: datetime) -> None:
        """
        Log the violation to a file.

        Args:
            deployment_time (datetime): The time at which the deployment was attempted.
        """
        db = await get_db_connection()
        try:
            db.row_factory = Row
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO deployment_violations (time) VALUES (?)",
                (deployment_time,)
            )
            db.commit()
        finally:
            db.close()

    async def notify_user(self, deployment_time: datetime) -> None:
        """
        Notify the user via the Genkit Explorer sidebar.

        Args:
            deployment_time (datetime): The time at which the deployment was attempted.
        """
        current_app.notify_user(f"Deployment attempt at {deployment_time} is outside allowed hours.")


async def get_current_time() -> datetime:
    """
    Get the current time in the specified timezone.

    Returns:
        datetime: The current time.
    """
    return datetime.now(timezone.utc).astimezone(timezone(offset=-(5 * 3600)))  # EST is UTC-5
from typing import Any
import logging
from datetime import datetime, timezone
from sqlite3 import Row
from flask import current_app

from .db import get_db, SQLiteRow  # Assuming a custom SQLiteRow class is defined

logging.basicConfig(level=logging.INFO)

class ScheduleEnforcementAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def enforce_schedule(self) -> None:
        self.logger.info("Starting schedule enforcement agent")

        async with get_db().acquire() as conn:
            self.logger.info("Acquired database connection")

            # Get current time
            now = datetime.now(timezone.utc)
            self.logger.info(f"Current time: {now}")

            # Fetch non-development hours from the database
            non_dev_hours = await self.fetch_non_dev_hours(conn)
            self.logger.info(f"Non-development hours: {non_dev_hours}")

            # Check if current time is within non-development hours
            if now.hour in non_dev_hours:
                self.logger.warning("Current time is within non-development hours. Enforcing schedule.")
                # Implement logic to enforce schedule here
                # Example: Send notifications, log actions, etc.
            else:
                self.logger.info("Current time is outside non-development hours. No action needed.")

    async def fetch_non_dev_hours(self, conn: SQLiteRow) -> list[int]:
        self.logger.info("Fetching non-development hours from the database")

        query = "SELECT hour FROM non_dev_hours"
        non_dev_hours = [row.hour for row in await conn.execute(query)]
        self.logger.info(f"Fetched non-development hours: {non_dev_hours}")

        return non_dev_hours
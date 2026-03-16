from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "tickerpulse.db"
ALLOWED_HOURS = (22, 8)  # 10 PM - 8 AM EST

class ScheduleEnforcementAgent:
    def __init__(self):
        self.db_connection = sqlite3.connect(DB_PATH, uri=True, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db_connection.row_factory = sqlite3.Row
        self.cursor = self.db_connection.cursor()

    def is_allowed_time(self) -> bool:
        now = datetime.now(timezone.utc).astimezone(timezone(offset=3600 * 5))  # EST
        return ALLOWED_HOURS[0] <= now.hour < ALLOWED_HOURS[1]

    async def enforce_schedule(self, deployment_time: datetime) -> None:
        if not self.is_allowed_time():
            logger.info(f"Deployment attempt at {deployment_time} is outside allowed hours {ALLOWED_HOURS}.")
            self.log_violation(deployment_time)
            await self.notify_user(deployment_time)

    def log_violation(self, deployment_time: datetime) -> None:
        self.cursor.execute("INSERT INTO deployment_violations (time) VALUES (?)", (deployment_time,))
        self.db_connection.commit()

    async def notify_user(self, deployment_time: datetime) -> None:
        # Assuming Genkit Explorer has a method to show notifications
        await current_app.notify_user(f"Deployment attempt at {deployment_time} is blocked due to schedule constraints.")

    def __del__(self):
        self.db_connection.close()
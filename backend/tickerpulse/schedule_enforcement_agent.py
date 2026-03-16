from typing import Any, Dict, List
import sqlite3
from sqlite3 import Row
from datetime import datetime
import logging

from flask import current_app

logger = logging.getLogger(__name__)

def get_non_dev_hours() -> List[Dict[str, Any]]:
    """Fetch non-development hours from the config."""
    config = current_app.config.get("NON_DEV_HOURS", [])
    return config

class ScheduleEnforcementAgent:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, isolation_level=None, uri=True)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    async def enforce_schedule(self) -> None:
        """Enforce the schedule by checking current time against non-dev hours."""
        non_dev_hours = get_non_dev_hours()
        current_time = datetime.now().time()

        for hour_range in non_dev_hours:
            start_time = datetime.strptime(hour_range["start"], "%H:%M").time()
            end_time = datetime.strptime(hour_range["end"], "%H:%M").time()

            if start_time <= current_time <= end_time:
                logger.warning("Current time is within non-development hours. Enforcing schedule.")
                # Add logic to enforce the schedule here
                break

    async def __aenter__(self) -> "ScheduleEnforcementAgent":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.close()
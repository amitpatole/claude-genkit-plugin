from typing import Any, Dict, Optional
import sqlite3
from sqlite3 import Row
import logging

from flask import current_app

logger = logging.getLogger(__name__)

def get_non_dev_hours() -> Dict[str, Any]:
    """Fetch non-development hours from config."""
    return current_app.config.get("NON_DEV_HOURS", {})

class ScheduleEnforcementAgent:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    async def connect(self) -> None:
        self.connection = await sqlite3.connect(self.db_path, isolation_level=None, uri=True, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.connection.row_factory = sqlite3.Row

    async def enforce_schedule(self, user_id: str) -> bool:
        non_dev_hours = get_non_dev_hours()
        if not non_dev_hours:
            logger.warning("No non-development hours configured.")
            return False

        current_time = await self._get_current_time()
        if current_time in non_dev_hours:
            logger.info(f"Enforced schedule for user {user_id} during non-dev hours.")
            return True
        else:
            logger.info(f"Allowing user {user_id} during dev hours.")
            return False

    async def _get_current_time(self) -> str:
        async with self.connection.execute("SELECT strftime('%H:%M', 'now', 'localtime') as current_time") as cursor:
            row = await cursor.fetchone()
            return row["current_time"] if row else "00:00"

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()

# Example usage and testing
if __name__ == "__main__":
    agent = ScheduleEnforcementAgent(db_path="tickerpulse.db")
    agent.connect()
    result = asyncio.run(agent.enforce_schedule("user123"))
    print(result)
    asyncio.run(agent.close())
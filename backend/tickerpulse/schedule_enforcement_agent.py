from typing import Any, AsyncContextManager, AsyncIterator, Optional
import sqlite3
from datetime import datetime, time
from flask import current_app

from tickerpulse.models import ScheduleEnforcementModel

logging.basicConfig(level=logging.INFO)


class ScheduleEnforcementAgent:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def _get_schedule(self) -> Optional[ScheduleEnforcementModel]:
        try:
            conn = await self._get_db_connection()
            cursor = await conn.execute("SELECT * FROM schedules WHERE is_active = 1 LIMIT 1")
            row = await cursor.fetchone()
            if row:
                return ScheduleEnforcementModel(**row)
            return None
        finally:
            await conn.close()

    async def _get_db_connection(self) -> AsyncContextManager[sqlite3.Connection]:
        return current_app.async_sqlite_db.connect()

    async def enforce_schedule(self) -> None:
        schedule = await self._get_schedule()
        if not schedule:
            logging.info("No active schedule found.")
            return

        current_time = datetime.now().time()
        if not (schedule.start_time <= current_time < schedule.end_time):
            logging.info("Current time is outside the active schedule.")
            return

        logging.info("Enforcing schedule.")
        # Add your enforcement logic here
        pass

    async def run(self) -> None:
        await self.enforce_schedule()


def configure_db(app: Any) -> None:
    app.async_sqlite_db = sqlite3.connect(
        current_app.config["DB_PATH"], isolation_level=None, check_same_thread=False, factory=sqlite3.Row
    )
    app.async_sqlite_db.execute("PRAGMA journal_mode=WAL")
    app.async_sqlite_db.row_factory = sqlite3.Row
    app.async_sqlite_db.execute("CREATE TABLE IF NOT EXISTS schedules (id INTEGER PRIMARY KEY, start_time TIME, end_time TIME, is_active BOOLEAN)")
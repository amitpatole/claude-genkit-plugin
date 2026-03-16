from typing import Any
import sqlite3
from datetime import datetime
from flask import current_app

from tickerpulse.utils import get_current_time

logging.basicConfig(level=logging.INFO)

def get_schedule_enforcement_config() -> dict[str, Any]:
    return current_app.config.get("SCHEDULE_ENFORCEMENT", {})

class ScheduleEnforcementAgent:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    async def enforce_schedule(self) -> None:
        try:
            current_time = await get_current_time()
            non_dev_hours = get_schedule_enforcement_config().get("non_dev_hours", [])

            if not non_dev_hours:
                logging.warning("No non-development hours configured for schedule enforcement.")
                return

            if current_time.hour in non_dev_hours:
                logging.info("Current time is within non-development hours. Enforcing schedule...")
                # Logic to enforce schedule goes here
                pass
            else:
                logging.info("Current time is outside non-development hours. No need to enforce schedule.")
        except Exception as e:
            logging.error(f"Error enforcing schedule: {e}")
        finally:
            self.cursor.close()
            self.conn.close()

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()
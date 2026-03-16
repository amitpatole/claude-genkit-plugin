from typing import Any, Dict, Optional
import sqlite3
from sqlite3 import Row
from flask import current_app
from datetime import datetime, time

from tickerpulse.models import ScheduleEnforcementLog

logging.basicConfig(level=logging.INFO)

def get_current_time() -> time:
    return datetime.now().time()

def is_in_non_dev_hours(current_time: time) -> bool:
    start_time = time(9, 0, 0)
    end_time = time(17, 0, 0)
    return start_time <= current_time < end_time

def enforce_schedule(log: bool = True) -> Optional[ScheduleEnforcementLog]:
    current_time = get_current_time()
    if is_in_non_dev_hours(current_time):
        logging.info("Enforcement not needed: current time is within non-development hours.")
        return None

    with current_app.app_context():
        conn = sqlite3.connect(current_app.config['DATABASE_PATH'], uri=True, uri=True, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO schedule_enforcement_logs (timestamp) VALUES (?)", (current_time,))
            conn.commit()
            log_entry = ScheduleEnforcementLog(timestamp=current_time)
            logging.info(f"Enforcement log entry created: {log_entry}")
            return log_entry
        except Exception as e:
            logging.error(f"Failed to enforce schedule: {e}")
            return None
        finally:
            conn.close()
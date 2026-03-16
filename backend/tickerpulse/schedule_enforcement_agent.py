from typing import Any, Dict, Optional
import sqlite3
from sqlite3 import Row
from datetime import datetime, timezone
from flask import current_app

from backend.utils.db import get_db_connection
from backend.models.schedule import Schedule

logger = logging.getLogger(__name__)

def enforce_schedule(user_id: int, current_time: datetime) -> Optional[bool]:
    """
    Enforces the schedule for a given user based on the current time.

    :param user_id: ID of the user to enforce the schedule for.
    :param current_time: Current datetime to check against the schedule.
    :return: True if the user is within their non-development hours, False otherwise.
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = Row
            query = "SELECT non_dev_hours FROM user_schedules WHERE user_id = ?"
            result = conn.execute(query, (user_id,)).fetchone()
            if result is None:
                logger.warning(f"No schedule found for user_id: {user_id}")
                return None

            non_dev_hours = result["non_dev_hours"]
            start_time, end_time = non_dev_hours.split("-")
            start_time = datetime.strptime(start_time, "%H:%M").time()
            end_time = datetime.strptime(end_time, "%H:%M").time()

            current_time = current_time.time()
            if start_time <= current_time < end_time:
                return True
            else:
                return False
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
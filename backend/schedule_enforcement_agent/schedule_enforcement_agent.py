from typing import Any, Optional
import sqlite3
from datetime import datetime, time
from flask import current_app

from backend.utils.db import get_db_connection
from backend.models.user import User
from backend.models.schedule import Schedule

logger = logging.getLogger(__name__)

def enforce_schedule(user_id: int, current_time: time) -> Optional[bool]:
    """
    Enforces the schedule for a given user based on the current time.
    Returns True if the user is in non-development hours, False otherwise.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(row_factory=sqlite3.Row)
        user = User.get_by_id(user_id)
        schedule = Schedule.get_by_user_id(user_id)
        
        if not user or not schedule:
            return False
        
        if schedule.non_dev_start <= current_time < schedule.non_dev_end:
            return True
        else:
            return False
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return False
    finally:
        conn.close()
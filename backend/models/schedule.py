from typing import Any
from datetime import time

class Schedule:
    """
    Represents a user's schedule.
    """
    
    non_dev_start: time
    non_dev_end: time

    @classmethod
    def get_by_user_id(cls, user_id: int) -> Optional['Schedule']:
        """
        Retrieves a schedule by user ID.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schedules WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return cls(**row)
        return None
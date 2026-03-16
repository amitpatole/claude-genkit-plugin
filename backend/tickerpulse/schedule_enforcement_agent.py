from typing import Any, Optional
import sqlite3
from sqlite3 import Row
from datetime import datetime, time
from flask import current_app

from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

class ScheduleEnforcementAgent:
    def __init__(self):
        self.db_connection = get_db_connection()

    def enforce_schedule(self, user_id: int) -> Optional[Row]:
        """
        Enforce non-development hours for a user.
        
        :param user_id: ID of the user to enforce schedule for.
        :return: Row object with schedule details if user is in development hours, else None.
        """
        try:
            with self.db_connection as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                current_time = datetime.now().time()
                development_hours_start = time(9, 0)
                development_hours_end = time(17, 0)

                if development_hours_start <= current_time < development_hours_end:
                    cursor.execute(
                        "SELECT * FROM user_schedule WHERE user_id = ?",
                        (user_id,)
                    )
                    return cursor.fetchone()
                else:
                    return None
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None
        finally:
            self.db_connection.close()

def main():
    agent = ScheduleEnforcementAgent()
    result = agent.enforce_schedule(1)
    if result:
        logging.info(f"User schedule: {result}")
    else:
        logging.info("User is in non-development hours.")

if __name__ == "__main__":
    main()
from typing import Any
import sqlite3
from sqlite3 import Row
from flask import current_app

from backend.utils import get_db_connection

logging.basicConfig(level=logging.INFO)

def enforce_schedule() -> None:
    """
    Enforce the schedule by checking if the current time is outside of non-development hours.
    """
    conn = get_db_connection()
    cursor = conn.cursor(row_factory=Row)
    try:
        # Get the current time
        current_time = current_app.config['CURRENT_TIME']

        # Query the database for non-development hours
        cursor.execute("SELECT start_time, end_time FROM non_dev_hours")
        non_dev_hours = cursor.fetchall()

        for start_time, end_time in non_dev_hours:
            if start_time <= current_time < end_time:
                logging.info("Schedule enforced: Current time is within non-development hours.")
                return

        logging.info("Schedule enforced: Current time is outside non-development hours.")
    finally:
        conn.close()

def get_db_connection() -> sqlite3.Connection:
    """
    Get a database connection using the SQLite database configured in the app.
    """
    conn = sqlite3.connect(current_app.config['DATABASE_PATH'], uri=True)
    conn.row_factory = sqlite3.Row
    return conn
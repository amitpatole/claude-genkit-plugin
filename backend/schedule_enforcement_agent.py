from typing import Any
import sqlite3
from sqlite3 import Error
from datetime import datetime, time
from flask import current_app

from .config import get_db_path

logging.basicConfig(level=logging.INFO)

def get_non_dev_hours() -> tuple[time, time]:
    """Return the start and end times for non-development hours."""
    return time(18, 0), time(8, 0)

def is_within_non_dev_hours(current_time: time) -> bool:
    """Check if the current time is within non-development hours."""
    start_time, end_time = get_non_dev_hours()
    return start_time <= current_time < end_time

def enforce_schedule(user_id: int) -> None:
    """Enforce schedule by logging or taking action if within non-development hours."""
    current_time = datetime.now().time()
    if is_within_non_dev_hours(current_time):
        logging.warning(f"User {user_id} is active during non-development hours.")
        # Add logic to take appropriate action here, e.g., send alert, log more details, etc.

def init_db() -> None:
    """Initialize the database with necessary tables and constraints."""
    db_path = get_db_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                is_active BOOLEAN DEFAULT FALSE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                activity TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
    except Error as e:
        logging.error(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()

def main() -> None:
    """Main entry point to run the schedule enforcement agent."""
    init_db()
    enforce_schedule(1)  # Example user ID, replace with actual logic

if __name__ == "__main__":
    main()
from typing import Any
import sqlite3
from datetime import datetime
from flask import current_app
from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

def enforce_schedule() -> None:
    """Enforce schedule by checking current time against non-development hours."""
    conn = get_db_connection()
    cursor = conn.cursor(row_factory=sqlite3.Row)
    
    try:
        # Get current time
        now = datetime.now()
        
        # Query non-development hours from the database
        cursor.execute("SELECT start_time, end_time FROM non_dev_hours")
        non_dev_hours = cursor.fetchall()
        
        # Check if current time is within non-development hours
        for hour in non_dev_hours:
            start_time = hour["start_time"]
            end_time = hour["end_time"]
            if start_time <= now.time() <= end_time:
                logging.info("Current time is within non-development hours. Enforcing schedule.")
                # Implement logic to enforce schedule here
                break
    finally:
        conn.close()
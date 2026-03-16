from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_PATH = "path/to/database.db"

def is_allowed_time() -> bool:
    """
    Check if the current time is within the allowed deployment hours (10 PM - 8 AM EST).
    """
    now = datetime.now(timezone.utc).astimezone(timezone(offset=-5, name="EST"))
    return 22 <= now.hour < 8

def log_violation(user_id: str, deployment_time: datetime, message: str) -> None:
    """
    Log a deployment violation to the database and a file.
    """
    conn = sqlite3.connect(DATABASE_PATH, uri=True, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO violations (user_id, deployment_time, message) VALUES (?, ?, ?)",
                       (user_id, deployment_time, message))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    with open("logs/deployment_violations.log", "a") as log_file:
        log_file.write(f"{deployment_time}: User {user_id} attempted deployment during non-development hours. Message: {message}\n")

def notify_user(user_id: str, deployment_time: datetime, message: str) -> None:
    """
    Notify the user via the Genkit Explorer sidebar about the deployment violation.
    """
    current_app.logger.info(f"Deployment attempt from user {user_id} at {deployment_time} during non-development hours. Message: {message}")

def enforce_schedule(user_id: str, deployment_time: datetime, message: str) -> None:
    """
    Enforce the schedule by checking the allowed time and logging/notifications if necessary.
    """
    if not is_allowed_time():
        log_violation(user_id, deployment_time, message)
        notify_user(user_id, deployment_time, message)

# Example usage
if __name__ == "__main__":
    enforce_schedule("user123", datetime(2023, 10, 1, 9, 0, 0, tzinfo=timezone.utc), "Attempted deployment")
from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
import sqlite3
from sqlite3 import Error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_allowed_time() -> bool:
    """Check if the current time is within allowed deployment hours (10 PM - 8 AM EST)."""
    now = datetime.now(timezone('EST'))
    return 22 <= now.hour < 8

def log_deployment_attempt(deployment_id: int, timestamp: datetime) -> None:
    """Log deployment attempt details to a file."""
    with open(current_app.config['VIOLATION_LOG_PATH'], 'a') as log_file:
        log_file.write(f"Deployment attempt {deployment_id} at {timestamp}\n")

def notify_user_via_genkit(deployment_id: int, timestamp: datetime) -> None:
    """Notify the user via the Genkit Explorer sidebar about a violation."""
    notification_message = f"Deployment attempt {deployment_id} at {timestamp} is outside allowed hours."
    current_app.genkit_explorer.notify(notification_message)

def enforce_schedule(deployment_id: int) -> None:
    """Enforce schedule by checking allowed time and logging/reporting violations."""
    try:
        if not is_allowed_time():
            timestamp = datetime.now(timezone('EST'))
            log_deployment_attempt(deployment_id, timestamp)
            notify_user_via_genkit(deployment_id, timestamp)
    except Exception as e:
        logger.error(f"Error enforcing schedule: {e}")

def get_violation_reports() -> list[tuple[int, datetime]]:
    """Retrieve violation reports from the database."""
    conn = sqlite3.connect(current_app.config['DB_PATH'], factory=sqlite3.Row)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT deployment_id, timestamp FROM violation_reports")
    return [dict(row) for row in cursor.fetchall()]

def log_violation_to_db(deployment_id: int, timestamp: datetime) -> None:
    """Log violation to the database."""
    conn = sqlite3.connect(current_app.config['DB_PATH'], factory=sqlite3.Row)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("INSERT INTO violation_reports (deployment_id, timestamp) VALUES (?, ?)",
                   (deployment_id, timestamp))
    conn.commit()

def enforce_schedule_with_db(deployment_id: int) -> None:
    """Enforce schedule by checking allowed time and logging/reporting violations to the database."""
    try:
        if not is_allowed_time():
            timestamp = datetime.now(timezone('EST'))
            log_violation_to_db(deployment_id, timestamp)
            notify_user_via_genkit(deployment_id, timestamp)
    except Exception as e:
        logger.error(f"Error enforcing schedule with DB: {e}")
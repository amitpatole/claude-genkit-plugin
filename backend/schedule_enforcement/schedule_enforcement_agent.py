from typing import Any
import logging
from datetime import datetime, timezone
from sqlite3 import connect, Row
from flask import current_app

from .config import ALLOWED_HOURS, VIOLATION_LOG_PATH, NOTIFICATION_SIDEBAR_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_allowed_time() -> bool:
    """Check if current time is within allowed hours (10 PM - 8 AM EST)."""
    now = datetime.now(timezone('EST'))
    return ALLOWED_HOURS['start'] <= now.hour < ALLOWED_HOURS['end']

def log_violation(deployment_id: int, timestamp: datetime) -> None:
    """Log a deployment violation to the specified file path."""
    with current_app.app_context():
        with connect(current_app.config['DATABASE_PATH'], uri=True, uri_same_file=True, isolation_level=None, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, row_factory=Row) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO deployment_violations (deployment_id, timestamp) VALUES (?, ?)", (deployment_id, timestamp))
            conn.commit()
            logger.info(f"Logged violation: {deployment_id} at {timestamp}")

def send_notification(deployment_id: int, timestamp: datetime) -> None:
    """Send a notification to the Genkit Explorer sidebar about a deployment violation."""
    notification_data = {
        "deployment_id": deployment_id,
        "timestamp": timestamp.isoformat(),
    }
    # Assuming Genkit Explorer has a method to send notifications
    current_app.genkit_explorer.send_notification(NOTIFICATION_SIDEBAR_ID, notification_data)

def enforce_schedule(deployment_id: int) -> bool:
    """Enforce schedule by blocking deployments outside allowed hours and logging violations."""
    if not is_allowed_time():
        timestamp = datetime.now(timezone('EST'))
        log_violation(deployment_id, timestamp)
        send_notification(deployment_id, timestamp)
        return False
    return True
from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import connect, Row
from contextlib import closing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_allowed_time() -> bool:
    """Check if the current time is within the allowed deployment hours (10 PM - 8 AM EST)."""
    est_tz = timezone(-5 * 3600)  # EST is UTC-5
    now = datetime.now(est_tz)
    return 22 <= now.hour < 8

def log_violation(deployment_id: int, user_email: str, violation_time: datetime) -> None:
    """Log a deployment violation to a file."""
    log_path = os.path.join(current_app.root_path, 'logs', 'violation_logs.txt')
    with open(log_path, 'a') as log_file:
        log_file.write(f"Deployment violation: {deployment_id} by {user_email} at {violation_time}\n")

def notify_user(user_email: str, violation_time: datetime) -> None:
    """Notify the user via the Genkit Explorer sidebar."""
    # Assuming Genkit Explorer has a method to send notifications
    current_app.genkit_explorer.notify_user(user_email, f"Deployment attempt at {violation_time} is blocked.")

def enforce_schedule(deployment_id: int, user_email: str) -> None:
    """Enforce schedule for deployment attempts."""
    if not is_allowed_time():
        violation_time = datetime.now(timezone.utc)
        log_violation(deployment_id, user_email, violation_time)
        notify_user(user_email, violation_time)

def get_violation_logs() -> list[str]:
    """Retrieve violation logs from the file."""
    log_path = os.path.join(current_app.root_path, 'logs', 'violation_logs.txt')
    with open(log_path, 'r') as log_file:
        return log_file.readlines()

def get_violations_since(start_time: datetime) -> list[str]:
    """Retrieve violation logs since a given time."""
    logs = get_violation_logs()
    return [line for line in logs if start_time <= datetime.fromisoformat(line.split()[4][:-1])]

def get_violation_count_since(start_time: datetime) -> int:
    """Count the number of violations since a given time."""
    return len(get_violations_since(start_time))

def setup_db() -> None:
    """Set up the SQLite database with the necessary schema."""
    db_path = os.path.join(current_app.root_path, 'db', 'schedule_enforcement.db')
    with closing(connect(db_path, uri=True, check_same_thread=False)) as conn:
        conn.row_factory = Row
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS violations (
                    id INTEGER PRIMARY KEY,
                    deployment_id INTEGER,
                    user_email TEXT,
                    violation_time TEXT
                )
            """)

async def log_violation_async(deployment_id: int, user_email: str, violation_time: datetime) -> None:
    """Log a deployment violation asynchronously."""
    await current_app.async_db.execute(
        "INSERT INTO violations (deployment_id, user_email, violation_time) VALUES (?, ?, ?)",
        (deployment_id, user_email, violation_time.isoformat())
    )
    await current_app.async_db.commit()

async def notify_user_async(user_email: str, violation_time: datetime) -> None:
    """Notify the user asynchronously."""
    await current_app.async_db.execute(
        "INSERT INTO notifications (user_email, notification_time) VALUES (?, ?)",
        (user_email, violation_time.isoformat())
    )
    await current_app.async_db.commit()

async def enforce_schedule_async(deployment_id: int, user_email: str) -> None:
    """Enforce schedule for deployment attempts asynchronously."""
    if not is_allowed_time():
        violation_time = datetime.now(timezone.utc)
        await log_violation_async(deployment_id, user_email, violation_time)
        await notify_user_async(user_email, violation_time)
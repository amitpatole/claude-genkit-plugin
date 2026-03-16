from typing import Any
import logging
from datetime import datetime
from flask import current_app
from sqlite3 import Row
import os

from .db import get_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_allowed_time() -> bool:
    """
    Check if the current time is within allowed deployment hours (10 PM - 8 AM EST).
    """
    now = datetime.now()
    allowed_start = datetime(now.year, now.month, now.day, 22)
    allowed_end = datetime(now.year, now.month, now.day, 8)
    
    if now >= allowed_start and now < allowed_end:
        return False
    return True

async def enforce_schedule() -> None:
    """
    Enforce schedule by checking if the current time is outside allowed deployment hours.
    If not, log a violation and notify via Genkit Explorer sidebar.
    """
    if not is_allowed_time():
        logger.error("Deployment attempt detected outside allowed hours.")
        await log_violation()
        await notify_user_of_violation()

async def log_violation() -> None:
    """
    Log a violation to a file.
    """
    violation_message = "Deployment attempt detected outside allowed hours."
    with open(os.path.join(current_app.root_path, 'logs', 'violation_log.txt'), 'a') as log_file:
        log_file.write(f"{datetime.now()}: {violation_message}\n")

async def notify_user_of_violation() -> None:
    """
    Notify the user via the Genkit Explorer sidebar.
    """
    violation_message = "Deployment attempt detected outside allowed hours."
    await current_app.notify_user(violation_message)

async def get_db_connection() -> Row:
    """
    Get a database connection with row factory enabled.
    """
    conn = await current_app.get_db_connection()
    conn.row_factory = Row
    return conn

# Example usage within a route or scheduled task
# async def some_route_or_task():
#     await enforce_schedule()
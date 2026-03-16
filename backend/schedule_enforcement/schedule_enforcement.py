from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager
from .config import ALLOWED_DEPLOYMENT_HOURS, DEPLOYMENT_VIOLATION_LOG_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_db_connection() -> Row:
    conn = current_app.extensions['sqlite'].get_db()
    conn.row_factory = Row
    yield conn

async def is_within_allowed_hours() -> bool:
    now = datetime.now(timezone('EST'))
    return ALLOWED_DEPLOYMENT_HOURS[0] <= now.hour < ALLOWED_DEPLOYMENT_HOURS[1]

async def log_deployment_violation(user_id: str, deployment_time: datetime) -> None:
    with open(DEPLOYMENT_VIOLATION_LOG_PATH, 'a') as log_file:
        log_file.write(f"Deployment violation detected at {deployment_time}. User ID: {user_id}\n")

async def notify_user_via_genkit_explorer(user_id: str, deployment_time: datetime) -> None:
    # Simulate notification via Genkit Explorer sidebar
    logger.info(f"Deployment attempt at {deployment_time} blocked for user {user_id}. Notifying via Genkit Explorer sidebar.")

async def enforce_schedule(user_id: str) -> None:
    try:
        if not await is_within_allowed_hours():
            logger.warning("Deployment attempt detected outside allowed hours.")
            await log_deployment_violation(user_id, datetime.now(timezone('EST')))
            await notify_user_via_genkit_explorer(user_id, datetime.now(timezone('EST')))
        else:
            logger.info("Deployment attempt within allowed hours.")
    except Exception as e:
        logger.error(f"Error enforcing schedule: {e}")
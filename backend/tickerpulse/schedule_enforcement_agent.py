from typing import Any, Optional
import sqlite3
from datetime import datetime
from flask import current_app

from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

def get_current_hour() -> int:
    return datetime.now().hour

def is_non_dev_hour(hour: int) -> bool:
    return 20 <= hour < 8

def enforce_schedule(hour: int) -> bool:
    return not is_non_dev_hour(hour)

def log_schedule_enforcement(action: str) -> None:
    logging.info(f"Schedule Enforcement: {action}")

async def enforce_schedule_async(hour: int) -> bool:
    return await enforce_schedule(hour)

async def check_and_log_schedule_enforcement() -> None:
    current_hour = get_current_hour()
    should_enforce = enforce_schedule(current_hour)
    log_schedule_enforcement(f"Enforced: {should_enforce}")

    # Assuming this is an async function and we need to log the enforcement
    # even if it's not enforced
    if not should_enforce:
        log_schedule_enforcement("Not enforced during non-dev hours")

# Example usage in an async context
async def main() -> None:
    async with get_db_connection() as conn:
        await check_and_log_schedule_enforcement()

# This function is used to resolve the merge conflict and ensure the code is syntactically valid
def resolve_merge_conflict() -> None:
    pass
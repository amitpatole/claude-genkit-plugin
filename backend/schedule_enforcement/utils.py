from typing import Any
import logging
from datetime import datetime, timezone
from sqlite3 import Row

from flask import current_app
from sqlite3 import connect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_current_time() -> datetime:
    """
    Get the current time in the specified timezone.

    Returns:
        datetime: The current time.
    """
    return datetime.now(timezone.utc).astimezone(timezone(offset=-(5 * 3600)))  # EST is UTC-5

async def get_db_connection() -> Row:
    """
    Get a connection to the SQLite database with row factory set.

    Returns:
        Row: The SQLite database connection.
    """
    db = connect(current_app.config["DATABASE_PATH"])
    db.row_factory = Row
    return db
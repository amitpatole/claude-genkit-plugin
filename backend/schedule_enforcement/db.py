from typing import Any
import sqlite3
from contextlib import asynccontextmanager
from sqlite3 import Row

from . import init_db

@asynccontextmanager
async def get_db() -> Row:
    """Context manager for database access."""
    db = await init_db()
    try:
        yield db
    finally:
        db.close()

async def init_db() -> sqlite3.Connection:
    """Initialize the database connection."""
    db = sqlite3.connect(
        os.path.join(current_app.root_path, "tickerpulse.db"),
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS deployment_attempts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            time TIMESTAMP NOT NULL,
            success BOOLEAN NOT NULL
        )
        """
    )
    return db
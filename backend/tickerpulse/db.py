from typing import Any
import sqlite3
from contextlib import asynccontextmanager

def get_db() -> sqlite3.Row:
    """Get a database connection with row factory set to Row."""
    conn = sqlite3.connect('tickerpulse.db', isolation_level=None, uri=True)
    conn.row_factory = sqlite3.Row
    return conn

@asynccontextmanager
async def get_async_db() -> sqlite3.Row:
    """Async context manager for database connection."""
    db = await get_db()
    try:
        yield db
    finally:
        db.close()
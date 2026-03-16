from typing import Any
import sqlite3
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_connection() -> sqlite3.Row:
    """Context manager to get a database connection."""
    conn = sqlite3.connect('tickerpulse.db', uri=True)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
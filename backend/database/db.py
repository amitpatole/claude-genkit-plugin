from typing import Any
import sqlite3
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_connection() -> Any:
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect("tickerpulse.db", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
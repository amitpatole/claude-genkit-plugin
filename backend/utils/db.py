from typing import Any
import sqlite3
from contextlib import asynccontextmanager

from backend.config import DB_PATH

@asynccontextmanager
async def get_db_connection() -> sqlite3.Connection:
    """
    Context manager for database connections.
    """
    conn = sqlite3.connect(DB_PATH, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
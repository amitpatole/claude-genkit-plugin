from typing import Any, AsyncIterable, Optional
import sqlite3
from sqlite3 import Row
from contextlib import asynccontextmanager

from flask import current_app

@asynccontextmanager
async def get_db_connection() -> AsyncIterable[Row]:
    """
    Context manager for database connections.

    :yield: A Row object representing a database row.
    """
    conn = await sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
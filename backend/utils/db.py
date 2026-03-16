from typing import Any
import sqlite3
from contextlib import asynccontextmanager

from flask import current_app

@asynccontextmanager
async def get_db_connection() -> sqlite3.Connection:
    """
    Provides a connection to the SQLite database using async context manager.
    """
    conn = sqlite3.connect(current_app.config["DATABASE_PATH"], uri=True)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
from typing import Any
import sqlite3
from contextlib import asynccontextmanager

from . import get_db

@asynccontextmanager
async def get_async_db() -> sqlite3.Row:
    conn = await get_db()
    try:
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        conn.close()

async def get_db() -> sqlite3.Connection:
    # Assume this function is already implemented and returns a connection to the SQLite database.
    pass
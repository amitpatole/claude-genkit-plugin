from typing import Any
import sqlite3
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect("path/to/database.db", uri=True)
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
    finally:
        conn.close()
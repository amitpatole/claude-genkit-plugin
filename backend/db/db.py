from typing import Any, List, Optional
from sqlite3 import Row, connect, Cursor
from contextlib import asynccontextmanager
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'tickerpulse.db')

@asynccontextmanager
async def get_db() -> Cursor:
    conn = connect(DB_PATH, isolation_level=None, journal_mode='wal')
    cursor: Cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def get_row_factory() -> Any:
    """Return a row factory for SQLite."""
    return Row
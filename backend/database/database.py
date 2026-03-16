from typing import Any, Dict, List, Optional
import sqlite3
from contextlib import asynccontextmanager
from sqlite3 import Row

from .config import DB_PATH

@asynccontextmanager
async def get_db() -> Row:
    """Async context manager for database connection."""
    conn = sqlite3.connect(DB_PATH, uri=True, detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def row_to_dict(row: Row) -> Dict[str, Any]:
    """Convert SQLite row to dictionary."""
    return {key: row[key] for key in row.keys()}
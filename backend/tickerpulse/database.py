from typing import Any, Dict, List
import sqlite3
from contextlib import asynccontextmanager

from flask import current_app

DB_PATH = 'tickerpulse.db'

@asynccontextmanager
async def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, uri=True, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
    finally:
        conn.close()
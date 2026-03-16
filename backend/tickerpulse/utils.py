from typing import Any
import sqlite3
import asyncio

from contextlib import asynccontextmanager

async def get_db_connection() -> sqlite3.Row:
    conn = await sqlite3.connect('tickerpulse.db', uri=True, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
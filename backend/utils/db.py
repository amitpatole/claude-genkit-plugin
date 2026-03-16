from typing import Any, AsyncContextManager, AsyncGenerator
import sqlite3
from sqlite3 import Row
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[sqlite3.Connection, None]:
    conn = sqlite3.connect('tickerpulse.db', uri=True, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
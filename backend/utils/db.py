from typing import Any, AsyncContextManager, AsyncGenerator, Optional
import sqlite3
from contextlib import asynccontextmanager

from backend.config import DB_PATH

@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[sqlite3.Connection, None]:
    conn = await sqlite3.connect(DB_PATH, isolation_level=None, check_same_thread=False)
    try:
        yield conn
    finally:
        await conn.close()
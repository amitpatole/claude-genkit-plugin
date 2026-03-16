from typing import Any, AsyncContextManager, AsyncGenerator, Optional
import sqlite3
from sqlite3 import Row

from contextlib import asynccontextmanager

def get_db_connection() -> AsyncContextManager[sqlite3.Connection]:
    @asynccontextmanager
    async def _get_db_connection() -> AsyncGenerator[sqlite3.Connection, None]:
        conn = sqlite3.connect("tickerpulse.db", uri=True, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.row_factory = Row
        try:
            yield conn
        finally:
            conn.close()

    return _get_db_connection()
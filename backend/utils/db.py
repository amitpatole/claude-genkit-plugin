from typing import Any, AsyncContextManager, AsyncIterator
import sqlite3
from contextlib import asynccontextmanager

def get_db_connection() -> AsyncContextManager[sqlite3.Connection]:
    @asynccontextmanager
    async def connect() -> AsyncIterator[sqlite3.Connection]:
        conn = sqlite3.connect("path/to/database.db", uri=True, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    return connect
from typing import Any, AsyncContextManager, AsyncGenerator
from sqlite3 import Row, connect, Connection
from contextlib import asynccontextmanager

from .config import get_db_config

@asynccontextmanager
async def get_db() -> AsyncContextManager[Connection]:
    config = get_db_config()
    conn = connect(config["db_path"], isolation_level=None, journal_mode="wal")
    conn.row_factory = Row
    try:
        yield conn
    finally:
        conn.close()
from typing import Any, AsyncContextManager
import sqlite3
from contextlib import asynccontextmanager
from flask import current_app

@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[sqlite3.Connection, None]:
    conn = sqlite3.connect(current_app.config['DATABASE'], uri=True, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
from typing import Any
import sqlite3
from contextlib import asynccontextmanager
from sqlite3 import Row

@asynccontextmanager
async def get_db_connection() -> Row:
    conn = await sqlite3.connect(current_app.config['DATABASE'], uri=True, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        await conn.close()
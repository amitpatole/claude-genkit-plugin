from typing import Any
from sqlite3 import Row
from contextlib import asynccontextmanager
from backend.utils.config import get_config

@asynccontextmanager
async def get_db_connection() -> Row:
    db_config = get_config().get("db", {})
    conn = await create_connection(db_config.get("path", "tickerpulse.db"))
    try:
        yield conn
    finally:
        await conn.close()

async def create_connection(db_path: str) -> Row:
    conn = await aiosqlite.connect(db_path)
    return conn
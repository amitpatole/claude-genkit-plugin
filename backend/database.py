from typing import Any, AsyncContextManager, AsyncIterator
import sqlite3
from contextlib import asynccontextmanager

DATABASE_PATH = 'path/to/database.db'

async def get_db_connection() -> AsyncContextManager[sqlite3.Connection]:
    conn = await sqlite3.connect(DATABASE_PATH, isolation_level=None, check_same_thread=False, uri=True)
    conn.execute('PRAGMA journal_mode=WAL')
    return conn

@asynccontextmanager
async def get_db() -> AsyncIterator[sqlite3.Row]:
    conn = await get_db_connection()
    try:
        yield conn
    finally:
        await conn.close()

async def execute_query(query: str, params: tuple) -> AsyncIterator[sqlite3.Row]:
    async with get_db() as db:
        cursor = await db.execute(query, params)
        async for row in cursor:
            yield row
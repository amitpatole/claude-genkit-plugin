from typing import Any
import sqlite3
from sqlite3 import Row
from contextlib import asynccontextmanager

from flask import current_app

async def get_db_connection() -> sqlite3.Connection:
    if current_app.config.get("TESTING"):
        return sqlite3.connect(":memory:")
    return sqlite3.connect(current_app.config["DATABASE"], uri=True, isolation_level=None, check_same_thread=False, factory=Row)

@asynccontextmanager
async def get_db_cursor() -> sqlite3.Cursor:
    conn = await get_db_connection()
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        await conn.close()
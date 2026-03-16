from typing import Any
import sqlite3
from contextlib import asynccontextmanager
from flask import current_app

@asynccontextmanager
async def get_db_connection() -> sqlite3.Connection:
    """
    Get a database connection with WAL mode enabled.
    """
    db_path = os.path.join(current_app.root_path, 'data', 'tickerpulse.db')
    conn = sqlite3.connect(db_path, uri=True, isolation_level=None, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
    finally:
        conn.close()

# Example usage
# async def some_function():
#     async with get_db_connection() as conn:
#         # Perform database operations
#         pass
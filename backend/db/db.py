from typing import Any
import sqlite3
from contextlib import asynccontextmanager
from datetime import timezone

@asynccontextmanager
async def get_db_connection() -> sqlite3.Connection:
    """
    Context manager for getting a database connection.
    
    :return: Database connection
    """
    conn = sqlite3.connect("tickerpulse.db", isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

# Example usage
# async with get_db_connection() as conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM table")
#     results = cursor.fetchall()
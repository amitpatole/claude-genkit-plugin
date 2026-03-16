from typing import Any
import sqlite3
from contextlib import asynccontextmanager

# Define the database connection function
async def get_db_connection() -> sqlite3.Connection:
    """Get a database connection with row factory and WAL mode."""
    conn = sqlite3.connect("tickerpulse.db", isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

# Example usage
async def example_usage() -> None:
    conn = await get_db_connection()
    cursor = conn.execute("SELECT * FROM some_table")
    rows = cursor.fetchall()
    print(rows)

# Main entry point for testing
if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
from typing import Any, Dict
import sqlite3
from sqlite3 import Error

def get_db_connection() -> sqlite3.Connection:
    """Get a database connection with WAL mode."""
    conn = sqlite3.connect('tickerpulse.db', uri=True)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn
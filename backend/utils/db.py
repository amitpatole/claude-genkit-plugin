from typing import Any
import sqlite3

def get_db_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    return sqlite3.connect(current_app.config["DATABASE_PATH"], isolation_level=None, check_same_thread=False)
from typing import Any, Dict, List, Optional
import sqlite3
from sqlite3 import Row

def get_db() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect("tickerpulse.db", isolation_level=None, factory=Row)
    conn.row_factory = Row
    return conn

def init_db() -> None:
    """Initialize the database with necessary tables."""
    with current_app.app_context():
        db = get_db()
        with current_app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def row_to_dict(row: Row) -> Dict[str, Any]:
    """Convert a SQLite3 Row object to a dictionary."""
    return dict(row)
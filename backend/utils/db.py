from typing import Any
import sqlite3
from sqlite3 import Row

from flask import current_app

def get_db_connection() -> sqlite3.Connection:
    """
    Get a database connection using SQLite3.
    
    :return: SQLite3 database connection.
    """
    conn = sqlite3.connect(current_app.config['DATABASE_PATH'], uri=True, check_same_thread=False)
    conn.row_factory = Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def close_db_connection(conn: sqlite3.Connection):
    """
    Close the database connection.
    
    :param conn: SQLite3 database connection.
    """
    conn.close()
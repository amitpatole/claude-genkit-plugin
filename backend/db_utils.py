from typing import Any, Dict, List
import sqlite3
from sqlite3 import Error

def get_db_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect('tickerpulse.db', uri=True)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None

def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Executes a parameterized SQL query and returns the results as a list of dictionaries."""
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.commit()
        return [dict(row) for row in rows]
    except Error as e:
        logging.error(f"Error executing query: {e}")
        return []

def execute_non_query(query: str, params: tuple = ()) -> int:
    """Executes a parameterized SQL non-query (e.g., INSERT, UPDATE, DELETE) and returns the number of affected rows."""
    conn = get_db_connection()
    if conn is None:
        return 0

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except Error as e:
        logging.error(f"Error executing non-query: {e}")
        return 0
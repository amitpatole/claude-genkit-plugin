from typing import Any, Optional
import sqlite3
from sqlite3 import Row

def get_db_connection() -> sqlite3.Connection:
    """
    Get a database connection with WAL mode enabled.

    :return: A database connection object.
    :rtype: sqlite3.Connection
    """
    conn = sqlite3.connect("tickerpulse.db", uri=True)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def execute_query(query: str, params: Optional[tuple] = None) -> Optional[Row]:
    """
    Execute a query with parameterized placeholders.

    :param query: The SQL query string.
    :type query: str
    :param params: Parameters to be used in the query.
    :type params: Optional[tuple]
    :return: The result row or None if no results.
    :rtype: Optional[Row]
    """
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor(row_factory=sqlite3.Row)
            cursor.execute(query, params)
            return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Failed to execute query: {e}")
        return None
    finally:
        conn.close()
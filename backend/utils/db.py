from typing import Any, Dict, Optional
import sqlite3

from config import SCHEDULE_ENFORCEMENT_CONFIG

def get_db_connection() -> sqlite3.Connection:
    """
    Get a connection to the SQLite database.

    :return: SQLite database connection.
    """
    conn = sqlite3.connect(SCHEDULE_ENFORCEMENT_CONFIG['db_path'], uri=True, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """
    Execute a parameterized SQLite query.

    :param query: SQL query with placeholders.
    :param params: Parameters to be used in the query.
    :return: Result of the query execution.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()
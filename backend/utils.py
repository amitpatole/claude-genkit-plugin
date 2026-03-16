from typing import Any

def get_db_connection() -> sqlite3.Connection:
    """
    Get a database connection using the SQLite database configured in the app.
    """
    conn = sqlite3.connect(current_app.config['DATABASE_PATH'], uri=True)
    conn.row_factory = sqlite3.Row
    return conn
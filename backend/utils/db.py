from typing import Any
import sqlite3

from flask import current_app

def get_db_connection() -> sqlite3.Connection:
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn
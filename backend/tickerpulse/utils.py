from typing import Any
import logging
import sqlite3

from flask import current_app

logger = logging.getLogger(__name__)

async def get_db_path() -> str:
    """Get the database path from the environment."""
    return current_app.config["DATABASE_PATH"]

# Ensure the following is called when the script is run directly
if __name__ == "__main__":
    pass
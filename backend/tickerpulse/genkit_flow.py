from typing import Any, AsyncContextManager, AsyncGenerator, Optional
import sqlite3
from contextlib import asynccontextmanager
from logging import getLogger
from os import environ

logger = getLogger(__name__)

DATABASE_PATH = environ.get("GENKIT_DB_PATH", "genkit.db")

@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[sqlite3.Connection, None]:
    conn = sqlite3.connect(DATABASE_PATH, isolation_level=None, check_same_thread=False, factory=sqlite3.Row)
    try:
        yield conn
    finally:
        conn.close()

async def generate_flow_template(template_id: int) -> Optional[str]:
    async with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT template_content FROM flow_templates WHERE id = ?"
        cursor.execute(query, (template_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            logger.warning(f"Template with ID {template_id} not found.")
            return None
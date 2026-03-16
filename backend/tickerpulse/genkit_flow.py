from typing import Any, AsyncContextManager, AsyncGenerator, Optional
import sqlite3
from sqlite3 import Row
from flask import current_app

from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

class GenkitFlowGenerator:
    def __init__(self, db_connection: sqlite3.Connection):
        self.db_connection = db_connection

    async def generate_flow(self, template_id: int) -> Optional[str]:
        try:
            query = """
                SELECT template_content
                FROM genkit_templates
                WHERE id = ?
            """
            cursor: AsyncContextManager[sqlite3.Cursor] = self.db_connection.execute(query, (template_id,))
            row: Row = await cursor.fetchone()
            if row:
                return row["template_content"]
            else:
                return None
        except sqlite3.Error as e:
            logging.error(f"Error generating genkit flow: {e}")
            return None

    async def __aenter__(self) -> 'GenkitFlowGenerator':
        self.db_connection = await get_db_connection()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db_connection.close()
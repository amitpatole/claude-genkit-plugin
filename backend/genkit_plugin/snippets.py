from typing import Any, Dict, List, Optional
import logging
from sqlite3 import Row
from flask import current_app

from . import db  # Assuming db is a module that provides database access

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class Snippet:
    def __init__(self, context: Dict[str, Any]):
        self.context = context

    async def fetch_snippets(self) -> List[str]:
        """
        Fetch AI-driven code snippets based on the project context.
        :param context: A dictionary containing the project context.
        :return: A list of code snippets.
        """
        try:
            async with db.get_db().acquire() as conn:
                cursor = await conn.execute(
                    "SELECT snippet FROM snippets WHERE context LIKE ?", (self.context,)
                )
                snippets = await cursor.fetchall()
                return [snippet[0] for snippet in snippets]
        except Exception as e:
            logger.error(f"Failed to fetch snippets: {e}")
            return []

    async def apply_snippet(self, snippet: str) -> None:
        """
        Apply a code snippet to the project.
        :param snippet: The code snippet to apply.
        """
        try:
            async with db.get_db().acquire() as conn:
                cursor = await conn.execute(
                    "INSERT INTO applied_snippets (snippet, context) VALUES (?, ?)",
                    (snippet, self.context)
                )
                await conn.commit()
        except Exception as e:
            logger.error(f"Failed to apply snippet: {e}")

async def get_snippets_for_project(context: Dict[str, Any]) -> List[str]:
    """
    Get AI-driven code snippets for a specific project.
    :param context: A dictionary containing the project context.
    :return: A list of code snippets.
    """
    snippet_service = Snippet(context)
    return await snippet_service.fetch_snippets()
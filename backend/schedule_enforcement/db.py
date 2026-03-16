from typing import Any
from sqlite3 import connect, Row
from contextlib import closing

class AsyncDB:
    """Async SQLite database context manager."""
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def __aenter__(self) -> 'AsyncDB':
        self.conn = connect(self.db_path, uri=True, check_same_thread=False)
        self.conn.row_factory = Row
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.conn.close()

    async def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a query with parameterized placeholders."""
        with closing(self.conn.cursor()) as cursor:
            await cursor.execute(query, params)

    async def commit(self) -> None:
        """Commit the transaction."""
        self.conn.commit()
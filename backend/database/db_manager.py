from typing import Any
from sqlite3 import Row, connect
from contextlib import asynccontextmanager

class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def connect(self) -> None:
        self.connection = connect(self.db_path, isolation_level=None, journal_mode='WAL')

    async def disconnect(self) -> None:
        self.connection.close()

    @asynccontextmanager
    async def session(self):
        try:
            yield self.connection
        finally:
            self.connection.close()

    def execute(self, query: str, params: tuple) -> None:
        with self.session() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def fetchall(self, query: str, params: tuple) -> list[Row]:
        with self.session() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
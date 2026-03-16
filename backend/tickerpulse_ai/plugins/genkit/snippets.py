from typing import Any, AsyncContextManager, AsyncGenerator, Optional
import sqlite3
from flask import current_app
from contextlib import asynccontextmanager

# Ensure the database is set up with WAL mode
def init_db() -> None:
    db = current_app.config['DATABASE']
    with sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        conn.execute('PRAGMA journal_mode=WAL;')
        conn.execute('CREATE TABLE IF NOT EXISTS code_snippets (id INTEGER PRIMARY KEY, project_context TEXT, snippet TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);')

# Parameterized query for SQLite
def execute_query(query: str, params: tuple) -> sqlite3.Cursor:
    db = current_app.config['DATABASE']
    with sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor

# Asynchronous context manager for database operations
@asynccontextmanager
async def get_db() -> AsyncGenerator[sqlite3.Connection, None]:
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    yield conn
    conn.close()

# Fetch AI-driven code snippets based on project context
async def fetch_snippets(project_context: str) -> list[dict[str, Any]]:
    async with get_db() as conn:
        cursor = await execute_query('SELECT snippet FROM code_snippets WHERE project_context = ?', (project_context,))
        rows = await cursor.fetchall()
        return [{'snippet': row.snippet} for row in rows]

# Add a new code snippet to the database
async def add_snippet(project_context: str, snippet: str) -> None:
    async with get_db() as conn:
        await execute_query('INSERT INTO code_snippets (project_context, snippet) VALUES (?, ?)', (project_context, snippet))

# Example usage
async def main() -> None:
    await init_db()
    snippets = await fetch_snippets('example_project')
    for snippet in snippets:
        print(snippet['snippet'])

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
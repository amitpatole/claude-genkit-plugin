from typing import Any, AsyncIterable, AsyncIterator, Optional
import sqlite3
from sqlite3 import Row
from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

genkit_flow_bp = Blueprint('genkit_flow', __name__)

class GenkitFlow:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    async def __aenter__(self):
        self.conn = sqlite3.connect(self.db_path, isolation_level=None, check_same_thread=False, factory=Row)
        self.conn.execute('PRAGMA journal_mode=WAL')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    async def execute_query(self, query: str, *args) -> AsyncIterable[Row]:
        async with self.conn.execute(query, args) as cursor:
            async for row in cursor:
                yield row

    async def get_flow_template(self, template_id: int) -> Optional[Row]:
        query = "SELECT * FROM flow_templates WHERE id=?"
        async for row in self.execute_query(query, template_id):
            return row

    async def run_flow_template(self, template_id: int) -> AsyncIterable[Row]:
        template = await self.get_flow_template(template_id)
        if not template:
            logger.error(f"Flow template with ID {template_id} not found.")
            return

        query = template['query']
        async for row in self.execute_query(query, *template['args']):
            yield row

    async def create_flow_template(self, name: str, query: str, args: tuple) -> int:
        query = "INSERT INTO flow_templates (name, query, args) VALUES (?, ?, ?) RETURNING id"
        async with self.conn.execute(query, (name, query, args)) as cursor:
            return cursor.fetchone()[0]

genkit_flow_bp.route('/genkit-flow/<int:template_id>', methods=['GET'])(async def get_flow_template_route(template_id: int) -> AsyncIterable[Row]:
    async with GenkitFlow('tickerpulse.db') as genkit_flow:
        return await genkit_flow.run_flow_template(template_id)

genkit_flow_bp.route('/genkit-flow', methods=['POST'])(async def create_flow_template_route() -> int:
    data = request.json
    name = data.get('name')
    query = data.get('query')
    args = tuple(data.get('args', ()))

    if not name or not query:
        return jsonify({"error": "Missing required fields"}), 400

    async with GenkitFlow('tickerpulse.db') as genkit_flow:
        return jsonify({"template_id": await genkit_flow.create_flow_template(name, query, args)})
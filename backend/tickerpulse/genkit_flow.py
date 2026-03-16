from typing import Any, AsyncIterable, AsyncIterator, Optional
import logging
from flask import Blueprint, request
from sqlite3 import Row
from contextlib import asynccontextmanager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the blueprint
genkit_flow = Blueprint('genkit_flow', __name__)

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the model
class FlowTemplate(db.Model):
    __tablename__ = 'flow_templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    template = db.Column(db.Text, nullable=False)

    @staticmethod
    async def get_all_templates() -> AsyncIterable[Row]:
        async with db.session_async() as session:
            async with session.begin():
                query = session.execute("SELECT * FROM flow_templates")
                for row in query.fetchall():
                    yield Row(row)

# Define the async context manager for database session
@asynccontextmanager
async def db_session_async():
    async with AsyncSession(db.engine) as session:
        yield session

# Define the route for generating flows
@genkit_flow.route('/genkit-flow', methods=['POST'])
async def generate_flow() -> Any:
    try:
        # Get the template ID from the request
        template_id = request.json.get('template_id')
        if not template_id:
            return {"error": "Template ID is required"}, 400

        # Fetch the template from the database
        async with db_session_async() as session:
            query = session.execute(
                "SELECT template FROM flow_templates WHERE id = ?", (template_id,)
            ).scalar()
            if not query:
                return {"error": "Template not found"}, 404

            # Generate the flow based on the template
            flow_template = query
            # Here you would implement the logic to generate the flow based on the template
            # For now, we just return the template as a sample response
            return {"flow": flow_template}, 200
    except Exception as e:
        logger.error(f"Error generating flow: {e}")
        return {"error": str(e)}, 500

# Define the route for streaming responses
@genkit_flow.route('/genkit-flow/stream', methods=['POST'])
async def stream_flow() -> AsyncIterable[bytes]:
    try:
        # Get the template ID from the request
        template_id = request.json.get('template_id')
        if not template_id:
            yield b'{"error": "Template ID is required"}\n'
            return

        # Fetch the template from the database
        async with db_session_async() as session:
            query = session.execute(
                "SELECT template FROM flow_templates WHERE id = ?", (template_id,)
            ).scalar()
            if not query:
                yield b'{"error": "Template not found"}\n'
                return

            # Generate the flow based on the template and stream the response
            flow_template = query
            # Here you would implement the logic to generate and stream the flow
            # For now, we just yield the template as a sample response
            yield f'{{"flow": "{flow_template}"}}\n'.encode()
    except Exception as e:
        logger.error(f"Error streaming flow: {e}")
        yield f'{{"error": "{str(e)}"}\n'.encode()

# Ensure SQLite uses WAL mode
db.engine.execute('PRAGMA journal_mode=WAL')

# Initialize the database
db.init_app(genkit_flow)
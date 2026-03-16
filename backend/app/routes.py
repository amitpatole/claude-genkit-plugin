from typing import Any, Dict, List
import logging
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import Row
from datetime import datetime

from .models import FlowTemplate, FlowStep
from .db import get_db_session

logger = logging.getLogger(__name__)

blueprint = Blueprint('genkit_flow', __name__)

@blueprint.route('/genkit-flow', methods=['POST'])
async def genkit_flow() -> Dict[str, Any]:
    """
    Generate a genkit flow based on the provided template.

    Args:
        request (Request): The Flask request object containing the template ID and parameters.

    Returns:
        Dict[str, Any]: A dictionary containing the generated flow steps.
    """
    try:
        template_id = request.json.get('template_id')
        parameters = request.json.get('parameters', {})

        if not template_id:
            return jsonify({"error": "Template ID is required"}), 400

        async with get_db_session() as session:
            flow_template = await session.get(FlowTemplate, template_id)
            if not flow_template:
                return jsonify({"error": "Template not found"}), 404

            steps = await session.execute(
                FlowStep.query.filter_by(template_id=template_id).order_by(FlowStep.order).with_row_labels().cte().select(),
                parameters
            )
            steps = [step._asdict() for step in steps]

            return jsonify({"steps": steps}), 200

    except Exception as e:
        logger.error(f"Error generating genkit flow: {e}")
        return jsonify({"error": str(e)}), 500

--- FILE: backend/app/models.py ---
from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Row
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import text

Base = declarative_base()

class FlowTemplate(Base):
    """
    A model representing a genkit flow template.

    Args:
        id (int): The unique identifier for the template.
        name (str): The name of the template.
        description (str): A brief description of the template.
        steps (List[FlowStep]): The steps in the template.

    Returns:
        None
    """
    __tablename__ = 'flow_templates'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    steps = relationship("FlowStep", back_populates="template")

class FlowStep(Base):
    """
    A model representing a step in a genkit flow template.

    Args:
        id (int): The unique identifier for the step.
        template_id (int): The ID of the template this step belongs to.
        order (int): The order of the step in the template.
        step_type (str): The type of the step (e.g., "input", "output", "action").
        parameters (Text): The parameters for the step.

    Returns:
        None
    """
    __tablename__ = 'flow_steps'

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('flow_templates.id'))
    order = Column(Integer)
    step_type = Column(String)
    parameters = Column(Text)
    template = relationship("FlowTemplate", back_populates="steps")

--- FILE: backend/db.py ---
from typing import Any, AsyncContextManager, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Row
from contextlib import asynccontextmanager

from .models import Base

DATABASE_URL = "sqlite+aiosqlite:///./genkit.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session.

    Args:
        None

    Yields:
        AsyncSession: A database session.

    Returns:
        None
    """
    try:
        session: AsyncSession = AsyncSessionLocal()
        yield session
    finally:
        await session.close()

# Enable row factory for SQLite
@event.listens_for(engine, "connect")
def set_row_factory(dbapi_con, _):
    """
    Set the row factory for SQLite.

    Args:
        dbapi_con (Any): The database connection.
        _ (Any): Placeholder for the second argument.

    Returns:
        None
    """
    cursor = dbapi_con.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA row_factory=ROW")
    cursor.close()

# Enable parameterized queries
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """
    Enable parameterized queries.

    Args:
        conn (Any): The database connection.
        cursor (Any): The cursor.
        statement (str): The SQL statement.
        parameters (Any): The parameters to be used in the statement.
        context (Any): The context.
        executemany (bool): Whether the statement is an executemany call.

    Returns:
        None
    """
    if parameters is not None:
        cursor.execute(statement, parameters)
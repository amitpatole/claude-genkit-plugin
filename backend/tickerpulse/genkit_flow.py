from typing import Any, AsyncIterable, AsyncIterator, Optional, TypeVar, cast
import logging
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from .models import FlowTemplate, FlowStep, StepType
from .config import get_config

logger = logging.getLogger(__name__)

genkit_flow_bp = Blueprint('genkit_flow', __name__)
db = SQLAlchemy()

T = TypeVar('T')

async def get_flow_template_by_id(template_id: int, session: AsyncSession) -> Optional[FlowTemplate]:
    result = await session.execute(select(FlowTemplate).where(FlowTemplate.id == template_id))
    return result.scalar_one_or_none()

async def create_flow_step(step_type: StepType, step_data: Any, session: AsyncSession) -> FlowStep:
    step = FlowStep(step_type=step_type, step_data=step_data, created_at=datetime.utcnow())
    session.add(step)
    await session.commit()
    await session.refresh(step)
    return step

async def run_flow_template(template_id: int, session: AsyncSession) -> AsyncIterable[FlowStep]:
    template = await get_flow_template_by_id(template_id, session)
    if not template:
        raise ValueError(f"Flow template with ID {template_id} not found")

    for step in template.steps:
        yield await create_flow_step(step.step_type, step.step_data, session)

@genkit_flow_bp.route('/genkit-flow', methods=['POST'])
async def genkit_flow() -> Any:
    template_id = request.json.get('template_id')
    if not template_id:
        return jsonify({"error": "Template ID is required"}), 400

    async with db.session() as session:
        async for step in run_flow_template(int(template_id), session):
            yield step
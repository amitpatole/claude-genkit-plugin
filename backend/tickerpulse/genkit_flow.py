from typing import Any, AsyncIterator, Dict, List, Optional, Tuple
import logging
from sqlite3 import Row
from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession

db = SQLAlchemy()
bp = Blueprint('genkit_flow', __name__)

class FlowTemplate(db.Model):
    __tablename__ = 'flow_templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    template = db.Column(db.JSON, nullable=False)

async def get_flow_template(template_name: str) -> Optional[Dict]:
    async with AsyncSession(db.engine) as session:
        flow_template = await session.get(FlowTemplate, template_name)
        return flow_template.template if flow_template else None

async def create_flow_template(template_name: str, template: Dict) -> None:
    async with AsyncSession(db.engine) as session:
        new_template = FlowTemplate(name=template_name, template=template)
        session.add(new_template)
        await session.commit()

async def update_flow_template(template_name: str, template: Dict) -> None:
    async with AsyncSession(db.engine) as session:
        flow_template = await session.get(FlowTemplate, template_name)
        if flow_template:
            flow_template.template = template
            await session.commit()

async def delete_flow_template(template_name: str) -> None:
    async with AsyncSession(db.engine) as session:
        flow_template = await session.get(FlowTemplate, template_name)
        if flow_template:
            session.delete(flow_template)
            await session.commit()

@bp.route('/genkit-flow', methods=['POST'])
async def create_or_update_flow_template() -> Tuple[Dict, int]:
    data = request.json
    template_name = data.get('name')
    template = data.get('template')

    if not template_name or not template:
        return {'error': 'Missing template name or template'}, 400

    existing_template = await get_flow_template(template_name)
    if existing_template:
        await update_flow_template(template_name, template)
        return {'message': f'Updated template: {template_name}'}, 200
    else:
        await create_flow_template(template_name, template)
        return {'message': f'Created new template: {template_name}'}, 201

@bp.route('/genkit-flow/<template_name>', methods=['DELETE'])
async def delete_flow_template_route(template_name: str) -> Tuple[Dict, int]:
    await delete_flow_template(template_name)
    return {'message': f'Deleted template: {template_name}'}, 200

@bp.route('/genkit-flow/<template_name>', methods=['GET'])
async def get_flow_template_route(template_name: str) -> Tuple[Dict, int]:
    template = await get_flow_template(template_name)
    if template:
        return {'template': template}, 200
    else:
        return {'error': f'Template not found: {template_name}'}, 404

@bp.route('/genkit-flow/stream', methods=['GET'])
async def stream_flow_templates() -> AsyncIterator[Dict]:
    async with AsyncSession(db.engine) as session:
        async with session.begin():
            flow_templates = await session.query(FlowTemplate).all()
            for template in flow_templates:
                yield {'name': template.name, 'template': template.template}

async def setup_flow_templates() -> None:
    # Example setup function to add initial templates
    await create_flow_template('simple_template', {'steps': ['step1', 'step2']})
    await create_flow_template('complex_template', {'steps': ['step1', 'step2', 'step3'], 'streaming': True})
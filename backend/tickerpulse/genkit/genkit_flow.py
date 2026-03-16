from typing import Any, AsyncIterable, Dict, List
import logging
from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query
from contextlib import asynccontextmanager
import sqlite3

db = SQLAlchemy()

bp = Blueprint('genkit_flow', __name__, url_prefix='/genkit-flow')

class GenkitFlow(db.Model):
    __tablename__ = 'genkit_flows'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template = db.Column(db.JSON, nullable=False)
    steps = db.relationship('GenkitStep', backref='flow', lazy=True)

class GenkitStep(db.Model):
    __tablename__ = 'genkit_steps'
    id = db.Column(db.Integer, primary_key=True)
    flow_id = db.Column(db.Integer, db.ForeignKey('genkit_flows.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    step_type = db.Column(db.String(50), nullable=False)
    parameters = db.Column(db.JSON, nullable=True)

@asynccontextmanager
async def get_db_connection() -> sqlite3.Connection:
    conn = db.session.connection().engine.raw_connection()
    try:
        yield conn
    finally:
        conn.close()

@bp.route('/create', methods=['POST'])
async def create_flow() -> Dict[str, Any]:
    data = request.json
    flow = GenkitFlow(name=data['name'], template=data['template'])
    db.session.add(flow)
    await db.session.flush()
    for step_data in data['template']:
        step = GenkitStep(flow_id=flow.id, step_number=step_data['step_number'], step_type=step_data['step_type'], parameters=step_data.get('parameters'))
        db.session.add(step)
    await db.session.commit()
    return {'id': flow.id}

@bp.route('/run/<flow_id>', methods=['GET'])
async def run_flow(flow_id: int) -> AsyncIterable[str]:
    flow = await db.session.get(GenkitFlow, flow_id)
    if not flow:
        return 'Flow not found', 404
    async with get_db_connection() as conn:
        for step in flow.steps:
            step_data = step.template
            if step.step_type == 'stream':
                async for line in step_data['stream']:
                    yield line
            else:
                result = await step_data['function']()
                yield result

@bp.route('/templates', methods=['GET'])
async def get_templates() -> List[Dict[str, Any]]:
    flows = await db.session.query(GenkitFlow).filter_by(template={'step_type': 'stream'}).all()
    return [{'id': flow.id, 'name': flow.name} for flow in flows]

if __name__ == '__main__':
    app.run()
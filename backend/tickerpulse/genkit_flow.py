from typing import Any, Dict, List, Optional
import sqlite3
from sqlite3 import Row
import logging
from flask import Blueprint, request, jsonify
from contextlib import asynccontextmanager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession

# Initialize Flask Blueprint and SQLAlchemy
bp = Blueprint('genkit_flow', __name__)
db = SQLAlchemy()

# Define the database model
class Flow(db.Model):
    __tablename__ = 'flows'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    template = db.Column(db.String, nullable=False)
    steps = db.Column(db.JSON, nullable=True)

# Define the row factory for SQLite
sqlite3.Row = Row

# Define the async context manager for database session
@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with db.sessionmaker(expire_on_commit=False, class_=AsyncSession) as session:
        yield session

# Define the function to create a new flow
async def create_flow(flow_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        async with get_async_session() as session:
            new_flow = Flow(**flow_data)
            session.add(new_flow)
            await session.commit()
            return new_flow.to_dict()
    except Exception as e:
        logging.error(f"Failed to create flow: {e}")
        return None

# Define the function to get all flows
async def get_all_flows() -> List[Dict[str, Any]]:
    try:
        async with get_async_session() as session:
            flows = await session.execute(db.select(Flow))
            return [flow._asdict() async for flow in flows]
    except Exception as e:
        logging.error(f"Failed to get flows: {e}")
        return []

# Define the function to get a specific flow by ID
async def get_flow_by_id(flow_id: int) -> Optional[Dict[str, Any]]:
    try:
        async with get_async_session() as session:
            flow = await session.get(Flow, flow_id)
            if flow:
                return flow.to_dict()
            return None
    except Exception as e:
        logging.error(f"Failed to get flow by ID: {e}")
        return None

# Define the route to create a new flow
@bp.route('/genkit-flow', methods=['POST'])
async def create_genkit_flow():
    flow_data = request.json
    if not flow_data:
        return jsonify({"error": "No flow data provided"}), 400
    new_flow = await create_flow(flow_data)
    if new_flow:
        return jsonify(new_flow), 201
    return jsonify({"error": "Failed to create flow"}), 500

# Define the route to get all flows
@bp.route('/genkit-flow', methods=['GET'])
async def get_genkit_flows():
    flows = await get_all_flows()
    return jsonify(flows), 200

# Define the route to get a specific flow by ID
@bp.route('/genkit-flow/<int:flow_id>', methods=['GET'])
async def get_genkit_flow(flow_id: int):
    flow = await get_flow_by_id(flow_id)
    if flow:
        return jsonify(flow), 200
    return jsonify({"error": "Flow not found"}), 404

# Define the function to update a flow
async def update_flow(flow_id: int, flow_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        async with get_async_session() as session:
            flow = await session.get(Flow, flow_id)
            if flow:
                for key, value in flow_data.items():
                    setattr(flow, key, value)
                await session.commit()
                return flow.to_dict()
            return None
    except Exception as e:
        logging.error(f"Failed to update flow: {e}")
        return None

# Define the route to update a flow
@bp.route('/genkit-flow/<int:flow_id>', methods=['PUT'])
async def update_genkit_flow(flow_id: int):
    flow_data = request.json
    if not flow_data:
        return jsonify({"error": "No flow data provided"}), 400
    updated_flow = await update_flow(flow_id, flow_data)
    if updated_flow:
        return jsonify(updated_flow), 200
    return jsonify({"error": "Flow not found"}), 404

# Define the function to delete a flow
async def delete_flow(flow_id: int) -> bool:
    try:
        async with get_async_session() as session:
            flow = await session.get(Flow, flow_id)
            if flow:
                await session.delete(flow)
                await session.commit()
                return True
            return False
    except Exception as e:
        logging.error(f"Failed to delete flow: {e}")
        return False

# Define the route to delete a flow
@bp.route('/genkit-flow/<int:flow_id>', methods=['DELETE'])
async def delete_genkit_flow(flow_id: int):
    if await delete_flow(flow_id):
        return jsonify({"message": "Flow deleted"}), 200
    return jsonify({"error": "Flow not found"}), 404

# Define the function to handle advanced templates
async def handle_advanced_template(flow_id: int, template: str) -> Optional[Dict[str, Any]]:
    try:
        async with get_async_session() as session:
            flow = await session.get(Flow, flow_id)
            if flow and flow.template == template:
                # Implement logic for handling advanced templates here
                return {"status": "success", "message": "Advanced template handled"}
            return None
    except Exception as e:
        logging.error(f"Failed to handle advanced template: {e}")
        return None

# Define the route to handle advanced templates
@bp.route('/genkit-flow/<int:flow_id>/advanced-template/<str:template>', methods=['POST'])
async def handle_advanced_genkit_flow(flow_id: int, template: str):
    if await handle_advanced_template(flow_id, template):
        return jsonify({"status": "success", "message": "Advanced template handled"}), 200
    return jsonify({"error": "Advanced template not found"}), 404

# Initialize the database
db.init_app(bp)

# Register the blueprint
def register_genkit_flow_routes(app):
    app.register_blueprint(bp)

# Example of a function to add a new flow
def add_new_flow(flow_data: Dict[str, Any]):
    db.session.add(Flow(**flow_data))
    db.session.commit()

# Example of a function to get all flows
def get_all_flows_db() -> List[Dict[str, Any]]:
    return db.session.query(Flow).all()

# Example of a function to get a specific flow by ID
def get_flow_by_id_db(flow_id: int) -> Optional[Dict[str, Any]]:
    return db.session.query(Flow).filter_by(id=flow_id).first()

# Example of a function to update a flow
def update_flow_db(flow_id: int, flow_data: Dict[str, Any]):
    flow = db.session.query(Flow).filter_by(id=flow_id).first()
    if flow:
        for key, value in flow_data.items():
            setattr(flow, key, value)
        db.session.commit()

# Example of a function to delete a flow
def delete_flow_db(flow_id: int):
    flow = db.session.query(Flow).filter_by(id=flow_id).first()
    if flow:
        db.session.delete(flow)
        db.session.commit()

# Example of a function to handle advanced templates
def handle_advanced_template_db(flow_id: int, template: str) -> Optional[Dict[str, Any]]:
    flow = db.session.query(Flow).filter_by(id=flow_id).first()
    if flow and flow.template == template:
        return {"status": "success", "message": "Advanced template handled"}
    return None
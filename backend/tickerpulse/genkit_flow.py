from typing import Any, AsyncIterable, Dict, List, Optional
import logging
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from .models import FlowTemplate, FlowStep
from .utils import get_db_session

bp = Blueprint('genkit_flow', __name__)

db = SQLAlchemy()

class FlowTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    steps = db.Column(db.JSON, nullable=False)

class FlowStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('flow_template.id'), nullable=False)
    step_name = db.Column(db.String(100), nullable=False)
    step_type = db.Column(db.String(50), nullable=False)
    step_config = db.Column(db.JSON, nullable=True)

@bp.route('/genkit-flow', methods=['POST'])
async def create_genkit_flow() -> Dict[str, Any]:
    """
    Create a new genkit flow with advanced templates.
    """
    data = request.get_json()
    template_name = data.get('template_name')
    if not template_name:
        return jsonify({"error": "Template name is required"}), 400

    try:
        async with get_db_session() as session:  # Use async context manager for database
            flow_template = await session.execute(
                db.select(FlowTemplate).where(FlowTemplate.name == template_name)
            )
            flow_template = flow_template.scalar_one_or_none()

            if not flow_template:
                return jsonify({"error": "Template not found"}), 404

            steps = flow_template.steps
            async for step in AsyncIterable(steps):
                await process_step(step)

            return jsonify({"message": "Flow created successfully"}), 201
    except Exception as e:
        logging.error(f"Error creating genkit flow: {e}")
        return jsonify({"error": str(e)}), 500

async def process_step(step: Dict[str, Any]) -> None:
    """
    Process a single step in the flow.
    """
    step_type = step.get('step_type')
    step_config = step.get('step_config')

    if step_type == 'streaming':
        async for chunk in stream_step(step_config):
            yield chunk
    else:
        result = await execute_step(step_config)
        logging.info(f"Step {step['step_name']} completed with result: {result}")

async def stream_step(config: Dict[str, Any]) -> AsyncIterable[str]:
    """
    Stream step execution.
    """
    # Simulate streaming step execution
    for i in range(5):
        yield f"Step {i+1} of 5 completed\n"
        await asyncio.sleep(1)

async def execute_step(config: Dict[str, Any]) -> Any:
    """
    Execute a step based on its configuration.
    """
    # Simulate step execution
    return {"status": "success", "data": "Step executed"}

def get_db_session() -> AsyncSession:
    """
    Get a new async SQLAlchemy session.
    """
    return db.session

# Example usage
if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run()
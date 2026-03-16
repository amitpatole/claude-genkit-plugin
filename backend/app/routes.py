from typing import Any, Dict, List, Optional
import logging
from flask import Flask, request, jsonify
from sqlite3 import Row
from contextlib import asynccontextmanager
from database import get_db_connection

app = Flask(__name__)

@asynccontextmanager
async def get_db() -> Row:
    conn = await get_db_connection()
    try:
        yield conn
    finally:
        await conn.close()

@app.route('/genkit-flow', methods=['POST'])
async def genkit_flow() -> Dict[str, Any]:
    logging.info("Generating Genkit Flow")
    template_id = request.json.get('template_id')
    if not template_id:
        return jsonify({"error": "Missing template_id"}), 400

    async with get_db() as db:
        # Example query to fetch template details
        query = "SELECT * FROM templates WHERE id = ?"
        template = await db.execute(query, (template_id,))
        if not template:
            return jsonify({"error": "Template not found"}), 404

        # Fetch and process template data
        template_data = await process_template(template)
        if not template_data:
            return jsonify({"error": "Failed to process template"}), 500

    # Generate flow based on template data
    flow = await generate_flow(template_data)
    if not flow:
        return jsonify({"error": "Failed to generate flow"}), 500

    # Stream the flow response
    return await stream_flow_response(flow)

def process_template(template: Row) -> Optional[Dict[str, Any]]:
    # Process template data and return as a dictionary
    return {
        "steps": [
            {"step_id": 1, "name": "Step 1", "description": "Description 1"},
            {"step_id": 2, "name": "Step 2", "description": "Description 2"}
        ]
    }

async def generate_flow(template_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    # Generate flow based on template data
    return [
        {"step_id": 1, "name": "Step 1", "description": "Description 1"},
        {"step_id": 2, "name": "Step 2", "description": "Description 2"}
    ]

async def stream_flow_response(flow: List[Dict[str, Any]]) -> Any:
    # Stream the flow response
    for step in flow:
        yield jsonify(step)
        await asyncio.sleep(1)  # Simulate streaming
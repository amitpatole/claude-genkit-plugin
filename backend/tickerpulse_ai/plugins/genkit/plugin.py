from flask import Blueprint, request, jsonify
from backend.tickerpulse_ai.plugins.genkit.snippets import fetch_snippets, add_snippet

genkit_plugin = Blueprint('genkit', __name__)

@genkit_plugin.route('/api/snippets', methods=['GET'])
async def get_snippets() -> Any:
    project_context = request.args.get('project_context')
    if not project_context:
        return jsonify({'error': 'Project context is required'}), 400
    snippets = await fetch_snippets(project_context)
    return jsonify(snippets)

@genkit_plugin.route('/api/snippets', methods=['POST'])
async def add_snippet_route() -> Any:
    project_context = request.form.get('project_context')
    snippet = request.form.get('snippet')
    if not project_context or not snippet:
        return jsonify({'error': 'Project context and snippet are required'}), 400
    await add_snippet(project_context, snippet)
    return jsonify({'message': 'Snippet added successfully'})
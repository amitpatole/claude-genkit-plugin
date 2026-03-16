from typing import Any, Dict, List
from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query

db = SQLAlchemy()

bp = Blueprint('genkit_templates', __name__, url_prefix='/genkit-templates')

class GenkitTemplate(db.Model):
    __tablename__ = 'genkit_templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template = db.Column(db.JSON, nullable=False)

@bp.route('/list', methods=['GET'])
async def list_templates() -> List[Dict[str, Any]]:
    templates = await db.session.query(GenkitTemplate).all()
    return [{'id': template.id, 'name': template.name} for template in templates]

@bp.route('/create', methods=['POST'])
async def create_template() -> Dict[str, Any]:
    data = request.json
    template = GenkitTemplate(name=data['name'], template=data['template'])
    db.session.add(template)
    await db.session.commit()
    return {'id': template.id}

if __name__ == '__main__':
    app.run()
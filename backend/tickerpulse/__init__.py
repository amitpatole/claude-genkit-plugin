from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.tickerpulse.genkit_flow import bp as genkit_flow_bp

db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickerpulse.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(genkit_flow_bp)
    with app.app_context():
        db.create_all()
        # Call setup functions here if needed
    return app
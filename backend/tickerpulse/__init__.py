from flask import Flask
from backend.tickerpulse.genkit_flow import genkit_flow_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(genkit_flow_bp)

    return app
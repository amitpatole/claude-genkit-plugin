from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['DATABASE'] = 'tickerpulse_ai.db'
    app.config['DATABASE_URI'] = 'sqlite:///tickerpulse_ai.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickerpulse_ai.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from backend.tickerpulse_ai.plugins.genkit import genkit_plugin
    app.register_blueprint(genkit_plugin)

    return app
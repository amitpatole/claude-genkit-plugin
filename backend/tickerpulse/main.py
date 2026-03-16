from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tickerpulse.genkit import bp as genkit_bp
from tickerpulse.genkit.templates import bp as templates_bp
from tickerpulse.config import app, db

app.register_blueprint(genkit_bp)
app.register_blueprint(templates_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
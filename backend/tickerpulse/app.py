from flask import Flask
from flask_sockets import Sockets
from tickerpulse.enforcement_agent import enforce_schedule

app = Flask(__name__)
sockets = Sockets(app)

@app.before_first_request
async def start_enforcement_agent() -> None:
    await enforce_schedule()
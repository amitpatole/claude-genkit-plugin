from flask import Flask
from backend.schedule_enforcement_agent import enforce_schedule

app = Flask(__name__)

@app.before_first_request
async def setup():
    await enforce_schedule()

if __name__ == "__main__":
    app.run()
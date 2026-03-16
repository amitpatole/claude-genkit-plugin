from flask import Flask
from backend.tickerpulse.enforcement_agent import enforce_schedule

app = Flask(__name__)
app.config['DATABASE'] = 'tickerpulse.db'

# Example route to test the enforcement agent
@app.route('/enforce-schedule/<user_id>/<current_time>', methods=['GET'])
async def enforce_schedule_route(user_id: int, current_time: str):
    result = await enforce_schedule(user_id, current_time)
    return {'result': result}
from flask import Flask
from tickerpulse.schedule_enforcement_agent import ScheduleEnforcementAgent

def create_app():
    app = Flask(__name__)
    app.config['DB_PATH'] = 'path/to/database.db'
    app.config['NON_DEV_HOURS'] = ('18:00', '06:00')  # Example non-dev hours

    @app.route('/enforce-schedule', methods=['GET'])
    async def enforce_schedule():
        agent = ScheduleEnforcementAgent()
        await agent.enforce_schedule()
        return 'Schedule enforced'

    return app
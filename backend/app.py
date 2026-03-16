from flask import Flask
from schedule_enforcement.schedule_enforcement import ScheduleEnforcementAgent
from schedule_enforcement.deployment_violations import get_all_violations

app = Flask(__name__)
enforcement_agent = ScheduleEnforcementAgent()

@app.before_request
def before_request():
    if not enforcement_agent.is_allowed_time():
        deployment_time = datetime.now(timezone.utc).astimezone(timezone(offset=3600 * 5))
        enforcement_agent.enforce_schedule(deployment_time)

@app.route('/violations')
def get_violations():
    violations = get_all_violations()
    return {"violations": [dict(v) for v in violations]}
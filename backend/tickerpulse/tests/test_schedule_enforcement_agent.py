from unittest.mock import patch
from datetime import datetime
from backend.tickerpulse.schedule_enforcement_agent import ScheduleEnforcementAgent, get_non_dev_hours

def test_enforce_schedule():
    with patch("backend.tickerpulse.schedule_enforcement_agent.datetime") as mock_datetime:
        mock_datetime.now.return_value.time.return_value = datetime.strptime("15:00", "%H:%M").time()
        non_dev_hours = [{"start": "14:00", "end": "16:00"}]
        current_app.config["NON_DEV_HOURS"] = non_dev_hours

        agent = ScheduleEnforcementAgent(db_path="test.db")
        with agent:
            agent.enforce_schedule()

        assert mock_datetime.now.return_value.time.call_count == 1
        assert agent.cursor.execute.call_count == 1
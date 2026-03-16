from unittest.mock import patch, MagicMock
import pytest
from tickerpulse.schedule_enforcement_agent import ScheduleEnforcementAgent, NON_DEV_HOURS

def test_enforce_schedule(caplog):
    with patch('tickerpulse.schedule_enforcement_agent.sqlite3.connect') as mock_connect:
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_cursor
        mock_cursor.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'id': 1, 'execution_time': '2023-10-01 18:00:00'}]

        agent = ScheduleEnforcementAgent()
        agent.enforce_schedule()

        assert len(caplog.records) == 2
        assert caplog.records[0].levelname == 'INFO'
        assert "Task 1 scheduled for non-dev hours, executing now." in caplog.text
        assert caplog.records[1].levelname == 'INFO'
        assert "Executing task 1" in caplog.text
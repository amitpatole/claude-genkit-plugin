from unittest.mock import patch, MagicMock
from datetime import time
from tickerpulse.schedule_enforcement import enforce_schedule, get_current_time, is_in_non_dev_hours
from tickerpulse.models import ScheduleEnforcementLog

def test_enforce_schedule_non_dev_hours(caplog):
    with patch('tickerpulse.schedule_enforcement.get_current_time', return_value=time(10, 0, 0)):
        assert enforce_schedule() is None
    assert "Enforcement not needed" in caplog.text

def test_enforce_schedule_dev_hours(caplog):
    with patch('tickerpulse.schedule_enforcement.get_current_time', return_value=time(18, 0, 0)):
        with patch('tickerpulse.schedule_enforcement.ScheduleEnforcementLog', new_callable=MagicMock) as mock_log_entry:
            enforce_schedule()
            mock_log_entry.assert_called_once_with(timestamp=time(18, 0, 0))
    assert "Enforcement log entry created" in caplog.text
from unittest.mock import patch
from backend.tickerpulse.schedule_enforcement import enforce_schedule, get_current_time, is_non_dev_hour
from backend.utils.db import execute_query

@patch("backend.tickerpulse.schedule_enforcement.get_current_time")
@patch("backend.tickerpulse.schedule_enforcement.is_non_dev_hour")
def test_enforce_schedule(mock_is_non_dev_hour, mock_get_current_time):
    mock_is_non_dev_hour.return_value = True
    mock_get_current_time.return_value = "2023-10-01 15:00:00"

    with patch("backend.tickerpulse.schedule_enforcement.execute_query") as mock_execute_query:
        mock_execute_query.return_value = {"active": True}
        enforce_schedule({"key": "value"})

    mock_execute_query.assert_called_once_with(
        "SELECT * FROM schedule WHERE active = ?",
        (True,)
    )
from unittest.mock import patch, MagicMock
from backend.tickerpulse.schedule_enforcement_agent import enforce_schedule
from backend.utils.db import get_db_connection

def test_enforce_schedule():
    """Test the enforce_schedule function."""
    with patch.object(get_db_connection, "cursor", return_value=MagicMock(row_factory=MagicMock(side_effect=[[{"start_time": "00:00", "end_time": "06:00"}]]))):
        with patch.object(logging, "info") as mock_log:
            enforce_schedule()
            mock_log.assert_called_with("Current time is within non-development hours. Enforcing schedule.")
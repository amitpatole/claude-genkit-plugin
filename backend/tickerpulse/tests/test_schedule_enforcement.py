from unittest.mock import patch
from backend.tickerpulse.schedule_enforcement import enforce_schedule, get_enforcement_periods
from backend.utils.db import get_db_connection

def test_enforce_schedule() -> None:
    """
    Test the enforce_schedule function.
    """
    with patch.object(get_db_connection, 'execute') as mock_execute:
        mock_execute.return_value.fetchall.return_value = [{}]
        enforce_schedule(5)
        mock_execute.assert_called_once_with("SELECT * FROM schedule_enforcement WHERE period = ?", (5,))

def test_get_enforcement_periods() -> None:
    """
    Test the get_enforcement_periods function.
    """
    with patch.object(get_db_connection, 'execute') as mock_execute:
        mock_execute.return_value.fetchall.return_value = [{}]
        periods = list(get_enforcement_periods())
        assert periods == [{}]
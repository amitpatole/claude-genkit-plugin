from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.tickerpulse.schedule_enforcement_agent import get_non_dev_hours, is_within_non_dev_hours, enforce_schedule, main, fetch_data

def test_get_non_dev_hours() -> None:
    """Test the get_non_dev_hours function."""
    with patch('backend.tickerpulse.schedule_enforcement_agent.current_app.config') as mock_config:
        mock_config.get.return_value = [(time(18, 0), time(22, 0)), (time(23, 0), time(05, 0))]
        assert get_non_dev_hours() == [(time(18, 0), time(22, 0)), (time(23, 0), time(05, 0))]

def test_is_within_non_dev_hours() -> None:
    """Test the is_within_non_dev_hours function."""
    with patch('backend.tickerpulse.schedule_enforcement_agent.time') as mock_time:
        mock_time.return_value = time(21, 30)
        assert is_within_non_dev_hours(time(21, 30)) is True

        mock_time.return_value = time(10, 0)
        assert is_within_non_dev_hours(time(10, 0)) is False

def test_enforce_schedule() -> None:
    """Test the enforce_schedule function."""
    with patch('backend.tickerpulse.schedule_enforcement_agent.logging') as mock_logging:
        with patch('backend.tickerpulse.schedule_enforcement_agent.is_within_non_dev_hours') as mock_is_within:
            mock_is_within.return_value = True
            enforce_schedule()
            mock_logging.warning.assert_called_once_with("Non-development hours detected. Enforcing schedule.")

def test_main() -> None:
    """Test the main function."""
    with patch('backend.tickerpulse.schedule_enforcement_agent.enforce_schedule') as mock_enforce:
        main()
        mock_enforce.assert_called_once()

def test_fetch_data() -> None:
    """Test the fetch_data function."""
    with patch('backend.tickerpulse.schedule_enforcement_agent.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'key': 'value'}
        mock_conn = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        result = fetch_data()
        assert result == {'key': 'value'}
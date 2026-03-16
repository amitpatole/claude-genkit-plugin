from unittest.mock import patch
from backend.tickerpulse.schedule_enforcement_agent import is_non_dev_hour, enforce_schedule, main
from datetime import datetime

def test_is_non_dev_hour() -> None:
    """Test is_non_dev_hour function."""
    with patch('backend.tickerpulse.schedule_enforcement_agent.datetime') as mock_datetime:
        mock_datetime.now.return_value.time.return_value = time(8, 0)
        assert is_non_dev_hour() == True

        mock_datetime.now.return_value.time.return_value = time(18, 0)
        assert is_non_dev_hour() == True

        mock_datetime.now.return_value.time.return_value = time(12, 0)
        assert is_non_dev_hour() == False

def test_enforce_schedule(caplog) -> None:
    """Test enforce_schedule function."""
    with patch('backend.tickerpulse.schedule_enforcement_agent.is_non_dev_hour', return_value=True):
        with patch('backend.tickerpulse.schedule_enforcement_agent.logging') as mock_logging:
            enforce_schedule()
            mock_logging.info.assert_called_once_with("Enforcing schedule: Non-development hour detected.")

def test_main(caplog) -> None:
    """Test main function."""
    with patch('backend.tickerpulse.schedule_enforcement_agent.is_non_dev_hour', return_value=True):
        main()
        assert "Enforcing schedule: Non-development hour detected." in caplog.text
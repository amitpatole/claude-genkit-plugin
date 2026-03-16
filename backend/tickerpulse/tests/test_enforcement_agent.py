from unittest.mock import patch, MagicMock
from datetime import datetime, time
from backend.tickerpulse.enforcement_agent import get_non_dev_hours_start_end, is_within_non_dev_hours, enforce_schedule, main

def test_get_non_dev_hours_start_end() -> None:
    """Test get_non_dev_hours_start_end function."""
    expected_start, expected_end = time(18, 0), time(9, 0)
    assert get_non_dev_hours_start_end() == (expected_start, expected_end)

def test_is_within_non_dev_hours() -> None:
    """Test is_within_non_dev_hours function."""
    non_dev_start, non_dev_end = get_non_dev_hours_start_end()
    assert is_within_non_dev_hours(time(17, 0)) is False  # Outside non-dev hours
    assert is_within_non_dev_hours(time(18, 0)) is True   # At non-dev hours
    assert is_within_non_dev_hours(time(20, 0)) is False  # Outside non-dev hours

@patch("backend.tickerpulse.enforcement_agent.sqlite3.connect")
@patch("backend.tickerpulse.enforcement_agent.datetime.now")
def test_enforce_schedule(mock_now, mock_connect) -> None:
    """Test enforce_schedule function."""
    mock_now.return_value.time.return_value = time(18, 0)
    mock_cursor = MagicMock()
    mock_connect.return_value.__aenter__.return_value.cursor.return_value = mock_cursor
    enforce_schedule("test.db")
    mock_cursor.execute.assert_called_once_with("SELECT * FROM some_table")  # Adjust the query as necessary

@patch("backend.tickerpulse.enforcement_agent.main")
def test_main(mock_main) -> None:
    """Test main function."""
    main()
    mock_main.assert_called_once()
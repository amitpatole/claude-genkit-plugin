from unittest.mock import patch
from backend.tickerpulse.genkit_flow import generate_flow_template, DATABASE_PATH
import pytest

@patch.dict("os.environ", {"GENKIT_DB_PATH": "test.db"})
def test_generate_flow_template():
    from backend.tickerpulse.genkit_flow import get_db_connection

    with patch.object(get_db_connection, "acquire") as mock_acquire:
        mock_acquire.return_value = {"template_content": "Test Template"}
        assert generate_flow_template(1) == "Test Template"

    with patch.object(get_db_connection, "acquire") as mock_acquire:
        mock_acquire.return_value = None
        assert generate_flow_template(2) is None
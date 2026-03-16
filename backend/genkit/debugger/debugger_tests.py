from typing import Any
import unittest
from unittest.mock import patch, MagicMock
from backend.genkit.debugger.debugger import setup_platform_configurations, start_debug_session

class TestDebugger(unittest.TestCase):
    @patch("backend.genkit.debugger.debugger.os.getenv")
    @patch("backend.genkit.debugger.debugger.create_connection")
    @patch("backend.genkit.debugger.debugger.execute_query")
    def test_setup_platform_configurations(self, mock_execute_query, mock_create_connection, mock_getenv) -> None:
        mock_getenv.return_value = "Darwin"
        setup_platform_configurations("Darwin")
        # Assertions for Darwin-specific configurations

    @patch("backend.genkit.debugger.debugger.os.getenv")
    @patch("backend.genkit.debugger.debugger.request")
    def test_start_debug_session(self, mock_request, mock_getenv) -> None:
        mock_request.json = {"platform": "Linux"}
        mock_getenv.return_value = "Linux"
        response = start_debug_session()
        self.assertEqual(response, {"status": "success"})
        # Additional assertions for the response

if __name__ == "__main__":
    unittest.main()
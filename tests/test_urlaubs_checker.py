from unittest.mock import MagicMock
from unittest.mock import patch

from urlaubs_checker.app import run


@patch("builtins.print")
def test_run(mock_print: MagicMock) -> None:
    run()
    mock_print.assert_called_once_with("Hello World from urlaubs-checker")

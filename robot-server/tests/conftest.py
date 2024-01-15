import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


@pytest.fixture
def expected_timestamp():
    return datetime.now()


@pytest.fixture
def expected_id():
    return "1234"


@pytest.fixture
def mock_transaction_scope(expected_id, expected_timestamp):
    mock_cursor = MagicMock()
    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = mock_cursor

    # Default values incase does not care about the returned values.
    mock_cursor.fetchone.return_value = [expected_id, expected_timestamp]

    with patch(
        "src.repositories.job_result_repository.transaction_scope",
        return_value=mock_context_manager,
    ):
        yield mock_cursor

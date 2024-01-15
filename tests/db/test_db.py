import pytest
from unittest.mock import patch, MagicMock

from psycopg2 import OperationalError

from src.db.db import transaction_scope, _get_connection_from_env


@patch("src.db.db.psycopg2.connect")
def test_transaction_scope_commits_and_closes(mock_connect):
    # Arrange
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Act
    with transaction_scope() as cursor:
        pass

    # Assert
    mock_cursor.execute.assert_not_called()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("src.db.db.psycopg2.connect")
def test_transaction_scope_rollbacks_and_closes_on_operational_error(mock_connect):
    # Arrange
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.side_effect = OperationalError
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Act
    with pytest.raises(OperationalError):
        with transaction_scope() as cursor:
            pass

    # Assert
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("src.db.db.psycopg2.connect")
@patch("src.db.db.os.getenv")
def test_connection_is_configurable_from_environment(mock_getenv, mock_connect):
    # Arrange
    mock_getenv.side_effect = lambda k, d: {
        "POSTGRES_HOST": "test_host",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DB": "test_db",
        "POSTGRES_USER": "test_user",
        "POSTGRES_PASSWORD": "test_password",
    }.get(k, d)

    mock_connect.return_value = MagicMock()

    # Act
    _get_connection_from_env()

    # Assert
    mock_connect.assert_called_once_with(
        host="test_host",
        port="5432",
        dbname="test_db",
        user="test_user",
        password="test_password",
    )

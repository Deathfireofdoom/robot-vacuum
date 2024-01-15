from src.repositories.job_result_repository import JobResultRepository, MIGRATION_FILES
from src.models.job_results import JobResult


def test_job_result_repository_adds_id_and_timestamp(
    mock_transaction_scope, expected_id, expected_timestamp
):
    # Arrange
    job_result = JobResult(commands=5, result=2, duration=3.5)
    job_result_repository = JobResultRepository()

    # Act
    updated_job_result = job_result_repository.insert_job_result(job_result)

    # Assert
    assert updated_job_result._id == expected_id
    assert updated_job_result.timestamp == expected_timestamp.isoformat()


def test_job_result_repository_correctly_create_insert_statement(
    mock_transaction_scope,
):
    # Arrange
    job_result = JobResult(commands=5, result=2, duration=3.5)
    expected_sql = """INSERT INTO job_results (commands, result, duration) VALUES (%s, %s, %s) RETURNING id, timestamp"""
    expected_params = [job_result.commands, job_result.result, job_result.duration]
    job_result_repository = JobResultRepository()

    # Act
    job_result_repository.insert_job_result(job_result)

    # Assert
    mock_transaction_scope.execute.assert_called_once_with(
        expected_sql, expected_params
    )


def test_job_result_repository_correctly_selects_migration_query(
    mock_transaction_scope,
):
    # Arrange
    version = "1"
    direction = "up"
    expected_migration_file = MIGRATION_FILES[version][direction]
    job_result_repository = JobResultRepository()

    # Act
    job_result_repository._migrate(version=version, direction=direction)

    # Assert
    mock_transaction_scope.execute.assert_called_once_with(expected_migration_file)

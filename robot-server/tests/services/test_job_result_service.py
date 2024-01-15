import pytest
from unittest.mock import patch, MagicMock

from src.models.job_results import JobResult
from src.models.job import Job

from src.services.job_result_service import JobResultService

from tests.utils.test_data import test_data


@pytest.fixture
@patch("src.services.job_result_service.JobResultRepository", MagicMock())
def patched_job_result_service():
    return JobResultService()


def test_job_result_service_calculates_and_save_job_result(patched_job_result_service):
    # Arrange
    job = Job.from_dict(_dict=test_data[0]["input"])
    duration = 0.0
    n_visited = test_data[0]["expected"]["result"]
    patched_job_result_service._calc_job_result = MagicMock(
        side_effect=patched_job_result_service._calc_job_result
    )

    # Act
    patched_job_result_service.calc_and_save_job_result(
        job=job, duration=0.0, n_visited=n_visited
    )

    # Assert
    patched_job_result_service._calc_job_result.assert_called_once()
    patched_job_result_service.job_result_repository.insert_job_result.assert_called_once()


# NOTE: Not sure if this test actually adds that much value with the current implementation.
#       Looking at the function, it looks like this test only test pythons built in function len
#       and if I put the parameters in the right place.
#
#       Could still be good to have a test for it in case the logic changes in the future,
#       since this is a critical function we want to know if it breaks, not that I can imagien
#       how it would break.
@pytest.mark.parametrize("test_case", test_data)
def test_calc_job_result_is_correct(test_case, patched_job_result_service):
    # Arrange
    job = Job.from_dict(_dict=test_case["input"])
    duration = 0.0
    expected_output = JobResult(
        commands=test_case["expected"]["commands"],
        result=test_case["expected"]["result"],
        duration=duration,
    )

    # Act
    job_result = patched_job_result_service._calc_job_result(
        job=job, duration=duration, n_visited=test_case["expected"]["result"]
    )

    # Assert
    assert job_result == expected_output

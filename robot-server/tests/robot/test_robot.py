import pytest

from src.models.job import Job
from src.models.direction import Direction
from src.models.location import Location

from src.robot.robot import Robot

from tests.utils.test_data import test_data


@pytest.fixture
def robot():
    return Robot()


@pytest.mark.parametrize("test_case", test_data)
def test_robot_can_handle_job(
    robot, test_case, mock_transaction_scope, expected_id, expected_timestamp
):
    # Arrange
    job = Job.from_dict(_dict=test_case["input"])
    expected_result = test_case["expected"]

    # Act
    job_result = robot.handle_job(job=job)

    # Compare
    assert job_result.commands == expected_result["commands"]
    assert job_result.result == expected_result["result"]
    assert job_result._id == expected_id
    assert job_result.timestamp == expected_timestamp.isoformat()

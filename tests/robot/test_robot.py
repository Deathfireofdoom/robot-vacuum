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


def test_robot_reset_memory_on_new_job(robot, mock_transaction_scope):
    # Arrange
    job_1 = Job.from_dict(_dict=test_data[0]["input"])
    job_2 = Job.from_dict(_dict=test_data[0]["input"])

    # Act
    robot.handle_job(job=job_1)
    first_job_memory = robot.memory
    robot.handle_job(job=job_2)
    second_job_memory = robot.memory

    # Assert
    assert first_job_memory != second_job_memory


def test_calculate_new_location_correctly(robot):
    """
    New location should be one cordinate in the provided direction
    """
    # Arrange
    start_x = 0
    start_y = 0
    start_location = Location(x=start_x, y=start_y)
    directions_with_expected_result = {
        Direction.NORTH: Location(x=start_x + 1, y=start_y),
        Direction.EAST: Location(x=start_x, y=start_y + 1),
        Direction.SOUTH: Location(x=start_x - 1, y=start_y),
        Direction.WEST: Location(x=start_x, y=start_y - 1),
    }

    # Act & Assert
    for direction, result in directions_with_expected_result.items():
        assert result == robot._calculate_new_location(start_location, direction)

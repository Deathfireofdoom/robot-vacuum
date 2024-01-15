# NOTE: In real life I would probably add some more test to the other models
#       but I dont think it adds any value for this case.
#
#       Also a lot of the other models are tested in this as a side effect.
import pytest

from dataclasses import asdict

from src.models.job import Job

from tests.utils.test_data import test_data


@pytest.mark.parametrize("test_case", test_data)
def test_job_model_parses_valid_dict(test_case):
    # Arrange
    valid_dict = test_case["input"]

    # Act
    job = Job.from_dict(_dict=valid_dict)

    # Assert - # NOTE: A better way is to manully setup the expected state and not use asdict.
    #                  But this is just a case and it save time.
    assert asdict(job) == valid_dict


def test_job_model_detects_invalid_dict():
    # Arrange
    invalid_dict = {
        "start": {
            "z": 4,
            "k": 2,
        },
        "commands": [],
    }

    # Act & Assert
    with pytest.raises(TypeError) as exc_info:
        Job.from_dict(_dict=invalid_dict)

    assert "got an unexpected keyword argument 'z'" in str(exc_info.value)


def test_job_model_detects_non_valid_direction():
    # Arrange
    invalid_direction_dict = {
        "start": {
            "x": 1,
            "y": 3,
        },
        "commands": [
            {"direction": "south", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "north", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "kayne", "steps": 1},
            {"direction": "west", "steps": 1},
        ],
    }

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Job.from_dict(_dict=invalid_direction_dict)

    assert "'kayne' is not a valid Direction" in str(exc_info.value)

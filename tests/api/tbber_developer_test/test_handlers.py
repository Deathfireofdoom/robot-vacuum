import pytest
import json

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture
def endpoint():
    return "/tibber-developer-test/enter-path"


# Long reaching test. - Testing the full system - borderline intergration test
from tests.utils.test_data import test_data
@pytest.mark.parametrize("test_case", test_data)
def test_endpoint_return_correct_result(
    client, endpoint, test_case, mock_transaction_scope, expected_id, expected_timestamp
):
    # Arrange
    job_body = test_case["input"]
    expected_result = test_case["expected"]

    # Act
    response = client.post(
        endpoint, data=json.dumps(job_body), content_type="application/json"
    )
    job_result = response.json

    # Assert
    assert response.status_code == 200
    assert job_result["commands"] == expected_result["commands"]
    assert job_result["result"] == expected_result["result"]
    assert job_result["_id"] == expected_id
    assert job_result["timestamp"] == expected_timestamp.isoformat()


def test_endpoint_needs_json_body(endpoint, client):
    # Act
    response = client.post(endpoint, content_type="application/json")

    # Assert
    assert response.status_code == 400


def test_endpoint_validates_data_correctly(endpoint, client):
    # Arrange
    invalid_body = {
        "start": {
            "x": 1,
            "y": 1,
        },
        "commandos": [{"commando": "right"}],
    }

    # Act
    response = client.post(
        endpoint, data=json.dumps(invalid_body), content_type="application/json"
    )

    # Assert
    assert response.status_code == 400

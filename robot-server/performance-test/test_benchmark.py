import json
import os
import pytest

from src.models.job import Job
from src.robot.robot import Robot


def run_heavy_job(sub_grid_size):
    with open("./performance-test/robotcleanerpathheavy.json", "r") as file:
        data_json = file.readlines()
    json_string = "".join(data_json)
    job_dict = json.loads(json_string)

    job = Job.from_dict(job_dict)
    job.commands = job.commands
    robot = Robot()
    robot.memory.sub_grid_size = sub_grid_size
    robot.handle_job(job=job)

@pytest.mark.parametrize('sub_grid_size', [100, 500, 1000])
def test_benchmark(sub_grid_size, benchmark, mock_transaction_scope):
    benchmark.pedantic(run_heavy_job, iterations=1, rounds=1, kwargs={'sub_grid_size': sub_grid_size})

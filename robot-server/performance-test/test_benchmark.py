import json

from src.models.job import Job
from src.robot.robot import Robot


def run_heavy_job():
    #N_COMMANDS = 300 # Make it a bit bareable

    with open("./performance-test/robotcleanerpathheavy.json", "r") as file:
        data_json = file.readlines()
    json_string = "".join(data_json)
    job_dict = json.loads(json_string)

    job = Job.from_dict(job_dict)
    job.commands = job.commands
    robot = Robot()

    robot.handle_job(job=job)


def test_benchmark(benchmark, mock_transaction_scope):
    benchmark.pedantic(run_heavy_job, iterations=1, rounds=1)
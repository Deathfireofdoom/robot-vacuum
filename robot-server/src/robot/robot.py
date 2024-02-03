from datetime import datetime

from src.models.job import Job
from src.models.job_results import JobResult
from src.models.command import Command
from src.models.direction import Direction
from src.models.location import Location

from src.services.job_result_service import JobResultService

import rust.rust_memory as rust_memory

from src.utils.logger import get_logger

log = get_logger("robot")


class Robot:
    def __init__(self) -> None:
        self.job_result_service = JobResultService()

    def handle_job(self, job: Job) -> JobResult:
        # start the job
        start_time = datetime.now()
        log.info(f"starting job at {start_time.isoformat()}")

        # calling the rust code from python
        unique_visited = rust_memory.handle_job(job.commands, job.start)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log.info(f"done at {end_time.isoformat()} took {duration}s")

        # calculate job result
        job_result = self.job_result_service.calc_and_save_job_result(
            job=job, duration=duration, n_visited=unique_visited
        )
        return job_result
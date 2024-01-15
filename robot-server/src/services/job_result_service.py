from src.models.job import Job
from src.models.job_results import JobResult

from src.repositories.job_result_repository import JobResultRepository


class JobResultService:
    def __init__(self) -> None:
        self.job_result_repository = JobResultRepository()

    def calc_and_save_job_result(
        self, job: Job, duration: float, n_visited: int
    ) -> JobResult:
        job_result = self._calc_job_result(
            job=job, duration=duration, n_visited=n_visited
        )

        # Saves job result to databasea, also adds timestamp and id to job-result
        job_result = self.job_result_repository.insert_job_result(job_result=job_result)

        return job_result

    @staticmethod
    def _calc_job_result(job: Job, duration: float, n_visited: int) -> JobResult:
        """
        NOTE: not really advanced calcuation, but to future proof the service I broke it out in a separate function
              for easy testing.
        """
        # commands
        n_commands = len(job.commands)

        return JobResult(commands=n_commands, result=n_visited, duration=duration)

from datetime import datetime

from src.models.job import Job
from src.models.job_results import JobResult
from src.models.command import Command
from src.models.direction import Direction
from src.models.location import Location

from src.services.job_result_service import JobResultService

from .memory_c import CMemoryWrapper

from src.utils.logger import get_logger

log = get_logger("robot")


class Robot:
    def __init__(self) -> None:
        self.location = Location(0, 0)
        self._reset_or_initilise_memory()
        self.job_result_service = JobResultService()

    def handle_job(self, job: Job) -> JobResult:
        # reset memory
        self._reset_or_initilise_memory()

        # move robot to start location
        start_time = datetime.now()
        log.info(f"starting job at {start_time.isoformat()}")
        self.x, self.y = job.start.x, job.start.y
        #self.memory.add_location(self.x, self.y) CHECK THIS

        # loop the commands and act on them
        for command in job.commands:
            self._act_on_command(command=command)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log.info(f"done at {end_time.isoformat()} took {duration}s")

        # calculate job result
        job_result = self.job_result_service.calc_and_save_job_result(
            job=job, duration=duration, n_visited=self.memory.get_unique_n_visited(free_memory=True)
        )
        return job_result

    def _act_on_command(self, command: Command):
        x_end, y_end = self._get_end_location(command.direction, command.steps)
        self.memory.add_locations(self.x, self.y, x_end, y_end)
        self.x = x_end
        self.y = y_end

    def _get_end_location(
        self, direction: Direction, steps: int
    ):
        match Direction(direction):
            case Direction.NORTH:
                return self.x + steps, self.y
            case Direction.EAST:
                return self.x, self.y + steps
            case Direction.SOUTH:
                return self.x - steps, self.y
            case Direction.WEST:
                return self.x, self.y - steps
            case _:
                log.warning(f"{direction} is not a real direction, ignoring...")

    def _reset_or_initilise_memory(self):
        """
        I could in theory put this logic inside the Memory class, but to avoid unexpected bugs with
        reusing a class I decided it would be best to just get a new one.
        """
        self.memory = CMemoryWrapper()

from datetime import datetime

from src.models.job import Job
from src.models.job_results import JobResult
from src.models.command import Command
from src.models.direction import Direction
from src.models.location import Location

from src.services.job_result_service import JobResultService

from .memory import BitMapMemory

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
        self.memory.add_location(self.x, self.y)

        # loop the commands and act on them
        for command in job.commands:
            self._act_on_command(command=command)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log.info(f"done at {end_time.isoformat()} took {duration}s")

        # calculate job result
        job_result = self.job_result_service.calc_and_save_job_result(
            job=job, duration=duration, n_visited=self.memory.get_unique_n_visited()
        )
        return job_result

    def _act_on_command(self, command: Command):
        action = self._get_action(command.direction)
        for _ in range(command.steps):
            action()
            self.memory.add_location(self.x, self.y)

    def _move_north(self):
        self.x += 1

    def _move_east(self):
        self.y += 1

    def _move_south(self):
        self.x -= 1
    
    def _move_west(self):
        self.y -= 1
    
    def _get_action(
        self, direction: Direction
    ):
        match Direction(direction):
            case Direction.NORTH:
                return self._move_north
            case Direction.EAST:
                return self._move_east
            case Direction.SOUTH:
                return self._move_south
            case Direction.WEST:
                return self._move_west
            case _:
                log.warning(f"{direction} is not a real direction, ignoring...")

    def _reset_or_initilise_memory(self):
        """
        I could in theory put this logic inside the Memory class, but to avoid unexpected bugs with
        reusing a class I decided it would be best to just get a new one.
        """
        self.memory = BitMapMemory()

from datetime import datetime

from src.models.job import Job
from src.models.job_results import JobResult
from src.models.command import Command
from src.models.direction import Direction
from src.models.location import Location

from src.services.job_result_service import JobResultService

from .memory import Memory

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
        self._update_location(location=job.start)

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
        for step in range(command.steps):
            log.info(
                f"taking {step} of {command.steps} in direction {command.direction}"
            )
            self._move_robot(direction=command.direction)

    def _move_robot(self, direction: Direction):
        new_location = self._calculate_new_location(
            old_location=self.location, direction=direction
        )
        self._update_location(new_location)

    def _update_location(self, location: Location):
        self.location = location
        self.memory.add_location(self.location)

    @staticmethod
    def _calculate_new_location(
        old_location: Location, direction: Direction
    ) -> Direction:
        match Direction(direction):
            case Direction.NORTH:
                return Location(old_location.x + 1, old_location.y)
            case Direction.EAST:
                return Location(old_location.x, old_location.y + 1)
            case Direction.SOUTH:
                return Location(old_location.x - 1, old_location.y)
            case Direction.WEST:
                return Location(old_location.x, old_location.y - 1)
            case _:
                log.warning(f"{direction} is not a real direction, ignoring...")
                return old_location

    def _reset_or_initilise_memory(self):
        """
        I could in theory put this logic inside the Memory class, but to avoid unexpected bugs with
        reusing a class I decided it would be best to just get a new one.
        """
        self.memory = Memory()

from __future__ import annotations
from dataclasses import dataclass

from .direction import Direction

from .exceptions import get_type_error_for_data_validation


@dataclass
class Command:
    direction: Direction
    steps: int

    def __post_init__(self):
        if Direction.valid_direction(Direction(self.direction)):
            raise get_type_error_for_data_validation(
                "direction", type(self.direction), Direction
            )

        if not isinstance(self.steps, int):
            raise get_type_error_for_data_validation("steps", type(self.steps), int)

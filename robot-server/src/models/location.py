from __future__ import annotations
from dataclasses import dataclass

from .exceptions import get_type_error_for_data_validation


@dataclass(frozen=True)  # To make it hashable
class Location:
    x: int
    y: int

    def __post_init__(self):
        if not isinstance(self.x, int):
            raise get_type_error_for_data_validation("x", type(self.x), int)

        if not isinstance(self.y, int):
            raise get_type_error_for_data_validation("y", type(self.y), int)

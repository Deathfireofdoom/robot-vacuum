from enum import Enum


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    @classmethod
    def valid_direction(cls, value):
        return value in cls._value2member_map_

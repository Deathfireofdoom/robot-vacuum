from __future__ import annotations
from dataclasses import dataclass

from .location import Location
from .command import Command


@dataclass
class Job:
    start: Location
    commands: list[Command]

    @classmethod
    def from_dict(cls, _dict: dict) -> Job:
        start_location_data = _dict.get("start")
        commands_data = _dict.get("commands")

        start_location = Location(**start_location_data)
        commands = [Command(**command_data) for command_data in commands_data]

        return cls(start=start_location, commands=commands)

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .exceptions import get_type_error_for_data_validation


@dataclass
class JobResult:
    commands: int
    result: int
    duration: float
    timestamp: Optional[str] = None
    _id: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.commands, int):
            raise get_type_error_for_data_validation(
                "commands", type(self.commands), int
            )

        if not isinstance(self.result, int):
            raise get_type_error_for_data_validation("result", type(self.result), int)

        if not isinstance(self.duration, float):
            raise get_type_error_for_data_validation(
                "duration", type(self.duration), float
            )

        if self.timestamp is not None and not isinstance(self.timestamp, str):
            raise get_type_error_for_data_validation(
                "timestamp", type(self.timestamp), str
            )

        if self._id is not None and not isinstance(self._id, str):
            raise get_type_error_for_data_validation("_id", type(self._id), str)

    @classmethod
    def from_db_results(cls, row: tuple) -> JobResult:
        """
        This assumes the sql query fecthes the fields in the right order,
        so not really a generic method.

        # NOTE: Did not end up using this function, so in real code I would probably removed it.
        """
        if row is None:
            return None

        return JobResult(
            _id=row[0],
            commands=row[1],
            result=row[2],
            duration=row[3],
            timestamp=row[4].isoformat(),
        )

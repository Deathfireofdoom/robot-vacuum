from src.models.location import Location


class Memory:
    """
    I decided to make a separate memory class to isolate the logic for calcuating memory, since I anticipated it would
    be a bit "complex".

    In hindsight it was not that complex and could possible be transfered into the robot-class, however, in the future
    if we start to get super long routes etc, then we maybe want to use some probalistic techniques and then it
    is kinda handy its already de-coupled from the robot.

    This was the most efficient way I came up to that did not involved super complex logic.

    Appending new element: O(1)
    Storage complexity: O(n)

    Similiar to storing in a list and then convert it to a set, but it adds a extra step.

    """

    def __init__(self):
        self.visited = set()

    def add_location(self, location: Location):
        self.visited.add(location)

    def get_unique_n_visited(self) -> int:
        return len(self.visited)

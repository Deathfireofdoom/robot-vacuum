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

from bitarray import bitarray
class BitMapMemory:
    width = 200_001
    height = 200_001

    def __init__(self):
        self.array = bitarray(self.width * self.height)
        self.array.setall(0)
        self.unique_visits = 0

    def _get_index(self, x, y):
        return (x + self.width // 2) * self.height + (y + self.height // 2)

    def add_location(self, x: int, y: int):
        index = self._get_index(x, y)
        if not self.array[index]:
            self.array[index] = 1
            self.unique_visits += 1

    def get_unique_n_visited(self):
        return self.unique_visits


from src.utils.bitarray.bitarray import BitArray
class BitMapMemoryHomeMade:
    width = 64
    height = 64
    
    def __init__(self):
        self.array = BitArray(self.width * self.height)
        self.unique_visits = 0

    def _get_index(self, x, y):
        return (x + self.width // 2) * self.height + (y + self.height // 2)
    
    def add_location(self, location: Location):
        index = self._get_index(location.x, location.y)
        if not self.array.get_bit(index):
            self.array.set_bit(index)
            self.unique_visits += 1
    
    def get_unique_n_visited(self):
        return self.unique_visits
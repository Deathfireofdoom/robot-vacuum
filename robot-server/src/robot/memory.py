from src.models.location import Location


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
    
    def add_location(self, x: int, y: int):
        index = self._get_index(x, y)
        if not self.array.get_bit(index):
            self.array.set_bit(index)
            self.unique_visits += 1
    
    def get_unique_n_visited(self):
        return self.unique_visits

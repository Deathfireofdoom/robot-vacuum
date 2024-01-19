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
        # NOTE: Need to add some extra logic in this function to make it
        #       work with our grid, which is centered around 0. 

        # adjust coordinates
        # Ex. y = 0, then we lift it to 100 000 (center of the grid in the class)
        y_adjusted = y + self.width // 2 
        x_adjusted = x + self.height // 2

        # Here we calculate the "location"-pos in the 2d array
        # To make it easier we leave the adjusted part and do a small array, 3*3.
        # Ex. [0, 0, 0, | 0, 0, 0, | 0, 0, 0] - each pipe is a COLUMN, so first value is
        #    (0, 0), (0, 1), (0, 2)
        # Thats why we need to tage x * height to move to the correct "x"-value, then we
        # just "climb" to right y by adding y.
        return x_adjusted * self.height + y_adjusted

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
        return (x + self.width // 2) * self.width + (y + self.height // 2)
    
    def add_location(self, x: int, y: int):
        index = self._get_index(x, y)
        if not self.array.get_bit(index):
            self.array.set_bit(index)
            self.unique_visits += 1
    
    def get_unique_n_visited(self):
        return self.unique_visits

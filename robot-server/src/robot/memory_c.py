import ctypes


class BitMapMemory(ctypes.Structure):
    _fields_ = [
        ("unique_n_visited", ctypes.c_int)
    ]



class CMemoryWrapper():
    def __init__(self):
        self.lib = ctypes.CDLL("./src/robot/libbitmapmemory_performance.so")
        self.lib.get_unique_n_visited.restype = ctypes.c_int
        self.lib.create_bitmap_memory.restype = ctypes.POINTER(BitMapMemory)
        self.bmm = self.lib.create_bitmap_memory()

    def add_locations(self, x_start: int, y_start: int, x_end: int, y_end: int):
        self.lib.add_locations(self.bmm, x_start, y_start, x_end, y_end)

    def get_unique_n_visited(self, free_memory: bool=False):
        # Not sure if this was the best way to do it but need
        # to free memory somehow.
        n_visited = self.lib.get_unique_n_visited(self.bmm)
        if free_memory:
            self.lib.free_bitmap_memory
        return n_visited

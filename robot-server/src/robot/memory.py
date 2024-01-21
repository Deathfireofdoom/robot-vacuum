from bitarray import bitarray


class BitMapMemory:
    # NOTE: First version bitmap-memory, below I implemented a better version.
    #       Still leaving this one since it shoulds the concept without extra complexity.

    width = 200_001
    height = 200_001

    def __init__(self):
        self.array = bitarray(self.width * self.height)
        self.array.setall(0)
        self.unique_visits = 0

    def _get_index(self, x: int, y: int):
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


class SmartDynamicGridBitMapMemory:
    # NOTE: This is a more advanced implementation of the above bitmap-memory, it uses 
    #       subgrids to avoid rendering uncessary parts of the grid.
    #
    #       It also has method to know if it may have stepped over a subgrid boundry
    #       by calculating N-steps from nearest grid, and only check when the robot has
    #       taken N steps.
    #
    #       WARNING: This memory class only works for robots that moves contiounsly, i.e.
    #       new location is adjecent to the old one. No teleporting. There is no check for
    #       this though. 

    total_grid_height = 200_001
    total_grid_width = 200_001
    sub_grid_size = 500

    def __init__(self):
        self.unique_visited = 0
        self.grids = {}
        self._current_grid = None
        self._current_grid_bounds = None
        self._steps_from_potential_edge = 0

    def add_location(self, x: int, y: int):
        # Adjust coordinates
        x_adjusted = x + self.total_grid_width // 2
        y_adjusted = y + self.total_grid_height // 2

        # Check how many steps from the edge of a subgrid the robot are
        if self._steps_from_potential_edge <= 0:
            # The robot may have step over a edge
            if not self._is_within_current_grid(x_adjusted, y_adjusted):
                # The robot has stepped into a different grid
                # calculate new subgrid
                grid_pos = self._get_grid_index(x_adjusted, y_adjusted)

                # update current grid 
                self._update_current_grid(grid_pos)

                # set steps from potential edge - ex. if it turns 180 degree, it will leave 
                # the new subgrid.
                self._steps_from_potential_edge = 1
            else:
                # The robot is still in the same grid - calculate steps to nearest edge.
                self._steps_from_potential_edge = self._calculate_steps_from_nearest_edge(x_adjusted, y_adjusted)

        # Get location index in the sub-grid
        location_index = self._get_location_index_in_grid(x_adjusted, y_adjusted)

        # Check if we already visited it
        if not self.grids[self._current_grid][location_index]:
            self.grids[self._current_grid][location_index] = 1
            self.unique_visited += 1

        # adjust steps from potential edge
        self._steps_from_potential_edge -= 1

    def get_unique_n_visited(self):
        return self.unique_visited

    def _update_current_grid(self, grid_pos):
        # Update the current grid and its bounds
        self._current_grid = grid_pos
        self._current_grid_bounds = self._calculate_grid_bounds(grid_pos)

        # Grid never been visited, render the grid.
        if grid_pos not in self.grids:
            self.grids[grid_pos] = bitarray(self.sub_grid_size * self.sub_grid_size)
            self.grids[grid_pos].setall(0)

    def _is_within_current_grid(self, x: int, y: int):
        if self._current_grid_bounds is None:
            return False
        x_min, x_max, y_min, y_max = self._current_grid_bounds
        return x_min <= x < x_max and y_min <= y < y_max

    def _calculate_grid_bounds(self, grid_pos):
        x_min = grid_pos[0] * self.sub_grid_size
        x_max = x_min + self.sub_grid_size
        y_min = grid_pos[1] * self.sub_grid_size
        y_max = y_min + self.sub_grid_size
        return x_min, x_max, y_min, y_max

    def _calculate_steps_from_nearest_edge(self, x: int, y: int):
        # Retrieve the bounds of the current grid
        x_min, x_max, y_min, y_max = self._current_grid_bounds

        # Calculate the distance to each edge
        distance_to_left_edge = x - x_min
        distance_to_right_edge = x_max - x - 1
        distance_to_top_edge = y_max - y - 1
        distance_to_bottom_edge = y - y_min

        # Find the minimum distance to an edge
        min_distance_to_edge = min(
            distance_to_left_edge, distance_to_right_edge, 
            distance_to_top_edge, distance_to_bottom_edge
        )

        return min_distance_to_edge

    def _get_grid_index(self, x: int, y: int):
        grid_x = x // self.sub_grid_size
        grid_y = y // self.sub_grid_size
        return (grid_x, grid_y)

    def _get_location_index_in_grid(self, x: int, y: int):
        local_x = x % self.sub_grid_size
        local_y = y % self.sub_grid_size
        return local_x * self.sub_grid_size + local_y


# The below class is just a proof of concept, a "homemade" version of the 
# memory class above, to show that I understand the concepts, but due to 
# different limitations, I needed to use a opensource package that implements
# a perofmant bitarray in c.
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

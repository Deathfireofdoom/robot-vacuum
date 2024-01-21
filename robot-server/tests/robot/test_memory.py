from src.robot.memory import BitMapMemory, BitMapMemoryHomeMade, SmartDynamicGridBitMapMemory


def test_bitmap_memory_counts_only_unique_locations():
    # Arrange
    memory = BitMapMemory()
    locations = [(0, 0), (0, 1), (0, 0)]
    
    # Act
    for location in locations:
        memory.add_location(location[0], location[1])
    
    # Assert
    assert memory.get_unique_n_visited() == 2


def test_homemade_bitmap_memory_counts_only_unique_locations():
    # Arrage
    memory = BitMapMemoryHomeMade()
    locations = [(0, 0), (0, 1), (0, 0)]
    
    # Act
    for location in locations:
        memory.add_location(location[0], location[1])
    
    # Assert
    assert memory.get_unique_n_visited() == 2

# NOTE: This memory may be missing some tests due to time constraints.  
def test_smart_dynamic_memory_counts_only_unique_locations():
    # Arrange
    memory = SmartDynamicGridBitMapMemory()
    locations = [(0, 0), (0, 1), (0, 0)]
    
    # Act
    for location in locations:
        memory.add_location(location[0], location[1])
    
    # Assert
    assert memory.get_unique_n_visited() == 2

def test_smart_dynamic_memory_works_over_sub_grids():
    # Arrange
    memory = SmartDynamicGridBitMapMemory()
    locations = [(0, y) for y in range(800)] # Subgrid is 500, so should have new grid.
    first_location = locations.pop(0)
    memory.add_location(first_location[0], first_location[1])
    first_grid = memory._current_grid

    # Act
    for location in locations:
        memory.add_location(location[0], location[1])

    # Assert
    assert first_grid != memory._current_grid
    assert memory.get_unique_n_visited() == len(locations) + 1 # The pop

def test_smart_dynamic_memory_works_when_re_entering_sub_grid():
    # Arrange
    length = 800
    memory = SmartDynamicGridBitMapMemory()
    locations = [(0, y) for y in range(length)] # Subgrid is 500, so should have new grid.
    locations.append((1, length - 1)) # one to the side
    locations.extend([(1, y) for y in reversed(range(length))]) # Going back down
    
    first_location = locations.pop(0)
    memory.add_location(first_location[0], first_location[1])
    first_grid = memory._current_grid

    # Act
    for location in locations:
        memory.add_location(location[0], location[1])

    # Assert
    assert first_grid == memory._current_grid
    assert memory.get_unique_n_visited() == len(locations) + 1 # The pop

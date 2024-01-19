from src.robot.memory import BitMapMemory, BitMapMemoryHomeMade


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

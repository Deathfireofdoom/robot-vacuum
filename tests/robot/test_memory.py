from src.robot.memory import Memory
from src.models.location import Location


def test_memory_should_only_remember_unqiue_locations():
    # Arrange
    memory = Memory()
    input_locations = [Location(0, 0), Location(0, 0), Location(1, 1)]
    expected_locations = [Location(0, 0), Location(1, 1)]
    expected_locations_len = len(expected_locations)

    # Act
    for location in input_locations:
        memory.add_location(location=location)

    # Assert
    assert memory.get_unique_n_visited() == expected_locations_len
    for location in expected_locations:
        assert location in memory.visited

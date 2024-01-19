import pytest
from src.utils.bitarray.bitarray import BitArray


@pytest.fixture
def bitarray():
    return BitArray(8)

def test_bitarray_is_correct_size():
    bitarray = BitArray(32)
    assert len(bitarray.bits) == 1

    bitarray = BitArray(64)
    assert len(bitarray.bits) == 2

def test_bitarray_set_and_get_bit(bitarray):
    # Arrange
    index = 2
    
    # Act
    bitarray.set_bit(index)

    # Assert
    assert bitarray.get_bit(index) == 1

def test_bitarray_clear_bit(bitarray):
    # Arrange
    index = 2
    bitarray.set_bit(index)
    assert bitarray.get_bit(index) == 1

    # Act
    bitarray.clear_bit(index)

    # Assert
    assert bitarray.get_bit(index)
    
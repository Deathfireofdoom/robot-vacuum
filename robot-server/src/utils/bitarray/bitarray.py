import array

class BitArray:
    def __init__(self, size):
        num_ints = (size + 31) // 32
        self.bits = array.array('I', [0] * num_ints)

    def set_bit(self, index):
        if 0 <= index < len(self.bits) * 32:
            word_index = index // 32
            bit_offset = index % 32
            self.bits[word_index] |= (1 << bit_offset)

    def get_bit(self, index):
        if 0 <= index < len(self.bits) * 32:
            word_index = index // 32
            bit_offset = index % 32
            return (self.bits[word_index] >> bit_offset) & 1
        return 0

    def clear_bit(self, index):
        if 0 <= index < len(self.bits) * 32:
            word_index = index // 32
            bit_offset = index % 32
            self.bits[word_index] &= ~(1 << bit_offset)

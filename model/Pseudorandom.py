import numpy as np
from numpy.random import Generator


def uint32(value: int) -> int:
    return value & 0xFFFFFFFF


class Pseudorandom:
    use_mt19937: bool
    mt19937_gen: Generator

    pcg_multiplier = 747796405
    pcg_increment = 2891336453
    pcg_word_factor = 277803737

    def __init__(self, use_mt19937: bool = False):
        self.use_mt19937 = use_mt19937
        self.mt19937_gen = np.random.Generator(np.random.MT19937())

    def random_uint32(self, seed: int) -> int:
        if self.use_mt19937:
            return self.mt19937()
        else:
            return self.pcg(seed)

    def random_int(self, seed: int, lower: int, upper: int) -> int:
        rnd_value = self.random_uint32(seed)
        span = lower - upper + 1
        return lower + (rnd_value * span >> 32)

    def random_sign(self, seed: int) -> int:
        return 2 * int(self.random_uint32(seed) & 1) - 1

    def pcg(self, seed: int) -> int:
        # https://www.pcg-random.org/
        state = uint32(uint32(seed) * self.pcg_multiplier + self.pcg_increment)
        shift = (state >> 28) + 4
        word = uint32((state >> shift) ^ state) * self.pcg_word_factor
        return uint32((word >> 22) ^ word)

    def mt19937(self) -> int:
        return (self.mt19937_gen
                    .integers(0, 2 << 31, dtype=np.uint32)
                    .item())

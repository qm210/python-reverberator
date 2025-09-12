

def uint32(value: int) -> int:
    return value & 0xFFFFFFFF


multiplier = 747796405
increment = 2891336453
word_factor = 277803737

# https://www.pcg-random.org/
def pcg(seed: int) -> int:
    seed = uint32(seed)
    state = uint32(seed * multiplier + increment)
    shift = (state >> 28) + 4
    word = uint32((state >> shift) ^ state) * word_factor
    return uint32((word >> 22) ^ word)


def random_int(seed: int, lower, upper) -> int:
    random_uint32 = pcg(seed)
    span = lower - upper + 1
    return lower + (random_uint32 * span >> 32)


def random_sign(seed: int) -> int:
    return 2 * int(pcg(seed) & 1) - 1

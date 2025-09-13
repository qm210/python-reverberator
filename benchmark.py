from contextlib import contextmanager
from time import perf_counter

from model.Params import Params
from model.Reverberator import Reverberator
from model.Wave import Wave


class Benchmark:
    def __init__(self, times: int = 1, prefix: str = "", suffix: str = ""):
        self.times = times
        self.prefix = prefix
        self.suffix = suffix
        self._index = 0

    def __enter__(self):
        self._index = 0
        self.started_at = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        delta_sec = perf_counter() - self.started_at
        avg_str = ""
        if self.times > 1:
            delta_sec /= self.times
            avg_str = "on average "
        print(f"{self.prefix}execution {avg_str}{delta_sec:.3E} seconds {self.suffix}")

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < self.times:
            self._index += 1
            return self._index
        else:
            raise StopIteration


@contextmanager
def log_time(prefix: str = "", suffix: str = ""):
    start = perf_counter()
    try:
        yield
    finally:
        end = perf_counter()
        print(f"{prefix}execution {end - start} seconds {suffix}")


def benchmark_mersenne_twister_vs_pcg():
    params = Params(dont_play=True, use_mt19937=False)
    wave = Wave(params.in_file)
    with Benchmark(prefix="[PCG] ", times=1000) as loop:
        reverb = Reverberator(params, wave.samplerate)
        for _ in loop:
            reverb.recalc_echoes()

    params = Params(dont_play=True, use_mt19937=True)
    with Benchmark(prefix="[MT]  ", times=1000) as loop:
        reverb = Reverberator(params, wave.samplerate)
        for _ in loop:
            reverb.recalc_echoes()


if __name__ == "__main__":
    benchmark_mersenne_twister_vs_pcg()

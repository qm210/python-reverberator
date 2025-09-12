import numpy as np
import math

from dataclasses import dataclass
from typing import List, Self, Callable

from model.Wave import Wave
from model.pseudorandom import random_sign, random_int


@dataclass
class Echo:
    pos: int = 0
    sign: int = 0
    amplitude: float = 0

    @classmethod
    def random(cls, step: int, spacing: int) -> Self:
        pos = step * spacing + random_int(step, 1, spacing)
        sign = random_sign(step)
        amplitude = 0
        return cls(pos, sign, amplitude)

    def evaluated(self, func: Callable[[int], float]) -> Self:
        self.amplitude = func(self.pos) * self.sign
        return self


@dataclass
class Params:
    rt60_seconds: float
    mix_amount: float = 0.5
    loop_seconds: float = 1.0
    n_echoes: int = 1000


class Reverberator:
    # working state
    pos_read: int
    pos_fb: int
    data: List[float]
    echoes: List[Echo]

    # derived params
    rt60_position: float
    echo_spacing: int
    loop_samples: int
    loop_capacity: int
    n_echoes: int

    # reference
    _samplerate: int
    _params: Params

    def __init__(self, params: Params, samplerate: int):
        self.samplerate = samplerate
        self._params = params
        self.rt60_position = self.samplerate * params.rt60_seconds
        self.echo_spacing = int(samplerate * params.loop_seconds / params.n_echoes)
        self.loop_samples = self.echo_spacing * params.n_echoes
        self.echoes = [
            Echo.random(step, self.echo_spacing)
                .evaluated(self.evaluate_decay)
            for step in range(params.n_echoes)
        ]

        self.pos_read = 0
        self.pos_fb = self.loop_samples
        self.data = [0 for _ in range(2 * self.loop_samples)]

    def evaluate_decay(self, sample: int) -> float:
        # (0.001) ^ (sample/rt60) = 10^(-3 * sample/rt60)
        return math.exp(-3 * sample/self.rt60_position * math.log(10))

    def apply(self, wave: Wave):
        # first, a simple amp
        gain = 1.0
        wave.data *= gain
        wave.data = np.clip(gain * wave.data, -1., 1.)

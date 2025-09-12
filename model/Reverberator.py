import numpy as np
import numpy.typing as npt
import math

from dataclasses import dataclass
from typing import List, Self, Callable, Optional

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
    gain: float = 1.0
    loop_seconds: float = 1.0
    n_echoes: int = 1000


class Reverberator:
    # working state
    pos_read: int
    pos_fb: int
    data: List[float]
    output: Optional[npt.NDArray[np.float32]]
    echoes: List[Echo]

    # derived params
    rt60_position: float
    echo_spacing: int
    loop_samples: int
    loop_capacity: int
    feedback_gain: float

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
        self.feedback_gain = self.evaluate_decay(self.loop_samples)

        self.pos_read = 0
        self.pos_fb = self.loop_samples
        self.data = [0 for _ in range(2 * self.loop_samples)]
        self.output = None

    def evaluate_decay(self, sample: int) -> float:
        # (0.001) ^ (sample/rt60) = 10^(-3 * sample/rt60)
        return math.exp(-3 * sample/self.rt60_position * math.log(10))

    def apply(self, wave: Wave):
        if wave.channels != 1:
            raise NotImplementedError("did only implement MONO for now")

        overall_gain = self._params.gain
        size = len(self.data)

        for echo in self.echoes:
            gain = echo.amplitude * overall_gain
            pos = (self.pos_read + echo.pos) % size
            for input in wave.data:
                self.data[pos] += gain * input
                pos = (pos + 1) % size

        self.output = wave.zeros()
        for s in range(len(self.output)):
            # move the data so we don't have it anymore
            self.output[s] = self.data[self.pos_read]
            self.data[self.pos_read] = 0
            self.data[self.pos_fb] += self.output[s] * self.feedback_gain

            self.pos_read = (self.pos_read + 1) % size
            self.pos_fb = (self.pos_fb + 1) % size

        wave.data = self.output

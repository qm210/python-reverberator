import numpy as np
import numpy.typing as npt
import math

from dataclasses import dataclass
from typing import List, Self, Callable, Optional, Any

from model.Params import Params
from model.Pseudorandom import Pseudorandom
from model.Wave import Wave


@dataclass
class Echo:
    pos: int = 0
    sign: int = 0
    amplitude: float = 0

    def amplitude_by(self, func: Callable[[int], float]) -> Self:
        self.amplitude = func(self.pos) * self.sign
        return self


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
    overall_gain: float
    feedback_gain: float

    # reference
    _samplerate: int
    _params: Params

    def __init__(self, params: Params, samplerate: int):
        self.samplerate = samplerate
        self._params = params
        self.rt60_position = self.samplerate * params.rt60_sec

        self.echo_spacing = int(samplerate * params.loop_sec / params.n_echoes)
        self.loop_samples = self.echo_spacing * params.n_echoes

        self.echoes = [Echo() for _ in range(params.n_echoes)]
        self.recalc_echoes()

        self.overall_gain = params.pregain * 90. / params.n_echoes
        self.feedback_gain = self.evaluate_decay(self.loop_samples)

        self.pos_read = 0
        self.pos_fb = self.loop_samples
        self.data = []
        self.output = None

    def recalc_echoes(self):
        rng = Pseudorandom(use_mt19937=self._params.use_mt19937)
        for i, echo in enumerate(self.echoes):
            echo.pos = i * self.echo_spacing + rng.random_int(1, self.echo_spacing)
            echo.sign = rng.random_sign()
            echo.amplitude_by(self.evaluate_decay)

    def evaluate_decay(self, sample: int) -> float:
        # (0.001) ^ (sample/rt60) = 10^(-3 * sample/rt60)
        return math.exp(-3 * sample/self.rt60_position * math.log(10))

    def mix(self, dry: Any, wet: Any):
        return (1 - self._params.mix_amount) * dry + self._params.mix_amount * wet

    def apply(self, wave: Wave):
        size = 2 * self.loop_samples
        if wave.is_mono:
            self.evaluate_mono(wave, size)
        else:
            self.evaluate_numpyed(wave, size)
        wave.data = self.mix(wave.data, self.output)

    def evaluate_mono(self, wave: Wave, datasize: int):
        self.data = wave.zeros(length=datasize)
        for echo in self.echoes:
            gain = echo.amplitude * self.overall_gain
            pos = (self.pos_read + echo.pos) % datasize
            for input in wave.data:
                self.data[pos] += gain * input
                pos = (pos + 1) % datasize

        self.output = wave.zeros()
        for s in range(len(self.output)):
            self.output[s] = self.data[self.pos_read]
            self.data[self.pos_read] = 0
            self.pos_read = (self.pos_read + 1) % datasize
            self.data[self.pos_fb] += self.output[s] * self.feedback_gain
            self.pos_fb = (self.pos_fb + 1) % datasize

    def evaluate_numpyed(self, wave: Wave, datasize: int):
        self.data = wave.zeros(length=datasize)
        for echo in self.echoes:
            gain = echo.amplitude * self.overall_gain
            pos = (self.pos_read + echo.pos) % datasize
            shifted = np.roll(wave.data, pos)
            self.data[:datasize] += gain * shifted[:datasize]

        self.output = wave.zeros()
        idx_read = (np.arange(len(self.output)) + self.pos_read) % datasize
        idx_fb = (np.arange(len(self.output)) + self.pos_fb) % datasize
        self.output[:] = self.data[idx_read]
        self.data[idx_read] = 0
        self.data[idx_fb] += self.output * self.feedback_gain

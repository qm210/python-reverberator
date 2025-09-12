from dataclasses import dataclass
from typing import Any

import numpy as np
import soundfile as sf
from numpy import typing as npt


@dataclass
class Wave:
    filename: str
    original: npt.NDArray[np.float32]
    data: npt.NDArray[np.float32]
    samplerate: int
    channels: int

    def __init__(self, filename: str):
        self.filename = filename
        self.original, self.samplerate = \
            sf.read(filename, dtype="float32")
        self.channels = self.read_channels(self.original)
        self.data = np.copy(self.original)

    @property
    def frames(self):
        return self.data.shape[0]

    @property
    def seconds(self):
        return round(self.frames / self.samplerate, 3)

    def as_int16_array(self) -> npt.NDArray[np.int16]:
        return np.clip(self.data * 32767, -32768, 32767).astype(np.int16)

    @staticmethod
    def read_channels(nparray: npt.NDArray[Any]):
        return 1 if nparray.ndim == 1 else nparray.shape[1]

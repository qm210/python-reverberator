from dataclasses import dataclass
from typing import Any, Tuple

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
    original_range: Tuple[float, float]

    def __init__(self, filename: str):
        self.filename = filename
        self.original, self.samplerate = \
            sf.read(filename, dtype="float32")
        self.channels = self.read_channels(self.original)
        self.original_range = np.min(self.original), np.max(self.original)
        self.data = np.copy(self.original)

    @property
    def frames(self):
        return self.data.shape[0]

    @property
    def seconds(self):
        return round(self.frames / self.samplerate, 3)

    @property
    def is_mono(self):
        return self.channels == 1

    @staticmethod
    def read_channels(nparray: npt.NDArray[Any]):
        return 1 if nparray.ndim == 1 else nparray.shape[1]

    def write(self, filename: str):
        sf.write(filename, self.data, self.samplerate)

    def extend_by_factor(self, factor: float):
        new_frames = int(self.frames * factor)
        if self.is_mono:
            resized = np.zeros(new_frames,
                               dtype=self.data.dtype)
            resized[:self.frames] = self.data
        else:
            resized = np.zeros((new_frames, self.channels),
                               dtype=self.data.dtype)
            resized[:self.frames, :] = self.data
        self.data = resized

    def as_int16_array(self) -> npt.NDArray[np.int16]:
        return (np.clip(self.data * 32767, -32768, 32767)
                .astype(np.int16))

    def zeros(self, length: int = None):
        if length is None:
            return np.zeros_like(self.data)
        else:
            return np.zeros((length,) + self.data.shape[1:],
                            dtype=self.data.dtype)

import time

import keyboard
import numpy as np
import simpleaudio as sa
import sounddevice as sd

from Wave import Wave


def apply_reverb(wave: Wave):
    # first, a simple amp
    gain = 1.0
    wave.data *= gain
    wave.data = np.clip(gain * wave.data, -1., 1.)


def play(wave: Wave):
    int_data = wave.as_int16_array()
    bytes_per_int16 = 2
    player = sa.play_buffer(int_data,
                            wave.channels,
                            bytes_per_int16,
                            wave.samplerate)
    while True:
        if keyboard.read_key(suppress=False):
            player.stop()
            print("Keypress = Cancel Playback.")
            break
        if not player.is_playing():
            print("Playback ended by itself.")
            break
        time.sleep(0.1)


def print_device_info():
    default_out = sd.default.device[1]
    device_info = sd.query_devices(default_out)
    print(default_out, device_info)


if __name__ == "__main__":
    print_device_info()
    input = "gnhnhahahaha.wav"
    print("Loading", input)
    wave = Wave(input)
    print("Hello Reverberator.")
    apply_reverb(wave)
    print("Now play seconds:", wave.seconds)
    play(wave)
    print("Wirsing.")

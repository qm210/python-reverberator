import time
from pprint import pprint

import keyboard
import simpleaudio as sa
import sounddevice as sd

from model.Reverberator import Reverberator, Params
from model.Wave import Wave


def play(wave: Wave):
    print("Now play", wave.seconds, "seconds.")
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
    print("Sound Output Device:")
    pprint(device_info)


def load_and_reverberate(filename: str, params: Params) -> Wave:
    print("Loading", filename)
    wave = Wave(filename)
    wave.extend_by_factor(2)
    print("Wave has values in", wave.original_range)
    reverberator = Reverberator(params, wave.samplerate)
    print("Hello Reverberator.", params)
    reverberator.apply(wave)
    return wave


if __name__ == "__main__":
    print_device_info()
    input_file = "gnhnhahahaha.wav."
    some_params = Params(rt60_seconds = 2.10,
                    mix_amount = 0.5,
                    loop_seconds = 1.0,
                    n_echoes = 10)
    the_wave = load_and_reverberate(input_file, some_params)
    play(the_wave)
    print("Wirsing.")

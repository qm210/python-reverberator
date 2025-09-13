import time

import keyboard
import simpleaudio as sa
import sounddevice as sd

from model.Wave import Wave


def play(wave: Wave):
    print("Now play", wave.seconds, "seconds.")
    int_data = wave.as_int16_array()
    bytes_per_int16 = 2
    player = sa.play_buffer(int_data,
                            wave.channels,
                            bytes_per_int16,
                            wave.samplerate)
    while player.is_playing():
        if keyboard.read_key(suppress=False):
            player.stop()
            print("Cancelled Playback.")
            break
        time.sleep(0.1)
    player.stop()
    time.sleep(0.5)


def print_device_info():
    default_out = sd.default.device[1]
    info = sd.query_devices(default_out)
    print(
        "Sound Output Device:", info['name'],
        "- Max Output Channels", info['max_output_channels']
    )

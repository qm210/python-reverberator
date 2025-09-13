import time
from pprint import pprint

from audio import play, print_device_info
from model.Reverberator import Reverberator
from model.Params import Params
from model.Wave import Wave


def load_and_reverberate(params: Params) -> Wave:
    print("Loading", params.in_file)
    wave = Wave(params.in_file)
    print(f"Wave has originally {wave.seconds} seconds and values in {wave.original_range}. Params:")
    params.maybe_adjust(wave)
    pprint(params)

    reverberator = Reverberator(params, wave.samplerate)
    print("Reverberator spawned, now doing its job...")
    t0 = time.perf_counter()
    reverberator.apply(wave)
    t1 = time.perf_counter()
    print(f"Took {t1-t0:.3f} seconds for a {params.output_sec} sec. sample.")
    return wave


if __name__ == "__main__":
    args = Params.from_cli(in_file="shortdudel.wav")
    sample = load_and_reverberate(args)
    sample.write(args.out_file)
    if not args.dont_play:
        print_device_info()
        play(sample)
    print("Wirsing.")

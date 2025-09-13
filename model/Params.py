import argparse

from dataclasses import dataclass, replace
from typing import Optional

from model.Wave import Wave


@dataclass
class Params:
    in_file: str = "gnhnhahahaha.wav"
    out_file: str = "output.wav"
    dont_play: bool = False
    rt60_sec: float = 2.1
    mix_amount: float = 0.5
    pregain: float = 0.95
    n_echoes: int = 200
    use_mt19937: bool = False
    output_sec: Optional[float] = None
    loop_sec: float = 1.0
    auto_loop_sec: float = False

    def maybe_adjust(self, wave: Wave) -> None:
        if self.auto_loop_sec:
            self.loop_sec = self.output_sec or wave.seconds
        if self.output_sec is not None:
            wave.extend_to(self.output_sec)
        else:
            self.output_sec = wave.seconds

    @classmethod
    def from_cli(cls, **overwrites):
        parser = argparse.ArgumentParser()
        default = cls()
        parser.add_argument(
            "-i", "--input",
            help="input .wav path to process",
            default=default.in_file,
        )
        parser.add_argument(
            "-o", "--output",
            help="output .wav path to write",
            default=default.out_file,
        )
        parser.add_argument(
            "-d", "--decay",
            help="decay time in seconds (should be ~ RT60, i.e. when levels have sunk to 60 dB of initial level)",
            type=float,
            default=default.rt60_sec,
        )
        parser.add_argument(
            "-m", "--mix",
            help="how much of the reverb (0 = dry, 1 = wet)",
            type=float,
            default=default.mix_amount,
        )
        parser.add_argument(
            "-n", "--echoes",
            help="the amount of sample points (will be somewhat randomized), i.e. \"number of echoes\"",
            type=int,
            default=default.n_echoes,
        )
        parser.add_argument(
            "-g", "--pregain",
            help="scale the input by that factor beforehand",
            type=float,
            default=default.pregain,
        )
        parser.add_argument(
            "--mt-random",
            help="Use Mersenne-Twister 19937 for the random numbers instead of simple PCG",
            action="store_true",
        )
        parser.add_argument(
            "--loop-sec",
            help="how long the interal loop is, should not be much smaller than the input",
            type=float,
            default=None,
        )
        parser.add_argument(
            "--auto-loop",
            help="fix the loop seconds to the output seconds, might be wasteful but less sucking",
            action="store_true"
        )
        parser.add_argument(
            "--out-sec",
            help="overwrite the seconds of the output, otherwise the original + \"--loop-sec\"",
            type=float,
            default=None,
        )
        parser.add_argument(
            "-q", "--quiet",
            help="whether not to actually play the processed wave",
            action="store_true",
        )
        args = parser.parse_args()
        result = cls(
            in_file=args.input,
            out_file=args.output,
            rt60_sec=args.decay,
            mix_amount=args.mix,
            pregain=args.pregain,
            n_echoes=args.echoes,
            use_mt19937=args.mt_random,
            output_sec=args.out_sec,
            loop_sec=args.loop_sec,
            auto_loop_sec=args.loop_sec is None or args.auto_loop,
            dont_play=args.quiet,
        )
        return replace(result, **overwrites)

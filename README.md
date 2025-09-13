## how to use

Start with `uv` via
```
uv run main.py -i <input.wav> [...params...]
```
If you don't have `uv`, you can plainly call python
```
# linux
./.venv/Scripts/python main.py shortdudel.wav bla.wav

# windows
.\.venv\Scripts\python.exe main.py shortdudel.wav bla.wav
```

For CLI parameters check `Params.py`, it should support
```
usage: main.py [-h] [-i INPUT] [-o OUTPUT] [-d DECAY] [-m MIX] [-n ECHOES] [-g PREGAIN] [--mt-random]
               [--loop-sec LOOP_SEC] [--auto-loop] [--out-sec OUT_SEC] [-q]

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     input .wav path to process
  -o, --output OUTPUT   output .wav path to write
  -d, --decay DECAY     decay time in seconds (should be ~ RT60, i.e. when levels have sunk to 60 dB of initial level)
  -m, --mix MIX         how much of the reverb (0 = dry, 1 = wet)
  -n, --echoes ECHOES   the amount of sample points (will be somewhat randomized), i.e. "number of echoes"
  -g, --pregain PREGAIN
                        scale the input by that factor beforehand
  --mt-random           Use Mersenne-Twister 19937 for the random numbers instead of simple PCG
  --loop-sec LOOP_SEC   how long the interal loop is, should not be much smaller than the input
  --auto-loop           fix the loop seconds to the output seconds, might be wasteful but less sucking
  --out-sec OUT_SEC     overwrite the seconds of the output, otherwise the original + "--loop-sec"
  -q, --quiet           whether not to actually play the processed wave
```

## have fun &ndash; recommends QM

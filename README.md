## how to use

Start with `uv` via
```
uv run main.py <input.wav> <output.wav>
```
Or without `uv` plainly
```
# linux
./.venv/Scripts/python main.py shortdudel.wav bla.wav

# windows
.\.venv\Scripts\python.exe main.py shortdudel.wav bla.wav
```

And in `main.py` you can play with the parameters

```
Params(
    rt60_seconds = 2.10,
    mix_amount = 0.7,
    loop_seconds = 1.0,
    n_echoes = 100,
    gain = 0.85,
    use_mt19937=False,
    output_seconds=3,
)
```

## have fun -- qm

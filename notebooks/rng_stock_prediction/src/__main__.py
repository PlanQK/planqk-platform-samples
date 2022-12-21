from .program import run
import json

with open("input/rng_4bits.json") as file:
    inp = json.load(file)

data = inp["data"]
params = inp["params"]

if __name__ == "__main__":
    run(data, params)

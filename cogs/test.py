import json
import time

with open("data/hendex.json", "r") as f:
    file = json.load(f)

file[str(time.time())] = "sarsrattss"

with open("data/hendex.json", "w") as f:
    json.dump(file, f)
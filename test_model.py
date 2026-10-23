
import json
import subprocess
import sys
from pathlib import Path

subprocess.run(
    [sys.executable, "train.py"],
    check=True
)

assert Path("model.json").exists()

with open("model.json") as file:
    model = json.load(file)

assert model["slope"] > 0
assert abs(model["slope"] - 10) < 0.001

prediction = model["slope"] * 6 + model["intercept"]
assert abs(prediction - 70) < 0.001

print("PASS: ML model training and prediction tests passed!")


import json
import math
from datetime import datetime, timezone
from pathlib import Path

required_files = [
    "model.json",
    "model_version.json",
    "metrics.json",
    "experiment_report.json",
]

for filename in required_files:
    if not Path(filename).is_file():
        raise FileNotFoundError(f"Required release file missing: {filename}")


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


model = load_json("model.json")
metadata = load_json("model_version.json")
metrics = load_json("metrics.json")
report = load_json("experiment_report.json")

for key in ("slope", "intercept"):
    if key not in model or not isinstance(model[key], (int, float)):
        raise ValueError(f"Invalid model parameter: {key}")
    if not math.isfinite(model[key]):
        raise ValueError(f"Non-finite model parameter: {key}")

for key in ("model_name", "version", "algorithm"):
    if not metadata.get(key):
        raise ValueError(f"Missing model metadata: {key}")

for key in ("mae", "mse", "r2"):
    if key not in metrics:
        raise ValueError(f"Missing model metric: {key}")
    if not isinstance(metrics[key], (int, float)):
        raise ValueError(f"Invalid model metric: {key}")
    if not math.isfinite(metrics[key]):
        raise ValueError(f"Non-finite model metric: {key}")

if metrics["mae"] > 5:
    raise ValueError("Release rejected: MAE exceeds 5")

if metrics["mse"] < 0:
    raise ValueError("Release rejected: MSE cannot be negative")

if not 0.90 <= metrics["r2"] <= 1:
    raise ValueError("Release rejected: R2 must be between 0.90 and 1")

if not report.get("best_model_version"):
    raise ValueError("Experiment report has no selected model version")

manifest = {
    "release_status": "APPROVED",
    "model_name": metadata["model_name"],
    "model_version": metadata["version"],
    "algorithm": metadata["algorithm"],
    "metrics": metrics,
    "validated_at": datetime.now(timezone.utc).isoformat(),
}

with open("release_manifest.json", "w", encoding="utf-8") as file:
    json.dump(manifest, file, indent=2)
    file.write("\n")

print("RELEASE APPROVED")
print(json.dumps(manifest, indent=2))
print("Release manifest saved to release_manifest.json")

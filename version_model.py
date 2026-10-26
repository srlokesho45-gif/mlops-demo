
import json
from datetime import datetime, timezone
from pathlib import Path

MODEL_FILE = Path("model.json")
VERSION_FILE = Path("model_version.json")
HISTORY_FILE = Path("model_versions.jsonl")


def create_version():
    if not MODEL_FILE.exists():
        raise FileNotFoundError("model.json not found. Run train.py first.")

    with MODEL_FILE.open(encoding="utf-8") as file:
        model = json.load(file)

    for key in ("slope", "intercept"):
        if key not in model:
            raise ValueError(f"Missing model parameter: {key}")

    previous_version = "0.0"
    if VERSION_FILE.exists():
        with VERSION_FILE.open(encoding="utf-8") as file:
            previous = json.load(file)
        previous_version = previous.get("version", "0.0")

    major, minor = map(int, previous_version.split("."))
    new_version = f"{major}.{minor + 1}"

    metadata = {
        "model_name": "student-marks-predictor",
        "version": new_version,
        "algorithm": "Linear Regression",
        "slope": model["slope"],
        "intercept": model["intercept"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with VERSION_FILE.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)
        file.write("\n")

    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(metadata) + "\n")

    print(f"Model version created: {new_version}")
    print(f"Model metadata saved to: {VERSION_FILE}")
    print(f"Version history saved to: {HISTORY_FILE}")


if __name__ == "__main__":
    create_version()

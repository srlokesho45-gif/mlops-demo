
import json
import math
from datetime import datetime, timezone

actual = [20, 30, 40, 50, 60]
hours = [1, 2, 3, 4, 5]

with open("model.json", encoding="utf-8") as file:
    model = json.load(file)

slope = model["slope"]
intercept = model["intercept"]
predicted = [slope * hour + intercept for hour in hours]

mae = sum(
    abs(real - pred) for real, pred in zip(actual, predicted)
) / len(actual)

mse = sum(
    (real - pred) ** 2 for real, pred in zip(actual, predicted)
) / len(actual)

mean_actual = sum(actual) / len(actual)
total_variation = sum((real - mean_actual) ** 2 for real in actual)
residual_variation = sum(
    (real - pred) ** 2 for real, pred in zip(actual, predicted)
)

r2 = (
    1 - residual_variation / total_variation
    if total_variation != 0
    else 0.0
)

metrics = {
    "mae": round(mae, 4),
    "mse": round(mse, 4),
    "r2": round(r2, 4),
}
if metrics["mae"] > 5:
    raise ValueError("Model failed: MAE is greater than 5")

if metrics["r2"] < 0.90:
    raise ValueError("Model failed: R2 is below 0.90")

print("Model quality gate passed!")

with open("metrics.json", "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=2)
    file.write("\n")

experiment = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "model_version": "1.0",
    "algorithm": "Linear Regression",
    "metrics": metrics,
}

with open("experiments.jsonl", "a", encoding="utf-8") as file:
    file.write(json.dumps(experiment) + "\n")

print("Model evaluation completed!")
print(json.dumps(metrics, indent=2))
print("Experiment recorded in experiments.jsonl")

if not all(math.isfinite(value) for value in metrics.values()):
    raise ValueError("Model metrics contain invalid numbers")


import json
from pathlib import Path

history_file = Path("experiments.jsonl")
report_file = Path("experiment_report.json")

if not history_file.exists():
    raise FileNotFoundError("experiments.jsonl not found")

experiments = []

with history_file.open(encoding="utf-8") as file:
    for line in file:
        if line.strip():
            experiments.append(json.loads(line))

if not experiments:
    raise ValueError("No experiments found")

for experiment in experiments:
    metrics = experiment["metrics"]
    print(
        f"Version: {experiment['model_version']} | "
        f"MAE: {metrics['mae']} | "
        f"MSE: {metrics['mse']} | "
        f"R2: {metrics['r2']}"
    )

best_model = min(
    experiments,
    key=lambda experiment: experiment["metrics"]["mae"],
)

report = {
    "total_experiments": len(experiments),
    "best_model_version": best_model["model_version"],
    "best_metrics": best_model["metrics"],
    "selection_criteria": "Lowest MAE",
}

with report_file.open("w", encoding="utf-8") as file:
    json.dump(report, file, indent=2)
    file.write("\n")

print("\nBest experiment selected using the lowest MAE.")
print(json.dumps(report, indent=2))
print(f"\nReport saved to: {report_file}")

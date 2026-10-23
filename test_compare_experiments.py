
import json
import subprocess
import sys
import unittest
from pathlib import Path


class TestExperimentComparison(unittest.TestCase):
    def test_comparison_generates_report(self):
        subprocess.run(
            [sys.executable, "compare_experiments.py"],
            check=True,
            capture_output=True,
            text=True,
        )

        report_path = Path("experiment_report.json")
        self.assertTrue(report_path.exists())

        with report_path.open(encoding="utf-8") as file:
            report = json.load(file)

        self.assertGreater(report["total_experiments"], 0)
        self.assertIn("best_model_version", report)
        self.assertIn("mae", report["best_metrics"])
        self.assertIn("mse", report["best_metrics"])
        self.assertIn("r2", report["best_metrics"])


if __name__ == "__main__":
    unittest.main()


import json
import unittest
from pathlib import Path


class TestModelEvaluation(unittest.TestCase):
    def test_metrics_are_valid(self):
        self.assertTrue(Path("metrics.json").exists())

        with open("metrics.json", encoding="utf-8") as file:
            metrics = json.load(file)

        self.assertIn("mae", metrics)
        self.assertIn("mse", metrics)
        self.assertIn("r2", metrics)

        self.assertGreaterEqual(metrics["mae"], 0)
        self.assertGreaterEqual(metrics["mse"], 0)
        self.assertLessEqual(metrics["r2"], 1)
        self.assertGreaterEqual(metrics["r2"], 0)

    def test_experiment_was_recorded(self):
        self.assertTrue(Path("experiments.jsonl").exists())

        with open("experiments.jsonl", encoding="utf-8") as file:
            records = [line for line in file if line.strip()]

        self.assertGreater(len(records), 0)

        experiment = json.loads(records[-1])
        self.assertEqual(experiment["model_version"], "1.0")
        self.assertIn("metrics", experiment)


if __name__ == "__main__":
    unittest.main()

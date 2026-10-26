
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import version_model


class TestModelVersioning(unittest.TestCase):
    def test_version_increments_and_history_is_appended(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            model_file = folder / "model.json"
            version_file = folder / "model_version.json"
            history_file = folder / "model_versions.jsonl"

            model_file.write_text(
                json.dumps({"slope": 10.0, "intercept": 10.0}),
                encoding="utf-8",
            )
            version_file.write_text(
                json.dumps({"version": "1.0"}),
                encoding="utf-8",
            )

            with (
                patch.object(version_model, "MODEL_FILE", model_file),
                patch.object(version_model, "VERSION_FILE", version_file),
                patch.object(version_model, "HISTORY_FILE", history_file),
            ):
                version_model.create_version()
                version_model.create_version()

            saved = json.loads(version_file.read_text(encoding="utf-8"))
            history = history_file.read_text(encoding="utf-8").splitlines()

            self.assertEqual(saved["version"], "1.2")
            self.assertEqual(len(history), 2)
            self.assertEqual(json.loads(history[0])["version"], "1.1")
            self.assertEqual(json.loads(history[1])["version"], "1.2")


if __name__ == "__main__":
    unittest.main()

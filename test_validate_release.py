
import json
import subprocess
import sys
import unittest
from pathlib import Path


class TestReleaseValidation(unittest.TestCase):
    def test_release_validation_generates_manifest(self):
        result = subprocess.run(
            [sys.executable, "validate_release.py"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout + result.stderr,
        )

        manifest_path = Path("release_manifest.json")
        self.assertTrue(manifest_path.is_file())

        with manifest_path.open(encoding="utf-8") as file:
            manifest = json.load(file)

        self.assertEqual(manifest["release_status"], "APPROVED")
        self.assertIn("model_version", manifest)
        self.assertIn("metrics", manifest)


if __name__ == "__main__":
    unittest.main()


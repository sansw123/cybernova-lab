from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cybernova.progress import add_topic, load_progress


class ProgressTests(unittest.TestCase):
    def test_add_and_load_topic(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.json"
            with patch("cybernova.progress.date") as fake_date:
                fake_date.today.return_value.isoformat.return_value = "2026-08-26"
                item = add_topic("  Linux   permissions  ", path)
            self.assertEqual(item, {"topic": "Linux permissions", "date": "2026-08-26"})
            self.assertEqual(load_progress(path)["topics"], [item])

    def test_rejects_empty_topic(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.json"
            with self.assertRaises(ValueError):
                add_topic("   ", path)


if __name__ == "__main__":
    unittest.main()


from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from cybernova.cli import main


class CliTests(unittest.TestCase):
    def test_hash_text_command(self):
        output = StringIO()
        with redirect_stdout(output):
            status = main(["hash", "--text", "abc"])
        self.assertEqual(status, 0)
        self.assertEqual(
            output.getvalue().strip(),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )

    def test_missing_file_is_friendly_error(self):
        output = StringIO()
        with redirect_stderr(output):
            status = main(["hash", "--file", "definitely-not-here.txt"])
        self.assertEqual(status, 2)
        self.assertIn("Error:", output.getvalue())

    def test_integrity_command_reports_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "watched"
            root.mkdir()
            sample = root / "sample.txt"
            sample.write_text("one", encoding="utf-8")
            manifest = Path(directory) / "manifest.json"
            with redirect_stdout(StringIO()):
                created = main(
                    ["integrity", "create", str(root), "--manifest", str(manifest)]
                )
            sample.write_text("two", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                checked = main(
                    ["integrity", "check", str(root), "--manifest", str(manifest)]
                )
            self.assertEqual(created, 0)
            self.assertEqual(checked, 1)
            self.assertIn("Modified sample.txt", output.getvalue())


if __name__ == "__main__":
    unittest.main()


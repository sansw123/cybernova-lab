import hashlib
from pathlib import Path
import tempfile
import unittest

from cybernova.hashing import hash_file, hash_text


class HashingTests(unittest.TestCase):
    def test_hash_text_matches_hashlib(self):
        expected = hashlib.sha256(b"hello cyber world").hexdigest()
        self.assertEqual(hash_text("hello cyber world"), expected)

    def test_hash_file_matches_hashlib(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            content = b"CyberNova\x00Lab" * 10_000
            path.write_bytes(content)
            self.assertEqual(hash_file(path), hashlib.sha256(content).hexdigest())


if __name__ == "__main__":
    unittest.main()


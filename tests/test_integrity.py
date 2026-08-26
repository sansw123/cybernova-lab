from pathlib import Path
import tempfile
import unittest

from cybernova.integrity import check_manifest, create_manifest


class IntegrityTests(unittest.TestCase):
    def test_detects_added_removed_and_modified_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "watched"
            root.mkdir()
            (root / "keep.txt").write_text("version one", encoding="utf-8")
            (root / "remove.txt").write_text("temporary", encoding="utf-8")
            manifest = Path(directory) / "manifest.json"

            self.assertEqual(create_manifest(root, manifest), 2)
            self.assertTrue(check_manifest(root, manifest).clean)

            (root / "keep.txt").write_text("version two", encoding="utf-8")
            (root / "remove.txt").unlink()
            (root / "new.txt").write_text("new", encoding="utf-8")
            result = check_manifest(root, manifest)

            self.assertEqual(result.added, ("new.txt",))
            self.assertEqual(result.removed, ("remove.txt",))
            self.assertEqual(result.modified, ("keep.txt",))
            self.assertFalse(result.clean)

    def test_ignores_git_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "watched"
            git_dir = root / ".git"
            git_dir.mkdir(parents=True)
            (git_dir / "index").write_text("changes often", encoding="utf-8")
            (root / "README.md").write_text("hello", encoding="utf-8")
            manifest = Path(directory) / "manifest.json"
            self.assertEqual(create_manifest(root, manifest), 1)


if __name__ == "__main__":
    unittest.main()


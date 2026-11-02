import os
import tempfile
import unittest
from pathlib import Path

from sandboxed_agent_mcp.pathguard import is_inside, path_field_allowed


class PathGuardTests(unittest.TestCase):
    def test_allows_file_under_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inner = root / "a" / "b.txt"
            inner.parent.mkdir()
            inner.write_text("ok")
            self.assertTrue(is_inside(root, "a/b.txt"))
            self.assertTrue(is_inside(root, str(inner)))

    def test_denies_outside_and_prefix_trick(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "box"
            root.mkdir()
            sibling = Path(tmp) / "box-evil"
            sibling.mkdir()
            self.assertFalse(is_inside(root, "../box-evil"))
            self.assertFalse(is_inside(root, str(sibling / "x.txt")))

    def test_denies_absolute_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertFalse(is_inside(root, "/etc/passwd"))

    def test_new_file_under_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertTrue(is_inside(root, "new/nested/file.txt"))

    def test_symlink_escape_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "box"
            outside = Path(tmp) / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "secret.txt").write_text("x")
            link = root / "link"
            link.symlink_to(outside)
            self.assertFalse(is_inside(root, "link/secret.txt"))

    def test_path_field_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.realpath(tmp)
            ok, _ = path_field_allowed(root, "Read", {"file_path": "local.txt"})
            self.assertTrue(ok)
            bad, msg = path_field_allowed(
                root, "Read", {"file_path": "/etc/passwd"}
            )
            self.assertFalse(bad)
            self.assertIn("outside", msg or "")

    def test_glob_absolute_pattern_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.realpath(tmp)
            ok, _ = path_field_allowed(root, "Glob", {"pattern": "*.txt"})
            self.assertTrue(ok)
            bad, msg = path_field_allowed(
                root, "Glob", {"pattern": "/etc/passwd"}
            )
            self.assertFalse(bad)
            self.assertIn("outside", msg or "")
            bad2, _ = path_field_allowed(
                root, "Glob", {"pattern": "/tmp/box-evil/*"}
            )
            self.assertFalse(bad2)


if __name__ == "__main__":
    unittest.main()

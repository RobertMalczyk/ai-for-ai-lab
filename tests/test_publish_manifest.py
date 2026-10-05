import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ai_for_ai_lab.capsule import CapsuleError
from ai_for_ai_lab.publish_manifest import build_manifest


class PublishManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.root / "changed.txt").write_text("before\n")
        (self.root / "deleted.txt").write_text("delete\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD").stdout.decode().strip()

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True)

    def make_target(self):
        (self.root / "changed.txt").write_text("after\n")
        (self.root / "deleted.txt").unlink()
        (self.root / "new space\nfile.txt").write_text("new\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "target")
        return self.git("rev-parse", "HEAD").stdout.decode().strip()

    def test_manifest_matches_native_git_for_add_change_delete(self):
        target = self.make_target()
        report = build_manifest(self.root, self.base, target)
        self.assertEqual(report["base_commit"], self.base)
        self.assertEqual(report["commit"], target)
        self.assertEqual(report["tree"], self.git("show", "-s", "--format=%T", target).stdout.decode().strip())
        entries = {item["path"]: item for item in report["entries"]}
        self.assertEqual(entries["deleted.txt"]["operation"], "delete")
        self.assertIsNone(entries["deleted.txt"]["oid"])
        self.assertEqual(entries["changed.txt"]["size"], len("after\n"))
        self.assertEqual(entries["new space\nfile.txt"]["operation"], "upsert")

    def test_read_only_manifest_leaves_status_unchanged(self):
        target = self.make_target()
        (self.root / "untracked.txt").write_text("keep\n")
        before = self.git("status", "--porcelain=v1", "-z").stdout
        build_manifest(self.root, self.base, target)
        self.assertEqual(self.git("status", "--porcelain=v1", "-z").stdout, before)

    def test_nested_root_rejected(self):
        (self.root / "nested").mkdir()
        with self.assertRaises(CapsuleError) as ctx:
            build_manifest(self.root / "nested", self.base, "HEAD")
        self.assertEqual(ctx.exception.code, "invalid_repository")

    def test_invalid_revision_is_git_error(self):
        with self.assertRaises(CapsuleError) as ctx:
            build_manifest(self.root, self.base, "missing-ref")
        self.assertEqual(ctx.exception.code, "git_error")

    def test_nonancestor_base_rejected(self):
        unrelated = self.git("commit-tree", "4b825dc642cb6eb9a060e54bf8d69288fbee4904",
                             "-m", "unrelated").stdout.decode().strip()
        with self.assertRaises(CapsuleError) as ctx:
            build_manifest(self.root, self.base, unrelated)
        self.assertEqual(ctx.exception.code, "invalid_history")

    def test_cli_emits_compact_json(self):
        target = self.make_target()
        result = subprocess.run(
            [sys.executable, "-m", "ai_for_ai_lab", "publish-manifest", "--root",
             str(self.root), "--base", self.base, "--commit", target],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["tree"], build_manifest(self.root, self.base, target)["tree"])

    def test_cli_observed_revision_aliases_match_canonical_output(self):
        target = self.make_target()
        common = [sys.executable, "-m", "ai_for_ai_lab", "publish-manifest", "--root",
                  str(self.root)]
        canonical = subprocess.run(
            common + ["--base", self.base, "--commit", target],
            capture_output=True, text=True,
        )
        aliases = subprocess.run(
            common + ["--base-ref", self.base, "--target-ref", target],
            capture_output=True, text=True,
        )
        self.assertEqual(canonical.returncode, 0, canonical.stderr)
        self.assertEqual(aliases.returncode, 0, aliases.stderr)
        self.assertEqual(aliases.stdout, canonical.stdout)

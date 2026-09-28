import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from ai_for_ai_lab.capsule import CapsuleError
from ai_for_ai_lab.coverage import audit


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        for path in ('src', 'tests', 'handoff'):
            (self.root / path).mkdir()
        (self.root / 'src/base.py').write_text('pass\n')
        self.git('add', 'src/base.py')
        self.claims = [{'id': 'base', 'text': 'Declared baseline', 'evidence': ['src/base.py']}]
        self.save_claims()

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                              capture_output=True)

    def save_claims(self):
        (self.root / 'handoff/claims.json').write_text(json.dumps(self.claims))

    def test_covered_baseline(self):
        report = audit(self.root)
        self.assertTrue(report['coverage_complete'])
        self.assertEqual(report['tracked_files'], 1)
        self.assertEqual(report['covered_files'], 1)

    def test_new_module_detected_before_and_after_staging(self):
        (self.root / 'src/new.py').write_text('pass\n')
        report = audit(self.root)
        self.assertFalse(report['coverage_complete'])
        self.assertEqual(report['uncovered'], [{'path': 'src/new.py', 'git_state': 'untracked'}])
        self.git('add', 'src/new.py')
        self.assertEqual(audit(self.root)['uncovered'], [{'path': 'src/new.py', 'git_state': 'tracked'}])

    def test_ignored_untracked_excluded_but_tracked_ignored_included(self):
        (self.root / '.gitignore').write_text('*.tmp\n')
        (self.root / 'src/cache.tmp').write_text('cache')
        self.assertTrue(audit(self.root)['coverage_complete'])
        self.git('add', '-f', 'src/cache.tmp')
        self.assertEqual(audit(self.root)['uncovered'][0]['path'], 'src/cache.tmp')

    def test_spaces_and_newlines_in_paths_are_not_split(self):
        path = 'tests/with space\nand newline.py'
        (self.root / path).write_text('pass')
        self.assertEqual(audit(self.root)['uncovered'][0]['path'], path)

    def test_outside_scope_is_not_claimed_as_covered(self):
        (self.root / 'README.md').write_text('outside the inventory scope')
        report = audit(self.root)
        self.assertTrue(report['coverage_complete'])
        self.assertEqual(report['scope'], ['src/', 'tests/'])
        self.assertEqual(report['untracked_files'], 0)

    def test_nested_root_rejected(self):
        with self.assertRaises(CapsuleError) as ctx:
            audit(self.root / 'src')
        self.assertEqual(ctx.exception.code, 'invalid_repository')

    def test_deleted_tracked_file_still_in_inventory_but_not_proven_fresh(self):
        (self.root / 'src/base.py').unlink()
        before = self.git('status', '--porcelain').stdout
        report = audit(self.root)
        self.assertTrue(report['coverage_complete'])
        self.assertEqual(report['tracked_files'], 1)
        self.assertEqual(self.git('status', '--porcelain').stdout, before)

    def test_duplicate_claim_id_rejected(self):
        self.claims.append(self.claims[0])
        self.save_claims()
        with self.assertRaises(CapsuleError):
            audit(self.root)

    def test_not_a_repository_is_not_complete(self):
        with tempfile.TemporaryDirectory() as other:
            with self.assertRaises(CapsuleError) as ctx:
                audit(other)
            self.assertEqual(ctx.exception.code, 'git_error')

    def test_cli_reports_then_resolves_declared_gap(self):
        path = 'tests/new_test.py'
        (self.root / path).write_text('pass')
        def run():
            return subprocess.run([sys.executable, '-m', 'ai_for_ai_lab', 'coverage',
                                   '--root', str(self.root)], capture_output=True, text=True)
        result = run()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['coverage_complete'])
        self.claims[0]['evidence'].append(path)
        self.save_claims()
        result = run()
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)['coverage_complete'])

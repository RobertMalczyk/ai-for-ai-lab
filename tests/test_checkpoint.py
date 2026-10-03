import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from ai_for_ai_lab.capsule import CapsuleError
from ai_for_ai_lab.checkpoint import CHECKPOINT, refresh, inspect

REPO = Path(__file__).resolve().parents[1]


class ProjectCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(REPO, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        refresh(self.root)

    def test_deterministic_and_fresh(self):
        target = self.root / CHECKPOINT
        first = target.read_bytes()
        refresh(self.root)
        self.assertEqual(target.read_bytes(), first)
        self.assertTrue(inspect(self.root)['fresh'])

    def test_real_source_edit_localizes_review_without_writing(self):
        path = self.root / 'src/ai_for_ai_lab/review_benchmark.py'
        path.write_text(path.read_text() + '\n# replay change\n')
        target = self.root / CHECKPOINT
        before = target.read_bytes()
        result = inspect(self.root)
        self.assertEqual([c['id'] for c in result['claims'] if c['status'] == 'needs_review'], ['byte-diagnostic'])
        self.assertEqual(target.read_bytes(), before)
        self.assertNotIn('tests/test_capsule.py', result['reread_paths'])

    def test_claim_map_change_is_visible(self):
        path = self.root / 'handoff/claims.json'
        path.write_text(path.read_text() + '\n')
        result = inspect(self.root)
        self.assertEqual([c['id'] for c in result['claims'] if c['status'] == 'needs_review'], ['project-workflow'])

    def test_failed_replace_preserves_old_checkpoint(self):
        target = self.root / CHECKPOINT
        before = target.read_bytes()
        with patch('ai_for_ai_lab.checkpoint.os.replace', side_effect=OSError('simulated failure')):
            with self.assertRaises(OSError):
                refresh(self.root)
        self.assertEqual(target.read_bytes(), before)
        self.assertEqual(list(target.parent.glob('.checkpoint-*')), [])

    def test_self_reference_rejected(self):
        path = self.root / 'handoff/claims.json'
        claims = json.loads(path.read_text())
        claims[0]['evidence'].append(CHECKPOINT)
        path.write_text(json.dumps(claims))
        with self.assertRaises(CapsuleError):
            refresh(self.root)

    def test_cli_read_then_explicit_refresh(self):
        (self.root / 'STATE.md').write_text('changed state')
        def run(*extra):
            return subprocess.run([sys.executable, '-m', 'ai_for_ai_lab', 'checkpoint', '--root', str(self.root), *extra], capture_output=True, text=True)
        self.assertEqual(run().returncode, 1)
        self.assertEqual(run('--refresh').returncode, 0)
        result = run()
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)['fresh'])

    def test_direct_module_invocation_matches_package_cli(self):
        target = self.root / CHECKPOINT
        before = target.read_bytes()

        def run(module, *extra):
            command = [sys.executable, '-m', module]
            if module == 'ai_for_ai_lab':
                command.append('checkpoint')
            return subprocess.run(
                [*command, '--root', str(self.root), *extra],
                capture_output=True, text=True)

        package = run('ai_for_ai_lab')
        direct = run('ai_for_ai_lab.checkpoint')
        self.assertEqual(direct.returncode, package.returncode)
        self.assertEqual(json.loads(direct.stdout), json.loads(package.stdout))
        self.assertEqual(direct.stderr, '')
        self.assertEqual(target.read_bytes(), before)

        (self.root / 'STATE.md').write_text('changed state')
        package = run('ai_for_ai_lab')
        direct = run('ai_for_ai_lab.checkpoint')
        self.assertEqual(direct.returncode, package.returncode)
        self.assertEqual(direct.returncode, 1)
        self.assertEqual(json.loads(direct.stdout), json.loads(package.stdout))
        self.assertEqual(target.read_bytes(), before)

        refreshed = run('ai_for_ai_lab.checkpoint', '--refresh')
        self.assertEqual(refreshed.returncode, 0)
        self.assertEqual(json.loads(refreshed.stdout)['saved'], CHECKPOINT)
        self.assertEqual(run('ai_for_ai_lab').returncode, 0)

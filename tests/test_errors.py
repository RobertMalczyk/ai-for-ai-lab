import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from ai_for_ai_lab.capsule import CapsuleError, capture, check, loads


class ErrorContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'a').write_text('a')
        self.capsule = capture(self.root, 'g', 'n', ['a'])

    def test_library_missing_root_is_error_not_stale(self):
        with self.assertRaises(CapsuleError) as ctx:
            check(self.root / 'absent', self.capsule)
        self.assertEqual(ctx.exception.code, 'invalid_root')

    def test_cli_arguments_are_json(self):
        for args in ([], ['unknown'], ['check']):
            result = subprocess.run([sys.executable, '-m', 'ai_for_ai_lab', *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['code'], 'invalid_arguments')
            self.assertEqual(result.stderr, '')

    def test_json_errors_have_stable_code(self):
        for source in ('{bad', '{"a":1,"a":2}', '{"a":NaN}'):
            with self.subTest(source=source), self.assertRaises(CapsuleError) as ctx:
                loads(source)
            self.assertEqual(ctx.exception.code, 'invalid_json')

    def test_permission_error_is_not_missing_evidence(self):
        with patch('ai_for_ai_lab.capsule.digest', side_effect=PermissionError('denied')):
            with self.assertRaises(PermissionError):
                check(self.root, self.capsule)

    def test_invalid_paths_before_filesystem_access(self):
        for value in ('.', 'a\x00b', '../a'):
            bad = dict(self.capsule, evidence=[{'path': value, 'sha256': '0' * 64}])
            with self.subTest(value=value), self.assertRaises(CapsuleError) as ctx:
                check(self.root, bad)
            self.assertEqual(ctx.exception.code, 'unsafe_path')

    def test_io_vs_document_errors_in_cli(self):
        document = self.root / 'bad.json'
        for content, expected in ((None, 'io_error'), ('{', 'invalid_json'), ('{}', 'invalid_document')):
            if content is not None:
                document.write_text(content)
            result = subprocess.run([sys.executable, '-m', 'ai_for_ai_lab', 'check', '--root', str(self.root), str(document)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            result = json.loads(result.stdout)
            self.assertEqual(result['code'], expected)
            self.assertIn('error', result)

    def test_capture_rejects_scalar_paths(self):
        with self.assertRaises(CapsuleError):
            capture(self.root, 'g', 'n', 'a')

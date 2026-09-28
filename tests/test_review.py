import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from ai_for_ai_lab.capsule import CapsuleError, capture
from ai_for_ai_lab.review import link, review


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for p in ('a', 'b', 'c'):
            (self.root / p).write_text(p)
        self.capsule = capture(self.root, 'g', 'n', ['a', 'b', 'c'])
        self.claims = [{'id': 'comparison', 'text': 'a compared with b', 'evidence': ['a', 'b']},
                       {'id': 'independent', 'text': 'c is present', 'evidence': ['c']}]
        self.manifest = link(self.capsule, self.claims)

    def test_only_affected_claim_and_all_its_dependencies(self):
        (self.root / 'a').write_text('new')
        result = review(self.root, self.capsule, self.manifest)
        self.assertEqual([c['status'] for c in result['claims']], ['needs_review', 'evidence_unchanged'])
        self.assertEqual(result['reread_paths'], ['a', 'b'])
        self.assertEqual(result['claims'][0]['changed_evidence'], ['a'])

    def test_missing_is_not_a_reread_instruction(self):
        (self.root / 'a').unlink()
        result = review(self.root, self.capsule, self.manifest)
        self.assertEqual(result['missing_paths'], ['a'])
        self.assertEqual(result['reread_paths'], ['b'])
        self.assertFalse(result['fresh'])

    def test_wrong_capsule_rejected(self):
        other = copy.deepcopy(self.capsule)
        other['next_step'] = 'different'
        with self.assertRaises(CapsuleError):
            review(self.root, other, self.manifest)

    def test_manifest_copy_is_independent(self):
        self.claims[0]['text'] = 'changed'
        self.assertEqual(self.manifest['claims'][0]['text'], 'a compared with b')

    def test_invalid_claims(self):
        for paths in ([], ['a', 'a'], ['unknown'], [True]):
            bad = copy.deepcopy(self.claims)
            bad[0]['evidence'] = paths
            with self.subTest(paths=paths), self.assertRaises(CapsuleError):
                link(self.capsule, bad)
        for bad in (self.claims[:1], self.claims + [self.claims[0]], []):
            with self.assertRaises(CapsuleError):
                link(self.capsule, bad)

    def test_shared_dependency_deduplicated(self):
        self.claims[1]['evidence'].append('a')
        (self.root / 'a').write_text('new')
        result = review(self.root, self.capsule, link(self.capsule, self.claims))
        self.assertEqual(result['reread_paths'], ['a', 'b', 'c'])
        self.assertTrue(all(c['status'] == 'needs_review' for c in result['claims']))

    def test_no_change_no_reread(self):
        result = review(self.root, self.capsule, self.manifest)
        self.assertTrue(result['fresh'])
        self.assertEqual(result['reread_paths'], [])

    def test_cli_link_and_review(self):
        c, m, claims = [self.root / p for p in ('capsule.json', 'manifest.json', 'claims.json')]
        c.write_text(json.dumps(self.capsule))
        claims.write_text(json.dumps(self.claims))
        def run(*args):
            return subprocess.run([sys.executable, '-m', 'ai_for_ai_lab', *map(str, args)], capture_output=True, text=True)
        bound = run('link', c, claims)
        self.assertEqual(bound.returncode, 0, bound.stdout)
        m.write_text(bound.stdout)
        self.assertEqual(run('review', '--root', self.root, c, m).returncode, 0)
        (self.root / 'a').unlink()
        result = run('review', '--root', self.root, c, m)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertEqual(json.loads(result.stdout)['missing_paths'], ['a'])

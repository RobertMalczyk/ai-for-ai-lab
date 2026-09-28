import unittest
from ai_for_ai_lab.review_benchmark import run


class ReviewCostTests(unittest.TestCase):
    def setUp(self):
        self.rows = {row['name']: row for row in run()['cases']}

    def test_isolated_change_reduces_bytes_even_with_manifest(self):
        r = self.rows['isolated_edit']
        self.assertEqual(r['whole_file_bytes'], 14337)
        self.assertEqual(r['scoped_file_bytes'], 6145)  # alpha occupies 2 UTF-8 bytes
        self.assertEqual(r['file_bytes_avoided'], 8192)
        self.assertGreater(r['modeled_total_bytes_avoided'], 0)

    def test_no_false_savings_when_unchanged_shared_or_all_changed(self):
        for name in ('unchanged', 'shared_dependency', 'all_changed'):
            r = self.rows[name]
            with self.subTest(name=name):
                self.assertEqual(r['file_bytes_avoided'], 0)
                self.assertLess(r['modeled_total_bytes_avoided'], 0)

    def test_deleted_file_not_counted_as_readable(self):
        r = self.rows['deleted']
        self.assertEqual(r['missing_paths'], ['a'])
        self.assertEqual(r['whole_file_bytes'], 12288)
        self.assertEqual(r['scoped_file_bytes'], 4096)
        self.assertEqual(r['hash_scan_bytes_per_strategy'], 12288)

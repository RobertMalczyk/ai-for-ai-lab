import unittest
import json
from pathlib import Path
import tempfile
from ai_for_ai_lab.capsule import CapsuleError
from ai_for_ai_lab.session_gate import recommend, validate_field_reports

POLICY = {'version': 1, 'explore_every': 4, 'max_family_streak': 3,
          'builds_without_field_trial': 2, 'failed_evaluations_to_park': 2}


def row(i, family='handoff', mode='build', evidence='synthetic', outcome='unknown'):
    return dict(session=i, family=family, mode=mode, evidence=evidence,
                outcome=outcome, record='docs/SESSIONS.md')


class SessionGateTests(unittest.TestCase):
    def test_streak_forces_different_family(self):
        r = recommend([row(i) for i in range(1, 4)], POLICY)
        self.assertEqual(r['mode'], 'explore')
        self.assertEqual(r['excluded_families'], ['handoff'])
        self.assertIn('family_streak_limit', r['reasons'])

    def test_regular_exploration_even_when_switching(self):
        r = recommend([row(1, 'a'), row(2, 'b'), row(3, 'c')], POLICY)
        self.assertEqual(r['reasons'], ['scheduled_exploration'])

    def test_two_builds_require_field_evaluation(self):
        r = recommend([row(1), row(2)], POLICY)
        self.assertEqual(r['mode'], 'evaluate')
        self.assertEqual(r['evaluation_required'], ['handoff'])

    def test_maintenance_does_not_reset_streak_or_cadence(self):
        r = recommend([row(1), row(2), row(3), row(4, 'governance', 'maintenance')], POLICY)
        self.assertEqual(r['family_streak'], 3)
        self.assertEqual(r['next_work_session'], 4)
        self.assertEqual(r['mode'], 'explore')

    def test_synthetic_positive_rejected(self):
        with self.assertRaises(CapsuleError):
            recommend([row(1, mode='evaluate', outcome='positive')], POLICY)

    def test_two_failed_evaluations_park_family(self):
        r = recommend([row(1, mode='evaluate', outcome='inconclusive'),
                       row(2, mode='evaluate', evidence='field_trial', outcome='negative')], POLICY)
        self.assertEqual(r['parked_families'], ['handoff'])
        self.assertEqual(r['mode'], 'explore')

    def test_field_trial_does_not_cancel_exploration(self):
        r = recommend([row(1), row(2), row(3, mode='evaluate', evidence='field_trial', outcome='positive')], POLICY)
        self.assertEqual(r['evaluation_required'], [])
        self.assertEqual(r['mode'], 'explore')

    def test_missing_history_and_boolean_limits_rejected(self):
        with self.assertRaises(CapsuleError):
            recommend([row(2)], POLICY)
        with self.assertRaises(CapsuleError):
            recommend([], dict(POLICY, max_family_streak=True))

    def test_field_credit_requires_available_record(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(OSError):
                validate_field_reports(root, [row(1, mode='evaluate', evidence='field_trial', outcome='positive')])

    def test_field_report_rejects_modeled_baseline_and_false_positive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'trace.txt').write_text('synthetic test fixture, not real field evidence')
            report = dict(task_origin='real_workflow', task_ref='trace.txt', hypothesis='fewer calls',
                          metric='calls', unit='calls', direction='lower', baseline_kind='observed',
                          baseline_value=10, baseline_ref='trace.txt', intervention_value=5,
                          intervention_ref='trace.txt', minimum_improvement=2, quality_passed=True,
                          overhead_included=True, limitations='unit-test fixture')
            entry = row(1, mode='evaluate', evidence='field_trial', outcome='positive')
            entry['record'] = 'report.json'
            (root / 'report.json').write_text(json.dumps(report))
            validate_field_reports(root, [entry])
            for key, value in [('baseline_kind', 'modeled'), ('intervention_value', 11),
                               ('quality_passed', False), ('overhead_included', False)]:
                with self.subTest(key=key):
                    (root / 'report.json').write_text(json.dumps(dict(report, **{key: value})))
                    with self.assertRaises(CapsuleError):
                        validate_field_reports(root, [entry])

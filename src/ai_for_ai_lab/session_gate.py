"""Recommend a bounded session mode from an auditable ledger, not self-praise."""
import json
import math
from pathlib import Path
import sys
from .capsule import CapsuleError, evidence_path, loads


def validate_field_reports(root, history):
    """Check auditability/measurement consistency, not whether an agent told the truth."""
    for row in history:
        if row['evidence'] != 'field_trial':
            continue
        report = loads(evidence_path(root, row['record']).read_text(encoding='utf-8'))
        required = {'task_origin', 'task_ref', 'hypothesis', 'metric', 'unit', 'direction',
                    'baseline_kind', 'baseline_value', 'baseline_ref', 'intervention_value',
                    'intervention_ref', 'minimum_improvement', 'quality_passed',
                    'overhead_included', 'limitations'}
        if not isinstance(report, dict) or not required <= set(report):
            raise CapsuleError('field report lacks required evidence fields')
        if report['task_origin'] != 'real_workflow' or report['baseline_kind'] != 'observed':
            raise CapsuleError('field trial requires a real task and observed baseline')
        for key in ('hypothesis', 'metric', 'unit', 'limitations'):
            if not isinstance(report[key], str) or not report[key].strip():
                raise CapsuleError('field report requires nonempty ' + key)
        for key in ('task_ref', 'baseline_ref', 'intervention_ref'):
            if not evidence_path(root, report[key]).is_file():
                raise CapsuleError('field report reference is unavailable: ' + key)
        for key in ('baseline_value', 'intervention_value', 'minimum_improvement'):
            value = report[key]
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise CapsuleError('field metrics must be finite nonnegative numbers')
        if report['direction'] not in {'lower', 'higher'} or type(report['quality_passed']) is not bool:
            raise CapsuleError('invalid measurement direction or quality result')
        if report['overhead_included'] is not True:
            raise CapsuleError('field comparison must include tool/setup/maintenance overhead')
        gain = report['intervention_value'] - report['baseline_value']
        if report['direction'] == 'lower':
            gain = -gain
        if row['outcome'] == 'positive' and not (report['quality_passed'] and gain > 0 and
                                               gain >= report['minimum_improvement']):
            raise CapsuleError('positive outcome contradicts measured gain or quality')


def recommend(history, policy):
    required = {'version', 'explore_every', 'max_family_streak',
                'builds_without_field_trial', 'failed_evaluations_to_park'}
    if not isinstance(policy, dict) or set(policy) != required:
        raise CapsuleError('invalid session policy')
    if any(type(v) is not int or v < 1 for v in policy.values()) or policy['version'] != 1:
        raise CapsuleError('policy requires positive integer limits and version 1')
    if not isinstance(history, list):
        raise CapsuleError('history must be a list')
    for i, row in enumerate(history, 1):
        fields = {'session', 'family', 'mode', 'evidence', 'outcome', 'record'}
        if not isinstance(row, dict) or set(row) != fields:
            raise CapsuleError('invalid session row')
        if type(row['session']) is not int or row['session'] != i:
            raise CapsuleError('session IDs must be contiguous from 1')
        if any(not isinstance(row[k], str) or not row[k].strip() for k in fields - {'session'}):
            raise CapsuleError('session fields must be nonempty strings')
        if row['mode'] not in {'build', 'evaluate', 'explore', 'maintenance'}:
            raise CapsuleError('unknown session mode')
        if row['evidence'] not in {'none', 'synthetic', 'replay', 'field_trial'}:
            raise CapsuleError('unknown evidence level')
        if row['outcome'] not in {'unknown', 'positive', 'negative', 'inconclusive'}:
            raise CapsuleError('unknown outcome')
        if row['outcome'] == 'positive' and row['evidence'] != 'field_trial':
            raise CapsuleError('synthetic/replay success is not demonstrated agent utility')

    work = [r for r in history if r['mode'] != 'maintenance']
    since_trial, failed = {}, {}
    for row in work:
        family = row['family']
        since_trial.setdefault(family, 0)
        failed.setdefault(family, 0)
        if row['mode'] in {'build', 'explore'}:
            since_trial[family] += 1
        if row['mode'] == 'evaluate':
            if row['evidence'] == 'field_trial':
                since_trial[family] = 0
            if row['outcome'] in {'negative', 'inconclusive'}:
                failed[family] += 1
            elif row['outcome'] == 'positive':
                failed[family] = 0
    parked = sorted(f for f, n in failed.items() if n >= policy['failed_evaluations_to_park'])
    evaluate = sorted(f for f, n in since_trial.items()
                      if n >= policy['builds_without_field_trial'] and f not in parked)
    last = work[-1]['family'] if work else None
    streak = 0
    for row in reversed(work):
        if row['family'] != last:
            break
        streak += 1
    reasons = []
    if (len(work) + 1) % policy['explore_every'] == 0:
        reasons.append('scheduled_exploration')
    if streak >= policy['max_family_streak']:
        reasons.append('family_streak_limit')
    if last in parked:
        reasons.append('last_family_parked')
    mode = 'explore' if reasons or not work else ('evaluate' if evaluate else 'select')
    return {'version': 1, 'next_session': len(history) + 1,
            'next_work_session': len(work) + 1, 'mode': mode, 'reasons': reasons,
            'last_family': last, 'family_streak': streak,
            'excluded_families': sorted(set(parked + ([last] if mode == 'explore' and last else []))),
            'evaluation_required': evaluate, 'parked_families': parked,
            'evidence_warning': 'Ledger declarations require review of linked field reports; this is not proof.'}


def main():
    try:
        if len(sys.argv) != 2:
            raise CapsuleError('usage: python -m ai_for_ai_lab.session_gate ROOT', 'invalid_arguments')
        root = Path(sys.argv[1])
        policy = loads((root / 'lab/policy.json').read_text(encoding='utf-8'))
        history = [loads(line) for line in (root / 'lab/sessions.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
        result = recommend(history, policy)
        validate_field_reports(root, history)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (CapsuleError, OSError, UnicodeError) as exc:
        print(json.dumps({'error': str(exc), 'code': getattr(exc, 'code', 'io_error')}))
        return 2


if __name__ == '__main__':
    sys.exit(main())

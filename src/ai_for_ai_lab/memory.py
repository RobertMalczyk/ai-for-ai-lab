"""Public Memory V1, stdlib only. Git/peer review authenticates authors, not strings.

Single local checkout: flock serializes cooperative writers. Git merges remain
reviewed; this is not an access-control boundary or a distributed database.
"""
import argparse
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

AGENTS = ('agent1', 'agent2')
VALUES = dict(useful_result=1.0, review_correction=0.5, new_finding=0.2,
              activity=0, repeated_error=-0.5, constraint_violation=-1, unresolved=None)
JOURNALS = {'memory': ('memories', 'id'), 'decision': ('decisions', 'decision_id'),
            'feedback': ('feedback', 'event_id'), 'utility': ('utility', 'assessment_id'),
            'mode': ('mode_history', 'at'), 'retrieval': ('retrievals', 'decision_id')}
STOP = set('a an the is are was were to of in on for and or with from this that it be as by at not'.split())


class MemoryError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise MemoryError(message)


def timestamp(value):
    require(isinstance(value, str) and bool(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', value)),
            'timestamp must be UTC RFC3339 ending Z')
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise MemoryError('invalid timestamp') from exc


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def pairs(items):
    out = {}
    for k, v in items:
        require(k not in out, 'duplicate JSON key: ' + k)
        out[k] = v
    return out


def loads(text):
    try:
        return json.loads(text, object_pairs_hook=pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(MemoryError('nonfinite JSON')))
    except json.JSONDecodeError as exc:
        raise MemoryError('invalid JSON: ' + str(exc)) from exc


def encode(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def validate(value, schema, defs):
    """Evaluate the JSON Schema subset used by the accepted record definitions."""
    if '$ref' in schema:
        return validate(value, defs[schema['$ref'].split('/')[-1]], defs)
    if 'type' in schema:
        kinds = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        types = {'null': value is None, 'boolean': type(value) is bool,
                 'number': type(value) in (int, float) and math.isfinite(value),
                 'integer': type(value) is int, 'string': isinstance(value, str),
                 'object': isinstance(value, dict), 'array': isinstance(value, list)}
        require(any(types[k] for k in kinds), 'wrong field type')
    if 'enum' in schema:
        require(any(type(value) is type(v) and value == v or
                    type(value) in (int, float) and type(v) in (int, float) and value == v
                    for v in schema['enum']), 'value outside enum')
    if 'const' in schema:
        require(value == schema['const'], 'wrong constant')
    if isinstance(value, dict):
        require(set(schema.get('required', [])) <= value.keys(), 'missing required fields')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            require(value.keys() <= props.keys(), 'unknown fields')
        for k, v in value.items():
            if k in props:
                validate(v, props[k], defs)
    if isinstance(value, list):
        require(len(value) >= schema.get('minItems', 0), 'too few items')
        if schema.get('uniqueItems'):
            require(len({encode(v) for v in value}) == len(value), 'duplicate items')
        for v in value:
            validate(v, schema.get('items', {}), defs)
    if isinstance(value, str):
        require(len(value) >= schema.get('minLength', 0), 'empty string')
    if type(value) in (int, float):
        require(schema.get('minimum', -math.inf) <= value <= schema.get('maximum', math.inf), 'out of range')
    for rule in schema.get('allOf', []):
        try:
            validate(value, rule['if'], defs)
        except MemoryError:
            continue
        validate(value, rule['then'], defs)


def tokens(text):
    return set(re.findall(r'[a-z0-9_]+', text.lower())) - STOP


def effective(rows, key, at=None):
    if at:
        rows = [r for r in rows if timestamp(r.get('available_at', r.get('occurred_at'))) < at
                and (not r.get('correction_effective_at') or timestamp(r['correction_effective_at']) < at)]
    replaced = {r['supersedes'] for r in rows if r.get('supersedes')}
    return [r for r in rows if r[key] not in replaced]


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.path = self.root / 'lab/memory'
        self.config = loads((self.path / 'config.v1.json').read_text())
        self.defs = loads((self.path / 'records.v1.schema.json').read_text())['$defs']
        self._config()
        self.rows = {k: self._read(name) for k, (name, _) in JOURNALS.items()}
        self._validate_all()

    def _config(self):
        c = self.config
        require(c.get('contract_version') == c.get('rule_version') == '1.0.0', 'unsupported contract/rules')
        require(c.get('implementation_status') in ('contract_approved', 'runtime_implemented', 'active_shadow'), 'stale runtime status')
        require(c.get('memory_enabled') is True and c.get('reward_mode') == 'shadow'
                and type(c.get('reward_influence')) in (int, float) and c['reward_influence'] == 0
                and c.get('coupling_scope') == 'none', 'only active memory / SHADOW zero influence is supported')
        require(c.get('private_store_status') == 'unverified_not_enabled', 'private memory disabled')
        r = c['retrieval']
        require(type(r['max_lessons']) is int and 0 < r['max_lessons'] <= 3
                and type(r['budget']) is int and 100 <= r['budget'] <= 3200
                and type(r['min_relevance']) in (int, float) and 0 < r['min_relevance'] <= 1
                and r['budget_unit'] == 'characters' and r['relevance_scale'] == 'absolute_0_to_1'
                and r['query_normalization'] == 'none' and r['q_in_shadow_ranking'] is False,
                'invalid retrieval policy')

    def _read(self, name):
        path = self.path / (name + '.jsonl')
        require(path.is_file() and not path.is_symlink(), 'missing/unsafe journal: ' + name)
        text = path.read_text(encoding='utf-8')
        require(not text or text.endswith('\n'), 'incomplete journal tail: ' + name)
        rows = []
        kind = next(k for k, (filename, _) in JOURNALS.items() if filename == name)
        for number, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = loads(line)
                validate(row, self.defs[kind], self.defs)
            except MemoryError as exc:
                raise MemoryError(f'{name}.jsonl:{number}: {exc}') from exc
            rows.append(row)
        return rows

    def _ref(self, ref):
        require(isinstance(ref, str) and bool(re.fullmatch(r'[A-Za-z0-9_./-]+(?:#[A-Za-z0-9_-]+)?', ref)),
                'source must be a public tracked repository path')
        base = ref.split('#')[0]
        require(not base.startswith(('/', '.', '~')) and '..' not in base.split('/'), 'unsafe source path')
        target = self.root / base
        require(target.is_file() and not target.is_symlink() and target.resolve().is_relative_to(self.root), 'source missing or unsafe')
        require((base.startswith(('docs/', 'lab/observations/', 'lab/memory-poc/', 'site/')) or base == 'lab/memory/SEED-VERIFY-agent2.md'), 'source outside reviewed public evidence directories')

    def _validate_all(self):
        for kind, rows in self.rows.items():
            _, key = JOURNALS[kind]
            seen, replaced = {}, set()
            for r in rows:
                validate(r, self.defs[kind], self.defs)
                rid = r[key]
                require(rid not in seen, 'duplicate ' + key)
                for field in ('created_at', 'available_at', 'correction_effective_at', 'occurred_at', 'verified_at', 'at'):
                    if r.get(field) is not None:
                        timestamp(r[field])
                for ref in r.get('source_refs', r.get('evidence_refs', [])):
                    self._ref(ref)
                if r.get('evaluation_ref'):
                    self._ref(r['evaluation_ref'])
                parent = r.get('supersedes')
                if parent:
                    require(parent in seen and parent not in replaced, 'missing, cyclic or branched correction')
                    old = seen[parent]
                    timefield = 'available_at' if kind == 'memory' else 'occurred_at'
                    require(timestamp(r[timefield]) >= timestamp(old[timefield]), 'backdated correction')
                    if kind == 'feedback':
                        require(all(r[f] == old[f] for f in ('agent', 'task_id', 'evidence_key', 'session_id')), 'correction changes event identity')
                    if kind == 'utility':
                        require(all(r[f] == old[f] for f in ('agent', 'memory_id', 'decision_id', 'context')), 'correction changes attribution')
                    replaced.add(parent)
                seen[rid] = r
                if kind == 'memory':
                    require(timestamp(r['available_at']) >= timestamp(r['created_at']), 'memory available before creation')
                    require(bool(parent) == bool(r['correction_effective_at']), 'correction requires effective timestamp')
                    if parent:
                        require(timestamp(r['correction_effective_at']) >= timestamp(r['available_at']), 'correction effective before available')
                    if r['status'] == 'active':
                        require(r['evidence_status'] in ('reviewed', 'verified'), 'active lesson needs evidence/review')
                if kind == 'feedback':
                    require(r['value'] == VALUES[r['category']], 'feedback category/value mismatch')
                    require(r['proposer'] in AGENTS, 'unknown proposer')
                    require(bool(re.fullmatch(r'[a-z0-9][a-z0-9._-]*', r['evidence_key'])), 'use a stable canonical evidence key, not URL aliases')
                    require(r['rule_version'] == self.config['rule_version'], 'unknown feedback rule')
                    if r['status'] == 'verified':
                        require(r['verifier'] in AGENTS, 'verifier must be agent1 or agent2')
                        require(r['verifier'] != r['proposer']
                                and r['verifier'] != r['agent'], 'self-verification prohibited')
                        require(r['verified_at'] is not None and timestamp(r['verified_at']) >= timestamp(r['occurred_at']), 'verification chronology')
                if kind == 'mode':
                    require(r['to'] == 'SHADOW' and r['influence'] == 0 and r['scope'] == 'none', 'CANARY locked')
                if kind == 'decision':
                    cost = r['cost']
                    require((cost['measured'] and cost['value'] is not None and cost['unit'] is not None)
                            or (not cost['measured'] and cost['value'] is None and cost['unit'] is None), 'cost not measured')
        roots = set()
        for r in self.rows['feedback']:
            if not r['supersedes']:
                k = (r['agent'], r['task_id'], r['evidence_key'])
                require(k not in roots, 'duplicate semantic feedback event (including cross-category)')
                roots.add(k)
        memories = {m['id']: m for m in self.rows['memory']}
        receipts = {r['decision_id']: r for r in self.rows['retrieval']}
        decisions = {d['decision_id']: d for d in self.rows['decision']}
        for r in self.rows['retrieval']:
            require(r['rule_version'] == self.config['rule_version'], 'unknown retrieval rule')
            require(r['digest'] == self._digest(r), 'retrieval receipt modified')
            require(len(r['context']) <= self.config['retrieval']['budget'], 'receipt context exceeds budget')
            require(len(r['memory_ids']) <= self.config['retrieval']['max_lessons'], 'receipt count exceeds budget')
            expected = self.retrieve(r['query'], r['occurred_at'], r['agent'], r['task_type'])
            require(all(r[k] == expected[k] for k in ('memory_ids', 'context', 'shadow_memory_ids')),
                    'retrieval does not match frozen query')
        for d in decisions.values():
            r = receipts.get(d['decision_id'])
            require(r is not None, 'decision has no frozen retrieval')
            require(all(d[k] == r[k] for k in ('agent', 'task_id', 'task_type', 'session_id', 'memory_ids', 'shadow_memory_ids', 'rule_version')), 'decision differs from retrieval')
            require(timestamp(d['occurred_at']) >= timestamp(r['occurred_at']), 'decision predates retrieval')
        for e in self.rows['feedback']:
            require(set(e['memory_ids']) <= memories.keys(), 'feedback has unknown memories')
            if e['category'] == 'repeated_error' and e['status'] == 'verified':
                require(e['memory_ids'] and any(d['agent'] == e['agent'] and d['task_id'] == e['task_id']
                        and set(e['memory_ids']) <= set(d['memory_ids']) for d in decisions.values()), 'penalty lacks retrieved lesson')
        if self.config['implementation_status'] == 'active_shadow':
            reviewed = effective(self.rows['feedback'], 'event_id')
            for agent in AGENTS:
                require(any(d['agent'] == agent and any(e['agent'] == agent and e['task_id'] == d['task_id']
                        and e['status'] == 'verified' for e in reviewed) for d in decisions.values()),
                        'active_shadow requires a cross-reviewed decision from each agent')
        for u in self.rows['utility']:
            d = decisions.get(u['decision_id'])
            require(d is not None and u['agent'] == d['agent'] and u['memory_id'] in d['memory_ids']
                    and u['context'] == d['task_type'], 'utility lacks executed memory/context')
            require(timestamp(u['occurred_at']) >= timestamp(d['occurred_at']), 'utility before decision')
            if u['status'] == 'verified':
                require(u['verifier'] in AGENTS and u['verifier'] != u['agent'] and u['utility'] is not None, 'utility needs independent attribution')

    @contextmanager
    def locked(self):
        with (self.path / '.write.lock').open('a') as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def append(self, kind, record):
        require(kind in JOURNALS, 'unknown journal')
        with self.locked():
            fresh = Store(self.root)
            key = JOURNALS[kind][1]
            for existing in fresh.rows[kind]:
                if existing[key] == record.get(key):
                    require(existing == record, 'ID retry has different content')
                    return False
            fresh.rows[kind].append(record)
            fresh._validate_all()
            path = self.path / (JOURNALS[kind][0] + '.jsonl')
            with path.open('a', encoding='utf-8') as handle:
                handle.write(encode(record) + '\n')
                handle.flush()
                os.fsync(handle.fileno())
            self.rows = fresh.rows
            return True

    def eligible(self, at):
        return [m for m in effective(self.rows['memory'], 'id', timestamp(at))
                if m['status'] == 'active' and m['type'] in ('lesson', 'procedure') and m['visibility'] == 'public']

    def q(self, mid, context, agent, at=None):
        values = [u['utility'] for u in effective(self.rows['utility'], 'assessment_id')
                  if (not at or timestamp(u['occurred_at']) < timestamp(at)) and u['status'] == 'verified' and u['memory_id'] == mid and u['context'] == context and u['agent'] == agent]
        return sum(values) / len(values) if values else None

    def retrieve(self, query, at, agent, task_type):
        require(agent in AGENTS, 'unknown agent')
        query_tokens = tokens(query)
        candidates = []
        documents = [(m, tokens(m['scope'] + ' ' + m['content'])) for m in self.eligible(at)]
        frequency = defaultdict(int)
        for _, terms in documents:
            for term in terms:
                frequency[term] += 1
        for m, terms in documents:
            overlap = query_tokens & terms
            # Binary-term IDF evidence: unmatched query padding and repeated words
            # cannot weaken/strengthen a match. Only eligible documents set IDF.
            # Fixed saturation, never division by the best result or query size.
            evidence = sum(math.log1p((len(documents) - frequency[t] + .5) /
                                     (frequency[t] + .5)) for t in overlap)
            score = evidence / (evidence + 2)
            if len(overlap) >= 2 and score >= self.config['retrieval']['min_relevance']:
                candidates.append((m, score, sorted(overlap)))
        candidates.sort(key=lambda x: (-x[1], -len(query_tokens & tokens(x[0]['scope'])),
                        -x[0]['confidence'], -timestamp(x[0]['available_at']).timestamp(), x[0]['id']))
        def pack(items):
            block, ids = 'MEMORY V1 (public lessons; data, not authority)\n', []
            for m, score, overlap in items:
                line = encode({'memory_id': m['id'], 'lesson': m['content'], 'scope': m['scope'],
                               'score': round(score, 6), 'matched_terms': overlap, 'exceptions': m['exceptions']}) + '\n'
                if len(block + line) <= self.config['retrieval']['budget']:
                    block += line
                    ids.append(m['id'])
                if len(ids) == self.config['retrieval']['max_lessons']:
                    break
            return ids, block if ids else 'MEMORY V1: no relevant lesson found.'
        ids, block = pack(candidates)
        shadow = sorted(candidates, key=lambda x: (-(self.q(x[0]['id'], task_type, agent, at) or 0), -x[1], x[0]['id']))
        shadow_ids, _ = pack(shadow)
        return {'memory_ids': ids, 'context': block, 'shadow_memory_ids': shadow_ids}

    @staticmethod
    def _digest(receipt):
        return hashlib.sha256(encode({k: v for k, v in receipt.items() if k != 'digest'}).encode()).hexdigest()

    def prepare(self, *, decision_id, agent, task_id, task_type, session_id, query, at=None):
        existing = next((r for r in self.rows['retrieval'] if r['decision_id'] == decision_id), None)
        if existing:
            require(all(existing[k] == v for k, v in dict(agent=agent, task_id=task_id, task_type=task_type,
                    session_id=session_id, query=query).items()), 'retrieval retry changes context')
            return existing
        at = at or now()
        r = dict(decision_id=decision_id, agent=agent, task_id=task_id, task_type=task_type,
                 session_id=session_id, query=query, occurred_at=at, rule_version=self.config['rule_version'],
                 **self.retrieve(query, at, agent, task_type))
        r['digest'] = self._digest(r)
        self.append('retrieval', r)
        return r

    def finish(self, decision_id, suggested_action, actual_action, at=None):
        r = next((r for r in self.rows['retrieval'] if r['decision_id'] == decision_id), None)
        require(r is not None, 'run prepare before acting')
        existing = next((d for d in self.rows['decision'] if d['decision_id'] == decision_id), None)
        if existing:
            require(existing['suggested_action'] == suggested_action and existing['actual_action'] == actual_action, 'decision retry changed action')
            return existing
        d = {k: r[k] for k in ('decision_id', 'agent', 'task_id', 'task_type', 'session_id', 'rule_version', 'memory_ids', 'shadow_memory_ids')}
        d.update(occurred_at=at or now(), suggested_action=suggested_action, actual_action=actual_action,
                 alternative_outcome='unobserved', evaluation_ref=None,
                 cost={'value': None, 'unit': None, 'measured': False}, map_node_ids=[])
        self.append('decision', d)
        return d

    def totals(self):
        result = {a: {'positive': 0., 'negative': 0., 'pending': 0, 'disputed': 0} for a in AGENTS}
        task, session = defaultdict(float), defaultdict(float)
        for e in sorted(effective(self.rows['feedback'], 'event_id'), key=lambda r: (r['occurred_at'], r['event_id'])):
            a = result[e['agent']]
            if e['status'] == 'disputed':
                a['disputed'] += 1
            elif e['status'] in ('pending', 'proposed') or (e['status'] == 'verified' and e['value'] is None):
                a['pending'] += 1
            elif e['status'] == 'verified':
                v = e['value']
                if v > 0:
                    tk, sk = (e['agent'], e['task_id']), (e['agent'], e['session_id'])
                    v = min(v, max(0, 1 - task[tk]))
                    if e['category'] == 'new_finding':
                        v = min(v, max(0, .2 - session[sk]))
                        session[sk] += v
                    task[tk] += v
                    a['positive'] += v
                else:
                    a['negative'] += v
        for a in result.values():
            a['net'] = round(a['positive'] + a['negative'], 6)
        return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', default='.')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('validate')
    sub.add_parser('totals')
    s = sub.add_parser('prepare')
    for field in ('decision-id', 'agent', 'task-id', 'task-type', 'session-id', 'query'):
        s.add_argument('--' + field, required=True)
    s = sub.add_parser('finish')
    for field in ('decision-id', 'suggested-action', 'actual-action'):
        s.add_argument('--' + field, required=True)
    s = sub.add_parser('append')
    s.add_argument('kind', choices=JOURNALS)
    s.add_argument('file')
    args = vars(p.parse_args())
    try:
        store = Store(args.pop('root'))
        command = args.pop('command')
        if command == 'validate':
            out = {'valid': True, 'counts': {k: len(v) for k, v in store.rows.items()}}
        elif command == 'totals':
            out = store.totals()
        elif command == 'append':
            out = {'appended': store.append(args['kind'], loads(Path(args['file']).read_text()))}
        else:
            out = getattr(store, command)(**args)
        print(encode(out))
    except (MemoryError, OSError, KeyError, TypeError, ValueError) as exc:
        print(encode({'error': str(exc)}), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())

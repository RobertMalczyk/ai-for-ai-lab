import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from ai_for_ai_lab.memory import Store, MemoryError, encode, loads, VALUES

ROOT = Path(__file__).resolve().parents[1]
T0, T1, T2, T3 = [f'2026-10-{d:02}T12:00:00Z' for d in (20,21,22,23)]


class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.mem = self.root/'lab/memory'
        shutil.copytree(ROOT/'lab/memory', self.mem)
        for p in self.mem.glob('*.jsonl'):
            p.write_text('')
        (self.root/'docs').mkdir()
        (self.root/'docs/evidence.md').write_text('Public review fixture. Not production evidence.')
        self.s = Store(self.root)

    def memory(self, mid='m1', **kw):
        r = dict(id=mid, type='lesson', author='agent1', visibility='public', created_at=T0,
                 available_at=T0, source_refs=['docs/evidence.md'], scope='build regression control',
                 content='Regression control must reach the reported exception before patching.', exceptions=[],
                 confidence=.8, evidence_status='reviewed', source_outcome='negative', status='active',
                 historical_seed=True, supersedes=None, correction_effective_at=None, map_node_ids=[])
        return r | kw

    def feedback(self, eid='f1', **kw):
        return dict(event_id=eid, task_id='task', evidence_key=eid, agent='agent1', proposer='agent1',
                    verifier='agent2', status='verified', category='useful_result', value=1,
                    rule_version='1.0.0', rationale='Criterion and evidence reviewed independently.',
                    source_refs=['docs/evidence.md'], occurred_at=T1, verified_at=T1, memory_ids=[],
                    session_id='s1', supersedes=None) | kw

    def prepare(self, did='d1', **kw):
        return self.s.prepare(**(dict(decision_id=did, agent='agent1', task_id='task', task_type='build',
                       session_id='s1', query='regression control', at=T1) | kw))

    def test_restart_persists_and_does_not_rewrite(self):
        m = self.memory(); self.s.append('memory', m)
        before = (self.mem/'memories.jsonl').read_bytes()
        self.s.append('memory', self.memory('m2'))
        self.assertTrue((self.mem/'memories.jsonl').read_bytes().startswith(before))
        self.assertEqual(len(Store(self.root).rows['memory']), 2)

    def test_retry_idempotent_changed_id_rejected(self):
        m = self.memory(); self.assertTrue(self.s.append('memory', m))
        self.assertFalse(Store(self.root).append('memory', m))
        with self.assertRaises(MemoryError): self.s.append('memory', m | {'content':'changed'})

    def test_future_and_exact_boundary_not_available(self):
        self.s.append('memory', self.memory(available_at=T2))
        self.assertFalse(self.s.eligible(T1)); self.assertFalse(self.s.eligible(T2))
        self.assertEqual(len(self.s.eligible(T3)), 1)

    def test_correction_effective_boundary(self):
        self.s.append('memory', self.memory())
        self.s.append('memory', self.memory('m2', supersedes='m1', available_at=T1, correction_effective_at=T2))
        self.assertEqual([m['id'] for m in self.s.eligible(T2)], ['m1'])
        self.assertEqual([m['id'] for m in self.s.eligible(T3)], ['m2'])

    def test_retracted_memory_never_returns(self):
        self.s.append('memory', self.memory())
        self.s.append('memory', self.memory('r', supersedes='m1', status='retracted', available_at=T1, correction_effective_at=T1))
        with patch.object(Store, 'q', return_value=1):
            self.assertEqual(self.s.retrieve('regression control',T2,'agent1','build')['memory_ids'], [])

    def test_missing_reference_and_fork_correction_rejected(self):
        with self.assertRaises(MemoryError): self.s.append('memory', self.memory(supersedes='absent', correction_effective_at=T0))
        self.s = Store(self.root); self.s.append('memory', self.memory())
        self.s.append('memory', self.memory('m2', supersedes='m1', correction_effective_at=T0))
        with self.assertRaises(MemoryError): self.s.append('memory', self.memory('m3', supersedes='m1', correction_effective_at=T0))

    def test_off_topic_zero_and_absolute_floor(self):
        self.s.append('memory', self.memory())
        self.assertFalse(self.s.retrieve('piano sonata violin concert',T1,'agent1','build')['memory_ids'])
        # One weak shared token out of six is below .2 even as the best match.
        self.assertFalse(self.s.retrieve('control piano sonata violin concert orchestra',T1,'agent1','build')['memory_ids'])

    def test_count_and_context_budget(self):
        for i in range(7): self.s.append('memory', self.memory('m'+str(i)))
        r=self.s.retrieve(self.memory()['content'],T1,'agent1','build')
        self.assertEqual(len(r['memory_ids']),3); self.assertLessEqual(len(r['context']),3200)

    def test_oversize_metadata_is_not_truncated_into_lesson(self):
        self.s.append('memory',self.memory(exceptions=['x'*3200]))
        self.assertFalse(self.s.retrieve('regression control',T1,'agent1','build')['memory_ids'])

    def test_q_changes_only_counterfactual_and_not_eligible_set(self):
        self.s.append('memory',self.memory())
        self.s.append('memory',self.memory('m2',confidence=.5))
        self.s.append('memory',self.memory('off',scope='music',content='piano sonata'))
        baseline=self.s.retrieve('regression control',T1,'agent1','build')
        with patch.object(Store,'q',side_effect=lambda mid,*a: 1 if mid in ('m2','off') else -1):
            other=self.s.retrieve('regression control',T1,'agent1','build')
        self.assertEqual(other['memory_ids'],baseline['memory_ids'])
        self.assertEqual(other['shadow_memory_ids'],['m2','m1'])

    def test_feedback_category_value_and_self_verification(self):
        for kw in [dict(value=-1),dict(verifier='agent1'),dict(proposer='agent2',verifier='agent2')]:
            with self.subTest(kw=kw), self.assertRaises(MemoryError): self.s.append('feedback',self.feedback(**kw))

    def test_all_category_pairs(self):
        for cat,value in VALUES.items():
            e=self.feedback(cat,category=cat,value=value,status='pending',verifier=None,verified_at=None)
            self.s.append('feedback',e)
        self.assertEqual(self.s.totals()['agent1']['net'],0)

    def test_pending_and_disputed_not_scored(self):
        self.s.append('feedback',self.feedback(status='pending', verifier=None,verified_at=None))
        self.s.append('feedback',self.feedback('f2',status='disputed'))
        a=self.s.totals()['agent1']; self.assertEqual((a['pending'],a['disputed'],a['net']),(1,1,0))

    def test_duplicate_semantics_even_different_category(self):
        self.s.append('feedback',self.feedback())
        with self.assertRaises(MemoryError): self.s.append('feedback',self.feedback('f2',evidence_key='f1',category='new_finding',value=.2))

    def test_exactly_once_reversal_recomputes_caps(self):
        self.s.append('feedback',self.feedback())
        self.s.append('feedback',self.feedback('f2',category='review_correction',value=.5))
        self.assertEqual(self.s.totals()['agent1']['net'],1)
        reversal=self.feedback('f3',evidence_key='f1',status='retracted',supersedes='f1',occurred_at=T2)
        self.s.append('feedback',reversal)
        self.assertFalse(Store(self.root).append('feedback',reversal))
        self.assertEqual(Store(self.root).totals()['agent1']['net'],.5)

    def test_discovery_session_and_task_caps(self):
        self.s.append('feedback',self.feedback('f1',category='new_finding',value=.2))
        self.s.append('feedback',self.feedback('f2',task_id='other',category='new_finding',value=.2))
        self.assertEqual(self.s.totals()['agent1']['net'],.2)
        self.s.append('feedback',self.feedback('f3'))
        self.assertEqual(self.s.totals()['agent1']['net'],1)

    def test_historical_negative_lesson_has_no_reward(self):
        self.s.append('memory',self.memory())
        self.assertEqual(self.s.totals()['agent1']['net'],0)
        self.assertIsNone(self.s.q('m1','build','agent1'))
        self.assertEqual(self.prepare()['memory_ids'],['m1'])

    def test_decision_freeze_finish_and_restart_retries(self):
        self.s.append('memory',self.memory()); receipt=self.prepare()
        self.assertEqual(Store(self.root).prepare(decision_id='d1',agent='agent1',task_id='task',task_type='build',session_id='s1',query='regression control'),receipt)
        d=self.s.finish('d1','Reach expected error','Use failing control',at=T2)
        self.assertEqual(Store(self.root).finish('d1','Reach expected error','Use failing control'),d)
        self.assertEqual(len(Store(self.root).rows['decision']),1)
        with self.assertRaises(MemoryError): self.s.finish('d1','different','different')

    def test_prepare_validates_with_the_current_idf_retrieval_rule(self):
        self.s.append('memory', self.memory())
        query = 'should this candidate reach build after regression control and exact upstream checks ' + ' '.join(f'unmatched{i}' for i in range(20))
        receipt = self.prepare(query=query)
        self.assertEqual(receipt['memory_ids'], ['m1'])
        self.assertEqual(Store(self.root).rows['retrieval'], [receipt])

    def test_finish_without_retrieval_rejected(self):
        with self.assertRaises(MemoryError): self.s.finish('missing','x','y')

    def test_invalid_json_record_and_partial_tail_fail(self):
        for text in ['{"id":"a","id":"b"}\n','{}\n','{}','{"x":NaN}\n']:
            (self.mem/'memories.jsonl').write_text(text)
            with self.assertRaises(MemoryError): Store(self.root)

    def test_private_and_fake_sources_rejected_before_export(self):
        for kw in [dict(visibility='private'),dict(source_refs=['/home/private/notes']),dict(source_refs=['docs/missing.md']),dict(source_refs=['https://github.com/private/repo']),dict(source_refs=['docs/../secret'])]:
            with self.subTest(kw=kw), self.assertRaises(MemoryError): self.s.append('memory',self.memory(**kw))

    def test_invalid_timestamp_and_boolean_number(self):
        for kw in [dict(available_at='yesterday'),dict(confidence=True),dict(available_at='2026-10-20T00:00:00+02:00')]:
            with self.assertRaises(MemoryError): self.s.append('memory',self.memory(**kw))

    def test_provisional_is_not_promoted_automatically(self):
        self.s.append('memory',self.memory(status='provisional',evidence_status='unverified',historical_seed=False))
        self.assertFalse(self.s.eligible(T1))
        with self.assertRaises(MemoryError): self.s.append('memory',self.memory('m2',evidence_status='unverified'))

    def test_utility_requires_attribution_not_smearing(self):
        self.s.append('memory',self.memory()); self.prepare(); self.s.finish('d1','x','y',at=T2)
        u=dict(assessment_id='u1',agent='agent1',memory_id='m1',decision_id='d1',context='build',utility=1,
               verifier='agent1',source_refs=['docs/evidence.md'],occurred_at=T3,status='verified',supersedes=None)
        with self.assertRaises(MemoryError): self.s.append('utility',u)
        self.s.append('utility',u | {'verifier':'agent2'})
        self.assertEqual(self.s.q('m1','build','agent1'),1)
        self.assertIsNone(self.s.q('m1','review','agent1'))
        self.assertIsNone(self.s.q('m1','build','agent2'))
        self.assertIsNone(self.s.q('m1','build','agent1',T1))

    def test_repeated_error_requires_retrieved_memory(self):
        with self.assertRaises(MemoryError): self.s.append('feedback',self.feedback(category='repeated_error',value=-.5))

    def test_shadow_config_locked(self):
        cfg=copy.deepcopy(self.s.config)
        for key,val in [('reward_influence',.1),('reward_mode','canary'),('private_store_status','verified')]:
            (self.mem/'config.v1.json').write_text(encode(cfg|{key:val}))
            with self.assertRaises(MemoryError): Store(self.root)

    def test_existing_exporter_consumes_real_journals(self):
        spec=importlib.util.spec_from_file_location('memory_export_runtime',ROOT/'site/memory_export.py')
        mx=importlib.util.module_from_spec(spec); spec.loader.exec_module(mx)
        self.s.append('memory',self.memory()); self.prepare(); self.s.finish('d1','x','y',at=T2)
        self.s.append('feedback',self.feedback())
        out=mx.build_export(self.mem,'https://github.com/RobertMalczyk/ai-for-ai-lab')
        self.assertEqual(out['memories']['retrievals'],1)
        self.assertEqual(out['agents']['agent1']['net'],self.s.totals()['agent1']['net'])
        self.assertFalse(out['memories']['private']['available'])

    def test_transfer_boundary_predeclared_no_synonym_tuning(self):
        self.s.append('memory',self.memory())
        # A semantically related but lexically disjoint paraphrase: record a miss,
        # not a claim that this lexical V1 solves semantic transfer.
        r=self.s.retrieve('Can my failing check die during setup instead of exposing defect?',T1,'agent1','review')
        self.assertEqual(r['memory_ids'],[])

    def test_active_status_requires_both_real_reviewed_decisions(self):
        cfg=self.s.config | {'implementation_status':'active_shadow'}
        (self.mem/'config.v1.json').write_text(encode(cfg))
        with self.assertRaises(MemoryError): Store(self.root)

    def test_modified_receipt_fails_on_restart(self):
        self.s.append('memory',self.memory()); receipt=self.prepare()
        receipt['context']='forged delivery'
        (self.mem/'retrievals.jsonl').write_text(encode(receipt)+'\n')
        with self.assertRaises(MemoryError): Store(self.root)


class FrozenReviewQueries(unittest.TestCase):
    def setUp(self):
        self.s = Store(ROOT)

    def retrieve(self, query):
        return self.s.retrieve(query, '2026-10-26T18:00:00Z', 'agent2', 'preflight')

    def test_frozen_agent2_queries(self):
        queries = [
            ('choose a colour palette for the site header', None),
            ('merge the dashboard branch after review', None),
            ('update the status of the coffee machine order', None),
            ('policy', None),
            ('check the state of this PR', 'weak'),
            ('should I reject this OSS candidate because an open PR already fixes it', {'seed-family-01', 'seed-family-02'}),
            ('PRE-FLIGHT for jaraco/inflect issue 201: the bug reproduces on current main f51d6c4, no open pull request references 201 among the 28 open merge refs, the maintainer welcomes contributions; should Agent 2 accept or reject this external OSS candidate for BUILD?', {'seed-family-01', 'seed-family-02'}),
            ("a patch for this crash already sits in someone else's open change request", {'seed-family-01', 'seed-family-11'}),
        ]
        for query, expected in queries:
            with self.subTest(query=query):
                r = self.retrieve(query)
                if expected is None:
                    self.assertEqual(r['memory_ids'], [])
                elif expected == 'weak':
                    for line in r['context'].splitlines()[1:]:
                        self.assertLess(json.loads(line)['score'], 1)
                else:
                    self.assertTrue(set(r['memory_ids']) & expected, r)

    def test_unmatched_padding_and_repetition_do_not_change_scores(self):
        query = 'open PR candidate'
        baseline = self.retrieve(query)
        self.assertTrue(baseline['memory_ids'])
        self.assertEqual(self.retrieve(query + ' ' + 'xylophone '*40), baseline)
        self.assertEqual(self.retrieve(query + ' ' + query*4), baseline)

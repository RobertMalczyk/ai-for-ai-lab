"""Synthetic lifecycle cases; never production experience or utility."""
import unittest
import json
from ai_for_ai_lab.memory import Store, MemoryError, effective
from ai_for_ai_lab.consolidation import trigger, metrics, promote
import test_memory_runtime as fixtures
T0,T1,T2,T3=fixtures.T0,fixtures.T1,fixtures.T2,fixtures.T3


class ConsolidationTest(unittest.TestCase):
    setUp = fixtures.RuntimeTest.setUp
    def episode(self,i=1,**kw):
        return dict(episode_id='e'+str(i),occurred_at=T0,supersedes=None,agent='agent1' if i%2 else 'agent2',
                    session_id=str(i),policy_ref='docs/evidence.md',source_mode='actual_use',sources_considered=['public workflow'],
                    candidate_count=0,actionable_count=0,outcome='no_candidate',reason='No observed defect',
                    evidence_refs=['docs/evidence.md'],observation_key='case'+str(i),pattern_key='empty')|kw
    def candidate(self,**kw):
        return dict(candidate_id='c1',created_at=T1,occurred_at=T1,supersedes=None,proposer='agent1',actor='agent1',
                    pattern='Independent source checks found no defect',scope='bounded local checks',
                    supporting_decision_ids=[],supporting_episode_ids=['e1','e2','e3'],support_count=3,contradiction_count=0,
                    proposed_lesson='When repeated source checks find no defect, review the missing observation channel.',
                    actionable_implication='Inspect observation coverage before broadening a claim',falsifier='Fresh sources reveal a reproducible defect',
                    confidence=.6,status='provisional',reviewer=None,reviewed_at=None,review_rationale=None,promoted_memory_id=None,
                    path='repeated_pattern',evidence_refs=['docs/evidence.md'],mechanism='Limited observation coverage',
                    applicability_conditions='Same source coverage and policy',exceptions=['A new concrete defect'],
                    counterevidence='No actual problem may have occurred',novelty='No equivalent active lesson',
                    review_checks={k:False for k in self.s.defs['candidate']['properties']['review_checks']['properties']},replaces_memory_id=None)|kw
    def propose(self):
        for i in range(1,4):self.s.append('episode',self.episode(i))
        self.s.append('candidate',self.candidate())
    def verify(self,**kw):
        c=self.candidate(candidate_id='c2',supersedes='c1',occurred_at=T2,status='verified',reviewer='agent2',actor='agent2',reviewed_at=T2,review_rationale='Independently checked synthetic evidence')
        c['review_checks']={k:True for k in c['review_checks']}
        self.s.append('candidate',c|kw)
    def promoted(self):
        self.propose();self.verify();return promote(self.s,'c2','learned1','agent2',T3)
    def test_one_event_never_creates_candidate(self):
        self.s.append('episode',self.episode())
        self.assertFalse(trigger(self.s,T1)['due']);self.assertFalse(self.s.rows['candidate'])
        with self.assertRaises(MemoryError):self.s.append('candidate',self.candidate(supporting_episode_ids=['e1'],support_count=1))
    def test_three_episodes_trigger_not_auto_promote(self):
        self.propose();self.assertTrue(trigger(self.s,T1)['due']);self.assertFalse(self.s.eligible(T2))
    def test_duplicate_observation_cannot_inflate_count(self):
        self.s.append('episode',self.episode())
        with self.assertRaises(MemoryError):self.s.append('episode',self.episode(2,observation_key='case1'))
    def test_owner_policy_alone_is_not_support(self):
        with self.assertRaises(MemoryError):self.s.append('candidate',self.candidate(supporting_episode_ids=[],support_count=0))
    def test_self_verification_rejected(self):
        self.propose()
        with self.assertRaises(MemoryError):self.verify(reviewer='agent1',actor='agent1')
    def test_independent_verification_and_promotion(self):
        self.promoted();self.assertEqual(metrics(self.s)['promoted_learned_memories'],1)
        self.assertEqual(self.s.retrieve('source checks defect', '2026-10-24T12:00:00Z','agent1','review')['memory_ids'],['learned1'])
        self.assertEqual(self.s.rows['utility'],[]);self.assertEqual(self.s.totals()['agent1']['net'],0)
    def test_self_promotion_rejected(self):
        self.propose();self.verify()
        with self.assertRaises(MemoryError):promote(self.s,'c2','m','agent1',T3)
    def test_narrowing_requires_fresh_review(self):
        self.propose();c=self.candidate(candidate_id='narrow',supersedes='c1',occurred_at=T2,scope='one repository',actor='agent2')
        self.s.append('candidate',c)
        with self.assertRaises(MemoryError):promote(self.s,'narrow','m','agent2',T3)
        self.assertEqual(len(self.s.rows['candidate']),2)
    def test_rejected_never_retrieved(self):
        self.propose();self.verify(status='rejected');self.assertFalse(self.s.eligible(T3))
    def test_missing_falsifier_fails_closed(self):
        for i in range(1,4):self.s.append('episode',self.episode(i))
        with self.assertRaises(MemoryError):self.s.append('candidate',self.candidate(falsifier=''))
    def test_changed_verified_text_rejected(self):
        self.propose()
        with self.assertRaises(MemoryError):self.verify(proposed_lesson='All repositories are bad')
    def evidence(self,**kw):
        return dict(evidence_id='ev1',occurred_at='2026-10-24T12:00:00Z',supersedes=None,memory_id='learned1',agent='agent2',relation='contradicts',evidence_key='case4',significant=True,rationale='New source contained defect',evidence_refs=['docs/evidence.md'])|kw
    def test_contradiction_preserves_history_and_active_memory(self):
        self.promoted();before=(self.mem/'memories.jsonl').read_bytes();self.s.append('memory_evidence',self.evidence())
        self.assertEqual(before,(self.mem/'memories.jsonl').read_bytes());self.assertEqual(len(self.s.eligible('2026-10-25T12:00:00Z')),1)
        self.assertEqual(metrics(self.s)['memories_requiring_reevaluation'],['learned1'])
    def test_retraction_excludes_only_after_effective_time(self):
        self.promoted();self.s.append('reevaluation',dict(reevaluation_id='r1',occurred_at='2026-10-25T12:00:00Z',supersedes=None,memory_id='learned1',agent='agent1',reviewer='agent2',trigger='policy_change',outcome='retract',rationale='Applicability ended',replacement_memory_id=None,evidence_refs=['docs/evidence.md']))
        self.assertEqual(len(self.s.eligible('2026-10-24T12:00:00Z')),1);self.assertFalse(self.s.eligible('2026-10-26T12:00:00Z'))
        self.assertEqual(len(self.s.rows['memory']),1)
    def test_no_lesson_is_valid_consolidation(self):
        self.s.append('consolidation',dict(consolidation_id='check1',occurred_at=T1,supersedes=None,agent='agent1',session_id='s1',decision_ids=[],episode_ids=[],trigger_reasons=['explicit_flag'],result='NO LESSON CANDIDATE',candidate_ids=[],rationale='Insufficient independent evidence',evidence_refs=['docs/evidence.md']))
        self.assertEqual(metrics(self.s)['latest_consolidation_result'],'NO LESSON CANDIDATE')
        self.assertFalse(trigger(self.s,T3)['due'])
    def test_no_candidate_has_no_reward(self):
        self.s.append('episode',self.episode());self.assertEqual(self.s.totals()['agent1']['net'],0);self.assertFalse(self.s.rows['feedback'])
    def test_strong_single_event_requires_peer_judgment(self):
        self.s.append('episode',self.episode());self.s.append('candidate',self.candidate(path='strong_single_event',supporting_episode_ids=['e1'],support_count=1))
        with self.assertRaises(MemoryError):promote(self.s,'c1','m','agent1',T2)
    def test_private_or_missing_evidence_rejected(self):
        with self.assertRaises(MemoryError):self.s.append('episode',self.episode(evidence_refs=['/private/secret']))
    def test_partial_tail_fails_closed(self):
        (self.mem/'lesson_candidates.jsonl').write_text('{')
        with self.assertRaises(MemoryError):Store(self.root)
    def test_review_rejects_different_causes_policy_and_existing_lesson(self):
        self.propose()
        for check in ('records_support_pattern','not_owner_policy','novel_to_active_memory'):
            flags={k:True for k in self.candidate()['review_checks']};flags[check]=False
            with self.assertRaises(MemoryError):self.verify(review_checks=flags)
    def test_cross_agent_path_requires_both_agents(self):
        self.s.append('episode',self.episode(1));self.s.append('episode',self.episode(3))
        with self.assertRaises(MemoryError):self.s.append('candidate',self.candidate(path='cross_agent',supporting_episode_ids=['e1','e3'],support_count=2))
    def test_clock_requires_new_experience(self):
        self.assertFalse(trigger(self.s,'2027-01-01T00:00:00Z')['due'])
        self.s.append('episode',self.episode())
        self.assertIn('72_hours_with_experience',trigger(self.s,'2026-10-24T12:00:00Z')['trigger_reasons'])
    def test_episode_and_decision_alias_does_not_double_count(self):
        self.s.prepare(decision_id='d1',agent='agent1',task_id='task',task_type='review',session_id='1',query='test',at=T0)
        self.s.finish('d1','No lesson','Inspect source',at=T0)
        self.s.append('episode',self.episode(observation_key='decision:d1'))
        with self.assertRaises(MemoryError):self.s.append('candidate',self.candidate(path='strong_single_event',supporting_decision_ids=['d1'],supporting_episode_ids=['e1'],support_count=2))
    def test_promotion_idempotent(self):
        self.promoted();self.assertEqual(promote(self.s,'c2','learned1','agent2',T3)['id'],'learned1')
        self.assertEqual(len(self.s.rows['memory']),1)
    def test_replacement_excludes_predecessor(self):
        self.promoted()
        c=self.candidate(candidate_id='n1',created_at='2026-10-24T12:00:00Z',occurred_at='2026-10-24T12:00:00Z',scope='narrow source checks',replaces_memory_id='learned1')
        self.s.append('candidate',c)
        c=c|dict(candidate_id='n2',supersedes='n1',status='verified',reviewer='agent2',actor='agent2',reviewed_at='2026-10-25T12:00:00Z',occurred_at='2026-10-25T12:00:00Z',review_rationale='Narrow scope reviewed',review_checks={k:True for k in c['review_checks']})
        self.s.append('candidate',c);promote(self.s,'n2','learned2','agent2','2026-10-26T12:00:00Z')
        self.assertEqual([m['id'] for m in self.s.eligible('2026-10-27T12:00:00Z')],['learned2'])
    def test_false_reward_and_canary_remain_locked(self):
        self.promoted()
        for key,value in [('reward_influence',.1),('reward_mode','canary')]:
            p=self.mem/'config.v1.json';before=p.read_text();c=json.loads(before);c[key]=value;p.write_text(json.dumps(c))
            with self.assertRaises(MemoryError):Store(self.root)
            p.write_text(before)

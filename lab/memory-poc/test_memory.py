import json,unittest,tempfile
from pathlib import Path
from memory import Memory,reward_event,choose_task
DATA=json.loads((Path(__file__).parent/'memories.json').read_text())
class CoreTests(unittest.TestCase):
 def test_persistence_and_duplicate_after_restart(self):
  e=Memory(DATA);e.feedback('evidence-1','raw_evidence',1,True,100)
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'state.json';e.save(path);restored=Memory.load(path)
   self.assertEqual(restored.q,e.q);self.assertEqual(restored.records,e.records)
   self.assertFalse(restored.feedback('evidence-1','raw_evidence',1,True,100))
 def test_no_future(self):
  e=Memory(DATA);self.assertNotIn('regression_cause',[m['id'] for m in e.eligible(113,'agent1')])
 def test_superseded_success(self):
  e=Memory(DATA);e.q['final_only']=1
  self.assertNotIn('final_only',[m['id'] for m in e.retrieve('final section session log',50,mode='utility')])
 def test_correction_not_available_at_session_start(self):
  e=Memory(DATA);self.assertIn('peer_continuity',[m['id'] for m in e.eligible(49,'agent1')])
  self.assertNotIn('peer_continuity',[m['id'] for m in e.eligible(50,'agent1')])
 def test_private_memory(self):
  p=dict(DATA[0],id='secret',visibility='private',owner='agent2');e=Memory([p])
  self.assertEqual(e.retrieve('tool schemas',200,'agent1'),[]);self.assertEqual(len(e.retrieve('tool schemas',200,'agent2')),1)
 def test_feedback_cannot_change_foreign(self):
  p=dict(DATA[0],id='secret',visibility='private',owner='agent2');e=Memory([p])
  self.assertFalse(e.feedback('x','secret',1,True,200,'agent1'))
 def test_pending_no_punishment(self):
  self.assertIsNone(reward_event(verified=True,status='pending'))
 def test_blocked_no_punishment(self):
  self.assertIsNone(reward_event(verified=True,status='blocked'))
 def test_negative_hypothesis_can_help(self):
  self.assertGreater(reward_event(verified=True,status='completed',new_evidence=True),0)
 def test_no_reward_for_activity(self):
  self.assertEqual(reward_event(verified=True,status='completed'),0)
 def test_unverified_no_reward(self):
  self.assertIsNone(reward_event(status='completed',useful_result=True))
 def test_idempotence(self):
  e=Memory(DATA);e.feedback('x','raw_evidence',1,True,100);q=e.q.copy()
  self.assertFalse(e.feedback('x','raw_evidence',1,True,100));self.assertEqual(q,e.q)
 def test_useful_failure_memory(self):
  e=Memory(DATA);e.feedback('later-success','raw_evidence',1,True,100)
  self.assertGreater(e.q['raw_evidence'],.5)
 def test_unverified_update_rejected(self):
  e=Memory(DATA);self.assertFalse(e.feedback('x','raw_evidence',1,False,100));self.assertEqual(e.q['raw_evidence'],.5)
 def test_high_q_not_relevance(self):
  e=Memory([DATA[0]]);e.q['discovery']=1
  self.assertEqual(e.retrieve('photosynthesis chlorophyll',200,mode='utility'),[])
 def test_correction_affects_later_retrieval(self):
  e=Memory(DATA)
  self.assertIn('final_only',[m['id'] for m in e.eligible(47-0.1,'agent1')]);self.assertNotIn('final_only',[m['id'] for m in e.eligible(48,'agent1')])
 def test_known_error_penalty(self):
  self.assertLess(reward_event(verified=True,status='completed',repeated_known_error=True),0)
 def test_task_motor(self):
  common=dict(permitted=True,actionable=True,external_value=1,cost=1)
  tasks=[dict(common,id='repeat',learning_opportunity=0),dict(common,id='new_transfer',learning_opportunity=1),dict(common,id='forbidden',learning_opportunity=100,permitted=False)]
  self.assertEqual(choose_task(tasks),'new_transfer')
 def test_wait_not_active_work(self):
  self.assertIsNone(choose_task([dict(id='poll',permitted=True,actionable=False,external_value=1,learning_opportunity=1,cost=0)]))
 def test_invalid_reward(self):
  with self.assertRaises(ValueError):Memory(DATA).feedback('x','raw_evidence',10,True,100)
if __name__=='__main__':unittest.main(verbosity=2)

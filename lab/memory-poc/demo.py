"""Real-history-inspired, explicitly synthetic reward and task-choice demonstrations."""
import json
from pathlib import Path
from memory import Memory,reward_event,choose_task
p=Path(__file__).parent;e=Memory(json.loads((p/'memories.json').read_text()))
observations=[
 dict(source_session=73,event='click-policy-check',status='completed',verified=True,new_evidence=True),
 dict(source_session=113,event='distutils-review-correction',status='completed',verified=True,review_correction=True),
 dict(source_session=134,event='waiting-for-upstream',status='pending',verified=True),
 dict(source_session=148,event='new-occupied-candidate',status='completed',verified=True,new_evidence=True),
 dict(source_session=None,event='repeated-no-change-poll',status='completed',verified=True),
 dict(source_session=None,event='repeat-known-error',status='completed',verified=True,repeated_known_error=True),
]
for o in observations:o['proposed_reward']=reward_event(**{k:v for k,v in o.items() if k not in {'source_session','event'}})
# Outcome labels from the original ledger are deliberately NOT used as rewards.
e.feedback('synthetic-downstream-use','raw_evidence',1,True,120);e.save(p/'results/demo_state.json')
restored=Memory.load(p/'results/demo_state.json')
tasks=[dict(id='unchanged_upstream_poll',permitted=True,actionable=False,external_value=1,learning_opportunity=0,cost=.1),dict(id='eligible_external_candidate',permitted=True,actionable=True,external_value=1,learning_opportunity=.7,cost=.4),dict(id='lab_only_helper',permitted=False,actionable=True,external_value=0,learning_opportunity=1,cost=.2)]
result={'label':'SIMULATION, not observed reward or live agent behavior','reward_examples':observations,'task_examples':tasks,'chosen_task':choose_task(tasks),'failure_memory_q_after_synthetic_success':restored.q['raw_evidence'],'persistence_verified':e.q==restored.q}
(p/'results/demo.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

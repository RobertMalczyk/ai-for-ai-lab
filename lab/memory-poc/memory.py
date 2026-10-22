"""Dependency-free experimental memory engine. No LLM, model training or service access."""
import math,re,json,os
from pathlib import Path
from collections import Counter
STOP=set('a an the to of and or in on for with by at from is are was were be it its this that as my their before after whether what how same'.split())
def tokens(text):
    return [w for w in re.findall(r'[a-z0-9_]+',text.lower()) if w not in STOP]
def bm25(query,documents):
    docs=[Counter(tokens(d)) for d in documents]; q=set(tokens(query)); n=len(docs)
    if not n:return []
    avg=sum(sum(d.values()) for d in docs)/n or 1
    scores=[]
    for d in docs:
        score=0
        for w in q:
            df=sum(w in x for x in docs)
            idf=math.log(1+(n-df+.5)/(df+.5))
            f=d[w]; score+=idf*f*2.2/(f+1.2*(.25+.75*sum(d.values())/avg))
        scores.append(score)
    return scores
class Memory:
    def __init__(self,records,alpha=.2):
        self.records=records;self.alpha=alpha;self.q={m['id']:m.get('q_initial',.5) for m in records};self.events=set();self.updates=[]
    def save(self,path):
        path=Path(path); temporary=path.with_suffix(path.suffix+'.tmp')
        temporary.write_text(json.dumps({'records':self.records,'alpha':self.alpha,'q':self.q,'events':[list(x) for x in sorted(self.events)],'updates':self.updates},indent=2))
        os.replace(temporary,path)
    @classmethod
    def load(cls,path):
        state=json.loads(Path(path).read_text()); obj=cls(state['records'],state['alpha'])
        obj.q=state['q'];obj.events={tuple(x) for x in state['events']};obj.updates=state['updates']
        return obj
    def eligible(self,at,agent):
        return [m for m in self.records if m['source_session']<at and (m.get('invalidated_at') is None or at<=m['invalidated_at']) and (m['visibility']=='shared' or m.get('owner')==agent)]
    def retrieve(self,query,at,agent='agent1',mode='lexical',k=3,weight=.25,budget=3200):
        rows=self.eligible(at,agent)
        scores=bm25(query,[m['scope']+' '+m['lesson'] for m in rows]); maxs=max(scores,default=1) or 1
        # Phase A: relevant lexical candidates only. Q cannot introduce irrelevant memories.
        ranked=sorted([(s/maxs,m) for s,m in zip(scores,rows) if s>0],key=lambda x:(-x[0],x[1]['id']))[:8]
        if mode=='utility':ranked.sort(key=lambda x:(-((1-weight)*x[0]+weight*self.q[x[1]['id']]),x[1]['id']))
        elif mode=='recent':ranked=sorted([(0,m) for m in rows],key=lambda x:-x[1]['source_session'])
        out=[];used=0
        for s,m in ranked:
            size=len(m['lesson'])+len(m['scope'])
            if used+size>budget:continue
            out.append(dict(m,score=s,q=self.q[m['id']]))
            used+=size
            if len(out)==k:break
        return out
    def feedback(self,event_id,memory_id,reward,verified,at,agent='agent1'):
        # A transport/auth layer must enforce evaluator identity in production.
        if not verified or reward is None:return False
        if not -1<=reward<=1:raise ValueError('Reward outside [-1,1]')
        if memory_id not in {m['id'] for m in self.eligible(at,agent)}:return False
        key=(event_id,memory_id)
        if key in self.events:return False
        self.events.add(key);old=self.q[memory_id];target=(reward+1)/2
        self.q[memory_id]=old+self.alpha*(target-old)
        self.updates.append(dict(event=event_id,id=memory_id,old=old,new=self.q[memory_id],reward=reward,at=at))
        return True

def reward_event(*,verified=False,status='pending',new_evidence=False,useful_result=False,review_correction=False,repeated_known_error=False):
    """Proposed shaping rule, NOT a mapping of ledger positive/negative labels."""
    if not verified or status in {'pending','blocked','unknown','inconclusive'}:return None
    return max(-1,min(1,1.*useful_result+.2*new_evidence+.5*review_correction-.5*repeated_known_error))

def choose_task(tasks):
    """Bounded task-ranking demo. Features must be externally checked; not a scheduler."""
    candidates=[t for t in tasks if t['permitted'] and t['actionable'] and t['external_value']>0]
    if not candidates:return None
    # Learning is capped so invented novelty cannot outweigh task utility.
    def score(t):return t['external_value'] + .2*max(0,min(1,t['learning_opportunity'])) - .1*t['cost']
    return max(candidates,key=lambda t:(score(t),t['id']))['id']

"""Retrospective retrieval evaluation. Gold never enters retrieve(), only post-query feedback."""
import json,hashlib,statistics
from pathlib import Path
from memory import Memory,bm25
P=Path(__file__).parent
mem=json.loads((P/'memories.json').read_text());cases=json.loads((P/'cases.json').read_text());eps=json.loads((P/'episodes.json').read_text())
manifest=json.loads((P/'source_manifest.json').read_text())
for name,h in manifest['files'].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h
protocol={'fixed_before_first_run':True,'not_preregistered_externally':True,'dataset_construction':'author saw historical outcomes; manual retrospective queries and gold','temporal_boundary':'source_session < query_session; current snapshot may contain retrospective edits','variants':['recent','raw_bm25','lexical','utility'],'k':3,'utility_weight':.25,'alpha':.2,'q_initial':.5,'feedback':'gold-relevance proxy only, not observed downstream task reward','pass_pilot':'All core tests pass; lexical useful-prior-evidence hit@3 >= 0.80; no future/invalidated/private retrieval. Does not qualify autonomous reward learning.','full_memrl_gate':'Not assessed: requires prospective independently evaluated agent outcomes.'}
# Refuse silent changes to the protocol, dataset or engine after first evaluated run.
frozen={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['memories.json','cases.json','memory.py']}
lock=P/'protocol_lock.json'
if lock.exists():assert json.loads(lock.read_text())==frozen,'Changed frozen input; record a new experiment version'
else:lock.write_text(json.dumps(frozen,indent=2))
(P/'protocol.json').write_text(json.dumps(protocol,indent=2))

def run(mode,weight=.25):
    engine=Memory(mem);traces=[]
    for c in cases:
        if mode=='raw_bm25':
            rows=[e for e in eps if e['session']<c['at_session']]
            scores=bm25(c['query'],[e['text'] for e in rows]); selected=sorted(zip(scores,rows),key=lambda x:(-x[0],x[1]['session']))[:3]
            ids=[m['id'] for m in mem if any(m['source_session']==e['session'] for _,e in selected)]
            chars=sum(len(e['text']) for _,e in selected)
            source_ids=[e['session'] for _,e in selected]
        else:
            selected=engine.retrieve(c['query'],c['at_session'],mode=mode,weight=weight)
            ids=[m['id'] for m in selected];chars=sum(len(m['scope'])+len(m['lesson']) for m in selected);source_ids=[m['source_session'] for m in selected]
            assert all(m['source_session']<c['at_session'] and (m['invalidated_at'] is None or c['at_session']<=m['invalidated_at']) for m in selected)
        hits=set(ids)&set(c['relevant'])
        traces.append(dict(case=c['id'],query=c['query'],retrieved=ids,source_sessions=source_ids,expected=c['relevant'],hit=bool(hits),recall=len(hits)/len(c['relevant']),chars=chars))
        if mode=='utility':
            # Synthetic relevance feedback AFTER decision. Does not claim actual memory causality.
            for mid in ids:engine.feedback(c['id'],mid,1 if mid in c['relevant'] else -1,True,c['at_session'])
    return {'hits':sum(t['hit'] for t in traces),'n':len(traces),'hit_at_3':statistics.mean(t['hit'] for t in traces),'mean_recall_at_3':statistics.mean(t['recall'] for t in traces),'mean_context_chars':statistics.mean(t['chars'] for t in traces),'traces':traces,'updates':engine.updates,'final_q':engine.q if mode=='utility' else {}}
result={m:run(m) for m in protocol['variants']}
sensitivity={str(w):{k:v for k,v in run('utility',w).items() if k not in {'traces','updates','final_q'}} for w in [0,.1,.25,.5]}
(P/'results/retrieval.json').write_text(json.dumps(result,indent=2));(P/'results/sensitivity.json').write_text(json.dumps(sensitivity,indent=2))
summary={m:{k:v for k,v in r.items() if k not in {'traces','updates','final_q'}} for m,r in result.items()}
print(json.dumps(summary,indent=2));print('SENSITIVITY',json.dumps(sensitivity))

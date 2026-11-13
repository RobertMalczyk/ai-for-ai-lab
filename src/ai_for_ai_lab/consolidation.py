"""Memory V1.1 lifecycle. No inference, reward assignment or author authentication.

Agents supply explicit, public evidence and judgments; peer review verifies their
meaning. Machine checks prevent malformed histories and obvious duplicate counts.
"""
from datetime import timedelta
from .memory import AGENTS, MemoryError, require, timestamp, effective, now

JOURNALS = {'episode': ('selection_episodes', 'episode_id'),
            'candidate': ('lesson_candidates', 'candidate_id'),
            'consolidation': ('consolidations', 'consolidation_id'),
            'memory_evidence': ('memory_evidence', 'evidence_id'),
            'reevaluation': ('reevaluations', 'reevaluation_id')}


def support(store, candidate):
    """Return distinct observation identities, sessions and agents, not row count."""
    observations, sessions, agents = set(), set(), set()
    for kind, field, key in [('decision','supporting_decision_ids','decision_id'),
                              ('episode','supporting_episode_ids','episode_id')]:
        records = {r[key]: r for r in effective(store.rows[kind], key, timestamp(candidate['created_at']) + timedelta(microseconds=1))}
        for rid in candidate[field]:
            require(rid in records, 'missing or superseded supporting record')
            r = records[rid]
            require(timestamp(r['occurred_at']) <= timestamp(candidate['created_at']), 'future supporting evidence')
            # Episodes naming a decision use decision:<ID>; prevents cross-journal aliases.
            identity = r.get('observation_key', 'decision:' + r.get('decision_id', ''))
            if identity.startswith('decision:'):
                did = identity.split(':',1)[1]
                ds = {d['decision_id']: d for d in store.rows['decision']}
                require(did in ds, 'episode decision identity does not exist')
                r = ds[did]
                identity = 'task:' + r['agent'] + ':' + r['session_id'] + ':' + r['task_id']
            observations.add(identity)
            sessions.add(r['session_id']); agents.add(r['agent'])
    return observations, sessions, agents


def validate_all(store):
    rows = store.rows
    candidates = {r['candidate_id']:r for r in rows['candidate']}
    memories = {m['id']:m for m in rows['memory']}
    episode_keys = set()
    for r in rows['episode']:
        store._ref(r['policy_ref'])
        require(r['actionable_count'] <= r['candidate_count'], 'actionable exceeds candidates')
        require((r['outcome'] == 'candidate_found') == (r['actionable_count'] > 0), 'inconsistent selection outcome')
        if not r['supersedes']:
            require(r['observation_key'] not in episode_keys, 'duplicate observation')
            episode_keys.add(r['observation_key'])
        else:
            old = next(e for e in rows['episode'] if e['episode_id'] == r['supersedes'])
            require(all(r[f] == old[f] for f in ('observation_key','agent','session_id')), 'episode correction changes identity')
    immutable = ('created_at','proposer','pattern','scope','supporting_decision_ids',
                 'supporting_episode_ids','support_count','contradiction_count','proposed_lesson',
                 'actionable_implication','falsifier','confidence','path','mechanism',
                 'applicability_conditions','exceptions','counterevidence','novelty','replaces_memory_id')
    for c in rows['candidate']:
        require(timestamp(c['created_at']) <= timestamp(c['occurred_at']), 'candidate creation chronology')
        obs, sessions, agents = support(store,c)
        require(len(obs) == c['support_count'] and obs, 'support must count distinct observations')
        if c['path'] == 'repeated_pattern':
            require(len(obs) >= 3 and len(sessions) >= 2, 'repeated pattern requires 3 observations in 2 sessions')
        if c['path'] == 'cross_agent':
            require(len(obs) >= 2 and agents == set(AGENTS), 'cross-agent evidence required')
        parent = candidates.get(c['supersedes'])
        if parent:
            require(c['proposer'] == parent['proposer'], 'candidate proposer cannot change')
            require(parent['status'] not in ('rejected','superseded','promoted'), 'terminal candidate')
            if c['status'] in ('verified','promoted'):
                require(all(c[k] == parent[k] for k in immutable), 'changed lesson requires new provisional review')
            if c['status'] == 'provisional':
                require(c['promoted_memory_id'] is None, 'narrowing cannot promote')
        else:
            require(c['status'] == 'provisional' and c['actor'] == c['proposer'], 'candidate starts provisional')
        if c['status'] in ('verified','rejected','promoted'):
            require(c['reviewer'] in AGENTS and c['reviewer'] != c['proposer']
                    and c['actor'] == c['reviewer'], 'independent review required')
            require(c['reviewed_at'] and c['review_rationale'], 'review evidence required')
            require(timestamp(c['created_at']) <= timestamp(c['reviewed_at']) <= timestamp(c['occurred_at']), 'review chronology')
        if c['status'] in ('verified','promoted'):
            require(all(c['review_checks'].values()), 'review checklist incomplete')
        if c['status'] == 'verified':
            require(parent and parent['status'] == 'provisional', 'verification requires provisional predecessor')
        if c['status'] == 'promoted':
            require(parent and parent['status'] == 'verified', 'promotion requires verified predecessor')
            m = memories.get(c['promoted_memory_id'])
            require(m and m.get('source_candidate_id') == parent['candidate_id'], 'promotion must link exact verified candidate')
        else:
            require(c['promoted_memory_id'] is None, 'nonpromoted candidate has memory ID')
    promoted_candidates = set()
    for m in rows['memory']:
        cid = m.get('source_candidate_id')
        if not m['historical_seed'] and m['status'] == 'active':
            require(cid is not None, 'active learned memory requires candidate')
        if not cid:
            continue
        require(cid not in promoted_candidates, 'candidate already promoted')
        promoted_candidates.add(cid)
        require(not m['historical_seed'], 'learned memory cannot become historical seed')
        c = candidates.get(cid)
        require(c and c['status'] == 'verified', 'memory requires verified candidate')
        require(m.get('promoted_by') == c['reviewer'] != c['proposer'], 'self-promotion prohibited')
        require(m['author'] == c['proposer'] and m['source_refs'] == c['evidence_refs'], 'memory provenance mismatch')
        require(m['content'] == c['proposed_lesson'] and m['scope'] == c['scope']
                and m['exceptions'] == c['exceptions'] and m['confidence'] == c['confidence']
                and m.get('applicability_conditions') == c['applicability_conditions']
                and m.get('falsifier') == c['falsifier'], 'memory differs from reviewed lesson')
        require(timestamp(m['available_at']) >= timestamp(m['promoted_at']) >= timestamp(c['occurred_at']), 'promotion chronology')
        require(m['supersedes'] == c['replaces_memory_id'], 'replacement requires reviewed candidate')
        # A later rejection/narrowing invalidates a pending verified candidate.
        successors = [x for x in rows['candidate'] if x['supersedes'] == cid
                      and timestamp(x['occurred_at']) <= timestamp(m['promoted_at'])]
        require(not successors or all(x['status']=='promoted' and x['promoted_memory_id']==m['id'] for x in successors), 'candidate no longer verified at promotion')
    seen = set()
    for e in rows['memory_evidence']:
        require(e['memory_id'] in memories, 'unknown evidence memory')
        require(timestamp(e['occurred_at']) >= timestamp(memories[e['memory_id']]['available_at']), 'evidence predates memory')
        k = (e['memory_id'],e['evidence_key'])
        if not e['supersedes']:
            require(k not in seen, 'duplicate memory evidence'); seen.add(k)
        else:
            old = next(x for x in rows['memory_evidence'] if x['evidence_id']==e['supersedes'])
            require(k == (old['memory_id'],old['evidence_key']), 'evidence correction changes identity')
    for r in rows['reevaluation']:
        require(r['memory_id'] in memories, 'unknown reevaluation memory')
        require(timestamp(r['occurred_at']) >= timestamp(memories[r['memory_id']]['available_at']), 'reevaluation predates memory')
        if r['supersedes']:
            old = next(x for x in rows['reevaluation'] if x['reevaluation_id']==r['supersedes'])
            require(old['memory_id']==r['memory_id'], 'reevaluation changes memory')
        if r['outcome'] != 'pending':
            require(r['reviewer'] in AGENTS and r['reviewer'] != r['agent'], 'reevaluation requires peer review')
        if r['outcome'] in ('narrow_scope','supersede'):
            m = memories.get(r['replacement_memory_id'])
            require(m and m['supersedes'] == r['memory_id'] and m.get('source_candidate_id'), 'replacement must be independently promoted')
            require(timestamp(m['available_at']) <= timestamp(r['occurred_at']), 'future replacement')
        else:
            require(r['replacement_memory_id'] is None, 'unexpected replacement')
    for r in rows['consolidation']:
        require(r['supersedes'] is None, 'consolidation receipts are immutable; append a new check')
        for field,kind,key in [('decision_ids','decision','decision_id'),('episode_ids','episode','episode_id'),('candidate_ids','candidate','candidate_id')]:
            indexed={x[key]:x for x in rows[kind]}
            require(set(r[field]) <= indexed.keys(), 'unknown consolidation input')
            require(all(timestamp(indexed[k]['occurred_at']) <= timestamp(r['occurred_at']) for k in r[field]), 'future consolidation input')
        require(bool(r['candidate_ids']) == (r['result']=='CANDIDATE PROPOSED'), 'consolidation result mismatch')


def excluded(store, at):
    """Independent reevaluation can retract; contradiction alone cannot."""
    return {r['memory_id'] for r in effective(store.rows['reevaluation'],'reevaluation_id',timestamp(at))
            if r['outcome'] in ('retract','supersede','narrow_scope')}


def trigger(store, at=None, explicit=False):
    at = timestamp(at or now())
    past = [r for r in store.rows['consolidation'] if timestamp(r['occurred_at']) < at]
    last = max((timestamp(r['occurred_at']) for r in past), default=None)
    decisions = [r for r in store.rows['decision'] if timestamp(r['occurred_at']) <= at
                 and (last is None or timestamp(r['occurred_at']) > last)]
    episodes = [r for r in effective(store.rows['episode'],'episode_id') if timestamp(r['occurred_at']) <= at
                and (last is None or timestamp(r['occurred_at']) > last)]
    reasons=[]
    if explicit: reasons.append('explicit_flag')
    if len(decisions)>=5: reasons.append('five_material_decisions')
    experience=decisions+episodes
    # A clock alone is insufficient: there must be new relevant experience.
    start=last or min((timestamp(r['occurred_at']) for r in experience), default=at)
    if experience and at-start>=timedelta(hours=72): reasons.append('72_hours_with_experience')
    patterns={}
    for e in episodes:
        patterns.setdefault(e['pattern_key'],set()).add(e['observation_key'])
    if any(len(v)>=3 for v in patterns.values()): reasons.append('three_pattern_observations')
    return dict(due=bool(reasons),trigger_reasons=reasons,
                decision_ids=[d['decision_id'] for d in decisions],episode_ids=[e['episode_id'] for e in episodes])


def metrics(store):
    cs=effective(store.rows['candidate'],'candidate_id')
    ms=effective(store.rows['memory'],'id')
    learned={m['id'] for m in store.rows['memory'] if m.get('source_candidate_id')}
    ev=effective(store.rows['memory_evidence'],'evidence_id')
    ree=effective(store.rows['reevaluation'],'reevaluation_id')
    due=set()
    for mid in learned & {m['id'] for m in store.eligible(now())}:
        contradictions=[e for e in ev if e['memory_id']==mid and e['relation']=='contradicts']
        last=max((timestamp(r['occurred_at']) for r in ree if r['memory_id']==mid and r['outcome']!='pending'),default=None)
        new=[e for e in contradictions if last is None or timestamp(e['occurred_at'])>last]
        if len(new)>=2 or any(e['significant'] for e in new): due.add(mid)
    due.update(r['memory_id'] for r in ree if r['outcome']=='pending')
    last=store.rows['consolidation'][-1] if store.rows['consolidation'] else None
    return dict(selection_episodes=len(effective(store.rows['episode'],'episode_id')),
                material_decisions=len(store.rows['decision']),lesson_candidates=sum(not c['supersedes'] for c in store.rows['candidate']),
                provisional_candidates=sum(c['status']=='provisional' for c in cs),
                candidates_verified=sum(c['status'] in ('verified','promoted') for c in cs),
                candidates_rejected=sum(c['status']=='rejected' for c in cs),
                historical_seeds=sum(m['historical_seed'] for m in ms),
                active_memories=len(store.eligible(now())),promoted_learned_memories=len(learned),
                contradictions=sum(e['relation']=='contradicts' for e in ev),
                supersessions_retractions=sum(m['status'] in ('superseded','retracted') or bool(m['supersedes']) for m in store.rows['memory'])+sum(r['outcome']=='retract' for r in ree),
                memories_requiring_reevaluation=sorted(due),
                learned_memories_later_retrieved=len(learned & {mid for d in store.rows['decision'] for mid in d['memory_ids']}),
                learned_memories_positive_utility=len(learned & {u['memory_id'] for u in effective(store.rows['utility'],'assessment_id') if u['status']=='verified' and u['utility'] is not None and u['utility']>0}),
                last_consolidation_time=last['occurred_at'] if last else None,
                latest_consolidation_result=last['result'] if last else None)


def promote(store, candidate_id, memory_id, actor, at=None):
    at=at or now()
    completed=next((c for c in store.rows['candidate'] if c['supersedes']==candidate_id and c['status']=='promoted'),None)
    if completed:
        require(completed['promoted_memory_id']==memory_id and completed['reviewer']==actor, 'promotion retry changed identity')
        return next(m for m in store.rows['memory'] if m['id']==memory_id)
    c=next((c for c in effective(store.rows['candidate'],'candidate_id') if c['candidate_id']==candidate_id),None)
    require(c and c['status']=='verified' and actor==c['reviewer']!=c['proposer'], 'only independent reviewer can promote verified candidate')
    m=dict(id=memory_id,type='lesson',author=c['proposer'],visibility='public',created_at=c['created_at'],available_at=at,
           source_refs=c['evidence_refs'],scope=c['scope'],content=c['proposed_lesson'],exceptions=c['exceptions'],
           confidence=c['confidence'],evidence_status='verified',source_outcome='unknown',status='active',historical_seed=False,
           supersedes=c['replaces_memory_id'],correction_effective_at=at if c['replaces_memory_id'] else None,map_node_ids=[],
           source_candidate_id=candidate_id,applicability_conditions=c['applicability_conditions'],falsifier=c['falsifier'],promoted_at=at,promoted_by=actor)
    # Two recoverable appends: memory is authoritative, candidate completion follows.
    # On a retry use the stored promotion timestamp, preserving exact bytes.
    existing=next((m for m in store.rows['memory'] if m['id']==memory_id),None)
    if existing:
        require(existing.get('source_candidate_id')==candidate_id, 'memory ID already used')
        m=existing;at=m['promoted_at']
    store.append('memory',m)
    result=c|dict(candidate_id=candidate_id+'-promoted',supersedes=candidate_id,status='promoted',occurred_at=at,promoted_memory_id=memory_id,actor=actor)
    store.append('candidate',result)
    return m

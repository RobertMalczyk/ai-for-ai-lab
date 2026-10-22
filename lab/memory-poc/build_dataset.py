"""Curated retrospective annotations, not an independent/blinded dataset."""
import json,re
from pathlib import Path
P=Path(__file__).parent
raw=(P/'source/SESSIONS.md').read_text()
sections={int(re.search(r'Session (\d+)',s[:180])[1]):s for s in re.split(r'(?m)(?=^## )',raw) if re.search(r'Session (\d+)',s[:180])}
# id, source session, lesson, applicable context, invalidated at session
spec=[
('discovery',19,'When operation names are already reliable, retrieve exact schemas directly. Names-first is useful when names are not known. Byte savings are not token or decision-quality gains.','tool discovery schemas publication payload',None),
('read_boundary',20,'Read large mandatory documents in separate responses and verify scope through EOF. Requested output budget alone does not ensure complete delivery.','startup documents truncation context reading',None),
('final_only',46,'The final section alone reduced visible bytes in one scoped latest-session read. This does not establish complete multi-agent continuity.','startup latest session log continuity',47),
('peer_continuity',47,'A final-only session read can omit your own next step when another agent wrote last. Inspect your own preceding session; the peer audit proposed keeping the last non-Agent-2 section, with full continuity still to be checked.','startup session log author continuity',49),
('continuity_window',49,'Read from your latest relevant session through EOF, preserving intervening peer and administrator sections. The successful three-section example does not guarantee comprehension.','startup session log author continuity',None),
('append_anchor',49,'A patch anchored on a repeated next-step line inserted a session in the middle. Anchor ordered-log append on a unique latest heading and exact tail; verify final position.','edit append markdown session log patch placement',None),
('stable_status',53,'Keep volatile run counts in dated evidence and a verification command in current status. A fresh byte checkpoint can still contain stale factual claims.','status summary release version test count stale',None),
('exact_commands',55,'Replay receipts need exact commands at the named commits rather than prose requiring reconstruction. Commands were corrected and replayed in this episode.','receipt replay exact commands evidence',None),
('alias_correction',60,'Positional revisions and guessed base-ref flags were different mistakes. The alias pair was observed once, not twice; do not infer repeated evidence from similar failures.','manifest aliases flags evidence repeated claim',None),
('alias_confirmed',61,'The alias evidence correction preserves tested parser behavior but removes an unsupported repetition claim. Keep the historical correction linked to its original claim.','manifest aliases flags evidence correction',None),
('lock_commit',70,'Historical test replays require dependencies synchronized to the target commit lock. Reusing the current environment can produce unrelated collection errors.','historical replay dependencies environment lock pytest collection',None),
('project_policy',73,'Before external implementation, check the specific project contribution policy. Click prohibited AI-generated PRs in this observation; do not generalize this fact to other projects or future policy.','external OSS contribution policy preflight permission',None),
('outer_boundary',77,'Separate inner reads in one orchestration response still share a capped output budget. Use separate outer responses for large mandatory documents.','startup documents truncation outer response reading',None),
('compact_output',82,'Full-log capture plus a compact success receipt helped one noisy test suite. Expose full output on failure; benefit for a different consumer must be measured.','verification output bytes compact receipt noisy suite build',None),
('raw_evidence',88,'Stored SHA-256 strings do not make absent raw outputs independently verifiable. Retain minimal source bytes or label them ephemeral; missing evidence does not disprove the diagnosis.','evidence artifacts hashes raw logs verification replay',None),
('replay_inputs',90,'Existing evidence files are insufficient: each execution group needs a copyable command and every referenced local input. Do not silently reconstruct missing prerequisites.','evidence receipts commands inputs replay completeness',None),
('regression_cause',113,'A regression control must reach the reported failure, not an earlier TypeError. Check adjacent install and bytecode-output paths for the same missing-cache-tag defect.','distutils regression tests control cause build_py install_lib cache_tag',None),
('scope_output',116,'The concise site-build JSON did not meet the compaction threshold. Keep direct output for this consumer; do not generalize the noisy full-suite success.','verification output bytes compact receipt site build',None),
('create_ref',126,'An update_ref call failed with HTTP 422 for an absent branch; dedicated create_branch succeeded. Distinguish creation from update.','github branch ref create update HTTP422 publication',None),
('waiting',134,'Submitted distutils PR awaits an external response. With both tasks waiting, a new bounded discovery is allowed under WIP=1; submission is not acceptance.','external PR waiting no response discover WIP',None),
('existing_fix',135,'Check for an existing matching fix PR before reproduction or implementation. Reject occupied candidates and continue discovery elsewhere, not the whole project forever.','external OSS candidate preflight open issue existing fix PR duplicate',None),
('resolved_candidate',151,'Pathspec candidate was already fixed by a merged disclosed AI-assisted contribution. A rejected candidate does not imply the project rejects AI assistance; revisit for a new eligible bug.','external OSS project policy pathspec resolved merged candidate',None),
]
mem=[]
for id,n,lesson,scope,end in spec:
 mem.append(dict(id=id,source_session=n,lesson=lesson,scope=scope,invalidated_at=end,visibility='shared',owner=None,kind='lesson',q_initial=.5,source_heading=sections[n].splitlines()[0]))
# Queries describe a later decision, exclude its observed outcome. Gold is manually curated useful PRIOR evidence.
spec_cases=[
(22,'Read the mandatory startup documents completely despite a long log and output truncation.',['read_boundary']),
(49,'Recover my next step when the last session entry was written by the other agent.',['peer_continuity']),
(51,'Append a new Markdown session entry with a patch; repeated next-step lines occur throughout the log.',['append_anchor']),
(57,'A different agent needs to replay public receipts at their original commits without reconstructing commands.',['exact_commands']),
(61,'Check a claim that the same manifest alias flags were guessed twice.',['alias_correction']),
(64,'Correct documentation still claiming repeated manifest alias failures after an evidence review.',['alias_correction','alias_confirmed']),
(77,'Batch mandatory startup document reads in a single orchestration output without losing content.',['read_boundary']),
(90,'Verify whether a fresh checkout contains independently checkable raw artifacts behind reported hashes.',['raw_evidence']),
(92,'Review updated receipts for reproducibility: command blocks and referenced local inputs for each group.',['replay_inputs','exact_commands']),
(94,'Publish multiple file blobs through a capped connector response and check what was transferred.',['read_boundary','outer_boundary']),
(105,'Audit a pytest reproduction report for replayable commands and minimal inputs.',['replay_inputs','raw_evidence','exact_commands']),
(107,'A status summary describes a tested uv release as the current version after another release.',['stable_status']),
(114,'Evaluate revised distutils regression controls and the install_lib missing cache_tag path.',['regression_cause']),
(116,'Decide whether a compact output receipt should also wrap the separate site build.',['compact_output']),
(118,'Check whether reported historical numerical results have retrievable evidence before publishing a narrative.',['raw_evidence','stable_status']),
(128,'Create a known-absent feature branch through the GitHub connector.',['create_ref']),
(148,'An open external issue looks actionable; check for a competing fix before starting reproduction.',['existing_fix']),
(149,'Decide whether to work on an OSS issue when the maintainer has declined an AI-assisted contribution.',['project_policy']),
(150,'An external issue is open with no comments; decide what to check before coding.',['existing_fix']),
(151,'Inspect a new candidate in a project with few PRs before cloning or implementing a fix.',['existing_fix']),
]
cases=[dict(id=f'C{n:03}',at_session=n,query=q,relevant=r,scope='retrospective retrieval probe; not a new agent execution') for n,q,r in spec_cases]
(P/'memories.json').write_text(json.dumps(mem,indent=2))
(P/'cases.json').write_text(json.dumps(cases,indent=2))
(P/'episodes.json').write_text(json.dumps([{'session':n,'text':s} for n,s in sections.items()],indent=2))
print(f'{len(sections)} episodes, {len(mem)} curated memories, {len(cases)} probes')

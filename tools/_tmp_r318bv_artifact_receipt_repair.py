from pathlib import Path
import json

OLD_ID = '10340803017'
NEW_ID = '10341754652'
OLD_SIZE = '5957'
NEW_SIZE = '2596'
OLD_DIGEST = '5dee811012dda32203126105d6edc17a5067a0c9ec6299af32e12642515015f0'
NEW_DIGEST = 'd63f87cb137483ac2b6f669bed144e69bd3f61a8cc97756cd16fb47560bd4110'
FILES = [
    'MIMIR_CONTINUE_HERE.md',
    'MIMIR_KNOWLEDGE_GRAPH.md',
    'docs/continuity/MIMIR_BOUNDARY_LOCKS.md',
    'docs/continuity/MIMIR_CONTINUITY_STATE.json',
    'docs/continuity/MIMIR_CURRENT_STATE.md',
    'docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md',
    'docs/continuity/MIMIR_PROGRESS_LEDGER.md',
    'docs/continuity/MIMIR_R3_18BV_DECISION.md',
    'docs/continuity/MIMIR_R3_18BW_EXECUTION_SPEC.md',
]

counts = {'id': 0, 'size': 0, 'digest': 0}
for name in FILES:
    path = Path(name)
    text = path.read_text(encoding='utf-8')
    c_id = text.count(OLD_ID)
    c_digest = text.count(OLD_DIGEST)
    if c_id:
        text = text.replace(OLD_ID, NEW_ID)
        counts['id'] += c_id
    if c_digest:
        text = text.replace(OLD_DIGEST, NEW_DIGEST)
        counts['digest'] += c_digest
    # Size appears in receipt prose immediately adjacent to the artifact identity. Replace only
    # when this generated file still carries the old artifact identity/digest lineage.
    if c_id or c_digest:
        c_size = text.count(OLD_SIZE)
        if c_size:
            text = text.replace(OLD_SIZE, NEW_SIZE)
            counts['size'] += c_size
    path.write_text(text, encoding='utf-8', newline='\n')

if counts['id'] == 0 or counts['digest'] == 0:
    raise SystemExit(f'R3.18BV artifact repair did not find stale receipt: {counts}')

state = json.loads(Path('docs/continuity/MIMIR_CONTINUITY_STATE.json').read_text(encoding='utf-8'))
admission = state['r3_18bv_admission']
assert admission['artifact'] == 10341754652, admission
assert admission['artifact_size'] == 2596, admission
assert admission['artifact_digest'] == NEW_DIGEST, admission
assert admission['same_head_ci_job'] == 103931122833, admission
assert state['current_pass'] == 'R3.18BW'
print(f'R3_18BV_ARTIFACT_RECEIPT_REPAIR=PASS {counts}')

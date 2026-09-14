from pathlib import Path
import json

REPLACEMENTS = {
    '103932439965': '103931122833',
    '10340803017': '10341754652',
    '5957': '2596',
    '5dee811012dda32203126105d6edc17a5067a0c9ec6299af32e12642515015f0': 'd63f87d75c9c745cfab9b04116cbb3249bcdede7329a0ec8ea5371379548b982',
}
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

counts = {k: 0 for k in REPLACEMENTS}
for name in FILES:
    path = Path(name)
    text = path.read_text(encoding='utf-8')
    for old, new in REPLACEMENTS.items():
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            counts[old] += n
    path.write_text(text, encoding='utf-8', newline='\n')

if any(v == 0 for v in counts.values()):
    raise SystemExit(f'R3.18BV receipt repair incomplete: {counts}')

state = json.loads(Path('docs/continuity/MIMIR_CONTINUITY_STATE.json').read_text(encoding='utf-8'))
a = state['r3_18bv_admission']
assert a['same_head_ci_job'] == 103931122833
assert a['artifact'] == 10341754652
assert a['artifact_size'] == 2596
assert a['artifact_digest'] == 'd63f87d75c9c745cfab9b04116cbb3249bcdede7329a0ec8ea5371379548b982'
assert state['current_pass'] == 'R3.18BW'
print(f'R3_18BV_CONTINUITY_RECEIPT_REPAIR_V3=PASS counts={counts}')

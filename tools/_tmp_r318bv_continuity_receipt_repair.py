from pathlib import Path
import json

OLD = '103932439965'
NEW = '103931122833'
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

replacements = 0
for name in FILES:
    path = Path(name)
    text = path.read_text(encoding='utf-8')
    count = text.count(OLD)
    if count:
        text = text.replace(OLD, NEW)
        path.write_text(text, encoding='utf-8', newline='\n')
        replacements += count

if replacements == 0:
    raise SystemExit('R3.18BV continuity repair found no stale same-head CI job receipt')

state = json.loads(Path('docs/continuity/MIMIR_CONTINUITY_STATE.json').read_text(encoding='utf-8'))
assert state['r3_18bv_admission']['same_head_ci_job'] == 103931122833
assert state['current_pass'] == 'R3.18BW'
print(f'R3_18BV_CONTINUITY_RECEIPT_REPAIR=PASS replacements={replacements}')

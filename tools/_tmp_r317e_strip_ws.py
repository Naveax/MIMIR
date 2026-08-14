from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    'MIMIR_CONTINUE_HERE.md',
    'MIMIR_KNOWLEDGE_GRAPH.md',
    'docs/continuity/MIMIR_CONTINUITY_STATE.json',
    'docs/continuity/MIMIR_CURRENT_STATE.md',
    'docs/continuity/MIMIR_R3_17E_DECISION.md',
    'docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md',
]
for rel in FILES:
    p = ROOT / rel
    text = p.read_text(encoding='utf-8')
    p.write_text('\n'.join(line.rstrip() for line in text.splitlines()) + '\n', encoding='utf-8', newline='\n')

from pathlib import Path

paths = [
    Path('MIMIR_CONTINUE_HERE.md'),
    Path('MIMIR_KNOWLEDGE_GRAPH.md'),
    Path('docs/continuity/MIMIR_CONTINUITY_STATE.json'),
    Path('docs/continuity/MIMIR_CURRENT_STATE.md'),
    Path('docs/continuity/MIMIR_R3_17L_DECISION.md'),
    Path('docs/continuity/MIMIR_R3_17M_EXECUTION_SPEC.md'),
]
for path in paths:
    text = path.read_text(encoding='utf-8')
    lines = [line.rstrip() for line in text.splitlines()]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
print('generated continuity whitespace normalized')

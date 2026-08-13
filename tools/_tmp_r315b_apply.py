from pathlib import Path
import json

pairs = [
    ('tools/_tmp_r315b_continue.txt', 'MIMIR_CONTINUE_HERE.md'),
    ('tools/_tmp_r315b_graph.txt', 'MIMIR_KNOWLEDGE_GRAPH.md'),
    ('tools/_tmp_r315b_current.txt', 'docs/continuity/MIMIR_CURRENT_STATE.md'),
]
for source_name, target_name in pairs:
    source = Path(source_name).read_text(encoding='utf-8')
    target = Path(target_name)
    current = target.read_text(encoding='utf-8')
    heading = next(line for line in source.splitlines() if line.startswith('## '))
    if heading not in current:
        target.write_text(current.rstrip() + '\n' + source.strip('\n') + '\n', encoding='utf-8', newline='\n')

path = Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
state = json.loads(path.read_text(encoding='utf-8'))
state.update(json.loads(Path('tools/_tmp_r315b_state_patch.json').read_text(encoding='utf-8')))
for entry in ['docs/continuity/MIMIR_R3_15B_DECISION.md', 'docs/continuity/MIMIR_R3_15C_EXECUTION_SPEC.md']:
    if entry not in state.get('next_files_to_read', []):
        state.setdefault('next_files_to_read', []).append(entry)
path.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8', newline='\n')
print('R3_15B_CONTINUITY_UPDATE=PASS')

from pathlib import Path
import json
import runpy

runpy.run_path('tools/_tmp_r3_14e_continuity.py', run_name='__main__')
path = Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
state = json.loads(path.read_text(encoding='utf-8'))
state['r3_14e']['pre_admission_state'] = {'current_pass': 'R3.14E'}
path.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8', newline='\n')

from pathlib import Path
import json

path = Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
state = json.loads(path.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-13'
state['current_pass'] = 'R3.15B'
state['current_pass_kind'] = 'planning / contract / docs-only NewActor native contract admission'
state['current_pass_goal'] = 'Admit the exact additive native contract for the current supported NewActor branch without changing production Rust.'
state['current_pass_stop_boundary'] = 'Docs-only. Production remains frozen after the first actor new bit; R3.15C is closed until this contract is admitted.'
state['last_completed_evidence_pass'] = 'R3.15A'
state['last_completed_evidence_outcome'] = 'A — exact 47-replay / 169538-NewActor evidence admitted'
state['r3_15a'] = {
    'outcome': 'A — admitted / complete',
    'production_source_changed': False,
    'production_sha': '7b17cb9033b6c71d476e500380d78402cbb3c56d',
    'continuity_base_sha': 'a51c0c1bf8c8927f4e2f39691ec63403d70bb0a8',
    'oracle_sha': 'c70e77df7af81b436cb545d070bb90c82f562d0b',
    'evidence_head_sha': '1e27674625fdff26e05436e882014db5c7c5116d',
    'workflow_run': 31708322309,
    'workflow_job': 94474438951,
    'evidence_artifact_id': 9184200143,
    'evidence_artifact_sha256': 'a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d',
    'instrumentation_patch_sha256': '79010fb8923b365db0764bc56d2cadc48a6d257f2936fbd928fc24c08dc090e8',
    'driver_sha256': '44ddbd3f22f60b2959b889b46c68b57d9ef0bc8285ca97ba501ed1fd355e66ba',
    'full_stream_sha256': 'ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba',
    'witness_count': 59,
    'witness_sha256': 'e7dc38f64cee7b458517211e601cdc0133a6a5a799c1f718ab51d330b0e16573',
    'replays_total': 47,
    'oracle_decode_success': 47,
    'new_actor_total': 169538,
    'spawn_kind_match': 169538,
    'spawn_kind_mismatch': 0,
    'name_gate_true': 169538,
    'name_gate_false': 0,
    'next_pass': 'R3.15B'
}
for entry in ['docs/continuity/MIMIR_R3_15A_DECISION.md', 'docs/continuity/MIMIR_R3_15B_EXECUTION_SPEC.md']:
    if entry not in state.get('next_files_to_read', []):
        state.setdefault('next_files_to_read', []).append(entry)
path.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8', newline='\n')
print('STATE_UPDATE_PASS')

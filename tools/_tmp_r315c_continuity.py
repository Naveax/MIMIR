from pathlib import Path
import json

ROOT = Path('.')


def append_once(path: str, marker: str, block: str):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if marker in text:
        raise SystemExit(f'{path}: marker already present')
    p.write_text(text.rstrip() + '\n\n---\n\n' + block.strip() + '\n', encoding='utf-8')

append_once('MIMIR_CONTINUE_HERE.md', 'R3.15C PRODUCTION ADMITTED / ACTIVE R3.15D', '''
## R3.15C PRODUCTION ADMITTED / ACTIVE R3.15D

```text
production code SHA = bf4bccff82203ed049d33e942681fed07f23beb4
R3.15C              = COMPLETE / PRODUCTION
ACTIVE NEXT PASS    = R3.15D — 47-replay first-NewActor differential audit
```

R3.15C adds one additive first-NewActor reader. The independently admitted R3.14D envelope remains preserved; only `is_new == true` advances through raw signed `name_id`, one opaque bit, raw signed `object_id`, static spawn dispatch, and the selected `None | Location | LocationAndRotation` trajectory. The hard stop is the exact trajectory endpoint. Property bits, another actor/frame, lifecycle state, raw state, events and skills remain closed.

Read `docs/continuity/MIMIR_R3_15C_DECISION.md` and `docs/continuity/MIMIR_R3_15D_EXECUTION_SPEC.md` next.''')

append_once('MIMIR_KNOWLEDGE_GRAPH.md', 'LATEST CANONICAL OVERRIDE — R3.15C PRODUCTION / R3.15D ACTIVE', '''
## LATEST CANONICAL OVERRIDE — R3.15C PRODUCTION / R3.15D ACTIVE

```text
R3.15A NewActor evidence — COMPLETE / OUTCOME A
        |
        v
R3.15B NewActor contract — ADMITTED
        |
        v
R3.15C first NewActor native reader — PRODUCTION bf4bccff82203ed049d33e942681fed07f23beb4
        |
        v
R3.15D 47-replay first-NewActor native-vs-pinned-Boxcars differential — ACTIVE / EVIDENCE ONLY
```

Latest mandatory reading order begins with `MIMIR_CONTINUE_HERE.md`, structured/current continuity state, `MIMIR_R3_15C_DECISION.md`, `MIMIR_R3_15D_EXECUTION_SPEC.md`, then pass protocol, boundary locks, roadmap and ledger before the superbook/archive registry/matrix/mapping sources. Current source/tests and exact-SHA evidence remain authoritative.''')

append_once('docs/continuity/MIMIR_CURRENT_STATE.md', 'CURRENT OVERRIDE — R3.15C PRODUCTION / R3.15D ACTIVE', '''
## CURRENT OVERRIDE — R3.15C PRODUCTION / R3.15D ACTIVE

R3.15C is production at `bf4bccff82203ed049d33e942681fed07f23beb4`. It extends only the first `new == true` actor through its static-dispatched spawn trajectory and stops exactly there. R3.15D is evidence-only and must compare the first native NewActor on all 47 admitted replay identities against the exact R3.15A pinned-Boxcars oracle. Property decoding and all later runtime layers remain closed.''')

state_path = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(state_path.read_text(encoding='utf-8'))
if state.get('current_pass') != 'R3.15C':
    raise SystemExit(f"unexpected current_pass={state.get('current_pass')}")
state['last_production_code_sha'] = 'bf4bccff82203ed049d33e942681fed07f23beb4'
state['last_production_milestone'] = 'R3.15C'
state['last_production_milestone_name'] = 'first NewActor native reader through spawn trajectory'
state['current_pass'] = 'R3.15D'
state['current_pass_kind'] = 'evidence-only 47-replay first-NewActor native-vs-pinned-Boxcars differential audit'
state['current_pass_goal'] = 'Compare the R3.15C first NewActor result to exactly one frame-0 actor-0 R3.15A oracle row for every admitted replay identity with exact field and trajectory-stop equality.'
state['current_pass_stop_boundary'] = 'Evidence only. Production Rust is frozen; property_present, stream/property IDs, attributes, another actor/frame, lifecycle state, raw state, events and skills remain closed.'
state['closed_now'] = [x for x in state['closed_now'] if x not in {'native name_id decode','native spawn object payload decode','native spawn trajectory payload decode'}]
for f in ['docs/continuity/MIMIR_R3_15C_DECISION.md','docs/continuity/MIMIR_R3_15D_EXECUTION_SPEC.md']:
    if f not in state['next_files_to_read']:
        state['next_files_to_read'].append(f)
state['r3_15c'] = {
    'outcome': 'admitted / production',
    'pre_pass_main_sha': '77395d40af97620c58b39427a351b23aede84482',
    'production_sha': 'bf4bccff82203ed049d33e942681fed07f23beb4',
    'production_tree': '62cc2a970704cbf0d6545a02a45a8b1ef46c5c99',
    'source_file': 'crates/mimir-replay/src/lib.rs',
    'source_git_blob': 'f64a5e0d66962f41026b2eb10e176219d4529931',
    'builder_run': 31714929500,
    'builder_job': 94497112417,
    'clean_branch_ci_run': 31715088860,
    'published_main_ci_run': 31715564598,
    'focused_tests': 15,
    'production_scope_file_count': 1,
    'cargo_dependency_changed': False,
    'first_new_actor_reader_in_production': True,
    'property_loop_in_production': False,
    'next_pass': 'R3.15D'
}
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

(ROOT / 'docs/continuity/MIMIR_R3_15C_DECISION.md').write_text('''# MIMIR — R3.15C Production Decision

**Date:** 2026-08-13  
**Pass:** `R3.15C — first NewActor native reader through spawn trajectory`  
**Outcome:** **ADMITTED / PRODUCTION**

## Exact identity

```text
pre-pass main SHA      = 77395d40af97620c58b39427a351b23aede84482
production SHA         = bf4bccff82203ed049d33e942681fed07f23beb4
production tree        = 62cc2a970704cbf0d6545a02a45a8b1ef46c5c99
source file            = crates/mimir-replay/src/lib.rs
source Git blob        = f64a5e0d66962f41026b2eb10e176219d4529931
builder run / job      = 31714929500 / 94497112417
clean exact-SHA CI     = 31715088860
published-main CI      = 31715564598
```

The clean production commit is exactly one commit ahead of R3.15B and changes exactly one production file. Cargo files, dependencies, fixtures and corpus are unchanged.

## Admitted capability

R3.15C adds an independent additive first-NewActor reader while preserving the existing R3.14D first-envelope result. Absent/dead/not-new branches do not consume NewActor payload. A new branch consumes raw signed 32-bit name ID, one opaque bit, raw signed 32-bit object ID, dispatches only through the existing static spawn table, and decodes `None`, `Location`, or `LocationAndRotation` to the exact trajectory endpoint. Vector and rotation composites are cursor-atomic; negative/out-of-range object IDs fail closed.

Focused R3.15C tests, crate check and clippy passed in the builder lane; the clean candidate then passed the normal repository verifier on exact SHA before force-free publication. Published `main` readback matched the production SHA. Continuity publication additionally requires the published-main run above to be green.

## Still closed

`property_present`, stream/property IDs, attributes, next actor/frame, lifecycle mutation, raw state, events and skills remain closed.

## Next exact pass

`R3.15D — 47-replay first-NewActor native-vs-pinned-Boxcars differential audit`, evidence-only.
''', encoding='utf-8')

# The exact R3.15D spec is installed from a separately reviewed Git blob by the staging workflow.
print('R3_15C_CONTINUITY_PATCH=PASS')

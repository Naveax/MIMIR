from pathlib import Path
import json

ROOT = Path('.')

PRODUCTION_SHA = 'bf4bccff82203ed049d33e942681fed07f23beb4'
EVIDENCE_HEAD = '10e5d05383dbc09e19af997e896a825d8d16e3ae'
EVIDENCE_RUN = 31736738234
EVIDENCE_JOB = 94570077736
EVIDENCE_ARTIFACT_ID = 9195419601
EVIDENCE_ARTIFACT_DIGEST = 'sha256:f6e11055c11ed0724c45fcc76c13a9da2dbbb285ab3744f9738f0d4a19ecab8a'
NORMAL_CI_RUN = 31736738075
ORACLE_ARTIFACT_ID = 9184200143
ORACLE_ARTIFACT_DIGEST = 'sha256:a488b7d1620303e609a517eeb098367edd77f25a71022492d4fb46810290e81d'
ORACLE_FULL_STREAM_SHA = 'ef1635d0476606bff202ba6b4d2767a865248fc37ae4fc0dab5755922a4d5dba'
ORACLE_LANE_SHA = 'a5acaea07b636aac3cfab5de9fcdfd9669a0233242084c2bd6adc793d269b5cc'


def append_once(path: str, marker: str, block: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if marker in text:
        raise SystemExit(f'{path}: marker already present')
    p.write_text(text.rstrip() + '\n\n---\n\n' + block.strip() + '\n', encoding='utf-8')


append_once('MIMIR_CONTINUE_HERE.md', 'R3.15D COMPLETE / OUTCOME A / ACTIVE R3.16A', f'''
## R3.15D COMPLETE / OUTCOME A / ACTIVE R3.16A

```text
production code SHA = {PRODUCTION_SHA}
R3.15D evidence head = {EVIDENCE_HEAD}
R3.15D outcome       = A / 47 OF 47 EXACT FIRST-NEWACTOR DIFFERENTIAL
ACTIVE NEXT PASS     = R3.16A — existing-actor first-property envelope evidence
```

R3.15D recovered and verified the exact R3.15A artifact, revalidated its 169,538-row parent stream identity, selected exactly one frame-0/actor-0 oracle row for each of the 47 admitted replay identities, verified all 47 replay SHA-256 values, then compared the frozen R3.15C native reader against those 47 rows. All 21 admitted fields/presence flags/bit-stop gates matched 47/47; `identity_error_count=0`, `native_error_count=0`, `mismatch_count=0`, and production/Cargo mutation remained zero.

The 169,538-row parent stream was provenance-verified; **only the 47 selected first-NewActor rows were native-differentially compared in R3.15D**. Property payloads and later runtime layers remain closed. Read `docs/continuity/MIMIR_R3_15D_DECISION.md` and `docs/continuity/MIMIR_R3_16A_EXECUTION_SPEC.md` next.''')

append_once('MIMIR_KNOWLEDGE_GRAPH.md', 'LATEST CANONICAL OVERRIDE — R3.15D COMPLETE / R3.16A ACTIVE', f'''
## LATEST CANONICAL OVERRIDE — R3.15D COMPLETE / R3.16A ACTIVE

```text
R3.15C first NewActor native reader — PRODUCTION {PRODUCTION_SHA}
        |
        v
R3.15D 47-replay first-NewActor differential — COMPLETE / OUTCOME A
        |
        v
R3.16A existing-actor first-property envelope evidence — ACTIVE / EVIDENCE ONLY
        |
        v
native property envelope / attribute payload — CLOSED until separately admitted
```

R3.15D's exact evidence head is `{EVIDENCE_HEAD}`. Its immutable evidence artifact is `{EVIDENCE_ARTIFACT_ID}` with digest `{EVIDENCE_ARTIFACT_DIGEST}`. The parent R3.15A stream identity (169,538 NewActor rows) was verified, but the R3.15D native differential surface is exactly 47 first-NewActor rows, not 169,538 rows. Latest mandatory reading order begins with `MIMIR_CONTINUE_HERE.md`, structured/current state, `MIMIR_R3_15D_DECISION.md`, `MIMIR_R3_16A_EXECUTION_SPEC.md`, then pass protocol, boundary locks, roadmap and ledger.''')

append_once('docs/continuity/MIMIR_CURRENT_STATE.md', 'CURRENT OVERRIDE — R3.15D OUTCOME A / R3.16A ACTIVE', f'''
## CURRENT OVERRIDE — R3.15D OUTCOME A / R3.16A ACTIVE

R3.15D is complete with Outcome A against production `{PRODUCTION_SHA}`. Exact evidence run `{EVIDENCE_RUN}` compared 47 admitted first-NewActor rows and produced zero identity, native, or field/stop mismatches. The upstream R3.15A 169,538-row stream was revalidated only as provenance for the 47-row selector; it was not itself a 169,538-row native differential. R3.16A is now the evidence-only existing-actor first-property-envelope pass and must stop before attribute payload consumption or production mutation.''')

state_path = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(state_path.read_text(encoding='utf-8'))
if state.get('current_pass') != 'R3.15D':
    raise SystemExit(f"unexpected current_pass={state.get('current_pass')}")
if state.get('last_production_code_sha') != PRODUCTION_SHA:
    raise SystemExit(f"unexpected production SHA={state.get('last_production_code_sha')}")

state['last_completed_read_only_audit'] = 'R3.15D'
state['current_pass'] = 'R3.16A'
state['current_pass_kind'] = 'evidence-only existing-actor first-property envelope characterization'
state['current_pass_goal'] = 'Select and characterize one reproducible new == false and property_present == true actor update per admitted replay, resolving stream/property context and stopping exactly at attribute payload_start_bit.'
state['current_pass_stop_boundary'] = 'Evidence only. Production Rust is frozen; do not consume attribute payload, mutate actor lifecycle state, iterate a native property loop, or widen raw-state/event/skill/runtime surfaces.'
state['last_completed_evidence_pass'] = 'R3.15D'
state['last_completed_evidence_outcome'] = 'A — exact 47/47 first-NewActor native-vs-pinned-oracle differential; 0 identity/native/mismatch errors'
for f in ['docs/continuity/MIMIR_R3_15D_DECISION.md', 'docs/continuity/MIMIR_R3_16A_EXECUTION_SPEC.md']:
    if f not in state['next_files_to_read']:
        state['next_files_to_read'].append(f)
state['r3_15d'] = {
    'outcome': 'A — admitted / complete',
    'production_source_changed': False,
    'production_sha': PRODUCTION_SHA,
    'production_source_blob': 'f64a5e0d66962f41026b2eb10e176219d4529931',
    'pre_pass_main_sha': 'c59453812b8399aca8056b77c3ae4f45da33e44a',
    'evidence_head_sha': EVIDENCE_HEAD,
    'workflow_run': EVIDENCE_RUN,
    'workflow_job': EVIDENCE_JOB,
    'normal_ci_run': NORMAL_CI_RUN,
    'evidence_artifact_id': EVIDENCE_ARTIFACT_ID,
    'evidence_artifact_digest': EVIDENCE_ARTIFACT_DIGEST,
    'r3_15a_parent_artifact_id': ORACLE_ARTIFACT_ID,
    'r3_15a_parent_artifact_digest': ORACLE_ARTIFACT_DIGEST,
    'r3_15a_full_stream_rows': 169538,
    'r3_15a_full_stream_sha256': ORACLE_FULL_STREAM_SHA,
    'selected_oracle_rows': 47,
    'selected_oracle_lane_sha256': ORACLE_LANE_SHA,
    'replays_total': 47,
    'native_success': 47,
    'identity_error_count': 0,
    'native_error_count': 0,
    'mismatch_count': 0,
    'exact_field_gates': 21,
    'all_field_gate_matches': '21 gates x 47/47',
    'production_mutation_count': 0,
    'cargo_mutation_count': 0,
    'discarded_precanonical_harness_runs': [31719341428, 31735271685],
    'next_pass': 'R3.16A'
}
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

(ROOT / 'docs/continuity/MIMIR_R3_15D_DECISION.md').write_text(f'''# MIMIR — R3.15D Decision

**Date:** 2026-08-13  
**Pass:** `R3.15D — 47-replay first-NewActor native-vs-pinned-Boxcars differential audit`  
**Outcome:** **A — ADMITTED / COMPLETE**

## Exact identities

```text
pre-pass main SHA          = c59453812b8399aca8056b77c3ae4f45da33e44a
production SHA             = {PRODUCTION_SHA}
production source blob     = f64a5e0d66962f41026b2eb10e176219d4529931
evidence head              = {EVIDENCE_HEAD}
exact differential run/job = {EVIDENCE_RUN} / {EVIDENCE_JOB}
normal repository CI run   = {NORMAL_CI_RUN}
evidence artifact ID       = {EVIDENCE_ARTIFACT_ID}
evidence artifact digest   = {EVIDENCE_ARTIFACT_DIGEST}
```

## Oracle provenance

```text
R3.15A artifact ID          = {ORACLE_ARTIFACT_ID}
R3.15A artifact digest      = {ORACLE_ARTIFACT_DIGEST}
R3.15A full stream rows     = 169538
R3.15A full stream SHA-256  = {ORACLE_FULL_STREAM_SHA}
R3.15D selected rows        = 47
R3.15D selected lane SHA256 = {ORACLE_LANE_SHA}
```

The exact R3.15A artifact digest was revalidated through the GitHub Actions artifact API before use. Its 169,538-row NewActor JSONL was rehashed and row-count checked. Exactly one `frame_index == 0 && actor_ordinal == 0` row was selected for each of the exact 47 admitted replay paths, and every replay byte stream was SHA-256 checked against its oracle identity.

**Scope clarification:** the 169,538-row parent stream is provenance evidence. R3.15D native-differentially compared exactly 47 selected first-NewActor rows.

## Differential result

```text
replays_total        = 47
oracle_rows_selected = 47
native_success       = 47
identity_error_count = 0
native_error_count   = 0
mismatch_count       = 0
```

All 21 admitted comparison gates matched **47/47**:

```text
actor_present
actor_id
alive
is_new
envelope_stop
name_id
opaque
object_id
spawn_kind
location_presence
location_x
location_y
location_z
rotation_presence
yaw_presence
yaw
pitch_presence
pitch
roll_presence
roll
trajectory_stop
```

The evidence run also re-audited the source boundary after the differential: production mutation count `0`, Cargo mutation count `0`, fixture/corpus mutation count `0`.

## Pre-canonical attempts

Runs `31719341428` and `31735271685` are **not parser mismatch evidence**. The first stopped at rustfmt before the differential; the second used a malformed copied TSV harness and stopped on its own field-count assertion. Neither changed production. They are superseded by exact run `{EVIDENCE_RUN}`, which derives the 47 oracle rows directly from the verified R3.15A artifact at runtime.

## Decision

R3.15C first-NewActor parsing is admitted across the exact current 47-replay first-NewActor surface. R3.15D is closed with Outcome A. This does not admit property decoding, lifecycle state, raw state, events, slicing, skills, or runtime widening.

## Next pass

`R3.16A — existing-actor first-property envelope evidence`, evidence-only. The roadmap-defined hard stop is `payload_start_bit`, before attribute payload consumption.
''', encoding='utf-8')

print('R3_15D_CONTINUITY_PATCH=PASS')

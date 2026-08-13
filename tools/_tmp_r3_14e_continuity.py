from pathlib import Path
import json

DECISION = r'''# MIMIR — R3.14E Differential Admission Decision

**Date:** 2026-08-13
**Pass:** `R3.14E — native first-envelope differential audit`
**Outcome:** **ADMITTED / OUTCOME A**
**Production Rust changed:** **NO**

## Frozen production identity

```text
production SHA      = 7b17cb9033b6c71d476e500380d78402cbb3c56d
continuity base     = b06a967b31e971431caa415721661088c630fdbc
production reader   = MinimalReplayNetworkFirstActorEnvelopeReader
hard stop           = after new / bit 78 on the supported lane
```

## Immutable oracle identity

```text
oracle repo                 = nickbabcock/boxcars
oracle SHA                  = c70e77df7af81b436cb545d070bb90c82f562d0b
R3.14A evidence head        = f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
R3.14A workflow run         = 31690714121
R3.14A artifact ID          = 9177314099
R3.14A artifact SHA-256     = d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b
selector manifest SHA-256   = 28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55
oracle rows                 = 47
```

The preserved R3.14A artifact was recovered by exact run/artifact identity. Its GitHub digest and independently downloaded ZIP byte digest both matched the canonical SHA-256 above.

## R3.14E evidence identity

```text
evidence branch head        = 96b5a2ee298bfa4dc88d320b13459646931b82a6
workflow run                = 31705946564
workflow job/check          = 94466421975 SUCCESS
artifact ID                 = 9183181430
artifact SHA-256            = 8cdbf0d3d9e96ff4f508e3da8fa913f53c76bb27061805f2059ddf72d4d06bed
preparer SHA-256            = a57b45fd727b1d9a38fb551c260aa6ba75896ccfcd1707eba2be41c73acdb559
native probe SHA-256        = 01398ac47faf9dd4a279f7d127de0c978693f9687459540e08f16f4178a4589c
```

The R3.14E artifact ZIP byte digest independently matched the GitHub artifact digest.

## Exact aggregate result

```text
replays_total               = 47
replays_unique_sha          = 47
native_parse_success        = 47
oracle_rows                 = 47
time_raw_match              = 47
delta_raw_match             = 47
actor_present_match         = 47
actor_id_match              = 47
alive_match                 = 47
new_match                   = 47
stop_bit_match              = 47
structural_context_match    = 47
build_version_match         = 47
mismatch_count              = 0
native_error_count          = 0
identity_error_count        = 0
production_source_mutation  = 0
```

The temporary native probe executed one integration test over the exact 47 replay identities and reported `R3_14E_NATIVE_PARSE_SUCCESS=47` and `R3_14E_EXACT_MATCH=47`.

## Admission decision

R3.14D is now differentially admitted across the current 47-replay supported lane through the first actor `new` bit. No production capability beyond that bit is implied.

Still closed:

```text
name_id
unnamed post-new bit
object_id
spawn location / rotation payload
property loop
stream_id / attribute payload
second actor / second frame production iteration
actor lifecycle state mutation
raw state / events / skills
```

## Next exact pass

`R3.15A — NewActor branch read-only differential evidence`.
'''

SPEC = r'''# MIMIR — R3.15A Exact Execution Spec

**Pass:** `R3.15A — NewActor branch read-only differential evidence`
**Pass type:** evidence-only / pinned-oracle instrumentation
**Production base:** `7b17cb9033b6c71d476e500380d78402cbb3c56d`
**Production Rust changes:** forbidden

## Goal

Characterize the wire contract immediately after an actor whose `new` bit is true, using the exact pinned Boxcars implementation and the current 47-replay supported corpus. This pass is evidence only. It must not add native NewActor parsing.

## Required source authorities

```text
Boxcars SHA = c70e77df7af81b436cb545d070bb90c82f562d0b
MIMIR production SHA = 7b17cb9033b6c71d476e500380d78402cbb3c56d
```

Pinned Boxcars `parse_new_actor` establishes the sequence:

```text
version-gated name_id: i32 when enabled
unnamed one-bit field
object_id: i32
spawn trajectory selected by object-index spawn plan
trajectory payload according to None / Location / LocationAndRotation
```

The Boxcars name gate to instrument exactly is:

```text
version >= (868,20,0)
OR
(version >= (868,14,0) AND !is_lan)
```

The current MIMIR static lookup plan already admits the same spawn-kind domain:

```text
None
Location
LocationAndRotation
```

R3.15A may compare that static plan with the oracle-selected spawn kind, but it may not consume these fields in production Rust.

## Input identity gate

Use the same exact 47 replay identities admitted by R3.14E. Before oracle instrumentation require:

```text
input_count = 47
unique_sha256 = 47
all replay files exist
all byte lengths match
all SHA-256 values match
BuildVersion identity preserved
```

Any identity mismatch is Outcome C until repaired.

## Evidence selection policy

Decode the supported replays with pinned Boxcars and inspect every encountered `new == true` actor for aggregate counts. Preserve a deterministic exact witness set containing at least:

1. the first NewActor occurrence in every replay;
2. the first occurrence of every observed `(build/version family, is_lan, name_id gate, spawn kind)` family;
3. the first occurrence of every distinct spawn kind;
4. object-id minimum and maximum witnesses;
5. location/rotation payload-length minimum and maximum witnesses for every observed spawn kind that carries payload.

If the full row set is reasonably bounded, preserve all NewActor rows as JSONL. Otherwise preserve aggregate counts plus the deterministic witness set and a digest over the full instrumentation stream.

## Fields to record for every retained witness

### Context

```text
replay path / SHA-256
BuildVersion
network_start / network_size
frame index
actor ordinal within frame
actor_id
new_bit_end
branch_start_bit
version triplet
net_version
is_lan
```

### Name gate

```text
do_parse_name
name_id_present
name_id_value
name_id_start_bit
name_id_end_bit
```

When the gate is false, no name bits may be consumed.

### Opaque one-bit field

```text
opaque_bit_value
opaque_bit_start
opaque_bit_end
```

Do not assign semantics to this bit in R3.15A.

### Object identity

```text
object_id_value
object_id_start_bit
object_id_end_bit
object_table_length
object_id_in_range
object_name when in range
```

Boxcars reads `object_id` as raw signed `i32`; do not silently replace this with a bounded-integer hypothesis.

### Spawn selection

```text
oracle_spawn_kind
mimir_static_spawn_kind
spawn_kind_match
trajectory_start_bit
trajectory_end_bit
```

### Location payload when present

Record the exact decoded integer vector and bit range:

```text
location_start_bit
location_end_bit
location_x_i32
location_y_i32
location_z_i32
```

Pinned Boxcars `Vector3i::decode` uses a variable component width derived from the encoded size prefix and `net_version`; R3.15A records observed bit consumption rather than inventing a fixed-width contract.

### Rotation payload when present

Record:

```text
rotation_start_bit
rotation_end_bit
yaw_present / yaw_i8
pitch_present / pitch_i8
roll_present / roll_i8
```

Pinned Boxcars rotation encoding uses a presence bit per component followed by an `i8` only when present. Preserve raw bit ranges so R3.15B can admit the exact contract.

### Branch endpoint

```text
branch_end_bit
branch_bit_length
```

## Aggregate distributions

At minimum compute:

```text
replays_total
oracle_decode_success
new_actor_total
name_gate_true / false
name_id_present count
spawn_none count
spawn_location count
spawn_location_rotation count
object_id_min / max
invalid_object_id count
mimir_spawn_kind_match / mismatch
location_payload_bit_length min / max
rotation_payload_bit_length min / max
instrumentation_error_count
```

Do not invent expected counts before observing the pinned corpus.

## Hard stop

R3.15A must stop at the end of the NewActor spawn trajectory. It must not instrument or admit as part of this pass:

```text
property_present loop for later existing-actor updates
stream_id
attribute payload semantics
second-frame production iteration
actor lifecycle mutation policy
raw-state mapping
events
skills
```

Oracle decoding may naturally continue so Boxcars can reach later NewActor occurrences, but the retained R3.15A row for each occurrence ends at that NewActor branch endpoint.

## Outcome model

### Outcome A — evidence sufficient

All 47 replay identities are verified; pinned oracle decoding succeeds on the supported lane; the name gate, opaque bit, object-id read, spawn dispatch, payload values/bit ranges, and static-spawn comparison have no unexplained divergence. Then create `R3.15B — NewActor contract admission`.

### Outcome B — bounded format family or mismatch

Preserve the failing replay/witness identities and the first divergent field/bit. Split the smallest additional evidence pass required. Do not change production Rust.

### Outcome C — identity/provenance invalid

No NewActor contract claim is admitted until the oracle/corpus identity gap is repaired.

## Completion artifact

Record at least:

```text
production SHA
oracle SHA
47-replay identity source
instrumentation head / tool SHA
artifact SHA-256
aggregate distributions
deterministic witness-set identity
mismatch/error list
outcome
next exact pass
```

Continuity and `MIMIR_KNOWLEDGE_GRAPH.md` update only after R3.15A is actually admitted.
'''

APPENDS = {
    'MIMIR_CONTINUE_HERE.md': r'''

---

## R3.14E OUTCOME A ADMITTED / ACTIVE R3.15A

> **CURRENT OVERRIDE:** exact source/tests/evidence remain authoritative over prose.

```text
production code SHA = 7b17cb9033b6c71d476e500380d78402cbb3c56d
R3.14D              = PRODUCTION + 47/47 DIFFERENTIAL ADMISSION
R3.14E              = COMPLETE / OUTCOME A
ACTIVE NEXT PASS    = R3.15A — NewActor branch read-only differential evidence
```

R3.14E evidence run `31705946564`, job `94466421975`, artifact `9183181430` proved exact 47/47 equality for raw time/delta, actor-present/id/alive/new, stop bit, BuildVersion, and structural context with zero mismatch/error and zero production mutation.

R3.15A is evidence-only. Production remains frozen before `name_id` and all NewActor spawn fields.
''',
    'MIMIR_KNOWLEDGE_GRAPH.md': r'''

---

## LATEST CANONICAL OVERRIDE — R3.14E ADMITTED / R3.15A ACTIVE

```text
R3.14D native first actor envelope — PRODUCTION 7b17cb9033b6c71d476e500380d78402cbb3c56d
        |
        v
R3.14E exact 47-replay differential — COMPLETE / OUTCOME A
        |
        v
R3.15A NewActor branch read-only evidence — ACTIVE
        |
        v
R3.15B NewActor contract — CLOSED until R3.15A admission
```

Latest mandatory reading order begins with `MIMIR_CONTINUE_HERE.md`, structured/current continuity state, `MIMIR_R3_14E_DECISION.md`, and `MIMIR_R3_15A_EXECUTION_SPEC.md`, then pass protocol/boundary locks/roadmap/ledger before the superbook and archive registry/matrix/mapping documents.
''',
    'MIMIR_ALL_SOURCES_SUPERBOOK.md': r'''

---

## CURRENT REPLAY DECODER ADMISSION UPDATE — R3.14E OUTCOME A / R3.15A ACTIVE

The native R3.14D first-envelope reader is now differentially admitted 47/47 against the exact pinned R3.14A Boxcars oracle. R3.15A is the evidence-only NewActor branch pass. It studies the version-gated name ID, opaque bit, raw object ID, static spawn-kind dispatch, and location/rotation trajectory wire ranges without changing production Rust.
''',
    'docs/continuity/MIMIR_CURRENT_STATE.md': r'''

---

## CURRENT OVERRIDE — R3.14E COMPLETE / R3.15A ACTIVE

R3.14E completed with Outcome A: exact 47/47 native-vs-pinned-Boxcars first-envelope equality and zero mismatch/error. Production code remains `7b17cb9033b6c71d476e500380d78402cbb3c56d`. The active pass is now R3.15A, read-only NewActor branch evidence through the spawn trajectory endpoint. No production `name_id`, object ID, or spawn payload reader is admitted yet.
''',
    'docs/continuity/MIMIR_BOUNDARY_LOCKS.md': r'''

---

## CURRENT OVERRIDE — At R3.15A

OPEN / ADMITTED:

```text
R3.14D first actor envelope through new
R3.14E 47/47 differential admission
static object-index spawn-kind lookup plan
```

R3.15A is EVIDENCE-ONLY. It may instrument pinned Boxcars through one NewActor spawn trajectory and compare static spawn-kind selection. Production decoding remains CLOSED for `name_id`, opaque post-new bit, `object_id`, location/rotation spawn payloads, properties, actor/frame iteration, state, events, and skills.
''',
    'docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md': r'''

---

## CURRENT EXECUTION OVERRIDE — R3.15A ACTIVE

R3.14E is COMPLETE / OUTCOME A with exact 47/47 first-envelope differential equality. The first incomplete canonical pass is R3.15A, NewActor branch read-only evidence. R3.15B and later passes remain closed.
''',
    'docs/continuity/MIMIR_PROGRESS_LEDGER.md': r'''

---

## 2026-08-13 — R3.14E admitted

- Production base remained `7b17cb9033b6c71d476e500380d78402cbb3c56d`.
- Exact 47 replay identities verified.
- Pinned Boxcars oracle identity verified.
- Native first-envelope exact matches: 47/47 for all required fields and structural context.
- Mismatch/native-error/identity-error: 0/0/0.
- Production source mutation: 0.
- Outcome A admitted.
- Next: R3.15A evidence-only NewActor branch audit.
''',
    'docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md': r'''

---

## CURRENT HANDOFF OVERRIDE — R3.15A

Fresh main must show R3.14E Outcome A admitted. Read `MIMIR_R3_14E_DECISION.md` and `MIMIR_R3_15A_EXECUTION_SPEC.md`. Continue only with pinned-Boxcars NewActor branch evidence. Do not change production Rust and stop retained evidence at each NewActor spawn trajectory endpoint.
''',
    'docs/continuity/README.md': r'''

### Current replay-decoder pass

- `MIMIR_R3_14E_DECISION.md` — exact 47-replay first-envelope differential admission, Outcome A.
- `MIMIR_R3_15A_EXECUTION_SPEC.md` — active evidence-only NewActor branch pass.
''',
}

Path('docs/continuity/MIMIR_R3_14E_DECISION.md').write_text(DECISION, encoding='utf-8', newline='\n')
Path('docs/continuity/MIMIR_R3_15A_EXECUTION_SPEC.md').write_text(SPEC, encoding='utf-8', newline='\n')

for name, block in APPENDS.items():
    path = Path(name)
    text = path.read_text(encoding='utf-8')
    marker = block.strip().splitlines()[2] if len(block.strip().splitlines()) > 2 else block.strip().splitlines()[0]
    if marker not in text:
        path.write_text(text.rstrip() + '\n' + block.strip('\n') + '\n', encoding='utf-8', newline='\n')

state_path = Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-13'
state['current_pass'] = 'R3.15A'
state['current_pass_kind'] = 'evidence-only pinned-oracle NewActor branch differential audit'
state['current_pass_goal'] = 'Instrument every encountered new actor for aggregate distributions and preserve deterministic exact witnesses for the version-gated name_id, opaque bit, raw object_id, static spawn-kind dispatch, and spawn trajectory bit ranges/values.'
state['current_pass_stop_boundary'] = 'Evidence only. Retained rows stop at the end of each NewActor spawn trajectory. Production Rust remains frozen before name_id; property payloads, actor/frame iteration, state, events, and skills remain closed.'
state['last_completed_evidence_pass'] = 'R3.14E'
state['last_completed_evidence_outcome'] = 'A — exact 47/47 native first-envelope differential match'
state['r3_14d']['differential_47_replay_admitted'] = True
state['r3_14e'] = {
    'outcome': 'A — admitted / complete',
    'production_source_changed': False,
    'production_sha': '7b17cb9033b6c71d476e500380d78402cbb3c56d',
    'continuity_base_sha': 'b06a967b31e971431caa415721661088c630fdbc',
    'oracle_sha': 'c70e77df7af81b436cb545d070bb90c82f562d0b',
    'oracle_evidence_head': 'f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1',
    'oracle_artifact_id': 9177314099,
    'oracle_artifact_sha256': 'd404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b',
    'selector_manifest_sha256': '28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55',
    'evidence_head_sha': '96b5a2ee298bfa4dc88d320b13459646931b82a6',
    'workflow_run': 31705946564,
    'workflow_job': 94466421975,
    'evidence_artifact_id': 9183181430,
    'evidence_artifact_sha256': '8cdbf0d3d9e96ff4f508e3da8fa913f53c76bb27061805f2059ddf72d4d06bed',
    'preparer_sha256': 'a57b45fd727b1d9a38fb551c260aa6ba75896ccfcd1707eba2be41c73acdb559',
    'native_probe_sha256': '01398ac47faf9dd4a279f7d127de0c978693f9687459540e08f16f4178a4589c',
    'replays_total': 47,
    'native_parse_success': 47,
    'exact_match': '47/47',
    'mismatch_count': 0,
    'native_error_count': 0,
    'identity_error_count': 0,
    'hard_stop_bit': 78,
    'next_pass': 'R3.15A'
}
next_files = state.get('next_files_to_read', [])
for entry in ['docs/continuity/MIMIR_R3_14E_DECISION.md', 'docs/continuity/MIMIR_R3_15A_EXECUTION_SPEC.md']:
    if entry not in next_files:
        next_files.append(entry)
state['next_files_to_read'] = next_files
state_path.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8', newline='\n')

print('R3_14E_CONTINUITY_UPDATE=PASS')

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CANONICAL = '''REPOSITORY: Naveax/MIMIR
DEFAULT_BRANCH: main
LANGUAGE: Rust 2024 workspace
RUST_VERSION_FLOOR: 1.85

LAST_PRODUCTION_CODE_SHA:
  c3d4c73ca34febb9f0383c59132a8bc8a363b06b

LAST_PRODUCTION_MILESTONE:
  R3.17C — native primitive scalar attribute decoder implementation

LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.17E — K2 object/reference/text wire evidence / Outcome A / 47/47 / 110539 occurrences

LAST_COMPLETED_CONTRACT_PASS:
  R3.17B — primitive scalar attribute wire contract / Outcome A

CURRENT_PASS:
  R3.17F — evidence-supported K2 object/reference/text contract admission

CURRENT_PASS_TYPE:
  contract-only / NO production Rust capability widening

CURRENT_SUPPORTED_REPLAY_LANE:
  47 replays

CHECKED_IN_REPLAY_SET:
  103 total = 3 historical fixtures + largest_100 stress corpus

PINNED_BOXCARS_ORACLE:
  repository: nickbabcock/boxcars
  exact SHA: c70e77df7af81b436cb545d070bb90c82f562d0b

CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar payload may be decoded natively
  stop exactly at payload_end_bit / stop_bit after that one scalar
  NO native K2 decoder, second property, next actor, next frame, K3 or K4 family is admitted

R3_17E_EVIDENCE_CLOSURE:
  evidence head: 19db534a3668f84f1c5ce36ef1252c52841d890f
  authority run/job: 31801482588 / 94770260529 SUCCESS
  exact-head normal CI: 31801482499 / 94770260054 SUCCESS
  artifact: 9219554878
  artifact digest: sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
  47/47 oracle decode; 110539 K2 occurrences
  ActiveActor: 86200; String: 14670; QWordString: 2920; UniqueId: 6443; PartyLeader: 306
  shape/unclassified: 0; bit monotonicity: 0; raw-payload-shape failures: 0
  privacy-safe output: PASS
  production/Cargo/corpus mutation: 0/0/0
  aggregate SHA256: 335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751
  summary SHA256: 9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e
  oracle JSONL SHA256: 196f4e4d2a588137ad12372cb2f0af79d7fca422c0bc2c5dea95506fa72cac4d
  witnesses JSONL SHA256: 7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
  receipt manifest SHA256: 400aa0b52a5e120b7791e34e9a364d4e40a2362c46d6770dad3c5292db8dc7cc

R3_17F_OPEN_BOUNDARY:
  contract only for R3.17E-observed K2 semantic variants
  ActiveActor33
  String observed Empty / Windows1252 / UTF16 branches
  QWordString observed legacy QWord64 + RL223 Windows1252 branches
  UniqueId observed Steam / PlayStation / PsyNet / Epic shapes only
  PartyLeader only observed Some(Epic, Windows1252 declared=33)
  unseen variants remain unadmitted

R3_17F_HARD_STOP:
  no production K2 implementation in the contract pass
  no inferred unseen K2 variants
  no second property / property-loop continuation
  no K3/K4, lifecycle, raw-state, event, skill, runtime or export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17F OUTCOME A:
  R3.17G — direct native K2 decoder implementation for contract-admitted variants only
'''

p = ROOT / 'MIMIR_CONTINUE_HERE.md'
txt = p.read_text(encoding='utf-8')
a = txt.index('# 1. CANONICAL CURRENT STATE BLOCK')
s = txt.index('```text', a)
e = txt.index('```', s + 7)
p.write_text(txt[:s] + '```text\n' + CANONICAL + '```' + txt[e+3:], encoding='utf-8', newline='\n')

GRAPH = '''# MIMIR — KNOWLEDGE GRAPH / MULTI-STAGE CONTINUITY GATE

> **Role:** Root cross-link and verification graph for all MIMIR knowledge sources.
>
> Current source/tests and exact-SHA evidence outrank prose. `MIMIR_CONTINUE_HERE.md` remains the execution handbook.

## Canonical graph

```text
fresh GitHub source/tests + exact-SHA evidence
        |
        v
MIMIR_CONTINUE_HERE.md
        |
        +-------------------------------+
        |                               |
        v                               v
docs/continuity/                MIMIR_ALL_SOURCES_SUPERBOOK.md
CURRENT_STATE + STATE.json              |
R3.17C production decision              |
R3.17D differential decision            |
R3.17E K2 evidence decision             |
R3.17F active contract spec             |
        |                               |
        +---------------+---------------+
                        |
                        v
docs/chatgpt-archive/SOURCE_REGISTRY.md
                        |
                        v
docs/chatgpt-archive/VALIDATION_MATRIX.md
                        |
                        v
docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md
                        |
                        v
scripts/verify_mimir_knowledge_archive.ps1
```

## Mandatory reading order

1. `MIMIR_CONTINUE_HERE.md`
2. `docs/continuity/MIMIR_CONTINUITY_STATE.json`
3. `docs/continuity/MIMIR_CURRENT_STATE.md`
4. `docs/continuity/MIMIR_R3_17C_DECISION.md`
5. `docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md`
6. `docs/continuity/MIMIR_R3_17D_DECISION.md`
7. `docs/continuity/MIMIR_R3_17E_EXECUTION_SPEC.md`
8. `docs/continuity/MIMIR_R3_17E_DECISION.md`
9. `docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md`
10. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
11. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
12. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
13. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
14. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
15. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
16. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`

## Current replay-decoder chain

```text
R3.13 static network lookup plan
 -> R3.14 actor envelope primitives
 -> R3.15 NewActor branch
 -> R3.16 existing-actor first-property header
 -> R3.17A-D K1 primitive scalar wave: CLOSED
      production c3d4c73ca34febb9f0383c59132a8bc8a363b06b
      R3.17D 31798478106 / 94760722134 SUCCESS / 96/96 exact
 -> R3.17E K2 object/reference/text evidence: OUTCOME A / CLOSED
      evidence 19db534a3668f84f1c5ce36ef1252c52841d890f
      authority 31801482588 / 94770260529 SUCCESS
      artifact 9219554878 / sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
      47/47 / 110539 K2 occurrences / 0 structural failures
 -> R3.17F evidence-supported K2 contract admission: ACTIVE
```

## Current capability lock

Production remains exactly at R3.17C: one already-resolved K1 primitive scalar payload may be decoded natively. R3.17E admitted K2 evidence, not native K2 production capability.

R3.17F may freeze contracts only for observed K2 semantic variants. Unseen variants remain closed. PartyLeader `None` and non-Epic PartyLeader variants are not authorized by R3.17E.

Property-loop continuation, next actor/frame iteration, lifecycle mutation, K3 spatial/physics and K4 gameplay-structured families remain closed.

## R3.17E closure identity

```text
evidence head              19db534a3668f84f1c5ce36ef1252c52841d890f
authority run/job          31801482588 / 94770260529 SUCCESS
normal CI                  31801482499 / 94770260054 SUCCESS
artifact                   9219554878
artifact digest            sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
aggregate SHA256           335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751
summary SHA256             9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e
oracle JSONL SHA256        196f4e4d2a588137ad12372cb2f0af79d7fca422c0bc2c5dea95506fa72cac4d
witness JSONL SHA256       7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
receipt manifest SHA256    400aa0b52a5e120b7791e34e9a364d4e40a2362c46d6770dad3c5292db8dc7cc
47/47 oracle decode        PASS
K2 occurrences             110539
shape/unclassified         0
bit monotonicity failures  0
raw-payload shape failures 0
privacy-safe output        PASS
production/Cargo/corpus    0/0/0 mutations
outcome                    A
```

## Authority rule

```text
current code/tests
> exact-SHA CI/evidence + immutable receipt streams
> MIMIR_CONTINUE_HERE.md
> docs/continuity/MIMIR_CONTINUITY_STATE.json
> docs/continuity/MIMIR_CURRENT_STATE.md
> admitted decision / active pass specs
> boundary locks
> roadmap
> historical artifacts/chat memory
```

## Verification

Run `scripts/verify_mimir_knowledge_archive.ps1`.
'''
(ROOT / 'MIMIR_KNOWLEDGE_GRAPH.md').write_text(GRAPH, encoding='utf-8', newline='\n')

CURRENT = '''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14  
**Repository:** `Naveax/MIMIR`  
**Canonical production SHA:** `c3d4c73ca34febb9f0383c59132a8bc8a363b06b`  
**Production milestone:** `R3.17C — native primitive scalar attribute decoder implementation`  
**Completed K1 differential:** `R3.17D — Outcome A / 96 of 96 exact`  
**Completed K2 evidence:** `R3.17E — Outcome A / 47 of 47 / 110539 occurrences`  
**Current exact pass:** `R3.17F — evidence-supported K2 object/reference/text contract admission`

## 1. Truthful production boundary

Production capability is unchanged from R3.17C. MIMIR can natively decode exactly one already-resolved K1 primitive scalar payload for Boolean, Byte, Enum, Float, Int or Int64 and stops exactly after that value. No K2 decoder is admitted yet.

## 2. R3.17E closure authority

```text
evidence head                  19db534a3668f84f1c5ce36ef1252c52841d890f
authority run/job              31801482588 / 94770260529 SUCCESS
exact-head normal CI           31801482499 / 94770260054 SUCCESS
artifact id                    9219554878
artifact digest                sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
replays / oracle success       47 / 47
K2 occurrences                 110539
ActiveActor                    86200
String                         14670
QWordString                    2920
UniqueId                       6443
PartyLeader                    306
shape/unclassified errors      0
bit monotonicity failures      0
raw payload shape failures     0
privacy-safe output            PASS
production/Cargo/corpus mut.   0 / 0 / 0
aggregate SHA256               335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751
summary SHA256                 9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e
```

## 3. R3.17F exact next pass

Freeze deterministic atomic contracts only for R3.17E-observed K2 semantic variants: ActiveActor33; String Empty/Windows1252/UTF16; QWordString legacy QWord64 plus observed RL223 Windows1252 text; observed UniqueId Steam/PlayStation/PsyNet/Epic; PartyLeader only observed Some(Epic, Windows1252 declared=33).

Do not widen from Boxcars type names alone. Unseen combinations remain closed until separately evidenced.

## 4. Still closed

```text
native K2 production decoder
second property / property-loop continuation
next actor / next frame iteration
K3 / K4 families
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
support-lane expansion
```
'''
(ROOT / 'docs/continuity/MIMIR_CURRENT_STATE.md').write_text(CURRENT, encoding='utf-8', newline='\n')

sp = ROOT / 'docs/continuity/MIMIR_CONTINUITY_STATE.json'
state = json.loads(sp.read_text(encoding='utf-8'))
state['updated_date'] = '2026-08-14'
state['last_completed_read_only_audit'] = 'R3.17E'
state['last_completed_evidence_pass'] = 'R3.17E'
state['last_completed_evidence_outcome'] = 'A — 47/47 oracle decode; 110539 K2 occurrences; zero structural/mutation failures; privacy-safe output PASS'
state['current_pass'] = 'R3.17F'
state['current_pass_kind'] = 'contract-only evidence-supported K2 object/reference/text contract admission'
state['current_pass_goal'] = 'Freeze exact atomic contracts only for R3.17E-observed K2 semantic variants before any production implementation.'
state['current_pass_stop_boundary'] = 'Contract only; no production K2 decoder, unseen variants, second property, actor/frame iteration, lifecycle, K3/K4 or support-lane widening.'
state['r3_17e'] = {
  'outcome':'A — admitted / complete','production_source_changed':False,
  'base_main_sha':'cfe4882f99dbce5e8148e476c177a0586b1e7986','production_sha':'c3d4c73ca34febb9f0383c59132a8bc8a363b06b','production_source_blob':'54e1bfb918ec1bd42a61cfa0131ca27412082ac5',
  'evidence_head_sha':'19db534a3668f84f1c5ce36ef1252c52841d890f','authority_run':31801482588,'authority_job':94770260529,'normal_ci_run':31801482499,'normal_ci_job':94770260054,
  'artifact_id':9219554878,'artifact_digest':'sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc','replays_total':47,'oracle_decode_success':47,'k2_occurrences_total':110539,
  'tag_occurrences':{'ActiveActor':86200,'String':14670,'QWordString':2920,'UniqueId':6443,'PartyLeader':306},
  'shape_mismatch_or_unclassified_count':0,'bit_monotonicity_failure_count':0,'raw_payload_shape_failure_count':0,'privacy_safe_output':True,
  'production_mutation_count':0,'cargo_mutation_count':0,'corpus_mutation_count':0,
  'aggregate_sha256':'335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751','summary_sha256':'9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e',
  'oracle_jsonl_sha256':'196f4e4d2a588137ad12372cb2f0af79d7fca422c0bc2c5dea95506fa72cac4d','witness_jsonl_sha256':'7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b','receipt_manifest_sha256':'400aa0b52a5e120b7791e34e9a364d4e40a2362c46d6770dad3c5292db8dc7cc','next_pass':'R3.17F'
}
state['next_files_to_read'] = [
  'MIMIR_CONTINUE_HERE.md','MIMIR_KNOWLEDGE_GRAPH.md','docs/continuity/MIMIR_CONTINUITY_STATE.json','docs/continuity/MIMIR_CURRENT_STATE.md',
  'docs/continuity/MIMIR_R3_17C_DECISION.md','docs/continuity/MIMIR_R3_17D_EXECUTION_SPEC.md','docs/continuity/MIMIR_R3_17D_DECISION.md','docs/continuity/MIMIR_R3_17E_EXECUTION_SPEC.md','docs/continuity/MIMIR_R3_17E_DECISION.md','docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md',
  'docs/continuity/MIMIR_PASS_PROTOCOL.md','docs/continuity/MIMIR_BOUNDARY_LOCKS.md','docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md','MIMIR_ALL_SOURCES_SUPERBOOK.md','docs/chatgpt-archive/SOURCE_REGISTRY.md','docs/chatgpt-archive/VALIDATION_MATRIX.md','docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md'
]
sp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

DECISION = '''# MIMIR R3.17E — K2 Wire Evidence Decision

**Decision:** Outcome A — ADMITTED / COMPLETE  
**Date:** 2026-08-14  
**Production capability change:** none

## Authority

- Base main: `cfe4882f99dbce5e8148e476c177a0586b1e7986`
- Production SHA/blob: `c3d4c73ca34febb9f0383c59132a8bc8a363b06b` / `54e1bfb918ec1bd42a61cfa0131ca27412082ac5`
- Evidence head: `19db534a3668f84f1c5ce36ef1252c52841d890f`
- Authority run/job: `31801482588 / 94770260529` SUCCESS
- Exact-head normal CI: `31801482499 / 94770260054` SUCCESS
- Artifact: `9219554878`
- Artifact digest: `sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc`

## Results

47/47 replays parsed. Complete K2 scan: 110,539 occurrences: ActiveActor 86,200; String 14,670; QWordString 2,920; UniqueId 6,443; PartyLeader 306. Shape/unclassified, bit-monotonicity and raw-payload-shape failures are all zero. Privacy-safe output passed. Production/Cargo/corpus mutation is 0/0/0.

Observed authority surface: ActiveActor33; String Empty/Windows1252/UTF16; QWordString legacy QWord64 and RL223 Windows1252; UniqueId Steam/PlayStation/PsyNet/Epic; PartyLeader only Some(Epic, Windows1252 declared=33). Unseen variants are not admitted by inference.

## Immutable hashes

```text
aggregate          335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751
summary            9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e
oracle JSONL       196f4e4d2a588137ad12372cb2f0af79d7fca422c0bc2c5dea95506fa72cac4d
witness JSONL      7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
receipt manifest   400aa0b52a5e120b7791e34e9a364d4e40a2362c46d6770dad3c5292db8dc7cc
replay identity    b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
```

R3.17F is opened as contract-only. Production remains at R3.17C until a separate implementation pass is admitted.
'''
(ROOT / 'docs/continuity/MIMIR_R3_17E_DECISION.md').write_text(DECISION, encoding='utf-8', newline='\n')

SPEC = '''# MIMIR R3.17F — Evidence-Supported K2 Contract Admission Spec

**Pass type:** contract-only  
**Production implementation:** forbidden  
**Input authority:** R3.17E Outcome A

## Goal

Freeze deterministic atomic decoding contracts only for K2 semantic variants actually observed by R3.17E.

## In scope

- ActiveActor exact 33-bit contract.
- String signed i32 length with observed Empty, Windows1252 and UTF16 branches, exact end-bit and truncation semantics.
- QWordString observed legacy 64-bit QWord branch and observed RL223 Windows1252 text branch.
- UniqueId observed Steam, PlayStation, PsyNet and Epic variants with evidence-supported version/width behavior.
- PartyLeader only observed Some(Epic, Windows1252 declared=33).
- Atomic malformed/truncation rules and privacy-safe test vectors derived from immutable R3.17E evidence identities.

## Not admitted

PartyLeader None/non-Epic variants, unobserved UniqueId systems/combinations, unobserved QWordString branches, any shape inferred only from Boxcars/type names, production K2 code, second property/loop continuation, actor/frame lifecycle widening, K3/K4, raw-state/event/skill/runtime/export, Cargo/corpus/support-lane widening.

## Admission gate

Outcome A requires a complete contract table for every admitted observed shape, deterministic success/end-bit semantics, explicit malformed/truncation behavior, privacy-safe vectors and zero contradiction with R3.17E. Outcome B requests targeted evidence. Outcome C stops the wave.

## Next pass on Outcome A

`R3.17G — direct native K2 decoder implementation for contract-admitted variants only`.
'''
(ROOT / 'docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md').write_text(SPEC, encoding='utf-8', newline='\n')

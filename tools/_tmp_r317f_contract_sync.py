from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "b4b4449a99dabbb97120d5393c3d5b1462b6f81e"
PROD = "c3d4c73ca34febb9f0383c59132a8bc8a363b06b"
EVIDENCE = "19db534a3668f84f1c5ce36ef1252c52841d890f"
ORACLE = "c70e77df7af81b436cb545d070bb90c82f562d0b"


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


decision = r'''# MIMIR — R3.17F K2 Contract Admission Decision

**Date:** 2026-08-14
**Pass:** `R3.17F — evidence-supported K2 object/reference/text contract admission`
**Outcome:** **A — ADMITTED / CONTRACT COMPLETE**
**Pass kind:** docs-only contract admission
**Production Rust changed:** **NO**

## Frozen authorities

```text
canonical continuity base    b4b4449a99dabbb97120d5393c3d5b1462b6f81e
production code checkpoint   c3d4c73ca34febb9f0383c59132a8bc8a363b06b
production source blob       54e1bfb918ec1bd42a61cfa0131ca27412082ac5
R3.17E evidence head         19db534a3668f84f1c5ce36ef1252c52841d890f
R3.17E authority run/job     31801482588 / 94770260529 SUCCESS
R3.17E exact-head CI         31801482499 / 94770260054 SUCCESS
R3.17E artifact              9219554878
R3.17E artifact digest       sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
aggregate SHA256             335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751
summary SHA256               9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e
oracle JSONL SHA256          196f4e4d2a588137ad12372cb2f0af79d7fca422c0bc2c5dea95506fa72cac4d
witness JSONL SHA256         7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
receipt manifest SHA256      400aa0b52a5e120b7791e34e9a364d4e40a2362c46d6770dad3c5292db8dc7cc
```

R3.17E observed 110,539 K2 payloads over 47/47 supported replays with zero shape/unclassified, bit-monotonicity, raw-payload-shape, production, Cargo or corpus failures.

## Common atomic cursor contract

All R3.17G K2 decodes must use the existing LSB-first network bit order and may begin at any bit offset. The caller supplies `network_bytes`, an already-resolved K2 attribute tag, `payload_start_bit`, and the minimum decode context required by this decision.

```text
start = payload_start_bit
byte alignment is NOT required
all checked arithmetic must fail closed
on success: payload_end_bit is the first bit after exactly one K2 value
on any truncation, malformed length, unsupported tag, unadmitted context or unadmitted shape:
    fail atomically
    consume 0 bits relative to start
    return no successor/continuation permission
```

A successful K2 decode does not authorize a second property, next actor, next frame, lifecycle mutation or any wider replay interpretation.

## Decode context contract

The direct implementation seam may use:

```text
ReplayNetworkK2DecodeContextV1 {
    net_version: i32,
    is_rl_223: bool,
}
```

The current supported K2 evidence lane has `net_version == 10`. R3.17G must reject other net versions for `UniqueId` and `PartyLeader` rather than silently applying unobserved layouts.

`is_rl_223` is a caller-supplied already-resolved context bit for the direct payload decoder. R3.17F does not widen replay-header/build-version policy. The pinned oracle derives it from its header build-version gate; integrating that derivation into a broader native frame loop remains outside this pass.

## Contract table

### ActiveActor

```text
wire width    33 bits exact
field 0       active: 1 bit
field 1       actor: 32-bit little-endian LSB-first bit pattern -> signed i32
semantic      { active: bool, actor: i32 }
lookup rule   no actor existence/class/lifecycle validation
context       independent of is_rl_223; both observed modes admitted
```

The actor value is a raw reference identifier only. A negative or currently unknown actor id is not made malformed by this decoder.

### String

The wire starts with a signed little-endian i32 length.

```text
length == 0
    width = 32 bits
    semantic = empty string

length > 0
    bytes = length
    width = 32 + bytes*8
    decode bytes[0 .. bytes-1] as Windows-1252
    final declared byte is a terminator slot and is omitted semantically

length < 0
    reject i32::MIN
    bytes = checked((-length) * 2)
    width = 32 + bytes*8
    decode bytes[0 .. bytes-2] as UTF-16LE with deterministic replacement behavior
    final declared two bytes are a terminator-code-unit slot and are omitted semantically
```

The pinned oracle drops the final terminator slot; it does not validate that the dropped byte/code-unit is numerically zero. R3.17G must reproduce that semantic behavior, not invent a stricter NUL check.

Positive and negative lengths use checked arithmetic and must fit entirely inside remaining network bits. Truncation at the length or content stage is atomic failure.

### QWordString

```text
is_rl_223 == false
    admitted shape = QWord64
    width = 64 bits exact
    semantic = u64

is_rl_223 == true
    admitted shape = Windows-1252 text only
    wire = String positive-length branch
    evidence observed declared lengths 7, 8, 9
    zero/negative text branches are not admitted for QWordString in this wave
```

The contract admits the positive Windows-1252 branch as the semantic shape, not a fixed 7/8/9 width table. Length arithmetic and full-payload availability remain mandatory.

### UniqueId

The first field is `system_id: u8`; the final field for every admitted variant is `local_id: u8`. Current admission requires `net_version == 10`.

```text
system 1 / Steam
    system_id:u8 + online_id:u64 + local_id:u8
    width 80 bits
    observed with is_rl_223 false and true

system 2 / PlayStation
    system_id:u8
    name_bytes:[u8;16]
    unknown:[u8;16]          # net_version 10 observed layout
    online_id:u64
    local_id:u8
    width 336 bits
    name semantic = bytes before first 0 decoded as Windows-1252
    observed with is_rl_223 true

system 7 / PsyNet
    system_id:u8 + online_id:u64 + local_id:u8
    width 80 bits at net_version 10
    observed with is_rl_223 true

system 11 / Epic
    system_id:u8
    text = String positive Windows-1252 branch with declared length exactly 33
    local_id:u8
    width 312 bits
    observed with is_rl_223 false and true
```

Unadmitted system ids include 0/SplitScreen, 4/Xbox, 5/QQ, 6/Switch and every unknown value. They must fail atomically. PlayStation/PsyNet at non-10 net versions and Epic with any text encoding/declared length other than positive Windows-1252 `33` remain unadmitted.

### PartyLeader

Only the observed non-null Epic form is admitted:

```text
context       net_version == 10 AND is_rl_223 == true
system_id     11
remote        Epic String positive Windows-1252 declared length exactly 33
local_id      u8
width         312 bits
semantic      Some(Epic unique id)
```

`system_id == 0` / `None`, non-Epic systems, non-33 Epic text, UTF-16/empty Epic text and other contexts remain unadmitted even though broader oracle source contains code for some of them.

## Error taxonomy for R3.17G

At minimum, implementation/tests must distinguish these failure classes in stable error text or typed categories:

```text
invalid-start
insufficient-bits
invalid-text-length
unadmitted-context
unadmitted-k2-shape
unsupported-k2-tag
```

Every class is atomic with respect to `payload_start_bit`.

## Privacy-safe implementation vectors

R3.17G tests must use synthetic identities/text and must not copy clear real player/account values from R3.17E artifacts. Required coverage includes:

```text
ActiveActor at unaligned start, active false/true, positive and negative i32 actor patterns
String empty, Windows-1252, UTF-16LE, unaligned starts, i32::MIN, prefix/content truncation
QWordString legacy u64 and RL223 positive Windows-1252; reject RL223 empty/UTF-16
UniqueId synthetic Steam, PlayStation, PsyNet and Epic(declared=33)
UniqueId reject wrong net version, unadmitted system ids and wrong Epic text shape
PartyLeader synthetic Some(Epic, declared=33); reject None and all non-Epic/unobserved forms
exact payload_end_bit / width equality for every success
zero-consumption semantics for every failure family
```

## Integration policy for R3.17G

Production implementation must be additive and reuse `NetworkBitCursor`. Preferred production scope:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs
```

No external parser or text-decoder dependency may be added. If text decoding requires a helper, implement only the minimal deterministic Windows-1252 / UTF-16LE behavior needed by this contract inside `mimir-replay` and test it directly.

## Still forbidden

```text
Cargo.toml / Cargo.lock changes
external Boxcars dependency in production
unobserved K2 shape support
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
K3/K4 attribute decode
raw state / events / replay slicing / skills
runtime or export widening
support-lane expansion
```

## Outcome

The R3.17E authority, pinned Boxcars wire behavior and existing MIMIR atomic LSB-first cursor admit a deterministic implementation contract without requiring new evidence. **Outcome A** is therefore admitted.

## Next exact pass

`R3.17G — direct native K2 decoder implementation for contract-admitted variants only`.
'''

r3_17g = r'''# MIMIR — R3.17G Direct Native K2 Decoder Execution Spec

**Pass type:** production implementation
**Input authority:** R3.17F Outcome A
**External parser dependency:** forbidden

## Goal

Implement a direct native one-value K2 decoder for only the contract-admitted R3.17F shapes, preserving exact bit boundaries and atomic failure semantics.

## Required production seam

Add an additive API in `mimir-replay` equivalent to:

```text
ReplayNetworkK2DecodeContextV1 { net_version: i32, is_rl_223: bool }
ReplayNetworkUniqueIdV1
ReplayNetworkK2ValueV1
ReplayNetworkK2DecodeV1 {
    attribute_tag,
    payload_start_bit,
    payload_end_bit,
    payload_width,
    value,
}

decode_replay_network_k2_v1(network_bytes, payload_start_bit, attribute_tag, context)
```

Exact Rust naming may vary only if the resulting API preserves this data and the focused tests remain explicit.

## Admitted implementation surface

- ActiveActor: exact 33-bit `{active, actor:i32}`.
- String: signed-i32 Empty / positive Windows-1252 / negative UTF-16LE branches per R3.17F.
- QWordString: legacy QWord64 when `is_rl_223=false`; positive Windows-1252 text only when true.
- UniqueId at `net_version=10`: Steam, PlayStation, PsyNet, Epic declared=33 only, with R3.17F observed context matrix.
- PartyLeader: only `net_version=10`, `is_rl_223=true`, Some(Epic Windows-1252 declared=33).

## Atomicity

Use `NetworkBitCursor` and snapshot the start position before any branch read. Every failure must restore the internal cursor to the starting position. No partial decode may expose an advanced end bit.

Checked arithmetic is mandatory for bit/byte lengths. `i32::MIN` text length fails closed.

## Text semantics

Implement deterministic decoding without adding Cargo dependencies.

- Windows-1252 uses the standard byte-to-Unicode mapping; omit the final declared terminator slot without requiring it to equal zero.
- UTF-16LE decodes complete 16-bit units before the final declared terminator slot and uses deterministic U+FFFD replacement for malformed surrogate structure.
- QWordString RL223 admits only the positive Windows-1252 branch.
- Epic IDs admit only positive Windows-1252 declared length 33.

## Focused tests

Create `crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs` with synthetic privacy-safe vectors covering every admitted shape and every rejection family from R3.17F. Include unaligned payload starts and exact end-bit assertions.

At minimum test:

```text
ActiveActor success x4 + truncation
String empty / Windows-1252 / UTF-16LE / i32::MIN / truncation
QWordString legacy / RL223 text / RL223 empty reject / RL223 UTF-16 reject
UniqueId Steam / PlayStation / PsyNet / Epic success
UniqueId wrong net version / systems 0,4,5,6 / unknown system / wrong Epic shape reject
PartyLeader Epic success / None reject / non-Epic reject / wrong context reject
non-K2 tag reject
payload_start beyond network reject
```

## Validation gates

```text
cargo fmt --all -- --check
cargo test -p mimir-replay --test r3_17g_k2_attribute_decoder
cargo test -p mimir-replay
cargo clippy --workspace --all-targets -- -D warnings
scripts/verify_repo.ps1
clean-tree / exact diff scope audit
published-main CI + Knowledge Archive
```

Production diff should remain limited to:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs
```

Any required Cargo, corpus, fixture or unrelated crate change stops R3.17G and requires a new contract/evidence decision.

## Hard stop

R3.17G decodes exactly one already-resolved K2 payload and stops at its `payload_end_bit`. It does not continue the property loop or mutate actor/frame state.

Still closed: unobserved K2 forms, K3/K4, second property, next actor/frame, lifecycle mutation, raw state, events, replay slices, skill mining, runtime/export and support-lane widening.

## Next pass on successful production publication

`R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses`.
'''

write("docs/continuity/MIMIR_R3_17F_DECISION.md", decision)
write("docs/continuity/MIMIR_R3_17G_EXECUTION_SPEC.md", r3_17g)

continue_path = ROOT / "MIMIR_CONTINUE_HERE.md"
continue_text = continue_path.read_text(encoding="utf-8")
continue_text = continue_text.replace(
    "LAST_COMPLETED_CONTRACT_PASS:\n  R3.17B — primitive scalar attribute wire contract / Outcome A",
    "LAST_COMPLETED_CONTRACT_PASS:\n  R3.17F — evidence-supported K2 object/reference/text contract / Outcome A",
)
continue_text = continue_text.replace(
    "CURRENT_PASS:\n  R3.17F — evidence-supported K2 object/reference/text contract admission\n\nCURRENT_PASS_TYPE:\n  contract-only / NO production Rust capability widening",
    "CURRENT_PASS:\n  R3.17G — direct native K2 decoder implementation for contract-admitted variants only\n\nCURRENT_PASS_TYPE:\n  production implementation / one already-resolved K2 payload only",
)
old_block = re.compile(
    r"R3_17F_OPEN_BOUNDARY:\n.*?NEXT PASS IF R3\.17F OUTCOME A:\n  R3\.17G — direct native K2 decoder implementation for contract-admitted variants only",
    re.S,
)
new_block = '''R3_17F_CONTRACT_CLOSURE:
  Outcome A / docs-only / production Rust unchanged
  common rule: LSB-first, unaligned allowed, exact one-value end bit, atomic failure
  context: net_version + already-resolved is_rl_223; current UniqueId/PartyLeader lane net_version=10
  ActiveActor: exact 1-bit active + 32-bit signed actor reference
  String: signed i32 Empty / Windows1252 / UTF16 with checked lengths
  QWordString: legacy QWord64 or RL223 positive Windows1252 only
  UniqueId: Steam / PlayStation / PsyNet / Epic(declared=33) only
  PartyLeader: only Some(Epic, Windows1252 declared=33), net10 + RL223 true
  unseen shapes/context combinations remain unadmitted

R3_17G_OPEN_BOUNDARY:
  implement direct native one-value K2 decoder only for R3.17F-admitted shapes
  reuse NetworkBitCursor and atomic rollback semantics
  synthetic privacy-safe focused vectors only
  expected source scope: crates/mimir-replay/src/lib.rs + r3_17g focused test

R3_17G_HARD_STOP:
  no second property / property-loop continuation
  no unobserved K2 variants
  no K3/K4, lifecycle, raw-state, event, skill, runtime or export widening
  no Cargo, fixture, corpus or support-lane change

NEXT PASS IF R3.17G PUBLISHES CLEANLY:
  R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses'''
continue_text, count = old_block.subn(new_block, continue_text, count=1)
if count != 1:
    raise SystemExit("failed to replace R3.17F current block in MIMIR_CONTINUE_HERE.md")
write("MIMIR_CONTINUE_HERE.md", continue_text)

graph_path = ROOT / "MIMIR_KNOWLEDGE_GRAPH.md"
graph = graph_path.read_text(encoding="utf-8")
graph = graph.replace(
    "R3.17E K2 evidence decision             |\nR3.17F active contract spec             |",
    "R3.17E K2 evidence decision             |\nR3.17F K2 contract decision             |\nR3.17G active implementation spec       |",
)
graph = graph.replace(
    "9. `docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md`\n10. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n11. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n12. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n13. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n14. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n15. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n16. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "9. `docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md`\n10. `docs/continuity/MIMIR_R3_17F_DECISION.md`\n11. `docs/continuity/MIMIR_R3_17G_EXECUTION_SPEC.md`\n12. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n13. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n14. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n15. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n16. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n17. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n18. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
)
graph = graph.replace(
    " -> R3.17F evidence-supported K2 contract admission: ACTIVE",
    " -> R3.17F evidence-supported K2 contract admission: OUTCOME A / CLOSED\n -> R3.17G direct native K2 decoder implementation: ACTIVE",
)
graph = graph.replace(
    "R3.17F may freeze contracts only for observed K2 semantic variants. Unseen variants remain closed. PartyLeader `None` and non-Epic PartyLeader variants are not authorized by R3.17E.",
    "R3.17F admitted atomic contracts only for evidence-supported K2 shapes. R3.17G may implement exactly one already-resolved K2 payload under those contracts; native K2 capability is not claimed until production publication succeeds. PartyLeader `None`, non-Epic PartyLeader and other unseen K2 variants remain closed.",
)
closure = '''\n## R3.17F contract closure\n\n```text\noutcome                    A / contract complete\nproduction Rust            unchanged at c3d4c73ca34febb9f0383c59132a8bc8a363b06b\ncontract base              b4b4449a99dabbb97120d5393c3d5b1462b6f81e\nActiveActor                33-bit exact reference contract\nString                     Empty / Windows1252 / UTF16 atomic contract\nQWordString                legacy QWord64 / RL223 positive Windows1252\nUniqueId                   Steam / PlayStation / PsyNet / Epic(declared=33), net10\nPartyLeader                Some(Epic declared=33) only, net10 + RL223 true\natomic failure             0-bit consumption from payload start\nprivacy-safe G vectors     synthetic only\nnext pass                  R3.17G production implementation\n```\n'''
marker = "\n## Authority rule\n"
if marker not in graph:
    raise SystemExit("graph authority marker missing")
graph = graph.replace(marker, closure + marker, 1)
write("MIMIR_KNOWLEDGE_GRAPH.md", graph)

current = r'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `c3d4c73ca34febb9f0383c59132a8bc8a363b06b`
**Production milestone:** `R3.17C — native primitive scalar attribute decoder implementation`
**Completed K1 differential:** `R3.17D — Outcome A / 96 of 96 exact`
**Completed K2 evidence:** `R3.17E — Outcome A / 47 of 47 / 110539 occurrences`
**Completed K2 contract:** `R3.17F — Outcome A / atomic evidence-supported shapes`
**Current exact pass:** `R3.17G — direct native K2 decoder implementation`

## 1. Truthful production boundary

Production capability is still unchanged from R3.17C until R3.17G is implemented, validated and published. MIMIR can currently decode exactly one already-resolved K1 primitive scalar payload. R3.17F authorizes implementation of one already-resolved K2 payload but does not itself create runtime capability.

## 2. R3.17F admitted contract

```text
common cursor              existing LSB-first NetworkBitCursor; unaligned starts allowed
failure                    atomic; zero bits consumed relative to payload start
ActiveActor                1-bit active + signed 32-bit actor reference / 33 bits exact
String                     signed-i32 Empty / Windows1252 / UTF16 checked-length branches
QWordString                legacy QWord64 or RL223 positive Windows1252 only
UniqueId net_version       10 only in current admission
UniqueId                   Steam / PlayStation / PsyNet / Epic Windows1252 declared=33
PartyLeader                only Some(Epic Windows1252 declared=33), net10 + RL223 true
unseen variants            rejected, not inferred from oracle source
privacy-safe tests         synthetic values only
```

R3.17E authority remains `19db534a3668f84f1c5ce36ef1252c52841d890f`, run/job `31801482588 / 94770260529` SUCCESS, artifact `9219554878` with digest `sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc`.

## 3. R3.17G exact next pass

Implement the R3.17F contract directly in `mimir-replay`, preferably limited to `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_17g_k2_attribute_decoder.rs`. Reuse `NetworkBitCursor`, preserve atomic rollback, add no external parser/text dependency and stop after exactly one K2 value.

A successful implementation publication opens `R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses`.

## 4. Still closed

```text
unobserved K2 variants
second property / property-loop continuation
next actor / next frame iteration
K3 / K4 families
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
Cargo/corpus/support-lane expansion
```
'''
write("docs/continuity/MIMIR_CURRENT_STATE.md", current)

state_path = ROOT / "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-14"
state["last_completed_contract_pass"] = "R3.17F"
state["last_completed_contract_outcome"] = "A — atomic evidence-supported K2 contract admitted; production Rust unchanged"
state["current_pass"] = "R3.17G"
state["current_pass_kind"] = "production direct native K2 decoder implementation for contract-admitted variants only"
state["current_pass_goal"] = "Implement exactly one already-resolved K2 payload decoder for R3.17F-admitted shapes using the existing LSB-first cursor and atomic failure semantics."
state["current_pass_stop_boundary"] = "One K2 payload only; no unseen variants, second property, actor/frame iteration, lifecycle, K3/K4, Cargo/corpus/support-lane or downstream widening."
state["r3_17f"] = {
    "outcome": "A — admitted / contract complete",
    "production_source_changed": False,
    "continuity_base_sha": BASE,
    "production_sha": PROD,
    "evidence_head_sha": EVIDENCE,
    "oracle_sha": ORACLE,
    "authority_run": 31801482588,
    "authority_job": 94770260529,
    "artifact_id": 9219554878,
    "artifact_digest": "sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc",
    "atomic_failure_zero_consumption": True,
    "active_actor_width_bits": 33,
    "string_branches": ["Empty", "Windows1252", "UTF16"],
    "qword_string_branches": ["legacy-QWord64", "RL223-positive-Windows1252"],
    "unique_id_net_version": 10,
    "unique_id_systems": ["Steam", "PlayStation", "PsyNet", "Epic-Windows1252-declared-33"],
    "party_leader": "Some(Epic-Windows1252-declared-33) only; net_version=10; is_rl_223=true",
    "privacy_safe_test_policy": "synthetic identities/text only",
    "next_pass": "R3.17G",
}
read_order = state.get("next_files_to_read", [])
for item in [
    "docs/continuity/MIMIR_R3_17F_DECISION.md",
    "docs/continuity/MIMIR_R3_17G_EXECUTION_SPEC.md",
]:
    if item not in read_order:
        anchor = "docs/continuity/MIMIR_R3_17F_EXECUTION_SPEC.md"
        if anchor in read_order:
            index = read_order.index(anchor) + 1
            read_order.insert(index, item)
        else:
            read_order.append(item)
state["next_files_to_read"] = read_order
write(
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    json.dumps(state, indent=2, ensure_ascii=False),
)

print("R3_17F_CONTRACT_SYNC=PASS")

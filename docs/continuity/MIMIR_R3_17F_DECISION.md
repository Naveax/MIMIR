# MIMIR — R3.17F K2 Contract Admission Decision

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

# MIMIR R3.17J — K3 Evidence-Supported Contract Admission Execution Spec

**Pass type:** contract-only
**Production implementation:** forbidden
**Evidence authority:** R3.17I Outcome A
**Production authority:** R3.17G, unchanged

## Goal

Convert the exact R3.17I observations for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` into a minimal fail-closed native-decoder contract without writing production K3 decoding code.

## Frozen identities

```text
continuity base              4df00aa76a99b85a122210c4f929523f72fe9ef4
native production SHA        9bfa837c69c4751f70ca63a17c65f0f89877ff32
native source blob           7288238cfb5338653552435be6af41f0dd7a4e85
R3.17I evidence head         8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
R3.17I authority run/job     31812804986 / 94807233173 SUCCESS
R3.17I artifact              9223916983
R3.17I artifact digest       sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
```

## Common contract questions to freeze

1. LSB-first unaligned one-value input and exact consumed/end-bit semantics.
2. Atomic failure: on unsupported, malformed or truncated input, no successful partial K3 value may escape.
3. Exact version/context gate. Current evidence is 868.32 / net10 only.
4. Checked arithmetic for bit width and component bounds.
5. No acceptance of an unobserved vector header/size merely because pinned Boxcars source supports it.
6. Evidence-derived privacy-safe positive vectors and synthetic negative vectors.
7. No hidden property-loop continuation: success returns exactly after one value.

## Shared net10 vector candidate

R3.17I proves the net10 prefix rule on observed outcomes:

```text
read low 4 bits
candidate = low + 16
if candidate < 22:
  consume one discriminator bit and select low or candidate
else:
  select low without discriminator
component_width = selected_size_bits + 2
read x/y/z with exactly component_width each
semantic float component = signed/decompressed integer / 100
```

Contract admission must explicitly bound accepted `selected_size_bits` to evidence-supported sets. Across K3 evidence the union is 0..19. `20` and `21` remain unobserved and must not silently become admitted.

Per-field evidence sets to preserve:

```text
standalone Location           0,7,8,14,15,16,17
RigidBody awake location      10..19
RigidBody sleeping location   13,16,17,18,19
RigidBody linear velocity     0..18
RigidBody angular velocity    0..15
```

The contract must decide whether to encode those per-field sets directly or prove that a narrower shared primitive plus field-level guards preserves the same admitted surface. It must not broaden to unobserved values by cross-product convenience.

## Location candidate

```text
context       version 868.32 / net10 / RL223 false or true
wire          one admitted net10 vector
end bit       exactly after z component
```

Only the seven R3.17I standalone vector structural shapes are candidates.

## RigidBody candidate

```text
context       version 868.32 / net10 / RL223 false or true
wire          sleeping bit
              admitted location vector
              56-bit quaternion
              if awake: admitted linear vector + admitted angular vector
sleeping      no velocity payload
awake         both velocity payloads required
end bit       exact after quaternion when sleeping; exact after angular vector when awake
```

The 48-bit legacy rotation path is unobserved and must remain rejected. Size/header outcomes outside the R3.17I per-subfield sets remain rejected.

## ReplicatedBoost candidate

```text
context       version 868.32 / net10 / RL223 true only
wire          grant_count:u8
              boost_amount:u8
              unused1:u8
              unused2:u8
width         exactly 32 bits
```

RL223=false is unobserved for this tag and remains closed unless separately evidenced.

## PickupNew candidate

```text
context       version 868.32 / net10 / RL223 false or true
None          presence=false + picked_up:u8 = 9 bits
SomeI32       presence=true + actor_ref:i32 + picked_up:u8 = 41 bits
```

No other branch shape is admitted.

## Negative/malformed contract requirements

The contract must specify fail-closed behavior for at least:

```text
wrong replay major/minor or net_version
unobserved vector selected_size_bits 20/21
truncated 4-bit vector prefix
truncated discriminator when required
truncated x/y/z component
RigidBody truncated sleeping/location/quaternion
RigidBody awake missing either velocity vector
RigidBody legacy quat48 attempt in current lane
ReplicatedBoost wrong RL223 context or truncation at each byte boundary
PickupNew truncation after presence, partial i32, or partial picked_up byte
extra bits are not consumed as a second property
```

## Required contract gates

```text
R3.17I authority identities frozen          PASS
all admitted forms trace to evidence        100%
unobserved forms remain explicit rejects    PASS
atomic failure semantics defined            PASS
exact end-bit semantics defined             PASS
privacy-safe positive vector plan           PASS
synthetic negative vector plan               PASS
production Rust mutation                     0
Cargo / fixture / corpus mutation            0
```

## Outcome rules

- **Outcome A:** exact evidence-supported K3 contract is frozen with no capability widening; open R3.17K implementation.
- **Outcome B:** evidence cannot support a required contract distinction; return to targeted evidence only.
- **Outcome C:** contract modeling contradicts R3.17I evidence or current production primitives; stop and repair before implementation.

## Hard stop

Do not implement a native K3 decoder in R3.17J. Do not continue to a second property, actor, frame or lifecycle state. K4, raw state, events, replay slicing, skills, runtime and export remain closed.

## Next pass

Only on Outcome A open `R3.17K — direct native K3 decoder implementation for contract-admitted variants only`.

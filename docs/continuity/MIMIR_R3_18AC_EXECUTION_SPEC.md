# MIMIR R3.18AC — Post-AA Following-Property Payload Real-Replay Evidence

**Status:** ACTIVE
**Pass type:** read-only evidence / payload boundary discovery
**Production authority:** R3.18AA `9392240c49f95766c214afee9865fed4155a87a4`
**Production mutation:** forbidden
**Another property control / repeated loop:** forbidden

## 1. Goal

Characterize exactly one payload beginning at the published R3.18AA `stop_bit == following_header.payload_start_bit` on the exact immutable 47-row R3.18AB lane. Compare a pinned Boxcars ordinal-3 payload oracle against the narrowest already-admitted native payload primitive for each observed tag. Stop at that one payload end and consume no later `property_present` bit.

R3.18AC is evidence only. It does not publish a fourth-property payload composition API.

## 2. Frozen authority

```text
production SHA/tree                 9392240c49f95766c214afee9865fed4155a87a4 / 968520d480f78c528086e4e31b2ce307f4f8d232
production lib/test blobs           46523f47f94231362b60f8aee038e943e41c7972 / 7df8f84af37d771b12da1334bd195634e4cc6a54
R3.18Z contract SHA256              81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9
R3.18AB evidence head/tree           b2f4b73600165b2d83389b6ce43709b64beba52a / 8d36c8c7118db8c6f0d28c4ae88e0400cf4a3cd1
R3.18AB authority run/job            32230919566 / 96000311036 SUCCESS
R3.18AB same-head CI                 32230919652 / 96000311479 SUCCESS
R3.18AB artifact                     9357559410 / 12607 bytes
R3.18AB artifact digest              sha256:4b6d72b154440ee2b819f5a5ecb6fa3768e086b7ec4ba0d0c53d0e8e3ad23d99
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh `main`, require the exact production SHA/tree/blobs and R3.18AB receipts above, verify the immutable AB artifact and inner SHA-256 manifest, verify R3.18Z SHA-256, and prove witness reselection remains zero.

## 3. Required source lane

Reuse exactly the 47 frozen R3.18AB rows. Do not select new replays, actors, properties, or easier payload classes.

Frozen header identity before payload discovery:

```text
rows                                47
exact R3.18Z contexts               18
header tags                         ActiveActor=39 / Int=7 / UniqueId=1
version                             868.32 / net10 on all 47
AA/frozen-Y/direct-header mismatch  0
witness reselection                 0
following payload bits consumed     0
another control bits consumed       0
Boxcars property ordinal            3 (zero-based)
```

The tag distribution above is a header fact only. R3.18AC must discover payload widths/subshapes from the real lane; it may not infer them from tag names alone.

## 4. Oracle and native candidate rules

Instrument pinned Boxcars only at the exact frozen ordinal-3 target and emit privacy-safe payload facts after the attribute decoder has consumed that payload:

- exact payload start/end and width;
- resolved tag;
- semantic value fields sufficient for differential equality without raw payload windows;
- UniqueId system/layout identity when the tag is `UniqueId`.

For the native candidate, reuse existing admitted primitives only:

- `ActiveActor` -> `decode_replay_network_k2_v1` under the exact net10/non-RL223 context;
- `Int` -> `decode_replay_network_primitive_scalar_v1`;
- `UniqueId` -> `decode_replay_network_k2_v1` under exact net10/non-RL223 context.

Known lower-level decoder capabilities are not evidence of this boundary. Native/oracle payload start, payload end, width and semantic value must match on every frozen row.

### UniqueId anti-assumption

Do not assume a single generic UniqueId width. The existing K2 decoder has admitted system-specific layouts, including 80-, 336-, and 312-bit shapes. The one frozen R3.18AC UniqueId row must independently prove its observed system id, exact layout and width against the pinned oracle before any later contract or production gate can use it.

## 5. Differential checks

For every frozen row require:

- published R3.18AA reconstructs exactly and stops at the frozen payload start;
- pinned Boxcars target identity matches the same replay/frame/actor/property coordinate;
- native candidate tag equals the frozen AA header tag;
- native/oracle payload start exact;
- native/oracle payload end exact;
- native/oracle payload width exact;
- privacy-safe semantic value equality exact;
- payload end is deterministic on repeated identical invocation;
- zero bits from the next property-control boundary are consumed.

Report exact width/subshape distributions from evidence. Do not normalize distinct UniqueId layouts or fabricate cross-product contexts.

## 6. Negative controls

At minimum:

- prefix truncation before the complete required payload -> reject atomically;
- wrong payload tag decoder -> reject or produce a non-equal result that is explicitly rejected by the differential gate;
- wrong replay/K2 context for context-sensitive payloads -> reject;
- post-payload poison -> returned payload result remains identical;
- repeated identical invocation -> exact identical result;
- unsupported/unadmitted UniqueId system/layout -> fail closed in synthetic lower-level controls;
- bits belonging to another `property_present` control are never inspected by the evidence/native candidate.

Use real frozen rows wherever byte-level truncation can represent the intended missing-payload prefix exactly. Synthetic lower-level truncation may supplement bit-granular edge cases but may not replace the 47-row real differential.

## 7. Evidence artifact

Produce a privacy-safe immutable artifact containing at least:

- exact production/AB/Z/Boxcars authority receipts;
- frozen replay identity and target coordinates without private raw payload windows;
- per-row AA/header identity and oracle/native payload comparison;
- exact payload width and semantic/subshape summary by tag;
- UniqueId system/layout evidence;
- negative-control results;
- another-control consumption counter;
- production/Cargo/fixture/corpus/support mutation counters;
- hashes for every evidence payload file.

## 8. Required validation

- deterministic double-run equality of target selection and native/oracle comparison;
- permanent focused R3.18AA tests PASS on the evidence head;
- relevant K1/K2 payload primitive tests PASS;
- full repository verifier PASS through the existing same-head normal CI;
- privacy scan PASS;
- witness reselection zero;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 9. Hard stop

R3.18AC may not change production Rust, Cargo files, fixtures, corpus, dependencies or support lanes. It may not consume another property-control bit, create a repeatable/generalized property loop or public cursor, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, run counterfactuals or widen runtime/export behavior.

## 10. Outcome gate

### Outcome A

All 47 frozen rows match pinned Boxcars exactly through one ordinal-3 payload end, observed width/subshape facts are complete for ActiveActor/Int/UniqueId, mismatch is zero, witness reselection is zero, another-control consumption is zero, privacy passes and production mutation is zero. Admit R3.18AC evidence. A later separate pass may define the narrow contract/production gate justified by those exact observed payload facts.

### Outcome B

A reproducible native/oracle mismatch appears inside a payload class already supported by the lower-level primitive. Record the exact privacy-safe coordinate and keep production widening closed.

### Outcome C

Authority drift, witness reselection, privacy failure, another-control access, unsupported payload shape without exact evidence, source mutation or validation contradiction. Stop without admission.

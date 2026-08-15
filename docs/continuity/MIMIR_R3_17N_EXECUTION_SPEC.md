# MIMIR R3.17N — K4 Evidence-Supported Contract Admission Execution Spec

**Pass type:** contract-only
**Production implementation:** forbidden
**Evidence authority:** R3.17M Outcome A
**Production authority:** R3.17K, unchanged

## Goal

Convert the exact R3.17M observations for the 11 K4 gameplay-structured tags into a minimal fail-closed one-value decoder contract. Do not write production K4 decoding code in this pass.

## Frozen identities

```text
continuity base              b1a4ad1a04623e3c8b002a7ea60817120b5fb551
production SHA               7390e3b145372252caaa8fa1fe3e0cd13b83336c
R3.17M evidence head         a50f09857f36ac52cec30b4bf3efbde9e15bb564
R3.17M authority run/job     31881779861 / 95005282281 SUCCESS
R3.17M exact-head CI         31881779862 / 95005282149 SUCCESS
R3.17M artifact              9246249473
R3.17M artifact digest       sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
R3.17M groups SHA256         80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
R3.17M witnesses SHA256      acd66e4b1fc6f8c13228c7c67c24855760d55569957177915521d685949f80c3
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
observed K4 groups           161
```

## Contract surface to freeze

The candidate K4 surface is exactly the 161 structural/context groups in the R3.17M groups JSONL:

```text
CamSettings        6314 occurrences / 1 shape
TeamPaint          6498 / 1
TeamLoadout        6443 / 1
ClubColors          208 / 1
Reservation        6392 / 35
StatEvent          2279 / 1
PlayerHistoryKey   3840 / 1
DemolishFx          131 / 12
DemolishExtended     16 / 5
ExtendedExplosion   701 / 1
LoadoutsOnline     6641 / 73
```

The contract must materialize a canonical, deterministic admitted-group artifact derived from the evidence artifact and prove byte-for-byte/equivalent tuple equality with the evidence groups. No group may be invented from prose or Boxcars source.

## Common contract rules

1. Input is one already-resolved attribute payload at an arbitrary unaligned bit start, LSB-first.
2. Success consumes exactly one contract-admitted K4 value and returns its exact end bit.
3. Wrong version/context, unsupported structural branch, malformed length/count, overflow or truncation fails atomically; no successful partial value escapes.
4. Exact replay version/net-version/RL223 context is part of admission where present in the evidence tuple.
5. Exact structural group membership outranks per-field union membership.
6. A branch seen only in one or two replays remains admissible only for its exact observed groups; rarity is not permission to generalize.
7. Boxcars source may explain a field ordering but may not admit an unobserved branch.
8. Extra trailing bits are not consumed as a second property.

## Family-specific minimums

### Fixed-shape families

Freeze exact observed field order/width for:

- `CamSettings`: observed `f32x7`, width 224.
- `TeamPaint`: `u8x3 + u32x2`, width 88.
- `TeamLoadout`: observed blue/orange `v28` loadout branch only, width 1040.
- `ClubColors`: `bit + u8 + bit + u8`, width 18.
- `StatEvent`: `bit + i32`, width 33.
- `PlayerHistoryKey`: exact u14, width 14.
- `ExtendedExplosion`: observed exact location-vector structural group plus actor/reference fields, width 112.

No earlier/later version branch is admitted merely because the oracle has code for it.

### Reservation

Freeze only the exact 35 observed structural/context groups. Identifier system, split-screen branch, Epic text-length shape, optional reservation-name text shape, six-bit version-gated tail and exact total width must remain group-coupled. Do not admit arbitrary identifier/name-length combinations.

### DemolishFx / DemolishExtended

Freeze exact actor/reference field order plus the exact observed vector-shape pairs. Do not admit the Cartesian product of independently observed attacker/victim vector shapes. `DemolishFx` has 12 observed shapes; `DemolishExtended` has 5.

### LoadoutsOnline

Freeze exactly the 73 observed nested shapes. Outer side counts, per-group product counts, product-attribute object branch, title-text lengths and product value branches remain coupled exactly as evidenced. Do not synthesize new online-loadout combinations from individually observed product branches.

## Required negative/malformed contract cases

At minimum define fail-closed tests for:

```text
wrong replay major/minor/net_version/RL223 context
unknown K4 tag
invalid start bit
truncation at every fixed primitive boundary
Reservation unobserved identifier/name/text-length combination
Reservation malformed signed text length / overflow
DemolishFx unobserved vector-pair combination
DemolishExtended unobserved vector-pair combination
LoadoutsOnline unobserved outer/group/product combination
LoadoutsOnline malformed count/length and unknown product object branch
unobserved TeamLoadout version branch
extra trailing bits not consumed as another property
```

## Required contract artifacts and gates

```text
R3.17M authority identities frozen            PASS
canonical admitted-group artifact             161 exact groups
admitted-group evidence equality              161/161
cross-product widening                        0
unobserved branches explicit rejects          PASS
atomic failure semantics                      PASS
exact one-value end semantics                 PASS
privacy-safe positive vector plan             PASS
synthetic negative vector plan                PASS
production Rust mutation                      0
Cargo / fixture / corpus / support mutation   0/0/0/0
```

The canonical admitted-group artifact should be checked in under `docs/continuity/` during R3.17N if Outcome A is selected, analogous to the R3.17J K3 group artifact. It is contract evidence, not production implementation.

## Outcome rules

- **Outcome A:** freeze exactly the evidence-supported K4 contract with 161/161 group equality and zero widening; only then open a separate native K4 implementation pass.
- **Outcome B:** a required contract distinction cannot be represented without ambiguity; return to targeted evidence.
- **Outcome C:** contract modeling contradicts R3.17M evidence or existing bit primitives; stop before implementation.

## Hard stop

Do not implement native K4 decoding in R3.17N. Do not consume a second property, actor or frame, mutate lifecycle state, extract raw state/events, slice replays, mine skills, or widen runtime/export.

## Next pass

Only on R3.17N Outcome A may a separate direct native K4 decoder implementation pass be opened. R3.18 remains closed until that implementation and its differential audit are separately completed or the roadmap is explicitly revised by evidence.

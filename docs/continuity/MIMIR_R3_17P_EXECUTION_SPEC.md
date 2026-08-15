# MIMIR R3.17P — Native K4 Real-Replay Differential Audit Execution Spec

**Pass type:** read-only differential audit
**Production mutation:** forbidden
**Production authority:** R3.17O Outcome A
**Contract authority:** R3.17N Outcome A
**Evidence authority:** R3.17M Outcome A

## Goal

Regenerate real K4 witnesses ephemerally from the frozen 47-replay R3.17M lane and compare the published R3.17O native decoder against pinned Boxcars for every one of the 161 admitted exact structural/context groups. This pass certifies production; it does not widen it.

## Frozen identities

```text
R3.17O production SHA       492cc8218be7abc6db8f75acaea33d009ab2f175
R3.17O production tree      a66c47d7fb58da508188e64d42141987a0021a07
lib.rs blob                 0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8
k4 groups module blob       103503e25bc5af48381df021ab58133694fcece6
k4 native module blob       a9c41f3bb11343165183ac9c815ab8fdf085936c
focused test blob           70437244bb49224281ee3a2e745e7b8a4b7a093a
R3.17O authority head       900d7eb122f10126558f13ea2c185cdb8c69fe1b
R3.17O authority run/job    31885987240 / 95015252318 SUCCESS
R3.17O candidate CI         31886194387 / 95015736899 SUCCESS
R3.17O published-main CI    31886353485 / 95016105618 SUCCESS
R3.17N allowlist SHA256     80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
R3.17M evidence head        a50f09857f36ac52cec30b4bf3efbde9e15bb564
R3.17M authority run/job    31881779861 / 95005282281 SUCCESS
R3.17M artifact             9246249473
R3.17M artifact digest      sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
pinned Boxcars SHA          c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane       47
exact admitted groups       161
```

Before audit work, fetch fresh `main`, verify all R3.17O production blobs and the canonical R3.17N allowlist, then verify the R3.17M artifact and exact 47 replay identities. If production moved, reconstruct current truth before continuing.

## Real-witness reconstruction

Use exactly the frozen 47 replay identities from R3.17M; do not widen the corpus. Instrument the pinned Boxcars oracle at the already-resolved K4 payload boundary, or reuse the previously verified R3.17M instrumentation only after exact source/patch identity checks. Regenerate deterministic structural observations and select at least one real witness for **every one of the 161 R3.17N groups**.

For `LoadoutsOnline`, supply the native decoder with the exact caller-resolved replay object table corresponding to that replay. Do not synthesize object names from the product branch being tested.

Durable evidence may include replay identity hashes/labels, frame/actor/property structural coordinates, version/context, bit ranges, structural shape, payload hashes, safe numeric fields and boolean/integer match flags. Never persist unrelated account/player names, Epic IDs, titles or other private text in clear form.

## Required native-vs-oracle comparisons

For every selected real witness compare:

```text
resolved K4 tag / semantic variant
version 868.32 / net10 / RL223 context
payload_start_bit
payload_end_bit
payload_width
exact structural shape
native success vs oracle success
semantic value
```

Tag-specific semantic requirements:

- `CamSettings`: compare all seven f32 fields by exact f32 bit identity when oracle operation order is identical.
- `TeamPaint`: compare all three u8 and two u32 fields exactly.
- `TeamLoadout`: compare version and every version-gated base/unknown/special/banner/product/extra field exactly.
- `ClubColors`: compare both flags and color bytes exactly.
- `Reservation`: compare system/ID branch, local ID, name encoding/length and unknown fields. Sensitive account/name text is compared only in memory; durable evidence stores hashes/length/encoding/match flags.
- `StatEvent` and `PlayerHistoryKey`: compare exact primitive fields.
- `DemolishFx` and `DemolishExtended`: compare actor flags/IDs and both vector structures/raw components/semantic components.
- `ExtendedExplosion`: compare actor/flag fields plus vector structure/raw/semantic values.
- `LoadoutsOnline`: compare nested group counts, each product object branch and numeric/text value. Sensitive title text is compared in memory and persisted only as hash/length/encoding/match flags.

## Floating-point comparison rule

Inspect the pinned Boxcars arithmetic before evaluating witnesses. If native and oracle use the same f32 operations in the same order, require exact f32 bit equality. If operation order differs materially while remaining mathematically equivalent, define and persist a deterministic comparison rule **before** evaluating the witness set. Never invent a tolerance after observing mismatches.

## Negative controls

Regenerate or synthesize bounded controls for at least:

```text
wrong major / minor / net_version
wrong RL223 tuple for a single-context group
unsupported non-K4 tag
invalid payload start
fixed and variable payload truncation
malformed signed text lengths including i32::MIN
unsupported Reservation system / unadmitted Reservation name-length combination
DemolishFx cross-product tuple absent from allowlist
DemolishExtended cross-product tuple absent from allowlist
LoadoutsOnline unknown product object / absent nested cross-product
unobserved TeamLoadout version/branch combination
trailing-bit non-consumption
atomic failure / no partial semantic value escape
```

Negative controls do not authorize new shapes.

## Required gates

```text
fresh production identity                         PASS
47/47 replay identity verification                PASS
pinned Boxcars oracle decode                       47/47
R3.17M group reconstruction                        161/161
real witness group coverage                        161/161 minimum
native decode success on admitted witnesses        100%
tag / semantic variant match                       100%
context match                                      100%
payload start / end / width match                  100%
exact structural shape match                       100%
semantic value match under predeclared rule        100%
negative controls                                  100%
bit monotonicity / packed-payload failures         0 / 0
privacy scan                                       PASS
production/Cargo/fixture/corpus/support mutation   0/0/0/0/0
normal CI on exact audit head                      PASS
```

## Outcome rules

- **Outcome A:** all 161 exact groups receive real witness coverage, every native/oracle comparison is exact under the predeclared numeric rule, negatives fail closed, privacy passes and mutations remain zero.
- **Outcome B:** reproducible evidence is insufficient to reconstruct one or more admitted groups; stop with targeted evidence work only. Do not widen or silently skip.
- **Outcome C:** any native/oracle mismatch, structural contradiction, source-identity contradiction or decoder defect. Stop and repair evidence/contract/implementation in a separately admitted pass.

## Hard stop

R3.17P must not modify production Rust, Cargo files, fixtures, replay corpus or support lane. It must not consume a second property or advance actor/frame/lifecycle state. Raw-state, events, replay slicing, skills, runtime and export work remain closed.

## After Outcome A

Re-read `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md` and select the first dependency-valid unfinished pass. R3.18 is not automatically admitted merely because K4 differential closure succeeded.

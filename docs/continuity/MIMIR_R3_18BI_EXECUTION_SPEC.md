# MIMIR R3.18BI — Bounded Post-BE One-Following-Payload Production

**Status:** ACTIVE
**Pass type:** bounded production composition
**Production base:** R3.18BE `1d717d3e82179edd85b197968f46b8f951a3e828` / `72cf2b907437a1ba62cc9deebd7608f7d0372f81`
**Direct payload authority:** R3.18BG artifact `10015405999`
**Control evidence authority:** R3.18BH artifact `10023482583` (boundary remains closed in BI)
**Target rows:** exactly 3 BG authority rows

## 1. Goal

Publish the smallest production capability justified by R3.18BG: after one valid published R3.18BE true-path following header, decode exactly one primitive payload using only the exact BG-supported header/tag/context rows and stop exactly at that payload end.

R3.18BI must **not** consume the R3.18BH-observed next control bit. BH is used only to prove that the payload boundary has a separately known next-bit boundary and to prevent accidental over-read.

## 2. Frozen authority

```text
production base                       1d717d3e82179edd85b197968f46b8f951a3e828 / 72cf2b907437a1ba62cc9deebd7608f7d0372f81
BG rows                               3/3
BG tags                               Boolean=2 / Float=1
BG payload widths                     Boolean=1 bit / Float=32 bits
BG mismatch/reselection               0/0
BH evidence                           34132181073/101774645567 SUCCESS
BH observed control                   false=1 / true=2
BH native/oracle exact                3/3
BH next-bit boundary                  evidence-only; production read forbidden
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## 3. Production behavior

For exactly one already-valid R3.18BE result with `following_header != None`:

1. require the embedded/recomputed R3.18BE result to be structurally exact;
2. require the following header to be one of the exact BG authority rows and therefore an exact R3.18BD member;
3. require requested payload start equal the BE header `payload_start` / BE `stop_bit`;
4. for `Boolean`, reuse the existing primitive scalar decoder and require exact one-bit width;
5. for `Float`, reuse the existing primitive scalar decoder and require exact 32-bit width and raw IEEE754-u32 identity;
6. require the decoded payload end equal the exact BG authority `payload_end_bit`;
7. return the bounded header+payload composition and `stop_bit = payload_end_bit`;
8. stop without reading the BH `property_present` bit.

No new wire primitive is allowed if an existing admitted decoder already expresses the exact payload semantics.

## 4. Required tests

- exact three BG rows compose 3/3;
- Boolean=2 / Float=1 and widths 1/1/32 preserved;
- payload semantic value and start/end exact 3/3;
- repeatability 3/3;
- truncate inside payload -> fail closed atomically;
- wrong payload start -> reject;
- wrong tag/header/context/actor/lookup -> reject;
- fabricated fourth BG row/context -> reject;
- poison the exact BH control bit at `payload_end_bit` -> BI result unchanged;
- 37 BF-false rows cannot enter payload production;
- 7 upstream AU-false rows cannot enter payload production;
- source-scope guard: exactly one BE prerequisite reconstruction/composition path, exactly one primitive payload decode, zero next-control reads, zero following stream/header/payload reads, no generalized/repeated loop.

## 5. Validation

Require focused BI tests, BE/BG prerequisite regressions, full `mimir-replay`, workspace fmt/check/test/clippy under Rust 1.85, repository verifier, clean two-file production candidate, exact-head validation-only PR CI, fresh-main ancestry audit, force=false publication and published-main exact-SHA CI.

## 6. Hard stop

- R3.18BH control bit remains evidence-only;
- following stream/header/payload after BI remains closed;
- second later property-control bit remains closed;
- unobserved payload tags/layouts/contexts remain closed;
- no generalized property cursor/loop;
- no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 7. Outcome gate

### Outcome A
Exactly the three BG payloads are published with exact payload semantics/boundaries and zero BH-bit consumption. Open a separate published-BI differential pass before any BH control production.

### Outcome B/C
Any narrower safe subset, authority drift, payload mismatch, BH-bit consumption, context widening or unrelated mutation keeps the wider boundary closed.

# MIMIR R3.18BA — Bounded Post-AY Mixed Following-Control Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production authority before pass:** R3.18AY `2558cc0559422a3e6695e1501f20d96d83b23e6d` / `93198ad2a4f929ac62b87beddbc9d5b5665f08d1`
**Published-production differential authority:** R3.18AZ Outcome A / `f46479faa2b230f7fde474f7f7696a1024420879` / run `33086674062` / artifact `9652520412` / `sha256:558c709e242d74150755565d07c7968853abad0a1de6c5f49cd8f5920e7f9fc4`
**Control evidence authority:** R3.18AX Outcome A / artifact `9644869549` / false=37 true=3 / oracle-native exact 40/40
**Frozen production lane:** exactly 40 valid R3.18AY payload rows; the 7 upstream AU false terminators remain outside the lane

## 1. Goal

Publish exactly one boundary-specific composition after a valid R3.18AY Int/32 payload. The API must validate/recompute the supplied AY authority instead of trusting an arbitrary cursor, begin exactly at the validated AY payload end, consume exactly one `property_present` bit, represent both R3.18AX-observed boolean values, and stop one bit later.

No following stream ID, header, payload or second later property-control bit may be consumed.

## 2. Frozen semantics

```text
AY payload rows                        40
upstream AU false terminators          7 / excluded before AY/BA
AX false                               37
AX true                                3
published AY exact by AZ               40/40
AW/direct-native/oracle exact by AZ    40/40
AZ mismatch / reselection              0 / 0
AZ following-control consumption       0
```

**Critical rule:** both false and true are admitted. R3.18BA must not inherit the true-only behavior of R3.18M, R3.18W or R3.18AG. The closest production methodology reference is R3.18AQ's mixed-control composition, but BA must recompute the current R3.18AY boundary and must not inherit historical coordinates or values.

## 3. Production contract

The new boundary-specific API must:

1. accept enough upstream authority to recompute one exact R3.18AY payload composition;
2. reject all seven upstream AU false terminators before any BA control read because no valid AY payload exists for them;
3. validate/recompute the supplied AY result and require exact equality of header composition, Int/32 payload identity and AY stop boundary;
4. initialize the private native bit cursor exactly at the validated AY `stop_bit`;
5. consume exactly one LSB-first control bit;
6. return a boundary-specific typed result retaining the validated AY payload composition plus `following_property_present`, exact control start/end and final stop;
7. accept both false and true, with no expected runtime-frequency promise beyond the frozen evidence;
8. require final `stop_bit == ay.stop_bit + 1`;
9. consume zero next stream ID bits, zero following-header bits, zero following-payload bits and zero second-control bits;
10. fail atomically on truncation, corrupt/mismatched AY authority, wrong actor/lookup/context, or boundary drift.

No generic or repeatedly-chainable property cursor is admitted.

## 4. Required focused tests

At minimum:

- exactly the 40 frozen AY/AZ payload witnesses reproduce before control consumption;
- observed BA control distribution is exactly false=37 / true=3 on that frozen lane, with no reselection;
- all seven upstream AU false terminators remain outside BA and never invoke a BA control read;
- exact control start/end/stop equality on 40/40;
- deterministic repeatability 40/40;
- truncate exactly before the BA control bit -> atomic reject;
- corrupt/mismatch the supplied AY prior -> reject before BA advancement;
- wrong actor, unresolved lookup and wrong exact version context reject through AY prerequisite recomputation;
- false path succeeds and stops before any stream/header lookup;
- true path also stops before any stream/header lookup;
- poison bits beginning at BA control end -> BA result unchanged;
- next stream/header/payload/second-control consumption remains `0/0/0/0`;
- source-scope guard proves one AY recomputation, exactly one new `cursor.read_bit()`, no `read_bits_le`, no bounded stream ID, no header/payload decoder and no loop/cursor widening.

## 5. Clean candidate

Expected clean production scope is only:

- `crates/mimir-replay/src/lib.rs`;
- one focused `crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs` integration test.

No workflow/helper/evidence artifact, Cargo/dependency, fixture/corpus, continuity, raw-state/event/skill/runtime/export or unrelated cleanup enters the production commit.

## 6. Validation and publication

Require Rust 1.85 formatting, focused BA tests, directly affected AY/AU/AQ prerequisite regressions, workspace check/test, Clippy with warnings denied, repository verifier, exact clean-candidate natural CI, fresh-main ancestry verification, force=false publication, exact published-main SHA/tree readback and published-main validation.

Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## 7. Hard stop

No following stream ID, property object/header, payload, second later control, generalized/repeated property loop/cursor, next actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening. The seven upstream false terminators remain no-payload/no-BA-control terminators.

## 8. Outcome gate

### Outcome A

Publish exactly one mixed false/true control bit after a validated R3.18AY payload, with all forty frozen rows exact, false=37 / true=3 preserved, all focused/negative/full validations PASS and adjacent consumption `0/0/0/0`. Then open a separate published-production differential before any following-header production/evidence is considered.

### Outcome B

Only a narrower safe result representation can be implemented without violating the current AY/AX/AZ authority. Publish only that narrower representation and rewrite the next differential to the actual production contract.

### Outcome C

Authority drift, rejection of an AX-admitted boolean class, upstream false-terminator access, adjacent-bit access, generic chaining, production-scope drift or validation contradiction. Stop without publication.

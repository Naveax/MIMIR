# MIMIR — Current Canonical State

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

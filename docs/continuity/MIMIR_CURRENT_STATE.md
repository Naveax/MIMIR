# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `9bfa837c69c4751f70ca63a17c65f0f89877ff32`
**Production milestone:** `R3.17G — direct native evidence-admitted K2 decoder implementation`
**Completed K1 differential:** `R3.17D — Outcome A / 96 of 96 exact`
**Completed K2 evidence:** `R3.17E — Outcome A / 47 of 47 / 110539 occurrences`
**Completed K2 contract:** `R3.17F — Outcome A / atomic evidence-supported shapes`
**Current exact pass:** `R3.17H — native K2 differential audit against immutable R3.17E witnesses`

## 1. Truthful production boundary

Production now includes a direct native decoder for exactly one already-resolved R3.17F-admitted K2 payload. It reuses the LSB-first `NetworkBitCursor`, accepts unaligned payload starts, returns exact payload end/width, and fails closed for unsupported tags, malformed/truncated text, unadmitted contexts and unobserved K2 shapes. It does not continue the property loop or mutate actor/frame state.

R3.17G production identity:

```text
production SHA               9bfa837c69c4751f70ca63a17c65f0f89877ff32
production source blob       7288238cfb5338653552435be6af41f0dd7a4e85
focused test blob            92033a72a8a737605ac3bf91e10d130082277e04
implementation run/job       31805820332 / 94784362093 SUCCESS
clean-candidate CI            31806206582 / 94785622371 SUCCESS
published-main CI             31806554445 / 94786777798 SUCCESS
focused R3.17G tests          8 / 8 PASS
mimir-replay tests            189 PASS
workspace clippy              PASS
production file scope         exactly 2 files
Cargo/corpus/support widening none
```

## 2. Native K2 surface now admitted

```text
ActiveActor     exact 33-bit active + signed actor reference
String          signed-i32 Empty / Windows1252 / UTF16 contract branches
QWordString     legacy QWord64 or RL223 positive Windows1252 only
UniqueId        net10 Steam / PlayStation / PsyNet / Epic(declared=33), observed contexts only
PartyLeader     only Some(Epic declared=33), net10 + RL223 true
```

Unobserved variants remain rejected. Native K2 success authorizes exactly one value and nothing after its `payload_end_bit`.

## 3. R3.17H exact next pass

R3.17H is audit-only. Use the immutable R3.17E evidence authority and the exact 469 privacy-safe witness identities. Regenerate the corresponding raw payload/decoded values ephemerally with pinned Boxcars, feed those exact payloads to the native R3.17G decoder, and compare tag/shape, context gate, exact width/end and decoded semantic value in memory. Persist only privacy-safe hashes/counts/match flags.

No production Rust change is allowed in R3.17H.

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

# MIMIR — Current Canonical State

**Continuity date:** 2026-08-14
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `9bfa837c69c4751f70ca63a17c65f0f89877ff32`
**Production milestone:** `R3.17G — direct native evidence-admitted K2 decoder implementation`
**Completed K1 differential:** `R3.17D — Outcome A / 96 of 96 exact`
**Completed K2 evidence:** `R3.17E — Outcome A / 47 of 47 / 110539 occurrences`
**Completed K2 contract:** `R3.17F — Outcome A / atomic evidence-supported shapes`
**Completed K2 native differential:** `R3.17H — Outcome A / 469 of 469 exact / 7 of 7 negatives`
**Current exact pass:** `R3.17I — K3 spatial/physics wire-format evidence`

## 1. Truthful production boundary

Production remains exactly R3.17G. MIMIR can directly decode one already-resolved K1 scalar or one R3.17F-admitted K2 payload and then stops at the exact end bit. R3.17H audited that K2 surface; it did not add another property, actor, frame, lifecycle transition or K3 decoder.

```text
production SHA               9bfa837c69c4751f70ca63a17c65f0f89877ff32
production source blob       7288238cfb5338653552435be6af41f0dd7a4e85
R3.17H authority head        9b8e8fe82ab5bdc663eecc3f5d3cd1e3b8ee38ac
R3.17H run/job               31809282874 / 94795704797 SUCCESS
R3.17H exact-head CI         31809282903 / 94795705073 SUCCESS
R3.17H artifact              9222624242
R3.17H artifact digest       sha256:d6c773d593c3c50957507a19056e85aef8b769fdc03fd88c6d693b1258c0af28
```

## 2. R3.17H closure

The immutable 469 R3.17E witness identities were regenerated from the same 47 replay lane with pinned Boxcars and compared against the native R3.17G decoder.

```text
witness selection            469 / 469
native decode                469 / 469
attribute variant            469 / 469 exact
payload width                469 / 469 exact
payload end                  469 / 469 exact
context gate                 469 / 469 exact
semantic value               469 / 469 exact in-memory
negative controls            7 / 7 PASS
privacy scan                 PASS
production/Cargo/corpus      0 / 0 / 0 mutations
outcome                      A
```

Two earlier disposable runs failed only in temporary audit plumbing before native/oracle comparison and are not authority: the first attempted an unnecessary raw-SHA fetch; the second used a line-ending-sensitive file SHA check. V3 replaced that check with the immutable Git blob identity and is the sole admitted audit authority.

## 3. R3.17I exact next pass

R3.17I is evidence-only for the roadmap K3 spatial/physics family:

```text
Location
RigidBody
ReplicatedBoost
PickupNew
```

On the exact same 47-replay lane, instrument pinned Boxcars to record exact payload start/end/width, version/context, field boundaries and every observed wire-shape family. Select privacy-safe witnesses per observed shape/context. If a tag is absent or a shape is ambiguous, request targeted evidence rather than inferring a production contract from Boxcars source.

No production Rust change is allowed in R3.17I. Outcome A may open `R3.17J — contract admission for evidence-supported K3 shapes only`.

## 4. Still closed

```text
native K3/K4 payload decode
second property / property-loop continuation
next actor / next frame iteration
actor lifecycle mutation
raw-state/event/skill/runtime/export widening
Cargo/corpus/support-lane expansion
```

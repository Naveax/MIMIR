# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `492cc8218be7abc6db8f75acaea33d009ab2f175`
**Production milestone:** `R3.17O — direct native exact-contract K4 decoder implementation`
**Completed K4 differential:** `R3.17P — Outcome A / 161/161 real-replay exact groups / 0 mismatch`
**Completed single-property evidence:** `R3.18A — Outcome A / real existing-actor Int property / exact header + payload end / 0 next-property bits`
**Current exact pass:** `R3.18B — minimal native existing-actor single-property K1 composition`

## 1. Truthful production boundary

Production remains R3.17O. MIMIR can decode one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload. R3.17P certified K4 on all 161 exact real-replay groups. R3.18A proved that an existing-actor first-property header can be composed with an already-admitted payload decoder through the exact payload end without consuming the next property bit. **That evidence did not itself widen production.**

```text
production SHA               492cc8218be7abc6db8f75acaea33d009ab2f175
production tree              a66c47d7fb58da508188e64d42141987a0021a07
lib.rs blob                  0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8
k4 groups blob               103503e25bc5af48381df021ab58133694fcece6
k4 native blob               a9c41f3bb11343165183ac9c815ab8fdf085936c
focused K4 test blob         70437244bb49224281ee3a2e745e7b8a4b7a093a
```

## 2. R3.18A evidence closure

```text
execution base main          c5878cf755302fe52e9e67741486306cd30db059
authority head               12ee215fd843260d5ece14f27aa1171cb862f49e
authority run/job            31941400273 / 95151024131 SUCCESS
exact-head normal CI         31941400276 / 95151024211 SUCCESS
artifact                     9262129856
artifact digest              sha256:295247a5f73159ac74539ffc5abf1eb2273fb6dc07a57f8b16976552a17b3ab8
replay identity/oracle       47/47
eligible candidates          47 deterministic first-property scalars
selected replay              external_fixtures/sample_001.replay
frame / actor ordinal / id   0 / 63 / 2
actor context object         98
stream / bound / prop bits   27 / 67 / 6
property object / tag/value  55 / Int / 62
property_present             [10227,10228)
stream                       [10228,10234)
payload                      [10234,10266) / 32 bits
payload SHA256               d2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f
header/start/semantic/end    exact / exact / exact / exact
next property bits consumed  0
truncation negative          PASS
mismatch / privacy           0 / PASS
prod/Cargo/fixture/corpus/
support mutation             0/0/0/0/0
```

The first disposable R3.18A run was not authority because temporary probe formatting failed before native comparison. A later evidence run produced valid Outcome-A data but its same-head normal CI rejected a temporary example API newer than the Rust 1.85 MSRV. The final authority head reran every substantive gate after replacing that tooling-only API.

## 3. R3.18B exact next pass

R3.18B is a narrow production composition pass. Reuse the existing R3.16B first-property header reader, require `property_present == true`, resolve the existing stream/property/tag through the lookup plan, then dispatch **only** the six already-admitted K1 primitive scalar tags to the existing R3.17C decoder:

```text
Boolean
Byte
Enum
Float
Int
Int64
```

Return the exact one-property payload end and set the composition stop bit to that same end. Unsupported K2/K3/K4 tags must fail closed in this new API even though their separate one-value decoders already exist. The next `property_present` bit remains opaque and unread.

## 4. Still closed

```text
second property / property_present loop
K2/K3/K4 dispatch in the R3.18B composition API
next actor / next frame iteration
actor lifecycle mutation
new attribute family/shape/context admission
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/fixture/corpus/support-lane expansion
```

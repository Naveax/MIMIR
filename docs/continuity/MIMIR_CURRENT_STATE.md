# MIMIR — Current Canonical State

**Continuity date:** 2026-08-16
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `492cc8218be7abc6db8f75acaea33d009ab2f175`
**Production milestone:** `R3.17O — direct native exact-contract K4 decoder implementation`
**Completed K3 differential:** `R3.17L — Outcome A / 1950 of 1950 real-replay exact groups / 0 mismatch`
**Completed K4 evidence:** `R3.17M — Outcome A / 39463 occurrences / 161 exact structural-context groups / all 11 tags observed`
**Completed K4 contract:** `R3.17N — Outcome A / 161/161 byte-identical groups / zero cross-product widening`
**Completed K4 production:** `R3.17O — Outcome A / 161/161 exact contract implementation / zero widening`
**Completed K4 differential:** `R3.17P — Outcome A / 161/161 real-replay exact groups / 0 mismatch`
**Current exact pass:** `R3.18A — existing-actor single-property boundary evidence`

## 1. Truthful production boundary

Production remains R3.17O. MIMIR may decode exactly one already-resolved K1 scalar, one R3.17F-admitted K2 payload, one R3.17J-admitted K3 payload, or one exact R3.17N-admitted K4 payload and stop at the exact one-value end bit. R3.17P certified that K4 boundary against real replay witnesses but did not widen production into a property loop.

```text
production SHA               492cc8218be7abc6db8f75acaea33d009ab2f175
production tree              a66c47d7fb58da508188e64d42141987a0021a07
lib.rs blob                  0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8
k4 groups blob               103503e25bc5af48381df021ab58133694fcece6
k4 native blob               a9c41f3bb11343165183ac9c815ab8fdf085936c
focused K4 test blob         70437244bb49224281ee3a2e745e7b8a4b7a093a
R3.17N allowlist SHA256      80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
```

## 2. R3.17P real-replay differential closure

```text
authority head               f2d87b732ad3103d50e2c047351f1017d4f3613f
authority run/job            31937527114 / 95141677175 SUCCESS
exact-head normal CI         31937527123 / 95141677140 SUCCESS
artifact                     9261118033
artifact digest              sha256:bc366b75e003531ba17351e880f259457ceba7cda702d912580c686990ba1beb
replay identity              47/47
Boxcars oracle decode        47/47
exact group reconstruction   161/161
real witness group coverage  161/161
native decode                161/161
variant/context/range        161/161 exact
shape/semantic               161/161 exact
mismatch count               0
negative controls            PASS
privacy                      PASS
production/Cargo/fixture/
corpus/support mutation      0/0/0/0/0
```

The numeric rule was frozen before evaluation: CamSettings requires exact f32 bit identity; vector families require exact selected size, component width, raw components and f32 bits; integer/boolean/object/count/version fields require exact equality. Tolerance is zero. `LoadoutsOnline` used the exact caller-resolved object table materialized from the same witness replay.

## 3. Evidence and contract authority

R3.17M remains the K4 wire-format evidence authority, R3.17N remains the exact 161-group contract authority, R3.17O remains production, and R3.17P is the real-replay certification authority. The four layers are intentionally separate.

```text
R3.17M authority             a50f09857f36ac52cec30b4bf3efbde9e15bb564 / 31881779861
R3.17N group SHA256          80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
R3.17O production            492cc8218be7abc6db8f75acaea33d009ab2f175
R3.17P authority             f2d87b732ad3103d50e2c047351f1017d4f3613f / 31937527114
pinned Boxcars SHA           c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane        47
```

## 4. R3.18A exact next pass

Roadmap R3.18 first requires one complete existing-actor property update before a property loop. R3.18A is the read-only evidence decomposition of that first boundary: choose a deterministic real update with `new == false` and `property_present == true`, preserve the already-resolved stream/property/tag context, decode exactly one already-admitted K1/K2/K3/K4 payload, and prove the native `payload_end_bit` equals the pinned Boxcars oracle end bit.

The hard stop is before consuming the next `property_present` bit. R3.18A does not admit a second property, loop continuation, next actor/frame, actor-table mutation, new attribute family, or production code.

## 5. Still closed

```text
second property / next property_present-bit consumption
property_present loop for one actor update
next actor / next frame iteration
actor lifecycle mutation
new attribute family/shape/context admission
raw-state extraction
native event extraction
replay slicing
skill/runtime/export widening
Cargo/corpus/support-lane expansion
```

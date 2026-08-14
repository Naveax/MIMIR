# MIMIR — R3.17I K3 Spatial/Physics Wire-Format Evidence Decision

**Date:** 2026-08-14
**Pass:** `R3.17I — K3 spatial/physics wire-format evidence`
**Outcome:** **A — ADMITTED / COMPLETE**
**Production Rust changed:** **NO**

## Frozen authority

```text
continuity base               4df00aa76a99b85a122210c4f929523f72fe9ef4
native production SHA         9bfa837c69c4751f70ca63a17c65f0f89877ff32
native source blob            7288238cfb5338653552435be6af41f0dd7a4e85
pinned Boxcars SHA            c70e77df7af81b436cb545d070bb90c82f562d0b
R3.17I authority head         8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
authority run/job             31812804986 / 94807233173 SUCCESS
exact-head normal CI          31812804992 / 94807233091 SUCCESS
artifact                      9223916983
artifact size                 1411635 bytes
artifact digest               sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
```

The downloaded canonical artifact ZIP hashes to the same SHA-256 carried by the GitHub artifact digest.

## Evidence result

```text
replay identities                         47 / 47 PASS
oracle replay decode                      47 / 47
K3 occurrences                            1,699,169
exact version/context groups              1,950
privacy-safe witness rows                 6,276
zero required tags                        0
shape mismatch / unclassified             0
bit monotonicity failures                 0
raw packed-payload shape failures         0
privacy scan                              PASS
production mutation                       0
Cargo mutation                            0
corpus / fixture mutation                 0
```

### Location

```text
occurrences                  26,734
replays                      47
version                      868.32 / net10
RL223                        false + true observed
observed structural shapes  7
exact context groups         11
payload widths               11, 31, 34, 52, 55, 59, 62 bits
```

Observed standalone vector size/header outcomes:

```text
size_bits 0  -> header 5 / component width 2
size_bits 7  -> header 4 / component width 9
size_bits 8  -> header 4 / component width 10
size_bits 14 -> header 4 / component width 16
size_bits 15 -> header 4 / component width 17
size_bits 16 -> header 5 / component width 18
size_bits 17 -> header 5 / component width 19
```

### RigidBody

```text
occurrences                  1,550,254
replays                      47
version                      868.32 / net10
RL223                        false + true observed
awake                        1,548,807
sleeping                     1,447
observed structural shapes   1,169
exact context groups         1,934
rotation                     56-bit quaternion only observed
```

Wire order is evidence-consistent with:

```text
sleeping bit
location vector
56-bit quaternion
if awake:
  linear velocity vector
  angular velocity vector
```

Observed vector size/header sets are intentionally recorded per subfield rather than generalized beyond evidence:

```text
awake location:   size_bits 10..19
sleeping location:size_bits 13,16,17,18,19
linear velocity:  size_bits 0..18
angular velocity: size_bits 0..15
```

For net10, observed header length is 5 bits for size_bits 0..5 and 16..19, and 4 bits for size_bits 6..15. Size bits 20/21 and the older 48-bit rotation representation were not observed and are not admitted by this pass.

### ReplicatedBoost

```text
occurrences                  11,058
replays                      11
version                      868.32 / net10
RL223                        true only observed
shape                        u8 x 4
payload width                32 bits
field order                  grant_count / boost_amount / unused1 / unused2
```

### PickupNew

```text
occurrences                  111,123
replays                      47
version                      868.32 / net10
RL223                        false + true observed
None branch                  90,312 / 9 bits
SomeI32 branch               20,811 / 41 bits
wire order                   presence bit / optional signed i32 actor ref / picked_up u8
```

## Durable receipt identities

```text
source scope SHA256          b47aacbcb2c1b6a245b0b8779b6e48369814934f045f2e73db1be98e485cd619
replay identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
instrumentation patch        6acf108213e526e15c463eb7f059a239f6f78b3b20036500c1ed3879e7cca013
groups JSONL                 04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b
witnesses JSONL              4ceb2290f753c59e4c3880eb43817923fbf3d6a44232582ca834205719839fda
summary JSON                 258a81be5c81e660e4db31fcef99b6ee78822496243ebaad0495cc0cb1e44a1e
aggregate                    884fee52b216fbb49ccd6e88be4a10cf66bc9e952ceb853d24923046b4d24e08
receipt manifest             1d63c0c4be779b65f98c3082656a20b42901d524b6b2e3d6171bdfdae3394303
raw Boxcars log              5bc6d8508b2a4af98b405d083f16b425c7fa9d092fc633eff61ff693562e4c5e
```

Durable witness rows contain structural identities, bounded numeric/spatial evidence and packed-payload hashes; unrelated account/player identity material and raw packed payload bytes are not persisted.

## Rejected disposable attempt

`31812224854 / 94805348633` is explicitly non-authoritative. Its frozen gate, Boxcars build/tests, 47-replay scan and analyzer all reached the same Outcome A counts, but the workflow then rejected the valid 1,950 groups / 6,276 witnesses using an arbitrary receipt-size bound. The authority run replaced that bound with the actual invariant: at least one and at most four witnesses per exact group. No analyzer, instrumentation, production, Cargo or corpus semantics changed.

## Capability consequence

R3.17I supplies wire evidence only. It does not make any K3 tag a native MIMIR decoder capability. Production remains R3.17G and still stops after one admitted K1/K2 value.

## Next exact pass

Open `R3.17J — K3 contract admission for evidence-supported shapes only` as contract-only. Production implementation remains forbidden until a later separate pass.

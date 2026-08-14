# MIMIR — R3.17J K3 Evidence-Supported Contract Admission Decision

**Date:** 2026-08-14
**Pass:** `R3.17J — K3 evidence-supported contract admission`
**Outcome:** **A — ADMITTED / COMPLETE**
**Production Rust changed:** **NO**

## Frozen authority

```text
continuity base               77028734ba33818c6ee7cac65f5f9e75aebca0e0
native production SHA         9bfa837c69c4751f70ca63a17c65f0f89877ff32
native source blob            7288238cfb5338653552435be6af41f0dd7a4e85
R3.17I evidence head          8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
R3.17I authority run/job      31812804986 / 94807233173 SUCCESS
R3.17I exact-head CI          31812804992 / 94807233091 SUCCESS
R3.17I artifact               9223916983
R3.17I artifact digest        sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
R3.17I groups SHA256          04e93bdbc964f89d0c3ec79cd11f714f8f2fb74d2dadc7c2bb6e2098cd93a22b
pinned Boxcars SHA            c70e77df7af81b436cb545d070bb90c82f562d0b
supported replay lane         47
```

R3.17J is contract-only. The pinned oracle remains evidence, not a production dependency.

## Exact admitted context

A future K3 entry point must use an explicit caller-resolved context containing:

```text
version_major = 868
version_minor = 32
net_version   = 10
is_rl_223     = caller-resolved bool
```

Any other major, minor or net version is `unadmitted-context`. `is_rl_223` acceptance remains tag/shape-specific through the exact structural allowlist. The K3 contract is intentionally separate from the existing K2 context/API so admitting K3 cannot silently widen K2.

## Common one-value semantics

```text
bit order                 LSB-first
alignment                 unaligned payload start allowed
input                     network bytes + payload_start_bit + resolved tag + K3 context
success                   exactly one K3 value
payload_end_bit           first bit after that value
payload_width             payload_end_bit - payload_start_bit
trailing bits             left untouched; never interpreted as another property
failure                    no partial value escapes
cursor semantics          rollback to payload_start_bit on every failure
arithmetic                checked offsets/widths only
```

Minimum error classes:

```text
invalid-start
insufficient-bits
unadmitted-context
unadmitted-k3-shape
invalid-k3-value
unsupported-k3-tag
```

## Shared net10 vector wire primitive

For the current net10 lane:

```text
low = read 4 LSB-first bits
candidate = low + 16
if candidate < 22:
    discriminator = read 1 bit
    selected_size_bits = candidate if discriminator else low
else:
    selected_size_bits = low
component_width = selected_size_bits + 2
bias = 1 << (selected_size_bits + 1)
raw_x = read component_width bits
raw_y = read component_width bits
raw_z = read component_width bits
signed_component = raw_component - bias
semantic_component = f32(signed_component) / 100.0
```

`selected_size_bits` 20 and 21 remain unadmitted. More importantly, the union `0..19` is **not** a global acceptance range. A decoded vector shape is admitted only when the enclosing tag/context structural key is present in `MIMIR_R3_17J_K3_ADMITTED_GROUPS.json`.

This prevents cross-product widening. R3.17I observed 1,169 unique RigidBody structural shapes but only 1,934 exact RL223-context groups; a field-wise union would admit combinations never seen in evidence.

## Durable exact structural allowlist

Canonical file: `docs/continuity/MIMIR_R3_17J_K3_ADMITTED_GROUPS.json`

```text
source R3.17I groups rows      1,950
Location exact groups            11
RigidBody exact groups         1,934
PickupNew exact groups             4
ReplicatedBoost exact groups       1
allowlist SHA256               9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
```

Packing is collision-free over the admitted domains:

```text
Location:
  (rl223_bit << 5) | selected_size_bits
RigidBody:
  (rl223_bit << 16) | (sleeping_bit << 15) | (location_size_bits << 10)
  | (linear_size_or_31 << 5) | angular_size_or_31
  sleeping uses 31 sentinels for linear/angular
PickupNew:
  (rl223_bit << 1) | some_i32_bit
ReplicatedBoost:
  rl223_bit
```

The exact packed-code arrays are contract authority. Implementation may use a source-local sorted constant representation, but it must be regenerated from this canonical JSON and must not broaden it.

## Location contract

Wire: one admitted net10 vector. Success ends exactly after `z`. The exact RL223/shape pairs are the 11 Location codes in the allowlist. Evidence did **not** observe every one of the seven size shapes in both RL223 contexts, so `RL223 false or true` is not by itself sufficient to admit a Location shape.

## RigidBody contract

Wire order:

```text
sleeping:1 bit
location: admitted vector
rotation: exact quat56
if sleeping == false:
    linear_velocity: admitted vector
    angular_velocity: admitted vector
```

Sleeping payloads contain no velocity vectors. Awake payloads require both.

### Quaternion56

Exactly 56 bits:

```text
largest = 2 bits
a_raw   = 18 bits
b_raw   = 18 bits
c_raw   = 18 bits
```

For each 18-bit value `v`:

```text
max_value = 262143
pos_range = f32(v) / f32(max_value)
range = (pos_range - 0.5) * 2.0
unpacked = range * FRAC_1_SQRT_2
```

Let unpacked values be `a,b,c`; `radicand = 1.0 - a*a - b*b - c*c`; `extra = sqrt(radicand)`. `radicand < 0`, non-finite intermediates or a non-finite reconstructed quaternion are `invalid-k3-value`.

Placement by `largest`:

```text
0 => x=extra, y=a,     z=b,     w=c
1 => x=a,     y=extra, z=b,     w=c
2 => x=a,     y=b,     z=extra, w=c
3 => x=a,     y=b,     z=c,     w=extra
```

The legacy 48-bit compressed quaternion is explicitly unadmitted for this lane. After reading an otherwise field-valid RigidBody, construct its exact packed structural key and require membership in the 1,934-code RigidBody allowlist. Missing membership is `unadmitted-k3-shape` and rolls back atomically.

## ReplicatedBoost contract

Only exact context `(868,32,net10,RL223=true)` is admitted.

```text
grant_count:u8
boost_amount:u8
unused1:u8
unused2:u8
```

Exact width: 32 bits. RL223=false is unadmitted.

## PickupNew contract

Both RL223 contexts are evidenced, but only these branches:

```text
presence=false: presence:1 + picked_up:u8 = 9 bits
presence=true:  presence:1 + actor_ref:i32 + picked_up:u8 = 41 bits
```

The exact four context/branch combinations are all present in the allowlist.

## Planned public production surface for R3.17K

R3.17K may add a **separate** K3 one-value API, reusing `ReplayNetworkAttributeTagV1`:

```text
ReplayNetworkK3DecodeContextV1
ReplayNetworkVector3V1
ReplayNetworkQuaternion56V1
ReplayNetworkRigidBodyV1
ReplayNetworkReplicatedBoostV1
ReplayNetworkPickupNewV1
ReplayNetworkK3ValueV1
ReplayNetworkK3DecodeV1
decode_replay_network_k3_v1(...)
```

The structural codec metadata is retained deliberately so the later differential audit can compare shape as well as semantic values.

## Positive and negative test contract

R3.17K focused tests must synthesize at least one valid payload for **every one of the 1,950 exact structural/context allowlist entries**.

They must also verify fail-closed behavior for wrong major/minor/net version; absent Location context/size pairs; vector size 20/21; vector truncation; every RigidBody candidate structural tuple absent from the allowlist; illicit sleeping velocity continuation; awake missing velocity; quat48; quat56 truncation and invalid reconstruction; ReplicatedBoost RL223=false/truncation; PickupNew truncation; unsupported non-K3 tag; invalid payload start; and trailing-bit non-consumption.

For structural exhaustiveness, tests may enumerate the finite current-lane candidate domain and assert acceptance iff the packed structural key is in the canonical allowlist.

Actual replay payload bytes are not persisted in contract files. R3.17L must regenerate real witness payloads ephemerally from the frozen 47-replay lane and pinned Boxcars, as R3.17H did for K2.

## Required gates

```text
R3.17I identities frozen                   PASS
1950/1950 groups represented               PASS
packed-code uniqueness                     PASS
cross-product widening                     0
unobserved shapes explicit rejects         PASS
atomic failure semantics                   PASS
exact one-value end semantics              PASS
privacy-safe synthetic positive plan       PASS
synthetic negative plan                    PASS
production Rust mutation                   0
Cargo / fixture / corpus mutation          0
```

## Capability consequence

No native K3 capability is created by R3.17J. Production remains R3.17G and may still decode only one admitted K1 scalar or one admitted K2 value.

## Next exact pass

Open `R3.17K — direct native K3 decoder implementation for contract-admitted variants only`.

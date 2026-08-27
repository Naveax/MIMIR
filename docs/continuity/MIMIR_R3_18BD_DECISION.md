# MIMIR R3.18BD — Exact Following-Header Context Contract Decision

**Date:** 2026-08-28
**Outcome:** **A — ADMITTED / BOUNDARY-SPECIFIC EXACT-EIGHT-FIELD CONTRACT**
**Production mutation:** none
**Canonical production:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Canonical continuity base:** `387e1693279dec062d3ef565cc5bc597de3a5a13` / `a0dedfb8de603cc4e000a1777ed074eaed1c3163`
**Contract:** `docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`

## Decision

R3.18BD closes Outcome A. The immutable R3.18BC three-row true-sublane header observation is frozen as exactly **three complete eight-field tuples**, each with evidence multiplicity one. The full mixed lane remains forty rows: **37 false R3.18BA controls are terminators outside header membership**, while only the exact three BC true rows contribute header contexts.

Membership is `exact_tuple_only`. Boolean-only, Float-only, ordinal-6-only, component-only, Cartesian, versionless, RL223-field-dropped, earlier-contract-inherited, or fabricated fourth-tuple membership is rejected. Multiplicity is evidence provenance, not a runtime-frequency promise.

## Exact authority

```text
canonical main before admission       387e1693279dec062d3ef565cc5bc597de3a5a13 / a0dedfb8de603cc4e000a1777ed074eaed1c3163
published-main CI / archive           33124420075 SUCCESS / 33124420084 SUCCESS
production SHA/tree                   5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BC decision / BD spec blobs           7e864047299c6aacdaa7c990dffd1a2064ec7ff4 / b9065f3e7bfa9e3a7d68386c4b49ccb25d2c529f
BC evidence head/tree                 0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
BC authority run/job                  33122152803 / 98691409657 SUCCESS
BC same-head CI                       33122152793 / 98691409674 SUCCESS
BC artifact                           9666964713 / 7795 bytes / sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
BC manifest SHA-256                   d9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf
BC header rows / summary SHA-256      131e8b3c964bb425d470a7036dcc8767f34783c002324bd644fff5749b086189 / fa0cd7467b48bc5a63e95b0245cf41d40cea26b028322d25f6074426c546ec46
BC partition / targets SHA-256        12a6de4ea98e2710ce01a02f19834e52433bd25e6e915aea6f871c3d06428300 / 4f7ae0b8c2a898478ac2f50342129f308e9e2c273f9ceb7a0531fe6656e3148c
BC negatives / validation SHA-256     5714746e1bddbbdf67cd8cec322392644dc366ca05fee98ea87ba420989affee / f7e09e08036d771c36716f5334ea47ec2c8b2cc9f242f57f9ff28bd3055265cf
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted contract

```text
membership policy                    exact_tuple_only
tuple fields                         stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223
frozen lane rows                     40
false terminators                    37 / outside header membership
observed header rows                 3
exact contexts                       3/3
observed multiplicity sum            3
observed tags                        Boolean=2 / Float=1
observed property ordinal            6 on 3/3
witness reselection                  0
native/oracle mismatch               0
following payload / second control   0/0
AT/AJ/Z/P inheritance                false/false/false/false
```

Exact admitted tuples:

```text
(72,  6, 92, Boolean, 868, 32, 10, false) x1
(72,  6, 94, Boolean, 868, 32, 10, false) x1
(110, 6, 58, Float,   868, 32, 10, false) x1
```

## Anti-widening validation

```text
exact tuple equality                 PASS 3/3
exact multiplicity equality          PASS 1/1/1 / sum 3
false terminators outside membership PASS 37/37
tag-only membership                  REJECT
component-only membership            REJECT
Cartesian candidate                  REJECT: (110,6,92,Boolean,868,32,10,false)
version-drop / version mutation      REJECT
RL223 field drop                     REJECT
RL223 false->true candidate          REJECT
fabricated fourth tuple              REJECT: (72,6,999,Boolean,868,32,10,false)
AT-valid BD-absent tuple             REJECT: (60,5,107,Int,868,32,10,false)
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

## Hard stop

R3.18BD admits a contract only. It does not publish a following-header production composition, decode the following payload, read a second later property-control bit, synthesize a header on any of the 37 false terminators, authorize a generalized/repeated property cursor, or widen actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior.

## Next gate

R3.18BE is a separate bounded production pass. It may validate/recompute one exact published R3.18BA mixed-control result. A false BA result must remain a successful no-header terminator. A true BA result may compose exactly one following existing-actor property header with the existing stateless primitive, must require exact R3.18BD eight-field membership, and must stop exactly at `payload_start`. No following payload or second later control is admitted.

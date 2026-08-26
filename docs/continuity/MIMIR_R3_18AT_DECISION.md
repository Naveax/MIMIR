# MIMIR R3.18AT — Post-AQ Mixed-Continuation Following-Header Exact-Context Contract Decision

**Date:** 2026-08-26
**Outcome:** **A — ADMITTED / BOUNDARY-SPECIFIC EXACT-EIGHT-FIELD CONTRACT**
**Production mutation:** none
**Canonical production:** `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`
**Contract:** `docs/continuity/MIMIR_R3_18AT_ADMITTED_HEADER_CONTEXTS.json`
**Contract SHA-256:** `3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5`

## Decision

R3.18AT closes Outcome A. The immutable R3.18AS mixed-continuation following-header observation has been crystallized into a boundary-specific contract containing exactly **16 complete eight-field tuples** with exact observed multiplicities summing to **40**. Membership is `exact_tuple_only`. All forty admitted header rows are `Int`.

The seven R3.18AQ false rows remain successful terminators and are explicitly outside following-header membership. `is_rl_223` is retained as the eighth tuple field even though all current AS rows are false. Earlier R3.18AJ, R3.18Z and R3.18P contracts are methodology/history only and are not inherited or unioned at this boundary.

## Exact authority

```text
canonical main before admission       b8e9bb465bd49974ca23e00c42ea29d59beecb39 / 7480a997259b5f77a88e1326da2ccfbebe801f80
production SHA/tree                   e1ccbef95c8424b689dee7d77fd8fde2af3e0204 / 4e7100625096594bcc5c5b4c6a8054c283643b13
production parent                     ec2d6c29f90863d9e312856043d01fb98a0c2d2d
production lib / AQ test blobs        b886c58400de0efe0a6a6113d79e6f78e751a213 / 983cbda666f40cbc739b250eac87bc4ce0c9eb99
AS execution spec / decision blobs    4b69c75012a7a358522b3399c1e943d537339838 / 8acdd1c4a3ba2a904e9a731bc5e82e7ac50f67e8
AT execution spec blob                479ea581972f74808bf6bb6b041e7087ac672879
AS evidence head/tree                 475650fea59332f74b9f69da50e3e4471622ab7e / 1303071ad3031f4095e29d775afd243286a67b64
AS authority run/job                  32959321642/98147938829 SUCCESS
AS same-head natural CI               32959321531/98147938016 SUCCESS
AS artifact                           9603335255 / 13250 bytes / sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
AS manifest SHA-256                   638f314ea585aa0ad33ea0b2ca7417687139fd67f4a27e04813348210009ae4a
AS header rows / summary SHA-256      b7f9b50935aa559011152c0722a24441d590f262ff2a69e85a51636605b89086 / ecb49bf9ee38d4249b3e6d91c5dec7ceb2288b6ed6452dbbb3dce3304d371a38
AS continuation / terminator SHA-256  3733514eeceea2ae80b5a4a6c3435c210ab3268901bae7be39e9ab1152860900 / 1af0a82eb9ba5a7b65755a99959f1754e1839db0cc61d90eb414e3ee9fedef27
AS canonical publication              32967201830/98172273710 SUCCESS
AS publication receipt artifact       9606191056 / sha256:1d35bd5228d9a186b99eb93c0cd60a86b3714521c7a56c15feb28934656b72e6
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

The R3.18AS ZIP was independently downloaded and its SHA-256 matched GitHub's artifact digest. Its internal manifest hash is the value above and all 13 listed payload entries verify.

## Admitted contract

```text
membership policy                    exact_tuple_only
tuple fields                         stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223
frozen lane rows                     47
false terminators                    7 / outside header membership
observed header rows                 40
exact contexts                       16/16
observed multiplicity sum            40
observed tags                        Int=40
witness reselection                  0
native/oracle mismatch               0
following payload / second control   0/0
AJ/Z/P inheritance                   false/false/false
```

The exact tuple identities and multiplicities are authoritative only through the JSON contract named above.

## Anti-widening validation

```text
exact tuple equality                 PASS 16/16
exact multiplicity equality          PASS 16/16 / sum 40
false terminators outside membership PASS 7/7
tag-only membership                  REJECT
component-only membership            REJECT
Cartesian candidate                  REJECT: (110,5,107,Int,868,32,10,false)
version/RL223-dropping candidate     REJECT
RL223 false->true candidate          REJECT
fabricated seventeenth tuple         REJECT: (60,5,999,Int,868,32,10,false)
AJ-valid AT-absent tuple             REJECT: (60,5,38,Int,868,32,10,false)
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

Multiplicity is evidence provenance, not a runtime-frequency promise.

## Hard stop

R3.18AT admits a contract only. It does not publish a post-AQ following-header composition, decode the following payload, read a second later property-control bit, synthesize a header on a false terminator, authorize a generalized/repeated property loop/cursor, advance actor/frame/lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactuals or widen runtime/export behavior.

## Next gate

R3.18AU is a separate bounded production pass. It may validate/recompute one exact published R3.18AQ result. A false AQ result must remain a successful terminator with no following-header lookup. A true AQ result may compose exactly one following existing-actor property header with the existing stateless primitive, must require exact R3.18AT eight-field membership, and must stop exactly at `payload_start`. It may not decode the payload or another control.

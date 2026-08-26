# MIMIR R3.18AS — One Following-Property-Header Evidence Decision

**Date:** 2026-08-26
**Outcome:** **A — ADMITTED / ONE FOLLOWING HEADER EXACT ON TRUE SUBLANE**
**Production SHA (unchanged):** `e1ccbef95c8424b689dee7d77fd8fde2af3e0204`
**Evidence authority:** `475650fea59332f74b9f69da50e3e4471622ab7e`

## Decision

R3.18AS preserves exactly the immutable R3.18AR 47-row mixed-control lane. The seven published R3.18AQ false rows remain terminators and perform no following-header observation. On only the exact forty true rows, the existing stateless existing-actor property-header primitive and pinned Boxcars ordinal-5 structural oracle agree exactly through one header `payload_start`.

The result is 40/40 exact headers, native/oracle mismatch zero, witness reselection zero, and sixteen unique complete structural/context tuples. All forty observed headers resolve to `Int`. This is evidence only and changes no production capability.

## Exact authority

```text
canonical continuity base             34897d5c7c24bd6ecba526fb3e951681a69d18c6 / bb2e1ba77432af772f15f32a85c334f1dc2e6bf9
production SHA/tree                   e1ccbef95c8424b689dee7d77fd8fde2af3e0204 / 4e7100625096594bcc5c5b4c6a8054c283643b13
production parent                     ec2d6c29f90863d9e312856043d01fb98a0c2d2d
lib / AQ focused-test blobs           b886c58400de0efe0a6a6113d79e6f78e751a213 / 983cbda666f40cbc739b250eac87bc4ce0c9eb99
AS execution spec blob                4b69c75012a7a358522b3399c1e943d537339838
AR decision blob                      8591566a6f375df58b3a83a35e27a0eec65083c6
evidence head/tree                    475650fea59332f74b9f69da50e3e4471622ab7e / 1303071ad3031f4095e29d775afd243286a67b64
authority run/job                     32959321642/98147938829 SUCCESS
same-head natural CI                  32959321531/98147938016 SUCCESS / count=1 / rerun=0
artifact                              9603335255 / 13250 bytes
artifact SHA-256                      0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
artifact manifest SHA-256             638f314ea585aa0ad33ea0b2ca7417687139fd67f4a27e04813348210009ae4a
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
Boxcars instrumentation patch SHA-256 abd386097cc2bd22bdd685f67c13687cd6a3330b12944a43d8d30da109a8e50e
AR source artifact                    9599823813 / sha256:20c7edce0ea6cc2d47168e9cb9bcc517cdad9b9bde78dcf7caa472403e525326
```

The artifact ZIP was independently downloaded and its SHA-256 matched GitHub's digest exactly. The internal manifest recomputed all 13 listed payload files successfully.

## Frozen result

```text
frozen witness identities             47/47
false terminators                     7/7 exact
true continuation rows                40/40
true one-header rows exact            40/40
native/oracle mismatch                0
unclassified                          0
unique exact contexts                 16
observed tags                         Int=40
witness reselection                   0
repeatability                         40/40 PASS
true-header truncation                40/40 PASS
wrong actor                           40/40 PASS
unresolved lookup                     40/40 PASS
wrong upstream exact context          PASS
post-payload-start poison             40/40 PASS
false terminator no-header            7/7 PASS
following payload bits consumed       0
second later control bits consumed    0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                               PASS
```

## Exact context identity

Tuple order is `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)`.

```text
(110,6,49,Int,868,32,10,false) x1
(60,5,106,Int,868,32,10,false) x4
(60,5,107,Int,868,32,10,false) x19
(60,5,113,Int,868,32,10,false) x1
(60,5,115,Int,868,32,10,false) x2
(60,5,117,Int,868,32,10,false) x1
(60,5,122,Int,868,32,10,false) x1
(60,5,130,Int,868,32,10,false) x2
(60,5,131,Int,868,32,10,false) x1
(60,5,134,Int,868,32,10,false) x1
(60,5,144,Int,868,32,10,false) x1
(60,5,60,Int,868,32,10,false) x1
(60,5,69,Int,868,32,10,false) x2
(67,6,81,Int,868,32,10,false) x1
(72,6,84,Int,868,32,10,false) x1
(72,6,87,Int,868,32,10,false) x1
```

The sixteen multiplicities sum to forty. `is_rl_223=false` is retained as an explicit observed context field. It must not be silently dropped merely because every current row shares the same value.

## Durable artifact hashes

```text
source scope                          1de6373e2565692e39d83fe2af5ef72ce30822613bfeaa01a90d47aee35cac14
replay identity                       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
frozen control rows                   8f4d9dd067a8493d9d7cd42f7580ee61612196a5a274ef2d067407308750356b
continuation targets                  3733514eeceea2ae80b5a4a6c3435c210ab3268901bae7be39e9ab1152860900
terminator rows                       1af0a82eb9ba5a7b65755a99959f1754e1839db0cc61d90eb414e3ee9fedef27
Boxcars instrumentation hash file     b457b2e389247fa59e430a24545e412a3c241257e940df804732104cac7cf378
header rows                           b7f9b50935aa559011152c0722a24441d590f262ff2a69e85a51636605b89086
header summary                        ecb49bf9ee38d4249b3e6d91c5dec7ceb2288b6ed6452dbbb3dce3304d371a38
negative controls                     653f6184b0731a9ab4dde9e2188ef19377fa2ab1412fbfbf067dca7a1894ea9e
validation                            75aedf9309f5fc78ecec8b51bf0d19ccabab8b475f6fe7beeddf0b6160cae78c
aggregate                             913156d675c8e106c8428a02ec6b42f54e31dcdd5f9fdc24cba10ef1fc935cab
upstream receipts                     718258f4c6503d22ed2f57c8ee7424b1b729187d7170bf652da869eacb532fc9
same-head CI receipt                  5747393e4c35d52f6ca5fd3b2839ea063cf5ba06a2e4888ec39f9fefb0e9869f
artifact manifest                     638f314ea585aa0ad33ea0b2ca7417687139fd67f4a27e04813348210009ae4a
```

## Boundary consequence

R3.18AS admits evidence only. It does not admit production following-header composition, payload decoding or another control. The seven false rows remain terminators. Because the true lane contains sixteen distinct complete contexts, a separate exact-context contract pass is required before production composition.

## Next gate

R3.18AT is contract-only. It may crystallize only the sixteen exact eight-field tuples and their exact observed multiplicities from the immutable forty true AS rows. Membership must be exact tuple equality. Tag-only, component-only, Cartesian, versionless, RL223-dropped/flipped, older AJ/Z/P inheritance and any seventeenth tuple remain rejected.

# MIMIR R3.18BC — One Following-Property-Header Evidence Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / READ-ONLY HEADER EVIDENCE CLOSED**
**Canonical production:** unchanged at R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Canonical continuity base:** `2296eb7eb93ac4946bb5b7152f5bc76ff4bf09d8` / `27b40170f2193d972bccf618ee6e2ef7f36806fb`

## Decision

R3.18BC closes Outcome A. The immutable R3.18BB forty-row lane is preserved exactly: all 37 false published-BA controls remain strict terminators, while only the exact three frozen true witnesses enter the following-header lane. Each true witness produces exactly one native property header matching pinned Boxcars through `payload_start`, with zero following-payload or second-later-control consumption.

Three complete eight-field structural contexts were observed. No Cartesian/component/tag-only widening is admitted by this evidence pass. Production remains R3.18BA; a separate R3.18BD contract-only pass must freeze exact context membership before production composition can be considered.

## Exact authority

```text
production SHA/tree                    5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
continuity base/tree                   2296eb7eb93ac4946bb5b7152f5bc76ff4bf09d8 / 27b40170f2193d972bccf618ee6e2ef7f36806fb
evidence head/tree                     0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
workflow blob                          e2c926f05379ff164bb5d3bfdd6f48347817a5af
runner / analyzer / extender blobs     546f3fd6e08d73834c2d405b5d7ec7cae57aaa08 / e2ebd01039af0d14f420ed2048beb158801cf658 / 06c84b5bfc4c4170e1d4268f72a62b09b09ff875
authority run/job                      33122152803 / 98691409657 SUCCESS
same-head natural CI                   33122152793 / 98691409674 SUCCESS
artifact                               9666964713 / 7795 bytes
artifact SHA-256                       88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
artifact manifest SHA-256              d9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf
manifest entries                       14/14 PASS
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Frozen result

```text
BB source partition                    40/40
published BA reconstruction            40/40
false terminators                      37/37
true continuation rows                 3/3
one following header                   3/3
unique exact contexts                  3
native/oracle mismatch                 0
witness reselection                    0
repeatability                          PASS 3/3
header truncation                      PASS 3/3
corrupt BA negative                    PASS 3/3
wrong actor negative                   PASS 3/3
unresolved lookup negative             PASS 3/3
wrong context negative                 PASS 3/3
post-payload-start poison              PASS 3/3
false terminator no-header             PASS 37/37
fabricated continuation identity       PASS
following payload bits consumed        0
second later control bits consumed     0
earlier contract inheritance assumed   0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                                PASS
```

## Exact observed contexts

Membership candidates for R3.18BD are exactly these complete tuples, each observed once:

```text
(stream_id_bound=72,  prop_id_bits=6, property_object_index=92, attribute_tag=Boolean, version_major=868, version_minor=32, net_version=10, is_rl_223=false) x1
(stream_id_bound=72,  prop_id_bits=6, property_object_index=94, attribute_tag=Boolean, version_major=868, version_minor=32, net_version=10, is_rl_223=false) x1
(stream_id_bound=110, prop_id_bits=6, property_object_index=58, attribute_tag=Float,   version_major=868, version_minor=32, net_version=10, is_rl_223=false) x1
```

Observed tags are Boolean=2 and Float=1. All three observed properties are ordinal 6. Shared components are descriptive evidence only and do not authorize component-only membership.

## Superseded non-authority seal attempt

Evidence head `a285ee75c8974f18edad1ef271897a63ea51e311` / run `33120199300` is not authority. Its science, same-head CI, manifest generation and artifact upload passed, but the job failed at the final artifact-seal comparison because the REST artifact digest includes the `sha256:` prefix while `actions/upload-artifact@v4` exposes the digest output as bare hex. The failed SHA was not rerun. The authoritative sibling `0f4d07f5...` retained the science helper blobs unchanged and corrected only the seal normalization / v2 branch trigger.

## Hard stop

R3.18BC admits no production following-header composition and no following payload. The 37 false rows remain terminators. No second later control, repeated/generalized property cursor, next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted.

## Next gate

R3.18BD is contract-only. It may freeze only the three evidence-supported complete eight-field tuples above, each with observed multiplicity one, and must preserve all 37 false terminators outside membership. No production code or payload decode belongs in R3.18BD.

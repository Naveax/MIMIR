# MIMIR R3.18BM — One Following-Property-Header Evidence Decision

**Date:** 2026-09-09
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**
**Production changed:** **NO**
**Canonical production:** R3.18BK `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`

## Decision

R3.18BM closes Outcome A. The immutable three-row R3.18BL/R3.18BK mixed-control lane remained exact: one false row terminated at the published BK boundary and exactly two true rows observed exactly one following existing-actor property header through `payload_start`.

Native MIMIR and pinned Boxcars matched **2/2** through the full header boundary. The two rows classify as exactly two complete eight-field contexts. Mismatch, unclassified rows, and witness reselection are all zero. Following-payload and second-later-control consumption are both zero. Production/Cargo/fixture/corpus/support mutation remained `0/0/0/0/0`.

## Immutable receipts

```text
canonical continuity base             607361a67b7eb03a868114b0171f30a6d26873e6 / 8a83d5d80b39d79cc7d3fc8612d02bd911e3446e
production SHA/tree                   f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf / 07656c7a43c1afb97903ef33c1109b764fbf8b7d
BM evidence head/tree                 689b1a24b57a84c81dc19c9a308fb1423f191c4b / 1d4e95409e1125b01a78aae6a436190b3c1381f4
BM evidence run/job                   34334615939/102410984005 SUCCESS
BM same-head natural CI               34334615886/102411487443 SUCCESS
BM artifact                           10097405795 / 8340 bytes / sha256:bd51a612be2cdd87d9ce1eb141f3f77f47ae29d42aabc8fc16c260a175f27963
BM archive members                    14
BM inner manifest                     sha256:167021cca2259c4d2ef16e9da50503007f381349219adb0f5684849f69f2cbd2 / 13/13 PASS
BM header rows                        sha256:2210a7c5e5d74f7ab95e0ace692462979bc4ac5934073b886a29c56085524ae0
BM header summary                     sha256:9b021ea415e76e06b8b38033c3d37a8ca11a8ca938ec5dfd4c9fd9096c690434
BM negatives                          sha256:0ebf4aa8ac72934f7c42af35560ce29db7f8fa32b772204f0a47a4e2526ee4d0
BM validation                         sha256:a21b33d5b5b0566b1f4f071178fcd40787ba6f8891b08627202f8ac556235bc9
BM same-head CI receipt               sha256:255a763ff6aa0ec566654c1f1fd9be95a1111669b1fbbebb53763771734a87ec
BM upstream receipts                  sha256:d98dc9d6002add804e6837ee9eeedc390682c665c531b52ca0a3f3bbcef43e1d
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

The ZIP SHA-256 was independently recomputed against fresh GitHub artifact metadata. All 13 manifest-listed non-self files independently verified, and the archive contains 14 members including the manifest itself.

## Exact frozen result

```text
frozen BL/BK control rows             3/3
false terminators                     1/1
true continuation rows                2/2
one following header exact            2/2
unique exact contexts                 2
property ordinal                      7 on 2/2
native/oracle mismatch                0
unclassified                          0
witness reselection                   0
following payload bits                0
second later control bits             0
production/Cargo/fixture/corpus/support 0/0/0/0/0
privacy                               PASS
full repository validation            PASS
```

Exact observed contexts, each multiplicity one:

```text
(72,  6, 95, Boolean,     868, 32, 10, false) x1
(110, 6, 66, ActiveActor, 868, 32, 10, false) x1
```

Tuple field order is:

```text
stream_id_bound, prop_id_bits, property_object_index, attribute_tag,
version_major, version_minor, net_version, is_rl_223
```

Exact row coordinates:

```text
external_fixtures/sample_002.replay
  BK true             11231 -> 11232
  stream_id           62 / bound 72
  header stop         11238
  payload_start       11238
  property index/tag  95 / Boolean

test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay
  BK true             3198 -> 3199
  stream_id           60 / bound 110
  header stop         3205
  payload_start       3205
  property index/tag  66 / ActiveActor

external_fixtures/sample_003.replay
  BK false terminator 7815 -> 7816
  following header    forbidden / zero access
```

## Negative controls

```text
repeatability                         PASS 2/2
header truncation                     PASS 2/2
corrupt BK prior                      PASS 2/2
wrong actor                           PASS 2/2
unresolved lookup                     PASS 2/2
wrong context                         PASS 2/2
post-payload_start poison             PASS 2/2
false terminator no-header            PASS 1/1
fabricated/substituted continuation   PASS
```

## Sequencing consequence

The next pass is **R3.18BN — Exact Following-Header Context Contract After R3.18BM**.

R3.18BN is contract-only. It may freeze only the two exact complete eight-field contexts observed above. It must preserve `sample_003` as a false terminator outside header membership and reject tag-only, component-only, Cartesian, versionless, RL223-field-dropped/flipped, older-contract-inherited, or fabricated membership.

## Hard stop

R3.18BM admits evidence only. No production following-header composition, following payload decode, second later property control, header success on the false row, generalized/repeated property cursor, witness expansion, actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted.

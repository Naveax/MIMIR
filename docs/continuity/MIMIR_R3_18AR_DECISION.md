# MIMIR R3.18AR — Published R3.18AQ Mixed Following-Control Differential Decision

**Date:** 2026-08-26
**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL COMPLETE**
**Production SHA (unchanged):** `e1ccbef95c8424b689dee7d77fd8fde2af3e0204`
**Evidence authority:** `7dfe2a0fc451a40d4c750dd2e401a2f0aa36dd9d`

## Decision

R3.18AR validates the published R3.18AQ mixed following-control API against exactly the immutable R3.18AP 47-row authority lane. Published AQ reconstructs the valid AN prerequisite, starts at the frozen AP control boundary, returns the exact frozen boolean, ends/stops one bit later, and consumes nothing adjacent.

The exact distribution is **false=7 / true=40**. Both classes remain valid published AQ results. The seven false rows are terminators; the forty true rows are the only continuation candidates.

## Exact authority

```text
canonical continuity base             5bf20063a829526cc090ada8c4221d6b42ae5655 / 8fa16095e28b418d12c3050c69462ecae64ba880
production SHA/tree                   e1ccbef95c8424b689dee7d77fd8fde2af3e0204 / 4e7100625096594bcc5c5b4c6a8054c283643b13
production parent                     ec2d6c29f90863d9e312856043d01fb98a0c2d2d
lib / AQ focused-test blobs           b886c58400de0efe0a6a6113d79e6f78e751a213 / 983cbda666f40cbc739b250eac87bc4ce0c9eb99
AR execution spec blob                01492ab1495dd93d5f066282773020d5b2890dc5
evidence head/tree                    7dfe2a0fc451a40d4c750dd2e401a2f0aa36dd9d / 85a48eebc2d3292c524f482b5c131156fa8d7931
authority run/job                     32949846799/98118570100 SUCCESS
same-head natural CI                  32949846724/98118570114 SUCCESS / count=1 / rerun=0
artifact                              9599823813 / 9680 bytes
artifact SHA-256                      20c7edce0ea6cc2d47168e9cb9bcc517cdad9b9bde78dcf7caa472403e525326
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
AP artifact                           9526988237 / sha256:b50b01bd87c0b61ca2e407abe43ac5db9fb15290f7cd3e908332d2ac2a26c4cc
```

The artifact ZIP was independently downloaded and its SHA-256 matched GitHub's digest exactly. Its internal manifest recomputed 10/10 files without mismatch.

## Differential result

```text
frozen witness identities             47/47
published AQ exact                    47/47
published AN prerequisite exact       47/47
false                                 7
true                                  40
mismatch                              0
witness reselection                   0
repeatability                         47/47 PASS
next stream bits consumed             0
next header bits consumed             0
next payload bits consumed            0
second later control bits consumed    0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                               PASS
```

## Negative and validation gates

Truncation before the control, wrong actor, unresolved lookup, wrong exact context, corrupt AN prior, post-stop poison and the source-scope one-read/no-loop guard all passed. Focused AQ tests, Rust 1.85 formatting, workspace check/test/clippy with warnings denied, full repository verifier, git diff check and clean-worktree verification passed.

## Durable artifact hashes

```text
summary                               7b389bbb7f10945bea36d36dde6d47403922ae7774d59192c3865551b9c6aad5
comparison                            8f4d9dd067a8493d9d7cd42f7580ee61612196a5a274ef2d067407308750356b
negative controls                     c9ccb6c5d97c3184ee93223d0938b631e0ec246e2712a17cc4c1a02738904d86
validation                            ce3f97f4f2119052962204a4d90f52e22bb37245c44a3ebc27515f86e6b1c9f7
aggregate                             90351a3d73d9de1b882b5dd1450d82764552c764865a18df80840fa7876795d9
```

## Boundary consequence

R3.18AR certifies the published AQ boundary; it does not widen production. Exactly seven rows terminate after the AQ control. Exactly forty rows may be considered for a later following-header evidence pass.

## Next gate

R3.18AS is a separate read-only following-header evidence pass. It may inspect exactly one following property header only on the exact 40 true rows, using the existing stateless header primitive and pinned Boxcars, and must stop at `payload_start`. It may not decode the payload, read another control bit, or pre-admit a header tag/context distribution.

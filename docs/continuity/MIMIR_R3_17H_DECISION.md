# MIMIR — R3.17H Native K2 Differential Audit Decision

**Date:** 2026-08-14
**Pass:** `R3.17H — native K2 differential audit against immutable R3.17E evidence-supported witnesses`
**Outcome:** **A — ADMITTED / COMPLETE**
**Production Rust changed:** **NO**

## Frozen authority

```text
continuity base               2d338d4244ce07122bb97097c516193f68ff73b7
native production SHA         9bfa837c69c4751f70ca63a17c65f0f89877ff32
native source blob            7288238cfb5338653552435be6af41f0dd7a4e85
R3.17E evidence head          19db534a3668f84f1c5ce36ef1252c52841d890f
R3.17E artifact               9219554878
R3.17E artifact digest        sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
R3.17E witnesses SHA256       7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
pinned Boxcars SHA            c70e77df7af81b436cb545d070bb90c82f562d0b
R3.17H authority head         9b8e8fe82ab5bdc663eecc3f5d3cd1e3b8ee38ac
authority run/job             31809282874 / 94795704797 SUCCESS
exact-head normal CI          31809282903 / 94795705073 SUCCESS
artifact                      9222624242
artifact digest               sha256:d6c773d593c3c50957507a19056e85aef8b769fdc03fd88c6d693b1258c0af28
```

## Differential result

The exact immutable 469 R3.17E witness occurrences were regenerated from all 47 supported replay identities. Raw/oracle semantic material existed only in ephemeral runner storage. The packed payload for each selected occurrence was normalized to bit zero without changing the packed bit sequence, then decoded by the frozen R3.17G native decoder.

```text
47 replay identities                     PASS
oracle regeneration                      47/47 / 110539 K2 occurrences
immutable witness selection              469/469
native decode success                    469/469
attribute tag / semantic variant         469/469 exact
payload width                            469/469 exact
payload end / consumed bits              469/469 exact
context gate                             469/469 exact
semantic value                           469/469 exact in-memory
negative controls                        7/7 PASS
privacy scan                             PASS
production mutation                      0
Cargo mutation                           0
corpus / fixture mutation                0
```

The seven fail-closed controls covered PartyLeader None, non-Epic PartyLeader, an unadmitted UniqueId system, wrong UniqueId net version, RL223 QWordString Empty, RL223 QWordString UTF16 and wrong Epic declared length.

## Durable receipt identities

```text
source scope SHA256          faff88fd850dfd9e6e8fd6b840a584f5890d27b394b938384d5944dddbf61c6c
replay identity SHA256       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
driver manifest SHA256       c27363f06a5eb408f5af925b3e86d4f5f7e0db687fddd337b9cf5e3c7cc3f573
match rows SHA256            745d4db19c55f91a3f8b8b88d85db866aeb3c8d64f15570a0f9af52677e37375
summary SHA256               24f9233670e52c8cd384782d7e4449bce91e7c06b54310a82cad1c1860c118e2
aggregate SHA256             752dd675cf211ea47aa2daa928032a4e104c4e68d0224dc8b98d6079b09b7701
```

Durable rows contain structural identities, cryptographic hashes and match flags only. Clear player names, account IDs, raw identity payloads and private text were not persisted.

## Rejected disposable attempts

Two earlier temporary runs are explicitly non-authoritative:

```text
31808925259 / 94794512217
  stopped before oracle build because the workflow attempted an unnecessary direct raw-SHA fetch

31809102097 / 94795103857
  stopped before oracle build because a canonical helper was checked with a line-ending-sensitive file SHA256
```

Neither reached native-vs-oracle semantic comparison. V3 froze the canonical helper by immutable Git blob identity `e6a551154a90ba7fa2cf5b887c9a8cfb9cfe933c` and is the sole audit authority.

## Capability consequence

R3.17H confirms the already-published R3.17G K2 surface. It does **not** widen production capability. One successful K2 value still stops at its exact payload end bit; no second property, actor/frame iteration or lifecycle mutation is admitted.

## Next exact pass

Roadmap order makes the first unfinished attribute wave `K3 spatial/physics`. Open:

`R3.17I — K3 spatial/physics wire-format evidence` for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew` only.

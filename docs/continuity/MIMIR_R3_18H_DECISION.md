# MIMIR R3.18H — Production Second-Property Header Differential Decision

**Date:** 2026-08-16
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE**
**Production authority:** `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c`
**Production mutation:** none

## Decision

R3.18H is admitted. The published R3.18G bounded optional second-property-header composition matches the frozen R3.18F real-replay oracle lane exactly on all 94 rows. The pass remains evidence-only and does not admit second-payload production decoding, a third property or a repeated property loop.

## Exact authority

```text
canonical main at evidence start    63f5de4e49abaf76fe6441a255a1a6770388a63c
production SHA/tree                 2b608aafae97b10ecbc884f99e4bd4a73abf7a5c / b130caf211ce72577870c70d6c0d87cd006e1b29
production lib.rs blob              5e2b9e5be9c6692e499abc97a89655c603728cef
R3.18G focused test blob            d56bf97d250b426e23fec4610cbb9ead6ec8a142
R3.18H spec blob                    4b3eacad1698b22c421adda6af4a5142ced291e6
evidence head/tree                  1db03fddabf84bfa189f983fa4a3b9110d105442 / be84d7709d60477bcbb916a11b4496dbddac2ab2
authority run/job                   31960174729 / 95196833572 SUCCESS
same-head normal CI                 31960174713 / 95196833409 SUCCESS
artifact                            9267045757
artifact size                       12070 bytes
artifact digest                     sha256:340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645
```

## Frozen evidence result

```text
frozen replay identity              47/47
frozen witness rows                 94/94
native rows                         94/94
terminator rows                     47
continuation rows                   47
continuation Int                    46
continuation String                 1
terminator second_header=None       47
real header truncation rows         32
terminator no-lookup rows           47
unresolved-stream negative          PASS
tag outside Int/String negative     PASS
repeatability                       PASS
post-stop poison                    PASS
second payload bits consumed        0
third property bits consumed        0
native/oracle mismatch              0
production/Cargo/fixture/corpus/support mutation  0/0/0/0/0
```

Frozen R3.18F replay-identity SHA256 remains `b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf`; frozen witness SHA256 remains `99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7`, proving the lane was not silently reselected.

Artifact file SHA256 receipt:

```text
r3_18h_source_scope.txt             38ff92a2448883802b73ea4e2ee0a65f18b83beb782d8f8c87451e2295f37fb8
r3_18h_replay_identity.tsv          b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
r3_18h_frozen_witnesses.json        99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
r3_18h_oracle_regeneration.txt      97767f90f5f9d46afcb68f568cf28d021f2081ddbf62bb5f2536d8d7d1bf569e
r3_18h_comparison.json              de4ca9d70fb7f56aec1c279473c3289b236cfa48e3a17f1faec8942ac3548d10
r3_18h_negative_controls.txt        4d0273b85c5af2ae2e2b1fd7b88fd5d876c210d1a20f4cdd544601d649c053c9
r3_18h_aggregate.txt                4357bc88426ac50da065875f56bc2f806158080767292c6210623091f6fdc31b
```

## Hard stop

R3.18H admits no second-property payload production composition or semantic API, no third property/control bit, no generalized loop/cursor, no new tag context, no actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior and no dependency/support-lane widening.

## Next gate

R3.18I is a separate read-only second-property payload contract/evidence audit. It may characterize exactly one second payload on each of the 47 frozen continuation rows and must keep the 47 terminators as no-payload controls. It stops at the payload end and may not read a third `property_present` bit.

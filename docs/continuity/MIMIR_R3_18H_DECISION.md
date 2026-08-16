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
artifact size                       18658 bytes
artifact digest                     sha256:340f75e22875cb5b00d66f2b4b05bbd6aa9c1a64625d79d0fb5bd0dcc104bb79
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
r3_18h_source_scope.txt             b85b1324cca458aa68a7433484831371097492388657401776329801d8b31ab1
r3_18h_replay_identity.tsv          b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
r3_18h_frozen_witnesses.json        99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
r3_18h_oracle_regeneration.txt      9c8ace30317132246911e5406cc425af862b61de8a59fe270c3f91a1fbbc7690
r3_18h_comparison.json              88767c2b2087cec0313d10df0d4354c13928f1f8596c4d7e2041f5d4eeefac3
r3_18h_negative_controls.txt        272854040775158cd948dd313dcec5da7cdf6a238050e03b7fc20b8434f8962e
r3_18h_aggregate.txt                6ff5e750569b4343518cb9c3fd0d8119f610d515b15434732097176482c8bbbc
```

## Receipt correction

The original continuity publication recorded a stale outer artifact receipt and stale hashes for five regenerated evidence files. R3.18I v1 (`9c2bc511fd20a6ef194fa3ecdce3ebb1ebf5bd3a`, `31963757848 / 95205621914`) detected that mismatch at authority freeze and stopped **before any payload evidence**. Fresh GitHub artifact metadata and the final R3.18H job receipt now agree with the downloaded artifact: API digest `sha256:340f75e22875cb5b00d66f2b4b05bbd6aa9c1a64625d79d0fb5bd0dcc104bb79`, size `18658` bytes, and all seven inner evidence hashes listed above. The downloaded ZIP bytes hash to `a0101720526e633974390dda46786fc471baa7679f387b7e03d97b5bcf7bcb55`; that local ZIP hash is intentionally recorded separately from GitHub's API artifact digest. Receipt manifest file SHA256 is `5a381630b2fc01bdc41babbb1aafe6542ff4bebbf5a99a50618214d546008b2b`.

This is a documentary correction only. Frozen replay identity, frozen witness identity, Outcome A aggregate, zero mismatch, zero second-payload/third-property consumption, zero production mutation and production authority `2b608aafae97b10ecbc884f99e4bd4a73abf7a5c` are unchanged.

## Hard stop

R3.18H admits no second-property payload production composition or semantic API, no third property/control bit, no generalized loop/cursor, no new tag context, no actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export behavior and no dependency/support-lane widening.

## Next gate

R3.18I is a separate read-only second-property payload contract/evidence audit. It may characterize exactly one second payload on each of the 47 frozen continuation rows and must keep the 47 terminators as no-payload controls. It stops at the payload end and may not read a third `property_present` bit.

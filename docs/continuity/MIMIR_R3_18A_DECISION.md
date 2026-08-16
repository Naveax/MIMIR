# MIMIR — R3.18A Decision

**Date:** 2026-08-16
**Pass:** `R3.18A — existing-actor single-property boundary evidence`
**Outcome:** **A — ADMITTED / EVIDENCE COMPLETE**
**Production mutation:** none

## Decision

A real existing-actor update can be composed from the already-published R3.16B property header boundary through exactly one already-admitted primitive payload and stopped at the exact Boxcars payload end without reading the next `property_present` bit. This closes the evidence prerequisite for the first production one-property composition. It does **not** admit a property loop.

## Frozen authority

```text
execution base main          c5878cf755302fe52e9e67741486306cd30db059
production SHA               492cc8218be7abc6db8f75acaea33d009ab2f175
authority head               12ee215fd843260d5ece14f27aa1171cb862f49e
authority run/job            31941400273 / 95151024131 SUCCESS
exact-head normal CI         31941400276 / 95151024211 SUCCESS
artifact                     9262129856
artifact digest              sha256:295247a5f73159ac74539ffc5abf1eb2273fb6dc07a57f8b16976552a17b3ab8
pinned Boxcars               c70e77df7af81b436cb545d070bb90c82f562d0b
replay identity/oracle       47/47
eligible first properties    47 scalar candidates
```

## Selected real witness

```text
replay                       external_fixtures/sample_001.replay
frame                        0
actor ordinal / actor id     63 / 2
actor context object         98
property ordinal             0
stream id / bound            27 / 67
prop_id_bits                 6
property object              55
attribute tag                Int
semantic value               62
property_present bits        [10227,10228)
stream bits                  [10228,10234)
payload bits                 [10234,10266)
payload width                32
payload SHA256               d2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f
```

Native header identity, payload start, semantic value, and payload end all matched the pinned Boxcars oracle exactly. `next_property_present_consumed_bits = 0`, the truncated payload negative failed closed, mismatch count is 0, and the durable artifact passed the privacy gate.

## Scope and mutation audit

```text
production Rust              unchanged
Cargo manifest/lock          unchanged
fixtures                     unchanged
corpus                       unchanged
support lane                 unchanged
raw payload cleartext        not durable
production/Cargo/fixture/
corpus/support mutation      0/0/0/0/0
```

Receipt SHA-256 values:

```text
source scope                 1d8cce3aa2dd0d16f6ddd04a1b03f8e1fc3aa9ff231b2c224611b1cbda492ac9
replay identity              b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation      97c2d07c16c7367e76e5f42a2383ee58e0aa970edcb04fa877ab6a24e49b5e44
selected witness             e67b93106d2c880db20ec6d80b788a78ca9753e271d64882128ff5a886386364
selection summary            33b93011ffded48a1a2a25a477cf5b16f0886394ebb160cdb377f26fffcc783f
comparison                   ae6167b401e84fdd33383fb9fc3294dc472d2fafb0d58377cc021a7db4bd9194
aggregate                    f29bec6fc775b87f339bce94fde3a9ed9e10e46d78141e1299fcce1c4441e18b
```

## Non-authority attempts

The first disposable head stopped on rustfmt in the temporary native probe. The next head produced valid evidence but same-head normal CI rejected `usize::is_multiple_of` because it is newer than MIMIR's Rust 1.85 MSRV. Neither is authority. The final head `12ee215fd843260d5ece14f27aa1171cb862f49e` reran the full oracle scan, native comparison, privacy/mutation gates and normal CI after the tooling-only correction.

## Next exact pass

`R3.18B — minimal native existing-actor single-property K1 composition`.

R3.18B may compose only the existing first-property header with the existing primitive K1 decoder. Property-loop continuation, K2/K3/K4 composition in this API, next actor/frame and lifecycle mutation remain closed.

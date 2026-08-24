# MIMIR R3.18AO — Published R3.18AN Post-AK Following-Payload Differential Decision

**Date:** 2026-08-24
**Outcome:** **A — ADMITTED / PUBLISHED DIFFERENTIAL EXACT**
**Production mutation:** none
**Canonical production:** `3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38` / `3efcc244bca55623b12bb21eb277753fc61144d4`

## Decision

R3.18AO closes Outcome A. On exactly the immutable 47 R3.18AM witnesses, the published R3.18AN API reproduced the frozen AK/AJ header authority and one following `Int/32` payload through its exact payload end on all 47 rows. Published AN, frozen AM and independent direct-native/oracle identity matched 47/47 with mismatch zero. The pass consumed zero next property-control bits.

This decision admits only the differential closure. It does not admit any value of the next `property_present` bit, a next stream/header/payload, a second later control bit, alternate payload layouts, a generalized property cursor/loop or semantic/runtime widening.

## Exact authority

```text
canonical main before admission     68014a3b9aa3e5a84a4a03c2464863e9a60bfec2 / 6180021a44355e92348785d1f0f0d50002fb1a66
production SHA/tree                 3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38 / 3efcc244bca55623b12bb21eb277753fc61144d4
production lib / AN test blobs      9d6b5ae2898cee745a17de9d1d7ef4b8fbd0e822 / 8aa48b2b74d0956d1d2e965d056e1cf14a81f703
AO execution spec                   docs/continuity/MIMIR_R3_18AO_EXECUTION_SPEC.md
evidence head/tree                  0f5ecb5b1dccf35aaabf6a45645bc70ad8a68a1c / 59126fe2757ecc500a5cc6f822d76fbc380ef85b
authority run/job                   32734420624/97453768432 SUCCESS
validation-only PR                  #194 closed unmerged
same-head normal CI                 32734946566/97455429462 SUCCESS
artifact                            9522750814 / 4619 bytes
artifact ZIP SHA-256                sha256:2e34f3be6963b2b6031a395e85e9699b64df7413d62dd9809fa8fd9794547d73
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
R3.18AJ contract                    sha256:cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c
R3.18AM authority                   842b94ed4c4e57323433585fea48116ecf18989b / artifact 9443581172 / sha256:2f65de5207bd96787fd7d1527a55991f08d5da614a0ddfce22a7aa267968e3c8
```

The downloaded R3.18AO ZIP digest equals the GitHub artifact digest exactly. Its manifest contains seven payload entries and all seven verified.

## Admitted evidence

```text
frozen rows                         47/47
published R3.18AN exact             47/47
R3.18AM/direct-native/oracle exact  47/47
Int tag                             47
payload width 32                    47/47
semantic Int range                  1..415
native/oracle/published mismatch    0
witness reselection                 0
next property-control bits consumed 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                        PASS
```

Artifact payload SHA-256:
- aggregate `63af8982928307ad6432a5935e32cd229f9316a1800c130e9547fdb4be0b0f3b`
- comparison rows `40b08b16f857aecd7e15b9cb6f20d5b35a1d5ff2fd280989e217e5b4511de343`
- negative controls `7d88f48abc322b49c35d7b7e246b9db7a7d2708e2391816b9eb901a3875f3bf7`
- source scope `c85e47a18a772aafd38b27524dc69ec90e2f1eb123dd7f6ff13d89916c39b815`
- summary `fbde2f6bd1f64f20bc685802e64dc267c934acc2ceeaad1a0f230c8b8e8436d4`
- upstream receipts `cf255d2f1be329f8ca21a60f6fbd9d25797ea6ea8a3baaa708be7402df192419`
- validation `05e30505bfafb841df4eab519aaeeb4f4645dd8dba3e0f900651bbb3ee981d35`
- manifest file `016c533cdde6b1cbd093a86227b0f989940ce39a1d27452144d35781bc21736a`

## Negative and validation authority

Payload truncation, wrong actor, unresolved lookup, wrong exact version/context, non-AJ/fabricated/old-Z-only tuple, corrupt AG/control/prior authority, wrong payload start, unsupported payload shape and post-stop poison gates passed. Focused AN/AK tests, formatting, workspace check/clippy/test and repository verification passed.

## Hard stop

No next control value is admitted by R3.18AO. No next stream/header/payload, second control, loop/cursor, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior is admitted.

## Next gate

R3.18AP is a separate read-only evidence pass. It may reconstruct the exact published R3.18AN result on the same 47 rows, then observe exactly one next `property_present` bit beginning at `R3.18AN.stop_bit`, cross-check that bit against pinned Boxcars with independent LSB-first evidence logic, and stop exactly one bit later. It may not resolve the following stream/header/payload or read a second control bit.

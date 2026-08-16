# MIMIR R3.18E — Production Control-Bit Differential Decision

**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL COMPLETE**
**Production SHA (unchanged):** `4adadd185783954c7fb6ad67db14b77b377cdde5`
**Evidence authority head:** `aae03a7fdec85e30be3954d14ffdc8cd1d86121e`

## 1. Decision

R3.18E validates the published R3.18D one-bit after-first-K1-property control API against pinned Boxcars on the exact supported real-replay lane. All required deterministic witnesses matched exactly. This admits the evidence result only; it does not widen production into a second-property decoder or repeated property loop.

## 2. Exact receipts

```text
canonical continuity base             dd7d9550910a0ad08cd5f1a171d782b5dd4e954a
production SHA/tree                   4adadd185783954c7fb6ad67db14b77b377cdde5 / 67b1969eaff49d2913b88b3921f27b1bd7fe8193
evidence authority head               aae03a7fdec85e30be3954d14ffdc8cd1d86121e
authority run/job                     31949407736 / 95170443262 SUCCESS
same-head normal CI                   31949407685 / 95170443059 SUCCESS
artifact                              9264243765
artifact SHA256                       005afc3c97bd6bdb9aef69be993538fd813e30481923c59beefcf37e71cdfc9b
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## 3. Differential result

```text
replay identity / oracle parse        47/47
terminator rows                       47
continuation rows                     47
total selected rows                   94
native first-property success         94/94
native control success                94/94
first stop == oracle control start    94/94
control start exact                   94/94
control boolean exact                 94/94
control end/stop exact                94/94
native/oracle mismatch                0
aligned truncation rows               6
second stream/header/payload bits     0/0/0
privacy                               PASS
production/Cargo/fixture/corpus/
support mutation                      0/0/0/0/0
```

Observed K1 tag distribution across the 94 rows was Boolean=1, Byte=6, Float=41 and Int=46. Negative controls for exact truncation, post-stop poison, repeatability and malformed-first-property rejection all passed.

## 4. Immutable artifact file hashes

```text
source scope                          3af876d4fee21e6f769b8db908babb67ec061dcc9265ab266aa4a0ce89a6d42a
replay identity                       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation               cd52172333fd095377c15d263f1f178291eb3588a637cc34720a202bc1408667
selected witnesses                    3fbbece797c146e71dd5b569cce6882d5719ea2d39ecdd5198da351dc028e4c8
selection summary                     353d90d7385fcf34f4dca246d63949653f7124641cf7a81185e62b32e0bff1cf
comparison                            9789a2fb6a5573a6bdacef2702c7cff169e764f244eb1736144b9b2c8258452d
aggregate                             1b505299bc155aa32d9e48dd6d1d39327ac9025fa480472d2c67cc721270fabd
```

## 5. Still closed

R3.18E does not admit production second-property header composition, any second-property payload, a third property, a repeated/generalized property loop, K2/K3/K4 wrapper widening, actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill/runtime/export behavior, or dependency expansion.

## 6. Next pass

`R3.18F` is a separate read-only second-property-header real-replay evidence pass. It may observe only the second property header boundary through `payload_start` on the continuation lane and must not decode the payload.

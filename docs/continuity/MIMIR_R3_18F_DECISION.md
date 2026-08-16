# MIMIR R3.18F — Second-Property-Header Evidence Decision

**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE COMPLETE**
**Production SHA (unchanged):** `4adadd185783954c7fb6ad67db14b77b377cdde5`
**Evidence authority head:** `27a855a9cfb82a0294dd1601e4da01c9fdfad264`

## 1. Decision

R3.18F proves the second-property header boundary on the exact supported real-replay lane without consuming the second payload. All continuation second headers matched pinned Boxcars exactly through `payload_start`; all terminators stopped after their false one-bit control and exposed no header fields. The result admits only this evidence boundary. Production remains R3.18D until a separate implementation pass succeeds.

## 2. Exact receipts

```text
canonical continuity base             3a10ee59ba42722b59ca6c5b816205f6e5d603ea
production SHA/tree                   4adadd185783954c7fb6ad67db14b77b377cdde5 / 67b1969eaff49d2913b88b3921f27b1bd7fe8193
evidence authority head/tree          27a855a9cfb82a0294dd1601e4da01c9fdfad264 / 4058b67da82e9fbfcc078e975b26d186ec68e6f0
authority run/job                     31951039411 / 95174417526 SUCCESS
same-head normal CI                   31951039378 / 95174417478 SUCCESS
artifact                              9264673141
artifact SHA256                       e31e09abf322b6458f9034b06efe5502bb3b7f1011dfb08c9ffd6d1b1cd1b361
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## 3. Evidence result

```text
replay identity / oracle parse        47/47
R3.18E witness reconstruction         94/94
continuation rows                     47
terminator rows                       47
continuation header native success    47/47
second property_present exact         47/47 + 47/47 terminator false
second stream start/end/value exact   47/47
second stream bound/prop-bits exact   47/47
resolved property object exact        47/47
resolved attribute tag exact          47/47
second payload_start/stop exact       47/47
terminator one-bit stop exact         47/47
terminator optionals None             47/47
real header truncation negatives      32
native/oracle mismatch                0
second payload bits consumed          0
third-property bits consumed          0
privacy                               PASS
production/Cargo/fixture/corpus/
support mutation                      0/0/0/0/0
```

Continuation second-header tag distribution was Int=46 and String=1. Unresolved-stream synthetic, false-terminator no-lookup synthetic, post-stop poison and repeatability controls all passed.

## 4. Immutable artifact file hashes

```text
source scope                          492f63c3cfcb27967426816f97858c8f4ad1d9ebb6ce40719f6d829ff3f0ea55
replay identity                       b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation receipt       ba0f63ca5cd09ff48e7f70141f6cc78dacc2307502af6c1e09a9695b2ba52e97
selected witnesses                    99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7
selection summary                     bd6c4d25b02533626485e4fdb000034a39e7c2b5f559d8a09a8a4eb5e5ca80d4
comparison                            53f4a9aefbfcc3d02e5a1501d2849455052c01612ddd299e795e89ad2938ddcd
aggregate                             57c90cb3617461aea1a078a7b0f72ae301fd35fc9d7c4f9fe56de6d7633a4a04
```

## 5. Still closed

R3.18F does not admit production second-header composition by itself, any second payload, a third property, a repeated/generalized property loop, a generic chainable property cursor, K2/K3/K4 wrapper widening, actor/frame iteration, lifecycle mutation, raw-state/event extraction, replay slicing, skill/runtime/export behavior or dependency expansion.

## 6. Next pass

`R3.18G` is the minimal production admission justified by this evidence: one optional second header after a valid first primitive property, terminating at the second payload start. Its continuation header-tag allowlist is exactly Int and String. This does not admit String payload decoding; every second payload remains forbidden.

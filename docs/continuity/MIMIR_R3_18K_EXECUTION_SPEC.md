# MIMIR R3.18K — Published Second-Property Payload Real-Replay Differential Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / production differential
**Production authority:** R3.18J `330ab01890a7c09eff1805e437584fb3be0a1134`
**Production mutation:** forbidden
**Third property/control bit:** forbidden

## 1. Goal

Differentially validate the published R3.18J bounded second-payload composition over the exact frozen R3.18I lane. Invoke the production R3.18J API, not merely the lower-level scalar/K2 decoders, and prove exact class/value/end behavior without observing the following `property_present` bit.

## 2. Frozen authority

```text
production SHA/tree                 330ab01890a7c09eff1805e437584fb3be0a1134 / 5540b6a86e53d243dabbabea223a5afa8657521c
lib.rs blob                         ee9b0c71871df7ff52275581eb7ad4c023b8ba79
R3.18J focused test blob            c5a97c5a17ae2ea292790a020673dd26a0150024
implementation run/job              31975731621 / 95234808797 SUCCESS
candidate CI                        31975907582 / 95235253244 SUCCESS
published-main CI                   31976100231 / 95235742210 SUCCESS
R3.18I evidence head                45090a2c18fb517088bb411782bbaed0d7d68199
R3.18I artifact                     9270842140
R3.18I artifact digest              sha256:9890ed33780412a8900692a627b212d80428a08229f9f691d914c8def31e06e2
frozen rows                         94 = 47 terminators + 47 continuations
continuation payload tags           Int=46 / String=1
R3.18I native/oracle mismatch       0
R3.18I third-property bits          0
```

Before evidence, fetch fresh main, verify production source/test blobs and every receipt above, then reuse the exact R3.18I witnesses without reselection.

## 3. Required differential checks

For each of 47 terminators invoke R3.18J and require no second header/payload, exact control stop and no post-control lookup/decode.

For each of 47 continuations invoke R3.18J and require:

- exact first-property reconstruction;
- exact R3.18G second-header coordinates/tag/payload_start;
- exactly one typed second payload;
- exact tag distribution `Int=46 / String=1`;
- exact payload start/end/width and semantic value against immutable R3.18I evidence/oracle;
- exact returned `stop_bit == payload_end_bit`;
- zero following/third `property_present` bits consumed.

Native/authority mismatch must be zero.

## 4. Negative controls

At minimum: real payload truncation; terminator post-control lookup poison; String wrong-context rejection; tag outside `Int|String`; repeated identical invocation; and bit poison beginning at returned payload end. All must preserve the hard stop and fail closed where applicable.

## 5. Evidence artifact

Emit a privacy-safe immutable artifact with exact production receipts, frozen witness/source identities, per-row result comparison without raw private payload windows, aggregate counts, negative controls, third-bit consumption counter, mutation counters and hashes of every evidence file.

## 6. Required validation

Production focused tests, full `mimir-replay`, workspace check/test/clippy, repository verifier, same-head normal CI, deterministic double run, privacy scan and production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 7. Hard stop

No production Rust/Cargo/fixture/corpus/support mutation. Do not inspect or semantically claim the bit after the second payload. No third property, repeated loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening.

## 8. Outcome gate

### Outcome A
All 94 frozen rows match the published R3.18J API exactly with zero mismatch and zero following-property bits consumed. Admit R3.18K evidence, then define a separate evidence pass for exactly the next `property_present` control bit.

### Outcome B
A reproducible production/authority mismatch appears. Record it and keep the post-second-payload control boundary closed.

### Outcome C
Authority drift, witness reselection, source mutation, privacy failure, following-bit access or validation contradiction. Stop without admission.

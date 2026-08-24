# MIMIR R3.18AP — Next Property-Control Bit Evidence After Published R3.18AN Payload Decision

**Date:** 2026-08-24
**Outcome:** **A — ADMITTED / ONE-BIT DISTRIBUTION EXACT**
**Production mutation:** none
**Canonical production:** `3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38` / `3efcc244bca55623b12bb21eb277753fc61144d4`

## Decision

R3.18AP closes Outcome A. On exactly the immutable 47-row R3.18AO lane, published R3.18AN reconstructed through its exact payload end on all rows and one following `property_present` bit was observed at that exact stop. Pinned Boxcars and an independent standalone native LSB-first probe matched 47/47. The observed distribution is **false=7 / true=40**.

This is the first material semantic difference from the recent M/W/AG true-only one-bit boundaries: false is genuinely observed here. R3.18AQ therefore must represent both booleans successfully and may not reject false by analogy.

## Exact authority

```text
canonical main before admission     c55c23c0fa86de6bacb79456795dafd996d2d96f / 26ba2777045299c99546a4777fc884048157dd60
production SHA/tree                 3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38 / 3efcc244bca55623b12bb21eb277753fc61144d4
evidence head/tree                  736ac33c099a9183693bfcb2b5f5b74704a8808e / 840011b603b5bb330e018bd060650cfb3af29b73
authority run/job                   32745234196/97489066582 SUCCESS
same-head natural CI                32745233671/97489738567 SUCCESS / count=1 / rerun=0
artifact                            9526988237 / 9692 bytes
artifact ZIP SHA-256                sha256:b50b01bd87c0b61ca2e407abe43ac5db9fb15290f7cd3e908332d2ac2a26c4cc
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
```

Downloaded ZIP SHA-256 equals the GitHub artifact digest. The artifact manifest contains ten evidence payload entries and all ten verify.

## Admitted evidence

```text
frozen rows                         47/47
published R3.18AN exact             47/47
oracle-native exact                 47/47
control false                       7
control true                        40
mismatch                            0
witness reselection                 0
next stream/header/payload/control  0/0/0/0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                             PASS
```

Artifact payload SHA-256 includes aggregate `72bb9b46532174906d622312da84208c258ae1fd8d14e2aab738cca57d23e926`, comparison `6ddf53ed8ce3fd75ac15d3f3c79337e1373583b66d3a0485c1f084738d69b721`, summary `97e5589de217f32c50079239eb0bd33ae998515f3e1942d0838bfa464de106e9`, negatives `79bed38a73ade4809f4c54433236376fa756698eacbb12a430a6adfd7b90f699`, validation `c112a8ce0cdb536b2fcde16a2b7987a29524d8f30f0d256f26b4f01e4a8facdb`, source scope `1b0acd7c9d1ade9b2b822e0b7f2608c480c0824a105f8c4b6e47d86dd72c28f7`, upstream receipts `4be30119f4a8638b81f3fad5ebbe9727b1a9667ca0ce23fc3ef64987b0e9cbcc`, same-head CI receipt `9d2afc376b6bcce96f593b287e7f1b9b0c035fdc7c2a92d88815210044cbaa0d` and manifest `6f184c0df4ea9bb00c91cf1959f9184e1090c139a5fe106c437b64cc23b1d715`.

## Hard stop

R3.18AP admits only the value of one control bit. It does not admit a next stream ID, header, payload, second later control, repeated/generalized loop/cursor, actor/frame/lifecycle advance or raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18AQ is a separate production pass. It may validate/recompute exactly one published R3.18AN prior, consume exactly one AP-admitted control bit, expose both false and true outcomes, and stop one bit later.

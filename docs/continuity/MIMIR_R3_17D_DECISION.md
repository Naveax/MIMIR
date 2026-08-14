# MIMIR — R3.17D Differential Decision

**Date:** 2026-08-14
**Pass:** `R3.17D — primitive scalar native differential`
**Outcome:** **A — ADMITTED / 96 OF 96 EXACT**
**Pass kind:** evidence-only differential
**Production Rust changed:** **NO**

## Frozen authorities

```text
canonical production SHA     c3d4c73ca34febb9f0383c59132a8bc8a363b06b
production source blob       54e1bfb918ec1bd42a61cfa0131ca27412082ac5
R3.17D evidence head         e8f1522fb6289368bbd254d2f839091452377e9e
R3.17D authority run/job     31798478106 / 94760722134 SUCCESS
exact-head normal CI         31798478071 / 94760722233 SUCCESS
artifact                     9218372907
artifact SHA-256             db049fbfd8514bb1cd661ab6b73ddf517d9786e961d764e62bc4e6137ce83e6f
identity TSV SHA-256         b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
witness JSONL SHA-256        b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
witness TSV SHA-256          ee7f1baaa7696056172e28da2fed0848975ff1d2440113bb4d242f49d0b9da6e
comparison TSV SHA-256       f10fa74e2975e1d13c8f23c5a570409667b0c4057428439a414b47f8aaa39f73
aggregate SHA-256            fcc1d93ff55f3cee89211fc77a2842adca33f32f94705390610edf749df1540d
receipt file SHA-256         c86e904254c6ce5a1eeeff03df9f9961ffd9169fce391d34849b54ddfccbe268
immutable receipt stream     PASS
```

## Result

The current native R3.17C one-scalar decoder was run at the exact replay/network bit positions of all 96 immutable R3.17A witnesses. Result:

```text
witness rows                 96
native decode success        96
exact match                  96/96
mismatch count               0
native error count           0
identity error count         0
unsupported tag count        0
production mutation count    0
Cargo mutation count         0
corpus mutation count        0
```

Exact equality covered tag, payload start/end, consumed width, stop bit and scalar value. Float rows additionally required raw `u32` equality and identical `f32::to_bits()` identity.

The first evidence attempt already achieved 96/96 but failed only repository `cargo fmt --check` on the temporary harness. The final authority head changed only evidence-harness formatting and then passed the full repository verifier plus normal CI. No witness or production semantics were changed.

## Decision

R3.17 K1 primitive scalar wave is closed: evidence, contract, production implementation and frozen native differential have all passed. This does **not** authorize property-loop continuation or another attribute family by analogy.

The execution roadmap orders the next wave as K2 object/reference/text. Therefore the next exact pass is evidence-only `R3.17E`.

# MIMIR — R3.17A Decision

**Date:** 2026-08-14
**Outcome:** `A — primitive scalar wire evidence exact / admitted`
**Production source changed:** `NO`
**Production code checkpoint remains:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`

## Decision

The primitive scalar evidence pass is admitted. All six candidate scalar tags were observed in the exact supported 47-replay lane, and every observed payload consumed one fixed width matching the pinned Boxcars source behavior.

R3.17A is evidence only. It does not grant MIMIR a native scalar payload decoder.

## Frozen authority

```text
canonical evidence base    ded95e8ae512876b46453585be05b8358025314a
evidence head              4cd21ea6db14c9becc11c17149af9201071859bc
workflow run/job           31792028292 / 94740870175 SUCCESS
exact-head normal CI       31792028275 / 94740869974 SUCCESS
artifact id                9216016802
artifact size              51,639,177 bytes
artifact SHA-256           59fe6d40b15bd3267e776abff48ef96c138314ca514b5e0d44c003b1edf117af
oracle                     nickbabcock/boxcars @ c70e77df7af81b436cb545d070bb90c82f562d0b
frame_decoder.rs blob      6f2ff153d3a27cdacccc65e3f23851489077a7d8
attributes.rs blob         5e2d5bc1cd8187af30c3ea95193ad987645cb76e
selector SHA-256           2ecbeea804f193796a539baee1e968719f03c0cd706efff0c22a61e6ef943dae
replay identity SHA-256    b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
replay identity rows       47
bounded witness rows       96
receipt stream             PASS
```

## Aggregate result

```text
oracle decode success      47 / 47
scalar occurrences         2,141,139
Boolean                    84,545 / 47 replays / 1 bit
Byte                       1,730,595 / 47 replays / 8 bits
Enum                       180,624 / 47 replays / 11 bits
Float                      33,857 / 47 replays / 32 bits
Int                        109,920 / 47 replays / 32 bits
Int64                      1,598 / 14 replays / 64 bits
shape mismatches           0
bit monotonicity failures  0
unexpected tag shapes      0
production mutations       0
Cargo mutations            0
corpus mutations           0
```

## Durable content hashes

```text
instrumentation patch      f10fc6206aaba14b8afd368c5ede8d8ce6bc1e4a7a56049be9d7012aa8b82877
full scalar oracle         af5c72982501bedb4a6283a0aca473b3620682ad797267aa625c37cce9a515a1
96 witnesses               b2e8800e55fd3760f77b7ac880aa2147f93d0aa00f65a0911cdbb89415ac68d9
summary                    a2f8a7c8efb87083986bb635d9c2c81e992556bbe9a41263d7bfd453c404ce2c
aggregate                  b5cf40d45a2f9f4bd6914b99117ec252d72afb5d955a0999770faf1f2764b34e
```

The job log permanently contains the bounded receipt stream. The one-day artifact is supplemental, not the only evidence carrier.

## Interpretation limits

- Fixed widths are admitted only for the six scalar tags above.
- Float exact identity is the raw 32-bit pattern; decimal rendering is not an exact comparison authority.
- `Int` and `Int64` signed interpretation is supported by the pinned oracle source contract; the supported replay witnesses do not need to contain every signed-domain edge case.
- `Enum` is admitted as an 11-bit numeric wire value, not as a semantic enum-name registry.
- No claim is made that compound/spatial tag families share these layouts.

## Next exact pass

`R3.17B — primitive scalar attribute contract admission`.

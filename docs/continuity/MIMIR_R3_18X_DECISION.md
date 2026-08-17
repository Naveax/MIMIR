# MIMIR R3.18X — Published R3.18W Control Differential Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / READ-ONLY PUBLISHED DIFFERENTIAL**
**Production mutation:** none
**Production remains:** `58872e94f00ef094807f21ab2ff984ac66b97d91` / `d6965d77903ea99dad0465bb350b6a673ee7dd00`

## Decision

R3.18X is admitted Outcome A. On exactly the immutable 47 R3.18V witnesses, the published R3.18W API reproduced the frozen one-bit control boundary exactly. All rows reconstructed the published R3.18T prior through its payload-end stop, then returned the same R3.18V control start/value/end/stop. The observed immutable distribution remains `false=0 / true=47`.

No next stream, next header, next payload or second later control bit was consumed. Production Rust remained unchanged.

## Exact authority

```text
canonical main during evidence       76abc44458e546e5a2dd6a19286bcc09cd69853d / ad532a2dfe14a9be16d1292ee70ac1a60015971c
production SHA/tree                  58872e94f00ef094807f21ab2ff984ac66b97d91 / d6965d77903ea99dad0465bb350b6a673ee7dd00
production lib/W-test blobs          d997ae8c3ad2d201b3f43c6ccca7ded2ef03b73b / ac176135c2e6ed56f0b91bdde8c7548f17641cf0
evidence head/tree                   75259a9b3705b16b21d89b975ee584a7765e8134 / fe90b38c98039cd1dde05b96613645d0ab69a8a9
authority run/job                    32065498170 / 95496521378 SUCCESS
same-head normal CI                  32065498109 / 95496518762 SUCCESS
artifact                             9299790869 / 19761 bytes / sha256:ac32daa92d88f1753da34123d074dcd8f3c98c58fdeb0b91f89cb837ea02ebff
admission authority                  32066091573 / 95498450308
```

The artifact ZIP SHA-256 equals its GitHub Actions digest. Its internal manifest contains 8 payload hashes and all 8 verify exactly.

## Proven aggregate

```text
frozen rows                          47/47
published R3.18T exact               47/47
published W vs frozen V mismatch     0
control distribution                 false=0 / true=47
repeatability                        47/47 PASS
control truncation                   47/47 PASS
false-control rejection              47/47 PASS
prior-boundary rejection             47/47 PASS
post-stop poison                     47/47 PASS
next stream/header/payload/2nd ctrl  0/0/0/0
witness reselection                  0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                              PASS
```

## Scope consequence

R3.18X does **not** admit a next property header. It only validates the already-published W one-bit composition. The next boundary is therefore a separate read-only pass, R3.18Y, beginning exactly at `R3.18W.stop_bit` and stopping at one following header's `payload_start`.

## Hard stop

False success semantics, next payload, another control, generalized property cursor/loop, next actor/frame/lifecycle behavior, raw state/events, replay slicing, skill mining, counterfactual execution and runtime/export widening remain closed.

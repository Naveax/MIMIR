# MIMIR — R3.18C Decision

**Date:** 2026-08-16
**Pass:** `R3.18C — existing-actor property-loop terminator / continuation evidence`
**Outcome:** **A — ADMITTED / EVIDENCE COMPLETE**
**Production mutation:** none
**Second property decode:** none

## Decision

R3.18C proves the first loop-control edge after the published R3.18B one-property K1 composition. Across the frozen 47-replay lane, the pinned Boxcars oracle produced both required witness classes: 47 terminator candidates and 47 continuation candidates. For the selected real witnesses, the native R3.18B `stop_bit` is exactly the oracle's next `property_present` start, and an evidence-only native reader consumes exactly that one bit and stops immediately after it.

This evidence does not admit a production property loop or a second property stream/header/payload.

## Frozen authority

```text
canonical evidence base main/tree  f8f6467f2ee652892329f08a3e532b1e1f834fb3 / 9943ee5620091142379763422dc22178b2278fbc
production SHA/tree                 de7a2ba40663bb619ca7bd8654846ce87670d023 / d1889038ca2eaeb8bb0f05e44b811d906f84cf6e
authority head                      a4b71ad43e5cf55c44c9518b24622ce29214acd2
authority run/job                   31944102614 / 95157425239 SUCCESS
same-head normal CI                 31944102575 / 95157425128 SUCCESS
artifact                            9262820284
artifact digest                     sha256:95e89cb350cc4c274d2b7a53198d78941bef54ff1b3f6a165b2ba9710659ec07
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
replay identity/oracle              47/47
candidate rows                      94
terminator / continuation           47 / 47
```

## Selected terminator witness

```text
replay                              external_fixtures/sample_001.replay
frame / actor ordinal / actor id    0 / 115 / 60
actor context object                344
property object / tag               18 / Float
semantic raw bits                   1092616192
property_present                    [36587,36588)
stream id / bound / bits            17 / 25 / 4
stream range                        [36588,36593)
payload                             [36593,36625) / 32 bits
payload SHA256                      b4f510e22e0831cf02a9151cb6c11149fcb7d1c6570487ebcddc93970ac58583
next property_present               false / [36625,36626)
loop-bit SHA256                     d189517f7ee56ad154263623d4ec3a8923a28692cd165600e93ee88672cd8145
native stop                         36625
one-bit evidence stop               36626
```

## Selected continuation witness

```text
replay                              external_fixtures/sample_001.replay
frame / actor ordinal / actor id    0 / 63 / 2
actor context object                98
property object / tag / value       55 / Int / 62
property_present                    [10227,10228)
stream id / bound / bits            27 / 67 / 6
stream range                        [10228,10234)
payload                             [10234,10266) / 32 bits
payload SHA256                      d2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f
next property_present               true / [10266,10267)
loop-bit SHA256                     e3d693ad5e420d2bd7828df2e5f18f38ec0a3f5660ac09414cea2fa06fd850c0
native stop                         10266
one-bit evidence stop               10267
```

## Gate results

```text
native stop == oracle next start    PASS / both classes
next property bit exact             PASS / both classes
one-bit stop exact                  PASS / both classes
truncation negative                 PASS / cursor unchanged
post-stop poison                    PASS
native repeatability                PASS
R3.18B focused regression           8/8 PASS
second stream bits consumed         0
second payload bits consumed        0
native/oracle mismatch              0
privacy                             PASS
prod/Cargo/fixture/corpus/support   0/0/0/0/0 mutation
```

Receipt SHA-256 values:

```text
source scope                        c4fdd423cbfd1672b96b748206440ddce7a47219fca3bb21fcb226fdfb9525e4
replay identity                     b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
Boxcars instrumentation receipt     482ed1ddc230e0ae7b482e8e964663a831cce00a0a6480fc69a052ddd8cb5b7d
selected witnesses                  321c3ba2f7ded131ddafc2449f9aa784bd9c798294754bef4cbee2d3c6cedda5
selection summary                   f4a9a12cfba9ba1850893d3421d141a25f462c53abbd36ae28ea152eafa86b3f
comparison                          b50ae6e09dd42450757c5a1e67646de638817007a67f8ef9a5c10dcb3129b2f0
aggregate                           a75bd832617fff9ed2bb450af78bec59efaee9e22f844534d514fee31b8e3d28
```

## Next exact pass

`R3.18D — minimal native existing-actor next-property control bit`.

R3.18D may publish only the single proven bit after one valid R3.18B K1 property result. It may not decode a second stream/header/payload, repeat the control operation as a property loop, or widen K2/K3/K4 composition.

# MIMIR — R3.16B Decision

**Date:** 2026-08-14
**Outcome:** `A — implementation exact / admitted to production`
**Production SHA:** `ebc0fa31ba90a8496c3d1719e436d2c17b605ff7`

## Decision

The narrow native existing-actor first-property header implementation is admitted. It consumes one `property_present` decision and, when present, one canonical bounded `stream_id`, resolves the existing static/inherited property context, records the exact payload boundary, and stops before consuming attribute payload bits.

## Frozen closure evidence

```text
base main                              fc020729396ad9f62ee4b8fd8fe6808f5bdb5489
disposable implementation authority    d843906a33321a3bde06a44e7187e92dd0c1d436
disposable verifier/differential       31787682424 / 94727174844 SUCCESS
clean production SHA                   ebc0fa31ba90a8496c3d1719e436d2c17b605ff7
source Git blob                        625ab2322e35f5f835871d42b9efeb04f5c299ab
source SHA-256                         186eb5c2d25a42c6028e4149adbb8fa5ac2807c4f1d187ab389ce565a7a5db28
focused test Git blob                  0fea53e1758e7b0b5f8d2a14b98cbce5feb400c2
focused tests                          8/8 PASS
immutable R3.16A rows                  47
native differential                    47/47 PASS
clean diff                             exactly 2 files, +331/-0
candidate CI                           31788230442 / 94728918384 SUCCESS
candidate Knowledge Archive            31788291777 / 94729116078 SUCCESS
published-main CI                      31788526050 / 94729854512 SUCCESS
published-main Knowledge Archive       31788566184 / 94729983908 SUCCESS
publication                            force=false fast-forward
```

## Scope audit

Canonical production changed only:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_16b_property_header.rs`

No Cargo manifest/lockfile, replay fixture/corpus, workflow, evidence tool, export crate, runtime, teacher, skill, or training surface entered the production commit.

## Hard stop preserved

No attribute payload bit is consumed. No second property, property loop, next actor/frame, lifecycle mutation, raw-state/event/skill/runtime/export capability is admitted.

## Next exact pass

`R3.16C — implementation continuity/check`.

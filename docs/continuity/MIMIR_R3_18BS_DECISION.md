# MIMIR R3.18BS — Bounded Post-BO One-Following-Payload Production Decision

**Date:** 2026-09-11
**Outcome:** **A — ADMITTED / PUBLISHED**
**Canonical production:** `5ab14575d0a698d752db35db76f3dbb300cdec8d` / `1c0b4c0a50385a34ba730a52a98a89423ff56869`
**Parent:** `2f4f536d52a10a28a66bcc7b9b9dc84f7e29b2a6` / `49df3c7cdb8dc36c0190cba51dc5a802f6fde3d2`
**Header contract:** R3.18BN `sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`
**Payload evidence authority:** R3.18BQ `16c43f38e740c57ae9cb90c92084002ec83815e7` / artifact `10144392560` / `sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c`

## Decision

R3.18BS publishes exactly one boundary-specific payload after a valid R3.18BO true following-header composition. The admitted lane is exactly the two immutable R3.18BQ payload witnesses: Boolean `[11238,11239)` width1/value=true and ActiveActor `[3205,3238)` width33/active=true/actor=1. The R3.18BP false terminator remains outside the payload lane.

The implementation recomputes published BO authority, requires the validated payload-start boundary, uses the already-admitted Boolean scalar or ActiveActor K2 primitive, returns exact payload boundary/value information and stops exactly at payload end. The R3.18BR-observed next control bit is not consumed.

## Exact authority and receipts

```text
production SHA/tree                  5ab14575d0a698d752db35db76f3dbb300cdec8d / 1c0b4c0a50385a34ba730a52a98a89423ff56869
parent SHA/tree                      2f4f536d52a10a28a66bcc7b9b9dc84f7e29b2a6 / 49df3c7cdb8dc36c0190cba51dc5a802f6fde3d2
lib/test blobs                       3428608283d6d0022d466671f90afc9304726dd0 / 706bbdee62a09f04af7bcf70e22567793084d0d6
BS execution spec blob               77818f7113a357b2577948e6700bfaf63de27db9
production builder head              40009f866344778be8b5e5d4c4577cf292bb1189
production builder run/job           34617577982/103323236248 SUCCESS
validation-only PR                   #218 CLOSED UNMERGED
exact-head candidate CI              34617945689/103324450173 SUCCESS
published-main CI                    34618640843/103326748345 SUCCESS
BN contract                          sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
BQ evidence head/artifact            16c43f38e740c57ae9cb90c92084002ec83815e7 / 10144392560
BQ artifact digest                   sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c
BR evidence head/artifact            ff1daab35e2e75bf7446a98a07a1db67e5196dbd / 10267123608
BR artifact digest                   sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Admitted production behavior

```text
BQ payload rows                      2/2
BP false terminator                  excluded before payload decode
Boolean                              [11238,11239) / width 1 / value true
ActiveActor                          [3205,3238) / width 33 / active true / actor 1
property ordinal                     7 on 2/2
final stop                           exact payload_end_bit
following BR control consumed        0
next stream/header/payload           0/0/0
second later control                 0
generalized/repeated cursor          0
```

The clean production commit contains only `crates/mimir-replay/src/lib.rs` and `crates/mimir-replay/tests/r3_18bs_post_bo_payload.rs`. No temporary workflow/helper, Cargo/dependency, fixture/corpus, continuity, raw-state/event/skill/runtime/export or unrelated mutation entered production.

## Validation

The final builder passed formatting, the focused BS integration suite 32/32, `cargo check -p mimir-replay --all-targets --all-features`, Clippy with warnings denied, exact two-file scope and clean reconstruction. Validation-only PR #218 supplied natural exact-head repository CI and was closed unmerged. Fresh-main ancestry was rechecked before publication; `main` was advanced with `force=false`; exact SHA/tree readback matched; published-main CI passed on the exact production SHA.

## Hard stop

No R3.18BR control-bit production, no payload access on the BP false terminator, no next stream/header/payload, no second later control, no generalized/repeated property loop/cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Next gate

R3.18BT is a separate read-only published-production differential. It must validate published R3.18BS against exactly the immutable two-row BQ payload authority, preserve BP-false exclusion, require exact payload identity/boundaries and consume zero BR control bits.

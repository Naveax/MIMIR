# MIMIR — R3.15C Production Decision

**Date:** 2026-08-13  
**Pass:** `R3.15C — first NewActor native reader through spawn trajectory`  
**Outcome:** **ADMITTED / PRODUCTION**

## Exact identity

```text
pre-pass main SHA      = 77395d40af97620c58b39427a351b23aede84482
production SHA         = bf4bccff82203ed049d33e942681fed07f23beb4
production tree        = 62cc2a970704cbf0d6545a02a45a8b1ef46c5c99
source file            = crates/mimir-replay/src/lib.rs
source Git blob        = f64a5e0d66962f41026b2eb10e176219d4529931
builder run / job      = 31714929500 / 94497112417
clean exact-SHA CI     = 31715088860
published-main CI      = 31715564598
```

The clean production commit is exactly one commit ahead of R3.15B and changes exactly one production file. Cargo files, dependencies, fixtures and corpus are unchanged.

## Admitted capability

R3.15C adds an independent additive first-NewActor reader while preserving the existing R3.14D first-envelope result. Absent/dead/not-new branches do not consume NewActor payload. A new branch consumes raw signed 32-bit name ID, one opaque bit, raw signed 32-bit object ID, dispatches only through the existing static spawn table, and decodes `None`, `Location`, or `LocationAndRotation` to the exact trajectory endpoint. Vector and rotation composites are cursor-atomic; negative/out-of-range object IDs fail closed.

Focused R3.15C tests, crate check and clippy passed in the builder lane; the clean candidate then passed the normal repository verifier on exact SHA before force-free publication. Published `main` readback matched the production SHA. Continuity publication additionally requires the published-main run above to be green.

## Still closed

`property_present`, stream/property IDs, attributes, next actor/frame, lifecycle mutation, raw state, events and skills remain closed.

## Next exact pass

`R3.15D — 47-replay first-NewActor native-vs-pinned-Boxcars differential audit`, evidence-only.

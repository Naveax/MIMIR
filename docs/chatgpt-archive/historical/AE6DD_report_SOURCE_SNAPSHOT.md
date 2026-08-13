# SOURCE SNAPSHOT — AE6DD..._v0_2.report.md

**Source class:** CURATED_SOURCE_SNAPSHOT
**Original:** `AE6DD28411F1508AD67AA6A178296A08_v0_2.report.md`
**Recorded size:** 8,581 bytes.

The historical report explicitly states:
- V0.2 is header/footer based;
- it extracts scoreboard, goals/highlights/tickmarks/keyframes/name tables;
- it does not decode true car/ball coordinates, boost, inputs, dodge/jump, aerial path or exact time-to-ball;
- exact tactical error explanation requires network stream decode.

The report's stated V1 requirements included:
- boxcars/rrrocket-style network stream parsing;
- per-event state windows;
- ball rigid body position/velocity/angular velocity;
- car rigid bodies including rotation and boost;
- touch sequence/last touch;
- jump/dodge/double-jump state when available;
- nearest-player ETA;
- goal angle, shot speed, approach angle and recovery time.

This document is highly relevant because those historical requirements map directly into the modern MIMIR native replay/raw-state roadmap.

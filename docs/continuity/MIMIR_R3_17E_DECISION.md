# MIMIR R3.17E — K2 Wire Evidence Decision

**Decision:** Outcome A — ADMITTED / COMPLETE
**Date:** 2026-08-14
**Production capability change:** none

## Authority

- Base main: `cfe4882f99dbce5e8148e476c177a0586b1e7986`
- Production SHA/blob: `c3d4c73ca34febb9f0383c59132a8bc8a363b06b` / `54e1bfb918ec1bd42a61cfa0131ca27412082ac5`
- Evidence head: `19db534a3668f84f1c5ce36ef1252c52841d890f`
- Authority run/job: `31801482588 / 94770260529` SUCCESS
- Exact-head normal CI: `31801482499 / 94770260054` SUCCESS
- Artifact: `9219554878`
- Artifact digest: `sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc`

## Results

47/47 replays parsed. Complete K2 scan: 110,539 occurrences: ActiveActor 86,200; String 14,670; QWordString 2,920; UniqueId 6,443; PartyLeader 306. Shape/unclassified, bit-monotonicity and raw-payload-shape failures are all zero. Privacy-safe output passed. Production/Cargo/corpus mutation is 0/0/0.

Observed authority surface: ActiveActor33; String Empty/Windows1252/UTF16; QWordString legacy QWord64 and RL223 Windows1252; UniqueId Steam/PlayStation/PsyNet/Epic; PartyLeader only Some(Epic, Windows1252 declared=33). Unseen variants are not admitted by inference.

## Immutable hashes

```text
aggregate          335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751
summary            9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e
oracle JSONL       196f4e4d2a588137ad12372cb2f0af79d7fca422c0bc2c5dea95506fa72cac4d
witness JSONL      7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
receipt manifest   400aa0b52a5e120b7791e34e9a364d4e40a2362c46d6770dad3c5292db8dc7cc
replay identity    b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf
```

R3.17F is opened as contract-only. Production remains at R3.17C until a separate implementation pass is admitted.

# SOURCE SNAPSHOT — MIMIR + Gabriel + V1 Full Architecture

**Source class:** CURATED_SOURCE_SNAPSHOT
**Original:** `MIMIR_Gabriel_V1_Tam_Mimari_ve_Yol_Haritasi.md`

Key ecosystem rules:
- MIMIR must stay independent from individual learners/bots;
- replay/live/self-play can feed MIMIR;
- BC, DAgger, PPO, SAC and runtime are consumers/adapters;
- replay may generate state extraction, event extraction, mistake mining, skill mining, teacher labels, counterfactuals, anti-targets, curriculum and validation scenarios;
- policy rollouts return to MIMIR for further mining;
- Gabriel and V1 form complementary diversity/exploitation pressure;
- exploit libraries and anti-exploit training are valid long-term consumers of MIMIR evidence.

Any old implementation status in the original is historical, not current.

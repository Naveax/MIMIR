# MIMIR — R3.17O Direct Native K4 Decoder Implementation Decision

**Date:** 2026-08-15
**Pass:** `R3.17O — direct native exact-contract K4 decoder implementation`
**Outcome:** **A — ADMITTED / PRODUCTION**
**Production Rust changed:** **YES, exact four-file admitted scope**

## Frozen authority

```text
pre-O canonical main         3392c28ba8ec7d72766303646c0ceb57ed1e5a19
R3.17N allowlist SHA256      80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
production SHA               492cc8218be7abc6db8f75acaea33d009ab2f175
production tree              a66c47d7fb58da508188e64d42141987a0021a07
production parent            3392c28ba8ec7d72766303646c0ceb57ed1e5a19
lib.rs blob                  0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8
k4 groups module blob        103503e25bc5af48381df021ab58133694fcece6
k4 native module blob        a9c41f3bb11343165183ac9c815ab8fdf085936c
focused test blob            70437244bb49224281ee3a2e745e7b8a4b7a093a
authority head               900d7eb122f10126558f13ea2c185cdb8c69fe1b
authority run/job            31885987240 / 95015252318 SUCCESS
exact-candidate CI           31886194387 / 95015736899 SUCCESS
published-main CI            31886353485 / 95016105618 SUCCESS
```

The earlier disposable runs `31885789107 / 95014781583` and `31885905139 / 95015053496` are **not authority**. The first stopped before Rust because temporary generation tooling incorrectly assumed tuple-sorted contract rows. The second stopped before Rust because the independent equality checker compared the evidence-only `occurrences` field. Neither changed the K4 contract. The authoritative third run repeated every substantive gate from scratch.

## Exact admitted production scope

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/src/k4_admitted_groups.rs
crates/mimir-replay/src/k4_native.rs
crates/mimir-replay/tests/r3_17o_k4_attribute_decoder.rs
```

No Cargo manifest/lockfile, fixture, replay corpus, support lane, workflow or temporary generator entered the clean production commit.

## Implemented surface

R3.17O adds a K4-specific one-value API while preserving the earlier K1/K2/K3 APIs. The public surface includes `ReplayNetworkK4DecodeContextV1`, K4 loadout/reservation/actor/product semantic structures, `ReplayNetworkK4ValueV1`, `ReplayNetworkK4DecodeV1`, `R3_17N_K4_ADMITTED_GROUPS_V1`, and `decode_replay_network_k4_v1`.

The decoder covers exactly these 11 contract families: `CamSettings`, `TeamPaint`, `TeamLoadout`, `ClubColors`, `Reservation`, `StatEvent`, `PlayerHistoryKey`, `DemolishFx`, `DemolishExtended`, `ExtendedExplosion`, and `LoadoutsOnline`. `LoadoutsOnline` accepts the caller-resolved replay object table to resolve product-attribute object IDs; it does not create a second lookup authority.

## Contract preservation

The production allowlist was generated from the canonical R3.17N JSONL and independently read back before tests:

```text
canonical contract rows      161
production allowlist rows    161
missing                       0
extra                         0
cross-product widening        0
allowlist equality            161/161 PASS
allowlist SHA256              80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
```

Acceptance is exact tuple membership over tag, replay version 868.32, net10, RL223 context, payload width and structural shape. Reservation, demolition-vector and nested online-loadout branches are not widened by taking independent field unions.

## Validation result

The focused integration suite materialized a valid synthetic payload for every admitted row and checked exact tag, shape, width, end bit and repeatability. Negatives cover wrong context/tag/start, truncation, malformed reservation text, unobserved TeamLoadout version, demolition cross-products, LoadoutsOnline unknown/cross-product branches, and RL223 tuple mismatch.

```text
161 synthetic positives            PASS
independent allowlist equality      PASS
cross-product widening              0
focused negative controls           PASS
full mimir-replay suite             PASS
workspace check/test/clippy         PASS
full repository verifier            PASS
exact candidate CI                  PASS
published-main CI                   PASS
```

## Capability consequence

Production may now decode **one** already-resolved R3.17N-admitted K4 value in addition to previously admitted K1/K2/K3 one-value surfaces. Success stops exactly at that payload end. This does not admit a second property, property-loop continuation, next actor/frame, actor lifecycle mutation, raw-state extraction, event extraction, replay slicing, skill synthesis, runtime integration or export widening.

Synthetic contract success is not the final K4 oracle certification. R3.17P must compare the published native decoder against regenerated real-replay witnesses for all 161 exact groups before later parser widening is considered.

## Next exact pass

Open `R3.17P — native K4 real-replay differential audit against regenerated R3.17M witnesses`.

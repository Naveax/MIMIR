# MIMIR — MASTER EXECUTION CHECKLIST, CONTINUITY HANDBOOK & BUILD MANUAL

> **THIS IS THE SINGLE REQUIRED CONTINUITY FILE FOR MIMIR.**
>
> A future ChatGPT/Codex/agent session must be able to know nothing about MIMIR, read only this file, inspect fresh repository truth, and continue correctly until the project is finished.
>
> Other files under `docs/continuity/`, historical `docs/`, executor artifacts and old chat summaries are useful evidence and design history, but they are **not required to understand how to continue**. If this file conflicts with fresh source/tests, source/tests win and this file must be repaired before capability widening.

---

# 0. EXECUTIVE DIRECTIVE FOR A COMPLETELY NEW CHAT

If you are a new session and know absolutely nothing about MIMIR, do this before writing code:

```text
1. Connect to GitHub repository Naveax/MIMIR.
2. Fetch fresh origin/main and record the exact SHA.
3. Read this entire file, not only the current-pass section.
4. Compare fresh main against LAST_PRODUCTION_CODE_SHA below.
5. Inspect all commits after LAST_PRODUCTION_CODE_SHA and classify them:
   a. production source change,
   b. continuity/docs-only,
   c. temporary/evidence-only.
6. If production source is newer than this file says, STOP capability widening.
   Reconstruct current truth from code/tests/CI and update this file first.
7. Inspect the source and tests directly related to CURRENT_PASS.
8. Inspect any in-flight branch recorded below.
9. Continue from the first unchecked item in CURRENT PASS CHECKLIST.
10. Do not reopen completed milestones without a concrete regression or contradiction.
11. Do not skip future phases because they look obvious.
12. After a pass is truly admitted/published, update THIS SAME FILE so the next chat can continue.
```

If the user only says **“devam et”**, do not ask them where MIMIR was. The answer is in this file plus fresh GitHub truth.

---

# 1. CANONICAL CURRENT STATE BLOCK

This block must be updated after every admitted evidence milestone or published production milestone.

```text
REPOSITORY: Naveax/MIMIR
DEFAULT_BRANCH: main
LANGUAGE: Rust 2024 workspace
RUST_VERSION_FLOOR: 1.85

LAST_PRODUCTION_CODE_SHA:
  492cc8218be7abc6db8f75acaea33d009ab2f175

LAST_PRODUCTION_MILESTONE:
  R3.17O — direct native exact-contract K4 decoder implementation

LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.17P — native K4 differential audit / Outcome A / 161 of 161 real-replay exact groups / 0 mismatch

LAST_COMPLETED_CONTRACT_PASS:
  R3.17N — evidence-supported K4 gameplay-structured contract / Outcome A / 161 exact groups / zero cross-product widening

LAST_COMPLETED_EVIDENCE_PASS:
  R3.18A — existing-actor single-property boundary evidence / Outcome A / one real Int property / exact end cursor / 0 next-property bits

CURRENT_PASS:
  R3.18B — minimal native existing-actor single-property K1 composition

CURRENT_PASS_TYPE:
  production implementation / first property-present header + exactly one K1 primitive scalar payload

CURRENT_SUPPORTED_REPLAY_LANE:
  47 replays

CHECKED_IN_REPLAY_SET:
  103 total = 3 historical fixtures + largest_100 stress corpus

PINNED_BOXCARS_ORACLE:
  repository: nickbabcock/boxcars
  exact SHA: c70e77df7af81b436cb545d070bb90c82f562d0b

CURRENT_PRODUCTION_HARD_STOP:
  one already-resolved K1 primitive scalar OR one R3.17F-admitted K2 payload OR one R3.17J-admitted K3 payload OR one R3.17N-admitted K4 payload may be decoded natively
  K3 remains limited to its exact R3.17J structural/context allowlist; K4 remains limited to the exact 161 R3.17N tuples
  stop exactly at payload_end_bit / stop_bit after that one value
  R3.17P certified the published R3.17O K4 decoder on all 161 exact real-replay groups; R3.18A then proved one real existing-actor property header + Int payload through the exact end cursor with 0 next-property bits consumed
  R3.18B may compose only the existing first-property header with the already-admitted K1 primitive scalar decoder; K2/K3/K4 composition and every property loop remain closed
  NO second property, next actor, next frame, lifecycle mutation, unobserved shape/family, or extra context inference is admitted

R3_17E_EVIDENCE_CLOSURE:
  evidence head: 19db534a3668f84f1c5ce36ef1252c52841d890f
  authority run/job: 31801482588 / 94770260529 SUCCESS
  exact-head normal CI: 31801482499 / 94770260054 SUCCESS
  artifact: 9219554878
  artifact digest: sha256:210a9138e7027672b27c2e557741625abba2af4836286ea2e4aa722fa613a0cc
  47/47 oracle decode; 110539 K2 occurrences
  ActiveActor: 86200; String: 14670; QWordString: 2920; UniqueId: 6443; PartyLeader: 306
  shape/unclassified: 0; bit monotonicity: 0; raw-payload-shape failures: 0
  privacy-safe output: PASS
  production/Cargo/corpus mutation: 0/0/0
  aggregate SHA256: 335e4d96143160b4927ca11ef7666f9a18fa00bdd71ae8c866059c00342c4751
  summary SHA256: 9472f4faf9c701302198b7907a8389c244af716ffe81a7d1951346c5b5a9566e
  oracle JSONL SHA256: 196f4e4d2a588137ad12372cb2f0af79d7fca422c0bc2c5dea95506fa72cac4d
  witnesses JSONL SHA256: 7db56e75d6754767d95a11af269ea2c31978a35e83be808bb6c9100eca71cb9b
  receipt manifest SHA256: 400aa0b52a5e120b7791e34e9a364d4e40a2362c46d6770dad3c5292db8dc7cc

R3_17F_CONTRACT_CLOSURE:
  Outcome A / docs-only / production Rust unchanged
  common rule: LSB-first, unaligned allowed, exact one-value end bit, atomic failure
  context: net_version + already-resolved is_rl_223; current UniqueId/PartyLeader lane net_version=10
  ActiveActor: exact 1-bit active + 32-bit signed actor reference
  String: signed i32 Empty / Windows1252 / UTF16 with checked lengths
  QWordString: legacy QWord64 or RL223 positive Windows1252 only
  UniqueId: Steam / PlayStation / PsyNet / Epic(declared=33) only
  PartyLeader: only Some(Epic, Windows1252 declared=33), net10 + RL223 true
  unseen shapes/context combinations remain unadmitted

R3_17G_PRODUCTION_CLOSURE:
  production SHA: 9bfa837c69c4751f70ca63a17c65f0f89877ff32
  source blob: 7288238cfb5338653552435be6af41f0dd7a4e85
  focused test blob: 92033a72a8a737605ac3bf91e10d130082277e04
  implementation validation: 31805820332 / 94784362093 SUCCESS
  clean-candidate CI: 31806206582 / 94785622371 SUCCESS
  published-main CI: 31806554445 / 94786777798 SUCCESS
  exact production scope: crates/mimir-replay/src/lib.rs + r3_17g focused test only
  focused tests: 8/8 PASS; mimir-replay total: 189 PASS; workspace clippy: PASS
  native one-value K2: ActiveActor / String / QWordString / admitted UniqueId / admitted PartyLeader
  Cargo/fixture/corpus/support-lane changes: none

R3_17H_AUDIT_CLOSURE:
  Outcome A / read-only / production Rust unchanged at 9bfa837c69c4751f70ca63a17c65f0f89877ff32
  authority head: 9b8e8fe82ab5bdc663eecc3f5d3cd1e3b8ee38ac
  authority run/job: 31809282874 / 94795704797 SUCCESS
  exact-head normal CI: 31809282903 / 94795705073 SUCCESS
  artifact: 9222624242
  artifact digest: sha256:d6c773d593c3c50957507a19056e85aef8b769fdc03fd88c6d693b1258c0af28
  immutable witnesses selected: 469/469
  native decode success: 469/469
  tag/semantic variant exact: 469/469
  payload width exact: 469/469
  payload end exact: 469/469
  context gate exact: 469/469
  semantic value exact in-memory: 469/469
  negative controls: 7/7 PASS; privacy scan: PASS
  production/Cargo/corpus mutation: 0/0/0

R3_17I_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at 9bfa837c69c4751f70ca63a17c65f0f89877ff32
  authority head: 8962ddc6bd77b5469fa7ebc93c95334e5725a8ab
  authority run/job: 31812804986 / 94807233173 SUCCESS
  exact-head normal CI: 31812804992 / 94807233091 SUCCESS
  artifact: 9223916983
  artifact digest: sha256:5acdf953a91c814637ba6038d085cc72e8215003f76d93ce43a85afc0be05e1b
  47/47 oracle decode; 1699169 K3 occurrences; exact groups 1950; privacy-safe witnesses 6276
  Location: 26734 / 47 replays / 7 observed vector shapes / exact context groups 11
  RigidBody: 1550254 / 47 replays / 1169 observed structural shapes / exact context groups 1934
  ReplicatedBoost: 11058 / 11 replays / exact u8x4 / RL223=true observed only
  PickupNew: 111123 / 47 replays / None=90312 / SomeI32=20811
  RigidBody awake=1548807 / sleeping=1447 / rotation=quat56 only
  version context: 868.32 / net10 only; Location/RigidBody/PickupNew observed in RL223 false+true
  zero-tag/unclassified/bit-monotonicity/raw-payload failures: 0/0/0/0
  privacy-safe output: PASS; production/Cargo/corpus mutation: 0/0/0

R3_17J_CONTRACT_CLOSURE:
  Outcome A / docs-only / production Rust unchanged
  exact context: version 868.32 / net10; RL223 acceptance remains tag/shape-specific
  common rule: LSB-first, unaligned allowed, checked arithmetic, atomic failure, exact one-value end
  shared vector codec: net10 4-bit low + conditional discriminator; selected size 20/21 rejected
  exact durable groups: 1950 = Location 11 + RigidBody 1934 + PickupNew 4 + ReplicatedBoost 1
  RigidBody: sleeping bit + location + quat56 + awake-only linear/angular; quat48 rejected
  exact structural allowlist SHA256: 9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
  cross-product widening: 0
  production/Cargo/corpus mutation: 0/0/0

R3_17K_PRODUCTION_CLOSURE:
  Outcome A / production / exact R3.17J contract only
  production SHA: 7390e3b145372252caaa8fa1fe3e0cd13b83336c
  production tree: eebe4e21de77a43b5d9d43a34a0bfb08e06bab02
  parent: b0c0a4665e72da012d6447ca647db526a3da0020
  authority run/job: 31836699291 / 94884467585 SUCCESS
  first lint-only run: 31836440825 / 94883657836 NOT AUTHORITY
  exact-candidate CI: 31837081536 / 94885655480 SUCCESS
  published-main CI: 31837383875 / 94886588065 SUCCESS
  lib.rs blob: 28d213f831c8968e6756a6ccea2cd7aa6cdbdfba
  k3 allowlist module blob: da545a7144fefabab7f5be4f07fde71311065293
  focused test blob: 4d1434cc0e59a6e5c72a8404c102a87d71b8b223
  production allowlist equality: 1950/1950 exact / SHA256 9e5e2eba0305d5e48bd2021cf7300af259d7c2ca3ab3c1ef1586ad57cba6a911
  focused positives: all 1950 exact groups PASS; exhaustive current-lane structural acceptance PASS
  full mimir-replay suite: PASS; workspace clippy: PASS; full repository verifier: PASS
  exact production scope: lib.rs + k3_admitted_groups.rs + r3_17k focused integration test
  Cargo/fixture/corpus/support-lane changes: none
  property-loop / actor / frame / lifecycle widening: none

R3_17L_AUDIT_CLOSURE:
  Outcome A / read-only / production Rust unchanged at 7390e3b145372252caaa8fa1fe3e0cd13b83336c
  authority head: 0febcde7b312b6724e86ba156c700b41cf0562b7
  authority run/job: 31871353806 / 94980384463 SUCCESS
  exact-head normal CI: 31871353749 / 94980384205 SUCCESS
  artifact: 9243555556
  artifact digest: sha256:514580727df642ebde04d69824402db46ed48ff66755d4b17c0db6e69ac5eb3d
  47/47 replay identity + Boxcars oracle decode
  1950/1950 exact group reconstruction + real witness coverage + native decode + semantic match
  mismatch count: 0; negative controls: PASS; privacy: PASS
  max quaternion reconstructed-largest abs diff: 5.960464477539063e-08 under frozen 1e-5 rule
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_17M_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at 7390e3b145372252caaa8fa1fe3e0cd13b83336c
  authority head: a50f09857f36ac52cec30b4bf3efbde9e15bb564
  authority run/job: 31881779861 / 95005282281 SUCCESS
  exact-head normal CI: 31881779862 / 95005282149 SUCCESS
  artifact: 9246249473
  artifact digest: sha256:50839ba19f65feb92a2e79be30d36bf78fc4cc2e3280049cd591faf6846e2987
  47/47 replay identity + Boxcars oracle decode; deterministic double scan exact
  K4 occurrences: 39463; exact structural/context groups: 161; witnesses: 617
  all 11 target tags observed; zero/unclassified/bit/raw failures: 0/0/0/0
  groups SHA256: 80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
  privacy: PASS; production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_17N_CONTRACT_CLOSURE:
  Outcome A / contract-only / production Rust unchanged at 7390e3b145372252caaa8fa1fe3e0cd13b83336c
  contract authority branch head: 086ec251aea4eea9881cfc224bfac2d09596269f
  contract authority run/job: 31883205829 / 95008550716 SUCCESS
  clean contract main: c8ebb872e510574bb69ab28c719f415ece8b7665 / tree 61e36d40e6af3853a887e840b22f759dda26ed75
  exact clean-candidate CI: 31883438754 / 95009080782 SUCCESS
  published-main Knowledge Archive: 31883625387 / 95009532717 SUCCESS
  published-main normal CI: 31883625362 / 95009532734 SUCCESS
  admitted groups: 161/161 byte-identical to R3.17M evidence
  admitted-group SHA256: 80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b
  cross-product widening: 0
  positive/negative vector plans: PASS/PASS
  atomic failure + exact one-value end semantics: PASS/PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_17O_PRODUCTION_CLOSURE:
  Outcome A / production / exact R3.17N 161-group contract only
  pre-O canonical main: 3392c28ba8ec7d72766303646c0ceb57ed1e5a19
  production SHA: 492cc8218be7abc6db8f75acaea33d009ab2f175
  production tree: a66c47d7fb58da508188e64d42141987a0021a07
  parent: 3392c28ba8ec7d72766303646c0ceb57ed1e5a19
  authority head: 900d7eb122f10126558f13ea2c185cdb8c69fe1b
  authority run/job: 31885987240 / 95015252318 SUCCESS
  exact-candidate CI: 31886194387 / 95015736899 SUCCESS
  published-main CI: 31886353485 / 95016105618 SUCCESS
  lib.rs blob: 0161ba7fdcb6e395a2c972061ff6f56d07b8b5e8
  k4 allowlist module blob: 103503e25bc5af48381df021ab58133694fcece6
  k4 native module blob: a9c41f3bb11343165183ac9c815ab8fdf085936c
  focused test blob: 70437244bb49224281ee3a2e745e7b8a4b7a093a
  production allowlist equality: 161/161 exact / SHA256 80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b / cross-product widening 0
  focused positives: all 161 exact groups PASS; focused malformed/context/cross-product negatives PASS
  full mimir-replay suite: PASS; workspace check/test/clippy: PASS; full repository verifier: PASS
  exact production scope: lib.rs + k4_admitted_groups.rs + k4_native.rs + r3_17o focused integration test
  Cargo/fixture/corpus/support-lane changes: none
  property-loop / actor / frame / lifecycle widening: none

R3_17P_AUDIT_CLOSURE:
  Outcome A / read-only / production Rust unchanged at 492cc8218be7abc6db8f75acaea33d009ab2f175
  authority head: f2d87b732ad3103d50e2c047351f1017d4f3613f
  authority run/job: 31937527114 / 95141677175 SUCCESS
  exact-head normal CI: 31937527123 / 95141677140 SUCCESS
  artifact: 9261118033
  artifact digest: sha256:bc366b75e003531ba17351e880f259457ceba7cda702d912580c686990ba1beb
  47/47 replay identity + pinned Boxcars decode
  exact R3.17N group reconstruction + real witness coverage: 161/161
  native decode/tag/context/range/shape/semantic equality: 161/161 each
  mismatch count: 0; exhaustive K4 negative controls: PASS; privacy: PASS
  frozen numeric rule: exact f32 bit equality for CamSettings; exact vector wire fields + f32 bits; exact integer/boolean/object/count/version fields; tolerance 0
  LoadoutsOnline caller object table: same replay footer materialization, not inferred
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_18A_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at 492cc8218be7abc6db8f75acaea33d009ab2f175
  execution base main: c5878cf755302fe52e9e67741486306cd30db059
  authority head: 12ee215fd843260d5ece14f27aa1171cb862f49e
  authority run/job: 31941400273 / 95151024131 SUCCESS
  exact-head normal CI: 31941400276 / 95151024211 SUCCESS
  artifact: 9262129856
  artifact digest: sha256:295247a5f73159ac74539ffc5abf1eb2273fb6dc07a57f8b16976552a17b3ab8
  replay identity + pinned Boxcars parse: 47/47
  deterministic eligible first-property scalar candidates: 47
  selected witness: external_fixtures/sample_001.replay / frame 0 / actor ordinal 63 / actor id 2 / actor context object 98
  selected property: ordinal 0 / stream 27 of bound 67 / property object 55 / Int / value 62
  property_present bits: [10227,10228); stream bits: [10228,10234); payload bits: [10234,10266) / width 32
  payload SHA256: d2e2a0bd72f6f10bfb67239ca75c4fa03bb3d8e5dc3cd13e312a1620cd31290f
  native header/payload-start/semantic/payload-end equality: PASS/PASS/PASS/PASS
  next property_present consumed bits: 0; truncation negative: PASS; mismatch count: 0; privacy: PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_18B_OPEN_BOUNDARY:
  production implementation; minimal existing-actor single-property composition only
  reuse the existing R3.16B first-property header reader and existing R3.17C primitive scalar decoder; do not duplicate either wire codec
  require property_present=true, resolve the exact stream/property/tag through the existing lookup plan, and admit only K1 Boolean/Byte/Enum/Float/Int/Int64 payload dispatch
  return the exact one-property end cursor with stop_bit == payload_end_bit; do not read the next property_present bit
  K2/K3/K4 composition is outside this pass despite those one-value decoders existing separately
  focused tests must cover all six K1 tags, truncation/unsupported/absent cases, poison bits after payload, and an R3.18A-shaped Int=62 regression

R3_18B_HARD_STOP:
  no second property and no property_present loop
  no K2/K3/K4 composition inside the new one-property API
  no next actor / next frame / actor-table lifecycle mutation
  no Cargo, fixture, corpus or support-lane change
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.18B:
  only after clean production publication + exact validation, select a separate evidence pass for property-loop terminator/continuation; do not infer loop admission from one-property success
```

**Important:** the newest `main` commit can be newer than `LAST_PRODUCTION_CODE_SHA` because docs-only continuity commits are expected. Never confuse “newest main SHA” with “newest production Rust SHA.” Always inspect the diff.

---

# 2. WHAT MIMIR IS — FINAL SYSTEM MISSION

MIMIR is not merely a replay parser and not merely a dataset exporter.

The final system is intended to be a standalone Rocket League **replay intelligence engine + teacher factory + skill compiler + curriculum generator + counterfactual laboratory + runtime bridge support system**.

Its long-term pipeline is:

```text
Replay corpus / self-play traces / Gabriel rollouts
→ deterministic replay ingestion
→ native network decode
→ actor lifecycle reconstruction
→ canonical raw state timeline
→ exact + inferred event extraction
→ replay slices
→ canonicalization
→ event/contact graph
→ phase segmentation
→ skill seed extraction
→ parameter inference
→ bounded counterfactual expansion
→ physics/reachability validation
→ multi-dimensional scoring/ranking
→ reusable skill-family synthesis
→ anti-target generation
→ curriculum generation
→ teacher labels / ranking pairs
→ BC export
→ DAgger export
→ PPO/RL auxiliary export
→ low-latency runtime packages
→ Gabriel/V1 training/runtime consumption
→ new rollout/failure/novelty ingestion
→ closed-loop refresh
→ skill aging/deduplication/retirement
```

MIMIR must remain useful as a standalone project. It must **not require BC, DAgger, PPO, SAC, Gabriel, or a particular runtime bot to exist**. Those systems are consumers/adapters.

MIMIR is also not intended to run enormous search loops inside a live Rocket League match. Heavy analysis belongs offline/bounded/cached. Runtime consumption should use small validated packages, options, skill selectors, fallback logic and opponent summaries.

---

# 3. FINAL DEFINITION OF MIMIR “DONE”

MIMIR is not finished when the replay parser works. It is finished only when the complete validated loop exists.

Minimum final completion criteria:

```text
[ ] Native replay decode works for the admitted production format coverage.
[ ] Actor lifecycle reconstruction is deterministic and evidence-backed.
[ ] Canonical raw-state timelines for ball/cars/game state exist.
[ ] Exact decoded events and inferred tactical events are separated by provenance.
[ ] Replay slicing works from automatic events and user-selected time ranges.
[ ] Canonicalization maps symmetric/equivalent situations consistently.
[ ] Event/contact graphs and phase segmentation are real, not placeholder contracts.
[ ] Rare replay moments can become skill seeds without being falsely called learned skills.
[ ] Skill parameter inference creates transferable family candidates.
[ ] Counterfactual expansion is bounded and physics-aware.
[ ] Reachability/feasibility validation rejects impossible branches.
[ ] Multi-dimensional scoring and ranking exist.
[ ] Skill family synthesis, fingerprints, deduplication and versioning exist.
[ ] Anti-targets are generated from meaningful near-miss/bad alternatives.
[ ] Curriculum generation can move easy → medium → hard → pressure/adversarial.
[ ] Teacher outputs include confidence and abstention.
[ ] Real BC export exists.
[ ] Real DAgger correction export exists.
[ ] PPO/RL auxiliary export exists without making MIMIR the PPO trainer.
[ ] Runtime bridge packages exist and are low-latency/bounded.
[ ] Player/opponent profiling and spatial heatmaps exist.
[ ] Gabriel rollout ingestion exists.
[ ] Failure/novelty mining closes the learning loop.
[ ] Skill aging/retirement/deduplication is implemented.
[ ] Incremental/resumable corpus indexing exists for the ~212K replay corpus.
[ ] Parallel processing, caching, invalidation and audit lineage are production-ready.
[ ] Fuzzing/malformed replay handling cannot crash or silently corrupt the pipeline.
[ ] A full low_boost_recovery vertical slice runs replay → skill → teacher/export end to end.
[ ] At least one additional mechanically/tactically different skill family proves generality.
[ ] Gabriel/V1 can consume MIMIR-produced artifacts through an explicit adapter boundary.
[ ] Every output can be traced back to replay/frame/slice/evidence identity.
```

Do not call MIMIR complete before these dependencies close.

---

# 4. CORE PHILOSOPHY — NON-NEGOTIABLE RULES

## 4.1 Truth first

Never claim a capability because a type, scaffold, README paragraph or external oracle exists.

Examples:

```text
Boxcars decodes actor bits
!= MIMIR decodes actor bits

MIMIR knows stream_id → RigidBody tag
!= MIMIR decodes RigidBody payload bits

Replay slice contract exists
!= automatic replay slicing works

BC row schema exists
!= real replay-derived BC dataset exists
```

Capability requires code + tests + corpus evidence + exact publication evidence where applicable.

## 4.2 Fail closed

Unknown build, unknown encoding, unknown property tag, truncated bitstream, impossible bounds, unresolved semantic mapping or unsupported branch must not silently guess.

Use explicit categories such as:

```text
Unsupported
Malformed
Truncated
MappingError
NotImplemented
Abstain / Uncertain
```

Do not turn unknown into zero/default merely to keep the pipeline moving.

## 4.3 Determinism

Given identical input bytes + configuration + versioned code, output must be reproducible.

When ordering matters, prefer deterministic collections (`BTreeMap`, `BTreeSet`, sorted vectors) unless a performance pass proves a different representation is necessary and output ordering remains canonicalized.

## 4.4 Evidence before widening

Binary/network format work must usually follow:

```text
read-only audit
→ corpus/oracle evidence
→ admitted contract
→ narrow implementation
→ differential/regression audit
```

One-bit mistakes poison everything after them. “Looks right” is not an admission policy.

## 4.5 Structural decode and semantics are separate

Maintain the layering:

```text
bytes
→ structural sections
→ wire fields
→ typed network values
→ actor property state
→ Rocket League semantic entity state
→ canonical raw state
→ events
→ slices
→ skills
```

Do not skip layers to save time.

## 4.6 Observed vs derived vs inferred vs unknown

Any future state/action/event field that is not directly decoded should carry provenance.

Recommended vocabulary:

```text
OBSERVED / DECODED
DERIVED
INFERRED
UNKNOWN
```

Confidence belongs on inference layers.

## 4.7 Abstention is a feature

If confidence is insufficient, MIMIR may abstain. Do not force a label or teacher target.

## 4.8 No hidden external production backend

Boxcars is an oracle/reference for evidence. RocketSim will be a simulation backend through an explicit adapter. Neither should become a hidden runtime dependency by accident.

## 4.9 Full corpus is not a development toy

The large local replay corpus must not be dumped into normal Git. Checked-in regression corpora prove development behavior. Full-corpus processing later requires indexed/resumable execution and likely a self-hosted GitHub runner or explicit external corpus worker/storage boundary.

---

# 5. SOURCE-OF-TRUTH PRECEDENCE

When sources disagree, use this order:

```text
1. fresh origin/main source code + tests
2. exact-SHA GitHub Actions/evidence tied to the relevant milestone
3. this file's CURRENT STATE BLOCK
4. admitted decision/evidence artifacts in repository
5. other docs/continuity files
6. current roadmap sections in this file
7. historical docs/executor artifacts
8. old chat summaries / memory
```

If source/tests disagree with this file:

```text
STOP new capability work
→ inspect git history / CI
→ reconstruct truth
→ update this file in docs-only commit
→ then continue
```

Never silently follow stale prose over code.

---

# 6. REPOSITORY / WORKSPACE MAP

Current Rust workspace members at the continuity checkpoint:

```text
crates/mimir-types
crates/mimir-config
crates/mimir-core
crates/mimir-io
crates/mimir-export
crates/mimir-replay
crates/mimir-anchor
crates/mimir-branch
crates/mimir-rollout
crates/mimir-score
crates/mimir-skill
crates/mimir-teacher
crates/mimir-cache
crates/mimir-cli
crates/mimir-sim-bridge
```

Use these responsibility boundaries unless current source proves they changed:

### `mimir-types`
Shared stable IDs, primitive/versioned data contracts, metadata/value types. Avoid putting heavy behavior here.

### `mimir-config`
Configuration schemas/loaders/defaults. Config should be explicit and versioned where behavior depends on it.

### `mimir-core`
Cross-cutting orchestration contracts and central composition logic that does not belong to a narrower domain crate.

### `mimir-io`
Filesystem/serialization/input-output boundaries. Keep OS/path mechanics away from pure parser logic where possible.

### `mimir-export`
Exported datasets/artifacts/manifests and reload/verification behavior.

### `mimir-replay`
Replay bytes, header/body/footer/network parsing, future actor reconstruction/raw-state extraction and replay-specific provenance. Binary wire code belongs here unless a later explicit crate split is admitted.

### `mimir-anchor`
Anchor discovery/contracts: decision onset, contact anchors, recovery starts, etc.

### `mimir-branch`
Counterfactual branch definitions/generation boundaries.

### `mimir-rollout`
Rollout request/job/result/report persistence and future simulation execution orchestration.

### `mimir-score`
Counterfactual/outcome scoring vectors, ranking components and scoring policies.

### `mimir-skill`
Skill seeds, canonicalization, phase plans, skill families, dedup/fingerprints, curriculum-facing skill contracts.

### `mimir-teacher`
Teacher labels, ranking pairs, confidence/abstain semantics and teacher synthesis.

### `mimir-cache`
Deterministic caching, keys, invalidation, artifact reuse.

### `mimir-cli`
User/automation commands. CLI should orchestrate real library behavior rather than contain hidden business logic.

### `mimir-sim-bridge`
Physics/simulator adapter boundary. Real RocketSim integration belongs here through an explicit versioned backend, not by copying another project wholesale.

Before adding code, ask:

```text
Is this wire parsing? → mimir-replay
Is this cross-replay skill representation? → mimir-skill
Is this simulation backend glue? → mimir-sim-bridge
Is this scoring? → mimir-score
Is this teacher artifact logic? → mimir-teacher
Is this only CLI orchestration? → mimir-cli
```

Do not create circular responsibilities for convenience.

---

# 7. RUST CODING RULES FOR FUTURE SESSIONS

## 7.1 Use narrow versioned contracts

Prefer names such as:

```text
ReplayNetworkFirstActorEnvelopeV1
CanonicalRawStateV1
SkillSeedV1
TeacherLabelV1
```

when the contract is expected to evolve materially.

Do not create a vague mega-struct with optional fields for every future feature.

## 7.2 Keep parsing helpers pure where possible

Binary functions should ideally receive byte/bit slices + explicit context and return typed results/errors. Avoid global mutable state.

## 7.3 Cursor accounting must be testable

For bitstream work:

- expose cursor offset internally or in diagnostic/evidence output;
- truncation must return explicit failure;
- no silent over-read;
- no cursor rewind unless the algorithm explicitly requires it and tests prove it.

## 7.4 Bounds before indexing

Every object index, actor ID, stream ID, cache/property index and slice boundary must be validated before indexing.

## 7.5 Preserve raw values when semantics are uncertain

If a field is structurally known but semantics are not, carry it as an opaque/raw typed field rather than inventing meaning.

## 7.6 One canonical bounded-integer implementation

Actor IDs and stream IDs must not each receive independent almost-identical helpers.

The admitted Rocket League bounded integer behavior is:

```text
read low bits determined by bound
compute candidate upper value
depending on candidate vs bound, possibly read one extra discriminator bit
choose low or upper value
```

Do not replace this with `read_bits(width)`.

## 7.7 Comments explain protocol reasons

Comment important “why” facts, especially:

- version gates;
- optional bits;
- overwrite semantics;
- weird trailer behavior;
- intentionally unsupported branches.

Avoid comments that merely restate syntax.

## 7.8 No incidental dependency changes

Parser/skill changes that do not require dependencies must not touch `Cargo.toml` or `Cargo.lock`. If Cargo regenerates lock state unexpectedly during validation, restore it and investigate separately.

## 7.9 No giant all-at-once decoder patches

Network progression is intentionally granular:

```text
bit primitive
→ first envelope
→ new actor branch
→ property envelope
→ attribute families
→ actor lifecycle
→ one frame
→ frame loop
```

Do not collapse them.

---

# 8. TESTING STANDARD — EVERY IMPLEMENTATION PASS

A future agent should not invent a lighter test bar because it is tired.

## 8.1 Focused validation

Typical minimum:

```text
cargo fmt --all -- --check
cargo check -p <target-crate> --all-targets --all-features
cargo test -p <target-crate> -- --nocapture
cargo clippy -p <target-crate> --all-targets --all-features -- -D warnings
```

If another crate consumes the changed API, include it.

## 8.2 Test categories

Every new capability should cover as applicable:

```text
[ ] real replay happy path
[ ] synthetic surgical happy path
[ ] truncation at every newly consumed field boundary
[ ] wrong/unsupported version
[ ] invalid index/bound
[ ] malformed value branch
[ ] previous behavior regression
[ ] future boundary remains closed
[ ] deterministic repeatability
[ ] differential oracle vectors when relevant
```

## 8.3 Corpus regression

Use checked-in real corpus appropriate to the claim:

- 3 historical fixtures for legacy evidence where relevant;
- `largest_100` for stress/compatibility evidence;
- current 47-supported lane for admitted network differential behavior;
- later semantically diverse corpus for events/skills.

Do not cherry-pick only files that pass.

## 8.4 Full repository validation

Before publication, use current canonical repository verifier/CI. At the current lineage this generally includes:

```text
cargo fmt check
cargo check workspace/all-targets/all-features
mimir-replay tests
mimir-skill tests
workspace tests
clippy -D warnings
replay corpus size/SHA verification
compatibility/admission matrix
repository verification wrapper
```

Use current workflow/scripts as source of truth if commands evolve.

## 8.5 PowerShell native exit-code rule

GitHub Actions PowerShell can remain green after a native process failed if exit codes are not propagated.

After native commands, explicitly gate:

```powershell
& cargo test ...
if ($LASTEXITCODE -ne 0) {
    throw "cargo test failed: $LASTEXITCODE"
}
```

Apply to:

```text
cargo
git
python
rustc
oracle binaries
custom evidence tools
```

A green job without proven native exit propagation is not evidence.

---

# 9. GITHUB-ONLY DEVELOPMENT / PUBLICATION PROTOCOL

The user wants MIMIR work performed through GitHub and GitHub Actions whenever practical.

## 9.1 Before every pass

```text
fetch fresh main
record main SHA
inspect last commits
compare against expected production base
inspect target source/tests
inspect current pass in this file
```

## 9.2 Branch types

Recommended naming:

```text
agent/<pass>-evidence
agent/<pass>-implementation
agent/<pass>-clean
agent/<pass>-clean-validation
docs/<milestone>-continuity
```

Names may vary, intent should not.

## 9.3 Temporary workflows

Temporary evidence/patch workflows may live on disposable branches.

They must not enter clean production commits unless separately admitted as permanent tooling.

## 9.4 Evidence pass

```text
fresh main
→ evidence branch
→ temporary tool/workflow
→ exact oracle/corpus identity
→ fail-fast run
→ evidence artifact/summary
→ Outcome A/B/C
```

No production source change unless pass explicitly says otherwise.

## 9.5 Implementation pass

```text
admitted evidence/contract
→ implementation branch
→ allowed files only
→ focused fail-fast validation
→ diff scope audit
```

## 9.6 Clean reconstruction

Do not publish temporary workflow history.

```text
verified source blob(s)
→ fresh main parent
→ source-only clean commit
→ audit changed files
```

Clean commit rules:

```text
behind main = 0
only allowed production files changed
no temporary workflow
no accidental Cargo.lock
no oracle source
no generated logs
```

## 9.7 Exact-SHA validation

Validation runner must first assert:

```text
git rev-parse HEAD == EXPECTED_CLEAN_SHA
```

Then run full verifier.

## 9.8 Publication

Immediately before main update:

```text
fetch main again
compare ancestry again
```

Publish only as fast-forward with:

```text
force = false
```

Ordinary MIMIR production passes must not force-push main.

## 9.9 Publication readback

After main moves:

```text
resolve exact main SHA
run/fetch exact-main CI
read actual test/corpus/differential counts
only then mark milestone production-complete
```

## 9.10 Continuity sync

After the milestone closes, update **this file** in a docs-only commit.

A production source commit and continuity update should normally be separate.

---

# 10. PASS TEMPLATE — COPY THIS FOR EVERY FUTURE PASS

Every pass begins by filling:

```text
PASS ID:
PASS TYPE:
BASE MAIN SHA:
LAST PRODUCTION CODE SHA:
ALLOWED FILES:
FORBIDDEN FILES:
INPUT CORPUS:
ORACLE / REFERENCE:
OPEN BOUNDARY:
HARD STOP BOUNDARY:
EXPECTED OUTPUTS:
FOCUSED VALIDATION:
FULL VALIDATION:
PUBLICATION POLICY:
CONTINUITY UPDATE REQUIRED:
```

Every pass ends with:

```text
PASS:
TYPE:
BASE SHA:
RESULT:
OUTCOME: A / B / C
CHANGED PRODUCTION FILES:
TEMPORARY FILES:
TEST COUNTS:
CORPUS COUNTS:
DIFFERENTIAL COUNTS:
BOUNDARY OPENED:
BOUNDARIES STILL CLOSED:
CLEAN COMMIT SHA:
PUBLISHED MAIN SHA:
PUBLICATION CI:
THIS FILE UPDATED:
NEXT EXACT PASS:
```

Outcome meanings:

```text
A = evidence/implementation sufficient, proceed
B = bounded gap, open only targeted follow-up
C = contradiction/regression, reopen policy/evidence; do not widen
```

---

# 11. CURRENTLY PROVEN PRODUCTION CAPABILITY

At R3.13 production can truthfully claim:

```text
[x] exact-admitted replay header parsing for current supported lane
[x] body structural boundary extraction
[x] content scaffold extraction
[x] network payload offset/size discovery
[x] footer scaffold extraction
[x] footer lookup materialization
[x] first-frame timing precondition/header-derived static information
[x] static network attribute-tag registry
[x] static spawn-trajectory registry
[x] static network lookup-plan construction
[x] per-object effective inherited stream/property maps
[x] per-object max_prop_id / prop_id_bits
[x] object lookups
[x] channel/build-derived plan flags
```

Differential evidence for the supported 47 replay lane:

```text
attribute updates checked:        3,990,310
property resolution matches:      3,990,310
unresolved_stream:                0
property_object_mismatch:         0
decoded_not_implemented_hits:     0
```

This proves the **static lookup plan**, not native payload decode.

---

# 12. CRITICAL NETWORK FORMAT FACTS ALREADY LEARNED

## 12.1 First frame/actor order

Pinned Boxcars confirms:

```text
frame:
    f32 time
    f32 delta
    actor_present bit loop

if actor_present:
    bounded actor_id
    alive bit

if alive:
    new bit

if new:
    version-gated name_id
    one bit
    object_id
    spawn trajectory
else:
    property_present loop
    bounded stream_id
    attribute payload
```

## 12.2 Bounded integer is value-dependent

Pinned Boxcars algorithm consumes low bits and may consume one additional discriminator bit depending on candidate value vs max bound.

Actor IDs and stream IDs must use the same admitted algorithm.

## 12.3 Actor ID overwrite

Same actor ID receiving another `NewActor` is not automatically malformed.

Observed supported-corpus evidence:

```text
same-class overwrite:       141,511
class-changing overwrite:   0
```

Pinned Boxcars explicitly overwrites existing actor state.

Therefore future code must never contain a blanket rule:

```text
duplicate actor ID => malformed
```

## 12.4 Network frame terminal

Format audit indicates `time == 0.0 && delta == 0.0` is the end-frame sentinel in Boxcars decoding.

Full production terminal/trailer behavior remains closed until the frame iteration phase.

---

# 13. CURRENT PASS CHECKLIST — R3.14A

**Goal:** gather exact differential evidence for first frame + first actor envelope header before MIMIR consumes these bits natively.

**Production source change:** forbidden.

**Pinned oracle:** `nickbabcock/boxcars@c70e77df7af81b436cb545d070bb90c82f562d0b`.

**Supported lane definition:** enumerate all 103 checked-in replay inputs; run MIMIR production header admission; the exact 47 admitted replays are the differential lane. Do not select “first 47 filenames.”

### Completed / in-flight

```text
[x] Fresh continuity main was inspected before branch creation.
[x] R3.14A evidence branch created: agent/r3-14a-first-actor-envelope-evidence.
[x] Boxcars pin recovered from historical R3.10 workflow/Cargo manifest.
[x] Boxcars pin independently exists upstream.
[x] R3.13 47-supported-lane mechanism recovered.
[x] tools/r3_14a_selector/Cargo.toml added on evidence branch.
[x] tools/r3_14a_selector/src/main.rs added on evidence branch.
[>] Validate selector via GitHub Actions with explicit native exit-code checks.
[ ] Confirm selector emits exact supported=47 / unsupported=56.
[ ] Confirm lookup-plan creation succeeds for all selected 47.
[ ] Produce stable manifest identity per supported replay.
[ ] Record relative path, bytes, SHA-256, BuildVersion, network_start/network_size, max_channels/channel_bits.
```

### Oracle instrumentation

```text
[ ] Clone/fetch exact Boxcars SHA in Actions temp directory or use exact patched dependency checkout.
[ ] Assert oracle HEAD == c70e77df7af81b436cb545d070bb90c82f562d0b.
[ ] Assert clean oracle tree before instrumentation.
[ ] Patch observation-only instrumentation into frame decoder.
[ ] Record instrumentation patch/hash.
[ ] Do NOT change parser decisions, bounds, branch order or error behavior.
```

### Evidence fields per replay

```text
[ ] frame_start_bit
[ ] time raw u32 + f32
[ ] delta raw u32 + f32
[ ] bit_after_time_delta
[ ] actor_present bit offset + value

if actor_present:
[ ] actor_id bound
[ ] actor_id start bit
[ ] actor_id value
[ ] actor_id end bit
[ ] actor_id bits consumed
[ ] optional discriminator consumption/value if instrumentation can expose non-invasively
[ ] alive bit offset + value

if alive:
[ ] new bit offset + value
[ ] first_actor_header_end_bit
```

### Hard stop

Do not admit evidence beyond:

```text
name_id
post-name_id bit
object_id
spawn payload
property_present
stream_id
attribute payload
second actor
second frame
raw state
```

### Aggregate gates

```text
[ ] replays_total = 47
[ ] unique_sha256 = 47
[ ] oracle_parse_success = 47
[ ] first_frame_rows = 47
[ ] non_finite_time = 0
[ ] non_finite_delta = 0
[ ] first-frame zero/zero terminal count = 0
[ ] schema_errors = 0
[ ] bit_offset_monotonicity_failures = 0
[ ] MIMIR production source mutation = 0
[ ] oracle SHA exact
```

### R3.14A result

```text
[ ] Choose Outcome A/B/C.
[ ] If A: update this file CURRENT_PASS → R3.14B.
[ ] If B: write only the smallest missing evidence follow-up.
[ ] If C: reopen format policy and do not implement native cursor.
```

---

# 14. MASTER TODO — PART I: NATIVE NETWORK DECODER

This dependency order is mandatory unless new evidence explicitly changes it. Future pass IDs may split, but do not skip dependencies.

## R3.14B — Evidence admission + BitCursor / bounded-int contract

Goal: convert R3.14A observations into a precise implementation contract.

Checklist:

```text
[ ] Define bit numbering/order relative to network_start.
[ ] Define cursor offset semantics.
[ ] Define read_bit behavior.
[ ] Define little-endian arbitrary-bit read behavior.
[ ] Define aligned/unaligned f32 read behavior.
[ ] Define bounded integer exact algorithm.
[ ] Define bound=0/1 edge policy.
[ ] Define truncation errors for low bits/discriminator.
[ ] Define maximum supported bound widths.
[ ] Turn all 47 oracle actor-ID rows into test vectors.
[ ] Specify expected end bit for every vector.
[ ] Keep actor semantics out of primitive contract.
```

Done when contract can be implemented without consulting Boxcars source during coding.

## R3.14C — Native BitCursor + bounded integer primitive

Implementation rules:

```text
[ ] Add smallest reusable bit cursor primitive in mimir-replay.
[ ] No actor-specific branching inside primitive.
[ ] Deterministic cursor offset.
[ ] No hidden allocations in hot path unless justified.
[ ] Explicit EOF/truncation errors.
[ ] Synthetic threshold/discriminator tests.
[ ] 47 oracle vector value equality = 100%.
[ ] 47 oracle vector end-bit equality = 100%.
[ ] Full repository regression unchanged.
```

## R3.14D — First actor envelope native reader

Reader stops after `new`.

Candidate output concept:

```text
time raw/decoded
delta raw/decoded
actor_present
actor_id optional
alive optional
new optional
stop_bit
```

Checklist:

```text
[ ] Use production lookup plan for bounds/preconditions.
[ ] Consume exactly first frame preamble + one actor envelope header.
[ ] Do not consume name_id/spawn/property data.
[ ] Unsupported header versions remain unsupported.
[ ] Add truncation test at every field.
[ ] Add no-actor-present branch test.
[ ] Add alive=false branch test.
[ ] Add alive=true/new=false test.
[ ] Add alive=true/new=true stop-before-name_id test.
```

## R3.14E — First-envelope differential audit

Require exact 47-replay equality for:

```text
[ ] time raw bits
[ ] delta raw bits
[ ] actor_present
[ ] actor_id
[ ] alive
[ ] new
[ ] stop bit
```

Any mismatch blocks R3.15.

## R3.15A — NewActor branch oracle evidence

Evidence only:

```text
[ ] version gate for name_id
[ ] name_id value/bit range where present
[ ] unnamed one-bit field value/range
[ ] object_id decode/value/range
[ ] spawn trajectory kind from static plan
[ ] spawn location wire values/range if required
[ ] spawn rotation wire values/range if required
[ ] branch end bit
[ ] distribution across 47 replays
```

## R3.15B — NewActor contract

```text
[ ] exact name_id gate
[ ] opaque one-bit policy if semantics unnecessary
[ ] object_id bounds
[ ] object lookup validation
[ ] spawn trajectory dispatch contract
[ ] malformed/truncation taxonomy
```

## R3.15C — Native NewActor envelope

```text
[ ] implement only admitted branch
[ ] retain raw wire values where semantic meaning not needed
[ ] differential value match
[ ] differential end-bit match
[ ] no actor lifecycle mutation yet beyond minimum test scaffolding
```

## R3.16A — Existing actor / first property envelope evidence

Stop at payload start:

```text
[ ] property_present bit
[ ] bounded stream_id start/end/value
[ ] resolved property object ID
[ ] attribute tag
[ ] payload_start_bit
[ ] compare static lookup plan to oracle context
```

## R3.16B — Native property-envelope header

```text
[ ] consume property_present
[ ] consume bounded stream_id with canonical primitive
[ ] resolve through ReplayNetworkLookupPlanV1
[ ] produce property object/tag
[ ] stop before payload
[ ] differential exact stream/property/tag/payload-start
```

## R3.17 — Attribute decoder program

Never implement all tags in one giant patch.

### Wave 1 — scalar primitives

```text
[ ] Boolean
[ ] Byte
[ ] Int
[ ] Int64
[ ] Float
[ ] Enum
```

### Wave 2 — reference/text-like

```text
[ ] ActiveActor/reference family
[ ] String
[ ] QWordString
[ ] UniqueId
[ ] PartyLeader
```

### Wave 3 — physics/spatial high-value

```text
[ ] Location/vector forms
[ ] RigidBody
[ ] ReplicatedBoost
[ ] PickupNew
```

### Wave 4 — structured gameplay families

```text
[ ] CamSettings
[ ] TeamPaint
[ ] TeamLoadout
[ ] ClubColors
[ ] Reservation
[ ] StatEvent
[ ] PlayerHistoryKey
[ ] DemolishFx
[ ] DemolishExtended
[ ] ExtendedExplosion
[ ] LoadoutsOnline
[ ] remaining observed admitted tags by frequency/value
```

For every attribute family:

```text
oracle vectors
→ wire contract
→ synthetic malformed tests
→ native implementation
→ differential corpus audit
→ publication
```

Unknown tag stays explicit `NotImplemented`/unsupported until admitted.

## R3.18 — One complete existing-actor property loop

```text
[ ] decode one full property payload
[ ] prove payload end cursor
[ ] iterate property_present loop for one actor update
[ ] never skip unknown payload by guessing size
[ ] exact oracle operation/value/end cursor comparison
```

## R3.19 — Actor lifecycle table

State table keyed by actor ID.

Must cover evidence-backed cases:

```text
[ ] NewActor unused ID
[ ] NewActor same-class overwrite
[ ] NewActor class-changing overwrite policy
[ ] update existing ID
[ ] update missing ID policy
[ ] delete existing ID
[ ] delete missing ID policy
```

Regression lock:

```text
same-class NewActor overwrite MUST remain accepted
```

## R3.20 — Complete one frame

```text
[ ] decode all actor envelopes in first frame
[ ] produce ordered actor operations
[ ] apply lifecycle state
[ ] exact frame end bit
[ ] differential operation order vs oracle
[ ] no second frame until first-frame cursor is exact
```

## R3.21 — Frame iteration + terminal/trailer

Evidence then implementation:

```text
[ ] zero/zero terminal behavior
[ ] NumFrames/keyframe relationship
[ ] supported version trailer behavior
[ ] newer version optional 32-bit trailer gate
[ ] final network cursor
[ ] multi-frame loop
[ ] malformed/truncated terminal handling
```

## R3.22 — Network decoder lane closure

Required before raw-state phase:

```text
[ ] all 47 supported replays decode natively without Boxcars fallback
[ ] deterministic actor-operation stream
[ ] no unresolved admitted attribute payloads in supported lane, or explicit support policy narrows lane
[ ] malformed/truncation corpus fails safely
[ ] final network cursor reconciles with payload boundary
[ ] performance baseline
[ ] memory baseline
[ ] differential summary archived
[ ] formal network-decoder capability matrix updated
```

---

# 15. MASTER TODO — PART II: CANONICAL RAW STATE

## R4.0 — Raw-state schema design

Do not begin semantic mapping until schema exists.

Target fields per sample/frame may include:

```text
time/frame identity
ball position / linear velocity / angular velocity
car position / linear velocity / angular velocity / orientation
boost
wheel/ground contact
jump state
dodge/flip availability/state when observable or inferable
team/player identity
score/game clock
demolition state
last touch/touch ownership where available
kickoff state
provenance/confidence per non-direct field
```

Checklist:

```text
[ ] version schema
[ ] decoded/derived/inferred/unknown provenance model
[ ] coordinate convention
[ ] orientation convention
[ ] units
[ ] sparse-update carry-forward policy
[ ] actor replacement reset policy
[ ] missing-field representation
[ ] deterministic serialization
```

## R4.x — Semantic network→entity mapping

Recommended order:

```text
[ ] ball actor identity
[ ] ball rigid body
[ ] car/pawn actor identity
[ ] car rigid body
[ ] player identity
[ ] team identity
[ ] boost amount
[ ] game/score state
[ ] demolition state
[ ] touch/contact references
[ ] jump/dodge mechanics if protocol evidence permits
```

Every mapping needs real replay evidence and regression tests.

## R5 — Raw-state extraction

```text
[ ] frame → canonical state materialization
[ ] stable entity identity across overwrite/delete
[ ] correct sparse property carry-forward
[ ] no non-finite state leakage
[ ] deterministic same replay → same sequence
[ ] provenance retained
[ ] state artifact reload/round-trip tests
```

---

# 16. MASTER TODO — PART III: EVENTS, TIMELINE & SLICES

## R6 — Primitive/exact event detector

Initial families:

```text
[ ] ball touch
[ ] goal
[ ] demolition
[ ] boost pickup
[ ] kickoff start/end
[ ] takeoff/landing
[ ] jump/dodge where observable
[ ] car-ball contact
[ ] ball-wall contact
[ ] ball-ground contact
[ ] car-ground/surface contact
```

Separate protocol-decoded vs derived events.

## R6.x — Tactical/inferred event detector

Examples:

```text
[ ] shot candidate
[ ] save candidate
[ ] clear
[ ] pass
[ ] challenge
[ ] fake challenge
[ ] 50/50
[ ] possession transition
[ ] shadow defense
[ ] pressure
[ ] boost starvation
[ ] recovery
[ ] overcommit
[ ] open net
[ ] counterattack
```

For every inferred event:

```text
confidence
features/reasons
window
model/detector version
abstain behavior
```

## R7 — Timeline / replay slice engine

Support automatic and user-selected slices.

Each slice:

```text
source replay identity
start/end frame
start/end time
participants
raw-state sequence
events/context
confidence/provenance
```

Add **Control-Onset Rewind** so decision branches begin near control decision onset rather than only at visible outcome/contact.

Checklist:

```text
[ ] event-centered windows
[ ] arbitrary selected time ranges
[ ] pre-roll/post-roll
[ ] stable ReplaySliceRef
[ ] slice identity hash
[ ] artifact lineage to replay SHA
```

---

# 17. MASTER TODO — PART IV: CANONICALIZATION, GRAPHS & SKILL SEEDS

## R8 — Canonicalization

Normalize equivalent situations:

```text
[ ] team-normalized attacking direction
[ ] field mirroring
[ ] goal-relative coordinates
[ ] player-relative coordinates
[ ] ball-relative features
[ ] heading/orientation normalization
[ ] optional surface-relative frames
[ ] temporal normalization where justified
```

Property tests should prove symmetries/inverses where applicable.

## R9 — Event/contact graph

Nodes can include:

```text
pose/ball states
jump/dodge
wheel/surface contact
ball contact
boost burst
goal/challenge/possession transition/recovery stable
```

Edges:

```text
precedes
causes
enables
contacts
transitions_to
overlaps
constrains
```

## R10 — Phase segmentation

Examples for recovery:

```text
air correction
→ descent
→ first contact
→ stabilization
→ exit acceleration
```

Examples for flick:

```text
approach
→ control/capture
→ setup
→ jump
→ dodge/contact
→ release
→ recovery
```

Store boundary confidence.

## R11 — Skill seed extraction

One rare replay moment is a **skill seed**, not a learned skill.

Seed contains:

```text
canonical initial state
context/intention proxy
phase graph
control/action evidence
contacts
timing
outcome
constraints
confidence
source lineage
```

The first end-to-end skill vertical slice remains:

```text
low_boost_recovery
```

After that, prove generality with at least one mechanically different family.

---

# 18. MASTER TODO — PART V: SKILL PARAMETERIZATION & COUNTERFACTUAL COMPILER

## R12 — Skill parameter inference

Infer reusable variables such as:

```text
approach speed
ball offset
boost budget
jump timing
dodge timing
yaw/pitch/roll corrections
surface angle
landing angle
exit vector
opponent ETA
wall distance
```

Output ranges/distributions/correlations rather than one fixed sequence.

## R13 — Counterfactual expansion

Bounded variation sources:

```text
state perturbations
timing shifts
approach angles
boost availability
opponent position/pressure
ball velocity/offset
primitive action variations
```

Do not brute force infinite action space. Use event-conditioned grammar + pruning.

## R14 — Physics / feasibility / reachability

Through `mimir-sim-bridge` and a real simulator backend when admitted:

```text
[ ] reachable position/orientation
[ ] acceleration/turn constraints
[ ] boost budget
[ ] jump/dodge availability
[ ] collision validity
[ ] contact geometry
[ ] arrival/intercept timing
[ ] surface constraints
```

Result:

```text
valid / invalid / uncertain-abstain
```

## R15 — Micro-rollout engine

For each anchor/slice:

```text
observed action branch
+ bounded alternative branches
→ simulator rollout
→ outcome vector
```

Heavy rollout work stays offline/cached.

---

# 19. MASTER TODO — PART VI: SCORING, RANKING, ANTI-TARGETS

## R16 — Multi-dimensional scoring

Components should include as evidence permits:

```text
goal probability
concede probability
possession
ball progress
boost economy
recovery quality
pressure
position quality
future controllability/options
robustness
punish risk
overcommit risk
```

Preserve component vector. Scalar aggregation can exist, but never destroy explainability.

## R17 — Observed vs counterfactual ranking

```text
[ ] pairwise preference data
[ ] confidence
[ ] margin/uncertainty
[ ] abstain on weak comparisons
```

## R18 — Anti-target generation

Examples:

```text
early dodge
late dodge
wrong landing orientation
overboost
bad challenge timing
unsafe approach
panic clear
possession throwaway
```

Anti-target means “avoid this near alternative,” not merely a random negative sample.

---

# 20. MASTER TODO — PART VII: SKILL FAMILY SYNTHESIS & LIFECYCLE

## R19 — Skill family synthesis

Validated seed + counterfactual coverage becomes reusable skill object.

Conceptual fields:

```text
skill_id
family
version
entry domain
parameters
phase graph
success predicates
failure predicates
anti-targets
difficulty
confidence
source evidence
counterfactual coverage
curriculum hooks
runtime hooks
training exports
```

## R20 — Skill fingerprint / deduplication

```text
[ ] canonical fingerprint
[ ] similarity metric
[ ] duplicate merge policy
[ ] near-family relation
[ ] conflicting-family handling
```

## R21 — Skill aging / retirement

Track:

```text
useful
redundant
obsolete
dominated
unsafe
low-confidence
```

Skills must be versionable and retireable as new policy/physics/evidence improves.

---

# 21. MASTER TODO — PART VIII: CURRICULUM & TEACHER FACTORY

## R22 — Curriculum generator

Progression:

```text
easy
→ medium
→ hard
→ pressure
→ adversarial
```

Difficulty should eventually calibrate from real performance distributions, not hand labels only.

## R23 — Teacher synthesis

Outputs may include:

```text
state → action
state → option
ranking pair
positive target
anti-target
confidence
abstention
provenance
```

Teacher must not fabricate a precise target where evidence/counterfactual score is uncertain.

## R24 — Ranking/preference dataset

Build versioned artifact contract with source lineage, skill family, confidence and ranking context.

---

# 22. MASTER TODO — PART IX: TRAINING ADAPTERS

MIMIR remains independent from training algorithms.

## R25 — Real BC export

Rows should include as needed:

```text
observation
behavior target/action
weight
confidence
provenance
skill family
slice/replay lineage
```

Validate serialization + reload + deterministic manifest.

## R26 — DAgger export

```text
policy state
policy action
teacher correction
teacher confidence
failure reason
skill/event context
```

## R27 — PPO/RL auxiliary export

MIMIR may supply:

```text
auxiliary labels
preference/ranking data
curriculum tasks
skill-conditioned scenarios
failure/novelty samples
```

MIMIR is not itself required to be the PPO trainer.

---

# 23. MASTER TODO — PART X: RUNTIME BRIDGE

Build low-latency packages only after skill/teacher artifacts are validated.

Possible runtime outputs:

```text
skill selector package
fallback option package
emergency recovery package
opponent profile summary
small option library
confidence/abstain gates
```

Rules:

```text
[ ] no huge replay search during match
[ ] no hidden heavyweight counterfactual tree in live tick path
[ ] deterministic bounded latency
[ ] version compatibility checks
[ ] safe fallback if package unsupported/stale
```

---

# 24. MASTER TODO — PART XI: PLAYER / OPPONENT INTELLIGENCE

MIMIR should extract as much useful behavioral information as practical from matches.

## Player profile features

```text
[ ] aggression / pressure tendency
[ ] challenge frequency/timing
[ ] fake-challenge tendency
[ ] boost greed / boost starvation patterns
[ ] possession preference
[ ] shot selection
[ ] clear style
[ ] recovery quality
[ ] kickoff tendencies
[ ] wall/air preference
[ ] risk tolerance
[ ] overcommit frequency
[ ] shadow-defense behavior
[ ] predictability by state
```

## Spatial analysis

```text
[ ] field heatmaps
[ ] boost-pad routing heatmaps
[ ] challenge zones
[ ] shot origin/target maps
[ ] recovery landing zones
[ ] possession transition maps
```

## Predictability model

Approximate/learn:

```text
P(action | state, player_profile)
```

with confidence and calibration.

## Match-level opponent report

Produce compact report usable for offline analysis and later runtime package generation.

---

# 25. MASTER TODO — PART XII: GABRIEL / V1 INTEGRATION

Gabriel is a separate bot project. Do not merge its codebase wholesale into MIMIR.

Integration sequence:

```text
[ ] define rollout/trace schema boundary
[ ] Gabriel collector/adapter emits admitted trace artifacts
[ ] MIMIR ingests Gabriel rollouts
[ ] failure/novelty detector finds weak/new states
[ ] replay/rollout slices become new skill/teacher candidates
[ ] curriculum refreshes
[ ] BC/DAgger/PPO consumers train next policy
[ ] next Gabriel policy produces new rollouts
```

Closed loop:

```text
Policy_N
→ Gabriel rollouts
→ MIMIR novelty/failure mining
→ new skill/teacher/curriculum artifacts
→ training
→ Policy_N+1
```

MIMIR should not depend on Gabriel to boot or parse replays.

---

# 26. MASTER TODO — PART XIII: MASS CORPUS, INDEXING & RESUME

Historical continuity records a full replay corpus around **212,339 replay files (~148 GB)** on the user’s machine. Re-audit actual count before mass processing.

Do not put the full corpus in normal Git.

## Corpus index

Per replay:

```text
path / external identity
size
mtime where relevant
SHA/hash
replay_id
version/build tuple
parse stage/status
last processed version
failure category
artifact pointers
```

## Incremental behavior

```text
[ ] skip unchanged files
[ ] reprocess when parser/artifact schema invalidates cache
[ ] quarantine malformed files
[ ] resumable after crash
[ ] deterministic shard assignment
```

## GitHub execution strategy

Normal GitHub-hosted Actions runners only see checked-in corpus. Full-corpus runs need an explicit execution boundary, for example:

```text
self-hosted Windows GitHub Actions runner on corpus machine
or
versioned external corpus worker/storage adapter triggered/audited through GitHub
```

Do not hardcode `D:\RocketLeague bot\...` paths into core logic.

---

# 27. MASTER TODO — PART XIV: PERFORMANCE & CACHE HIERARCHY

Cache layers may include:

```text
replay bytes identity
parsed structural body
network operation stream
raw state
events
slices
canonical skill seeds
counterfactual rollouts
scores
skills/teachers/exports
```

Requirements:

```text
[ ] content-addressed/versioned keys
[ ] invalidation when parser/schema/config changes
[ ] deterministic serialization
[ ] no stale artifact silently reused
[ ] cache hit/miss metrics
```

Parallelization:

```text
CPU: parsing, state reconstruction, event extraction, independent replay jobs
GPU: only when useful for learned models, embeddings, similarity, batch scoring/policy evaluation
```

Do not GPU-accelerate byte parsing merely because a GPU exists.

---

# 28. MASTER TODO — PART XV: HARDENING, FUZZING & OBSERVABILITY

## Parser robustness

```text
[ ] fuzz header/body/network readers
[ ] truncated-at-every-boundary tests for critical readers
[ ] size/count overflow guards
[ ] pathological list length limits
[ ] invalid UTF/text behavior
[ ] invalid object/stream indices
[ ] impossible version branches
[ ] no panic on untrusted replay bytes
```

## Determinism

```text
[ ] same input/config/code → byte-identical deterministic artifacts where promised
[ ] stable ordering
[ ] stable IDs/hashes
[ ] reproducible manifests
```

## Observability

Metrics/reports should include:

```text
parse stage counts
unsupported version counts
malformed counts
abstain counts
cache hit/miss
runtime per stage
memory per stage
skill generation/retirement counts
teacher confidence distributions
```

## Audit lineage

Every important artifact should trace:

```text
skill/teacher/export
→ counterfactual/scoring evidence
→ slice
→ frame/time
→ replay identity/SHA
→ parser/schema versions
```

---

# 29. MASTER TODO — PART XVI: BENCHMARK / REGRESSION CORPORA

Current `largest_100` is a **size/stress heuristic**, not semantic coverage.

Build separate admitted corpora:

```text
[ ] parser format/version corpus
[ ] malformed/edge-case corpus
[ ] event corpus
[ ] raw-state semantic corpus
[ ] skill-family corpus
[ ] counterfactual/physics corpus
[ ] teacher/export corpus
[ ] rare-mechanic corpus
```

Selection must be explicit and versioned.

---

# 30. MASTER TODO — PART XVII: END-TO-END LOW_BOOST_RECOVERY VERTICAL SLICE

This is the first complete proof that MIMIR is more than infrastructure.

Target path:

```text
real replay
→ native state timeline
→ recovery event candidate
→ ReplaySliceRef
→ canonical low-boost recovery state
→ event/contact graph
→ phase segmentation
→ parameter inference
→ skill seed
→ counterfactual variations
→ feasibility validation
→ scoring/ranking
→ reusable skill-family object
→ curriculum cases
→ teacher labels/anti-targets
→ real BC/DAgger export
```

Definition of vertical-slice done:

```text
[ ] at least several independent real replay examples
[ ] automatic candidate discovery, not hand-fed structs only
[ ] evidence lineage retained
[ ] counterfactual variants demonstrably feasible/invalidated
[ ] teacher output contains confidence/abstain
[ ] exported artifacts reload and verify
[ ] tests cover regression and malformed inputs
```

Then repeat with a distinct family such as a flick/recovery/challenge family to prove the architecture generalizes.

---

# 31. FULL SYSTEM CHECKLIST — ONE-LINE PROGRESS VIEW

Use this section as the quick dashboard. Update statuses after admitted milestones.

Legend:

```text
[x] complete/admitted
[>] active/in progress
[ ] not yet admitted
```

```text
[x] Foundation: Rust workspace/contracts/artifacts/deterministic IDs
[x] Replay header exact admission lane
[x] Body/content/footer structural parsing
[x] Footer lookup materialization
[x] Static network registries / lookup plan R3.13
[x] R3.14 read-only network format audit
[>] R3.14A first frame + first actor oracle evidence
[ ] R3.14B bit-cursor/bounded-int contract
[ ] R3.14C native bit primitive
[ ] R3.14D first actor envelope native reader
[ ] R3.14E differential closure
[ ] R3.15 NewActor payload
[ ] R3.16 existing actor/property envelope
[ ] R3.17 attribute decoder families
[ ] R3.18 complete property loop
[ ] R3.19 actor lifecycle table
[ ] R3.20 complete frame
[ ] R3.21 frame iteration / terminal / trailer
[ ] R3.22 native network decoder lane closure
[ ] R4 raw-state contract
[ ] semantic ball/car/player mapping
[ ] R5 raw-state extraction
[ ] R6 primitive + tactical event extraction
[ ] R7 replay slice engine + control-onset rewind
[ ] R8 canonicalization
[ ] R9 event/contact graph
[ ] R10 phase segmentation
[ ] R11 skill seed extraction
[ ] R12 skill parameter inference
[ ] R13 counterfactual expansion
[ ] R14 feasibility/reachability
[ ] R15 micro-rollout engine
[ ] R16 scoring vector
[ ] R17 observed/counterfactual ranking
[ ] R18 anti-target generation
[ ] R19 skill-family synthesis
[ ] R20 skill dedup/fingerprint
[ ] R21 skill aging/retirement/versioning
[ ] R22 curriculum generation
[ ] R23 teacher factory
[ ] R24 ranking/preference dataset
[ ] R25 BC export
[ ] R26 DAgger export
[ ] R27 PPO/RL auxiliary export
[ ] runtime bridge
[ ] player profiling
[ ] spatial heatmaps
[ ] predictability model
[ ] match-level opponent report
[ ] Gabriel rollout ingestion
[ ] failure/novelty mining
[ ] closed-loop refresh Policy_N → Policy_N+1
[ ] full corpus index
[ ] incremental/resumable processing
[ ] parallel execution
[ ] cache hierarchy / invalidation
[ ] fuzzing / malformed hardening
[ ] observability / metrics
[ ] artifact lineage/audit
[ ] semantically diverse benchmark corpora
[ ] low_boost_recovery end-to-end vertical slice
[ ] second distinct skill-family vertical slice
[ ] final production hardening
[ ] MIMIR final completion gate
```

---

# 32. STOP CONDITIONS — DO NOT “PUSH THROUGH” THESE

Stop capability widening if any occurs:

```text
production-code drift vs expected base
unknown oracle pin
corpus identity mismatch
unexpected changed file
native command non-zero
workflow did not propagate native failure
exact clean SHA not verified
unexplained differential mismatch
ambiguous bit cursor interpretation
unsupported tag/format required to continue
malformed test reveals multiple interpretations
main advanced during publication and clean commit is no longer fast-forward
semantic mapping lacks evidence
counterfactual feasibility is uncertain but code wants to label valid
```

When stopped:

```text
preserve evidence
classify Outcome B/C
write smallest targeted follow-up
update this file if current pass changes
```

Stopping at a truthful boundary is correct engineering.

---

# 33. WHAT MUST NEVER BE DONE

```text
DO NOT wildcard-admit future ReplayVersion/BuildVersion families.
DO NOT use filename/path/hash as parser support predicate.
DO NOT treat Boxcars as MIMIR production decoder.
DO NOT treat static tag lookup as payload decode.
DO NOT use read_bits(width) for bounded actor/stream IDs.
DO NOT classify duplicate actor ID alone as malformed.
DO NOT skip unknown attribute payload size and continue cursor guessing.
DO NOT implement multi-frame before one-frame cursor is exact.
DO NOT jump decoded wire property directly to skill label.
DO NOT call inferred state “decoded.”
DO NOT force a teacher target when confidence is low.
DO NOT put 148 GB corpus in Git.
DO NOT vendor NX-HyperBot/Gabriel/RocketSim wholesale into MIMIR.
DO NOT force-push main for ordinary development.
DO NOT trust green PowerShell Actions without native exit-code handling.
DO NOT mark a pass complete without exact evidence/CI counts.
DO NOT let this master file become stale after milestones.
```

---

# 34. HOW TO UPDATE THIS FILE AFTER EVERY PASS

This is the key rule that makes cross-chat continuity permanent.

After a pass is admitted:

## 34.1 Update Current State Block

Change:

```text
LAST_PRODUCTION_CODE_SHA if production changed
LAST_PRODUCTION_MILESTONE
LAST_COMPLETED_READ_ONLY_AUDIT if applicable
CURRENT_PASS
CURRENT_PASS_TYPE
CURRENT_SUPPORTED_REPLAY_LANE if changed
CURRENT_HARD_STOP
IN_FLIGHT_BRANCH / HEAD
IN_FLIGHT_WORK DONE / NOT DONE
NEXT PASS
```

## 34.2 Update master checklist status

Change only evidence-backed `[ ] → [>] → [x]` states.

Never mark future work complete because scaffolds already existed historically.

## 34.3 Add newly learned invariants

Examples:

```text
version gate
weird trailer
actor lifecycle behavior
coordinate convention
skill canonicalization invariant
simulator discrepancy
```

If a fact matters to future implementation, it belongs in this file.

## 34.4 Update exact next-pass checklist

Replace or rewrite the CURRENT PASS CHECKLIST so a zero-context chat knows the next concrete operations.

## 34.5 Keep old roadmap items

Do not delete future roadmap just because current pass changed. This file must remain sufficient until MIMIR is finished.

## 34.6 Commit policy

Prefer a docs-only continuity commit after production publication/readback.

The continuity commit should not contain Rust/Cargo/test-corpus changes.

---

# 35. HOW A NEW CHAT SHOULD RESUME AN IN-FLIGHT BRANCH

If `IN_FLIGHT_NON_PRODUCTION_BRANCH` is non-empty:

```text
1. fetch branch metadata/head
2. compare branch base with fresh main
3. inspect every changed file
4. determine whether work is evidence-only, implementation, temporary workflow or clean source
5. inspect GitHub Actions runs for the branch/head
6. never assume branch work passed merely because files exist
7. continue the first unchecked item in CURRENT PASS CHECKLIST
8. if main advanced with production changes, recreate/rebase/reconstruct after audit
```

If the branch is stale or gone, reconstruct only from admitted evidence and this file; do not guess missing outputs.

---

# 36. HOW A NEW CHAT SHOULD HANDLE “DEVAM ET”

When user says “devam et”, behavior is:

```text
DO:
- inspect fresh main
- read current state in this file
- inspect active branch
- inspect current GitHub Actions state
- continue execution immediately

DO NOT:
- ask what MIMIR is
- ask which step was next
- restart roadmap from R1
- rely only on prior chat memory
- skip validation because another chat allegedly ran it
```

---

# 37. READY-TO-PASTE NEW CHAT INSTRUCTION

If the user starts a new conversation, this short prompt is sufficient:

> **GitHub’daki `Naveax/MIMIR` reposuna bağlan. Önce root `MIMIR_CONTINUE_HERE.md` dosyasını TAMAMEN oku. Bu dosyayı tek continuity source-of-truth handbook olarak kullan ama fresh `main` source/tests/CI ile doğrula. Current State Block’taki aktif pass ve in-flight branch’ten kaldığımız yerden devam et. Tamamlanmış işleri yeniden yapma, kapalı boundary’leri erken açma, tüm evidence/implementation/test/publication kurallarına uy ve her admitted milestone sonunda aynı master dosyayı güncelle ki bir sonraki chat MIMIR bitene kadar sıfır bağlamla devam edebilsin.**

---

# 38. OPTIONAL SUPPORTING FILES — NOT REQUIRED, ONLY SUPPLEMENTAL

If deeper historical context is needed, optional files include:

```text
docs/continuity/MIMIR_CONTINUITY_STATE.json
docs/continuity/MIMIR_CURRENT_STATE.md
docs/continuity/MIMIR_PASS_PROTOCOL.md
docs/continuity/MIMIR_BOUNDARY_LOCKS.md
docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md
docs/continuity/MIMIR_PROGRESS_LEDGER.md
historical docs/executor artifacts
```

But a new chat must **not need them to understand how to build MIMIR**. This file is deliberately redundant enough to stand alone.

---

# 39. CURRENT ONE-LINE TRUTH

> **MIMIR currently has an evidence-backed production static network lookup plan at R3.13, proven on 3,990,310 supported-corpus attribute updates, but it still has not admitted native actor-envelope bit consumption; R3.14A evidence is in flight on `agent/r3-14a-first-actor-envelope-evidence`, and the project must proceed through the complete roadmap in this file until replay → raw state → event/slice → skill compiler → counterfactual teacher → training/runtime adapters → Gabriel closed loop → scalable corpus intelligence is fully productionized.**

---

# 40. MASTER MAINTENANCE CHECKBOX

At the end of every meaningful MIMIR work session, before handing off:

```text
[ ] Fresh main truth checked.
[ ] Current pass status correct.
[ ] In-flight branch/head correct.
[ ] Completed items have evidence.
[ ] No incomplete item falsely marked complete.
[ ] Newly learned invariants recorded.
[ ] Current hard stop recorded.
[ ] Exact next action obvious to a zero-context chat.
[ ] Future roadmap still present.
[ ] This file alone remains enough to continue MIMIR toward completion.
```

If the last checkbox is false, continuity work is not done.

---

## CHATGPT STORAGE KNOWLEDGE GRAPH

The continuity manual is cross-linked to the sanitized historical/design archive. A future session should use these when reconstructing design history, migration candidates, or claims that predate the current Rust repository:

- [All-sources superbook](MIMIR_ALL_SOURCES_SUPERBOOK.md)
- [Knowledge graph / reading order](MIMIR_KNOWLEDGE_GRAPH.md)
- [Source registry and classification](docs/chatgpt-archive/SOURCE_REGISTRY.md)
- [Cross-source validation matrix](docs/chatgpt-archive/VALIDATION_MATRIX.md)
- [Historical-to-current migration map](docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md)

Do not let a historical snapshot override fresh source/tests. Historical files are evidence, design history, or migration candidates according to their registry classification.


---

## R3.14A OUTCOME A / R3.14B ADMISSION / ACTIVE R3.14C

> **CURRENT OVERRIDE:** This section is newer than earlier R3.14A `current pass` wording in this historical continuation file. Fresh source/tests still outrank this document.

As of the 2026-08-13 R3.14A/R3.14B closure:

```text
production code checkpoint = ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
production milestone        = R3.13 static replay network lookup plan
R3.14 read-only audit       = complete
R3.14A evidence             = OUTCOME A / COMPLETE
R3.14B contract planning    = ADMITTED / COMPLETE
ACTIVE NEXT PASS            = R3.14C native bit cursor + bounded integer primitive implementation
```

R3.14A durable decision:

```text
docs/continuity/MIMIR_R3_14A_DECISION.md
successful evidence head = f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
pinned Boxcars            = c70e77df7af81b436cb545d070bb90c82f562d0b
47 / 47 oracle parse      = PASS
selector manifest SHA256  = 28bd08e2b6a376020cd6e91fc90c1b34f076734cbd6a441d82d33ac047f19c55
artifact ZIP SHA256       = d404437e994fd7d539ea554bd63a456273330340b1d678e635d1bb601440c10b
```

R3.14A exact observed first-envelope cursor across all 47 supported replays:

```text
frame_start               0
f32 time + f32 delta       0..64
actor_present bit          64
actor_id start             65
actor_id end               76
alive bit                  76
new bit                    77
hard stop                  78
```

Current 47-row bounded actor-ID observation:

```text
bound                      2047
low_width                  10
bits_consumed              11
extra discriminator        consumed in 47 / 47
extra discriminator value  0 in 47 / 47
actor_id                   0 in 47 / 47
```

This is evidence, not a native production actor reader.

R3.14B contract:

```text
docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md
```

Active R3.14C exact execution spec:

```text
docs/continuity/MIMIR_R3_14C_EXECUTION_SPEC.md
```

R3.14C may implement only private/internal replay-network bit primitives in `crates/mimir-replay/src/lib.rs` plus focused tests. It must not add an actor-envelope production result, external parser dependency, Cargo dependency, support-lane expansion, actor lifecycle mutation, spawn/property/attribute decoding, multi-actor iteration, or multi-frame iteration.

The first production actor-envelope reader remains R3.14D.


---

## R3.14C PRODUCTION ADMITTED / ACTIVE R3.14D

> **CURRENT OVERRIDE:** This section supersedes earlier R3.14C `ACTIVE` wording in this historical continuation file. Fresh code/tests and exact-SHA evidence still outrank prose.

Current exact state:

```text
main / last production code SHA = bad2db9d5043a7a0087a4fab1d278df5f36c7717
production milestone            = R3.14C — private native network bit cursor + bounded-u32 primitive
R3.14A                          = COMPLETE / Outcome A
R3.14B                          = COMPLETE / contract admitted
R3.14C                          = COMPLETE / PRODUCTION
ACTIVE NEXT PASS                = R3.14D — first actor envelope header native reader
```

R3.14C durable decision:

```text
docs/continuity/MIMIR_R3_14C_DECISION.md
```

R3.14C clean production identity:

```text
pre-pass main              = c42836647673cecc47cc9c89908da1de11d8a222
production SHA             = bad2db9d5043a7a0087a4fab1d278df5f36c7717
source file                = crates/mimir-replay/src/lib.rs
source Git blob            = 3ff6c7823f45126595e7e59f7b5fb50980d8234c
source SHA256              = ac1c2ae2919ad0c5d6d8ea615dd5dac82f4c5e5240f33618ef5e74ef9cb1cb92
clean branch CI            = 31698938025 SUCCESS
published-main CI          = 31699241010 SUCCESS
```

Validation evidence:

```text
focused tests              = 19 PASS
R3.14A actor-id vectors    = 47/47 value match
R3.14A end-bit vectors     = 47/47 match
mimir-replay regression    = PASS
workspace check/test       = PASS
clippy -D warnings         = PASS
corpus verifier            = PASS
knowledge verifier         = PASS
Cargo locked               = PASS
hard-stop source scope     = PASS
```

What R3.14C opened:

```text
private NetworkBitCursor
private LSB-first read_bit/read_bits_le
private canonical read_bounded_u32
atomic truncation/error cursor behavior
```

What R3.14C did NOT open:

```text
actor-envelope production result
actor_present/actor_id/alive/new replay reader
name_id/object/spawn/property/stream/attribute payloads
actor state
multi-actor
multi-frame
raw state/events/skills
```

The exact R3.14D execution spec is:

```text
docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md
```

R3.14D may consume only:

```text
first frame time raw/value
first frame delta raw/value
actor_present
bounded actor_id if present
alive if present
new if alive
STOP
```

Hard stop remains before `name_id` and everything after it. R3.14D implementation is not the 47-replay differential admission; that remains R3.14E.

Repository hygiene note: before R3.14C, stale `Cargo.lock` state was repaired separately at `c42836647673cecc47cc9c89908da1de11d8a222` and `scripts/verify_repo.ps1` now enforces Cargo `--locked`. This is reproducibility maintenance, not replay capability expansion.


---

## R3.14D PRODUCTION ADMITTED / ACTIVE R3.14E

> **CURRENT OVERRIDE:** Fresh source/tests and exact-SHA evidence still outrank prose.

```text
last production code SHA = 7b17cb9033b6c71d476e500380d78402cbb3c56d
production milestone     = R3.14D — first actor envelope header native reader
R3.14D                   = COMPLETE / PRODUCTION
ACTIVE NEXT PASS         = R3.14E — native first-envelope differential audit
```

R3.14D decision: `docs/continuity/MIMIR_R3_14D_DECISION.md`.
R3.14E exact spec: `docs/continuity/MIMIR_R3_14E_EXECUTION_SPEC.md`.

R3.14D production now natively consumes first-frame time/delta through the R3.14C cursor, verifies raw timing bits against the admitted timing preamble, then reads exactly one first actor envelope through `actor_present -> bounded actor_id -> alive -> new` according to branch conditions and stops.

Still closed: `name_id`, object/spawn/property/stream/attribute payloads, second actor/frame, actor state, raw state, events, skills.

R3.14E is evidence-only: compare the native reader against the exact 47-row R3.14A pinned-Boxcars evidence. Production Rust must not change.
---

## R3.14E OUTCOME A ADMITTED / ACTIVE R3.15A

> **CURRENT OVERRIDE:** exact source/tests/evidence remain authoritative over prose.

```text
production code SHA = 7b17cb9033b6c71d476e500380d78402cbb3c56d
R3.14D              = PRODUCTION + 47/47 DIFFERENTIAL ADMISSION
R3.14E              = COMPLETE / OUTCOME A
ACTIVE NEXT PASS    = R3.15A — NewActor branch read-only differential evidence
```

R3.14E evidence run `31705946564`, job `94466421975`, artifact `9183181430` proved exact 47/47 equality for raw time/delta, actor-present/id/alive/new, stop bit, BuildVersion, and structural context with zero mismatch/error and zero production mutation.

R3.15A is evidence-only. Production remains frozen before `name_id` and all NewActor spawn fields.
---

## R3.15A OUTCOME A ADMITTED / ACTIVE R3.15B

```text
production code SHA = 7b17cb9033b6c71d476e500380d78402cbb3c56d
R3.15A              = COMPLETE / OUTCOME A / EVIDENCE-ONLY
ACTIVE NEXT PASS    = R3.15B — NewActor native contract admission
```

R3.15A  run `31708322309`, job `94474438951`, artifact `9184200143` admitted 169,538 NewActor rows across all 47 supported replays with zero oracle errors, zero invalid object IDs, zero static-spawn mismatches, and zero production mutation. Production remains frozen after the first actor `new` bit.
---

## R3.15B CONTRACT ADMITTED / ACTIVE R3.15C

```text
production code SHA = 7b17cb9033b6c71d476e500380d78402cbb3c56d
R3.15B              = ADMITTED / CONTRACT COMPLETE / DOCS-ONLY
ACTIVE NEXT PASS    = R3.15C — first NewActor native reader through spawn trajectory
```

R3.15B changes no production Rust. Read `docs/continuity/MIMIR_R3_15B_DECISION.md` and `docs/continuity/MIMIR_R3_15C_EXECUTION_SPEC.md`. Property decoding, next actor/frame iteration, state, events and skills remain closed.

---

## R3.15C PRODUCTION ADMITTED / ACTIVE R3.15D

```text
production code SHA = bf4bccff82203ed049d33e942681fed07f23beb4
R3.15C              = COMPLETE / PRODUCTION
ACTIVE NEXT PASS    = R3.15D — 47-replay first-NewActor differential audit
```

R3.15C adds one additive first-NewActor reader. The independently admitted R3.14D envelope remains preserved; only `is_new == true` advances through raw signed `name_id`, one opaque bit, raw signed `object_id`, static spawn dispatch, and the selected `None | Location | LocationAndRotation` trajectory. The hard stop is the exact trajectory endpoint. Property bits, another actor/frame, lifecycle state, raw state, events and skills remain closed.

Read `docs/continuity/MIMIR_R3_15C_DECISION.md` and `docs/continuity/MIMIR_R3_15D_EXECUTION_SPEC.md` next.

---

## R3.15D COMPLETE / OUTCOME A / ACTIVE R3.16A

```text
production code SHA = bf4bccff82203ed049d33e942681fed07f23beb4
R3.15D evidence head = 10e5d05383dbc09e19af997e896a825d8d16e3ae
R3.15D outcome       = A / 47 OF 47 EXACT FIRST-NEWACTOR DIFFERENTIAL
ACTIVE NEXT PASS     = R3.16A — existing-actor first-property envelope evidence
```

R3.15D recovered and verified the exact R3.15A artifact, revalidated its 169,538-row parent stream identity, selected exactly one frame-0/actor-0 oracle row for each of the 47 admitted replay identities, verified all 47 replay SHA-256 values, then compared the frozen R3.15C native reader against those 47 rows. All 21 admitted fields/presence flags/bit-stop gates matched 47/47; `identity_error_count=0`, `native_error_count=0`, `mismatch_count=0`, and production/Cargo mutation remained zero.

The 169,538-row parent stream was provenance-verified; **only the 47 selected first-NewActor rows were native-differentially compared in R3.15D**. Property payloads and later runtime layers remain closed. Read `docs/continuity/MIMIR_R3_15D_DECISION.md` and `docs/continuity/MIMIR_R3_16A_EXECUTION_SPEC.md` next.

---

## R3.16A COMPLETE / OUTCOME A / ACTIVE R3.16B

```text
production code SHA = bf4bccff82203ed049d33e942681fed07f23beb4
R3.16A evidence head = 31b858de7d855cbc32501e03282c8db6bf68ecd0
R3.16A final run/job = 31748905111 / 94609885915
R3.16A outcome       = A / 47 OF 47 EXISTING-ACTOR FIRST-PROPERTY ROWS RESOLVED
ACTIVE NEXT PASS     = R3.16B — native existing-actor first-property envelope header implementation
```

R3.16A selected the earliest reproducible `actor_present == true && alive == true && new == false && property_present == true` row for every one of the exact 47 admitted replay identities. All 47 stream IDs resolved through the admitted `ReplayNetworkLookupPlanV1` family; unresolved streams, property-object mismatches, invalid property IDs, oracle errors, payload-start monotonicity failures, differential mismatches, production mutations and Cargo mutations were all zero.

The exact final GitHub Actions job log is the immutable R3.16A receipt surface. It serializes 13 bounded evidence records and ends `R3_16A_RECEIPT_STREAM=PASS`. No separate R3.16A Actions artifact was uploaded or is claimed.

Observed first-property tags were `RigidBody=33`, `ActiveActor=11`, `Byte=1`, `Float=1`, `Int=1`. These are lookup tags only, **not admitted payload decoders**. `prop_id_bits` distribution was `4:7, 5:38, 6:2`; actual canonical bounded stream-ID consumption was `5 bits:11, 6 bits:35, 7 bits:1`, proving again that stream IDs must not be treated as fixed-width reads.

R3.16B may extend only one existing-actor branch through `property_present`, one canonical bounded `stream_id` when present, existing inherited/static lookup resolution, and `payload_start_bit`, then HARD STOP. Attribute payload consumption, second-property/property-loop iteration, lifecycle mutation, later actor/frame iteration, raw state, events, slices, skills, training/runtime/export widening and support-lane expansion remain closed.

Read `docs/continuity/MIMIR_R3_16A_DECISION.md` and `docs/continuity/MIMIR_R3_16B_EXECUTION_SPEC.md` next.

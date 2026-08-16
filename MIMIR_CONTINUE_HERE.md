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
  4adadd185783954c7fb6ad67db14b77b377cdde5

LAST_PRODUCTION_MILESTONE:
  R3.18D — minimal native existing-actor next-property control bit

LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.18C — property-loop terminator/continuation evidence / Outcome A / exact one-bit boundary / 0 mismatch

LAST_COMPLETED_CONTRACT_PASS:
  R3.17N — evidence-supported K4 gameplay-structured contract / Outcome A / 161 exact groups / zero cross-product widening

LAST_COMPLETED_EVIDENCE_PASS:
  R3.18C — property-loop terminator/continuation evidence / Outcome A / 47 terminator + 47 continuation candidates / exact one-bit control / 0 mismatch

CURRENT_PASS:
  R3.18E — production control-bit real-replay differential audit

CURRENT_PASS_TYPE:
  read-only differential audit / compare the published R3.18D one-bit control result against pinned Boxcars on the exact real-replay witness lane

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
  R3.18B composes exactly one existing-actor K1 property through its payload end
  R3.18D is published production at 4adadd185783954c7fb6ad67db14b77b377cdde5 and, only from an already-valid R3.18B first-property result, reads exactly the next property_present bit and stops one bit later
  R3.18E is read-only differential evidence only: compare that published one-bit result with pinned Boxcars on real witnesses; production mutation remains forbidden
  NO second property stream/header/payload, repeated/generalized property loop, K2/K3/K4 wrapper composition, next actor, next frame, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening is admitted
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

R3_18B_PRODUCTION_CLOSURE:
  Outcome A / published production / minimal existing-actor one-property K1 composition
  production SHA/tree: de7a2ba40663bb619ca7bd8654846ce87670d023 / d1889038ca2eaeb8bb0f05e44b811d906f84cf6e
  parent main: f12365b43029f19f3ab1dd889e651f9781b0655e
  lib.rs blob: 478ae5b70514fcff79117b834733849517c48500
  focused test blob: 927e9a2c834115d1c918fa96fb6d0690bd03965e
  implementation run/job: 31942254523 / 95153021330 SUCCESS
  exact clean-candidate validation: 31942696817 / 95154052998 SUCCESS
  published main CI: 31942870294 / 95154460239 SUCCESS
  published-main validator: 31942896666 / 95154519828 SUCCESS
  clean scope: crates/mimir-replay/src/lib.rs + crates/mimir-replay/tests/r3_18b_single_k1_property.rs only
  K1 dispatch: Boolean/Byte/Enum/Float/Int/Int64 only; non-K1 rejects before payload read
  exact one-property stop: header.stop_bit == payload_start_bit and composition.stop_bit == scalar.payload_end_bit
  focused tests: 8/8 PASS including R3.18A-shaped Int=62, poison trailing bits, absent/non-K1/truncation/repeatability
  production/Cargo/fixture/corpus/support/workflow/continuity mutation outside clean scope: 0/0/0/0/0/0/0

R3_18C_EVIDENCE_CLOSURE:
  Outcome A / read-only / production unchanged at de7a2ba40663bb619ca7bd8654846ce87670d023
  canonical evidence base main/tree: f8f6467f2ee652892329f08a3e532b1e1f834fb3 / 9943ee5620091142379763422dc22178b2278fbc
  authority head: a4b71ad43e5cf55c44c9518b24622ce29214acd2
  authority run/job: 31944102614 / 95157425239 SUCCESS
  exact-head normal CI: 31944102575 / 95157425128 SUCCESS
  artifact: 9262820284
  artifact digest: sha256:95e89cb350cc4c274d2b7a53198d78941bef54ff1b3f6a165b2ba9710659ec07
  replay identity + pinned Boxcars parse: 47/47
  loop-control candidate rows: 94 = 47 terminator + 47 continuation
  selected terminator: sample_001 / frame0 / actor60 / object344 / property18 / Float raw=1092616192 / payload [36593,36625) / next bit [36625,36626)=false
  selected continuation: sample_001 / frame0 / actor2 / object98 / property55 / Int=62 / payload [10234,10266) / next bit [10266,10267)=true
  native first-property stop == oracle next property_present start: PASS for both classes
  one-bit value/end exact: PASS for both classes; truncation cursor unchanged: PASS; post-stop poison: PASS; repeatability: PASS
  second stream bits consumed: 0; second payload bits consumed: 0; mismatch count: 0; privacy: PASS
  R3.18B focused regression: 8/8 PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_18D_PRODUCTION_CLOSURE:
  Outcome A / production / exact one-bit after-first-K1-property control only
  previous canonical main: e9f3c4d34ebd84fc9c51431ad4489c4d407b1535
  production SHA/tree: 4adadd185783954c7fb6ad67db14b77b377cdde5 / 67b1969eaff49d2913b88b3921f27b1bd7fe8193
  lib.rs blob: 42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662
  focused R3.18D test blob: 2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b
  implementation run/job: 31945358707 / 95160386174 SUCCESS
  exact clean-candidate validator: 31947511554 / 95165765329 SUCCESS
  published main normal CI: 31947695046 / 95166220676 SUCCESS
  exact published-main validator: 31947722626 / 95166287502 SUCCESS
  exact clean scope: crates/mimir-replay/src/lib.rs + crates/mimir-replay/tests/r3_18d_next_property_control.rs
  source audit: exactly one NetworkBitCursor::read_bit; no read_bits_le/bounded/property-header/scalar/K2/K3/K4 call and no production while/for loop in the new control function
  positive boundary: false terminator + true continuation; aligned + unaligned ends; R3.18C Float terminator + Int=62 continuation shapes
  negatives/invariants: missing next bit fail-closed; malformed first-property boundary rejected; post-control poison has no effect; repeatability exact
  full mimir-replay, workspace check/test/clippy and full repository verifier: PASS
  Cargo/fixture/corpus/support/workflow/continuity changes in clean production commit: 0/0/0/0/0/0
  second property stream/header/payload consumed by the new API: 0/0/0

R3_18E_OPEN_BOUNDARY:
  read-only production differential audit; production Rust mutation forbidden
  exact production under audit: 4adadd185783954c7fb6ad67db14b77b377cdde5
  replay lane: the exact 47 supported replays with the same identity policy used by R3.18C
  pinned oracle: nickbabcock/boxcars@c70e77df7af81b436cb545d070bb90c82f562d0b
  reconstruct the deterministic R3.18C loop-control witness policy: at most one terminator and one continuation witness per replay, yielding the frozen 94-row target when both classes remain present
  for every selected row, run the published R3.18B first-property production decoder and then the published R3.18D control-bit API
  compare first-property stop == oracle next property_present start, control start, boolean value, one-bit end/stop, replay identity and witness context
  require zero native/oracle mismatch and zero second-stream/header/payload bits consumed
  include fail-closed truncation and post-stop poison/repeatability negatives without decoding the second property

R3_18E_HARD_STOP:
  no production source, Cargo, fixture, corpus or support-lane mutation
  no second property stream id, header/tag resolution or payload decode
  no repeated property loop / control-bit chaining in production or audit semantics
  no new K2/K3/K4 composition through the R3.18B wrapper
  no next actor, next frame, lifecycle mutation, raw state, event, replay slice, skill, runtime or export widening

NEXT PASS AFTER R3.18E:
  only after Outcome A and exact production differential parity may a separately scoped read-only second-property-header evidence pass be considered; R3.18E itself does not admit that header or a repeated loop
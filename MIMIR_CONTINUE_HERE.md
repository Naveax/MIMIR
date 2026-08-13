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
  ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa

LAST_PRODUCTION_MILESTONE:
  R3.13 — static replay network lookup plan

LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.14 — first native network bitstream format audit

CURRENT_PASS:
  R3.14A — first frame + first actor envelope differential evidence

CURRENT_PASS_TYPE:
  evidence-only / pinned oracle instrumentation / NO production Rust change

CURRENT_SUPPORTED_REPLAY_LANE:
  47 replays

CHECKED_IN_REPLAY_SET:
  103 total = 3 historical fixtures + largest_100 stress corpus

PINNED_BOXCARS_ORACLE:
  repository: nickbabcock/boxcars
  exact SHA: c70e77df7af81b436cb545d070bb90c82f562d0b

CURRENT_HARD_STOP:
  after first actor envelope fields time/delta/actor_present/actor_id/alive/new
  DO NOT cross into name_id/object_id/spawn/property payload in R3.14A

IN_FLIGHT_NON_PRODUCTION_BRANCH:
  agent/r3-14a-first-actor-envelope-evidence

IN_FLIGHT_BRANCH_HEAD_AT_LAST_SYNC:
  f5713deee1a5a41620be257f07163cb33605c758

IN_FLIGHT_WORK_ALREADY DONE:
  - R3.14A evidence branch created from continuity main.
  - pinned Boxcars SHA recovered and independently confirmed.
  - historical R3.10 probe hard-pins the same Boxcars SHA.
  - supported-lane selection mechanism recovered from R3.13 evidence.
  - tools/r3_14a_selector/Cargo.toml created on evidence branch.
  - tools/r3_14a_selector/src/main.rs created on evidence branch.
  - selector uses MIMIR production header admission + static lookup-plan reader.
  - selector expects exact 103 checked-in inputs and exact 47 supported / 56 unsupported split.

IN_FLIGHT_WORK NOT YET CLAIMED COMPLETE:
  - selector GitHub Actions validation has not yet been recorded here as complete.
  - Boxcars observation-only instrumentation patch not yet admitted.
  - 47/47 first-frame/first-actor evidence rows not yet collected.
  - R3.14A aggregate report not yet admitted.
  - R3.14A Outcome A/B/C not yet chosen.

NEXT PASS IF R3.14A OUTCOME A:
  R3.14B — evidence admission + native bit-cursor / bounded-integer contract
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

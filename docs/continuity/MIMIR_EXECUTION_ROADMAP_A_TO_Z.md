# MIMIR — Execution Roadmap A→Z

**Scope:** from current R3.14C checkpoint to the full MIMIR target architecture
**Policy:** full vision accepted, staged delivery mandatory  
**Current production checkpoint:** R3.13 static network lookup plan  
**Current next pass:** R3.14C native bit cursor + bounded integer primitive implementation

---

# 0. Roadmap usage rules

This is a directional and sequencing document, not permission to implement future phases early.

For every phase:

1. current exact-pass spec wins over this roadmap;
2. boundary locks win over convenience;
3. repository truth wins over stale roadmap text;
4. each phase is decomposed into evidence → admission → implementation → audit → publication;
5. a phase may split into additional passes when evidence reveals new format branches;
6. pass IDs may evolve, but the dependency order should remain unless an explicit design decision changes it.

The roadmap has two zoom levels:

- **Part I:** exact near-term network decoder passes;
- **Part II:** full MIMIR system from raw state to skill/teacher/runtime/mass corpus.

---

# PART I — NATIVE REPLAY NETWORK DECODER

# A. R3.14A — First frame + first actor envelope oracle evidence — COMPLETE / OUTCOME A

Goal:

```text
prove cursor/field order before native bit reader
```

Evidence fields:

```text
time
delta
actor_present
actor_id
alive
new
```

Rules:

- pinned Boxcars only;
- 47 supported replay set exactly;
- production source unchanged;
- bit offsets recorded;
- bounded actor ID consumption characterized;
- stop before `name_id` / spawn / property payload.

Done when:

- 47/47 evidence valid;
- no unexplained cursor divergence;
- Outcome A allows R3.14B.

---

# B. R3.14B — Evidence admission + native bit-cursor contract — COMPLETE / ADMITTED

This pass converts R3.14A facts into a production implementation contract.

Define:

```text
BitCursorV1 semantics
bit ordering within byte
read_bit
read_bits_le / equivalent exact primitive
read_f32 at byte/bit boundary
bounded integer algorithm
EOF/truncation errors
bit-position accounting
maximum bound validation
```

Important questions:

- Is `time/delta` always byte-aligned at frame start?
- Does bounded integer use exactly one optional discriminator path or multiple branches?
- How are zero/one bounds handled?
- What is the exact error on impossible bound/value/cursor exhaustion?

Tests planned before implementation:

```text
synthetic exact bit patterns
boundary values
values around discriminator threshold
truncated low bits
truncated discriminator bit
47 oracle-derived actor-ID vectors
```

No actor lifecycle yet.

---

# C. R3.14C — Native bit cursor + bounded integer primitive implementation — ACTIVE

Production code may now add the minimum generic bit primitives.

Required properties:

- deterministic;
- no allocations in primitive path unless necessary;
- exact cursor offset available for diagnostics/tests;
- fail closed on truncation;
- bounded integer matches oracle vectors;
- no actor semantics in primitive layer.

Focused differential gate:

```text
all R3.14A actor-id vectors
value match = 100%
end-bit match = 100%
```

Do not implement spawn/property payload here.

---

# D. R3.14D — First actor envelope header native reader

Build the smallest production reader using the new cursor:

Output candidate:

```text
ReplayNetworkFirstActorEnvelopeV1 {
  time
  delta
  actor_present
  actor_id: Option<u32>
  alive: Option<bool>
  new: Option<bool>
  stop_bit
}
```

The type name is illustrative; final code should use repo naming conventions.

Hard stop:

```text
before name_id/spawn/property payload
```

Corpus expectations:

- only current production-supported lane;
- unsupported versions remain unsupported;
- no broad header admission.

---

# E. R3.14E — Native first-envelope differential audit

Run MIMIR native reader vs pinned oracle on all 47 supported replays.

Require exact equality for:

```text
time raw bits
 delta raw bits
actor_present
actor_id
alive
new
stop bit offset
```

Any mismatch blocks R3.15.

After success, publish and continuity-sync.

---

# F. R3.15A — NewActor branch read-only evidence

Select first/new-actor occurrences across supported corpus, not only first actor if it is not new.

Instrument oracle for:

```text
new branch start bit
version-gated name_id presence/value/bit range
unnamed one-bit field
object_id bounded/raw decode details
spawn trajectory kind selected from static plan
spawn location payload bit range/value if required
spawn rotation payload bit range/value if required
branch end bit
```

Measure branch distribution:

```text
new actor total
name_id-present family counts
spawn None count
spawn Location count
spawn LocationAndRotation count
object ID range
bit lengths
```

No production change.

---

# G. R3.15B — NewActor contract admission

Decide exact rules for:

- version/build gate controlling name ID;
- meaning/handling of the one-bit field (may stay opaque if semantics unnecessary);
- object ID bounds;
- lookup-plan validation for object ID;
- spawn trajectory dispatch;
- vector/rotation wire formats;
- truncation/malformed conditions.

If location/rotation format requires additional evidence, split before implementation.

---

# H. R3.15C — Native new-actor envelope implementation

Implement only the admitted new-actor branch.

Output should carry raw/typed spawn information without prematurely mapping to canonical car/ball state.

Lifecycle table still not required unless needed to test one branch.

Differentially verify values + end bit.

---

# I. R3.16A — Existing actor first-property envelope evidence

Find actor updates where `new == false`.

Oracle evidence stops after:

```text
property_present
bounded stream_id
resolved property object ID
tag
payload_start_bit
```

Do not consume payload as native production yet.

This validates that production `prop_id_bits` and inherited lookup plan produce the same stream lookup context at the exact bit cursor.

---

# J. R3.16B — Native property-envelope header implementation

Native reader may now consume:

```text
property_present
stream_id bounded integer
lookup resolution to ReplayNetworkResolvedPropertyV1
```

Then stop before payload.

Differential requirements:

```text
stream_id exact
property object exact
tag exact
payload start bit exact
```

---

# K. R3.17 — Attribute decoder family program

Do NOT implement all tags at once.

Prioritize by corpus frequency and semantic value.

Suggested waves:

## K1 Primitive scalar family

```text
Boolean
Byte
Int
Int64
Float
Enum
```

## K2 Object/reference/text family

```text
ActiveActor
String
QWordString
UniqueId
PartyLeader
```

## K3 Spatial/physics family

```text
Location
RigidBody
ReplicatedBoost
PickupNew
```

## K4 Gameplay structured family

```text
CamSettings
TeamPaint
TeamLoadout
ClubColors
Reservation
StatEvent
PlayerHistoryKey
DemolishFx
DemolishExtended
ExtendedExplosion
LoadoutsOnline
```

Each wave:

```text
oracle vectors
wire contract
implementation
malformed tests
differential corpus audit
publication
continuity sync
```

Unknown/NotImplemented stays fail-closed until separately admitted.

---

# L. R3.18 — One complete existing-actor property update

Once enough attribute families exist, decode one full property payload and return exact end cursor.

Then extend to:

```text
property_present loop for one actor update
```

Requirements:

- every encountered property tag in admitted corpus must either be decoded or cause explicit unsupported, not cursor guessing;
- property loop terminator proven;
- end bit matches oracle.

---

# M. R3.19 — Actor lifecycle table

Now introduce stateful actor lifecycle processing.

Define actor state table keyed by actor ID.

Evidence-backed rules must cover:

```text
NewActor on unused ID
NewActor same-class overwrite
NewActor class-changing overwrite
update existing ID
delete existing ID
update missing ID
delete missing ID
```

Known evidence that must be preserved:

```text
same-class NewActor overwrite = valid
141,511 observations
class-changing overwrite = 0 observations
```

Do not classify absent evidence as impossible without explicit policy.

Tests should include same-class overwrite regression.

---

# N. R3.20 — Complete one frame

Decode all actor envelopes for exactly one frame.

Output:

```text
frame time/delta
ordered actor operations
end bit
actor table result after frame
```

Differentially compare operation sequence with oracle.

No second frame until first-frame end cursor is exact.

---

# O. R3.21 — Frame iteration + terminal/trailer handling

Evidence first:

- zero time/delta terminal semantics;
- keyframe/NumFrames relationship;
- supported family trailer behavior;
- post-loop 32-bit trailer gates where applicable;
- exact final network cursor.

Then implement frame loop.

Completion gate:

```text
for each supported replay:
  native frame iteration completes
  expected frame/terminal policy holds
  final bit cursor reconciles with network payload boundary/trailer contract
```

---

# P. R3.22 — Full network decoder audit / lane closure

Before semantic raw state:

- full supported 47 replay native decode;
- no oracle fallback in production;
- deterministic actor-operation output;
- known malformed/truncated cases fail cleanly;
- property tag coverage report;
- performance baseline;
- memory baseline;
- exact oracle differential summary.

Declare a formal **network decoder lane closure**.

Only after this should raw-state semantics become the main active lane.

---

# PART II — RAW STATE AND SEMANTIC REPLAY MODEL

# Q. R4 — Canonical raw-state contract

Design before mapping.

Per frame/timestep target fields:

```text
time / frame identity
ball position
ball linear velocity
ball angular velocity
player/car position
player/car linear velocity
player/car angular velocity
orientation
boost
wheel/contact state
jump state
dodge/flip state if decoded/inferable
team
score
demolition state
last touch / touch ownership if available
kickoff state
confidence / provenance flags
```

Contract rules:

- parser-specific IDs do not leak unnecessarily;
- decoded vs inferred fields distinguished;
- missing fields allowed explicitly where evidence cannot support them;
- schema versioned.

---

# R. R4.x — Semantic class/property mapping

Map network actor/object/property names to semantic entities incrementally.

Suggested order:

1. ball actor identity and rigid body;
2. car/pawn actor identity and rigid body;
3. player replication identity/team;
4. boost amount;
5. score/game state;
6. demolition state;
7. touch/contact references;
8. optional mechanics states.

Each semantic mapping needs real replay examples and cross-checks.

---

# S. R5 — Raw-state extraction implementation

Build frame → canonical raw-state materialization.

Required validation:

- deterministic same replay → same state sequence;
- entity identity stable across lifecycle overwrite/delete;
- impossible NaN/non-finite state handled explicitly;
- coordinate/orientation representation documented;
- sparse updates correctly carry forward state only when protocol semantics justify it.

Do not infer an unchanged property incorrectly if actor replacement reset semantics say otherwise.

---

# T. R6 — Event extraction

Separate **exact decoded** events from **inferred** events.

Initial event families:

```text
ball touch
goal
shot candidate
save candidate
clear
kickoff start/end
demolition
boost pickup
possession transition
challenge start/end
50/50 candidate
wall/ground contact
recovery stable
```

For inferred events store:

```text
confidence
features/reasons
window
version of detector
```

Do not mix inferred labels with protocol-decoded events without provenance.

---

# U. R7 — Replay timeline and slice engine

Build stable temporal windows:

```text
event trigger
→ pre-roll
→ core event
→ post-roll
→ slice
```

Each slice:

```text
source replay identity
start/end frame
start/end time
participants
raw-state sequence
events
context
confidence
provenance
```

Support explicit user-selected replay time windows as future skill-seed input.

---

# V. R8 — Canonicalization

Normalize equivalent situations:

```text
field mirroring
team-normalized attack direction
goal-relative coordinates
player-relative coordinates
ball-relative features
heading/orientation normalization
time normalization
optional surface-relative frames
```

Property tests should verify inverse/round-trip invariants where applicable.

Goal:

```text
same behavior under symmetry → same family representation
```

---

# W. R9 — Event/contact graph

Graph model:

Nodes can include:

```text
pose state
ball state
jump
dodge
wheel contact
ball contact
surface contact
boost burst
goal
challenge
possession transition
recovery stable
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

The graph is used for phase segmentation and transferable skill structure.

---

# X. R10 — Phase segmentation

Split slices into meaningful phases.

Examples:

Recovery:

```text
airborne correction
descent
first contact
stabilization
exit acceleration
```

Flick:

```text
approach
control/capture
setup
jump
contact/dodge
release
follow-through/recovery
```

Store phase-boundary confidence.

---

# Y. R11 — Skill seed extraction

A replay moment becomes a `skill seed`, not a fully learned skill.

Seed should contain:

```text
canonical initial state
context/intention proxy
phase graph
action/control evidence
key contacts
timing
outcome
constraints
confidence
source lineage
```

Rare moments can enter here with low support; they are not immediately stable skills.

---

# Z. R12 — Skill parameter inference

Convert fixed example to parameterized family candidate.

Candidate parameters:

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

Infer ranges/distributions and parameter correlations.

---

# PART III — COUNTERFACTUAL SKILL COMPILER

# AA. R13 — Counterfactual expansion

Generate bounded variations, not brute-force infinite action space.

Variation sources:

```text
state perturbations
timing shifts
approach-angle shifts
boost differences
opponent-position differences
ball velocity/offset differences
primitive action variants
```

Use event-conditioned action grammar and pruning.

---

# AB. R14 — Feasibility / reachability

Every counterfactual must pass physical and control feasibility.

Check:

```text
reachable position/orientation
rotation time
boost budget
contact geometry
collision validity
temporal ordering
surface constraints
```

Output:

```text
valid
invalid
abstain/uncertain
```

Uncertain is not automatically valid.

---

# AC. R15 — Outcome scoring / ranking

Score multi-dimensionally:

```text
possession
opponent beaten
shot threat
defensive safety
recovery quality
boost efficiency
future controllability
robustness
punish risk
overcommit risk
```

Preserve component vector, not only scalar aggregate.

Generate ranking pairs where confidence is sufficient.

---

# AD. R16 — Skill object synthesis

Validated family becomes reusable skill object.

Minimum conceptual fields:

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

---

# AE. R17 — Anti-targets

Generate explicit near-miss/bad-action examples:

```text
early dodge
late dodge
wrong landing orientation
overboost
bad challenge timing
unsafe ball-side approach
panic clear
possession throwaway
```

Use for ranking/preference/DAgger/auxiliary objectives.

---

# AF. R18 — Curriculum generator

For each skill family:

```text
easy deterministic setup
→ low variance
→ medium perturbation
→ adversarial perturbation
→ match context
```

Difficulty adapts from measured success, not fixed mythology.

---

# AG. R19 — Teacher factory

Teacher outputs may include:

```text
action target
trajectory target
phase label
subgoal
ranking pair
anti-target
expected outcome
confidence
abstain
```

Teacher can combine replay evidence, counterfactual search, validated skills, models, and ensembles.

ABSTAIN is a valid output.

---

# PART IV — TRAINING / RUNTIME ADAPTERS

# AH. R20 — BC adapter/export

Transform MIMIR teacher/skill evidence into BC dataset format.

Potential fields:

```text
observation
action
weight
phase
skill_id
confidence
anti-target metadata
lineage
```

MIMIR core remains independent of BC.

---

# AI. R21 — DAgger bridge

Flow:

```text
student rollout state
→ MIMIR teacher query
→ correction / abstain
→ append evidence
→ retrain
```

Track student distribution and confidence.

---

# AJ. R22 — PPO/RL auxiliary adapter

Possible outputs:

```text
skill phase auxiliary targets
curriculum scenarios
reward-shaping proposals
success/failure predicates
teacher hints
```

MIMIR does not become PPO itself.

---

# AK. R23 — Runtime bridge

Runtime flow:

```text
current state
→ applicable skill candidates
→ confidence/risk gate
→ skill/option selection
→ closed-loop controller
→ fallback/base policy
```

Never blindly replay recorded trajectories open-loop.

---

# AL. R24 — Closed-loop refresh

Feed rollout outcomes back:

```text
attempt
→ success/failure
→ failure cluster
→ new coverage
→ teacher refresh
→ curriculum refresh
→ skill update
```

This turns MIMIR into a living system rather than one-time preprocessing.

---

# AM. R25 — Skill library lifecycle

Implement:

```text
deduplication
merge
split
versioning
aging
retirement
revival
coverage statistics
success statistics
novelty memory
```

A library without lifecycle becomes a landfill with JSON formatting.

---

# PART V — LARGE-CORPUS INTELLIGENCE

# AN. R26 — Rare skill mining

Explicitly support rare moments such as:

```text
double wave dash
rare flick
advanced recovery
unusual wall setup
high-value save/recovery sequence
```

Pipeline:

```text
rare slice
→ canonicalize
→ phase segment
→ parameter infer
→ counterfactual expand
→ validate
→ family candidate
```

One example can seed discovery; validation determines transferability.

---

# AO. R27 — 212K+ replay index

Build tiered ingestion:

```text
file discovery
→ identity/hash
→ cheap header parse
→ support/version classification
→ cheap metadata/event candidate filters
→ deep native parse for selected files
→ raw-state/event index
→ slice/skill mining
```

Do not deep-parse all files first merely because storage exists.

---

# AP. R28 — Incremental/resumable mass scan

Requirements:

```text
content-addressed identity
resume checkpoints
deterministic sharding
bounded worker pool
backpressure
failure quarantine
retries by error class
artifact checksums
index versioning
```

A power loss must not turn 200K parsed replays into folklore.

---

# AQ. R29 — Performance and parallelism

Profile before optimizing.

Measure:

```text
header parse throughput
network decode throughput
raw-state materialization throughput
memory per replay
allocation hotspots
string interning benefits
lookup-plan cache effectiveness
I/O bottlenecks
compression/storage costs
```

CPU parallelism first for parser-heavy stages; GPU only where workload justifies it.

---

# AR. R30 — Corpus coverage expansion

Current exact support lane is intentionally narrow.

Expand format families through evidence clusters:

```text
unknown BuildVersion inventory
network version families
property/tag coverage
trailer variations
spawn variations
older/newer replay families
```

Admission remains evidence-backed; do not convert this into a wildcard parser policy without proof.

---

# PART VI — PRODUCTION HARDENING

# AS. R31 — Malformed replay corpus / fuzzing

Build:

```text
truncation corpus
bit flips around section boundaries
invalid counts
invalid indices
unknown tags
broken bounded integers
actor lifecycle anomalies
payload truncation
footer/header mismatches
```

Use fuzz/property tests where appropriate.

---

# AT. R32 — Determinism and reproducibility

Require:

```text
same replay + parser version = same canonical outputs
stable artifact hashes where intended
explicit schema versions
explicit parser/evidence versions
repeatable sharding/order
```

---

# AU. R33 — Observability

Metrics/logging:

```text
replays/sec
frames/sec
actor updates/sec
unsupported families
malformed categories
NotImplemented tag hits
raw-state missing fields
skill mining yields
teacher abstain rate
counterfactual acceptance rate
```

Observability must not change semantics.

---

# AV. R34 — Artifact lineage and migration

Every downstream artifact should be traceable:

```text
skill
→ seed
→ slice
→ event/raw state
→ replay
→ file hash
→ parser version
```

Add schema migration/version policy for long-lived libraries.

---

# AW. R35 — Backup / export / recovery

Production corpora and skill libraries need:

```text
manifested backups
incremental snapshots
index rebuild path
artifact checksum validation
restore drills
```

---

# AX. R36 — End-to-end vertical slice acceptance

Before calling MIMIR practically useful, close at least one complete family:

```text
real replay
→ native parse
→ raw state
→ event/slice
→ canonicalization
→ skill seed
→ counterfactual alternatives
→ validation
→ teacher/skill artifact
→ training/runtime consumer
→ controlled evaluation
→ measurable gain
```

Recommended first family remains something narrow and testable, such as low-boost recovery, with rare-skill demonstration afterward.

---

# AY. R37 — Closed-loop bot integration

Integrate with Gabriel/V1/other consumers only after the vertical slice is proven.

Measure:

```text
task success
catastrophic failure
policy regression
Elo/win rate where appropriate
skill invocation success
teacher correction usefulness
```

Keep MIMIR independent: consumers are adapters.

---

# AZ. R38+ — Continuous intelligence system

Long-term operating loop:

```text
new replay / rollout
→ ingest
→ novelty/failure discovery
→ teacher/skill refresh
→ curriculum update
→ train/runtime update
→ evaluation
→ library merge/retire
→ new rollout
```

At this point MIMIR is no longer just a replay parser project. It is the intended replay intelligence + teacher factory + skill compiler + curriculum + runtime/export system.

---

# Final completion criteria

MIMIR should not be called “complete” because a parser can read every replay.

A strong completion bar is:

- native replay decoding robust across target corpus families;
- canonical raw-state timeline;
- reliable event/slice extraction;
- reusable skill-family synthesis;
- counterfactual validation;
- confidence/abstain;
- curriculum generation;
- at least BC/DAgger/runtime consumers proven;
- closed-loop refresh;
- skill lifecycle management;
- large corpus indexing/resume/performance;
- production observability/recovery;
- measurable task/policy gain on controlled evaluation.

The current project is at the beginning of the native network-bit layer: **R3.14A next**. Do not let the size of the roadmap tempt a future executor into skipping the next six bits.

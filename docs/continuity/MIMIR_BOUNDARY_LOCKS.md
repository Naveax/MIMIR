# MIMIR — Boundary Locks

**Purpose:** keep current capability claims narrow and prevent a future chat from opening several binary/semantic layers at once.

This file is not a wishlist. It is the list of boundaries that are currently **OPEN**, **EVIDENCE-ONLY**, or **CLOSED**.

---

# 0. Current override — R3.18AU production / R3.18AV active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AU
- `6a9f456c78ffccab177823234a8d9fe4ba59a850` / `cbda5db96e88cc208f872c2237cf4741b8fcfaef` is canonical production; parent `7068884bd1982a99ea68647156addc5b381f9613`;
- exact clean-candidate CI `32976370318/98201978533` and published-main CI `32977973145/98207283247` are SUCCESS;
- validates/recomputes one exact published R3.18AQ mixed control;
- false stays a successful no-header terminator with zero post-AQ reads;
- true composes exactly one stateless following header only under exact R3.18AT membership and stops at `payload_start`;
- immutable behavior remains false=7 / true=40; true headers exact 40/40; Int=40; 16 exact contexts.

## CLOSED EVIDENCE — R3.18AS Outcome A
- evidence `475650fea59332f74b9f69da50e3e4471622ab7e` / artifact `9603335255` / `sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45`;
- frozen rows 47/47; false terminators 7/7; true headers exact 40/40; native/oracle mismatch 0;
- unique exact contexts 16; tags Int=40; witness reselection 0; payload/second-control consumption 0/0.

## CLOSED CONTRACT — R3.18AT Outcome A
- contract `docs/continuity/MIMIR_R3_18AT_ADMITTED_HEADER_CONTEXTS.json` / `sha256:3c412a5fdf5ed647fbe2b2e4db1f3adf4e4f578ae07c58a302c261f6abafd0a5`;
- membership `exact_tuple_only`; 16 complete eight-field tuples; exact observed multiplicities sum 40;
- `is_rl_223` is required; all 7 false AQ rows remain outside header membership;
- AJ/Z/P inheritance, tag/component/Cartesian/versionless/RL223-drop-or-flip/fabricated membership are rejected.

## ACTIVE DIFFERENTIAL GATE — R3.18AV
- compare published R3.18AU against exactly the immutable 47-row AS/AT authority;
- require false=7 no-header terminators and true=40 exact one-header results;
- require exact header identity, boundaries, AT context/multiplicity equality, mismatch 0 and witness reselection 0;
- production mutation is forbidden; following payload and second later property-control bit remain unread.

## CLOSED
- any following-header success on the 7 false terminator rows;
- any following-header context outside exact R3.18AT membership;
- following payload after the R3.18AU true header `payload_start`;
- second later property-control bit after R3.18AU;
- repeated/generalized property loop or generic cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

---

# 1. Status vocabulary

## OPEN / PRODUCTION

Implemented in production code and admitted by tests/audit.

## EVIDENCE-ONLY

Observed/proven using structural scanner, corpus analysis, or pinned external oracle, but not yet a production MIMIR capability.

## CLOSED

Must not be implemented or claimed unless an explicit future pass reopens it.

---

# 2. Header / structural replay boundaries

## OPEN / PRODUCTION

- exact-admitted replay header parsing for the current supported lane;
- `ReplayInput::Memory` parsing path used by the admitted minimal readers;
- body structural boundary extraction;
- content scaffold extraction;
- network payload offset/size discovery;
- footer scaffold extraction;
- footer lookup materialization;
- static first-frame timing precondition materialization already present before R3.13;
- static network attribute-tag registry;
- static spawn trajectory registry;
- static network lookup plan construction.

## CLOSED / unchanged unless separately reopened

- broad wildcard BuildVersion support;
- “all ReplayVersion 8” support;
- automatic future-build admission;
- path/hash/filename as parser support predicates;
- CRC validity as a prerequisite for current static plan unless separately admitted;
- external parser as production runtime backend.

---

# 3. Network lookup plan boundary

## OPEN / PRODUCTION — R3.13

Production can derive:

```text
object lookup table
inherited effective stream/property map
max_prop_id
prop_id_bits
spawn trajectory table
channel/build flags admitted by plan
```

Production can use footer objects/net-cache structures to build these tables.

## LOCK

`ReplayNetworkLookupPlanV1` is a **static predecode plan**.

It must not be described as:

```text
frame decoder
actor decoder
attribute decoder
raw-state decoder
```

---

# 4. Native network bit cursor boundary

## EVIDENCE-ADMITTED — R3.14A / CONTRACT-ADMITTED — R3.14B

Known order:

```text
f32 time
f32 delta
actor_present
bounded actor_id
alive
new
```

for the first actor-envelope header, subject to branch conditions.

## CLOSED

Production does not yet have an admitted native reader that consumes this whole envelope.

Reopen condition:

```text
R3.14A differential evidence
→ R3.14B admission/contract
→ R3.14C bit primitive implementation
→ R3.14D envelope reader
→ R3.14E differential audit
```

No shortcut.

---

# 5. Bounded integer boundary

## EVIDENCE-ONLY format rule

Bounded integer is not ordinary fixed width. A value-dependent discriminator bit may be consumed after low bits.

## OPEN FOR NARROW IMPLEMENTATION — R3.14C

R3.14C may implement one canonical private primitive only. Until R3.14C is admitted:

- do not add an ad-hoc actor-ID bit read;
- do not implement stream ID using `read_bits(prop_id_bits)` alone;
- do not implement multiple independent slightly-different bounded-int helpers.

Reopen with one canonical tested primitive shared by actor/channel/property decode paths as appropriate.

---

# 6. First actor envelope boundary

## Current target fields

R3.14A evidence may observe only:

```text
time
delta
actor_present
actor_id
alive
new
```

## HARD STOP

Do not cross into:

```text
name_id
one-bit new-actor field
object_id
spawn trajectory
property_present
stream_id
attribute payload
```

until the relevant follow-up pass explicitly opens it.

---

# 7. NewActor branch boundary

## EVIDENCE-ONLY order

Current format audit says:

```text
if new:
    version-gated name_id
    1 bit
    object_id
    spawn trajectory
```

## CLOSED production decode

The native reader may not consume these fields before R3.15 admission.

Planned reopen:

```text
R3.15A differential evidence
R3.15B implementation planning/reader
R3.15C differential audit if split is needed
```

---

# 8. Existing actor property branch boundary

## EVIDENCE-ONLY order

```text
property_present loop
→ bounded stream_id
→ attribute payload determined through static lookup plan
```

## CLOSED production decode

Do not attempt to iterate an arbitrary number of properties until the reader can correctly stop/skip each payload. A property envelope cannot be safely iterated if the payload size is unknown.

Planned sequence:

```text
first property envelope evidence
→ bounded stream ID primitive validation
→ first attribute family decoders
→ only then broader property-loop iteration
```

---

# 9. Attribute payload boundary

## OPEN / PRODUCTION

Static attribute **tag lookup** exists.

## CLOSED

Wire payload decoding for those tags is not globally admitted.

Do not confuse:

```text
stream ID resolves to ReplayNetworkAttributeTagV1::RigidBody
```

with:

```text
RigidBody payload bits decoded
```

Planned decoder families must be admitted incrementally.

---

# 10. Actor lifecycle boundary

## EVIDENCE-ONLY facts

- same actor ID may be reintroduced with `NewActor`;
- 141,511 same-class overwrites observed;
- zero class-changing overwrites observed in supported evidence;
- pinned Boxcars accepts same-class overwrite behavior.

## LOCKED policy

Never use:

```text
duplicate actor ID => malformed
```

## CLOSED production state table

No full native actor lifecycle state table is admitted yet.

Before opening it, define evidence-backed behavior for:

```text
new unused ID
same-class overwrite
class-changing overwrite
update missing ID
delete missing ID
delete existing ID
```

---

# 11. Frame iteration boundary

## CLOSED

R3.14A/D must not become a hidden multi-frame iterator.

Before full iteration:

- first-frame cursor proven;
- actor envelope proven;
- new actor payload proven;
- existing actor property payload can be consumed safely;
- terminal frame behavior proven;
- version-gated trailer behavior proven.

Only then open multi-frame iteration.

---

# 12. Raw network trailer/end boundary

## EVIDENCE-ONLY

Prior audit indicates version-dependent post-frame trailer behavior exists for newer network versions/builds.

## CLOSED

Do not claim complete network-section consumption until:

- frame loop termination is proven;
- exact trailer conditions are admitted;
- final cursor matches expected network end for corpus.

---

# 13. Semantic actor/property state boundary

## CLOSED

Decoded wire values are not yet canonical gameplay state.

Future semantic mapping must distinguish:

```text
wire attribute
actor property state
entity/class identity
Rocket League semantic field
canonical raw-state field
```

Do not skip these contracts.

---

# 14. Ball/car/player raw-state boundary

## CLOSED

No claim yet that native replay parsing yields canonical:

```text
ball position/velocity/angular velocity
car position/velocity/angular velocity/orientation
boost
wheel contact
jump/dodge state
team/score
touch ownership
demo state
```

These require dedicated raw-state contract and semantic mapping passes after network decoding.

---

# 15. Event extraction boundary

## CLOSED

No native event claims yet for:

```text
touch
shot
goal
save
clear
50/50
kickoff
demo
boost pickup
recovery
possession transition
challenge
```

Event extraction opens only after raw state/event evidence is trustworthy enough.

Exact decoded events and inferred events must remain separately labeled.

---

# 16. Replay slice boundary

## CLOSED

Do not generate production skill slices directly from structural/footer/network-plan data.

Replay slice requires:

```text
usable timeline
raw state
relevant events/context
stable frame/time identity
confidence/provenance
```

---

# 17. Skill pipeline boundaries

All remain CLOSED for the **new native replay path** until upstream contracts exist:

```text
canonicalization
event/contact graph
phase segmentation
skill seed extraction
skill parameter inference
counterfactual expansion
feasibility/reachability validation
skill synthesis
anti-target generation
curriculum generation
teacher synthesis
```

Existing scaffold/contracts elsewhere in the repo do not equal a completed native replay-to-skill vertical slice.

---

# 18. Training adapters

## Existing contract/scaffold history

MIMIR contains extensive historical BC/export/teacher/scaffold work.

## LOCK

Do not wire newly decoded replay network values into BC/DAgger/PPO runtime/export merely because those consumer surfaces exist.

A new native replay-derived artifact must pass the full upstream lineage:

```text
network decode
→ raw state
→ event/slice
→ skill/teacher artifact
→ adapter
```

---

# 19. Runtime bridge

## CLOSED for native replay-derived decisions

No direct “decoded replay actor update → runtime action” path.

Runtime bridge will consume validated skill/option outputs, not replay packets blindly.

---

# 20. Full 212K+ corpus boundary

## CLOSED for deep native parse

The checked-in stress corpus and current 47 supported replay lane are development evidence.

Do not launch deep parsing of 212K+ replays before:

- parser format coverage strategy exists;
- failure quarantine exists;
- deterministic indexing/resume exists;
- performance profiling exists;
- parser crash/malformed behavior is hardened.

Mass scan should initially be tiered, with cheap identity/header filtering before deep decode.

---

# 21. Reopen protocol

A CLOSED boundary opens only through an explicit pass containing:

```text
evidence
scope
accepted forms
rejected forms
error taxonomy
implementation plan
focused tests
corpus regression
audit
publication
continuity sync
```

A future chat must not reopen a boundary merely because it is “the obvious next step.”

---

# 22. Current immediate lock summary

At R3.14C:

```text
OPEN / PRODUCTION:
  R3.13 static network lookup plan and earlier structural layers

EVIDENCE-ADMITTED:
  R3.14A first-frame / first-actor envelope order through new
  bounded actor-ID discriminator behavior

OPEN FOR IMPLEMENTATION NOW:
  one private LSB-first network bit cursor
  one private canonical bounded-u32 primitive
  focused primitive tests

CLOSED:
  public/native actor-envelope result reader until R3.14D
  name_id and everything after new
  actor lifecycle mutation
  multi-actor
  multi-frame
  attribute payload decode
  raw state
  events
  skills
```

That is the current hard boundary. R3.14C primitive implementation is not permission to decode the first actor envelope.


---

## CURRENT OVERRIDE — At R3.14D

R3.14C is now OPEN / PRODUCTION at `bad2db9d5043a7a0087a4fab1d278df5f36c7717` for only:

```text
private LSB-first NetworkBitCursor
private read_bit / read_bits_le
private canonical bounded-u32 primitive
```

R3.14D is the active narrow implementation boundary:

```text
first frame time + delta
first actor_present
bounded actor_id if present
alive if present
new if alive
STOP
```

Still CLOSED:

```text
name_id
post-name one-bit field
object_id
spawn payload
property_present loop
stream_id production path
attribute payload
second actor
second frame
actor lifecycle mutation
raw state
events
skills
```

R3.14D implementation does not by itself close the oracle differential requirement. `R3.14E` remains required before R3.15.


---

## CURRENT OVERRIDE — At R3.14E

OPEN / PRODUCTION at `7b17cb9033b6c71d476e500380d78402cbb3c56d`:
```text
private native bit primitives
first frame timing raw/value native consumption
one first actor envelope: actor_present -> bounded actor_id -> alive -> new, branch-dependent
```

R3.14E is EVIDENCE-ONLY differential audit. Production source remains frozen.

Still CLOSED: `name_id`, post-name bit, object/spawn/property/stream/attribute payloads, second actor/frame, actor state, raw state, events, skills.
---

## CURRENT OVERRIDE — At R3.15A

OPEN / ADMITTED:

```text
R3.14D first actor envelope through new
R3.14E 47/47 differential admission
static object-index spawn-kind lookup plan
```

R3.15A is EVIDENCE-ONLY. It may instrument pinned Boxcars through one NewActor spawn trajectory and compare static spawn-kind selection. Production decoding remains CLOSED for `name_id`, opaque post-new bit, `object_id`, location/rotation spawn payloads, properties, actor/frame iteration, state, events, and skills.


---

## CURRENT OVERRIDE — R3.18M PRODUCTION / R3.18N ACTIVE

Fresh source/tests and exact-SHA evidence override older current-like sections above.

```text
OPEN / PRODUCTION:
  R3.18M at fd74ba8c520ab83b808730572c41e45d6dc616e6
  from one valid R3.18J second-payload result, validate exact prior payload end
  read exactly one following property_present bit
  admit true only; false fails closed
  stop exactly one bit later

ACTIVE EVIDENCE:
  R3.18N published-R3.18M differential on exact frozen R3.18L 47-row lane

CLOSED:
  false following-control production context
  following stream/header/payload
  another control bit
  repeated/generalized property loop
  next actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export widening
```

## R3.18Q following-property header production lock

- Production SHA/tree: `f41c59d26ed6c810a640b4fa8cd76129decb32aa` / `606db4b5778e5218f2bd0117cc5dd72d7f3e37a5`.
- Exact R3.18P contract: `0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b`; membership is the full seven-field tuple only.
- From one valid R3.18J second payload, R3.18Q reuses R3.18M true control and decodes exactly one stateless following header.
- Exact stop is the following header `payload_start`; following-payload bits consumed `0`; another-control bits consumed `0`.
- Frozen authority result: 47/47 Q rows exact, 47/47 R3.18M control equality, 47/47 stateless-header equality.
- No tag-only/component-only/Cartesian/versionless widening, no repeated/generalized property loop/cursor.

## R3.18R active differential hard stop

- Read-only audit of published R3.18Q on the immutable R3.18O 47-row lane.
- Production/Cargo/fixture/corpus/support mutation is forbidden.
- Following payload, another `property_present`, loop/cursor, actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export widening is forbidden.
- Outcome A may only open a later separate payload evidence/contract pass; it does not itself admit payload.


## R3.18R evidence closure / R3.18S active payload lock

- R3.18R read-only authority `32044430149/95429267025` and same-head CI `32044430126/95429266690` are SUCCESS on `47bf441f2c795702e4ee75c66b4dbe710ccc9a9c`.
- Artifact `9292549978` / `18820` bytes / `sha256:142a2480f38a7ddc4f74e73dd9ce84ed70ccd740645f05d2e90579825927220f` is canonical; published Q/header/control equality is 47/47 with 18 exact contexts and mismatch 0.
- R3.18S may inspect one following payload from each frozen `payload_start` through one independently proven payload end only.
- Boolean and ActiveActor are separate evidence classes. No payload production API, another `property_present`, loop/cursor, next actor/frame or semantic/runtime widening is open.


## R3.18S evidence closure / R3.18T active production lock

- R3.18S authority `32047433925/95438466699` and same-head CI `32047433876/95438466663` are SUCCESS on `7fed9a90d2cb1e356b2a388503650b434d7f3f87`.
- Artifact `9293436309` / `18955` bytes / `sha256:dac07647e288bfc3b177000e1bfa6b9cfd892b80fd77d46c2f4974a3832cf422` is canonical evidence; 47/47 one-payload exact, 18 contexts, Boolean 39×1 bit, ActiveActor 8×33 bits, mismatch 0.
- R3.18T may publish only one exact admitted following payload after R3.18Q and must stop at payload end.
- Another `property_present`, another header/payload, loop/cursor, context widening, actor/frame or semantic/runtime widening is not open.


## R3.18T production closure / R3.18U active differential lock

- Production `c2765ab9f04f9c981a6868cb6503bdf0e339ce1b` / tree `a6f27fe606cd3446da02ef1cb8cf53fff071e383`; lib/test blobs `cf992670b461e9d923e773ed375bef2b42aea20d` / `430676ec118fa0755a9c64abc0067bf5c5c88d05`.
- Implementation `32049639448/95445637593`, candidate CI `32049893219/95446478223`, PR CI `32050205389/95447503058`, published CI `32050650336/95448937493` are SUCCESS.
- Production decodes exactly one R3.18S-admitted Boolean|ActiveActor payload and stops at payload end.
- R3.18U may only validate that published boundary on the frozen 47-row lane. Another `property_present`, another header/payload, loop/cursor, context widening or actor/frame/runtime widening is not open.

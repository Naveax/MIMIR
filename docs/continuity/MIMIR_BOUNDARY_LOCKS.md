# MIMIR — Boundary Locks

**Purpose:** keep current capability claims narrow and prevent a future chat from opening several binary/semantic layers at once.

This file is not a wishlist. It is the list of boundaries that are currently **OPEN**, **EVIDENCE-ONLY**, or **CLOSED**.

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

## EVIDENCE-ONLY — current R3.14/R3.14A work

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

## CLOSED production general primitive

Until R3.14B/C:

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

At R3.14A:

```text
OPEN:
  static network lookup plan

EVIDENCE TARGET:
  first frame time/delta
  first actor_present
  actor_id bounded decode
  alive
  new

CLOSED:
  everything after new
  multi-actor
  multi-frame
  actor state mutation
  attributes
  raw state
  events
  skills
```

That is the current hard boundary.

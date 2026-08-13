# MIMIR — Progress Ledger

**Policy:** append-only milestone ledger.  
Do not rewrite old entries to make history prettier. If an earlier entry is later found wrong, append a correction entry.

---

# How to append a milestone

Use this template:

```text
## YYYY-MM-DD — PASS_ID — TITLE
Production base SHA:
Production commit SHA:
Pass type:
Outcome:

What changed:
- ...

Evidence:
- ...

Validation:
- ...

Boundaries opened:
- ...

Boundaries still closed:
- ...

Important negative facts / anti-regressions:
- ...

Next exact pass:
- ...
```

A docs-only continuity sync commit is not a production milestone; it may be mentioned under the milestone it documents.

---

# Condensed historical baseline

The detailed historical record remains in existing `docs/` and `executor_*` artifacts. This ledger intentionally starts with a condensed continuity baseline rather than duplicating hundreds of old pass files.

## Historical replay-header foundation

MIMIR progressed from an explicit unsupported replay-reader boundary into narrow real replay parsing through evidence-driven exact version/build admission.

Important retained principles:

- no fake `ReplayHeader` success;
- exact support before broad wildcard support;
- `ReplayInput::Memory` as the narrow parser carrier;
- structural evidence separated from parser success;
- malformed/error boundaries tested;
- header/body/network layers opened in separate passes.

The old fixture_001/002/003 implementation plans/checklists are historical now, not the active `next` state.

---

# Replay body/footer/static-network progression

Before R3.13, production progressively admitted:

```text
ReplayBodyBoundaryV1
ReplayContentScaffoldV1
ReplayFooterScaffoldV1
ReplayFooterLookupMaterializationV1
ReplayNetworkTimingPreambleV1
ReplayNetworkAttributeTagV1
ReplayNetworkSpawnTrajectoryV1
```

Key evidence from that progression included:

- checked-in body framing matching corpus structure;
- content scaffold through network payload;
- footer structure through known footer sections;
- observed opaque terminal tail forms;
- raw footer object/name/class-index/net-cache materialization;
- first network timing/precondition evidence;
- conservative attribute tag admission.

These milestones established prerequisites but did not constitute a native network frame decoder.

---

# 2026-08-13 continuity checkpoint — R3.13

## R3.13 — Static replay network lookup plan

**Production commit SHA:** `ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa`  
**Commit message:** `Add replay network lookup plan`  
**Pass type:** production implementation + differential audit + publication  
**Outcome:** closed / production

### What changed

Production added a static network-decoder lookup plan derived from already-admitted header/footer structure.

The plan includes:

- `ReplayNetworkResolvedPropertyV1`;
- `ReplayNetworkObjectLookupV1`;
- `ReplayNetworkLookupPlanV1`;
- object-index lookup table;
- effective inherited stream/property mapping;
- `max_prop_id`;
- `prop_id_bits`;
- separate spawn trajectory table;
- channel/build-derived flags required by later decoder stages.

### Critical negative fact

R3.13 does **not** consume actor/frame network payload bits.

It is static preparation for later decoding.

### Differential evidence

Supported replay lane:

```text
47 replays
```

Attribute update oracle comparison:

```text
3,990,310 / 3,990,310 matched
unresolved_stream = 0
property_object_mismatch = 0
decoded_not_implemented_hits = 0
```

Interpretation:

MIMIR's production registry/hierarchy resolves the same property object IDs as the pinned Boxcars oracle for every checked supported-corpus attribute update.

### Actor lifecycle finding discovered in differential work

Repeated `NewActor` on an already-used actor ID is not automatically malformed.

Observed:

```text
same actor ID, same class overwrite = 141,511
same actor ID, different class overwrite = 0
```

Pinned Boxcars explicitly permits the same-class overwrite behavior.

Anti-regression rule:

```text
DO NOT implement duplicate actor ID => malformed
```

### Boundaries opened

- static per-object network lookup plan;
- inherited stream/property resolution;
- per-object bounded property-ID parameters;
- static spawn trajectory lookup;
- decoder prerequisite flags.

### Boundaries still closed

- native actor bits;
- native frame iteration;
- spawn payload decode;
- property payload decode;
- attribute payload decode;
- actor lifecycle state table;
- raw state;
- events;
- replay-to-skill path.

### Next

Read-only R3.14 format audit.

---

# 2026-08-13 continuity checkpoint — R3.14

## R3.14 — Native bitstream order read-only audit

**Pass type:** read-only format audit  
**Production source changed:** no  
**Outcome:** sufficient to plan R3.14A

### Exact order established

```text
frame:
  f32 time
  f32 delta

  actor_present bit
  if actor_present:
      bounded actor_id
      alive bit

      if !alive:
          delete

      if alive:
          new bit

          if new:
              version-gated name_id
              1 bit
              object_id
              spawn trajectory
          else:
              property_present bit loop
              bounded stream_id
              attribute payload
```

### Critical bounded integer finding

Actor ID and stream ID use Rocket League's bounded-integer behavior, not a plain constant-width integer read.

Low bits may be followed by a value-dependent discriminator bit. Cursor correctness must therefore be proven before a native envelope reader is trusted.

### Decision

Do not implement the full frame/actor decoder.

Next exact pass:

```text
R3.14A — temporarily instrument pinned Boxcars and collect first-frame + first-actor-envelope-header differential evidence over all 47 supported replays.
```

Evidence stop boundary:

```text
time
delta
actor_present
actor_id
alive
new
STOP
```

---

# Next ledger entry placeholder

## R3.14A — First frame + first actor envelope differential evidence

Status: **NOT YET COMPLETED** at continuity bootstrap.

When completed, append a new dated entry below this line with:

- MIMIR base SHA;
- exact oracle SHA;
- exact 47 replay manifest identity;
- time/delta evidence counts;
- actor_present distribution;
- actor_id bit-consumption range;
- alive/new distribution;
- mismatch/error counts;
- Outcome A/B/C;
- next exact pass.

Do not edit the R3.13/R3.14 entries to smuggle R3.14A results into history.

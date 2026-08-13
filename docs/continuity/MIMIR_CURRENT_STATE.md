# MIMIR — Current Canonical State

**Continuity date:** 2026-08-13  
**Repository:** `Naveax/MIMIR`  
**Production code checkpoint:** `7b17cb9033b6c71d476e500380d78402cbb3c56d`
**Production milestone:** `R3.14D — first actor envelope header native reader`
**Completed read-only format audit:** `R3.14`  
**Next exact pass:** `R3.14E — native first-envelope differential audit`

---

# 1. How to interpret this document

This document describes **what MIMIR can truthfully claim right now**.

It deliberately distinguishes:

```text
external/oracle evidence
production structural parsing
production lookup/materialization
native network-bit decoding
semantic raw-state extraction
```

These are not interchangeable.

If this file and current Rust code disagree, current repository code/tests win and continuity must be repaired before capability widening.

---

# 2. What is already production reality

The replay ingestion lane has advanced far beyond the old three-header-fixture stage.

Production currently contains narrow, auditable layers for:

1. exact-admitted replay header parsing;
2. replay body structural boundary discovery;
3. content scaffold discovery through the raw network payload;
4. footer scaffold discovery;
5. footer lookup materialization;
6. first-frame timing preamble / header-derived decoder preconditions;
7. conservative network attribute tag registry;
8. spawn-trajectory registry;
9. static network lookup-plan construction.

The R3.13 commit added the static network lookup plan. The plan is derived without consuming network payload bits.

Current code-level concepts include:

```text
ReplayHeader
ReplayBodyBoundaryV1
ReplayContentScaffoldV1
ReplayFooterScaffoldV1
ReplayFooterLookupMaterializationV1
ReplayNetworkTimingPreambleV1
ReplayNetworkAttributeTagV1
ReplayNetworkSpawnTrajectoryV1
ReplayNetworkResolvedPropertyV1
ReplayNetworkObjectLookupV1
ReplayNetworkLookupPlanV1
```

The exact symbol set may grow later; this list records the R3.13 continuity surface.

---

# 3. R3.13 — exact production meaning

R3.13 does **not** mean “network replay decoder exists.”

It means MIMIR can prepare the static lookup information required by a future native decoder before actor/frame payload bits are consumed.

Per replay the plan now carries:

- admitted `ReplayHeader`;
- footer lookup materialization;
- `NumFrames`;
- `MaxChannels`;
- derived channel bit-width information;
- build/match-derived flags already admitted by the pass;
- separate spawn-trajectory lookup table;
- per-object effective inherited property lookup;
- per-object `max_prop_id`;
- per-object `prop_id_bits`;
- stream ID → property object/tag information through the effective object lookup.

The implementation intentionally keeps spawn-trajectory semantics separate from object cache availability.

The implementation intentionally preserves fail-closed boundaries for attribute tags that are not admitted.

---

# 4. R3.13 differential evidence

The production registry/hierarchy was differentially checked against the pinned Boxcars oracle over the supported replay corpus.

Recorded result:

```text
supported replays                    = 47
attribute updates checked            = 3,990,310
attribute updates matched            = 3,990,310
unresolved_stream                    = 0
property_object_mismatch             = 0
decoded_not_implemented_hits         = 0
```

Interpretation:

- for every checked attribute update, production stream/property lookup resolved to the same property object ID as the pinned oracle;
- there was no unresolved stream in the admitted supported lane;
- there was no mismatch between MIMIR's production property-object resolution and oracle output;
- no update that the oracle successfully decoded landed on MIMIR's explicit `NotImplemented` tag boundary.

This evidence validates the **static lookup plan**, not native attribute-bit decoding.

---

# 5. Actor lifecycle evidence that must not be forgotten

A major format fact was established while auditing actor lifecycle behavior.

The same actor ID may receive another `NewActor` event later.

Observed supported-corpus result:

```text
same actor ID + NewActor + same class overwrite = 141,511
same actor ID + NewActor + class changed         = 0
```

Pinned Boxcars treats the same-class overwrite behavior as normal.

Therefore future native decoder logic MUST NOT contain a rule equivalent to:

```text
if actor_id already exists:
    malformed
```

The correct future lifecycle policy must distinguish at least:

```text
new actor on unused ID
same-class NewActor overwrite / replacement
class-changing overwrite
update existing actor
delete actor
update/delete missing actor
```

Only evidence-backed policy may decide which of these are malformed.

Current admitted evidence says **duplicate actor ID alone is not malformed**.

---

# 6. R3.14 read-only format audit

R3.14 did not modify production code.

It established the exact high-level order for the first native actor/frame bitstream layer:

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

The ordering above is the current planning surface. It is not permission to implement all of it at once.

---

# 7. Critical bounded-integer format fact

The native decoder must not implement actor IDs or stream IDs as an ordinary fixed-width read.

The admitted format fact is:

> Bounded integer decoding reads low bits according to the bound and may consume an additional discriminator bit depending on the decoded value and the bound.

Consequences:

- `actor_id` decoding must use the exact bounded-integer algorithm;
- `stream_id` decoding must use the exact bounded-integer algorithm;
- precomputed widths such as `channel_bits` / `prop_id_bits` are inputs to the algorithm, not permission to simply `read_bits(width)` and stop;
- bit cursor position must be differentially verified, because one missed discriminator bit corrupts every later field.

This is one of the primary reasons R3.14A is evidence-only before a native reader is admitted.

---

# 8. What production still does NOT do

The following capabilities are still closed:

```text
native actor_present bit consumption as an admitted production reader
native actor_id bounded-int consumption
native actor alive/new envelope parsing
native name_id parsing
native new-actor object payload parsing
native spawn trajectory payload parsing
native existing-actor property loop parsing
native stream_id bounded-int consumption
native attribute payload decoding
actor lifecycle state-table mutation from network bits
multi-actor iteration
multi-frame iteration
end-of-network/trailer handling as a complete native decoder
raw-state extraction
semantic ball/car/player state materialization
event extraction
replay slice extraction
skill mining from native replay state
counterfactual simulation from native replay state
```

R3.13 static tables and R3.14 format knowledge must not be described as these capabilities.

---

# 9. Current supported corpus meaning

Current continuity records **47 supported replays** for the production admission lane used by R3.13 differential work.

“Supported” here means the replay satisfies the currently admitted production header/structural/lookup-plan lane required for the R3.13 evidence.

It does not imply all 100 checked-in stress replays are production-supported by the same header/version lane.

Any future support expansion must be a separate explicit admission pass. The native network decoder must not silently become an excuse to broaden header BuildVersion support.

---

# 10. Current next pass: R3.14A

R3.14A is **evidence-only**.

Goal:

> Differentially prove the first frame timing fields and first actor-envelope header bit cursor against the already pinned Boxcars oracle across all 47 supported replays before implementing the native reader.

Fields admitted for evidence in this pass:

```text
first_frame.time
first_frame.delta
first_actor.actor_present
first_actor.actor_id      if actor_present
first_actor.alive         if actor_present
first_actor.new           if actor_present && alive
```

Hard stop boundary:

```text
name_id
unnamed one-bit field after name_id
object_id
spawn trajectory payload
property_present loop
stream_id
attribute payload
next actor
next frame
raw state
```

Production Rust source must not change during R3.14A.

---

# 11. Pinned Boxcars oracle rule

R3.14A must use the **already pinned Boxcars revision** associated with the differential work.

Do NOT:

- pull “latest” Boxcars and silently treat it as the oracle;
- change the oracle revision during the evidence pass;
- add Boxcars as a production dependency;
- copy broad decoder code into MIMIR before admission;
- mutate the oracle and then forget to record exactly what instrumentation changed.

If the exact pin cannot be recovered from repository history/artifacts/current evidence scripts, the pass outcome is:

```text
BLOCKED: ORACLE PIN NOT PROVEN
```

Then first create a pin-recovery evidence artifact. Do not invent a new pin merely to keep moving.

---

# 12. Production code discipline inherited from prior passes

Prior passes exposed several process failures that are now permanent lessons.

## 12.1 PowerShell native exit codes

A GitHub Actions step can appear green even if a native `cargo` command failed when PowerShell does not propagate the native exit code.

Therefore every temporary PowerShell workflow/script that invokes native tools must check `$LASTEXITCODE` or use another explicit fail-fast mechanism.

A green Actions job without native-command fail-fast is not accepted evidence.

## 12.2 Temporary workflows

Temporary patch/evidence workflows may live on disposable branches.

They must not enter the clean production source commit.

## 12.3 Clean reconstruction

After focused validation, production source changes are reconstructed onto fresh `main` ancestry using only the verified source blobs/files.

The clean commit must be audited before publication.

## 12.4 Publication

Publication is force-free:

```text
fresh main
→ compare ancestry
→ require expected ahead/behind relation
→ update main with force=false
→ validate exact published main SHA
```

---

# 13. What a future chat must do first

A new chat must NOT start coding immediately.

First:

```text
1. fetch fresh origin/main
2. record main SHA
3. inspect latest commits since last_production_code_sha
4. confirm whether newer commits are docs-only continuity sync or production code
5. read continuity JSON/current-state/exact-pass spec
6. inspect crates/mimir-replay/src/lib.rs around the active network layer
7. inspect relevant current tests
8. locate the exact pinned Boxcars oracle revision/evidence tooling
9. confirm 47-replay supported corpus definition
10. only then execute R3.14A
```

If a newer production milestone exists, stop following R3.14A and repair the continuity control plane from repository truth.

---

# 14. Near-term intended sequence after R3.14A

Subject to evidence outcome:

```text
R3.14A  oracle evidence: first frame + first actor envelope header
R3.14B  evidence admission + native bit-cursor/bounded-int contract planning
R3.14C  native bit cursor + bounded integer primitive implementation
R3.14D  first actor envelope header native reader implementation
R3.14E  47-replay differential audit of native first actor envelope
R3.15A  new-actor spawn header/trajectory evidence
R3.15B  narrow native new-actor spawn envelope implementation
R3.16A  existing-actor first-property envelope evidence
R3.16B  narrow native property-envelope implementation
R3.17+  incremental attribute payload decoders by admitted tag family
```

Do not skip directly from R3.14A to “full frame decoder.”

---

# 15. Long-term system direction

Once the native replay network layer is genuinely complete, the broader MIMIR sequence remains:

```text
network decode
→ actor lifecycle reconstruction
→ canonical raw-state contract
→ ball/car/player semantic extraction
→ event extraction
→ replay slicing
→ canonicalization
→ event/contact graph
→ phase segmentation
→ skill seed extraction
→ parameter inference
→ counterfactual expansion
→ feasibility/reachability validation
→ reusable skill synthesis
→ anti-target generation
→ curriculum generation
→ teacher factory
→ BC/DAgger/PPO adapters
→ runtime bridge
→ closed-loop refresh
→ skill lifecycle management
→ rare-skill mining
→ 212K+ replay indexing/mass scan
→ performance/parallelism
→ production hardening
```

The exact pass decomposition is in `MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`.

---

# 16. Current one-line truth

> **MIMIR has a production static network lookup plan proven against 3,990,310 supported-corpus attribute updates, but it still has not admitted native actor-envelope bit consumption; the next correct step is R3.14A differential evidence for the first frame and first actor envelope header only.**


---

# 17. R3.14A Outcome A + R3.14B admission update

R3.14A is complete with **Outcome A — evidence sufficient**.

Durable decision:

```text
docs/continuity/MIMIR_R3_14A_DECISION.md
```

Exact evidence identity:

```text
production code SHA        = ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa
evidence head              = f1c4eedb6a7e4d96577d2c0a429cbe8b170aa9a1
Boxcars SHA                = c70e77df7af81b436cb545d070bb90c82f562d0b
supported replays          = 47 / 47
oracle decode success      = 47 / 47
schema errors              = 0
bit monotonicity failures  = 0
production source mutation = 0
```

The first-envelope evidence consistently stopped at bit 78 after `new`. No `name_id`, object/spawn, property, stream, attribute, second-actor, second-frame, raw-state, event, or skill boundary was admitted.

R3.14B converted that evidence into the narrow native primitive contract and is complete:

```text
docs/continuity/MIMIR_R3_14B_EXECUTION_SPEC.md
```

Current exact pass:

```text
R3.14C — native bit cursor + bounded integer primitive implementation
spec: docs/continuity/MIMIR_R3_14C_EXECUTION_SPEC.md
```

R3.14C opens only the private primitive implementation boundary. The production actor-envelope reader remains closed until R3.14D.

Current one-line truth after this admission:

> **MIMIR still has R3.13 as its last production replay capability. R3.14A has proven the first-frame/first-actor cursor over all 47 supported replays, R3.14B has admitted the private native bit-cursor/bounded-int contract, and the next correct production pass is R3.14C primitive implementation only.**


---

# 18. R3.14C production admission / R3.14D active

R3.14C is now a production milestone at:

```text
bad2db9d5043a7a0087a4fab1d278df5f36c7717
```

Production now contains one private/internal LSB-first network bit cursor and one canonical bounded-u32 decoder with atomic failure behavior. The primitive passed 19 focused tests and all 47 R3.14A actor-ID value/end-bit vectors, then full locked repository validation, clean reconstruction, force-free publication, and published-main CI.

Durable decision:

```text
docs/continuity/MIMIR_R3_14C_DECISION.md
```

The first actor-envelope reader is still not production capability. It is the active next pass:

```text
R3.14D — first actor envelope header native reader
docs/continuity/MIMIR_R3_14D_EXECUTION_SPEC.md
```

R3.14D opens only the first frame timing pair and one first actor header through `new`, then stops. The 47-replay native-vs-Boxcars admission remains R3.14E.

Current one-line truth:

> **MIMIR now has native private network bit primitives in production, but it still does not have an admitted actor-envelope reader; the next exact pass is R3.14D and the hard stop remains immediately after the first actor `new` bit.**


---

# 19. R3.14D production admission / R3.14E active

R3.14D is production at `7b17cb9033b6c71d476e500380d78402cbb3c56d`. The first native reader now materializes one first-frame/first-actor envelope header through `new` only.

Validation: 17 focused tests PASS; locked repository verifier PASS; clean CI `31702049792` SUCCESS; published-main CI `31702341993` SUCCESS; source blob `67752868807c0b7169e46f22762c7a0ea9efce40`; source SHA-256 `06b767622108ca1aea82ee5c0aad6cc503fbcfddaba05012cf022dd901a5a385`.

Active pass: `R3.14E`, evidence-only 47-replay native-vs-pinned-Boxcars differential audit. No production Rust change is allowed.
---

## CURRENT OVERRIDE — R3.14E COMPLETE / R3.15A ACTIVE

R3.14E completed with Outcome A: exact 47/47 native-vs-pinned-Boxcars first-envelope equality and zero mismatch/error. Production code remains `7b17cb9033b6c71d476e500380d78402cbb3c56d`. The active pass is now R3.15A, read-only NewActor branch evidence through the spawn trajectory endpoint. No production `name_id`, object ID, or spawn payload reader is admitted yet.
---

## CURRENT OVERRIDE — R3.15B

R3.15A is complete with Outcome A. The current pass is R3.15B. See `MIMIR_R3_15A_DECISION.md` and `MIMIR_R3_15B_EXECUTION_SPEC.md` for exact evidence and scope.
---

## CURRENT OVERRIDE — R3.15B ADMITTED / R3.15C ACTIVE

R3.15B is contract-complete and docs-only. Production remains `7b17cb9033b6c71d476e500380d78402cbb3c56d` until R3.15C is implemented and admitted. R3.15C may extend only the first `new == true` actor through its static-dispatched spawn trajectory, then must stop before property decoding or further actor/frame iteration.

# MIMIR — CONTINUE HERE

> **Yeni bir ChatGPT/Codex oturumu MIMIR üzerinde çalışmaya BURADAN başlamalıdır.**
>
> Bu dosyanın amacı, yüzlerce tarihsel executor/doc artifact arasından yanlış kilometre taşını seçip eski işi yeniden yapmayı engellemektir.

## 1. Canonical repository

- Repository: `Naveax/MIMIR`
- Default branch: `main`
- Last production-code milestone before this continuity-control-plane work: `ee23fe4d6975caf4910fd6db84a18c3a2f3f70aa`
- Production milestone: **R3.13 — static replay network lookup plan**
- Last completed read-only format audit: **R3.14 format audit**
- Current next pass: **R3.14A — pinned Boxcars differential evidence for first frame + first actor envelope header**

The continuity documentation commits may make `main` newer than the production-code SHA above. That is expected. Never assume the newest commit changed Rust code. Inspect the diff.

## 2. Mandatory reading order

Read these files in this exact order before changing production code:

1. `docs/continuity/MIMIR_CONTINUITY_STATE.json`
2. `docs/continuity/MIMIR_CURRENT_STATE.md`
3. `docs/continuity/MIMIR_R3_14A_EXECUTION_SPEC.md`
4. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
5. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
6. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
7. `docs/continuity/MIMIR_PROGRESS_LEDGER.md`
8. Only then inspect historical `docs/`, executor files, reports, commits, tests, and source code required for the active pass.

## 3. Source-of-truth precedence

When sources disagree, use this precedence:

1. **Current repository code/tests at fresh `origin/main`**
2. **Exact commit / GitHub Actions evidence tied to the current production milestone**
3. `MIMIR_CONTINUITY_STATE.json`
4. `MIMIR_CURRENT_STATE.md`
5. Active exact-pass spec (currently `MIMIR_R3_14A_EXECUTION_SPEC.md`)
6. `MIMIR_BOUNDARY_LOCKS.md`
7. A→Z roadmap
8. Progress ledger
9. Older historical docs/executor artifacts
10. Old chat memory or prose summaries

If code/tests contradict continuity docs, do not silently choose one. Record the drift, stop capability widening, and repair continuity after establishing repository truth.

## 4. Current exact checkpoint

R3.13 put the static network lookup plan into production. The admitted plan now contains, per replay:

- `object_lookups`
- inherited stream/property maps
- `max_prop_id`
- `prop_id_bits`
- separate spawn-trajectory table
- channel/build-derived flags
- raw footer lookup materialization used to build the plan

**Network payload bits are still not consumed by the production lookup-plan layer.**

Differential evidence recorded for the supported corpus:

- supported replay count: **47**
- attribute updates checked against pinned Boxcars oracle: **3,990,310 / 3,990,310**
- `unresolved_stream = 0`
- `property_object_mismatch = 0`
- `decoded_not_implemented_hits = 0`

Actor lifecycle evidence:

- same actor ID receiving another `NewActor` with the **same class** is valid behavior
- same-class overwrite observations: **141,511**
- class-changing overwrite observations: **0**
- future native decoder MUST NOT classify `duplicate actor ID` alone as malformed

## 5. R3.14 read-only format result

The exact first native bitstream order currently admitted for planning is:

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

Important bounded-integer rule:

> Rocket League bounded integers are **not** ordinary fixed-width integers. After low bits are consumed, an additional discriminator bit may be consumed depending on the decoded value/bound. Actor ID and stream ID implementations must preserve this exact behavior.

## 6. The next action is NOT a production implementation

The next pass is **R3.14A evidence-only**:

- production code unchanged
- pinned Boxcars temporarily instrumented
- 47 supported replays only
- capture differential evidence for:
  - first frame `time`
  - first frame `delta`
  - first actor-envelope `actor_present`
  - if present: `actor_id`
  - `alive`
  - if alive: `new`
- stop before:
  - `name_id`
  - object spawn payload
  - spawn trajectory payload
  - property loop
  - attribute payload
  - frame iteration
  - raw-state

Read `docs/continuity/MIMIR_R3_14A_EXECUTION_SPEC.md` for the exact pass contract.

## 7. Permanent operating rule

Every production milestone follows:

```text
repository re-audit
→ evidence
→ admission/policy
→ implementation planning
→ implementation on isolated branch
→ focused fail-fast validation
→ source-only clean reconstruction
→ exact-SHA full validation
→ fresh-main ancestry audit
→ force=false publication
→ exact-main publication validation/readback
→ continuity sync
```

Never collapse evidence and implementation merely because the format looks obvious.

## 8. Continuity sync rule

After every production milestone is fully published and validated, update at minimum:

- `docs/continuity/MIMIR_CONTINUITY_STATE.json`
- `docs/continuity/MIMIR_CURRENT_STATE.md`
- `docs/continuity/MIMIR_PROGRESS_LEDGER.md`
- `docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md`
- exact next-pass spec if the next pass changed

Do this in a **docs-only continuity sync commit**. Do not mix continuity edits into the source implementation commit unless explicitly required.

## 9. Historical documents

Existing historical MIMIR docs are retained as evidence and design history. They are not automatically current. In particular, old files that say replay body/network/frame work is still completely unopened are stale relative to R3.13.

The older checklist/roadmap lineage remains useful for the long-term architecture, but the current progression is controlled by `docs/continuity/`.

## 10. One-sentence resume instruction

If a new chat has only one instruction available, use:

> **Fetch fresh `Naveax/MIMIR` main, read `MIMIR_CONTINUE_HERE.md` and every file in its mandatory reading order, verify repository truth, then execute only the exact current pass without reopening completed work or widening locked boundaries.**

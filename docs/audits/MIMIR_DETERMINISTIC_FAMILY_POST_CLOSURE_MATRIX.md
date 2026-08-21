# MIMIR Deterministic-Family Post-Closure Matrix

Status: noncanonical auxiliary audit/index only.

Base authority: `fec9dca3cb8366108245788fc9a2b24a0c99fe94` / tree `3bf5f68ec7df5565f78f89fd4bc2254f2a64e010`.

This document does not widen runtime behavior, replay parsing, export semantics, CLI surface, rollout capability, physics capability, or canonical R3.18 continuity. Its purpose is to prevent stale Stage 84/91/95 roadmap language from reopening work already closed by the Stage 69–101 deterministic-family evidence.

## Status vocabulary

- **Closed**: current repo source/tests provide a direct or sufficiently strong contract proof at the intended deterministic fake-backend boundary.
- **Partial**: behavior is guarded, but not every lane has an independent direct proof or the contract still relies on an implementation property.
- **Deferred**: deliberately outside this deterministic-family boundary; not missing work for this family.
- **Superseded**: historical roadmap item that later evidence closed and must not be revived without new contradictory evidence.

## Post-closure matrix

| Surface | Status | Current authority / meaning |
| --- | --- | --- |
| Deterministic fake-backend vertical-slice execution | Closed | Stage 69/73/80 family plus current repeated-run tests |
| Canonical reload of export bundle + scoreboard + teacher artifacts | Closed | Current deterministic vertical-slice positive reload tests |
| Repeated-run determinism and lane-distinct snapshots | Closed | Both fixture lanes have repeatability and non-collapse checks |
| Stage69 `teacher_namespace` propagation | Closed | Stage87 direct-effect proof |
| Stage77 `teacher_namespace` propagation | Closed | Stage96 direct-effect proof |
| Stage69 anchor metadata propagation | Closed | Stage88 direct-effect proof |
| Stage77 anchor metadata propagation | Closed | Stage97 direct-effect proof |
| Proposal label/actions/legal_hint/metadata propagation | Closed | Stage89 + Stage101 and closure-batch negatives |
| Stage77 proposal actions -> simulation commands | Closed | Stage77 closure-batch direct-consumption proof |
| Stage69 scorer weights -> components/total/teacher ordering | Closed | Stage85 |
| Stage77 scorer weights -> components/total/teacher ordering | Closed | Stage99 |
| Stage69 proposal score signals -> score/teacher ordering | Closed | Stage90 |
| Stage77 proposal score signals -> score/teacher ordering | Closed | Stage98 |
| Stage69 simulation seed -> `SimulationRequest.seed` | Closed | Stage86 |
| Stage77 simulation seed -> `SimulationRequest.seed` | Closed | Stage100 |
| `export_name -> TeacherLabelId` family behavior | Closed | Stage92 direct proof plus Stage77 stability coverage |
| Teacher ordering / artifact ordinals | Closed | Stage73/80 + current ordering/drift tests |
| Scoreboard component-key identity | Closed | Stage93 index + Stage94 explicit Stage77 drift guard |
| Branch artifact corruption rejection | Closed | Stage77 closure-batch canonical-load negative |
| Required proposal-label rejection | Closed | Stage77 persisted-input negative |
| Manifest/index stability under proposal-only mutation | Closed | Stage77 closure-batch proof |
| Heterogeneous branch metadata `FieldValue` shapes | Closed | Stage77 closure-batch preservation proof |
| Independent branch-payload parity via distinct implementation | Deferred | Current runtime and canonical reload intentionally share the same consumer path; a second proof would be tautological without a genuinely independent implementation |
| Real replay ingestion | Deferred | Persisted vertical-slice input is the trusted boundary for this family |
| Real rollout / real physics / backend diversity | Deferred | Fake backend is intentional here |
| Async queues/retries/background orchestration | Deferred | Different runtime-system contract family |
| Snapshot widening | Deferred | Snapshot is intentionally narrower than canonical artifacts |
| Missing optional proposal `actions`/`legal_hint`/`metadata` rejection | Deferred | These fields intentionally deserialize with defaults; changing that would be a semantics change |
| Stage77-only independent `export_name -> TeacherLabelId` mutation | Partial | Family-level behavior is closed; same-lane symmetry remains optional diagnostic work rather than a known defect |
| Scoreboard component ordering as separate schema/version | Partial | Determinism is currently inherited intentionally from `BTreeMap<String, f64>` rather than a separately versioned component schema |

## Scoreboard component ordering no-change lock

Current deterministic scoreboard component ordering is intentionally inherited from Rust `BTreeMap<String, f64>` lexical key ordering.

This is a **current implementation contract, not a new wire-schema version**. The repository already guards component-key identity and value effects. Until an external consumer requires a separately versioned component-order schema, introducing one would add schema surface without closing a demonstrated defect.

Therefore the current policy is:

1. preserve deterministic lexical ordering through `BTreeMap`;
2. treat unexpected key-set drift as a contract failure where existing tests name that surface;
3. do not introduce a new component-order schema/version merely to restate `BTreeMap` behavior;
4. reconsider only if ordering becomes independently serialized/consumed in a way that requires a stronger public compatibility guarantee.

## Superseded roadmap items

Do not reopen the following merely because older Stage 84/91/95/98–100 documents list them as future work:

- Stage77 teacher namespace direct proof;
- Stage77 anchor metadata direct proof;
- Stage77 score-signals direct proof;
- Stage77 scorer-weights direct proof;
- Stage77 simulation-seed direct proof;
- Stage77 proposal-surface propagation;
- Stage77 branch action-order as a separate pass;
- Stage77 teacher-label text derivation from branch label as a separate pass;
- Stage77 sibling-proposal field-isolation as a separate pass.

Later source/tests and Stage94/96–101/closure-batch evidence supersede those roadmap entries.

## Reopen rule

A closed or superseded row may be reopened only with concrete contradictory evidence such as:

- a fresh source change that removes the asserted boundary;
- a deterministic regression test that now fails for the named edge;
- a new independent consumer contract that makes the current partial/deferred boundary insufficient;
- a canonical decision that deliberately widens the family.

Absence of a duplicate same-lane test by itself is not contradictory evidence.

## Bottom line

The deterministic fake-backend family is strongly closed at its intended narrow scope. Remaining work is mostly explicit boundary management, not a license to manufacture new runtime features or replay/physics claims inside this contract family.

# MIMIR Export Record-ID Uniqueness Audit

## Status

- Scope: non-canonical auxiliary audit only.
- Base authority: `02233c8125e658513dcb068370c48b1e8f15a01c` (`Admit R3.18AK and open R3.18AL`).
- Production code changed: no.
- Replay parser, fixtures, corpus, workflows, continuity, and canonical pass state changed: no.
- Finding classification: evidence-backed cross-boundary contract risk; not yet an admitted production defect.

## Question

Should `mimir-export` require `ExportIndexEntry.record_id` to be unique within each `ExportArtifactKind`?

The current public boundaries are inconsistent about duplicate same-kind record identifiers. The exporter/index loader can represent them, while the candidate-planning boundary rejects the resulting duplicate identifier list.

## Current evidence

### 1. Export index identity is explicit

`ExportIndexEntry` stores both:

- `artifact_kind`
- `record_id`
- `relative_path`

This means record identity is represented independently from the on-disk path.

### 2. Export paths are ordinal, not record-ID-derived

The current exporter writes deterministic ordinal artifact paths such as:

- `anchors/anchor-0000.json`
- `anchors/anchor-0001.json`
- `branches/branch-0000.json`

Therefore two anchor artifacts with the same payload `AnchorId` can still receive different relative paths. Duplicate-path validation alone does not imply duplicate-record-ID validation.

### 3. `validate_index(...)` rejects duplicate paths but does not visibly reject duplicate record IDs

The current index validator tracks `seen_paths` and rejects a repeated `relative_path`. It validates each `record_id` for non-empty identifier form, but it does not maintain a same-kind record-ID set in the observed implementation.

As a result, entries equivalent to the following shape can remain structurally distinct by path:

```text
Anchor, record_id = "anchor-x", path = "anchors/anchor-0000.json"
Anchor, record_id = "anchor-x", path = "anchors/anchor-0001.json"
```

### 4. Per-file load validation does not resolve the ambiguity

`validate_loaded_anchor_entry(...)` and `validate_loaded_branch_entry(...)` verify that each index entry's `record_id` equals the loaded payload ID and that the content hash matches.

Two different files containing the same same-kind ID can therefore each satisfy their own entry-to-payload identity check.

### 5. Candidate planning rejects the duplicate identity later

`validate_consumer_export_for_selection(...)` collects anchor and branch IDs and passes each list through `validate_identifier_list(...)`.

`validate_identifier_list(...)` explicitly rejects duplicate values using a set.

Therefore a bundle that can pass the earlier export/index/load shape can become unusable at the later candidate-planning boundary solely because the same-kind record identifiers are duplicated.

## Boundary inconsistency

The observed behavior is:

```text
export/index/load boundary: duplicate same-kind record IDs can be represented
candidate planning boundary: duplicate same-kind record IDs are rejected
```

This creates a fail-late integrity boundary. It is preferable for a persisted bundle to be rejected at the earliest boundary that can prove the identity ambiguity, if same-kind uniqueness is intended to be part of the contract.

## Cross-kind identity must remain separate

This audit does **not** recommend global string uniqueness across artifact kinds.

The shared data-contract design deliberately uses typed IDs such as `AnchorId` and `BranchId` to prevent cross-type identity mixing. Therefore an anchor whose textual ID is `"x"` and a branch whose textual ID is also `"x"` should not automatically be treated as an identity collision without an explicit contract decision.

The narrow candidate policy is:

```text
unique within Anchor entries
unique within Branch entries
no new cross-kind string-uniqueness rule
```

## Recommended admission decision

Before changing production behavior, explicitly decide one of the following:

### Outcome A: admit same-kind uniqueness

If persisted export IDs are intended to be stable identities, add fail-closed same-kind duplicate detection to the export/index boundary and focused tests covering:

1. duplicate anchor `record_id` rejection;
2. duplicate branch `record_id` rejection;
3. identical textual IDs across one anchor and one branch remaining allowed;
4. exporter rejection before publication of a bundle whose same-kind payload IDs collide;
5. loader/index rejection for a tampered persisted bundle containing same-kind duplicate IDs.

### Outcome B: duplicate same-kind IDs are intentionally representable

If duplicates are intentional, document how downstream selection identifies one specific record when textual IDs collide, and revise candidate-planning validation so the public boundaries are coherent.

## Non-goals

This audit does not:

- change `mimir-export` production semantics;
- change artifact schemas or schema versions;
- change replay parsing or replay evidence;
- change execution-result ledger semantics;
- reopen frozen execution-result wrapper cleanup;
- change path-traversal validation;
- claim that cross-kind textual ID reuse is invalid;
- claim an admitted defect before the uniqueness policy is explicitly accepted.

## Conclusion

The repository currently has enough evidence to justify a narrow contract decision on same-kind export record-ID uniqueness. The safest implementation direction, if uniqueness is admitted, is to fail at export/index validation rather than allow a bundle to survive until candidate planning rejects the same identity set later.

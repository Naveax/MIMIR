# MIMIR Skill Forge BC Replay-Input Locator Implementation Reopen Decision v1

## A. PURPOSE

### What this pass owns

This pass owns exactly one reopen-decision question above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`

It defines:

- whether actual replay-input locator implementation work must now be deliberately reopened at all
- the exact criteria used to answer that question
- the narrowest honest next contract shape only if reopening is justified

### Why it exists

The boundary below this pass already fixed the current truthful limit:

- `RealizedForTruthfulNonLocatedReplayInputLocatorOnly`

That matters because the repo can now prove all of the following:

- one admitted specimen yields one truthful replay-input locator result
- that result preserves receipt-bound specimen identity, deferred observation lineage, and the
  contract-only locator handle kind
- that result still does not locate replay input
- that result still does not parse replay input

This pass exists because the repo can now prove it can do no more than a truthful non-located /
non-parsed replay-input locator result. The remaining question is whether the next missing work is
now truly replay-input locator implementation work.

### How it differs from the replay-input locator realization boundary below it

- The lower boundary realizes the current truth:
  `RealizedForTruthfulNonLocatedReplayInputLocatorOnly`.
- This pass does not realize more output.
- This pass decides whether one narrower replay-input locator implementation boundary must now be
  deliberately reopened above that truthful non-located result.
- This pass is still not replay-input locator implementation.
- This pass is still not replay parsing.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this reopen-decision version.

This replay-input locator implementation reopen decision remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`
- the preserved lineage tuple is only the low-boost-recovery BC specimen tuple already carried by
  that result
- the audited family root reference is still only the low-boost-recovery BC specimen-tree anchor
- no second family exists that would justify a shared replay-input locator implementation
  framework

No generic all-family replay/raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`
- the audited family root directory reference already preserved by that result

From `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `source_chosen_replay_parsing_contract_shape`
- `source_chosen_replay_input_access_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `consumed_replay_input_locator_boundary_input.lane_ordinal`
- each `consumed_replay_input_locator_boundary_input.specimen_ordinal`
- each `consumed_replay_input_locator_boundary_input.artifact_id`
- each `consumed_replay_input_locator_boundary_input.anchored_bc_specimen_file_path`
- each `consumed_replay_input_locator_boundary_input.source_raw_state_window_ref`
- each `consumed_replay_input_locator_boundary_input.source_slice_id`
- each `consumed_replay_input_locator_boundary_input.source_replay`
- each `consumed_replay_input_locator_boundary_input.source_subject`
- each `consumed_replay_input_locator_boundary_input.source_phase_id`
- each `consumed_replay_input_locator_boundary_input.preserved_observation_binding_kind`
- each `consumed_replay_input_locator_boundary_input.preserved_accepted_reference_window`
- each `preserved_replay_input_locator_output_boundary.lane_ordinal`
- each `preserved_replay_input_locator_output_boundary.specimen_ordinal`
- each `preserved_replay_input_locator_output_boundary.artifact_id`
- each `preserved_replay_input_locator_output_boundary.anchored_bc_specimen_file_path`
- each `preserved_replay_input_locator_output_boundary.source_raw_state_window_ref`
- each `preserved_replay_input_locator_output_boundary.source_slice_id`
- each `preserved_replay_input_locator_output_boundary.source_replay`
- each `preserved_replay_input_locator_output_boundary.source_subject`
- each `preserved_replay_input_locator_output_boundary.source_phase_id`
- each `preserved_replay_input_locator_output_boundary.preserved_observation_binding_kind`
- each `preserved_replay_input_locator_output_boundary.preserved_accepted_reference_window`
- each `preserved_replay_input_locator_output_boundary.bound_replay_input_locator_handle_kind`
- each `replay_input_locator_disposition`
- `realization_disposition`
- `realization_notes`
- `chosen_replay_input_locator_contract_shape`

The following are no longer direct input at this boundary:

- replay-input locator contracts
- replay-input locator reopen decisions below this layer
- replay-input-access/source-binding realizations
- blocked replay-side parse-attempt results
- parse-attempt contracts
- materialization-attempt realizations
- replay-parsing reopen decisions
- replay-parsing-success reopen decisions
- materialization-contract results
- validation results
- lower locator-contract results
- lower locator-realization results
- planning results
- proof results
- emitted-output audit/readback results
- actual emission receipts
- plans
- export-layout results
- specimen batches
- refined specimens
- persisted artifacts
- BC rows
- shells
- lower planning boundaries

Those lower layers remain frozen. This pass starts strictly from the truthful non-located
replay-input locator realization result and the already-preserved audited family root reference.

## D. DECISION QUESTION

The exact question is:

- should actual replay-input locator implementation work now be deliberately reopened above the
  truthful non-located replay-input locator realization result?

This question exists only because the current repo can now prove it can do no more than a
non-located / non-parsed replay-input locator result.

That means the unresolved gap is no longer whether replay-input locator contract shape exists or
whether the truthful non-located locator result has been made explicit.

The unresolved gap is narrower:

- whether the repo now needs one explicit replay-input locator implementation-facing boundary above
  the truthful non-located replay-input locator realization result

This is still not replay-input locator implementation and still not replay parsing.

## E. REOPEN CRITERIA

Reopening is justified only if all of the following hold:

1. the remaining missing piece is truly replay-input locator implementation work and not another
   lower-layer contract defect below the truthful non-located replay-input locator realization
2. the next boundary can stay low-boost-recovery-specific
3. the next boundary can stay receipt-bound
4. the next boundary can avoid sidecars, manifests, and generic indexing
5. the next boundary can avoid `mimir_export`
6. the next boundary can stay below actual replay parsing
7. the next boundary can stay below actual raw-state payload materialization, tensor
   materialization, and control/action materialization
8. the next boundary can introduce one locator-implementation-facing handle contract without
   inventing replay-path semantics absent from the admitted realization result
9. the next boundary can preserve the existing truth that:
   - `source_replay` remains opaque lineage only
   - `audited_family_root_directory` remains only a BC specimen-tree anchor
   - `FutureParserConsumableReplayHandleOnly` remains contract-only until a later explicit
     implementation-facing boundary says more

The audited repo state satisfies those criteria because:

- the current realization result already preserves the exact receipt-bound identity tuple, replay
  lineage, and deferred observation lineage
- the current realization result already proves the current truthful limit is
  `RealizedForTruthfulNonLocatedReplayInputLocatorOnly`
- no replay-input locator implementation-facing boundary exists above that truthful result
- `mimir-replay` already exposes a narrow parser-consumable replay handle surface,
  `ReplayInput`, while still exposing no parser-success boundary or parser implementation

That last point matters because reopening is only honest if the missing capability can be isolated
to one receipt-bound implementation-facing contract without pretending parsing already exists.

## F. DECISION

The decision in v1 is:

- reopen justified for one narrow receipt-bound replay-input locator implementation boundary

### Why reopening is justified

Reopening is justified because the truthful non-located replay-input locator result already
isolates the missing piece precisely:

- the repo preserves enough trustworthy receipt-bound identity and lineage to support one next
  narrow implementation-facing boundary
- the repo still does not expose any boundary above the truthful non-located locator result that
  says how that exact preserved tuple may later reach a parser-consumable replay input surface

The current repo already preserves enough trustworthy input to define that boundary narrowly:

- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`
- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`
- `bound_replay_input_locator_handle_kind`
- the audited family root directory reference

That means the minimum honest reopen is not replay parsing, not raw-state payload materialization,
not tensor/control materialization, and not sidecar/manifest work.

It is one contract-only replay-input locator implementation boundary above the truthful
non-located replay-input locator realization result.

### Narrowest honest next boundary shape

The narrowest honest next boundary shape is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`

### What it would consume

It would consume only:

- the admitted truthful non-located replay-input locator realization result
- the audited family root directory reference already preserved by that realization result

### What it would expose

It would expose exactly one contract-only replay-input locator implementation-facing boundary per
admitted specimen:

- one implementation-facing handle contract keyed by the exact preserved receipt-bound lineage
  tuple already carried by the truthful non-located realization result

### What remains deferred

This decision still defers:

- actual replay-input locator implementation
- actual replay-input location
- actual `mimir-replay::ReplayInput`
- actual replay parsing
- actual raw-state payload materialization
- tensor materialization
- control/action extraction
- sidecar/manifest realization
- generic indexing
- `mimir_export`

### Why this is the minimum honest reopen

This is the minimum honest reopen because:

- the truthful non-located replay-input locator realization result is already explicit and
  machine-checkable
- the missing problem is now earlier than replay parsing but later than replay-input locator
  contract/realization shaping
- `source_replay` still remains opaque lineage only
- `audited_family_root_directory` still remains only a BC specimen-tree anchor
- no current evidence proves that sidecars, manifests, generic indexing, or `mimir_export` belong
  in the missing defect path

## G. REPLAY-INPUT LOCATOR IMPLEMENTATION CONTRACT SHAPE V1

Because reopening is justified, the narrowest contract-only next boundary is defined here.

### Contract name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`

### Exact inputs it would consume from the non-located replay-input locator realization result

For one admitted specimen, the contract would consume exactly:

- `audited_family_root_directory`
- `lane_ordinal`
- `specimen_ordinal`
- `artifact_id`
- `anchored_bc_specimen_file_path`
- `source_raw_state_window_ref`
- `source_slice_id`
- `source_replay`
- `source_subject`
- `source_phase_id`
- `preserved_observation_binding_kind`
- `preserved_accepted_reference_window`
- `bound_replay_input_locator_handle_kind`

Those values would be consumed only from:

- `consumed_replay_input_locator_boundary_input`
- `preserved_replay_input_locator_output_boundary`
- `replay_input_locator_disposition`

The next contract would not recompute those values from lower layers.

### Exact replay-input locator implementation-facing boundary it would expose

The next contract would expose exactly one per-specimen replay-input locator implementation-facing
boundary that:

- preserves the exact admitted receipt-bound lineage tuple
- preserves the exact deferred observation lineage fields
- preserves that the current handle kind is still
  `FutureParserConsumableReplayHandleOnly`
- adds only one new implementation-facing contract boundary whose admitted meaning is:
  this exact preserved tuple now requires one later explicit replay-input locator implementation
  step before any replay-input location or parsing claim can exist

The next contract may acknowledge that later implementation work might target
`mimir-replay::ReplayInput`, but it must not materialize or promise one in the contract itself.

### Exact invariant

The exact invariant is:

- for one admitted low-boost-recovery truthful non-located replay-input locator specimen, the
  tuple
  (`lane_ordinal`, `specimen_ordinal`, `artifact_id`, `anchored_bc_specimen_file_path`,
  `source_raw_state_window_ref`, `source_slice_id`, `source_replay`, `source_subject`,
  `source_phase_id`, `preserved_observation_binding_kind`,
  `preserved_accepted_reference_window`) plus preserved receipt-bound lineage and the preserved
  `FutureParserConsumableReplayHandleOnly` contract-only handle kind binds to exactly one honest
  replay-input locator implementation-facing handle contract
- that contract is authoritative only for that exact preserved tuple
- that contract must not silently rewrite, drop, pad, or reorder preserved lineage
- that contract must not reinterpret `source_replay.provenance_label` as a path contract
- that contract must not reinterpret `audited_family_root_directory` as replay storage

### Exact relationship to deferred observation access

The relationship to deferred observation access remains narrow:

- `preserved_observation_binding_kind` and `preserved_accepted_reference_window` stay preserved as
  deferred lineage only
- the replay-input locator implementation contract does not reopen observation materialization
- the next contract only guarantees that deferred observation lineage stays attached to the same
  specimen while replay-input locator implementation work is being defined

### What it explicitly refuses to promise

The next contract explicitly refuses to promise:

- actual replay-input locator implementation
- actual replay-input location
- actual `mimir-replay::ReplayInput`
- actual replay parsing
- replay frame availability
- replay byte availability
- replay file path derivation from `source_replay`
- replay storage derivation from `audited_family_root_directory`
- actual raw-state payload materialization
- tensor materialization
- control/action extraction
- sidecar/manifest realization
- generic index semantics
- `mimir_export` integration

## H. ADMISSION RULES

A replay-input locator realization result may enter this reopen-decision boundary only when all of
the following hold:

1. the input is exactly
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`
2. `source_contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorOnly`
3. `source_contract_notes` still equal the exact replay-input locator contract note set
4. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
5. `source_chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
6. `source_chosen_replay_parsing_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
7. `source_chosen_replay_input_access_contract_shape ==`
   `ReceiptBoundReplayInputAccessSourceBindingOnly`
8. `realization_disposition == RealizedForTruthfulNonLocatedReplayInputLocatorOnly`
9. `realization_notes` still equal the exact truthful non-located replay-input locator realization
   note set
10. `chosen_replay_input_locator_contract_shape == ReceiptBoundReplayInputLocatorOnly`
11. `specimen_count > 0`
12. `group_count > 0`
13. `group_count` equals the number of preserved ordered lane results
14. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
15. `audited_family_root_directory` still exists as a directory at decision time
16. lane order and specimen order still match concrete lane/specimen position
17. each `consumed_replay_input_locator_boundary_input.anchored_bc_specimen_file_path` still
    remains receipt-bound below `audited_family_root_directory`
18. each `preserved_replay_input_locator_output_boundary` still matches the corresponding consumed
    replay-input locator boundary input on:
    - `lane_ordinal`
    - `specimen_ordinal`
    - `artifact_id`
    - `anchored_bc_specimen_file_path`
    - `source_raw_state_window_ref`
    - `source_slice_id`
    - `source_replay`
    - `source_subject`
    - `source_phase_id`
    - `preserved_observation_binding_kind`
    - `preserved_accepted_reference_window`
19. each specimen still preserves
    `replay_input_locator_disposition ==`
    `RealizedForTruthfulNonLocatedReplayInputLocatorOnly`
20. each preserved output boundary still preserves
    `bound_replay_input_locator_handle_kind ==`
    `FutureParserConsumableReplayHandleOnly`
21. no lower boundary is silently reopened to repair or reinterpret the admitted realization input

Admission here means only:

- this reopen decision may rely on the truthful non-located replay-input locator result as the
  last trusted pre-replay-input-locator-implementation layer

Admission here does not mean:

- replay-input locator implementation is implemented
- replay-input location succeeds
- replay parsing succeeds
- replay files or replay bytes are available
- raw-state payload exists
- tensors or controls are available

## I. FAILURE RULES

This pass must hard-fail for:

- degraded replay-input locator realization input
- count/order/root/path drift
- duplicate or missing artifact ids
- any input/output-boundary identity drift
- any specimen whose replay-input locator disposition no longer remains truthful non-located only
- any attempt to reinterpret `source_replay` or `provenance_label` as an implicit replay path
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen this pass into actual replay-input locator implementation
- any attempt to widen this pass into actual replay parsing
- any attempt to widen this pass into actual raw-state payload materialization
- any attempt to widen this pass into tensor/control materialization
- any attempt to widen this pass into sidecars, manifests, generic indexing, or `mimir_export`

This v1 pass produces `reopen justified` only when all admission rules hold.

There is no valid-input `no reopen` output in v1.

That is deliberate.

For valid admitted input, the current repo-local evidence already proves all of the following:

- the lower replay-input locator realization boundary is intact
- the current truthful limit is explicitly non-located only
- the remaining unresolved boundary is one receipt-bound replay-input locator
  implementation-facing contract above that result

Anything weaker would only restate the already-known non-located truth without isolating the next
contract the following pass actually needs.

## J. NON-GOALS

This pass does not do any of the following:

- no actual replay-input locator implementation
- no actual replay parsing
- no actual raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no generic manifest/index framework
- no usefulness proof
- no policy-improvement proof
- no replay corpus ingestion
- no rollout or physics work
- no async/background system
- no database work

## K. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- the replay-input locator implementation reopen decision is explicit and auditable
- the decision stays low-boost-recovery-specific
- the decision stays receipt-bound
- the narrowest honest next contract shape is fixed:
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`
- `mimir_export` remains untouched and forbidden

### What remains deferred

This pass still does not guarantee:

- actual replay-input locator implementation
- actual replay-input location
- actual `mimir-replay::ReplayInput`
- actual replay parsing
- actual raw-state-window payload materialization
- tensor/control materialization
- sidecar/manifest necessity

### Immediate next-stage implication

The immediate next pass should be:

- one first narrow contract-definition pass for
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorImplementationContractV1`
- still above
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputLocatorRealizationResultV1`
- still without actual replay-input locator implementation
- still without actual replay parsing
- still without `mimir_export` widening unless that separate boundary is explicitly reopened

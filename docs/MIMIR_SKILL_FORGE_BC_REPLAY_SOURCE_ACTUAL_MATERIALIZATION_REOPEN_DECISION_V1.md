# MIMIR Skill Forge BC Replay-Source Actual-Materialization Reopen Decision v1

## A. PURPOSE

### What this pass owns

This pass owns exactly one reopen-decision question above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`

It defines:

- whether one receipt-bound replay-source actual-materialization boundary must now be
  deliberately reopened at all
- the exact criteria used to answer that question
- the narrowest honest next contract shape only if reopening is justified

### Why it exists

The realization boundary below this pass already fixed the current truthful limit:

- `RealizedForTruthfulBlockedReplaySourceMaterializationOnly`

That matters because the repo can now prove all of the following from one admitted
machine-verifiable result:

- the admitted low-boost-recovery specimen identity and deferred observation lineage survive into
  the truthful blocked replay-source-materialization result
- the blocked result still exposes no replay path
- the blocked result still exposes no replay bytes
- the blocked result still exposes no replay frames
- the blocked result still exposes no actual `mimir_replay::ReplayInput`
- `source_replay` still remains opaque lineage only
- `source_replay.provenance_label` still remains opaque lineage only
- `audited_family_root_directory` still remains only a BC specimen-tree anchor

This pass exists because the repo can now prove it cannot honestly materialize replay source from
the current admitted contract/result chain without reopening one explicit actual-materialization
boundary first.

### How it differs from the replay-source-materialization realization boundary below it

- The lower boundary realizes the current truth:
  `RealizedForTruthfulBlockedReplaySourceMaterializationOnly`.
- This pass does not realize more replay source.
- This pass decides whether one broader replay-source actual-materialization boundary must now be
  deliberately reopened above that truthful blocked result.
- This pass is still not replay-source materialization implementation.
- This pass is still not replay parsing.
- This pass is still not raw-state payload materialization.

## B. FAMILY SCOPE

`low_boost_recovery` is the only supported family in this reopen-decision version.

This replay-source actual-materialization reopen decision remains family-specific because:

- the admitted input is only
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`
- the preserved lineage tuple is only the low-boost-recovery BC specimen tuple already carried by
  that result
- the preserved deferred observation lineage is only the low-boost-recovery BC observation-binding
  pair already carried by that result
- no second family exists that would justify a shared replay/raw-state/index/export/materialization
  framework

No generic all-family replay/raw-state/index/export/materialization framework is introduced here.

## C. INPUT BOUNDARY

This pass consumes only:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`
- the audited family root directory reference already preserved by that result

From
`LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`,
this pass consumes exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `source_chosen_replay_parsing_contract_shape`
- `source_chosen_replay_input_access_contract_shape`
- `source_chosen_replay_input_locator_contract_shape`
- `source_chosen_replay_input_locator_implementation_contract_shape`
- `source_chosen_replay_input_locator_actual_implementation_contract_shape`
- `audited_family_root_directory`
- ordered `preserved_ordered_lane_results`
- each `lane_ordinal`
- each ordered `ordered_specimen_results`
- each `specimen_ordinal`
- each `consumed_replay_source_materialization_boundary_input`
- each `preserved_replay_source_materialization_output_boundary`
- each `replay_source_materialization_disposition`
- `realization_disposition`
- `realization_notes`
- `chosen_replay_source_materialization_contract_shape`

The following are no longer direct input at this boundary:

- replay-source-materialization contracts below this layer
- replay-source-materialization reopen-decision docs/artifacts below this layer
- replay-input locator actual-implementation contracts and realizations below this layer
- replay-input locator implementation contracts and realizations below this layer
- replay-input locator contracts and realizations below this layer
- replay-input-access/source-binding contracts and realizations below this layer
- raw-state materialization reopen, contract, and realization layers below this layer
- replay parsing reopen, contract, and realization layers below this layer
- sidecars, manifests, generic indexes, persisted artifacts, and `mimir_export`

Those lower layers remain frozen. This pass starts strictly from the truthful blocked
replay-source-materialization realization result and the already-preserved audited family root
reference.

## D. DECISION QUESTION

The exact question is:

- should one replay-source actual-materialization boundary now be deliberately reopened above the
  truthful blocked replay-source-materialization realization result?

This question exists only because the current repo can now prove something narrower and stricter
than before:

- the current admitted contract/result chain can preserve receipt-bound identity, deferred
  observation lineage, the future parser-consumable replay-handle contract fact, and the explicit
  replay-source-materialization requirement kind
- the same chain cannot honestly yield replay-source semantics from the currently admitted fields
  without cheating through implicit path or storage reinterpretation

That means the unresolved gap is no longer:

- whether the blocked replay-source-materialization result is explicit
- whether the repo already has a replay-source-materialization contract or realization boundary

The unresolved gap is now later than blocked replay-source-materialization realization but earlier
than replay parsing:

- whether the repo must now reopen one explicit replay-source actual-materialization boundary so
  later work can admit explicit replay-source semantics without inventing them from opaque lineage
  or audited-root presence alone

## E. REOPEN CRITERIA

Reopening is justified only if all of the following hold:

1. the remaining missing piece is truly replay-source actual-materialization and not another
   defect in the lower replay-source chain
2. the next boundary can stay low-boost-recovery-specific
3. the next boundary can stay receipt-bound
4. the next boundary can avoid `mimir_export`
5. the next boundary can stay below replay parsing
6. the next boundary can stay below raw-state payload materialization, tensor materialization, and
   control/action materialization
7. the next boundary can introduce one explicit replay-source actual-materialization semantics
   boundary without cheating through `source_replay`, `source_replay.provenance_label`, or
   `audited_family_root_directory` reinterpretation
8. sidecars, manifests, and generic indexing remain unjustified unless the audited repo state now
   proves one of them is the minimum honest way to represent replay source
9. the audited crate surfaces do not already supply a richer truthful replay-source
   actual-materialization boundary that would make this reopen dishonest or redundant:
   - `mimir-skill` already makes the blocked replay-source-materialization result
     machine-checkable
   - `mimir-replay` still exposes only `ReplayInput`, `ReplayHeader`, `ReplayReader`, and
     `UnsupportedReplayReader`
   - `mimir-io` still exposes raw artifact read/write helpers and no replay-source locator or
     actual-materialization framework
   - `mimir-export` still remains unrelated and untouched
   - `mimir-types::ReplaySourceRef` still contains only `replay_id` and `provenance_label`
10. the broader reopen still remains narrower than replay parsing, raw-state payload
    materialization, tensor/control materialization, corpus-wide replay ingestion, sidecar
    realization, and generic framework work

The audited repo state in v1 satisfies those criteria.

## F. DECISION

The decision in v1 is:

- reopen justified for one narrow receipt-bound replay-source actual-materialization boundary

### Why reopening is justified

Reopening is justified because the truthful blocked replay-source-materialization result already
isolates the missing piece precisely:

- the repo preserves enough trustworthy receipt-bound identity and deferred observation lineage to
  bind one later explicit replay-source actual-materialization boundary
- the repo still has no honest way to move from that preserved tuple to explicit replay-source
  semantics without violating the opacity/root rules
- replay parsing still sits downstream of that missing source boundary

The audited repo state also shows that the missing boundary is not already implemented elsewhere:

- `mimir-replay` exposes a replay-input type, but the current admitted result cannot truthfully
  produce one
- `mimir-io` does not provide a replay-source lookup or actual-materialization layer
- `mimir-export` is unrelated to the missing defect path and remains forbidden

That means the minimum honest reopen is not:

- another lower replay-source-chain repair
- replay parsing
- raw-state payload materialization
- tensor/control materialization
- sidecar/manifest realization
- generic indexing

It is one explicit replay-source actual-materialization contract-definition pass above the
truthful blocked replay-source-materialization realization result.

### Narrowest honest next boundary shape

The narrowest honest next boundary shape is:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`

### What it would consume

It would consume only:

- the admitted truthful blocked replay-source-materialization realization result
- the audited family root directory reference already preserved by that realization result

### What it would expose

It would expose exactly one contract-only replay-source-actual-materialization-facing boundary per
admitted specimen:

- one boundary keyed by the exact preserved receipt-bound lineage tuple and deferred observation
  lineage already carried by the truthful blocked replay-source-materialization result
- one explicit replay-source-actual-materialization-facing contract element whose only admitted
  meaning is that this exact preserved tuple may later enter one explicit actual-materialization
  step without deriving replay source from opaque lineage or audited-root presence alone

### What remains deferred

This decision still defers:

- replay-source materialization implementation
- replay file discovery
- replay file path materialization
- replay bytes materialization
- replay frames materialization
- actual `mimir_replay::ReplayInput`
- replay parsing
- raw-state payload materialization
- tensor materialization
- control/action extraction
- sidecar/manifest realization
- generic indexing
- `mimir_export`

### Why this is the minimum honest reopen

This is the minimum honest reopen because:

- the truthful blocked replay-source-materialization realization result is already explicit and
  machine-checkable
- the missing problem is now later than blocked replay-source-materialization realization but
  earlier than replay parsing
- `source_replay` still remains opaque lineage only
- `source_replay.provenance_label` still remains opaque lineage only
- `audited_family_root_directory` still remains only a BC specimen-tree anchor
- no current evidence proves that sidecars, manifests, generic indexing, or `mimir_export`
  belong in the missing defect path

Anything narrower would only restate the already-known blocked truth. Anything broader would
invent replay-source semantics, parser semantics, or framework scope that the admitted result
still does not carry.

## G. REPLAY-SOURCE ACTUAL-MATERIALIZATION CONTRACT SHAPE V1

Because reopening is justified, the narrowest contract-only next boundary is fixed here.

### Contract name

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`

### Exact inputs it would consume from the blocked replay-source-materialization realization result

At the top level, the contract would consume exactly:

- `specimen_count`
- `group_count`
- `source_contract_disposition`
- `source_contract_notes`
- `source_chosen_locator_contract_shape`
- `source_chosen_materialization_contract_shape`
- `source_chosen_replay_parsing_contract_shape`
- `source_chosen_replay_input_access_contract_shape`
- `source_chosen_replay_input_locator_contract_shape`
- `source_chosen_replay_input_locator_implementation_contract_shape`
- `source_chosen_replay_input_locator_actual_implementation_contract_shape`
- `audited_family_root_directory`
- `realization_disposition`
- `realization_notes`
- `chosen_replay_source_materialization_contract_shape`

For one admitted specimen, the contract would consume exactly:

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
- `preserved_replay_input_locator_handle_kind`
- `bound_replay_source_materialization_requirement_kind`
- `replay_source_materialization_disposition`

Those values would be consumed only from:

- `consumed_replay_source_materialization_boundary_input`
- `preserved_replay_source_materialization_output_boundary`
- `replay_source_materialization_disposition`

The next contract would not recompute those values from lower layers.

### Exact replay-source-actual-materialization-facing boundary it would expose

The next contract would expose exactly one per-specimen replay-source-actual-materialization-facing
boundary that:

- preserves the exact admitted receipt-bound lineage tuple
- preserves the exact deferred observation lineage fields
- preserves that the current replay-input-locator handle kind is still
  `FutureParserConsumableReplayHandleOnly`
- preserves that the current replay-source-materialization requirement kind is still
  `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`
- adds only one new explicit replay-source-actual-materialization-facing contract element whose
  admitted meaning is:
  this exact preserved tuple may later bind to one explicit replay-source carrier admitted by a
  later actual-materialization realization or implementation pass, without treating lineage or
  audited-root presence as that carrier

That next contract may acknowledge that later work could eventually target file-backed,
byte-backed, or `mimir_replay::ReplayInput`-backed semantics, but it must not materialize or
promise any of them in the contract itself.

### Exact invariant

The exact invariant is:

- for one admitted low-boost-recovery truthful blocked replay-source-materialization specimen, the
  tuple (`lane_ordinal`, `specimen_ordinal`, `artifact_id`, `anchored_bc_specimen_file_path`,
  `source_raw_state_window_ref`, `source_slice_id`, `source_replay`, `source_subject`,
  `source_phase_id`, `preserved_observation_binding_kind`,
  `preserved_accepted_reference_window`) plus preserved deferred observation lineage, preserved
  receipt-bound lineage, preserved `FutureParserConsumableReplayHandleOnly`, and preserved
  `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing` binds to exactly one
  honest replay-source-actual-materialization-facing contract
- that contract is authoritative only for that exact preserved tuple
- that contract must not silently rewrite, drop, pad, reorder, or widen preserved lineage
- that contract must not reinterpret `source_replay.provenance_label` as a path contract
- that contract must not reinterpret `audited_family_root_directory` as replay storage

### What it explicitly refuses to promise

The next contract explicitly refuses to promise:

- replay file discovery
- replay file path availability
- replay path derivation from `source_replay` or `source_replay.provenance_label`
- replay storage derivation from `audited_family_root_directory`
- replay bytes availability
- replay frames availability
- actual `mimir_replay::ReplayInput`
- replay parsing
- raw-state payload availability
- tensor availability
- control/action availability
- usefulness proof
- policy-improvement proof
- sidecar/manifest realization
- generic index semantics
- `mimir_export` integration

## H. ADMISSION RULES

A replay-source-materialization realization result may enter this reopen-decision boundary only
when all of the following hold:

1. the input is exactly
   `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`
2. `source_contract_disposition ==`
   `ContractDefinedForReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationOnly`
3. `source_contract_notes` still equal the exact replay-source-materialization contract note set
4. `source_chosen_locator_contract_shape == ReceiptBoundSpecimenFileAnchored`
5. `source_chosen_materialization_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefMaterializationAttemptOnly`
6. `source_chosen_replay_parsing_contract_shape ==`
   `ReceiptBoundValidatedSpecimenFileSourceRawStateWindowRefReplaySideParseAttemptOnly`
7. `source_chosen_replay_input_access_contract_shape ==`
   `ReceiptBoundReplayInputAccessSourceBindingOnly`
8. `source_chosen_replay_input_locator_contract_shape == ReceiptBoundReplayInputLocatorOnly`
9. `source_chosen_replay_input_locator_implementation_contract_shape ==`
   `ReceiptBoundReplayInputLocatorImplementationOnly`
10. `source_chosen_replay_input_locator_actual_implementation_contract_shape ==`
    `ReceiptBoundReplayInputLocatorActualImplementationOnly`
11. `chosen_replay_source_materialization_contract_shape ==`
    `ReceiptBoundReplaySourceMaterializationOnly`
12. `realization_disposition ==`
    `RealizedForTruthfulBlockedReplaySourceMaterializationOnly`
13. `realization_notes` still equal the exact truthful blocked replay-source-materialization
    realization note set
14. `specimen_count > 0`
15. `group_count > 0`
16. `group_count` equals the number of preserved ordered lane results
17. `audited_family_root_directory` still ends in `low_boost_recovery_bc_v1`
18. `audited_family_root_directory` still exists as a directory at decision time
19. lane order and specimen order still match concrete lane/specimen position
20. each `consumed_replay_source_materialization_boundary_input.anchored_bc_specimen_file_path`
    still remains receipt-bound below `audited_family_root_directory`
21. each `preserved_replay_source_materialization_output_boundary` still matches the
    corresponding consumed replay-source-materialization boundary input on:
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
    - `preserved_replay_input_locator_handle_kind`
22. each preserved output boundary still preserves
    `bound_replay_source_materialization_requirement_kind ==`
    `ExplicitReplaySourceMaterializationRequiredBeforeReplayInputOrParsing`
23. each specimen still preserves
    `replay_source_materialization_disposition ==`
    `RealizedForTruthfulBlockedReplaySourceMaterializationOnly`
24. no lower boundary is silently reopened to repair or reinterpret the admitted realization input

Admission here means only:

- this reopen decision may rely on the truthful blocked replay-source-materialization result as
  the last trusted pre-actual-materialization layer

Admission here does not mean:

- replay source is materialized
- replay-source actual-materialization succeeds
- replay-input access succeeds
- replay parsing succeeds
- replay files, replay bytes, or replay frames are available
- raw-state payload exists
- tensors or controls are available

## I. FAILURE RULES

This pass must hard-fail for:

- degraded replay-source-materialization realization input
- count/order/root/path drift
- duplicate or missing artifact ids
- any input/output-boundary identity drift
- any specimen whose replay-source-materialization disposition no longer remains truthful blocked
  only
- any specimen whose replay-source-materialization requirement kind no longer remains explicit
  replay-source materialization required before replay-input or replay parsing
- any attempt to reinterpret `source_replay` or `source_replay.provenance_label` as an implicit
  replay path or replay source
- any attempt to reinterpret the audited family root as replay storage
- any attempt to widen this pass into replay-source materialization implementation
- any attempt to widen this pass into replay parsing
- any attempt to widen this pass into raw-state payload materialization
- any attempt to widen this pass into tensor/control materialization
- any attempt to widen this pass into sidecars, manifests, generic indexing, or `mimir_export`

This v1 pass does not emit a separate valid-input `reopen not justified yet` disposition.

Reason:

- once the admitted truthful blocked replay-source-materialization result remains exact, the
  remaining missing boundary is already replay-source actual-materialization

So failure behavior is:

- hard-fail on any admission violation
- otherwise emit the single reopen-justified decision defined above

## J. NON-GOALS

This pass does not do any of the following:

- no replay-source materialization implementation
- no replay-input locator logic
- no replay parsing
- no actual raw-state payload materialization
- no tensor materialization
- no control/action extraction
- no `mimir_export` integration
- no usefulness proof
- no policy-improvement proof
- no corpus-wide replay ingestion
- no replay rollout or physics work
- no async/background system
- no database work
- no deterministic-family reopen
- no execution-result cleanup boundary change

## K. RELATION TO NEXT STAGES

### What this pass now guarantees

This pass now guarantees:

- the replay-source actual-materialization reopen decision is explicit and auditable
- the decision stays low-boost-recovery-specific
- the decision stays receipt-bound
- the narrowest honest next contract shape is fixed:
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`
- `source_replay` remains opaque lineage only
- `source_replay.provenance_label` remains opaque lineage only
- `audited_family_root_directory` remains only a BC specimen-tree anchor
- `mimir_export` remains untouched and forbidden

### What remains deferred

This pass still does not guarantee:

- replay-source actual-materialization succeeds
- replay file path, replay bytes, or replay frames exist
- actual `mimir_replay::ReplayInput` exists
- replay parsing
- raw-state payload materialization
- tensor/control materialization
- sidecar/manifest necessity

### Immediate next-stage implication

The immediate next pass should be:

- one first narrow contract-definition pass for
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceActualMaterializationContractV1`
- still above
  `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplaySourceMaterializationRealizationResultV1`
- still without replay-source materialization implementation
- still without replay parsing
- still without raw-state payload materialization
- still without `mimir_export` widening unless that separate boundary is explicitly reopened

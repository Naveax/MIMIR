# MIMIR Skill Forge BC Post ReplayInput Creation Realization Boundary Decision v1

## A. PURPOSE

This pass owns exactly one narrow boundary decision above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationResultV1`

The decision question is:

- does the realized memory-backed `mimir_replay::ReplayInput` bridge uniquely justify opening one
  downstream domain now, or is the honest next move still to stop?

This pass does not implement:

- replay parsing
- parser-success logic
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- raw-state payload parsing
- export widening

This pass is a low-boost-recovery boundary-decision and planning artifact only.

## B. FAMILY SCOPE

The only supported family is:

- `low_boost_recovery`

This remains family-specific because the admitted boundary result is the low-boost-recovery
ReplayInput-creation realization result. No generic all-family replay, raw-state, index, export,
or materialization framework is introduced.

## C. CURRENT FROZEN CHAIN SUMMARY

The frozen chain below this pass proves only the following facts:

1. The receipt-bound low-boost-recovery lane/specimen/artifact tuple is preserved.
2. The opaque caller-admitted replay-byte payload is preserved byte-for-byte.
3. A `mimir_replay::ReplayInput::Memory { label, bytes }` is created.
4. The label is derived only from:
   - `artifact_id`
   - `lane_ordinal`
   - `specimen_ordinal`
5. The `ReplayInput::Memory` byte payload equals the preserved opaque caller-admitted replay bytes.

The frozen chain does not prove:

- replay parsing
- parser-success logic
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- raw-state payload parsing
- export widening

`source_replay`, `source_replay.provenance_label`, and `audited_family_root_directory` remain
lineage and receipt anchors only. They are not replay paths, replay storage roots, locator inputs,
or parser-readiness proof.

## D. AUDITED SURFACE

The audited Rust surface relevant to this pass is:

- `mimir-skill` owns the low-boost-recovery ReplayInput-creation contract and realization types.
- The realized per-specimen output preserves a created `mimir_replay::ReplayInput`.
- The only admitted created input form is `ReplayInput::Memory { label, bytes }`.
- `mimir-replay` exposes:
  - `ReplayInput`
  - `ReplayHeader`
  - `ReplayReader`
  - `UnsupportedReplayReader`
- `UnsupportedReplayReader` still returns an explicit error and is not a parser.
- `mimir-io` exposes artifact read/write helpers and no replay-source carrier discovery, replay
  locator, or replay parser implementation.
- `mimir-export` remains export-bundle and execution-result infrastructure. It has no current
  low-boost-recovery ReplayInput, replay parsing, raw-state, or widened BC export path.
- `mimir-types` still keeps low-boost-recovery BC payloads reference-bound at this layer. It does
  not define parsed replay frames or raw-state payloads.

The Cargo dependency edges relevant to this pass are:

- `mimir-skill` depends on `mimir-replay`, `mimir-io`, `mimir-types`, `mimir-core`, and `serde`.
- `mimir-replay` depends on `mimir-core`, `mimir-types`, and `serde`.
- `mimir-io` depends on `mimir-core`, `mimir-score`, `mimir-types`, `serde`, `serde_json`, and
  `toml`.
- `mimir-export` depends on `mimir-anchor`, `mimir-branch`, `mimir-core`, `mimir-io`,
  `mimir-types`, `serde`, `serde_json`, and `toml`.
- `mimir-types` depends only on `serde`.

No crate dependency change is required for this decision pass.

## E. STILL-CLOSED DOWNSTREAM DOMAINS

The candidate domains evaluated in this pass are:

- actual replay parsing
- parser-success logic
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- raw-state payload parsing
- export widening

At most one may be selected.

## F. PER-DOMAIN ANALYSIS

### Actual Replay Parsing

Does the current realized ReplayInput bridge provide a concrete input surface?

- Yes. The realized bridge carries a per-specimen `ReplayInput::Memory` whose bytes are the exact
  preserved opaque caller-admitted replay bytes.

Does it provide a concrete output expectation?

- Narrowly yes, but only at the parser boundary level already exposed by `mimir-replay`:
  `ReplayReader::read_header(&ReplayInput) -> Result<ReplayHeader>`.
- This is not a raw-state payload expectation.
- This is not parser-success policy.
- This is not proof that the bytes are parseable.

Can it be opened without silently opening another domain first?

- Yes, if opened only as the next downstream domain decision for replay parsing against the
  realized memory input.
- It must not define parser-success policy, raw-state payload parsing, locator logic, carrier
  discovery, or export widening in the same pass.

Can it be opened without forbidden crate changes?

- Yes for this decision pass. No Rust change is required.
- A future contract-definition pass must still decide whether it can stay in `mimir-skill` using
  the existing `mimir_replay::ReplayReader` surface or whether parser implementation work must be
  explicitly scoped later.

Does opening it force replay path or storage semantics?

- No. The admitted input is already `ReplayInput::Memory`.
- No path is derived from `source_replay`, `source_replay.provenance_label`, or
  `audited_family_root_directory`.

Is it more directly justified than every competing domain?

- Yes. It is the only candidate with a concrete parser-consumable input surface already realized
  by the trusted boundary.

### Parser-Success Logic

Does the current realized ReplayInput bridge provide a concrete input surface?

- It provides a memory `ReplayInput`, but it does not provide a parser attempt result.

Does it provide a concrete output expectation?

- No. Parser-success logic needs an actual parser attempt output or failure mode to classify.

Can it be opened without silently opening another domain first?

- No. It would silently depend on actual replay parsing or at least one explicit parse-attempt
  result.

Can it be opened without forbidden crate changes?

- Not honestly in this pass. It would either duplicate the memory bridge or invent parse-success
  semantics that are absent.

Does opening it force replay path or storage semantics?

- Not necessarily, but it would force parser-attempt semantics that are not present.

Is it more directly justified than every competing domain?

- No. It is downstream of actual replay parsing.

### Replay-Source Actual-Materialization Implementation

Does the current realized ReplayInput bridge provide a concrete input surface?

- No for this domain. The bridge already has caller-admitted bytes and creates memory input. It
  does not expose a replay-source carrier to materialize.

Does it provide a concrete output expectation?

- No. The realized bridge does not define file-backed source materialization, carrier identity, or
  storage output.

Can it be opened without silently opening another domain first?

- No. It would need carrier/source semantics that remain absent.

Can it be opened without forbidden crate changes?

- Not as an implementation domain in this pass.

Does opening it force replay path or storage semantics?

- Yes. Actual materialization implementation would need explicit source carrier semantics that the
  admitted boundary does not contain.

Is it more directly justified than every competing domain?

- No. The current bridge bypasses this by preserving caller-admitted bytes as memory input.

### Replay-Source Carrier Discovery

Does the current realized ReplayInput bridge provide a concrete input surface?

- No. It provides memory bytes, not a discoverable storage carrier.

Does it provide a concrete output expectation?

- No. No carrier index, search root, sidecar, manifest, or storage convention is admitted.

Can it be opened without silently opening another domain first?

- No. It would require source-storage semantics that remain forbidden.

Can it be opened without forbidden crate changes?

- Not honestly as a real carrier-discovery domain in this pass.

Does opening it force replay path or storage semantics?

- Yes.

Is it more directly justified than every competing domain?

- No. It is less direct than parsing the already-realized memory input.

### Replay-Input Locator Logic

Does the current realized ReplayInput bridge provide a concrete input surface?

- No for locator logic. It already carries a concrete `ReplayInput::Memory`, so locating an input
  is not the current missing piece.

Does it provide a concrete output expectation?

- No locator output is needed or expected at this boundary.

Can it be opened without silently opening another domain first?

- No. Any locator work would need path, carrier, storage, sidecar, or manifest semantics that the
  realized memory bridge intentionally avoided.

Can it be opened without forbidden crate changes?

- Not honestly as a real locator domain in this pass.

Does opening it force replay path or storage semantics?

- Yes.

Is it more directly justified than every competing domain?

- No. It would move backward from the already-created memory input.

### Raw-State Payload Parsing

Does the current realized ReplayInput bridge provide a concrete input surface?

- No. It provides replay bytes as `ReplayInput::Memory`, not parsed frames or raw-state payloads.

Does it provide a concrete output expectation?

- No. No raw-state payload schema or parser output is admitted above this bridge.

Can it be opened without silently opening another domain first?

- No. It depends on replay parsing and parser-success evidence first.

Can it be opened without forbidden crate changes?

- No honest docs-only decision can make raw-state payload parsing ready from memory input alone.

Does opening it force replay path or storage semantics?

- Not necessarily, but it would force parsed replay semantics that are absent.

Is it more directly justified than every competing domain?

- No. It is downstream of actual replay parsing and parser-success logic.

### Export Widening

Does the current realized ReplayInput bridge provide a concrete input surface?

- No. It provides a memory replay input, not an exportable raw-state, tensor, control, or replay
  parse result.

Does it provide a concrete output expectation?

- No. The bridge defines no `mimir_export` bundle item, manifest entry, index entry, or exported
  low-boost-recovery replay/raw-state payload.

Can it be opened without silently opening another domain first?

- No. Export widening would depend on parser, raw-state, tensor, or consumer semantics that remain
  absent.

Can it be opened without forbidden crate changes?

- No. `mimir_export` widening is explicitly forbidden unless separately reopened.

Does opening it force replay path or storage semantics?

- It would force export storage semantics and likely additional index or manifest semantics.

Is it more directly justified than every competing domain?

- No. It remains the least justified candidate in this pass.

## G. DECISION

Decision chosen:

- Outcome B: explicitly reopen exactly one downstream closed domain

Selected domain:

- actual replay parsing

This is a domain reopen only. It is not a parser implementation, not parser-success logic, not
raw-state payload parsing, and not export widening.

## H. WHY ACTUAL REPLAY PARSING WINS

Actual replay parsing is uniquely justified because:

1. It is the only candidate whose direct input is already realized by the trusted boundary:
   `ReplayInput::Memory`.
2. It can consume that input without reinterpreting lineage fields as paths or storage.
3. It is directly downstream of memory ReplayInput creation.
4. It does not require replay-source carrier discovery or replay-input locator logic first.
5. It remains earlier than parser-success policy and raw-state payload parsing.
6. It remains unrelated to `mimir_export` widening.

This decision does not claim parser readiness. It only says the next single downstream domain to
reopen is actual replay parsing because a parser-consumable memory input now exists.

## I. WHY COMPETING DOMAINS REMAIN CLOSED

Parser-success logic remains closed because no parser attempt result exists yet.

Replay-source actual-materialization implementation remains closed because the realized memory
input does not define a replay-source carrier or storage target.

Replay-source carrier discovery remains closed because the bridge preserves caller-admitted bytes
and introduces no discoverable storage surface.

Replay-input locator logic remains closed because the bridge already created a memory input and no
locator path, root, sidecar, manifest, or carrier semantics are needed or admitted.

Raw-state payload parsing remains closed because no parsed replay frame or raw-state payload
surface exists.

Export widening remains closed because no parsed payload, tensor, control, export item, or
consumer-ready widened export semantics exist. `mimir_export` widening remains forbidden unless
explicitly reopened.

## J. WHY NO RUST IS ADDED

No Rust is added in this pass because Outcome B is a reopen decision, not a contract definition or
implementation. Adding types now would prematurely define actual replay parsing semantics before
the next contract-definition pass accounts for:

- exact parser input tuple
- exact reader surface
- exact parser output boundary
- explicit failure behavior
- whether `ReplayHeader` is sufficient for the first parsing contract
- how parser attempts remain separate from parser-success policy

Docs-only is more honest because the decision is clear, but the parser contract is not yet defined.

## K. DEFERRED WORK

The next pass may define exactly one low-boost-recovery actual replay parsing contract boundary
above:

- `LowBoostRecoveryBcReceiptBoundValidatedSpecimenFileRawStateWindowReplayInputCreationFromOpaqueCallerAdmittedReplayBytesRealizationResultV1`

That next pass must still not implement replay parsing unless explicitly authorized by its own
scope.

Deferred beyond this decision:

- parser-success logic
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- raw-state payload parsing
- tensor/control materialization
- corpus-wide replay ingestion
- runtime CLI behavior
- `mimir_export` widening

## L. FORBIDDEN WORK

This pass forbids:

- replay parsing implementation
- parser-success logic
- replay-source actual-materialization implementation
- replay-source carrier discovery
- replay-input locator logic
- raw-state payload parsing
- export widening
- generic all-family replay/raw-state/index/export/materialization framework creation
- reinterpretation of `source_replay` as a replay path
- reinterpretation of `source_replay.provenance_label` as a replay path
- reinterpretation of `audited_family_root_directory` as replay storage
- changes to `mimir-replay`
- changes to `mimir-io`
- changes to `mimir-export`
- changes to `mimir-types`

`mimir_export` widening remains forbidden unless explicitly reopened.

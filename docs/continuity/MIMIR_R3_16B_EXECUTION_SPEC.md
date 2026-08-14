# MIMIR — R3.16B Execution Spec

**Date:** 2026-08-14  
**Pass:** `R3.16B — native existing-actor first-property envelope header implementation`  
**Kind:** narrow production implementation  
**Admitted evidence:** `R3.16A Outcome A`  
**Frozen production base before this pass:** `bf4bccff82203ed049d33e942681fed07f23beb4`

## 1. Goal

Implement the smallest native production reader extension proven by R3.16A for one existing-actor first-property envelope.

The admitted prefix is:

```text
existing actor (`new == false`)
property_present
bounded stream_id
resolved actor/object lookup context
resolved property object ID / property name
attribute tag
payload_start_bit
```

The implementation must stop **before consuming the selected attribute payload**.

R3.16B is not a full property-loop pass and is not an attribute decoder pass.

## 2. Frozen evidence identity

Implementation and differential tests must treat the following R3.16A result as the frozen oracle/admission source:

```text
R3.16A base main SHA       = 76cbcc2094189e637e135f8c7d99e999e32311a0
R3.16A evidence head       = 31b858de7d855cbc32501e03282c8db6bf68ecd0
R3.16A final CI run/job    = 31748905111 / 94609885915
R3.16A receipt terminal    = R3_16A_RECEIPT_STREAM=PASS
pinned Boxcars SHA         = c70e77df7af81b436cb545d070bb90c82f562d0b
selected replay rows       = 47
mismatch_count             = 0
```

The exact R3.16A job log is the immutable receipt stream. It contains 13 bounded evidence records. No separate R3.16A Actions artifact ID exists or may be invented.

## 3. Allowed production surface

R3.16B may modify only the smallest replay production/test surface required for the new first-property header reader, expected primarily in:

```text
crates/mimir-replay/src/lib.rs
```

Focused replay tests may be added/updated as needed.

Cargo manifests, `Cargo.lock`, replay corpus/fixtures, unrelated crates, export surfaces, and permanent oracle dependencies are forbidden unless a separately documented blocking requirement proves they are necessary. The default outcome for an incidental dependency change is rejection, not convenience.

## 4. Required native branch

Starting from the already admitted first actor envelope, R3.16B may advance only when the selected actor is alive and existing:

```text
actor_present == true
alive == true
new == false
```

Then:

1. consume exactly one `property_present` bit;
2. if `property_present == false`, stop at that branch endpoint with no property envelope;
3. if `property_present == true`, resolve the actor/object lookup context already admitted by `ReplayNetworkLookupPlanV1`;
4. use the object's admitted `max_prop_id` / bound context;
5. consume one `stream_id` with the existing canonical bounded-u32 primitive;
6. resolve that stream through the object's effective inherited/static property lookup;
7. materialize only structural property metadata needed by this pass;
8. record the exact `payload_start_bit`;
9. **stop without reading the attribute payload**.

## 5. Bounded stream-ID rule

Do not implement stream IDs as `read_bits(prop_id_bits)`.

R3.16A observed:

```text
prop_id_bits:
  4 -> 7 rows
  5 -> 38 rows
  6 -> 2 rows

actual bounded stream-ID consumption:
  5 bits -> 11 rows
  6 bits -> 35 rows
  7 bits -> 1 row
```

The existing canonical value-dependent bounded integer primitive admitted in R3.14B/R3.14C must be reused. A second almost-identical decoder is forbidden.

## 6. Lookup resolution contract

The stream must resolve through the existing admitted lookup-plan family, not through a copied Boxcars table or a new hidden resolver.

Required context comes from the current `ReplayNetworkLookupPlanV1` / object lookup surface, including the already admitted effective inherited property mapping and its bound context.

For `property_present == true`:

```text
stream_id must be in the admitted bound
stream_id must resolve for the selected actor context
resolved property object ID must be valid
resolved property/tag metadata must match the frozen R3.16A row
```

Unresolved/invalid conditions fail closed. Do not substitute property 0, an empty tag, or a guessed payload type.

## 7. Candidate output boundary

The exact production type name is an implementation choice after fresh source inspection, but the result must remain narrow and versioned/explicit enough to represent, as applicable:

```text
existing actor envelope context
property_present
stream_id optional
resolved_property_object_id optional
resolved_property_object_name optional or lookup-derived diagnostic equivalent
resolved_attribute_tag optional
property envelope stop / payload_start_bit
```

Do not add fields for decoded attribute values, reconstructed actor state, semantic game state, events, or skills.

## 8. Required tests

At minimum cover:

```text
[ ] existing actor + property_present=false exact stop
[ ] existing actor + property_present=true exact bounded stream decode
[ ] inherited/static stream resolution
[ ] invalid/unresolved stream fails closed
[ ] truncation at property_present
[ ] truncation inside bounded stream low bits
[ ] truncation at value-dependent discriminator when required
[ ] no payload bit consumed after successful resolution
[ ] prior NewActor reader behavior unchanged
[ ] prior alive=false / actor_present=false branches unchanged
[ ] deterministic repeatability
```

Synthetic tests may establish surgical error branches, but the production claim also requires the frozen 47-replay differential below.

## 9. Frozen 47-replay differential gate

For each R3.16A selected row, the native implementation must match the frozen oracle/admission record for every field the production surface exposes, at minimum:

```text
property_present_value
stream_id_value
resolved_property_object_id
resolved_attribute_tag
payload_start_bit
```

Where available and stable, also compare:

```text
property_present_start_bit
property_present_end_bit
stream_id_start_bit
stream_id_end_bit
stream_id_bound
prop_id_bits/bound context
```

Admission target:

```text
replays = 47
native_success = 47
identity errors = 0
lookup errors = 0
field mismatches = 0
payload-start mismatches = 0
```

Any unexplained mismatch blocks publication.

## 10. Regression gate

R3.16B must preserve all already admitted lanes:

```text
R3.14C bit cursor / bounded integer primitive
R3.14D first actor envelope through `new`
R3.14E 47-replay first-envelope admission
R3.15C first NewActor spawn trajectory reader
R3.15D first-NewActor 47-replay differential
R3.13 static/inherited lookup plan
```

The implementation must be additive. Existing public behavior must not silently change to make the new test pass.

## 11. Full validation

Before a clean production source commit is considered publishable, run the repository's current exact verifier. At minimum the current lane is expected to include:

```text
cargo fmt --all -- --check
cargo check workspace/all-targets/all-features
mimir-replay tests
workspace tests
cargo clippy -- -D warnings
replay corpus identity/size verification
knowledge/continuity verification where triggered
repository verification wrapper
```

Current workflow/scripts, not this prose, are authoritative if the verifier evolves.

Native command failures must be propagated explicitly in PowerShell evidence/validation wrappers.

## 12. Clean publication policy

Temporary oracle code, evidence scripts, generated rows, logs, or workflows must not enter the clean production commit.

Required sequence:

```text
fresh admitted main
→ disposable R3.16B implementation/evidence branch
→ focused implementation + differential validation
→ source-scope audit
→ reconstruct only admitted production/test changes on fresh main ancestry
→ exact-SHA full validation
→ fresh-main ancestry recheck
→ force=false publication
→ exact published-main CI/readback
→ R3.16C continuity/check
```

If `main` advances with relevant source while R3.16B is in flight, do not force or blindly replay the patch. Reconcile against fresh source first.

## 13. Hard stop

R3.16B remains closed to:

```text
attribute payload consumption of any tag
RigidBody payload decoding
ActiveActor payload decoding
Byte/Float/Int payload decoding
property loop iteration / second property
complete existing-actor update parsing
next actor iteration
next frame iteration
actor lifecycle state mutation
raw state
events
replay slicing
skills
counterfactual execution
training/runtime/export widening
support-lane expansion
new production dependency
```

The fact that R3.16A observed `RigidBody`, `ActiveActor`, `Byte`, `Float`, and `Int` tags does not admit their wire payloads.

## 14. Outcome rules

### Outcome A — implementation exact

The narrow native first-property header matches the frozen R3.16A 47-row evidence exactly, all regression/full gates pass, scope is clean, and the hard payload boundary remains intact.

Proceed to roadmap-defined `R3.16C — implementation continuity/check`.

### Outcome B — bounded implementation/evidence gap

A reproducible branch cannot be represented by the admitted first-property header contract without widening or clarifying one narrow rule. Preserve evidence and open only the smallest targeted follow-up. Do not decode payloads as a workaround.

### Outcome C — contradiction/regression

The implementation contradicts admitted evidence, changes previous production behavior, cannot preserve exact cursor accounting, or requires unexplained dependency/scope drift. Stop and reopen the relevant earlier assumption. Do not publish.

## 15. Exit record required

R3.16B closure must record at least:

```text
base main SHA
implementation/evidence head
clean production SHA
changed production files
source blob/SHA identity
focused test counts
47-replay differential counts
full verifier run/job
published-main CI/readback
production/Cargo/corpus mutation audit
hard-stop statement
next exact pass = R3.16C
```

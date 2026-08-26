# MIMIR R3.18AT — Post-AQ Mixed-Continuation Following-Header Exact-Context Contract

**Status:** ACTIVE
**Pass type:** contract-only admission
**Evidence authority:** R3.18AS Outcome A
**Production authority:** R3.18AQ `e1ccbef95c8424b689dee7d77fd8fde2af3e0204` / `4e7100625096594bcc5c5b4c6a8054c283643b13`
**Production mutation:** forbidden
**Payload decode:** forbidden
**Second later control:** forbidden

## Goal

Turn the immutable R3.18AS true-sublane header observation into the narrowest boundary-specific exact-context contract. Exactly forty AQ-true rows contribute header contexts. The seven AQ-false rows remain terminators and contribute no header tuple.

## Frozen evidence authority

```text
canonical continuity base            34897d5c7c24bd6ecba526fb3e951681a69d18c6 / bb2e1ba77432af772f15f32a85c334f1dc2e6bf9
production SHA/tree                  e1ccbef95c8424b689dee7d77fd8fde2af3e0204 / 4e7100625096594bcc5c5b4c6a8054c283643b13
AS evidence head/tree                475650fea59332f74b9f69da50e3e4471622ab7e / 1303071ad3031f4095e29d775afd243286a67b64
AS authority run/job                 32959321642/98147938829 SUCCESS
AS same-head CI                      32959321531/98147938016 SUCCESS / count=1 / rerun=0
AS artifact                          9603335255 / 13250 / sha256:0642a4c6c6e57edad8e23dc93bdff96f54ed9563633ebe63c332a8ecbac40a45
AS manifest file SHA-256             638f314ea585aa0ad33ea0b2ca7417687139fd67f4a27e04813348210009ae4a
AS header rows / summary             b7f9b50935aa559011152c0722a24441d590f262ff2a69e85a51636605b89086 / ecb49bf9ee38d4249b3e6d91c5dec7ceb2288b6ed6452dbbb3dce3304d371a38
AS continuation / terminator hashes  3733514eeceea2ae80b5a4a6c3435c210ab3268901bae7be39e9ab1152860900 / 1af0a82eb9ba5a7b65755a99959f1754e1839db0cc61d90eb414e3ee9fedef27
AS frozen rows                       47
AS false terminators / true headers  7 / 40
AS unique exact contexts             16
AS observed tags                     Int=40
AS mismatch / reselection            0 / 0
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
Boxcars instrumentation patch        abd386097cc2bd22bdd685f67c13687cd6a3330b12944a43d8d30da109a8e50e
```

Any source/artifact/witness drift stops the pass.

## Required contract artifact

Create `docs/continuity/MIMIR_R3_18AT_ADMITTED_HEADER_CONTEXTS.json` with:

- schema version and a boundary-specific post-AQ mixed-continuation contract name;
- membership policy `exact_tuple_only`;
- tuple fields exactly `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)`;
- frozen lane row count 47;
- false terminator count 7;
- observed header row count 40;
- unique exact context count 16;
- exact R3.18AS authority receipts and durable hashes;
- exactly the 16 observed tuples and exact observed multiplicities;
- explicit flags that false terminators produce no header membership;
- explicit anti-widening flags, including no AJ/Z/P inheritance and no RL223-field dropping.

## Admission semantics

Membership is complete eight-field equality only. Multiplicity is evidence provenance, not a runtime frequency guarantee. The seven false AQ rows are terminators and are not contract members.

Even though every AS header is `Int` and every AS row is `868.32 / net10 / is_rl_223=false`, none of those shared components may replace complete tuple equality.

## Required validation and negatives

At minimum prove:

1. exact 16/16 tuple equality against immutable AS header summary;
2. exact 16/16 multiplicities and sum 40;
3. exact 7/7 false terminator identities remain outside header membership;
4. tag-only candidate rejection;
5. component-only candidate rejection;
6. fabricated Cartesian candidate rejection;
7. version-drop candidate rejection;
8. `is_rl_223` field drop and false→true flip rejection;
9. fabricated seventeenth tuple rejection;
10. an R3.18AJ-valid but R3.18AT-absent tuple such as `(60,5,38,Int,868,32,10,false)` rejects at this later boundary;
11. production/Cargo/fixture/corpus/support mutation remains `0/0/0/0/0`;
12. knowledge archive verifier and JSON/schema consistency PASS.

## Clean scope

Contract/continuity docs only. No Rust production source, tests, Cargo manifest/lockfile, dependency, fixture, corpus, workflow, support lane or runtime/export widening belongs in the clean contract commit.

## Duplicate-CI rule

Before any dispatch/rerun inspect queued/waiting/in-progress runs for the same SHA/workflow/input. Reuse an equivalent run. Rerun is not polling.

## Hard stop

R3.18AT does not publish a post-AQ following-header composition. It does not decode the following payload, read another property-control bit, synthesize a header for a false terminator, create a repeated/generalized property loop/cursor, iterate another actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, execute counterfactuals or widen runtime/export behavior.

## Outcome gate

### Outcome A
Admit exactly the 16 eight-field contexts with multiplicities summing to 40, preserve 7 false terminators outside membership, and pass all anti-widening/mutation/archive gates. Production remains R3.18AQ. A later separate R3.18AU production pass may compose exactly one following header only for an AQ-true result, require exact R3.18AT membership, and stop at `payload_start`.

### Outcome B
A bounded tuple/multiplicity/terminator discrepancy is isolated. Admit only supported facts and keep production following-header composition closed.

### Outcome C
Authority drift, witness reselection, false-terminator header synthesis, older-contract inheritance, tuple/RL223 widening, payload/later-control access or production mutation. Stop without admission.

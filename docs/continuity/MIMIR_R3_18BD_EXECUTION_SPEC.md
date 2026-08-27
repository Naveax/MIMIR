# MIMIR R3.18BD — Exact Following-Header Context Contract After R3.18BC

**Status:** ACTIVE
**Pass type:** contract-only admission
**Evidence authority:** R3.18BC Outcome A
**Production authority:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden

## Goal

Turn the immutable R3.18BC three-row true-sublane header observation into the narrowest boundary-specific exact-context contract. The full BB/BC lane remains forty rows: 37 false BA controls are terminators and contribute no header membership; exactly three true rows contribute exactly three observed complete contexts.

R3.18BD does not compose a header in production. It only freezes exact context membership so a later separate production pass can require that membership before composing one header.

## Frozen evidence authority

```text
canonical continuity base             2296eb7eb93ac4946bb5b7152f5bc76ff4bf09d8 / 27b40170f2193d972bccf618ee6e2ef7f36806fb
production SHA/tree                   5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BC evidence head/tree                 0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
BC authority run/job                  33122152803 / 98691409657 SUCCESS
BC same-head natural CI               33122152793 / 98691409674 SUCCESS
BC artifact                           9666964713 / 7795 / sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
BC manifest SHA-256                   d9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf
BC frozen rows                        40
BC false terminators / true headers   37 / 3
BC unique exact contexts              3
BC observed tags                      Boolean=2 / Float=1
BC mismatch / reselection             0 / 0
BC payload / second-control bits      0 / 0
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

Any authority, witness, tuple, multiplicity, or terminator drift stops the pass.

## Required contract artifact

Create `docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json` with:

- schema version and a boundary-specific post-BA mixed-continuation contract name;
- membership policy `exact_tuple_only`;
- tuple fields exactly `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)`;
- frozen lane row count 40;
- false terminator count 37;
- observed header row count 3;
- unique exact context count 3;
- exact R3.18BC authority receipts and durable hashes;
- exactly the three observed tuples below and exact observed multiplicity 1 each;
- explicit flags that false terminators produce no header membership;
- explicit anti-widening flags against tag-only, component-only, Cartesian, versionless, RL223-field-dropping, earlier-contract inheritance, and fabricated fourth-tuple membership.

## Exact candidate membership

```text
(72,  6, 92, Boolean, 868, 32, 10, false) x1
(72,  6, 94, Boolean, 868, 32, 10, false) x1
(110, 6, 58, Float,   868, 32, 10, false) x1
```

Membership is complete eight-field equality only. Multiplicity records evidence provenance and is not a runtime frequency guarantee. Boolean-only, Float-only, ordinal-6-only, version-only, bound-only, or any Cartesian recombination is insufficient.

## Required validation and negatives

At minimum prove:

1. exact 3/3 tuple equality against immutable BC header summary;
2. exact multiplicity 1/1/1 and sum 3;
3. exact 37/37 false terminators remain outside header membership;
4. tag-only candidate rejection;
5. component-only candidate rejection;
6. fabricated Cartesian candidate rejection;
7. version-drop candidate rejection;
8. `is_rl_223` field drop and false→true flip rejection;
9. fabricated fourth tuple rejection;
10. an earlier R3.18AT/AJ/Z/P-valid but R3.18BD-absent tuple rejects at this boundary;
11. production/Cargo/fixture/corpus/support mutation remains `0/0/0/0/0`;
12. JSON/schema consistency and knowledge archive verifier PASS.

## Clean scope

Contract/continuity docs only. No Rust production source, tests, Cargo manifest/lockfile, dependency, fixture, corpus, workflow, support lane, payload decoder, or runtime/export widening belongs in the clean R3.18BD contract commit.

## Duplicate-CI rule

Before any dispatch/rerun inspect queued/waiting/in-progress runs for the same SHA/workflow/input. Reuse an equivalent run. Rerun is not polling.

## Hard stop

No production following-header composition, no following payload decode, no second later property control, no synthesized header for a false terminator, no repeated/generalized property loop/cursor, no next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A

Admit exactly the three eight-field contexts with multiplicities summing to 3, preserve 37 false terminators outside membership, and pass all anti-widening/mutation/archive gates. Production remains R3.18BA. A later separate R3.18BE production pass may compose exactly one following header only after a valid published BA true result, require exact R3.18BD membership, and stop at `payload_start`.

### Outcome B

A bounded tuple/multiplicity/terminator discrepancy is isolated. Admit only supported facts and keep production following-header composition closed.

### Outcome C

Authority drift, witness reselection, false-terminator header synthesis, older-contract inheritance, tuple/RL223 widening, payload/later-control access, production mutation, or generalized chaining. Stop without admission.

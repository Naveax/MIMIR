# MIMIR R3.18BN — Exact Following-Header Context Contract After R3.18BM

**Status:** ACTIVE
**Pass type:** contract-only admission
**Evidence authority:** R3.18BM Outcome A
**Production authority:** R3.18BK `f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf` / `07656c7a43c1afb97903ef33c1109b764fbf8b7d`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden

## Goal

Turn the immutable R3.18BM two-row true-sublane header observation into the narrowest boundary-specific exact-context contract. The full BL/BK lane remains three rows: one false BK control is a terminator outside header membership, while exactly two true rows contribute exactly two observed complete contexts.

R3.18BN does not compose a header in production. It only freezes exact context membership so a later separate production pass can require that membership before composing one header.

## Frozen evidence authority

```text
canonical continuity base             607361a67b7eb03a868114b0171f30a6d26873e6 / 8a83d5d80b39d79cc7d3fc8612d02bd911e3446e
production SHA/tree                   f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf / 07656c7a43c1afb97903ef33c1109b764fbf8b7d
BM evidence head/tree                 689b1a24b57a84c81dc19c9a308fb1423f191c4b / 1d4e95409e1125b01a78aae6a436190b3c1381f4
BM authority run/job                  34334615939/102410984005 SUCCESS
BM same-head natural CI               34334615886/102411487443 SUCCESS
BM artifact                           10097405795 / 8340 / sha256:bd51a612be2cdd87d9ce1eb141f3f77f47ae29d42aabc8fc16c260a175f27963
BM inner manifest                     sha256:167021cca2259c4d2ef16e9da50503007f381349219adb0f5684849f69f2cbd2 / 13/13 PASS
BM frozen rows                        3
BM false terminators / true headers   1 / 2
BM unique exact contexts              2
BM observed tags                      Boolean=1 / ActiveActor=1
BM property ordinal                   7 on 2/2
BM mismatch / reselection             0 / 0
BM payload / second-control bits      0 / 0
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

Any authority, witness, tuple, multiplicity, or terminator drift stops the pass.

## Required contract artifact

Create `docs/continuity/MIMIR_R3_18BN_ADMITTED_HEADER_CONTEXTS.json` with:

- schema version and a boundary-specific post-BK mixed-continuation contract name;
- membership policy `exact_tuple_only`;
- tuple fields exactly `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)`;
- frozen lane row count 3;
- false terminator count 1;
- observed header row count 2;
- unique exact context count 2;
- exact R3.18BM authority receipts and durable hashes;
- exactly the two observed tuples below and exact observed multiplicity 1 each;
- explicit flags that false terminators produce no header membership;
- explicit anti-widening flags against tag-only, component-only, Cartesian, versionless, RL223-field-dropping/flipping, earlier-contract inheritance, and fabricated third-tuple membership.

## Exact candidate membership

```text
(72,  6, 95, Boolean,     868, 32, 10, false) x1
(110, 6, 66, ActiveActor, 868, 32, 10, false) x1
```

Membership is complete eight-field equality only. Multiplicity records evidence provenance and is not a runtime-frequency guarantee. Boolean-only, ActiveActor-only, ordinal-7-only, version-only, bound-only, or any Cartesian recombination is insufficient.

## Required validation and negatives

At minimum prove:

1. exact 2/2 tuple equality against immutable BM header summary;
2. exact multiplicity 1/1 and sum 2;
3. exact 1/1 false terminator remains outside header membership;
4. tag-only candidate rejection;
5. component-only candidate rejection;
6. fabricated Cartesian candidate rejection, e.g. `(72,6,66,ActiveActor,868,32,10,false)`;
7. version-drop / version-mutation candidate rejection;
8. `is_rl_223` field drop and false→true flip rejection;
9. fabricated third tuple rejection, e.g. `(72,6,999,Boolean,868,32,10,false)`;
10. an earlier R3.18BD-valid but R3.18BN-absent tuple rejects here, e.g. `(72,6,92,Boolean,868,32,10,false)`;
11. production/Cargo/fixture/corpus/support mutation remains `0/0/0/0/0`;
12. JSON/schema consistency and knowledge archive verifier PASS.

## Clean scope

Contract/continuity docs only. No Rust production source, tests, Cargo manifest/lockfile, dependency, fixture, corpus, workflow, support lane, payload decoder, or runtime/export widening belongs in the clean R3.18BN contract commit.

## Duplicate-CI rule

Before any dispatch/rerun inspect queued/waiting/in-progress runs for the same SHA/workflow/input. Reuse an equivalent run. Rerun is not polling.

## Hard stop

No production following-header composition, no following payload decode, no second later property control, no synthesized header for the false terminator, no repeated/generalized property loop/cursor, no next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A

Admit exactly the two eight-field contexts with multiplicities summing to 2, preserve the one false terminator outside membership, and pass all anti-widening/mutation/archive gates. Production remains R3.18BK. A later separate **R3.18BO** production pass may compose exactly one following header only after a valid published BK true result, require exact R3.18BN membership, return the BK-false row as a successful no-header terminator, and stop exactly at `payload_start`.

### Outcome B

A bounded tuple/multiplicity/terminator discrepancy is isolated. Admit only supported facts and keep production following-header composition closed.

### Outcome C

Authority drift, witness reselection, false-terminator header synthesis, older-contract inheritance, tuple/RL223 widening, payload/later-control access, production mutation, or generalized chaining. Stop without admission.

# MIMIR R3.18P Execution Spec — Following-Property Header Context Contract

Date: 2026-08-17  
Pass type: **contract-only / no production code change**

## Goal

Convert the admitted R3.18O following-header evidence into one canonical, privacy-safe exact structural-context contract without widening the observed domain.

## Frozen authority

- base production: `fd74ba8c520ab83b808730572c41e45d6dc616e6` (R3.18M)
- R3.18O evidence head: `5046e1594b87ce2828db5faa48aceba456c3166f`
- R3.18O run/job: `32017369100` / `95349613184` — SUCCESS
- same-head normal CI: `32017369071` / `95349613066` — SUCCESS
- artifact: `9284144768` / `sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d` / `25129` bytes
- source-summary SHA-256: `f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc`
- header-rows SHA-256: `599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4`
- aggregate SHA-256: `170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233`
- exact frozen lane: 47 rows, witness reselection 0

## Required contract artifact

Create `docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json` with:

- schema/version metadata;
- R3.18O authority receipts above;
- `observed_row_count = 47`;
- `unique_exact_context_count = 18`;
- exactly the 18 unique tuples `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)`;
- exact observed multiplicity for every tuple;
- explicit policy: only exact tuple membership is admitted; multiplicity is provenance, not a production frequency promise.

The canonical candidate tuple set is:

| stream_id_bound | prop_id_bits | property object index | attribute tag | version | observed rows |
|---:|---:|---:|---|---|---:|
| 60 | 5 | 32 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 41 | `Boolean` | `868.32 / net10` | 2 |
| 60 | 5 | 78 | `Boolean` | `868.32 / net10` | 4 |
| 60 | 5 | 79 | `Boolean` | `868.32 / net10` | 19 |
| 60 | 5 | 80 | `ActiveActor` | `868.32 / net10` | 6 |
| 60 | 5 | 83 | `ActiveActor` | `868.32 / net10` | 1 |
| 60 | 5 | 85 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 87 | `Boolean` | `868.32 / net10` | 2 |
| 60 | 5 | 89 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 94 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 102 | `Boolean` | `868.32 / net10` | 2 |
| 60 | 5 | 103 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 106 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 116 | `Boolean` | `868.32 / net10` | 1 |
| 67 | 6 | 61 | `Boolean` | `868.32 / net10` | 1 |
| 72 | 6 | 62 | `Boolean` | `868.32 / net10` | 1 |
| 72 | 6 | 65 | `Boolean` | `868.32 / net10` | 1 |
| 110 | 6 | 36 | `ActiveActor` | `868.32 / net10` | 1 |

## Equality gate

The generated contract must be derived from the immutable R3.18O `r3_18o_source_summary.json` and must prove:

1. artifact ZIP digest exact;
2. inner manifest 11/11 exact;
3. R3.18O source-summary hash exact;
4. `rows=47`, `unique=18` exact;
5. tuple values exact;
6. tuple multiplicities exact and sum to 47;
7. version context remains exactly `868.32 / net10` for all 47 rows;
8. no witness reselection and no new corpus selection.

## Mandatory anti-widening negatives

Reject/fail validation for any proposed contract that:

- accepts `Boolean` or `ActiveActor` by tag alone;
- accepts `stream_id_bound` or `prop_id_bits` by component alone;
- accepts property object index by component alone;
- creates a Cartesian product of individually observed components;
- fabricates an exact tuple by swapping two individually observed object/tag/bound/width values;
- drops version context;
- changes any observed multiplicity;
- adds any nineteenth tuple.

## Scope gate

Allowed clean committed files for the R3.18P milestone:

- `docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json`;
- `docs/continuity/MIMIR_R3_18P_DECISION.md`;
- the next-pass execution spec;
- continuity / knowledge-graph / handoff / ledger files needed to record the admitted milestone.

Forbidden:

- `crates/**` changes;
- `Cargo.toml` / `Cargo.lock` changes;
- fixture/corpus mutation;
- support-table mutation;
- production runtime dependency on Boxcars;
- generic/repeatable property cursor;
- following payload decode;
- another control bit;
- next actor/frame/lifecycle/raw-state/event/slice/skill/runtime/export widening.

## Outcome rule

- **Outcome A:** exact 18-tuple contract is admitted; production stays `fd74ba8c520ab83b808730572c41e45d6dc616e6` and a separate minimal production-composition pass may be opened.
- **Outcome B:** any authority/equality/negative/scope gate fails; admit no contract and do not open production composition.

# MIMIR R3.18O Decision — Following-Property Header Evidence

Date: 2026-08-17  
Outcome: **A — ADMITTED / READ-ONLY EVIDENCE**

## Authority

- fresh base `main`: `c1d68daf989952ccf40645ca99616bccf43bb2f4`
- production remains: `fd74ba8c520ab83b808730572c41e45d6dc616e6` (R3.18M)
- evidence head/tree: `5046e1594b87ce2828db5faa48aceba456c3166f` / `74fb036dfde837e3ecb7e459da00df9ff6c22e28`
- evidence run/job: `32017369100` / `95349613184` — SUCCESS
- same-head normal CI: `32017369071` / `95349613066` — SUCCESS
- immutable artifact: `9284144768` / `25129` bytes
- artifact digest: `sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d`
- pinned Boxcars: `c70e77df7af81b436cb545d070bb90c82f562d0b`

The artifact was independently downloaded from the successful run, its ZIP SHA-256 matched GitHub's artifact digest exactly, and `r3_18o_artifact_sha256.txt` verified **11/11** inner files.

## Result

The exact frozen R3.18N lane was reused without witness reselection:

- frozen rows: **47/47**
- R3.18J reconstruction exact: **47/47**
- published R3.18M following-control exact: **47/47**
- following property header native/oracle exact: **47/47**
- native/oracle mismatch: **0**
- witness reselection: **0**
- observer following-payload bits consumed: **0**
- observer another-control bits consumed: **0**
- production/Cargo/fixture/corpus/support mutation: **0/0/0/0/0**
- privacy gate: **PASS**

Every frozen row was `868.32 / net10`. The observed following-header domain contains **18 exact structural context tuples** across 47 rows:

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

Aggregate tag distribution: `Boolean=39`, `ActiveActor=8`.  
`prop_id_bits`: `5=43`, `6=4`.  
`stream_id_bound`: `60=43`, `67=1`, `72=2`, `110=1`.

## Negative controls

All required controls passed:

- truncation before following `property_present`: 47/47
- truncation before following stream-id completion: 47/47
- prior R3.18M stop mismatch: 47/47
- wrong unresolved actor-stream context: 47/47
- outside exact observed property/tag/context tuple: PASS
- repeatability: 47/47
- post-`payload_start` poison invariance: 47/47

The evidence observer stops exactly at the following property's `payload_start`. Boxcars may continue its own replay parse after the instrumentation point; that does **not** widen the MIMIR observer boundary.

## Immutable inner receipts

- `r3_18o_source_scope.txt`: `f0e12fcd241779c9e0d4d362e5364b309aacafc86d00b188816ab081d4156fa4`
- `r3_18o_replay_identity.tsv`: `b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf`
- `r3_18o_frozen_witnesses.json`: `99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7`
- `r3_18o_r318n_authority_sha256.txt`: `54d12c79d829f74f139f3490c38d4886faea0dabad86e7e2bf4c8a70f164c735`
- `r3_18o_boxcars_instrumentation_sha256.txt`: `8b85d625067b7bc27e585aa5cf21e6f182c79212d6923b881197bce3cabc9848`
- `r3_18o_source_summary.json`: `f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc`
- `r3_18o_targets.tsv`: `448a6402f24fa9d8ba8ebdaa0cf8f8de34970a50d25b8705d9de7f21c198ad0b`
- `r3_18o_oracle_header_rows.json`: `c4a8e5ef1df2bdfee34b1d97dc08c75ee19d843bd1ceb012e1cb7feb7da509e9`
- `r3_18o_header_rows.json`: `599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4`
- `r3_18o_negative_controls.txt`: `5bb2b701b4156b53468a064c75e9259acb4264312bdf41274452633c5b4a73c0`
- `r3_18o_aggregate.txt`: `170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233`

## Admission

R3.18O is admitted as **evidence only**. No production Rust capability changes.

The 18 observed tuple identities are evidence-supported candidates, not a tag-only, bound-only, object-only, Cartesian-product, or generic following-property-header production contract. In particular, seeing `Boolean` or `ActiveActor` here does not make those tags universally valid in arbitrary actor/property/version contexts.

## Next exact pass

**R3.18P — Following-Property Header Context Contract**.

R3.18P is contract-only. It must crystallize the exact 18 observed structural tuples and their 47-row multiplicities from the immutable R3.18O artifact into one privacy-safe committed contract artifact, prove exact logical equality back to R3.18O, and keep production code frozen. Only a later separately admitted production pass may compose the header.

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
- artifact digest: `sha256:e6dc02f087395e2d6b5fb568233484430feba51223848367edd2c6cf15b4b94d`
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
| 60 | 5 | 12 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 13 | `Boolean` | `868.32 / net10` | 2 |
| 60 | 5 | 14 | `ActiveActor` | `868.32 / net10` | 3 |
| 60 | 5 | 17 | `Boolean` | `868.32 / net10` | 3 |
| 60 | 5 | 18 | `Boolean` | `868.32 / net10` | 3 |
| 60 | 5 | 19 | `Boolean` | `868.32 / net10` | 7 |
| 60 | 5 | 21 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 22 | `Boolean` | `868.32 / net10` | 2 |
| 60 | 5 | 23 | `Boolean` | `868.32 / net10` | 8 |
| 60 | 5 | 27 | `ActiveActor` | `868.32 / net10` | 3 |
| 60 | 5 | 30 | `ActiveActor` | `868.32 / net10` | 2 |
| 60 | 5 | 42 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 43 | `Boolean` | `868.32 / net10` | 1 |
| 60 | 5 | 44 | `Boolean` | `868.32 / net10` | 3 |
| 60 | 5 | 54 | `Boolean` | `868.32 / net10` | 3 |
| 67 | 6 | 37 | `Boolean` | `868.32 / net10` | 1 |
| 72 | 6 | 15 | `Boolean` | `868.32 / net10` | 2 |
| 110 | 6 | 44 | `Boolean` | `868.32 / net10` | 1 |

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

- `r3_18o_source_scope.txt`: `6120672ca758c4d951e63cb6c5e3dc4cdd003dc7438319c9d459a36331f0e123`
- `r3_18o_replay_identity.tsv`: `b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf`
- `r3_18o_frozen_witnesses.json`: `99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7`
- `r3_18o_r318n_authority_sha256.txt`: `8f933b6601538d79624969e38290297389bcba217908c0b7ecd3526b807bd547`
- `r3_18o_boxcars_instrumentation_sha256.txt`: `f76e15fb1cec92e5f2604b2ace1be194446eda88613527dbfe1015fbceb815cb`
- `r3_18o_source_summary.json`: `a261368f51770efee56e3d8d760390f633b6190bed81446feaf57b076189ae01`
- `r3_18o_targets.tsv`: `03e6d06c5435013df92ba9d1bcf799816352718795c6a02ece0ae97ea8336adb`
- `r3_18o_oracle_header_rows.json`: `458329fb7924805774056c3187032c6149401143d31ff8f0f8d055bafa0cc625`
- `r3_18o_header_rows.json`: `503bae96ac51ff27532fc80b5e537b3cb7ccd58cea1584a9a1f975da8a4748a9`
- `r3_18o_negative_controls.txt`: `5993bff36da50dbb19a75dc7a42d1fc68a57d429636e8776dc972ba244c4b598`
- `r3_18o_aggregate.txt`: `02324f5a0caa68257a0af93999245124242569f8d582ab2aba2f8119fe6cd676`

## Admission

R3.18O is admitted as **evidence only**. No production Rust capability changes.

The 18 observed tuple identities are evidence-supported candidates, not a tag-only, bound-only, object-only, Cartesian-product, or generic following-property-header production contract. In particular, seeing `Boolean` or `ActiveActor` here does not make those tags universally valid in arbitrary actor/property/version contexts.

## Next exact pass

**R3.18P — Following-Property Header Context Contract**.

R3.18P is contract-only. It must crystallize the exact 18 observed structural tuples and their 47-row multiplicities from the immutable R3.18O artifact into one privacy-safe committed contract artifact, prove exact logical equality back to R3.18O, and keep production code frozen. Only a later separately admitted production pass may compose the header.

# MIMIR R3.18O Receipt Correction

Date: 2026-08-17  
Type: **continuity / immutable-receipt correction only**

## Why this correction exists

After R3.18O was admitted, a fresh download from the exact GitHub Actions run exposed that the published continuity receipt did not match the authoritative artifact bytes. R3.18P correctly failed its authority gate instead of inheriting those stale values.

Canonical authority is now established by **both** current GitHub artifact metadata and a fresh `gh run download` from run `32017369100`, artifact `9284144768`.

## Correct immutable receipt

- evidence head: `5046e1594b87ce2828db5faa48aceba456c3166f`
- run/job: `32017369100 / 95349613184` — SUCCESS
- artifact: `9284144768` / `25129` bytes
- artifact ZIP SHA-256: `e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d`
- source scope: `f0e12fcd241779c9e0d4d362e5364b309aacafc86d00b188816ab081d4156fa4`
- replay identity: `b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf`
- frozen witnesses: `99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7`
- R3.18N authority file: `54d12c79d829f74f139f3490c38d4886faea0dabad86e7e2bf4c8a70f164c735`
- Boxcars instrumentation receipt: `8b85d625067b7bc27e585aa5cf21e6f182c79212d6923b881197bce3cabc9848`
- source summary: `f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc`
- targets: `448a6402f24fa9d8ba8ebdaa0cf8f8de34970a50d25b8705d9de7f21c198ad0b`
- oracle header rows: `c4a8e5ef1df2bdfee34b1d97dc08c75ee19d843bd1ceb012e1cb7feb7da509e9`
- native header rows: `599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4`
- negatives: `5bb2b701b4156b53468a064c75e9259acb4264312bdf41274452633c5b4a73c0`
- aggregate: `170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233`
- inner-manifest file: `8082c22bdd0606f887700c720913b38b2dff7e758e261d41e22c31a195bb174d`

## Correct exact 18 structural contexts

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

The aggregate facts remain unchanged: 47/47 following headers exact, mismatch 0, `Boolean=39`, `ActiveActor=8`, bounds `60=43, 67=1, 72=2, 110=1`, widths `5=43, 6=4`, all `868.32/net10`, payload/another-control consumption `0/0`.

## Impact

R3.18O **Outcome A remains valid**. No production capability changes. This correction repairs provenance hashes and exact tuple identities only. R3.18P remains active and must derive its contract from this corrected immutable authority.

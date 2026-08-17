# MIMIR R3.18P Decision — Following-Property Header Context Contract

Date: 2026-08-17  
Outcome: **A — ADMITTED / CONTRACT-ONLY**

## Authority

- base main: `a431d57e945505b6b4879475e51fc2c2e1c14df7`
- production remains: `fd74ba8c520ab83b808730572c41e45d6dc616e6` (R3.18M)
- R3.18O evidence: `5046e1594b87ce2828db5faa48aceba456c3166f` / `32017369100/95349613184` SUCCESS
- immutable artifact: `9284144768` / `25129` bytes / `sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d`
- source summary: `sha256:f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc`
- following-header rows: `sha256:599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4`
- aggregate: `sha256:170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233`
- witness reselection: `0`

## Contract

Committed artifact: `docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json`  
SHA-256: `0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b`

The contract contains exactly **18** unique structural tuples and their exact **47-row** observed multiplicities. All tuples retain full `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)` identity. All 47 rows remain `868.32 / net10`.

Admission is **exact tuple membership only**. `Boolean` or `ActiveActor` by tag alone, any individual bound/width/object component, any Cartesian product, any versionless tuple, and any nineteenth tuple remain outside the contract.

## Validation

- immutable O source summary hash exact: PASS
- exact tuple equality: 18/18
- exact multiplicities: 18/18; sum 47
- tag-only negative: PASS
- component-only negative: PASS
- fabricated Cartesian tuple negative: PASS
- version-drop negative: PASS
- nineteenth-tuple negative: PASS
- production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

## Admission boundary

R3.18P changes no production Rust capability. It only crystallizes the evidence-supported structural domain for one following existing-actor property header. Following payload, another control bit, generalized/repeated property loops, next actor/frame and semantic/runtime layers remain closed.

## Next exact pass

**R3.18Q — bounded following-property header production composition.** It may compose only one header after a valid R3.18M true control, must require exact R3.18P tuple membership, and must stop exactly at `payload_start`.

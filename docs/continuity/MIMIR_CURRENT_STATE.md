# MIMIR Current State

Updated: 2026-08-17

## Canonical truth

- repository: `Naveax/MIMIR`
- production code SHA: `fd74ba8c520ab83b808730572c41e45d6dc616e6`
- last production milestone: **R3.18M**
- last completed read-only evidence pass: **R3.18O / Outcome A**
- last completed contract pass: **R3.17N**
- active canonical pass: **R3.18P — following-property header exact-context contract**
- supported/frozen evidence lane: **47 replays / 47 rows**

## R3.18O admitted receipt

- evidence head/tree: `5046e1594b87ce2828db5faa48aceba456c3166f` / `74fb036dfde837e3ecb7e459da00df9ff6c22e28`
- evidence run/job: `32017369100` / `95349613184` — SUCCESS
- same-head normal CI: `32017369071` / `95349613066` — SUCCESS
- artifact: `9284144768` / `25129` bytes
- artifact digest: `sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d`
- artifact inner manifest: `11/11` exact
- R3.18J reconstruction: `47/47` exact
- published R3.18M following control: `47/47` exact
- following header native/oracle: `47/47` exact, mismatch `0`
- exact observed header contexts: `18`
- tags: `Boolean=39`, `ActiveActor=8`
- `prop_id_bits`: `5=43`, `6=4`
- bounds: `60=43`, `67=1`, `72=2`, `110=1`
- version context: `868.32 / net10` on `47/47`
- following payload / another-control bits consumed: `0/0`
- witness reselection: `0`
- production/Cargo/fixture/corpus/support mutation: `0/0/0/0/0`

## Active boundary

R3.18P is contract-only. It may crystallize only the exact 18 R3.18O structural tuples and their observed multiplicities into a privacy-safe admitted artifact. It may not create tag-only/component-only/cross-product support and may not modify production Rust. Following payload, another control, generalized/repeated property loop, next actor/frame, lifecycle state, raw state, events, replay slicing, skills, runtime and exports remain closed.

Read `docs/continuity/MIMIR_R3_18O_DECISION.md` and `docs/continuity/MIMIR_R3_18P_EXECUTION_SPEC.md` before widening anything.

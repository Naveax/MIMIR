from __future__ import annotations

import json
from pathlib import Path

BASE_MAIN = "c8ebb872e510574bb69ab28c719f415ece8b7665"
PROD_SHA = "7390e3b145372252caaa8fa1fe3e0cd13b83336c"
AUTH_HEAD = "5472413a9c9cafcf309293daa490acc5188c88d6"
AUTH_RUN = 31883205829
AUTH_JOB = 95008550716
CONTRACT_SHA = "c8ebb872e510574bb69ab28c719f415ece8b7665"
CONTRACT_TREE = "61e36d40e6af3853a887e840b22f759dda26ed75"
CANDIDATE_CI_RUN = 31883438754
CANDIDATE_CI_JOB = 95009080782
PUBLISHED_ARCHIVE_RUN = 31883625387
PUBLISHED_ARCHIVE_JOB = 95009532717
PUBLISHED_CI_RUN = 31883625362
PUBLISHED_CI_JOB = 95009532734
GROUP_SHA = "80c50783d70951bf125ccdadb818750a7ce35012891997f9b396241d84a9ae2b"
GROUP_BLOB = "b5fa6aaa729772ab3d113703952effe2346c9866"
CONTRACT_BLOB = "76deabf8241b419ca224645106d2a19b041e20f8"


def exact_replace(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, got {count}")
    return text.replace(old, new, 1)


def write(path: str, text: str) -> None:
    Path(path).write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def decision() -> str:
    return f"""# MIMIR R3.17N Decision — K4 Evidence-Supported Contract Admission

**Outcome:** A — ADMITTED / COMPLETE
**Pass type:** contract-only
**Production Rust:** unchanged / forbidden in this pass

## Frozen authority

```text
continuity base / published contract main  {BASE_MAIN}
production SHA                             {PROD_SHA}
contract authority branch head             {AUTH_HEAD}
contract authority run/job                 {AUTH_RUN} / {AUTH_JOB} SUCCESS
clean contract commit                      {CONTRACT_SHA}
clean contract tree                        {CONTRACT_TREE}
exact clean-candidate CI                   {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
published-main Knowledge Archive           {PUBLISHED_ARCHIVE_RUN} / {PUBLISHED_ARCHIVE_JOB} SUCCESS
published-main normal CI                   {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
admitted-group SHA256                      {GROUP_SHA}
admitted-group git blob                    {GROUP_BLOB}
contract git blob                          {CONTRACT_BLOB}
```

## Result

R3.17N admitted exactly the R3.17M evidence surface and nothing more.

```text
R3.17M evidence groups                     161
R3.17N admitted groups                     161
byte-for-byte evidence equality            161/161 PASS
cross-product widening                     0
positive-vector plan                       PASS
negative/malformed vector plan             PASS
atomic failure semantics                   PASS
exact one-value end semantics              PASS
production mutation                        0
Cargo / fixture / corpus / support         0 / 0 / 0 / 0
outcome                                    A
```

The canonical admitted-group artifact is `docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl`. Its SHA-256 is `{GROUP_SHA}` and it is byte-for-byte identical to the R3.17M evidence groups.

## Exact contract boundary

Admission identity is the exact tuple `(attribute_tag, shape, version_major, version_minor, net_version, is_rl_223, payload_width)`. The 161 rows contain 132 unique shapes because context remains part of admission. `Reservation` remains 46 exact group rows / 35 shapes, `DemolishFx` 19 / 12, `DemolishExtended` 5 / 5 and `LoadoutsOnline` 79 / 73. No Cartesian recombination of observed subfields is legal.

The contract freezes LSB-first unaligned decoding, checked arithmetic, atomic failure, exact one-value end, explicit rejection of unobserved version/context/shape combinations, and preservation of trailing bits. It does not authorize a second property.

## What remains closed

- native K4 production implementation,
- any K4 group outside the exact 161-row artifact,
- second-property / property-loop continuation,
- next actor/frame iteration or lifecycle mutation,
- raw-state/event extraction,
- replay slicing, skill mining, runtime or export widening.

## Next pass

Open `R3.17O — Direct Native Exact-Contract K4 Decoder Implementation`. R3.17O may implement only the exact 161-group R3.17N contract. A later separate R3.17P real-replay differential audit remains mandatory before any R3.18 property-loop reopening.
"""


def o_spec() -> str:
    return f"""# MIMIR R3.17O — Direct Native Exact-Contract K4 Decoder Implementation Execution Spec

**Pass type:** production implementation
**Contract authority:** R3.17N Outcome A
**Evidence authority:** R3.17M Outcome A
**Current production authority:** R3.17K / `{PROD_SHA}`

## Goal

Implement a direct native Rust one-value decoder for the exact 161 R3.17N K4 structural/context groups. The implementation must not infer additional combinations from independently observed fields and must stop at the exact end of one already-resolved attribute payload.

## Frozen contract identities

```text
contract commit                  {CONTRACT_SHA}
contract tree                    {CONTRACT_TREE}
admitted-group SHA256            {GROUP_SHA}
admitted-group blob              {GROUP_BLOB}
contract document blob           {CONTRACT_BLOB}
exact admitted rows              161
cross-product widening           0
production parent authority      {PROD_SHA}
```

The checked-in `docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl` is the source of truth for structural acceptance. Production code may use a generated/static Rust representation, but CI must independently prove exact tuple equality with all 161 rows and zero extras.

## Allowed production scope

Keep changes narrowly inside `crates/mimir-replay`:

```text
crates/mimir-replay/src/lib.rs
crates/mimir-replay/src/k4_admitted_groups.rs          optional generated/static exact allowlist
crates/mimir-replay/tests/r3_17o_k4_attribute_decoder.rs
```

A different similarly narrow file split is acceptable only if the clean diff remains within `crates/mimir-replay`. `Cargo.toml`, `Cargo.lock`, fixtures, corpus and supported replay lane must remain unchanged.

## Required public one-value surface

Expose a K4-specific API separate from K1/K2/K3, following existing naming/style conventions. It must carry the caller-resolved replay context needed by the contract and return:

- the decoded K4 value/variant,
- exact structural identity sufficient to prove admitted-group membership,
- exact payload end bit / consumed width,
- no continuation into another property.

Do not broaden existing K1/K2/K3 APIs merely to make K4 convenient.

## Decoder requirements

1. LSB-first bit order; arbitrary unaligned payload start is legal.
2. Checked arithmetic for all cursor movement, signed text lengths, nested counts and byte/bit multiplications.
3. Success only when the decoded exact tuple exists in the 161-row allowlist.
4. On failure, no successful partial value or admitted end position escapes.
5. Extra trailing bits stay unconsumed.
6. Source-known but R3.17M-unobserved branches fail closed.
7. No cross-product construction across `Reservation`, vector-pair or `LoadoutsOnline` substructures.
8. Preserve existing K1/K2/K3 behavior and tests exactly.

## Family surface

Implement only the R3.17N-admitted shapes:

```text
CamSettings          2 group rows / 1 shape / observed f32x7 width 224
ClubColors           1 / 1 / bit+u8+bit+u8 width 18
DemolishExtended     5 / 5
DemolishFx          19 / 12
ExtendedExplosion    2 / 1 / width 112
LoadoutsOnline      79 / 73 nested shapes
PlayerHistoryKey     1 / 1 / u14 width 14
Reservation         46 / 35
StatEvent            2 / 1 / bit+i32 width 33
TeamLoadout          2 / 1 / observed v28 branch width 1040
TeamPaint            2 / 1 / u8x3+u32x2 width 88
TOTAL              161 exact rows
```

For variable families, the allowlist tuple is decisive. A field branch appearing somewhere in evidence does not legalize a new combination.

## Positive gates

Create deterministic synthetic/materialized positives covering every admitted row:

```text
161/161 admitted rows decode successfully
returned K4 tag/variant exact
context exact
structural shape exact
payload width/end exact
allowlist membership exact
trailing poison bits consumed 0
repeatability exact
```

The test builder may derive vectors from the admitted-group artifact or a checked-in generated table, but private real replay payloads must not be added to the repository.

## Structural acceptance gate

Independently enumerate the production K4 allowlist and compare it against the R3.17N artifact:

```text
missing groups                  0
extra groups                    0
cross-product widening          0
161/161 equality                PASS
```

For feasible bounded branch dimensions, add explicit negative enumeration around admitted groups rather than testing only a few hand-picked rejects.

## Required negative / malformed gates

At minimum cover:

```text
unknown/non-K4 tag
invalid start bit
wrong major/minor/net_version/RL223 context
truncation at fixed primitive boundaries
representative one-bit truncation of variable-width groups
malformed signed text length / i32::MIN / checked overflow
Reservation unobserved identifier/name/text-length/context combination
DemolishFx unobserved attacker/victim vector-pair combination
DemolishExtended unobserved vector-pair combination
LoadoutsOnline unobserved outer/group/product combination
LoadoutsOnline malformed nested count/length
LoadoutsOnline unknown product-attribute object branch
unobserved TeamLoadout version branch
source-known but evidence-unobserved branch
extra trailing bits remain unconsumed
```

Map failures deterministically into the established fail-closed style, including invalid-start, insufficient-bits, invalid-length-or-count, unadmitted-context, unadmitted-k4-shape and unsupported-k4-tag semantics.

## Validation gates

```text
cargo fmt --all -- --check                            PASS
focused R3.17O tests                                  PASS
all 161 synthetic positives                          PASS
exact structural acceptance equality                 161/161
cross-product widening                               0
cargo test --locked -p mimir-replay                  PASS
cargo check --locked --workspace --all-targets --all-features PASS
cargo test --locked --workspace --all-targets --all-features  PASS
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings PASS
scripts/verify_repo.ps1                              PASS
Cargo/fixture/corpus/support-lane mutation            0/0/0/0
```

The clean production candidate must be rebuilt directly from fresh canonical `main`, contain only the intended `crates/mimir-replay` production/test changes, pass exact-SHA normal CI, and publish with `force=false`.

## Hard stop

R3.17O implements exactly one already-resolved K4 value only. Do not consume a second property, continue the property loop, advance to another actor/frame, mutate actor lifecycle state, materialize raw state/events, slice replay windows, mine skills, or widen runtime/export.

Do not perform the real-replay differential audit inside R3.17O.

## Next pass

Only if R3.17O closes Outcome A, open `R3.17P — Native K4 Real-Replay Differential Audit` as a separate read-only pass against regenerated pinned-Boxcars witnesses. R3.18 remains closed until that audit is separately complete or evidence explicitly revises the roadmap.
"""


def update_continue() -> None:
    p=Path('MIMIR_CONTINUE_HERE.md')
    s=p.read_text(encoding='utf-8')
    s=exact_replace(s,
        'LAST_COMPLETED_CONTRACT_PASS:\n  R3.17J — evidence-supported K3 spatial/physics contract / Outcome A / 1950 exact groups',
        'LAST_COMPLETED_CONTRACT_PASS:\n  R3.17N — evidence-supported K4 gameplay-structured contract / Outcome A / 161 exact groups / zero cross-product widening',
        'continue last contract')
    s=exact_replace(s,
        'CURRENT_PASS:\n  R3.17N — K4 evidence-supported contract admission\n\nCURRENT_PASS_TYPE:\n  contract-only / exact evidence-group admission; production Rust forbidden',
        'CURRENT_PASS:\n  R3.17O — direct native exact-contract K4 decoder implementation\n\nCURRENT_PASS_TYPE:\n  production implementation / exact 161-group contract only',
        'continue current pass')
    s=exact_replace(s,
        '  NO second property, next actor, next frame, lifecycle mutation, unobserved K2/K3 shape or K4 family is admitted',
        '  R3.17N admits the exact K4 contract but production K4 decode is not yet implemented\n  NO second property, next actor, next frame, lifecycle mutation, unobserved K2/K3/K4 shape or family is admitted',
        'continue hard stop')
    old='''R3_17N_OPEN_BOUNDARY:
  contract-only; production Rust changes are forbidden
  freeze exactly the 161 R3.17M structural/context groups into a canonical admitted-group artifact
  prove 161/161 evidence equality and zero cross-product widening
  Reservation 35 shapes, DemolishFx 12, DemolishExtended 5 and LoadoutsOnline 73 remain exact-group coupled
  source-only or zero-occurrence branches remain rejected

R3_17N_HARD_STOP:
  no production Rust, Cargo, fixture, corpus or support-lane mutation
  no native K4 implementation
  no second property / property-loop continuation
  no next actor / next frame / lifecycle mutation
  no raw-state, event, replay-slice, skill, runtime or export widening

NEXT PASS AFTER R3.17N:
  only if Outcome A, open a separate direct native K4 decoder implementation pass; R3.18 remains closed'''
    new=f'''R3_17N_CONTRACT_CLOSURE:
  Outcome A / contract-only / production Rust unchanged at {PROD_SHA}
  contract authority branch head: {AUTH_HEAD}
  contract authority run/job: {AUTH_RUN} / {AUTH_JOB} SUCCESS
  clean contract main: {CONTRACT_SHA} / tree {CONTRACT_TREE}
  exact clean-candidate CI: {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
  published-main Knowledge Archive: {PUBLISHED_ARCHIVE_RUN} / {PUBLISHED_ARCHIVE_JOB} SUCCESS
  published-main normal CI: {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
  admitted groups: 161/161 byte-identical to R3.17M evidence
  admitted-group SHA256: {GROUP_SHA}
  cross-product widening: 0
  positive/negative vector plans: PASS/PASS
  atomic failure + exact one-value end semantics: PASS/PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

R3_17O_OPEN_BOUNDARY:
  production implementation; exact R3.17N 161-group K4 contract only
  direct native one-value K4 decoder; arbitrary unaligned start; checked arithmetic; atomic failure
  all 161 admitted rows require positive coverage and independent allowlist equality
  Reservation / DemolishFx / DemolishExtended / LoadoutsOnline combinations remain exact-group coupled
  Cargo/fixture/corpus/support lane stay unchanged

R3_17O_HARD_STOP:
  no second property / property-loop continuation
  no next actor / next frame / lifecycle mutation
  no raw-state, event, replay-slice, skill, runtime or export widening
  no real-replay differential audit inside implementation pass

NEXT PASS AFTER R3.17O:
  only if Outcome A, open separate R3.17P native K4 real-replay differential audit; R3.18 remains closed'''
    s=exact_replace(s,old,new,'continue N boundary')
    write(str(p),s)


def update_graph() -> None:
    p=Path('MIMIR_KNOWLEDGE_GRAPH.md')
    s=p.read_text(encoding='utf-8')
    s=exact_replace(s,
        'R3.17M K4 evidence decision                  |\nR3.17N active K4 contract spec                |',
        'R3.17M K4 evidence decision                  |\nR3.17N K4 contract decision                  |\nR3.17O active K4 production spec              |',
        'graph nodes')
    s=exact_replace(s,
        '25. `docs/continuity/MIMIR_R3_17M_DECISION.md`\n26. `docs/continuity/MIMIR_R3_17N_EXECUTION_SPEC.md`\n27. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n28. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n29. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n30. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n31. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n32. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n33. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`',
        '25. `docs/continuity/MIMIR_R3_17M_DECISION.md`\n26. `docs/continuity/MIMIR_R3_17N_EXECUTION_SPEC.md`\n27. `docs/continuity/MIMIR_R3_17N_CONTRACT.md`\n28. `docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl`\n29. `docs/continuity/MIMIR_R3_17N_DECISION.md`\n30. `docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md`\n31. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n32. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n33. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n34. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n35. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n36. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n37. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`',
        'graph reading order')
    s=exact_replace(s,
        ' -> R3.17N K4 evidence-supported contract admission: ACTIVE / CONTRACT-ONLY',
        f' -> R3.17N K4 evidence-supported contract admission: OUTCOME A / CLOSED\n      authority {AUTH_HEAD} / {AUTH_RUN} / {AUTH_JOB} SUCCESS\n      clean contract {CONTRACT_SHA} / tree {CONTRACT_TREE}\n      candidate CI {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS\n      published archive/CI {PUBLISHED_ARCHIVE_RUN} / {PUBLISHED_CI_RUN} SUCCESS\n      161/161 exact groups / SHA256 {GROUP_SHA} / cross-product widening 0\n -> R3.17O direct native exact-contract K4 decoder implementation: ACTIVE / PRODUCTION',
        'graph decoder chain')
    s=exact_replace(s,
        'R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups with zero cross-product widening; R3.17K implemented exactly that contract; R3.17L then matched all 1,950 exact groups against regenerated real-replay witnesses with zero mismatch. R3.17M subsequently observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups with zero structural failures. R3.17N is now contract-only and may admit only those exact groups; native K4 implementation, property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed.',
        'R3.17I closed Outcome A for `Location`, `RigidBody`, `ReplicatedBoost`, and `PickupNew`; R3.17J froze exactly 1,950 structural/context groups with zero cross-product widening; R3.17K implemented exactly that contract; R3.17L matched all 1,950 exact groups against regenerated real-replay witnesses with zero mismatch. R3.17M observed all 11 K4 target tags across 39,463 occurrences and froze 161 exact structural/context evidence groups. R3.17N then admitted exactly those 161 groups byte-for-byte with zero cross-product widening. R3.17O is now the separate native K4 implementation pass; property-loop continuation, next actor/frame iteration and lifecycle mutation remain closed.',
        'graph capability')
    s += f'''\n\n## R3.17N K4 contract closure\n\n```text\nauthority head              {AUTH_HEAD}\nauthority run/job           {AUTH_RUN} / {AUTH_JOB} SUCCESS\nclean contract main         {CONTRACT_SHA}\nclean contract tree         {CONTRACT_TREE}\ncandidate CI                {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS\npublished Knowledge Archive {PUBLISHED_ARCHIVE_RUN} / {PUBLISHED_ARCHIVE_JOB} SUCCESS\npublished main CI           {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS\nadmitted groups             161/161 exact\ngroup SHA256                {GROUP_SHA}\ncross-product widening      0\natomic failure              PASS\nexact one-value end         PASS\nprod/Cargo/fixture/corpus/\nsupport mutations           0/0/0/0/0\noutcome                     A\nnext                        R3.17O native K4 implementation\n```\n'''
    write(str(p),s)


def update_current() -> None:
    p=Path('docs/continuity/MIMIR_CURRENT_STATE.md')
    s=p.read_text(encoding='utf-8')
    s=exact_replace(s,
        '**Completed K4 evidence:** `R3.17M — Outcome A / 39463 occurrences / 161 exact structural-context groups / all 11 tags observed`\n**Current exact pass:** `R3.17N — K4 evidence-supported contract admission`',
        '**Completed K4 evidence:** `R3.17M — Outcome A / 39463 occurrences / 161 exact structural-context groups / all 11 tags observed`\n**Completed K4 contract:** `R3.17N — Outcome A / 161/161 byte-identical groups / zero cross-product widening`\n**Current exact pass:** `R3.17O — direct native exact-contract K4 decoder implementation`',
        'current header')
    old='''## 5. R3.17N exact next pass

R3.17N is contract-only. Freeze the exact 161 R3.17M structural/context groups into a canonical admitted-group artifact, prove 161/161 equality with the evidence artifact, define atomic failure and exact one-value end semantics, and keep all unobserved branches explicit rejects. Production Rust remains unchanged.

Only after R3.17N Outcome A may a separate native K4 implementation pass open. R3.18 property-loop work remains closed.

## 6. Still closed

```text
K4 contract not yet admitted / native payload decode'''
    new=f'''## 5. R3.17N K4 contract closure

```text
contract authority head       {AUTH_HEAD}
authority run/job             {AUTH_RUN} / {AUTH_JOB} SUCCESS
clean contract main           {CONTRACT_SHA}
clean contract tree           {CONTRACT_TREE}
exact candidate CI            {CANDIDATE_CI_RUN} / {CANDIDATE_CI_JOB} SUCCESS
published Knowledge Archive   {PUBLISHED_ARCHIVE_RUN} / {PUBLISHED_ARCHIVE_JOB} SUCCESS
published normal CI           {PUBLISHED_CI_RUN} / {PUBLISHED_CI_JOB} SUCCESS
admitted groups               161/161 byte-identical
group SHA256                  {GROUP_SHA}
group blob                    {GROUP_BLOB}
contract blob                 {CONTRACT_BLOB}
cross-product widening        0
atomic failure                PASS
exact one-value end           PASS
production/Cargo/fixture/
corpus/support mutation       0/0/0/0/0
outcome                       A
```

R3.17N admits the K4 contract only; production still cannot decode K4. Exact tuple membership remains mandatory, especially for Reservation and nested LoadoutsOnline shapes.

## 6. R3.17O exact next pass

Implement the direct native K4 one-value decoder for exactly the 161 R3.17N groups. Require 161/161 positive coverage, independent allowlist equality, zero cross-product widening, negative/malformed coverage, atomic failure, exact end-bit semantics, full repository validation and a clean `crates/mimir-replay`-only production diff. Cargo, fixtures, corpus and support lane remain unchanged.

R3.17O must not perform its own real-replay differential audit. That is a separate R3.17P pass after implementation Outcome A. R3.18 remains closed.

## 7. Still closed

```text
native K4 payload decode (until R3.17O closes)'''
    s=exact_replace(s,old,new,'current N section')
    write(str(p),s)


def update_state() -> None:
    p=Path('docs/continuity/MIMIR_CONTINUITY_STATE.json')
    state=json.loads(p.read_text(encoding='utf-8'))
    if state.get('current_pass')!='R3.17N': raise SystemExit('unexpected current pass')
    state['last_completed_contract_pass']='R3.17N'
    state['last_completed_contract_outcome']='A — 161/161 byte-identical K4 structural/context groups; zero cross-product widening; atomic failure and exact one-value end admitted'
    state['current_pass']='R3.17O'
    state['current_pass_kind']='production implementation of exact R3.17N K4 one-value contract'
    state['current_pass_goal']='Implement a direct native K4 decoder for exactly the 161 R3.17N admitted structural/context groups with 161/161 positive coverage, exact allowlist equality, zero cross-product widening, atomic failure and exact one-value end semantics.'
    state['current_pass_stop_boundary']='One already-resolved K4 value only; no second property/property loop, actor/frame, lifecycle, raw-state/event/skill/runtime/export widening, and no real-replay differential audit inside implementation.'
    state['closed_now']=[x for x in state['closed_now'] if x!='native K4 attribute payload decode']
    state['closed_now'].insert(0,'native K4 attribute payload decode until R3.17O production closes')
    files=state['next_files_to_read']
    anchor='docs/continuity/MIMIR_R3_17N_EXECUTION_SPEC.md'
    idx=files.index(anchor)+1
    for item in ['docs/continuity/MIMIR_R3_17N_CONTRACT.md','docs/continuity/MIMIR_R3_17N_ADMITTED_GROUPS.jsonl','docs/continuity/MIMIR_R3_17N_DECISION.md','docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md']:
        if item not in files:
            files.insert(idx,item); idx+=1
    state['r3_17n']={
        'outcome':'A — admitted / complete',
        'pass_type':'contract-only K4 exact-group admission',
        'production_source_changed':False,
        'continuity_base_sha':'86665c73acaaa20cb2c2b927b2283a28c66ecc10',
        'production_sha':PROD_SHA,
        'authority_head':AUTH_HEAD,
        'workflow_run':AUTH_RUN,
        'workflow_job':AUTH_JOB,
        'clean_contract_sha':CONTRACT_SHA,
        'clean_contract_tree':CONTRACT_TREE,
        'exact_candidate_ci_run':CANDIDATE_CI_RUN,
        'exact_candidate_ci_job':CANDIDATE_CI_JOB,
        'published_knowledge_archive_run':PUBLISHED_ARCHIVE_RUN,
        'published_knowledge_archive_job':PUBLISHED_ARCHIVE_JOB,
        'published_main_ci_run':PUBLISHED_CI_RUN,
        'published_main_ci_job':PUBLISHED_CI_JOB,
        'evidence_groups':161,
        'admitted_groups':161,
        'evidence_equality':'161/161 byte-identical',
        'admitted_groups_sha256':GROUP_SHA,
        'admitted_groups_blob':GROUP_BLOB,
        'contract_blob':CONTRACT_BLOB,
        'cross_product_widening':0,
        'positive_vector_plan':'PASS',
        'negative_vector_plan':'PASS',
        'atomic_failure_semantics':'PASS',
        'exact_one_value_end_semantics':'PASS',
        'production_cargo_fixture_corpus_support_mutation':'0/0/0/0/0',
        'next_pass':'R3.17O'
    }
    write(str(p),json.dumps(state,indent=2,ensure_ascii=False))


def main() -> None:
    write('docs/continuity/MIMIR_R3_17N_DECISION.md',decision())
    write('docs/continuity/MIMIR_R3_17O_EXECUTION_SPEC.md',o_spec())
    update_continue(); update_graph(); update_current(); update_state()
    print('R3.17N continuity closure generated')
    print('next=R3.17O direct native exact-contract K4 decoder implementation')

if __name__=='__main__': main()

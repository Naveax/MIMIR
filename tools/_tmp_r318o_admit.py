#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE_MAIN = "c1d68daf989952ccf40645ca99616bccf43bb2f4"
PROD = "fd74ba8c520ab83b808730572c41e45d6dc616e6"
EVIDENCE_HEAD = "5046e1594b87ce2828db5faa48aceba456c3166f"
EVIDENCE_TREE = "74fb036dfde837e3ecb7e459da00df9ff6c22e28"
EVIDENCE_RUN = "32017369100"
EVIDENCE_JOB = "95349613184"
SAME_HEAD_RUN = "32017369071"
SAME_HEAD_JOB = "95349613066"
ARTIFACT_ID = "9284144768"
ARTIFACT_SIZE = 25129
ARTIFACT_DIGEST = "e6dc02f087395e2d6b5fb568233484430feba51223848367edd2c6cf15b4b94d"

CONTEXTS = [
    (60, 5, 12, "Boolean", 1),
    (60, 5, 13, "Boolean", 2),
    (60, 5, 14, "ActiveActor", 3),
    (60, 5, 17, "Boolean", 3),
    (60, 5, 18, "Boolean", 3),
    (60, 5, 19, "Boolean", 7),
    (60, 5, 21, "Boolean", 1),
    (60, 5, 22, "Boolean", 2),
    (60, 5, 23, "Boolean", 8),
    (60, 5, 27, "ActiveActor", 3),
    (60, 5, 30, "ActiveActor", 2),
    (60, 5, 42, "Boolean", 1),
    (60, 5, 43, "Boolean", 1),
    (60, 5, 44, "Boolean", 3),
    (60, 5, 54, "Boolean", 3),
    (67, 6, 37, "Boolean", 1),
    (72, 6, 15, "Boolean", 2),
    (110, 6, 44, "Boolean", 1),
]

INNER_HASHES = {
    "r3_18o_source_scope.txt": "6120672ca758c4d951e63cb6c5e3dc4cdd003dc7438319c9d459a36331f0e123",
    "r3_18o_replay_identity.tsv": "b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf",
    "r3_18o_frozen_witnesses.json": "99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7",
    "r3_18o_r318n_authority_sha256.txt": "8f933b6601538d79624969e38290297389bcba217908c0b7ecd3526b807bd547",
    "r3_18o_boxcars_instrumentation_sha256.txt": "f76e15fb1cec92e5f2604b2ace1be194446eda88613527dbfe1015fbceb815cb",
    "r3_18o_source_summary.json": "a261368f51770efee56e3d8d760390f633b6190bed81446feaf57b076189ae01",
    "r3_18o_targets.tsv": "03e6d06c5435013df92ba9d1bcf799816352718795c6a02ece0ae97ea8336adb",
    "r3_18o_oracle_header_rows.json": "458329fb7924805774056c3187032c6149401143d31ff8f0f8d055bafa0cc625",
    "r3_18o_header_rows.json": "503bae96ac51ff27532fc80b5e537b3cb7ccd58cea1584a9a1f975da8a4748a9",
    "r3_18o_negative_controls.txt": "5993bff36da50dbb19a75dc7a42d1fc68a57d429636e8776dc972ba244c4b598",
    "r3_18o_aggregate.txt": "02324f5a0caa68257a0af93999245124242569f8d582ab2aba2f8119fe6cd676",
}


def require(cond, msg):
    if not cond:
        raise SystemExit(msg)


def write(path: Path, text: str):
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    require(count == 1, f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def context_table():
    lines = [
        "| stream_id_bound | prop_id_bits | property object index | attribute tag | version | observed rows |",
        "|---:|---:|---:|---|---|---:|",
    ]
    for bound, bits, obj, tag, count in CONTEXTS:
        lines.append(f"| {bound} | {bits} | {obj} | `{tag}` | `868.32 / net10` | {count} |")
    return "\n".join(lines)


def decision_doc():
    hashes = "\n".join(f"- `{name}`: `{sha}`" for name, sha in INNER_HASHES.items())
    return f"""# MIMIR R3.18O Decision — Following-Property Header Evidence

Date: 2026-08-17  
Outcome: **A — ADMITTED / READ-ONLY EVIDENCE**

## Authority

- fresh base `main`: `{BASE_MAIN}`
- production remains: `{PROD}` (R3.18M)
- evidence head/tree: `{EVIDENCE_HEAD}` / `{EVIDENCE_TREE}`
- evidence run/job: `{EVIDENCE_RUN}` / `{EVIDENCE_JOB}` — SUCCESS
- same-head normal CI: `{SAME_HEAD_RUN}` / `{SAME_HEAD_JOB}` — SUCCESS
- immutable artifact: `{ARTIFACT_ID}` / `{ARTIFACT_SIZE}` bytes
- artifact digest: `sha256:{ARTIFACT_DIGEST}`
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

{context_table()}

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

{hashes}

## Admission

R3.18O is admitted as **evidence only**. No production Rust capability changes.

The 18 observed tuple identities are evidence-supported candidates, not a tag-only, bound-only, object-only, Cartesian-product, or generic following-property-header production contract. In particular, seeing `Boolean` or `ActiveActor` here does not make those tags universally valid in arbitrary actor/property/version contexts.

## Next exact pass

**R3.18P — Following-Property Header Context Contract**.

R3.18P is contract-only. It must crystallize the exact 18 observed structural tuples and their 47-row multiplicities from the immutable R3.18O artifact into one privacy-safe committed contract artifact, prove exact logical equality back to R3.18O, and keep production code frozen. Only a later separately admitted production pass may compose the header.
"""


def p_spec():
    return f"""# MIMIR R3.18P Execution Spec — Following-Property Header Context Contract

Date: 2026-08-17  
Pass type: **contract-only / no production code change**

## Goal

Convert the admitted R3.18O following-header evidence into one canonical, privacy-safe exact structural-context contract without widening the observed domain.

## Frozen authority

- base production: `{PROD}` (R3.18M)
- R3.18O evidence head: `{EVIDENCE_HEAD}`
- R3.18O run/job: `{EVIDENCE_RUN}` / `{EVIDENCE_JOB}` — SUCCESS
- same-head normal CI: `{SAME_HEAD_RUN}` / `{SAME_HEAD_JOB}` — SUCCESS
- artifact: `{ARTIFACT_ID}` / `sha256:{ARTIFACT_DIGEST}` / `{ARTIFACT_SIZE}` bytes
- source-summary SHA-256: `{INNER_HASHES['r3_18o_source_summary.json']}`
- header-rows SHA-256: `{INNER_HASHES['r3_18o_header_rows.json']}`
- aggregate SHA-256: `{INNER_HASHES['r3_18o_aggregate.txt']}`
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

{context_table()}

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

- **Outcome A:** exact 18-tuple contract is admitted; production stays `{PROD}` and a separate minimal production-composition pass may be opened.
- **Outcome B:** any authority/equality/negative/scope gate fails; admit no contract and do not open production composition.
"""


def patch_json(root: Path):
    p = root / "docs/continuity/MIMIR_CONTINUITY_STATE.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    require(d["current_pass"] == "R3.18O", "continuity current pass drift")
    require(d["last_production_code_sha"] == PROD, "continuity production drift")
    d["last_completed_read_only_audit"] = "R3.18O"
    d["last_completed_evidence_pass"] = "R3.18O"
    d["last_completed_evidence_outcome"] = (
        "A — exact frozen 47-row following-property header evidence; 47/47 native/oracle exact, "
        "18 exact structural context tuples, mismatch 0, witness reselection 0, following payload/another-control consumption 0/0."
    )
    d["current_pass"] = "R3.18P"
    d["current_pass_kind"] = "contract-only following-property header exact-context crystallization"
    d["current_pass_goal"] = (
        "Crystallize the immutable R3.18O 18 exact following-header structural context tuples and their 47-row multiplicities into one privacy-safe committed contract artifact with no cross-product widening."
    )
    d["current_pass_stop_boundary"] = (
        "No production code change. Admit only exact R3.18O tuple identity; no following payload, another control, generalized loop, actor/frame, semantic or runtime widening."
    )
    d["r3_18o"] = {
        "outcome": "A — admitted / read-only evidence",
        "production_source_changed": False,
        "production_sha": PROD,
        "base_main_sha": BASE_MAIN,
        "evidence_head_sha": EVIDENCE_HEAD,
        "evidence_tree_sha": EVIDENCE_TREE,
        "evidence_run": int(EVIDENCE_RUN),
        "evidence_job": int(EVIDENCE_JOB),
        "same_head_ci_run": int(SAME_HEAD_RUN),
        "same_head_ci_job": int(SAME_HEAD_JOB),
        "artifact_id": int(ARTIFACT_ID),
        "artifact_size": ARTIFACT_SIZE,
        "artifact_sha256": ARTIFACT_DIGEST,
        "artifact_inner_manifest_verified": "11/11",
        "frozen_rows": 47,
        "native_oracle_exact": "47/47",
        "native_oracle_mismatch": 0,
        "witness_reselection": 0,
        "unique_exact_header_context_tuples": 18,
        "attribute_tag_counts": {"ActiveActor": 8, "Boolean": 39},
        "prop_id_bits_counts": {"5": 43, "6": 4},
        "stream_id_bound_counts": {"60": 43, "67": 1, "72": 2, "110": 1},
        "version_context": "868.32/net10 on 47/47",
        "following_payload_bits_consumed": 0,
        "another_control_bits_consumed": 0,
        "production_cargo_fixture_corpus_support_mutation": "0/0/0/0/0",
        "privacy": "PASS",
        "next_pass": "R3.18P"
    }
    files = d.get("next_files_to_read", [])
    for new in [
        "docs/continuity/MIMIR_R3_18O_DECISION.md",
        "docs/continuity/MIMIR_R3_18P_EXECUTION_SPEC.md",
    ]:
        if new not in files:
            idx = files.index("docs/continuity/MIMIR_R3_18O_EXECUTION_SPEC.md") + 1
            files.insert(idx, new)
    d["next_files_to_read"] = files
    write(p, json.dumps(d, indent=2, ensure_ascii=False))


def patch_current(root: Path):
    write(root / "docs/continuity/MIMIR_CURRENT_STATE.md", f"""# MIMIR Current State

Updated: 2026-08-17

## Canonical truth

- repository: `Naveax/MIMIR`
- production code SHA: `{PROD}`
- last production milestone: **R3.18M**
- last completed read-only evidence pass: **R3.18O / Outcome A**
- last completed contract pass: **R3.17N**
- active canonical pass: **R3.18P — following-property header exact-context contract**
- supported/frozen evidence lane: **47 replays / 47 rows**

## R3.18O admitted receipt

- evidence head/tree: `{EVIDENCE_HEAD}` / `{EVIDENCE_TREE}`
- evidence run/job: `{EVIDENCE_RUN}` / `{EVIDENCE_JOB}` — SUCCESS
- same-head normal CI: `{SAME_HEAD_RUN}` / `{SAME_HEAD_JOB}` — SUCCESS
- artifact: `{ARTIFACT_ID}` / `{ARTIFACT_SIZE}` bytes
- artifact digest: `sha256:{ARTIFACT_DIGEST}`
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
""")


def patch_handoff(root: Path):
    write(root / "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", f"""# MIMIR Next Chat Handoff — R3.18P

Fresh-read `main` before work. Production remains `{PROD}` at R3.18M. R3.18O is admitted Outcome A and production source did not change.

Canonical R3.18O authority:
- evidence head `{EVIDENCE_HEAD}` / tree `{EVIDENCE_TREE}`
- run/job `{EVIDENCE_RUN}` / `{EVIDENCE_JOB}` SUCCESS
- same-head CI `{SAME_HEAD_RUN}` / `{SAME_HEAD_JOB}` SUCCESS
- artifact `{ARTIFACT_ID}` / `{ARTIFACT_SIZE}` bytes
- digest `sha256:{ARTIFACT_DIGEST}`
- inner manifest `11/11` exact
- exact frozen rows `47/47`; following-header native/oracle mismatch `0`
- exact structural contexts `18`; tags Boolean=39 / ActiveActor=8
- following payload / another-control consumption `0/0`; witness reselection `0`

First unfinished canonical pass: **R3.18P following-property header exact-context contract**.

Read `MIMIR_CONTINUE_HERE.md`, apply the `MIMIR_KNOWLEDGE_GRAPH.md` mandatory order, then execute `docs/continuity/MIMIR_R3_18P_EXECUTION_SPEC.md`. Derive the contract only from immutable R3.18O authority. Preserve all 18 exact tuples and all 47 multiplicities. No component-wise or Cartesian-product widening. Production Rust remains frozen.
""")


def patch_ledger(root: Path):
    p = root / "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
    s = p.read_text(encoding="utf-8").rstrip()
    entry = f"""

## 2026-08-17 — R3.18O — Following-property header evidence

Production base SHA: `{PROD}`
Production commit SHA: unchanged
Pass type: read-only evidence / differential
Outcome: **A — ADMITTED / READ-ONLY**

What changed:
- no production code changed;
- the exact frozen 47-row R3.18N lane was extended only through one following existing-actor property header and stopped at `payload_start`.

Evidence:
- evidence `{EVIDENCE_HEAD}` / `{EVIDENCE_RUN}` / `{EVIDENCE_JOB}` SUCCESS;
- same-head CI `{SAME_HEAD_RUN}` / `{SAME_HEAD_JOB}` SUCCESS;
- artifact `{ARTIFACT_ID}` / `{ARTIFACT_SIZE}` bytes / `sha256:{ARTIFACT_DIGEST}`;
- artifact inner manifest 11/11 exact;
- R3.18J reconstruction 47/47; published R3.18M control 47/47; following header 47/47; mismatch 0;
- 18 exact structural context tuples over 47 rows; Boolean=39 / ActiveActor=8;
- all 47 rows 868.32/net10; witness reselection 0.

Validation:
- property-present and stream truncation, prior-stop mismatch, wrong actor-stream context, outside-exact-tuple, repeatability and post-payload-start poison controls PASS;
- following payload / another-control bits consumed 0/0;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0;
- privacy PASS.

Boundaries opened:
- evidence support only for the exact 18 observed following-header structural contexts.

Boundaries still closed:
- production composition of that following header;
- any context outside the exact observed tuples;
- following payload, another control, repeated/generalized property loop, next actor/frame/lifecycle and all semantic/runtime layers.

Important negative facts / anti-regressions:
- tag/component membership alone is not support;
- do not cross-product individually observed bounds, widths, object indices or tags;
- Boxcars continuing its own parse after the instrumentation point is not MIMIR observer consumption.

Next exact pass:
- `R3.18P — following-property header exact-context contract`.
"""
    write(p, s + entry)


def patch_kg(root: Path):
    p = root / "MIMIR_KNOWLEDGE_GRAPH.md"
    s = p.read_text(encoding="utf-8")
    s = replace_once(
        s,
        "R3.18O active following-property header evidence spec                             |",
        "R3.18O following-property header evidence decision / Outcome A CLOSED             |\nR3.18P active following-property exact-context contract spec                               |",
        "KG canonical O->P",
    )
    start = s.index("## Mandatory reading order")
    end = s.index("\n### R3.18I payload evidence", start)
    prefix = s[:start]
    suffix = s[end:]
    section = s[start:end]
    lines = section.splitlines()
    paths = []
    for line in lines:
        stripped = line.strip()
        if stripped and stripped[0].isdigit() and "`" in stripped:
            paths.append(stripped.split("`", 2)[1])
    require(paths and paths[-1].endswith("HISTORICAL_TO_CURRENT_MAPPING.md"), "KG mandatory parse drift")
    oidx = paths.index("docs/continuity/MIMIR_R3_18O_EXECUTION_SPEC.md") + 1
    for new in ["docs/continuity/MIMIR_R3_18O_DECISION.md", "docs/continuity/MIMIR_R3_18P_EXECUTION_SPEC.md"]:
        if new not in paths:
            paths.insert(oidx, new)
            oidx += 1
    rebuilt = "## Mandatory reading order\n\n" + "\n".join(f"{i}. `{path}`" for i, path in enumerate(paths, 1)) + "\n"
    s = prefix + rebuilt + suffix
    old = """### R3.18O following-property header evidence: ACTIVE
- exact frozen 47-row N/L lane only; no witness reselection
- evidence-only; production remains `fd74ba8c520ab83b808730572c41e45d6dc616e6`
- stop at following payload_start; payload and another control remain closed
"""
    new = f"""### R3.18O following-property header evidence: OUTCOME A / CLOSED
- production unchanged at `{PROD}`
- evidence `{EVIDENCE_HEAD}` / `{EVIDENCE_RUN}/{EVIDENCE_JOB}` SUCCESS; same-head CI `{SAME_HEAD_RUN}/{SAME_HEAD_JOB}` SUCCESS
- artifact `{ARTIFACT_ID}` / `sha256:{ARTIFACT_DIGEST}` / `{ARTIFACT_SIZE}` bytes; inner manifest 11/11 exact
- frozen 47/47; following header exact 47/47; mismatch 0; witness reselection 0
- 18 exact structural contexts; Boolean=39 / ActiveActor=8; all 868.32/net10
- following payload / another-control consumption 0/0; no production widening

### R3.18P following-property header context contract: ACTIVE
- contract-only; production remains `{PROD}`
- exact R3.18O 18-tuple identity + 47 multiplicities only
- no tag/component-only support, no Cartesian product, no payload/control/loop widening
"""
    s = replace_once(s, old, new, "KG status O->P")
    write(p, s)


def patch_continue(root: Path):
    p = root / "MIMIR_CONTINUE_HERE.md"
    s = p.read_text(encoding="utf-8")
    s = replace_once(
        s,
        "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18N — published R3.18M following-control differential / Outcome A / 47/47 exact / false=0 true=47 / 0 mismatch / following stream+header+payload+another-control bits 0",
        "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18O — following-property header differential / Outcome A / 47/47 exact / 18 exact structural contexts / 0 mismatch / following payload+another-control bits 0",
        "continue last audit",
    )
    s = replace_once(
        s,
        "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18N — published after-second-payload control differential / Outcome A / 47 continuation rows / false=0 true=47 / 0 mismatch / no following stream/header/payload/another-control",
        "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18O — following-property header evidence / Outcome A / 47 rows / 18 exact structural contexts / 0 mismatch / no following payload or another-control",
        "continue last evidence",
    )
    s = replace_once(s, "CURRENT_PASS:\n  R3.18O — following-property header evidence", "CURRENT_PASS:\n  R3.18P — following-property header exact-context contract", "continue current pass")
    s = replace_once(
        s,
        "CURRENT_PASS_TYPE:\n  read-only differential / characterize exactly one following property header on the frozen 47-row lane and stop at payload_start; no following payload or another-control access",
        "CURRENT_PASS_TYPE:\n  contract-only / crystallize exactly the 18 R3.18O structural context tuples and their 47-row multiplicities; production Rust frozen; no cross-product widening",
        "continue current type",
    )
    s = replace_once(
        s,
        "  R3.18O ACTIVE read-only following-property header evidence; stop at following payload_start\n  NO following payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
        "  R3.18O CLOSED Outcome A: 47/47 following headers exact through payload_start; 18 exact structural contexts; mismatch 0; following payload/another-control consumption 0/0\n  R3.18P ACTIVE contract-only: exact 18-tuple identity + 47 multiplicities only; production unchanged\n  NO following-header production composition, following payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
        "continue hard stop O->P",
    )
    marker = "R3_18L_EVIDENCE_CLOSURE:"
    require(marker in s, "continue closure marker drift")
    oclose = f"""R3_18O_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at {PROD}
  authority head/tree: {EVIDENCE_HEAD} / {EVIDENCE_TREE}
  authority run/job: {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
  exact-head normal CI: {SAME_HEAD_RUN} / {SAME_HEAD_JOB} SUCCESS
  artifact: {ARTIFACT_ID} / {ARTIFACT_SIZE} bytes
  artifact digest: sha256:{ARTIFACT_DIGEST}
  inner artifact manifest: 11/11 exact
  frozen rows: 47/47 / R3.18J reconstruction 47/47 / published R3.18M control 47/47 / following header 47/47 / mismatch 0
  exact structural contexts: 18 / tags Boolean=39 ActiveActor=8 / all rows 868.32 net10
  prop_id_bits: 5=43 6=4 / stream_id_bound: 60=43 67=1 72=2 110=1
  property-present truncation / stream truncation / prior-stop / wrong-context / outside-exact-tuple / repeatability / poison: PASS
  following payload/another-control bits consumed: 0/0; witness reselection: 0; privacy: PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0
"""
    s = replace_once(s, marker, oclose + marker, "continue insert O closure")
    final = s.rfind("# CURRENT PASS CHECKLIST — R3.18N")
    require(final >= 0, "stale final checklist not found")
    pcheck = f"""# R3.18O OUTCOME A ADMITTED / ACTIVE R3.18P — 2026-08-17

```text
production code SHA = {PROD}
R3.18O evidence head = {EVIDENCE_HEAD}
R3.18O run/job        = {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.18O same-head CI   = {SAME_HEAD_RUN} / {SAME_HEAD_JOB} SUCCESS
R3.18O artifact       = {ARTIFACT_ID} / sha256:{ARTIFACT_DIGEST}
R3.18O outcome        = A / 47 OF 47 FOLLOWING HEADERS EXACT / 18 EXACT CONTEXT TUPLES
ACTIVE NEXT PASS      = R3.18P — following-property header exact-context contract
```

R3.18O reused the exact frozen 47-row authority and stopped the MIMIR observer exactly at the following property's `payload_start`. The observed domain contains 18 exact structural tuples. Those tuple identities, not their individual components, are the only evidence-supported basis for the next contract pass.

## CURRENT PASS CHECKLIST — R3.18P

- [ ] Fresh-read `main`; require production still exactly R3.18M `{PROD}` and no production/Cargo/fixture/corpus/support drift.
- [ ] Freeze R3.18O head/run/job/CI/artifact/digest plus all 11 inner SHA-256 receipts.
- [ ] Download the immutable R3.18O artifact and require its ZIP digest and 11/11 inner manifest exact.
- [ ] Derive exactly 18 unique tuples from `r3_18o_source_summary.json`; require observed multiplicities to sum to 47.
- [ ] Preserve tuple identity `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)` exactly.
- [ ] Write one privacy-safe committed `MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json` artifact with authority receipts, exact tuples and multiplicities.
- [ ] Prove the committed artifact is logically identical to the immutable evidence summary; witness reselection = 0.
- [ ] Negative-test tag-only, bound-only, width-only, object-only and fabricated Cartesian-product tuple acceptance; all must fail closed.
- [ ] Do not modify production Rust, Cargo, fixture/corpus or support tables; do not decode following payload or another control bit.
- [ ] Run repository verification and exact-clean-SHA CI for the contract commit.
- [ ] Outcome A may open only a separate bounded production composition tied to the admitted exact tuple contract; no generic property cursor or loop.
"""
    s = s[:final] + pcheck
    write(p, s)


def patch_boundary(root: Path):
    p = root / "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
    s = p.read_text(encoding="utf-8")
    anchor = "---\n\n# 1. Status vocabulary"
    require(anchor in s, "boundary anchor drift")
    override = f"""---

# 0. Current override — R3.18O admitted / R3.18P active

This current override supersedes older R3.18M/N/O status wording later in this historical lock file.

## OPEN / PRODUCTION

- production remains R3.18M at `{PROD}`;
- exactly one true following `property_present` bit after a valid R3.18J second payload is production-admitted;
- no later following header is production-admitted yet.

## EVIDENCE-ONLY — R3.18O

- exact frozen 47-row following-header evidence is admitted Outcome A;
- 47/47 native/oracle headers matched through `payload_start`;
- exactly 18 structural context tuples were observed, all at `868.32 / net10`;
- `Boolean=39`, `ActiveActor=8`; witness reselection=0; mismatch=0;
- following payload and another-control observer consumption remain 0/0.

## ACTIVE CONTRACT GATE — R3.18P

- only exact 18-tuple identity and exact 47-row multiplicities may be crystallized;
- tag-only/component-only/Cartesian-product widening is forbidden;
- production Rust remains frozen.

## CLOSED

- production composition of the following header until a contract is separately admitted;
- contexts outside the exact admitted tuple set;
- following payload;
- another property control bit;
- repeated/generalized property loop or generic repeatable cursor;
- next actor/frame, lifecycle mutation, raw state, events, replay slices, skills, runtime and exports.

---

# 1. Status vocabulary"""
    s = replace_once(s, anchor, override, "boundary current override")
    write(p, s)


def main():
    require(len(sys.argv) == 2, "usage: patcher ROOT")
    root = Path(sys.argv[1])
    require((root / ".git").exists(), "root is not git checkout")
    write(root / "docs/continuity/MIMIR_R3_18O_DECISION.md", decision_doc())
    write(root / "docs/continuity/MIMIR_R3_18P_EXECUTION_SPEC.md", p_spec())
    patch_json(root)
    patch_current(root)
    patch_handoff(root)
    patch_ledger(root)
    patch_kg(root)
    patch_continue(root)
    patch_boundary(root)
    print("R3_18O_ADMISSION_PATCH=PASS")

if __name__ == "__main__":
    main()

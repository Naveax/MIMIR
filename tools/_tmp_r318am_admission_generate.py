from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: _tmp_r318am_admission_generate.py <same_head_ci_run> <same_head_ci_job>")

CI_RUN = int(sys.argv[1])
CI_JOB = int(sys.argv[2])

BASE = "fec9dca3cb8366108245788fc9a2b24a0c99fe94"
BASE_TREE = "3bf5f68ec7df5565f78f89fd4bc2254f2a64e010"
PROD = "f20f529e3ada6e9a671ea91e5676a17a00770145"
PROD_TREE = "98c675811cca4e4d7f0122c762f371548c9266c2"
AM_HEAD = "842b94ed4c4e57323433585fea48116ecf18989b"
AM_TREE = "486d0a0f3833dcb8872f062ae1927c9aefde87ba"
AM_RUN = 32473716883
AM_JOB = 96745647750
AM_ART = 9443581172
AM_SIZE = 14827
AM_DIGEST = "2f65de5207bd96787fd7d1527a55991f08d5da614a0ddfce22a7aa267968e3c8"
AL_HEAD = "06b8570a25a989651fc800a4ded900ce5e2f3dbe"
AJ_CONTRACT = "cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c"


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_one(path: str, old: str, new: str, label: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: {label}: expected one match, got {count}")
    write(path, text.replace(old, new, 1))


def regex_replace_one(path: str, pattern: str, replacement: str, label: str) -> None:
    text = read(path)
    text2, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{path}: {label}: expected one regex match, got {count}")
    write(path, text2)


# ---------------------------------------------------------------------------
# MIMIR_CONTINUE_HERE.md
# ---------------------------------------------------------------------------
replace_one(
    "MIMIR_CONTINUE_HERE.md",
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AL — published R3.18AK following-header differential / Outcome A / 47/47 / 17 exact contexts / Int=47 / mismatch 0 / artifact 9442034802",
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18AM — post-AK one-following-payload evidence / Outcome A / 47/47 / Int=47 / width32=47 / mismatch 0 / artifact 9443581172",
    "last read-only audit",
)
replace_one(
    "MIMIR_CONTINUE_HERE.md",
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AL — published AK/frozen AI/direct header exact 47/47 / 17 contexts / Int=47 / mismatch 0 / payload-control 0/0 / artifact 9442034802",
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18AM — one post-AK Int payload exact 47/47 / width32=47 / semantic range 1..415 / mismatch 0 / another-control 0 / artifact 9443581172",
    "last evidence pass",
)
replace_one(
    "MIMIR_CONTINUE_HERE.md",
    "CURRENT_PASS:\n  R3.18AM — post-AK one following-payload evidence\n\nCURRENT_PASS_TYPE:\n  read-only payload evidence / begin at validated R3.18AK payload_start, decode exactly one payload against pinned Boxcars/native evidence, stop at payload end, consume zero another-control bits",
    "CURRENT_PASS:\n  R3.18AN — bounded post-AK one-following-payload production\n\nCURRENT_PASS_TYPE:\n  production implementation / validate and recompute the R3.18AK/AJ header boundary, decode exactly the R3.18AM-admitted Int/32 payload, stop at payload end, consume zero another-control bits",
    "current pass",
)
replace_one(
    "MIMIR_CONTINUE_HERE.md",
    "  R3.18AM ACTIVE read-only payload evidence: start exactly at R3.18AK payload_start on the same 47 rows; prove one payload independently; another-control consumption must remain 0\n  NO post-AK payload production before R3.18AM evidence closure, another property control, alternate unadmitted payload layout, repeated/generalized property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "  R3.18AM CLOSED Outcome A: one post-AK payload exact 47/47; Int=47; width=32 on 47/47; semantic Int range 1..415; native-oracle mismatch 0; witness reselection 0; another-control bits 0; artifact 9443581172\n  R3.18AN ACTIVE bounded production: validate/recompute the R3.18AK/AJ header boundary, decode exactly one AM-admitted Int/32 payload, stop at payload end, and consume zero another-control bits\n  NO another property control after the R3.18AN payload end, alternate payload tag/layout, repeated/generalized property loop/cursor, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "current hard stop",
)
continue_text = read("MIMIR_CONTINUE_HERE.md")
marker = "R3_18AL_EVIDENCE_CLOSURE:\n"
if continue_text.count(marker) != 1:
    raise SystemExit("MIMIR_CONTINUE_HERE.md: AL closure marker drift")
am_block = f"""R3_18AM_EVIDENCE_CLOSURE:
  Outcome A / read-only / production unchanged at {PROD}
  evidence head/tree: {AM_HEAD} / {AM_TREE}
  authority run/job: {AM_RUN}/{AM_JOB} SUCCESS
  same-head normal CI: {CI_RUN}/{CI_JOB} SUCCESS / PR #135 closed unmerged
  artifact: {AM_ART} / {AM_SIZE} bytes / sha256:{AM_DIGEST}; downloaded ZIP digest exact / inner manifest 11/11 PASS
  47/47 published-AK exact / Int=47 / payload width 32 on 47/47 / semantic Int range 1..415 / native-oracle mismatch 0
  witness reselection 0 / another-control bits consumed 0 / earlier-payload-contract inheritance rejected
  repeatability/truncation/wrong-tag/wrong-start/wrong-version/corrupt-control/corrupt-prior/post-stop-poison 47/47 PASS
  production/Cargo/fixture/corpus/support mutation 0/0/0/0/0

"""
write("MIMIR_CONTINUE_HERE.md", continue_text.replace(marker, am_block + marker, 1))

# ---------------------------------------------------------------------------
# MIMIR_KNOWLEDGE_GRAPH.md
# ---------------------------------------------------------------------------
replace_one(
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "R3.18AM post-AK one-following-payload evidence / ACTIVE                                              |",
    "R3.18AM post-AK one-following-payload evidence / Outcome A CLOSED\nR3.18AN bounded post-AK one-following-payload production / ACTIVE                                      |",
    "graph frontier",
)
old_order = """112. `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`
113. `docs/continuity/MIMIR_R3_18AL_DECISION.md`
114. `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md`
115. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
116. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
117. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
118. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
119. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
120. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
121. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
new_order = """112. `docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md`
113. `docs/continuity/MIMIR_R3_18AL_DECISION.md`
114. `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md`
115. `docs/continuity/MIMIR_R3_18AM_DECISION.md`
116. `docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md`
117. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
118. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
119. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
120. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
121. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
122. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
123. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
replace_one("MIMIR_KNOWLEDGE_GRAPH.md", old_order, new_order, "mandatory order tail")
old_am_section = """### R3.18AM post-AK one-following-payload evidence: ACTIVE
- read-only; production frozen at R3.18AK `f20f529e3ada6e9a671ea91e5676a17a00770145`
- reuse exactly the immutable 47-row R3.18AI/R3.18AL lane; witness reselection 0
- start at AK payload_start; prove exactly one payload independently; stop at payload end; another-control bits remain 0
"""
new_am_section = f"""### R3.18AM post-AK one-following-payload evidence: OUTCOME A / CLOSED
- evidence `{AM_HEAD}` / tree `{AM_TREE}`; run/job `{AM_RUN}/{AM_JOB}` SUCCESS
- same-head CI `{CI_RUN}/{CI_JOB}` SUCCESS; PR #135 closed unmerged
- artifact `{AM_ART}` / `sha256:{AM_DIGEST}`; downloaded ZIP digest exact / internal manifest 11/11 PASS
- 47/47 published-AK exact; Int=47; width 32 on 47/47; semantic range 1..415; mismatch 0; witness reselection 0; another-control bits 0

### R3.18AN bounded post-AK one-following-payload production: ACTIVE
- production remains frozen at R3.18AK `{PROD}` until a clean R3.18AN candidate is published
- validate/recompute the R3.18AK/AJ boundary; admit only R3.18AM Int/32; stop exactly at payload end
- another property-control bit, alternate payload tags/layouts and generalized cursor/loop remain closed
"""
replace_one("MIMIR_KNOWLEDGE_GRAPH.md", old_am_section, new_am_section, "AM/AN sections")

# ---------------------------------------------------------------------------
# Boundary locks
# ---------------------------------------------------------------------------
new_override = f"""# 0. Current override — R3.18AM closed / R3.18AN active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18AK
- `{PROD}` / `{PROD_TREE}` remains canonical production;
- exact R3.18AJ membership; exactly one following header; stop at `payload_start`;
- post-AK payload production is not admitted until R3.18AN publishes.

## CLOSED EVIDENCE — R3.18AM Outcome A
- exact immutable 47-row lane; published-AK boundary exact 47/47;
- `Int=47`; payload width `32` on 47/47; semantic Int range `1..415`; mismatch 0; witness reselection 0;
- artifact `{AM_ART}` / `sha256:{AM_DIGEST}`; downloaded ZIP/internal manifest 11/11 PASS;
- another-control consumption 0; earlier payload-contract inheritance rejected.

## ACTIVE PRODUCTION GATE — R3.18AN
- validate/recompute a valid R3.18AK/AJ header boundary;
- begin exactly at the validated `payload_start`;
- decode exactly one R3.18AM-admitted `Int/32` payload;
- stop exactly at payload end and consume zero another-control bits;
- production candidate must contain only the minimum replay source plus one focused AN test.

## CLOSED
- another property-control bit after the R3.18AN payload end; alternate payload tags/layouts; repeated/generalized property loop or cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
"""
regex_replace_one(
    "docs/continuity/MIMIR_BOUNDARY_LOCKS.md",
    r"# 0\. Current override .*?\n---\n\n# 1\. Status vocabulary",
    new_override + "\n---\n\n# 1. Status vocabulary",
    "current override",
)

# ---------------------------------------------------------------------------
# Small current-state documents
# ---------------------------------------------------------------------------
write(
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-21
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18AK — bounded post-AG following-header production composition`
**Last read-only evidence:** `R3.18AM — Outcome A / post-AK Int payload exact 47/47 / width32=47 / semantic 1..415 / mismatch 0 / artifact {AM_ART}`
**Last contract:** `R3.18AJ — Outcome A / exact_tuple_only / 17 contexts / multiplicity 47 / sha256:{AJ_CONTRACT}`
**Current exact pass:** `R3.18AN — bounded post-AK one-following-payload production`

## Truthful boundary

R3.18AK remains published production and stops at the admitted post-AG following-header `payload_start`. R3.18AM independently proved the next single payload on all 47 frozen rows: `Int=47`, exact width 32 on 47/47, semantic integer range 1..415, native/oracle mismatch 0, witness reselection 0, and zero another-control consumption. This is evidence authority only; payload production opens only through R3.18AN.

```text
R3.18AM evidence                    {AM_RUN}/{AM_JOB} SUCCESS
R3.18AM same-head CI                {CI_RUN}/{CI_JOB} SUCCESS
R3.18AM validation PR               #135 closed unmerged
R3.18AM artifact                    {AM_ART} / {AM_SIZE} / sha256:{AM_DIGEST}
production mutation                 0
another control consumed            0
```

## Current gate

R3.18AN is bounded production. It must validate/recompute the R3.18AK/AJ header boundary, begin exactly at the proven payload start, decode exactly one R3.18AM-admitted `Int/32` payload, stop exactly at payload end, and consume zero bits of another property-control boundary.

## Hard stop

Another property control, alternate payload tags/layouts, generalized/repeated property iteration or cursor, next actor/frame/lifecycle and raw-state/event/slice/skill/counterfactual/runtime/export behavior remain closed.
""",
)

write(
    "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",
    f"""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AK** at `{PROD}` / `{PROD_TREE}`. R3.18AM is now **Outcome A / CLOSED** as read-only post-AK payload evidence: head `{AM_HEAD}` / tree `{AM_TREE}`, run/job `{AM_RUN}/{AM_JOB}` SUCCESS, same-head CI `{CI_RUN}/{CI_JOB}` SUCCESS, validation PR #135 closed unmerged, artifact `{AM_ART}` / `sha256:{AM_DIGEST}` independently downloaded and internally verified 11/11.

Frozen AM result: 47/47 published-AK boundary exact; `Int=47`; payload width 32 on 47/47; semantic Int range 1..415; native/oracle mismatch 0; witness reselection 0; another-control bits 0; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0. Earlier payload contracts were not inherited as authority.

The active pass is **R3.18AN**, bounded one-following-payload production. Reconstruct from fresh canonical main, validate/recompute the R3.18AK/AJ boundary, admit only the AM-proven `Int/32` payload, stop exactly at payload end, and consume zero following-control bits. Do not cherry-pick stale preparatory AN branches as authority.

Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json`, `docs/continuity/MIMIR_R3_18AK_DECISION.md`, `docs/continuity/MIMIR_R3_18AL_DECISION.md`, `docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md`, `docs/continuity/MIMIR_R3_18AM_DECISION.md`, and `docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md` before widening.
""",
)

# ---------------------------------------------------------------------------
# Append-only progress ledger
# ---------------------------------------------------------------------------
ledger = read("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
heading = "## 2026-08-21 — R3.18AM — Post-AK One Following-Payload Evidence — Outcome A / CLOSED"
if heading in ledger:
    raise SystemExit("progress ledger already contains R3.18AM closure")
ledger_block = f"""

{heading}

- Canonical production unchanged: `{PROD}` / `{PROD_TREE}`.
- Evidence authority: `{AM_HEAD}` / `{AM_TREE}`; run/job `{AM_RUN}/{AM_JOB}` SUCCESS.
- Same-head normal CI: `{CI_RUN}/{CI_JOB}` SUCCESS; validation PR #135 closed unmerged.
- Immutable artifact: `{AM_ART}` / {AM_SIZE} bytes / `sha256:{AM_DIGEST}`; downloaded ZIP digest exact and internal manifest 11/11 PASS.
- Result: published-AK boundary exact 47/47; `Int=47`; width 32 on 47/47; semantic Int range 1..415; native/oracle mismatch 0; witness reselection 0.
- Negative controls: repeatability, payload truncation, wrong tag, wrong payload start, wrong exact version/context, corrupt AG control, corrupt prior, post-payload-end poison all 47/47 PASS.
- Earlier payload-contract inheritance: REJECTED. Another property-control bits consumed: 0.
- Production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0.
- Superseded harness-only failures were not rerun: runs 32473299304 and 32473502712.
- Next pass opened: R3.18AN bounded post-AK `Int/32` one-payload production.
"""
write("docs/continuity/MIMIR_PROGRESS_LEDGER.md", ledger.rstrip() + ledger_block + "\n")

# ---------------------------------------------------------------------------
# Machine-readable continuity state
# ---------------------------------------------------------------------------
state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-21"
state["last_completed_read_only_audit"] = "R3.18AM"
state["current_pass"] = "R3.18AN"
state["current_pass_kind"] = "bounded production implementation / one post-AK Int/32 payload"
state["current_pass_goal"] = "Validate/recompute the R3.18AK/AJ header boundary, begin exactly at payload_start, decode exactly one R3.18AM-admitted Int/32 payload, stop at payload end, and consume zero another-control bits."
state["current_pass_stop_boundary"] = "Exactly one R3.18AM-admitted Int/32 payload end after R3.18AK. No another property control, alternate payload layout, generalized loop/cursor, next actor/frame or semantic/runtime/export widening."
state["last_completed_evidence_pass"] = "R3.18AM"
state["last_completed_evidence_outcome"] = "A — one post-AK Int payload exact 47/47; width 32 on 47/47; semantic Int range 1..415; native-oracle mismatch 0; witness reselection 0; another-control bits 0; artifact 9443581172."

closed = list(state.get("closed_now", []))
for item in [
    "post-R3.18AK following-payload production before R3.18AN publication",
    "another property control after the one R3.18AN payload end",
    "payload tags/layouts outside the R3.18AM Int/32 authority",
    "earlier payload-contract inheritance at the R3.18AN boundary",
]:
    if item not in closed:
        closed.append(item)
state["closed_now"] = closed

order = list(state.get("next_files_to_read", []))
for p in [
    "docs/continuity/MIMIR_R3_18AL_DECISION.md",
    "docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md",
    "docs/continuity/MIMIR_R3_18AM_DECISION.md",
    "docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md",
]:
    order = [x for x in order if x != p]
anchor = "docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md"
if anchor not in order:
    raise SystemExit("continuity state reading-order anchor missing")
pos = order.index(anchor) + 1
order[pos:pos] = [
    "docs/continuity/MIMIR_R3_18AL_DECISION.md",
    "docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md",
    "docs/continuity/MIMIR_R3_18AM_DECISION.md",
    "docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md",
]
state["next_files_to_read"] = order

state["r3_18am"] = {
    "outcome": "A",
    "closed": True,
    "pass_kind": "read-only post-AK one-following-payload evidence",
    "production_sha": PROD,
    "evidence_head": AM_HEAD,
    "evidence_tree": AM_TREE,
    "authority_run": AM_RUN,
    "authority_job": AM_JOB,
    "same_head_ci_run": CI_RUN,
    "same_head_ci_job": CI_JOB,
    "validation_pr": 135,
    "artifact_id": AM_ART,
    "artifact_size": AM_SIZE,
    "artifact_sha256": AM_DIGEST,
    "rows": 47,
    "published_ak_exact": 47,
    "tags": {"Int": 47},
    "payload_widths": {"32": 47},
    "semantic_int_min": 1,
    "semantic_int_max": 415,
    "native_oracle_mismatch": 0,
    "witness_reselection": 0,
    "another_control_bits_consumed": 0,
    "earlier_payload_contract_inheritance_assumed": False,
    "production_cargo_fixture_corpus_support_mutation": "0/0/0/0/0",
}
write(str(state_path), json.dumps(state, indent=2, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------------------
# Decision + next execution spec
# ---------------------------------------------------------------------------
decision = f"""# MIMIR R3.18AM — Post-AK One Following-Payload Evidence Decision

**Date:** 2026-08-21
**Outcome:** **A — ADMITTED / READ-ONLY PAYLOAD EVIDENCE**
**Production mutation:** none
**Canonical production:** `{PROD}` / `{PROD_TREE}`

## Decision

R3.18AM closes Outcome A. On exactly the immutable 47-row R3.18AI/R3.18AL lane, the published R3.18AK boundary was reconstructed exactly and one following payload was observed independently with pinned Boxcars plus the existing native primitive scalar decoder. All 47 headers were `Int`; all 47 payloads were exactly 32 bits; privacy-safe semantic values ranged from 1 through 415. Native and oracle start/end/width/value matched on 47/47 rows with mismatch zero and witness reselection zero.

This pass consumes zero bits of the following property-control boundary. It is evidence only and does not itself publish a post-AK payload API.

## Exact authority

```text
canonical parent main/tree           {BASE} / {BASE_TREE}
production SHA/tree                  {PROD} / {PROD_TREE}
R3.18AJ contract SHA256              {AJ_CONTRACT}
R3.18AL authority head               {AL_HEAD}
evidence head/tree                   {AM_HEAD} / {AM_TREE}
authority run/job                    {AM_RUN} / {AM_JOB} SUCCESS
same-head normal CI                  {CI_RUN} / {CI_JOB} SUCCESS
validation PR                        #135 closed unmerged
artifact                             {AM_ART} / {AM_SIZE} bytes
artifact digest / ZIP SHA256         sha256:{AM_DIGEST}
```

The downloaded artifact ZIP SHA-256 equals the GitHub artifact digest exactly. Its internal SHA-256 manifest verifies all 11 payload files.

## Frozen result

```text
frozen rows                          47/47
published R3.18AK exact              47/47
observed tags                        Int=47
observed payload width               32 bits on 47/47
semantic Int range                   1..415
native/oracle mismatch               0
witness reselection                  0
another property-control bits read   0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy scan                         PASS
```

## Negative controls

Repeatability, exact payload truncation, wrong-tag boundary guard, wrong-payload-start boundary guard, wrong exact version/context, corrupt AG control, corrupt prior, and post-payload-end poison invariance pass on 47/47 rows. Earlier R3.18AC/R3.18S payload contracts were explicitly not inherited as authority.

## Superseded attempts

Run `32473299304` on head `72184f77f3016ac38a41ca5bb11a9b44f2f1b16a` stopped before payload measurement because a temporary Boxcars instrumentation insertion marker did not match. Run `32473502712` on head `8917d4bfe69418f74f03b5611bf91670effad827` reached the independent 47/47 Boxcars payload oracle and then stopped because Rust 1.85 minimal lacked the rustfmt component required by the temporary native probe. Neither SHA was rerun. The immutable authority is `{AM_HEAD}`.

## Hard stop

Production remains R3.18AK until R3.18AN is separately implemented, validated and published. Another property-control bit, alternate payload tags/layouts, repeated/generalized property loops/cursors, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export behavior remain closed.

## Next gate

R3.18AN is a bounded production pass. It may compose exactly one post-AK `Int/32` payload only after validating/recomputing the supplied R3.18AK/AJ header authority, must start exactly at `payload_start`, stop exactly at the 32-bit payload end, and consume zero bits of the following property-control boundary.
"""
write("docs/continuity/MIMIR_R3_18AM_DECISION.md", decision)

an_spec = f"""# MIMIR R3.18AN — Bounded Post-AK One Following-Payload Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production parent:** R3.18AK `{PROD}` / `{PROD_TREE}`
**Evidence authority:** R3.18AM Outcome A / `{AM_HEAD}`
**Admitted payload family:** `Int / 32 bits` only
**Another property-control bit:** forbidden

## 1. Goal

Publish exactly one boundary-specific payload composition after a valid R3.18AK following-header result. The API must validate or recompute the supplied R3.18AK/AJ authority, begin exactly at the validated `payload_start`, decode exactly one R3.18AM-admitted signed `Int` payload of 32 bits with the existing primitive scalar machinery, return the exact payload boundary/value identity, and stop exactly at payload end.

No generic cursor or repeatedly-chainable property loop is admitted.

## 2. Frozen authority

```text
R3.18AK production SHA/tree          {PROD} / {PROD_TREE}
R3.18AJ exact-context contract       sha256:{AJ_CONTRACT} / 17 tuples / multiplicity 47 / Int=47
R3.18AL published-header authority   {AL_HEAD}
R3.18AM evidence head/tree           {AM_HEAD} / {AM_TREE}
R3.18AM authority run/job            {AM_RUN} / {AM_JOB} SUCCESS
R3.18AM same-head CI                 {CI_RUN} / {CI_JOB} SUCCESS
R3.18AM artifact                     {AM_ART} / sha256:{AM_DIGEST}
R3.18AM frozen rows                  47
R3.18AM payload identity             Int=47 / width32=47 / semantic range 1..415
R3.18AM native/oracle mismatch       0
R3.18AM witness reselection          0
```

R3.18AM, not resemblance to earlier boundaries, is the authority for `Int/32` here.

## 3. Production contract

The new boundary-specific API must:

1. reject any replay/version/context outside the exact existing R3.18AK/AJ authority;
2. validate/recompute the supplied R3.18AK result instead of trusting arbitrary caller coordinates;
3. require the resolved header tag to be exactly `ReplayNetworkAttributeTagV1::Int`;
4. require the payload start to equal the validated R3.18AK header/composition stop;
5. call the existing primitive scalar decoder for exactly one `Int` payload;
6. require exact 32-bit width and `ReplayNetworkPrimitiveScalarValueV1::Int` identity;
7. expose the exact payload start/end/width/value and retain the validated header composition;
8. set final `stop_bit` to exactly the payload end;
9. consume zero following `property_present` bits.

Every other payload tag/layout is fail-closed even if a lower-level decoder can parse it elsewhere.

## 4. Required focused tests

At minimum:

- exact real frozen witness coverage sufficient to prove the admitted boundary plus deterministic equality with the existing lower scalar decoder;
- `Int/32` exact start/end/value and final stop equality;
- deterministic repeatability;
- truncation before all required payload bits rejects;
- wrong resolved tag rejects;
- payload-start/header-stop mismatch rejects;
- corrupt/mismatched R3.18AK prior rejects;
- wrong actor / unresolved lookup / wrong exact version context rejects through prerequisite recomputation;
- fabricated Cartesian AJ tuple and old Z/P-only context reject;
- post-payload-end poison, including the following control bit, leaves the result unchanged;
- following-control consumption remains 0.

Synthetic tests supplement but do not widen beyond the frozen AM authority.

## 5. Clean candidate

The clean production commit must contain only the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18AN test file. No workflow/helper, evidence artifact, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup may enter the production commit.

## 6. Validation and publication

Require Rust 1.85 format/check/test/clippy, focused AN tests, full `mimir-replay`, workspace tests, repository verification, exact clean-candidate CI, a single validation PR for the exact head, and force-free publication only after fresh-main ancestry verification. After publication require exact published-main SHA/tree readback and the unique natural push CI receipt. Before every dispatch/rerun, inspect queued/waiting/in-progress equivalent runs and reuse them instead of creating duplicates.

## 7. Hard stop

No following property-control bit, next header/payload, second control, generalized/repeated property loop/cursor, next actor/frame/lifecycle, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
The bounded `Int/32` post-AK composition matches the R3.18AM authority, all focused/negative/full validation passes, and following-control consumption remains zero. Publish only this one-payload composition, then open R3.18AO as a separate published-production differential.

### Outcome B
Only a strict safe subset of the R3.18AM authority can be implemented without widening. Publish only that exact subset and rewrite AO to the actual production contract.

### Outcome C
Authority drift, unexplained payload mismatch, context/layout widening, later-control access, generic chaining or validation contradiction. Stop without publication.
"""
write("docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md", an_spec)

# Final structural assertions.
for required in [
    "docs/continuity/MIMIR_R3_18AM_DECISION.md",
    "docs/continuity/MIMIR_R3_18AN_EXECUTION_SPEC.md",
]:
    if not Path(required).is_file():
        raise SystemExit(f"missing generated file: {required}")

state_check = json.loads(read("docs/continuity/MIMIR_CONTINUITY_STATE.json"))
assert state_check["current_pass"] == "R3.18AN"
assert state_check["last_completed_evidence_pass"] == "R3.18AM"
assert state_check["r3_18am"]["payload_widths"] == {"32": 47}
assert state_check["r3_18am"]["another_control_bits_consumed"] == 0

print("R3_18AM_ADMISSION_GENERATION=PASS")
print(f"R3_18AM_SAME_HEAD_CI={CI_RUN}/{CI_JOB}")
print("R3_18AN_GATE=OPEN_PREPARED_NOT_PRODUCTION")

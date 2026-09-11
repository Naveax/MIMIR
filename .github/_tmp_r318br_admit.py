from pathlib import Path
import json
import re


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one replacement target, found {count}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


decision = """# MIMIR R3.18BR — Next Property-Control Bit Evidence Decision

**Date:** 2026-09-11
**Outcome:** **A — CLOSED / ADMITTED READ-ONLY ONE-BIT EVIDENCE**
**Production mutation:** none
**Canonical production remains:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`

## Decision

R3.18BR closes Outcome A on exactly the two immutable R3.18BQ payload rows. Each BQ payload was byte-exactly rematerialized through its admitted `payload_end_bit`; the BP false terminator remained outside the BR lane. Exactly one following `property_present` bit was then observed with independent native evidence logic and pinned Boxcars, and native/oracle start/value/end matched 2/2 with zero reselection.

The observed distribution is **false=1 / true=1**. This distribution was not inherited from any historical boundary.

```text
BQ payload rows exact                    2/2
BQ rematerialization                     byte-exact 2/2
BP false terminator control access       0
next-control native/oracle exact          2/2
next-control false                        1
next-control true                         1
witness reselection                       0
following stream/header/payload           0/0/0
second later control                      0
production/Cargo/fixture/corpus/support   0/0/0/0/0
privacy + full validation                 PASS
```

Exact admitted observations:

- `external_fixtures/sample_002.replay`: admitted Boolean payload `[11238,11239)`; next control `[11239,11240)` = `false`.
- `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: admitted ActiveActor payload `[3205,3238)`; next control `[3238,3239)` = `true`.

## Exact authority

```text
canonical evidence parent/tree           265b780dc554715a7bc6bfb5c8e0fbe7ee279265 / d19218dea425819c8ec8eee8464ab5e198945bb6
production SHA/tree                      cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
BQ evidence head/tree                    16c43f38e740c57ae9cb90c92084002ec83815e7 / 58248877a59fb0ddad707e32f92b2cec91f6b434
BQ artifact                              10144392560 / sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c
BR evidence head/tree                    ff1daab35e2e75bf7446a98a07a1db67e5196dbd / 373d516dbab42b49216e50c09cbd6744863a88b1
BR run/job                               34606677020 / 103286690781 SUCCESS
BR same-head natural CI                  34606676915 / 103287920321 SUCCESS / count 1
BR artifact                              10267123608 / 8783 bytes / sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1
BR inner manifest SHA-256                f18ef70512227d5968a1fa0594bf522ae1924d9668a1bb353da8747618d3b7e1
pinned Boxcars                           c70e77df7af81b436cb545d070bb90c82f562d0b
```

The evidence candidate is exactly one commit ahead of the canonical parent and changes only `.github/workflows/_tmp_r318br_evidence.yml`. Its artifact manifest verifies every listed payload file. Workspace fmt/check/test/clippy, repository verifier, diff-check, privacy scan and unique same-head natural CI all passed.

## Canonical sequencing consequence

R3.18BR does **not** make the observed control bit the next production boundary. Canonical production R3.18BO still stops at following-header `payload_start`, because R3.18BQ payload decoding is evidence-only. Therefore the next bounded production pass is **R3.18BS**: publish exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload after a valid BO/BN header and stop at payload end. Only after that payload production is independently validated may the BR mixed control semantics be considered for production in a later pass.

## Hard stop

No production control-bit consumption is admitted by BR. No payload/control access on the BP false terminator, next stream/header/payload after the BR observation, second later control, generalized/repeated property cursor, actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening, or historical control-value inheritance is admitted.
"""

bs_spec = """# MIMIR R3.18BS — Bounded Post-BO One-Following-Payload Production

**Status:** ACTIVE
**Pass type:** bounded production implementation
**Production parent:** R3.18BO `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`
**Header contract:** R3.18BN `sha256:904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c` / 2 exact eight-field tuples / multiplicity 2
**Payload evidence authority:** R3.18BQ Outcome A / artifact `10144392560` / `sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c`
**Later-control evidence:** R3.18BR Outcome A / false=1 true=1 / artifact `10267123608` (evidence only; consumption forbidden in BS)
**Admitted payload families:** `Boolean / 1 bit` and `ActiveActor / 33 bits` only

## 1. Goal

Publish exactly one boundary-specific payload composition after a valid R3.18BO true following-header result. The API must validate or recompute the supplied BO/BN authority, begin exactly at the validated `payload_start`, decode exactly one R3.18BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload using existing admitted primitive machinery, return exact payload boundary/value identity, and stop exactly at payload end.

The one R3.18BP false terminator remains outside the BS payload lane. The R3.18BR-observed following control bit must not be consumed. No generic cursor or repeatedly-chainable property loop is admitted.

## 2. Frozen authority

```text
R3.18BO production SHA/tree              cbb823ce7d3fc871c35a83afc5ee21ae71945821 / 146cb78edfb434fd43e532593efce8e35ee97111
R3.18BN exact-context contract            904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c
R3.18BN contexts / multiplicity           2 / 2
R3.18BQ evidence head                     16c43f38e740c57ae9cb90c92084002ec83815e7
R3.18BQ artifact                          10144392560 / sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c
R3.18BQ payload identity                  Boolean=1x1 / ActiveActor=1x33
R3.18BQ native/oracle mismatch            0
R3.18BR evidence head                     ff1daab35e2e75bf7446a98a07a1db67e5196dbd
R3.18BR artifact                          10267123608 / sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1
R3.18BR next-control distribution         false=1 / true=1
R3.18BR control production authority      NONE
```

R3.18BQ, not resemblance to older payload ordinals, is the payload authority for BS. R3.18BR proves the boundary after those payloads but does not authorize BS to cross it.

## 3. Production contract

The new boundary-specific API must:

1. accept only a valid R3.18BO true following-header composition under exact R3.18BN membership;
2. reject the BP/BO false-terminator result before any payload decode;
3. validate/recompute supplied BO prerequisites instead of trusting arbitrary caller coordinates;
4. require the resolved header tag to be exactly the BQ-admitted Boolean or ActiveActor tag for its frozen context;
5. require payload start to equal the validated BO header/composition stop;
6. call existing primitive payload machinery for exactly one admitted payload;
7. require exact width and semantic identity: Boolean=1 bit or ActiveActor=33 bits;
8. expose exact payload start/end/width/value while retaining the validated BO header composition;
9. set final `stop_bit` to exactly payload end;
10. consume zero following `property_present` bits.

Every other payload tag/layout and every context outside exact BO/BN/BQ authority is fail-closed even if a lower-level primitive can decode it elsewhere.

## 4. Required focused tests

At minimum:

- exact two frozen BQ true rows reproduce the admitted BO header and payload boundary/value;
- Boolean row reproduces `[11238,11239)` and semantic `true`;
- ActiveActor row reproduces `[3205,3238)` and semantic `active=true, actor=1`;
- the BP false terminator is rejected/excluded before payload decode;
- exact start/end/width/value and final stop equality;
- deterministic repeatability;
- truncation before complete payload rejects atomically;
- wrong resolved tag rejects;
- payload-start/header-stop mismatch rejects;
- corrupt/mismatched BO prior rejects;
- wrong actor / unresolved lookup / wrong exact version context rejects through prerequisite recomputation;
- fabricated Cartesian BN tuple and historical BD/AT/AJ/Z/P-only context reject;
- post-payload-end poison, including the BR control bit, leaves the BS result unchanged;
- following-control consumption remains 0;
- source-scope guard proves no generic/repeated loop or later-control read.

## 5. Clean candidate

Expected clean production scope is the minimum `crates/mimir-replay/src/lib.rs` change plus one focused R3.18BS integration test file. No workflow/helper/evidence artifact, Cargo/dependency, fixture/corpus, continuity, skill/runtime/export or unrelated cleanup enters the production commit.

## 6. Validation and publication

Require Rust 1.85 formatting, focused BS tests, workspace check, clippy with warnings denied, workspace test, repository verifier, exact clean-candidate natural CI, fresh-main ancestry verification, force=false publication and published-main exact-SHA validation. Before any dispatch/rerun, inspect queued/waiting/in-progress equivalent runs; if an equivalent run exists, reuse that run ID. Rerun is never polling.

## 7. Hard stop

No R3.18BR following-control bit, next stream/header/payload, second later control, generalized/repeated property loop/cursor, next actor/frame/lifecycle advance, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## 8. Outcome gate

### Outcome A
Publish exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload composition after valid BO/BN authority, with all focused/negative/full validations PASS and following-control consumption zero. Then open R3.18BT as a separate published-production differential before any control-bit production is considered.

### Outcome B
Only a strict safe subset of the BQ payload authority can be implemented without widening. Publish only that subset and rewrite the next differential pass to the actual production contract.

### Outcome C
Authority drift, unexplained payload mismatch, context/layout widening, BR control-bit access, generic chaining or validation contradiction. Stop without publication.
"""

Path("docs/continuity/MIMIR_R3_18BR_DECISION.md").write_text(decision, encoding="utf-8")
Path("docs/continuity/MIMIR_R3_18BS_EXECUTION_SPEC.md").write_text(bs_spec, encoding="utf-8")

Path("docs/continuity/MIMIR_CURRENT_STATE.md").write_text("""# MIMIR — Current Canonical State

**Continuity date:** 2026-09-11
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `cbb823ce7d3fc871c35a83afc5ee21ae71945821`
**Production tree:** `146cb78edfb434fd43e532593efce8e35ee97111`
**Production milestone:** `R3.18BO — bounded post-BK mixed-continuation following-header production`
**Last read-only evidence/audit:** `R3.18BR — Outcome A / exact rows 2/2 / false=1 true=1 / native-oracle mismatch=0 / artifact 10267123608`
**Last completed contract:** `R3.18BN — exact_tuple_only / 2 contexts / multiplicity 2 / contract 904a6c69d716964f756000d71e9b36c10400176057003dc5b811b1d8eb87040c`
**Current exact pass:** `R3.18BS — bounded post-BO one-following-payload production`

## Truthful boundary

R3.18BO remains production and stops at the following-header `payload_start`. R3.18BQ admitted exactly two read-only payload witnesses: Boolean `[11238,11239)` width1/value=true and ActiveActor `[3205,3238)` width33/active=true/actor=1.

R3.18BR independently observed exactly one next `property_present` bit after those immutable payload ends. Native and pinned Boxcars matched 2/2: Boolean-row control `[11239,11240)` = false; ActiveActor-row control `[3238,3239)` = true. BP-false access, witness reselection and adjacent reads remained zero.

R3.18BS is the active bounded production pass. It may publish exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload after valid BO/BN authority and must stop exactly at payload end.

## Hard stop

No BS consumption of the BR control bit, no payload access on the BP false terminator, no next stream/header/payload or second later control, no generalized cursor, and no wider semantic/runtime behavior.
""", encoding="utf-8")

Path("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md").write_text("""# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BO** at `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111`.

R3.18BQ is **Outcome A / CLOSED** at `16c43f38e740c57ae9cb90c92084002ec83815e7`; artifact `10144392560` / `sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c`. Exact lane: one Boolean/1-bit payload and one ActiveActor/33-bit payload; the BP false terminator remained excluded.

R3.18BR is **Outcome A / CLOSED** at `ff1daab35e2e75bf7446a98a07a1db67e5196dbd` / `373d516dbab42b49216e50c09cbd6744863a88b1`; run/job `34606677020/103286690781` SUCCESS; same-head CI `34606676915/103287920321` SUCCESS / count 1; artifact `10267123608` / 8783 bytes / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1`; inner manifest `f18ef70512227d5968a1fa0594bf522ae1924d9668a1bb353da8747618d3b7e1`. Exact observed controls: Boolean row `[11239,11240)` = false; ActiveActor row `[3238,3239)` = true; native/oracle exact=2/2; BP-false access=0; adjacent consumption=0/0/0/0.

Active pass: **R3.18BS — bounded post-BO one-following-payload production**. Publish exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload after valid BO/BN authority and stop exactly at payload end. BR control consumption remains forbidden in BS. Production/Cargo/fixture/corpus/support scope must remain narrowly bounded and all historical cross-boundary inference stays fail-closed.
""", encoding="utf-8")

sp = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(sp.read_text(encoding="utf-8"))
if state.get("current_pass") != "R3.18BR" or state.get("last_completed_read_only_audit") != "R3.18BQ":
    raise SystemExit("continuity state drift before BR admission")
state["updated_date"] = "2026-09-11"
state["last_completed_read_only_audit"] = "R3.18BR"
state["current_pass"] = "R3.18BS"
state["current_pass_kind"] = "bounded post-BO one-following-payload production on the two R3.18BQ payload rows"
state["current_pass_goal"] = "Publish exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload after valid R3.18BO/R3.18BN authority and stop at payload end."
state["current_pass_stop_boundary"] = "Stop exactly at BS payload_end_bit. Do not consume the R3.18BR following control bit or any later stream/header/payload/control."
state["r3_18br"] = {
    "status": "closed_outcome_a",
    "head": "ff1daab35e2e75bf7446a98a07a1db67e5196dbd",
    "tree": "373d516dbab42b49216e50c09cbd6744863a88b1",
    "run": 34606677020,
    "job": 103286690781,
    "same_head_ci_run": 34606676915,
    "same_head_ci_job": 103287920321,
    "artifact": 10267123608,
    "artifact_size": 8783,
    "artifact_digest": "sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1",
    "inner_manifest_sha256": "f18ef70512227d5968a1fa0594bf522ae1924d9668a1bb353da8747618d3b7e1",
    "target_rows": 2,
    "native_oracle_exact": 2,
    "false": 1,
    "true": 1,
    "witness_reselection": 0,
    "bp_false_control_access": 0,
    "following_stream_consumed": 0,
    "following_header_consumed": 0,
    "following_payload_consumed": 0,
    "second_later_control_consumed": 0,
}
nfr = state.get("next_files_to_read", [])
for item in ["docs/continuity/MIMIR_R3_18BR_DECISION.md", "docs/continuity/MIMIR_R3_18BS_EXECUTION_SPEC.md"]:
    if item not in nfr:
        nfr.append(item)
state["next_files_to_read"] = nfr
sp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

replace_once(
    "MIMIR_CONTINUE_HERE.md",
    """LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.18BQ — one following payload Outcome A / true=2 / Boolean=1x1 / ActiveActor=1x33 / mismatch 0 / artifact 10144392560""",
    """LAST_COMPLETED_READ_ONLY_AUDIT:
  R3.18BR — next property-control bit Outcome A / exact=2/2 / false=1 true=1 / mismatch 0 / artifact 10267123608""",
)
replace_once(
    "MIMIR_CONTINUE_HERE.md",
    """LAST_COMPLETED_EVIDENCE_PASS:
  R3.18BQ — exact two payloads / Boolean width1 / ActiveActor K2 width33 / mismatch=0 / next-control=0 / artifact 10144392560

CURRENT_PASS:
  R3.18BR — next property-control bit evidence after exact BQ payload end

CURRENT_PASS_TYPE:
  read-only exactly-one-control-bit differential evidence / BQ payload rows=2 / unknown false-true distribution / no next stream-header-payload""",
    """LAST_COMPLETED_EVIDENCE_PASS:
  R3.18BR — exact two next-control observations / Boolean-row=false / ActiveActor-row=true / mismatch=0 / adjacent reads=0 / artifact 10267123608

CURRENT_PASS:
  R3.18BS — bounded post-BO one-following-payload production

CURRENT_PASS_TYPE:
  bounded production implementation / exact BQ payload rows=2 / Boolean width1 + ActiveActor width33 / BR control consumption forbidden""",
)
cp = Path("MIMIR_CONTINUE_HERE.md")
ct = cp.read_text(encoding="utf-8")
marker = "# CURRENT OVERRIDE — 2026-09-11 — R3.18BR CLOSED / R3.18BS ACTIVE"
if marker in ct:
    raise SystemExit("BR admission override already present")
ct += """

# CURRENT OVERRIDE — 2026-09-11 — R3.18BR CLOSED / R3.18BS ACTIVE

- BR `ff1daab35e2e75bf7446a98a07a1db67e5196dbd` / `34606677020/103286690781` SUCCESS; same-head CI `34606676915/103287920321` SUCCESS / count 1.
- artifact `10267123608` / 8783 bytes / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1` / inner manifest `sha256:f18ef70512227d5968a1fa0594bf522ae1924d9668a1bb353da8747618d3b7e1`.
- exact controls: Boolean payload end 11239 -> `[11239,11240)` false; ActiveActor payload end 3238 -> `[3238,3239)` true; native/oracle 2/2; reselection 0; BP-false access 0; adjacent consumption 0/0/0/0.
- active R3.18BS: publish exactly one BQ-admitted Boolean/1-bit or ActiveActor/33-bit payload after exact BO/BN authority and stop at payload end. BR control remains evidence-only and closed to BS.
"""
cp.write_text(ct, encoding="utf-8")

replace_once(
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "R3.18BR next property-control bit evidence after exact BQ payload end / ACTIVE",
    "R3.18BR next property-control bit evidence after exact BQ payload end / Outcome A CLOSED\nR3.18BS bounded post-BO one-following-payload production / ACTIVE",
)
replace_once(
    "MIMIR_KNOWLEDGE_GRAPH.md",
    "185. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "185. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`\n186. `docs/continuity/MIMIR_R3_18BR_DECISION.md`\n187. `docs/continuity/MIMIR_R3_18BS_EXECUTION_SPEC.md`",
)
kg = Path("MIMIR_KNOWLEDGE_GRAPH.md")
kgt = kg.read_text(encoding="utf-8")
kgt += """

### R3.18BR next property-control evidence: Outcome A / CLOSED
- evidence `ff1daab35e2e75bf7446a98a07a1db67e5196dbd`; run/job `34606677020/103286690781` SUCCESS; same-head CI `34606676915/103287920321` SUCCESS.
- exact BQ rows 2/2; native/oracle exact 2/2; observed false=1 true=1; BP-false access=0; witness reselection=0; adjacent reads 0/0/0/0.
- Boolean-row control `[11239,11240)` = false; ActiveActor-row control `[3238,3239)` = true.
- artifact `10267123608` / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1`.

### R3.18BS bounded post-BO one-following-payload production: ACTIVE
- production remains R3.18BO until BS is actually published.
- authority is exact BQ Boolean/1 + ActiveActor/33 payload evidence under BO/BN; BR control is evidence-only and must not be consumed.
- stop exactly at payload end; no next control/stream/header/payload or generalized cursor.
"""
kg.write_text(kgt, encoding="utf-8")

bp = Path("docs/continuity/MIMIR_BOUNDARY_LOCKS.md")
bt = bp.read_text(encoding="utf-8")
new_override = """# 0. Current override — R3.18BR next-control evidence closed / R3.18BS payload production active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BO
- `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111` remains canonical production until BS is published.
- BQ payload composition and BR later-control consumption remain absent from production.

## CLOSED READ-ONLY NEXT-CONTROL EVIDENCE — R3.18BR
- evidence `ff1daab35e2e75bf7446a98a07a1db67e5196dbd` / `34606677020/103286690781` SUCCESS; same-head CI `34606676915/103287920321` SUCCESS / count 1.
- artifact `10267123608` / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1` / inner manifest `f18ef70512227d5968a1fa0594bf522ae1924d9668a1bb353da8747618d3b7e1`.
- exact=2/2; false=1 true=1; BP-false access=0; adjacent stream/header/payload/second-control=0/0/0/0.

## ACTIVE BOUNDED PAYLOAD PRODUCTION — R3.18BS
- exactly the two BQ-admitted payload contexts may be implemented: Boolean/1 bit and ActiveActor/33 bits.
- valid BO/BN authority is mandatory; stop exactly at payload end.

## CLOSED
- payload access on the BP false terminator;
- BR following-control consumption during BS;
- next stream/header/payload after BS;
- second later control;
- generalized/repeated cursor and wider semantics/runtime.

"""
bt2, n = re.subn(r"# 0\. Current override.*?(?=# 1\. Status vocabulary)", new_override, bt, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f"boundary-lock override replacement count={n}")
bp.write_text(bt2, encoding="utf-8")

lp = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
lt = lp.read_text(encoding="utf-8")
ledger_marker = "## 2026-09-11 — R3.18BR — Next Property-Control Bit Evidence"
if ledger_marker in lt:
    raise SystemExit("BR ledger entry already present")
lt += """

## 2026-09-11 — R3.18BR — Next Property-Control Bit Evidence
Outcome: **A — CLOSED / ADMITTED READ-ONLY EVIDENCE**

- Evidence `ff1daab35e2e75bf7446a98a07a1db67e5196dbd` / `34606677020/103286690781` SUCCESS; same-head CI `34606676915/103287920321` SUCCESS / count 1.
- Artifact `10267123608` / 8783 bytes / `sha256:bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1`; inner manifest `f18ef70512227d5968a1fa0594bf522ae1924d9668a1bb353da8747618d3b7e1`.
- Exact BQ rematerialization 2/2; native/oracle control exact 2/2; false=1 true=1; reselection=0; BP-false control access=0.
- Boolean control `[11239,11240)` = false; ActiveActor control `[3238,3239)` = true.
- Following stream/header/payload/second-control consumption `0/0/0/0`; production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`; privacy/full validation PASS.
- Sequencing: production remains BO; R3.18BS opens bounded BQ-payload production before BR control semantics can be considered for production.
"""
lp.write_text(lt, encoding="utf-8")

assert "R3.18BS — bounded post-BO one-following-payload production" in Path("MIMIR_CONTINUE_HERE.md").read_text(encoding="utf-8")
assert "R3.18BS bounded post-BO one-following-payload production / ACTIVE" in Path("MIMIR_KNOWLEDGE_GRAPH.md").read_text(encoding="utf-8")
assert json.loads(Path("docs/continuity/MIMIR_CONTINUITY_STATE.json").read_text(encoding="utf-8"))["current_pass"] == "R3.18BS"

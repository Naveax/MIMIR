from pathlib import Path
import json, re

EXPECTED_MAIN = "3257d32fbc617b6dae7bb42d41629639acf6ce95"
PROD = "2b608aafae97b10ecbc884f99e4bd4a73abf7a5c"
EVIDENCE_HEAD = "45090a2c18fb517088bb411782bbaed0d7d68199"
EVIDENCE_RUN = "31975063743"
EVIDENCE_JOB = "95233164711"
NORMAL_RUN = "31975063703"
NORMAL_JOB = "95233164610"
ARTIFACT_ID = "9270842140"
ARTIFACT_DIGEST = "sha256:9890ed33780412a8900692a627b212d80428a08229f9f691d914c8def31e06e2"


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly one match, got {n}")
    return text.replace(old, new, 1)

# Decision and next exact spec.
decision = f'''# MIMIR R3.18I — Second-Property Payload Evidence Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**
**Production mutation:** **NONE**
**Production authority remains:** `{PROD}`

## Decision

R3.18I is admitted as read-only evidence. The frozen R3.18F/R3.18H lane was reused without witness reselection. All 94 rows reproduced: 47 terminators remained no-second-payload controls and all 47 continuations decoded exactly one second-property payload from the already-proven second `payload_start` through its exact payload end.

The continuation distribution is exactly `Int=46 / String=1`. Native/oracle mismatch is zero. No third-property/control bit was consumed. Wrong-tag, truncation, repeatability and post-payload poison/invariance controls passed. Production Rust, Cargo, fixtures, corpus and support lanes remained unchanged.

## Immutable authority

```text
pre-pass canonical main             {EXPECTED_MAIN}
evidence head                       {EVIDENCE_HEAD}
evidence workflow run/job           {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
same-head normal CI run/job          {NORMAL_RUN} / {NORMAL_JOB} SUCCESS
artifact                            {ARTIFACT_ID} / 18741 bytes
artifact digest                     {ARTIFACT_DIGEST}
frozen rows                         94/94
terminator / continuation           47 / 47
continuation tags                   Int=46 / String=1
native/oracle mismatch              0
third-property bits consumed        0
witness reselection                 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

## Payload contract established by evidence

For the exact R3.18I lane only:

- `Int`: exactly 32 payload bits, native primitive-scalar semantics, exact end cursor;
- `String`: exactly the already-admitted K2 String wire contract for the observed row, declared length 7, Windows-1252, exact 88-bit payload width and exact end cursor;
- a terminator has no second payload and stops at the R3.18G control end;
- a continuation begins only at the R3.18G second header's exact `payload_start`;
- success stops immediately after exactly one second payload;
- the next `property_present` bit is outside this evidence pass.

This is evidence authority, not a production capability claim.

## Hard stop retained

Production still does not compose or expose a second-property payload, does not read the third `property_present` bit, and has no repeated/general property loop. Next actor/frame iteration, actor lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening remain closed.

## Next exact pass

`R3.18J — bounded native second-property payload composition` may implement only the exact `Int | String` second-payload surface established here, with one payload maximum and no third-control access.
'''
Path("docs/continuity/MIMIR_R3_18I_DECISION.md").write_text(decision, encoding="utf-8")

spec = f'''# MIMIR R3.18J — Bounded Native Second-Property Payload Composition

**Status:** ACTIVE
**Pass type:** production implementation
**Evidence authority:** R3.18I Outcome A
**Production authority before pass:** `{PROD}`
**Allowed second-payload tags:** exactly `Int | String`
**Third property / repeated loop:** forbidden

## 1. Goal

Publish the smallest production composition justified by R3.18I. Starting from the published R3.18G result after one valid R3.18B first primitive property, preserve the terminator path unchanged or decode exactly one present second payload and return its typed value plus exact payload end/stop cursor.

This pass is deliberately not a generic property cursor and not a property loop.

## 2. Frozen evidence authority

```text
R3.18I evidence head                {EVIDENCE_HEAD}
R3.18I run/job                      {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
R3.18I same-head normal CI          {NORMAL_RUN} / {NORMAL_JOB} SUCCESS
R3.18I artifact                     {ARTIFACT_ID}
R3.18I artifact digest              {ARTIFACT_DIGEST}
frozen rows                         94/94
terminator / continuation           47 / 47
second-payload tags                 Int=46 / String=1
native/oracle mismatch              0
third-property bits consumed        0
```

Before mutation, fetch fresh `main`; prove production source/tests are unchanged from `{PROD}` or re-audit any production drift. Verify the evidence receipts and artifact identity above.

## 3. Admitted implementation shape

Reuse existing production primitives rather than duplicating wire logic:

- R3.18G bounded optional second-header composition;
- `decode_replay_network_primitive_scalar_v1` for the exact `Int` second payload;
- `decode_replay_network_k2_v1` for the exact observed `String` second payload with the same admitted context required by the existing K2 decoder.

The new API/result name must encode bounded **after-first-primitive second property payload** semantics. It may return the existing R3.18G result plus an optional typed second payload and exact stop bit.

Terminator:

```text
R3.18G control false
-> second_header=None
-> second_payload=None
-> stop exactly at control end
-> no payload decoder call
```

Continuation:

```text
R3.18G second_header present
-> require resolved tag Int or String
-> start exactly at header.payload_start_bit
-> decode exactly one payload with the already-published lower-level decoder
-> stop exactly at returned payload end
-> do not read the following property_present bit
```

## 4. Required value identity

For `Int`, preserve native signed integer semantics and raw/start/end/width identity from the primitive-scalar result. For `String`, preserve the existing K2 String typed semantic value and exact payload start/end/width identity. Do not invent a second text decoder.

## 5. Fail-closed rules

Reject atomically on malformed/inconsistent first property, R3.18G composition failure, missing payload start, tag outside exact `Int | String`, scalar/K2 decode failure, truncation, invalid String length/context or any stop/end inconsistency. A failure must not be converted into partial successful second-payload composition.

## 6. Required focused tests

At minimum:

- terminator returns no header/no payload and performs zero payload lookup/decode;
- Int second payload success, aligned and unaligned starts, exact 32-bit width/end/value;
- String second payload success in the exact admitted context, exact length/encoding/end/value;
- R3.18I-shaped real boundary witnesses;
- truncation at every required Int payload boundary;
- String truncation / malformed length / wrong context;
- tag outside `Int | String` rejects before payload;
- bytes after payload end may be poisoned without changing the result;
- result is exactly repeatable;
- explicit proof that no third `property_present` bit is read.

## 7. Clean production scope

Preferred clean scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18j_*.rs`

No Cargo manifest/lockfile, fixture, corpus, continuity file, temporary workflow/tool or support-lane change may enter the clean production commit.

## 8. Validation and publication

Require focused tests, full `mimir-replay`, workspace check/test/clippy at Rust 1.85 floor, repository verifier, exact clean-candidate SHA validation, fresh-main ancestry audit, force-free publication, fresh-main readback and exact published-main validation.

## 9. Hard stop

R3.18J does not admit the third `property_present` bit, a third property header/payload, repeated/generalized property loops, generic cursor chaining, second-header tags outside `Int | String`, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening or dependency/corpus/support expansion.

## 10. Outcome gate

### Outcome A
The exact bounded second payload composition is published and all validation gates pass. Then run a separate real-replay differential audit of the published R3.18J API before opening the next property-control boundary.

### Outcome B
A bounded mismatch appears. Record it and keep production at R3.18G.

### Outcome C
Any scope drift, third-control access, generalized loop, dependency widening, validation contradiction or unadmitted payload form. Stop without publication.
'''
Path("docs/continuity/MIMIR_R3_18J_EXECUTION_SPEC.md").write_text(spec, encoding="utf-8")

# Machine continuity.
state_path = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"] = "2026-08-17"
state["last_completed_read_only_audit"] = "R3.18I"
state["current_pass"] = "R3.18J"
state["current_pass_kind"] = "production implementation / bounded second-property payload composition"
state["current_pass_goal"] = "Publish exactly one optional second-property payload after the R3.18G bounded second header, only for the R3.18I-admitted Int/String surface, returning exact payload end without reading the third property_present bit."
state["current_pass_stop_boundary"] = "Terminators stop at R3.18G control end. Continuations may compose exactly one Int/String second payload through its exact end. The following property_present bit, third property, generalized loop, next actor/frame/lifecycle/raw-state/event/skill/runtime/export boundaries remain closed."
state["r3_18i"] = {
    "outcome": "A",
    "kind": "read-only evidence",
    "evidence_head": EVIDENCE_HEAD,
    "evidence_run": int(EVIDENCE_RUN),
    "evidence_job": int(EVIDENCE_JOB),
    "normal_ci_run": int(NORMAL_RUN),
    "normal_ci_job": int(NORMAL_JOB),
    "artifact_id": int(ARTIFACT_ID),
    "artifact_digest": ARTIFACT_DIGEST,
    "frozen_rows": 94,
    "terminators": 47,
    "continuations": 47,
    "int_rows": 46,
    "string_rows": 1,
    "native_oracle_mismatch": 0,
    "third_property_bits_consumed": 0,
    "witness_reselection": 0
}
for f in ["docs/continuity/MIMIR_R3_18I_DECISION.md", "docs/continuity/MIMIR_R3_18J_EXECUTION_SPEC.md"]:
    if f not in state.get("next_files_to_read", []):
        state.setdefault("next_files_to_read", []).append(f)
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Current snapshot.
current = f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-17
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.18G — bounded second-property header composition`
**Completed read-only evidence:** `R3.18I — Outcome A / 94/94 / Int=46 String=1 / mismatch 0 / third-property bits 0`
**Current exact pass:** `R3.18J — bounded native second-property payload composition`

## Truthful production boundary

Production remains R3.18G. It can compose at most one optional second header and stops at that header's `payload_start`. R3.18I proved the exact second-payload contract on the frozen lane but did not change production.

## R3.18I closure

```text
evidence head                       {EVIDENCE_HEAD}
run/job                             {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS
same-head normal CI                 {NORMAL_RUN} / {NORMAL_JOB} SUCCESS
artifact                            {ARTIFACT_ID} / 18741 bytes
artifact digest                     {ARTIFACT_DIGEST}
rows                                94/94
terminator / continuation           47 / 47
payload tags                        Int=46 / String=1
native/oracle mismatch              0
third-property bits                 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

## Current gate

R3.18J may publish only one bounded optional second payload using the existing primitive Int and K2 String decoders. It must stop at exact payload end. It may not inspect the next `property_present` bit.

## Still closed

```text
third property control/header/payload
repeated/generalized property loop
generic repeatedly-chainable property cursor
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction / events / replay slicing
skill / teacher / runtime / export widening
dependency or corpus/support expansion
```
'''
Path("docs/continuity/MIMIR_CURRENT_STATE.md").write_text(current, encoding="utf-8")

# Handoff snapshot.
handoff = f'''# MIMIR — Next Chat Handoff

Fresh canonical continuity after R3.18I admission.

- Production authority: `{PROD}` (R3.18G). Production still stops at second `payload_start`.
- R3.18I: CLOSED Outcome A, read-only. Evidence `{EVIDENCE_HEAD}`, run/job `{EVIDENCE_RUN}/{EVIDENCE_JOB}`, artifact `{ARTIFACT_ID}`, digest `{ARTIFACT_DIGEST}`. 94/94 exact, Int=46, String=1, mismatch 0, third-property bits consumed 0.
- Current pass: `R3.18J — bounded native second-property payload composition`.
- Hard stop: exactly one optional second payload only; do not read the following `property_present` bit and do not create a property loop.
- Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, continuity state/current state, R3.18I decision and R3.18J spec before mutation.
'''
Path("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md").write_text(handoff, encoding="utf-8")

# Progress ledger append.
ledger = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
ledger_text = ledger.read_text(encoding="utf-8")
entry = f'''\n\n## 2026-08-17 — R3.18I admitted\n\n- Outcome A, read-only evidence; production unchanged at `{PROD}`.\n- Evidence `{EVIDENCE_HEAD}`; workflow `{EVIDENCE_RUN}/{EVIDENCE_JOB}` SUCCESS; same-head CI `{NORMAL_RUN}/{NORMAL_JOB}` SUCCESS.\n- Artifact `{ARTIFACT_ID}` / `{ARTIFACT_DIGEST}`; 94/94 exact; 47 terminators + 47 continuations; Int=46/String=1; mismatch 0; third-property bits 0.\n- Next exact pass: R3.18J bounded native second-property payload composition.\n'''
if "## 2026-08-17 — R3.18I admitted" not in ledger_text:
    ledger.write_text(ledger_text.rstrip() + entry, encoding="utf-8")

# Master handbook targeted sync.
p = Path("MIMIR_CONTINUE_HERE.md")
t = p.read_text(encoding="utf-8")
t = replace_once(t,
"LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18H — published R3.18G second-header real-replay differential audit / Outcome A / 94/94 exact / 0 mismatch",
"LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18I — second-property payload evidence / Outcome A / 94/94 exact / Int=46 String=1 / 0 mismatch / third-property bits 0",
"continue last audit")
t = replace_once(t,
"LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18H — published R3.18G second-header differential / Outcome A / 47 terminators + 47 continuations / Int=46 String=1 / 0 mismatch / second payload + third property 0 + 0",
"LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18I — second-property payload evidence / Outcome A / 47 terminators + 47 continuations / Int=46 String=1 / 0 mismatch / third property 0",
"continue last evidence")
t = replace_once(t,
"CURRENT_PASS:\n  R3.18I — second-property payload contract/evidence audit\n\nCURRENT_PASS_TYPE:\n  read-only evidence / characterize exactly one second-property payload on the frozen R3.18F continuation lane; no production composition and no third-property access",
"CURRENT_PASS:\n  R3.18J — bounded native second-property payload composition\n\nCURRENT_PASS_TYPE:\n  production implementation / compose exactly one optional Int|String second payload after R3.18G; stop at exact payload end; no third-property access",
"continue current pass")
t = replace_once(t,
"  R3.18I is read-only evidence only: on the same frozen lane, characterize exactly one second payload after the admitted second header; 46 Int rows and 1 String row must be handled as separate observed tag classes, with 47 terminators remaining no-payload/no-lookup controls\n  NO production second-property payload composition, third property/control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
"  R3.18I CLOSED Outcome A: 94/94 frozen rows exact; 47 terminators + 47 continuations; second payload Int=46/String=1; native/oracle mismatch 0; third-property bits consumed 0; production unchanged\n  R3.18J ACTIVE: may compose exactly one optional Int|String second payload through exact payload end using existing native decoders\n  NO third property/control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
"continue hard stop")
closure = f'''R3_18I_EVIDENCE_CLOSURE:\n  Outcome A / read-only / production Rust unchanged at {PROD}\n  authority head: {EVIDENCE_HEAD}\n  authority run/job: {EVIDENCE_RUN} / {EVIDENCE_JOB} SUCCESS\n  exact-head normal CI: {NORMAL_RUN} / {NORMAL_JOB} SUCCESS\n  artifact: {ARTIFACT_ID} / 18741 bytes\n  artifact digest: {ARTIFACT_DIGEST}\n  94/94 rows exact / 47 terminator + 47 continuation / Int=46 String=1 / mismatch 0\n  third-property bits consumed: 0\n  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0\n'''
anchor = "R3_18H_EVIDENCE_CLOSURE:\n"
if "R3_18I_EVIDENCE_CLOSURE:" not in t:
    t = replace_once(t, anchor, closure + anchor, "continue closure anchor")
# Repair any explicitly current-like stale one-line pointers.
lines=[]
for line in t.splitlines():
    low=line.lower()
    if "first unfinished" in low and ("r3.18d" in low or "r3.18i" in low):
        line=re.sub(r"R3\.18[DI]", "R3.18J", line)
    lines.append(line)
t="\n".join(lines)+"\n"
p.write_text(t, encoding="utf-8")

# Knowledge graph sync including mandatory order.
p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
t = p.read_text(encoding="utf-8")
t = replace_once(t,
"R3.18H production second-header differential decision                         |\nR3.18I active second-property payload evidence spec                              |",
"R3.18H production second-header differential decision                         |\nR3.18I second-property payload evidence decision / Outcome A CLOSED            |\nR3.18J active bounded second-property payload implementation spec               |",
"kg graph current")
# Insert decision + J spec and renumber mandatory rows >= 51.
needle="50. `docs/continuity/MIMIR_R3_18I_EXECUTION_SPEC.md`\n"
if "`docs/continuity/MIMIR_R3_18I_DECISION.md`" not in t.split("## Current replay-decoder chain",1)[0]:
    before, after = t.split(needle, 1)
    mandatory_tail, rest = after.split("\n## Current replay-decoder chain", 1)
    adjusted=[]
    for line in mandatory_tail.splitlines():
        m=re.match(r"(\d+)\. (.*)", line)
        if m and int(m.group(1)) >= 51:
            line=f"{int(m.group(1))+2}. {m.group(2)}"
        adjusted.append(line)
    inserted = needle + "51. `docs/continuity/MIMIR_R3_18I_DECISION.md`\n52. `docs/continuity/MIMIR_R3_18J_EXECUTION_SPEC.md`\n" + "\n".join(adjusted)
    t = before + inserted + "\n## Current replay-decoder chain" + rest
# Add current closure block before chain if absent.
kg_note=f'''\n### R3.18I payload evidence: OUTCOME A / CLOSED\n- evidence head `{EVIDENCE_HEAD}`; run/job `{EVIDENCE_RUN}/{EVIDENCE_JOB}` SUCCESS\n- same-head normal CI `{NORMAL_RUN}/{NORMAL_JOB}` SUCCESS\n- artifact `{ARTIFACT_ID}` / `{ARTIFACT_DIGEST}`\n- 94/94 exact; terminator=47; continuation=47; Int=46; String=1; mismatch=0; third-property bits=0\n- production unchanged at `{PROD}`\n- next exact pass: R3.18J bounded native second-property payload composition\n'''
if "### R3.18I payload evidence: OUTCOME A / CLOSED" not in t:
    t=t.replace("\n## Current replay-decoder chain", kg_note+"\n## Current replay-decoder chain",1)
lines=[]
for line in t.splitlines():
    low=line.lower()
    if "first unfinished" in low and ("r3.18d" in low or "r3.18i" in low):
        line=re.sub(r"R3\.18[DI]", "R3.18J", line)
    if "current_pass" in low and "r3.18i" in low:
        line=re.sub(r"R3\.18I", "R3.18J", line)
    lines.append(line)
t="\n".join(lines)+"\n"
p.write_text(t, encoding="utf-8")

# Sanity gates.
json.loads(state_path.read_text(encoding="utf-8"))
required = [
    "docs/continuity/MIMIR_R3_18I_DECISION.md",
    "docs/continuity/MIMIR_R3_18J_EXECUTION_SPEC.md",
    "docs/continuity/MIMIR_CONTINUITY_STATE.json",
    "docs/continuity/MIMIR_CURRENT_STATE.md",
    "docs/continuity/MIMIR_PROGRESS_LEDGER.md",
    "docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",
    "MIMIR_CONTINUE_HERE.md",
    "MIMIR_KNOWLEDGE_GRAPH.md",
]
for f in required:
    if not Path(f).exists(): raise SystemExit(f"missing {f}")
print("R3_18I_CONTINUITY_PATCH=PASS")

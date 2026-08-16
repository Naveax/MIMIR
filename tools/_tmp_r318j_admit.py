from pathlib import Path
import json, re

PRE_MAIN = "9fc863114b22b72ec56a606075f7a8e87fa6fd5c"
PROD = "330ab01890a7c09eff1805e437584fb3be0a1134"
PROD_TREE = "5540b6a86e53d243dabbabea223a5afa8657521c"
LIB_BLOB = "ee9b0c71871df7ff52275581eb7ad4c023b8ba79"
TEST_BLOB = "c5a97c5a17ae2ea292790a020673dd26a0150024"
IMPL_RUN = 31975731621
IMPL_JOB = 95234808797
CANDIDATE_RUN = 31975907582
CANDIDATE_JOB = 95235253244
PUBLISHED_RUN = 31976100231
PUBLISHED_JOB = 95235742210
I_HEAD = "45090a2c18fb517088bb411782bbaed0d7d68199"
I_ARTIFACT = 9270842140
I_DIGEST = "sha256:9890ed33780412a8900692a627b212d80428a08229f9f691d914c8def31e06e2"


def replace_once(text, old, new, label):
    n=text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected 1 match, got {n}")
    return text.replace(old,new,1)

Path("docs/continuity/MIMIR_R3_18J_DECISION.md").write_text(f'''# MIMIR R3.18J — Bounded Second-Property Payload Production Decision

**Date:** 2026-08-17
**Outcome:** **A — ADMITTED / PRODUCTION PUBLISHED**
**Production SHA:** `{PROD}`
**Production tree:** `{PROD_TREE}`

## Decision

R3.18J is admitted. Production now composes at most one second-property payload after the already-bounded R3.18G second header. A terminator still returns immediately with no second header/payload. A continuation decodes exactly one second payload and stops at its exact payload end.

The admitted surface is deliberately narrow: `Int` reuses `decode_replay_network_primitive_scalar_v1`; `String` reuses `decode_replay_network_k2_v1` and is additionally restricted by the R3.18J composition to the exact R3.18I-observed context `net_version=10`, `is_rl_223=false`. The following `property_present` bit is not read.

## Exact authority

```text
pre-pass main                       {PRE_MAIN}
production SHA/tree                 {PROD} / {PROD_TREE}
lib.rs blob                         {LIB_BLOB}
focused test blob                   {TEST_BLOB}
implementation run/job              {IMPL_RUN} / {IMPL_JOB} SUCCESS
clean candidate CI                  {CANDIDATE_RUN} / {CANDIDATE_JOB} SUCCESS
published-main CI                   {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
R3.18I evidence head                {I_HEAD}
R3.18I artifact                     {I_ARTIFACT}
R3.18I artifact digest              {I_DIGEST}
```

## Clean scope

Exactly two production files changed from `{PRE_MAIN}`:

1. `crates/mimir-replay/src/lib.rs`
2. `crates/mimir-replay/tests/r3_18j_second_property_payload.rs`

No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file entered the clean production commit.

## Admitted behavior

- terminator: `second_payload=None`, exact R3.18G control end, no post-control lookup/payload decode;
- continuation `Int`: exact 32-bit primitive scalar value/end;
- continuation `String`: exact existing K2 String decoder, additionally gated to net10 / non-RL223;
- result retains the R3.18G header composition plus optional typed second payload and exact stop bit;
- stop equals exactly the one second payload end;
- bits after payload end do not affect the result;
- truncation and malformed/wrong-context String fail closed;
- no third-control access and no property loop.

## Hard stop

R3.18J does not admit the following `property_present` bit, a third header/payload, repeated/generalized property iteration, generic chainable cursor behavior, second tags outside exact `Int|String`, next actor/frame iteration, lifecycle mutation, raw-state/event/replay-slice/skill/runtime/export widening or dependency/corpus/support expansion.

## Next exact pass

`R3.18K — published second-property payload real-replay differential audit` over the immutable R3.18I 94-row lane. Only a clean Outcome A may open evidence for the control bit after the second payload.
''', encoding="utf-8")

Path("docs/continuity/MIMIR_R3_18K_EXECUTION_SPEC.md").write_text(f'''# MIMIR R3.18K — Published Second-Property Payload Real-Replay Differential Audit

**Status:** ACTIVE
**Pass type:** read-only evidence / production differential
**Production authority:** R3.18J `{PROD}`
**Production mutation:** forbidden
**Third property/control bit:** forbidden

## 1. Goal

Differentially validate the published R3.18J bounded second-payload composition over the exact frozen R3.18I lane. Invoke the production R3.18J API, not merely the lower-level scalar/K2 decoders, and prove exact class/value/end behavior without observing the following `property_present` bit.

## 2. Frozen authority

```text
production SHA/tree                 {PROD} / {PROD_TREE}
lib.rs blob                         {LIB_BLOB}
R3.18J focused test blob            {TEST_BLOB}
implementation run/job              {IMPL_RUN} / {IMPL_JOB} SUCCESS
candidate CI                        {CANDIDATE_RUN} / {CANDIDATE_JOB} SUCCESS
published-main CI                   {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
R3.18I evidence head                {I_HEAD}
R3.18I artifact                     {I_ARTIFACT}
R3.18I artifact digest              {I_DIGEST}
frozen rows                         94 = 47 terminators + 47 continuations
continuation payload tags           Int=46 / String=1
R3.18I native/oracle mismatch       0
R3.18I third-property bits          0
```

Before evidence, fetch fresh main, verify production source/test blobs and every receipt above, then reuse the exact R3.18I witnesses without reselection.

## 3. Required differential checks

For each of 47 terminators invoke R3.18J and require no second header/payload, exact control stop and no post-control lookup/decode.

For each of 47 continuations invoke R3.18J and require:

- exact first-property reconstruction;
- exact R3.18G second-header coordinates/tag/payload_start;
- exactly one typed second payload;
- exact tag distribution `Int=46 / String=1`;
- exact payload start/end/width and semantic value against immutable R3.18I evidence/oracle;
- exact returned `stop_bit == payload_end_bit`;
- zero following/third `property_present` bits consumed.

Native/authority mismatch must be zero.

## 4. Negative controls

At minimum: real payload truncation; terminator post-control lookup poison; String wrong-context rejection; tag outside `Int|String`; repeated identical invocation; and bit poison beginning at returned payload end. All must preserve the hard stop and fail closed where applicable.

## 5. Evidence artifact

Emit a privacy-safe immutable artifact with exact production receipts, frozen witness/source identities, per-row result comparison without raw private payload windows, aggregate counts, negative controls, third-bit consumption counter, mutation counters and hashes of every evidence file.

## 6. Required validation

Production focused tests, full `mimir-replay`, workspace check/test/clippy, repository verifier, same-head normal CI, deterministic double run, privacy scan and production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 7. Hard stop

No production Rust/Cargo/fixture/corpus/support mutation. Do not inspect or semantically claim the bit after the second payload. No third property, repeated loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening.

## 8. Outcome gate

### Outcome A
All 94 frozen rows match the published R3.18J API exactly with zero mismatch and zero following-property bits consumed. Admit R3.18K evidence, then define a separate evidence pass for exactly the next `property_present` control bit.

### Outcome B
A reproducible production/authority mismatch appears. Record it and keep the post-second-payload control boundary closed.

### Outcome C
Authority drift, witness reselection, source mutation, privacy failure, following-bit access or validation contradiction. Stop without admission.
''', encoding="utf-8")

state_path=Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
state=json.loads(state_path.read_text(encoding="utf-8"))
state["updated_date"]="2026-08-17"
state["last_production_code_sha"]=PROD
state["last_production_milestone"]="R3.18J"
state["last_production_milestone_name"]="bounded native second-property payload composition"
state["current_pass"]="R3.18K"
state["current_pass_kind"]="read-only evidence / published second-property payload differential"
state["current_pass_goal"]="Differentially validate the published R3.18J optional second-payload API over the exact R3.18I 94-row lane with Int=46/String=1, exact semantic/end parity and zero following-property bits consumed."
state["current_pass_stop_boundary"]="Stop exactly at the R3.18J second payload end. Do not read the following property_present bit; no third property, repeated loop, next actor/frame/lifecycle/raw-state/event/skill/runtime/export widening."
state["r3_18j"]={
 "outcome":"A","kind":"production","production_sha":PROD,"production_tree":PROD_TREE,
 "lib_blob":LIB_BLOB,"focused_test_blob":TEST_BLOB,"implementation_run":IMPL_RUN,"implementation_job":IMPL_JOB,
 "candidate_ci_run":CANDIDATE_RUN,"candidate_ci_job":CANDIDATE_JOB,"published_ci_run":PUBLISHED_RUN,"published_ci_job":PUBLISHED_JOB,
 "second_tags":["Int","String"],"string_context":{"net_version":10,"is_rl_223":False},"third_property_bits_consumed":0
}
for f in ["docs/continuity/MIMIR_R3_18J_DECISION.md","docs/continuity/MIMIR_R3_18K_EXECUTION_SPEC.md"]:
    if f not in state.get("next_files_to_read",[]): state.setdefault("next_files_to_read",[]).append(f)
state_path.write_text(json.dumps(state,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

Path("docs/continuity/MIMIR_CURRENT_STATE.md").write_text(f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-17
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production milestone:** `R3.18J — bounded native second-property payload composition`
**Completed read-only evidence:** `R3.18I — Outcome A / 94/94 / Int=46 String=1 / mismatch 0`
**Current exact pass:** `R3.18K — published second-property payload real-replay differential audit`

## Truthful production boundary

Production now composes at most one optional second payload after the R3.18G second header. Terminators stop at the control end. Continuations admit only Int and String; String is additionally gated to net10/non-RL223. Success stops exactly at the second payload end. The following `property_present` bit remains closed.

```text
production SHA/tree                 {PROD} / {PROD_TREE}
lib/test blobs                      {LIB_BLOB} / {TEST_BLOB}
implementation                     {IMPL_RUN} / {IMPL_JOB} SUCCESS
candidate CI                       {CANDIDATE_RUN} / {CANDIDATE_JOB} SUCCESS
published-main CI                  {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS
```

## Current gate

R3.18K must differentially validate the published R3.18J API on the immutable 94-row R3.18I lane. No production mutation and no observation of the following property control bit is permitted.

## Still closed

```text
following/third property_present control bit
third property header/payload
repeated/generalized property loop
generic repeatedly-chainable property cursor
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction / events / replay slicing
skill / teacher / runtime / export widening
```
''',encoding="utf-8")

Path("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md").write_text(f'''# MIMIR — Next Chat Handoff

- Production authority: `{PROD}` — R3.18J bounded second-property payload.
- J receipts: implementation `{IMPL_RUN}/{IMPL_JOB}`, candidate CI `{CANDIDATE_RUN}/{CANDIDATE_JOB}`, published CI `{PUBLISHED_RUN}/{PUBLISHED_JOB}`, all SUCCESS.
- R3.18I immutable evidence: `{I_HEAD}`, artifact `{I_ARTIFACT}`, `{I_DIGEST}`, 94/94 exact, Int=46/String=1.
- Current pass: `R3.18K` read-only differential of the published J API.
- Hard stop: stop at second payload end; following `property_present` bit and property loop remain closed.
''',encoding="utf-8")

ledger=Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
lt=ledger.read_text(encoding="utf-8")
entry=f'''\n\n## 2026-08-17 — R3.18J published\n\n- Outcome A / production `{PROD}`.\n- Exact two-file clean scope: lib + focused R3.18J test.\n- Implementation `{IMPL_RUN}/{IMPL_JOB}`, candidate CI `{CANDIDATE_RUN}/{CANDIDATE_JOB}`, published CI `{PUBLISHED_RUN}/{PUBLISHED_JOB}` SUCCESS.\n- Exactly one optional second payload is now production; Int plus exact-context String only; following property bit remains closed.\n- Next pass: R3.18K published API differential.\n'''
if "## 2026-08-17 — R3.18J published" not in lt: ledger.write_text(lt.rstrip()+entry,encoding="utf-8")

# Master handbook sync using stable current-block phrases from R3.18I admission.
p=Path("MIMIR_CONTINUE_HERE.md"); t=p.read_text(encoding="utf-8")
t=replace_once(t,"LAST_PRODUCTION_CODE_SHA:\n  2b608aafae97b10ecbc884f99e4bd4a73abf7a5c","LAST_PRODUCTION_CODE_SHA:\n  "+PROD,"master production sha")
t=replace_once(t,"LAST_PRODUCTION_MILESTONE:\n  R3.18G — minimal native existing-actor bounded second-property header composition","LAST_PRODUCTION_MILESTONE:\n  R3.18J — bounded native second-property payload composition","master production milestone")
t=replace_once(t,"CURRENT_PASS:\n  R3.18J — bounded native second-property payload composition\n\nCURRENT_PASS_TYPE:\n  production implementation / compose exactly one optional Int|String second payload after R3.18G; stop at exact payload end; no third-property access","CURRENT_PASS:\n  R3.18K — published second-property payload real-replay differential audit\n\nCURRENT_PASS_TYPE:\n  read-only evidence / validate the published R3.18J API on the frozen R3.18I lane; no following property control access","master current")
# Replace exact J active hard-stop lines introduced by I admission.
t=t.replace("  R3.18J ACTIVE: may compose exactly one optional Int|String second payload through exact payload end using existing native decoders\n  NO third property/control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
            "  R3.18J PRODUCTION at "+PROD+": composes exactly one optional Int|String second payload through exact payload end; String is additionally net10/non-RL223 only\n  R3.18K ACTIVE read-only differential; following property/control bit remains unobserved\n  NO following/third property control/header/payload, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted")
closure=f'''R3_18J_PRODUCTION_CLOSURE:\n  Outcome A / production {PROD} / tree {PROD_TREE}\n  lib/test blobs: {LIB_BLOB} / {TEST_BLOB}\n  implementation: {IMPL_RUN} / {IMPL_JOB} SUCCESS\n  candidate CI: {CANDIDATE_RUN} / {CANDIDATE_JOB} SUCCESS\n  published-main CI: {PUBLISHED_RUN} / {PUBLISHED_JOB} SUCCESS\n  second payload: Int + exact-context String only / following property bits consumed 0\n'''
anchor="R3_18I_EVIDENCE_CLOSURE:\n"
if "R3_18J_PRODUCTION_CLOSURE:" not in t: t=replace_once(t,anchor,closure+anchor,"master closure")
p.write_text(t,encoding="utf-8")

# KG sync.
p=Path("MIMIR_KNOWLEDGE_GRAPH.md"); t=p.read_text(encoding="utf-8")
t=t.replace("R3.18J active bounded second-property payload implementation spec", "R3.18J bounded second-property payload production decision / CLOSED\nR3.18K active published second-payload differential spec")
head=t.split("## Current replay-decoder chain",1)[0]
if "`docs/continuity/MIMIR_R3_18J_DECISION.md`" not in head:
    needle="52. `docs/continuity/MIMIR_R3_18J_EXECUTION_SPEC.md`\n"
    before, after=t.split(needle,1)
    mandatory_tail, rest=after.split("\n## Current replay-decoder chain",1)
    adjusted=[]
    for line in mandatory_tail.splitlines():
        m=re.match(r"(\d+)\. (.*)",line)
        if m and int(m.group(1))>=53: line=f"{int(m.group(1))+2}. {m.group(2)}"
        adjusted.append(line)
    t=before+needle+"53. `docs/continuity/MIMIR_R3_18J_DECISION.md`\n54. `docs/continuity/MIMIR_R3_18K_EXECUTION_SPEC.md`\n"+"\n".join(adjusted)+"\n## Current replay-decoder chain"+rest
note=f'''\n### R3.18J bounded second payload: PRODUCTION / CLOSED\n- production `{PROD}` / tree `{PROD_TREE}`\n- implementation `{IMPL_RUN}/{IMPL_JOB}`, candidate CI `{CANDIDATE_RUN}/{CANDIDATE_JOB}`, published CI `{PUBLISHED_RUN}/{PUBLISHED_JOB}` SUCCESS\n- one optional second payload only; Int + exact-context String; following property bit remains closed\n- next exact pass: R3.18K published API differential\n'''
if "### R3.18J bounded second payload: PRODUCTION / CLOSED" not in t: t=t.replace("\n## Current replay-decoder chain",note+"\n## Current replay-decoder chain",1)
for old in ["CURRENT_PASS: R3.18J","first unfinished canonical pass is R3.18J","first unfinished pass is R3.18J"]:
    t=t.replace(old,old.replace("R3.18J","R3.18K"))
p.write_text(t,encoding="utf-8")

json.loads(state_path.read_text(encoding="utf-8"))
print("R3_18J_CONTINUITY_PATCH=PASS")

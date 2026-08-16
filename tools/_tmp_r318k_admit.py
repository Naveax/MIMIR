#!/usr/bin/env python3
import json
from pathlib import Path

MAIN = "0a9bdab3717aacf320459d738a322ce00415fec7"
PROD = "330ab01890a7c09eff1805e437584fb3be0a1134"
K_HEAD = "926ddd88331ef0372b17b495cb06502010ab39ac"
K_RUN = "31977860600"
K_JOB = "95239932737"
K_CI_RUN = "31977860563"
K_CI_JOB = "95239932564"
K_ARTIFACT = "9271561853"
K_DIGEST = "sha256:a455984c1149cb8f186eedb34d3e148fe45b8592c928cd9246d36cd52843262f"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def rep(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{label}: expected {count} exact matches, got {actual}")
    return text.replace(old, new, count)


def insert_before(text, marker, block, label):
    if block in text:
        raise SystemExit(f"{label}: block already present")
    return rep(text, marker, block + marker, label)


# -----------------------------------------------------------------------------
# MIMIR_CONTINUE_HERE.md
# -----------------------------------------------------------------------------
p = Path("MIMIR_CONTINUE_HERE.md")
s = read(p)
s = rep(
    s,
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18I — second-property payload evidence / Outcome A / 94/94 exact / Int=46 String=1 / 0 mismatch / third-property bits 0",
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18K — published R3.18J second-property payload differential / Outcome A / 94/94 exact / Int=46 String=1 / 0 mismatch / following-property bits 0",
    "continue last read-only",
)
s = rep(
    s,
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18I — second-property payload evidence / Outcome A / 47 terminators + 47 continuations / Int=46 String=1 / 0 mismatch / third property 0",
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18K — published second-property payload differential / Outcome A / 47 terminators + 47 continuations / Int=46 String=1 / 0 mismatch / following property 0",
    "continue last evidence",
)
s = rep(
    s,
    "CURRENT_PASS:\n  R3.18K — published second-property payload real-replay differential audit\n\nCURRENT_PASS_TYPE:\n  read-only evidence / validate the published R3.18J API on the frozen R3.18I lane; no following property control access",
    "CURRENT_PASS:\n  R3.18L — following-property control-bit evidence after one published second payload\n\nCURRENT_PASS_TYPE:\n  read-only evidence / on the exact 47 R3.18K continuation rows, inspect exactly the one property_present bit at the published R3.18J stop and compare it to pinned Boxcars; no following stream/header/payload",
    "continue current pass",
)
s = rep(
    s,
    "  R3.18K ACTIVE read-only differential; following property/control bit remains unobserved\n  NO following/third property control/header/payload, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "  R3.18K CLOSED Outcome A: published R3.18J API matched the frozen 94-row lane exactly; mismatch 0; following-property bits consumed 0\n  R3.18L ACTIVE read-only evidence may inspect exactly one following property_present control bit after a successful R3.18J second payload\n  NO following stream/header/payload, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "continue hard stop",
)
k_closure = f"""R3_18K_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at {PROD}
  authority head: {K_HEAD}
  authority run/job: {K_RUN} / {K_JOB} SUCCESS
  exact-head normal CI: {K_CI_RUN} / {K_CI_JOB} SUCCESS
  artifact: {K_ARTIFACT} / 18744 bytes
  artifact digest: {K_DIGEST}
  94/94 rows exact / 47 terminator + 47 continuation / Int=46 String=1 / mismatch 0
  terminator no-post-control lookup: 47/47; real payload truncation: 47/47
  String wrong-context / tag-outside-Int-String / repeatability / post-payload poison: PASS
  following-property bits consumed: 0; witness reselection: 0; privacy: PASS
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0
"""
s = insert_before(s, "R3_18J_PRODUCTION_CLOSURE:\n", k_closure, "continue K closure")

# Explicitly demote stale current-like historical headings discovered by the required full read.
s = rep(s, "# 13. CURRENT PASS CHECKLIST — R3.14A", "# 13. HISTORICAL PASS CHECKLIST — R3.14A (CLOSED; RETAINED FOR ROADMAP HISTORY)", "continue stale R314A heading")
s = rep(
    s,
    "[>] R3.14A first frame + first actor oracle evidence\n[ ] R3.14B bit-cursor/bounded-int contract\n[ ] R3.14C native bit primitive\n[ ] R3.14D first actor envelope native reader\n[ ] R3.14E differential closure\n[ ] R3.15 NewActor payload\n[ ] R3.16 existing actor/property envelope\n[ ] R3.17 attribute decoder families\n[ ] R3.18 complete property loop",
    "[x] R3.14A first frame + first actor oracle evidence\n[x] R3.14B bit-cursor/bounded-int contract\n[x] R3.14C native bit primitive\n[x] R3.14D first actor envelope native reader\n[x] R3.14E differential closure\n[x] R3.15 NewActor branch through admitted spawn trajectory\n[x] R3.16 existing actor/property envelope header\n[x] R3.17 attribute decoder families K1/K2/K3/K4 through admitted contracts\n[>] R3.18 complete property loop — active R3.18L following-property control evidence",
    "continue dashboard stale block",
)
old_truth = "> **MIMIR currently has an evidence-backed production static network lookup plan at R3.13, proven on 3,990,310 supported-corpus attribute updates, but it still has not admitted native actor-envelope bit consumption; R3.14A evidence is in flight on `agent/r3-14a-first-actor-envelope-evidence`, and the project must proceed through the complete roadmap in this file until replay → raw state → event/slice → skill compiler → counterfactual teacher → training/runtime adapters → Gabriel closed loop → scalable corpus intelligence is fully productionized.**"
new_truth = f"> **MIMIR production is at R3.18J `{PROD}`: one existing-actor K1 first property may compose an optional second `Int|String` payload through its exact end. R3.18K closed Outcome A on the frozen 94-row real-replay lane with zero mismatch and zero following-property-bit consumption. R3.18L is now the first unfinished canonical pass and may inspect exactly one following `property_present` control bit; following stream/header/payload and generalized looping remain closed.**"
s = rep(s, old_truth, new_truth, "continue one-line truth")
s = rep(s, "# CURRENT PASS CHECKLIST — R3.18I", "# HISTORICAL PASS CHECKLIST — R3.18I (CLOSED / OUTCOME A)", "continue stale I checklist")

l_section = f"""

---

# R3.18K OUTCOME A ADMITTED / ACTIVE R3.18L — 2026-08-17

```text
production code SHA = {PROD}
R3.18K evidence head = {K_HEAD}
R3.18K run/job        = {K_RUN} / {K_JOB} SUCCESS
R3.18K same-head CI   = {K_CI_RUN} / {K_CI_JOB} SUCCESS
R3.18K artifact       = {K_ARTIFACT} / {K_DIGEST}
R3.18K outcome        = A / 94 OF 94 PUBLISHED SECOND-PAYLOAD DIFFERENTIAL EXACT
ACTIVE NEXT PASS      = R3.18L — following-property control-bit read-only evidence
```

R3.18K reused the exact immutable R3.18I 94-row lane without witness reselection. The published R3.18J API matched all 47 terminators and all 47 continuations; continuation tags remained `Int=46 / String=1`; semantic/shape/end/stop equality was exact; mismatch count was zero; all 47 real payload truncation controls, all 47 terminator no-lookup controls, String wrong-context, tag-outside-`Int|String`, repeatability and post-payload poison controls passed. No following property bit was consumed and production/Cargo/fixture/corpus/support mutation remained `0/0/0/0/0`.

## CURRENT PASS CHECKLIST — R3.18L

- [ ] Re-fetch fresh `main`; require production Rust still exactly R3.18J `{PROD}` except continuity-only commits.
- [ ] Freeze R3.18K authority receipt and immutable R3.18I/K replay+witness identities; no witness reselection.
- [ ] Use exactly the 47 R3.18K continuation rows that successfully decoded a second payload.
- [ ] Reconstruct the published R3.18J result and require its `stop_bit` to equal the frozen second-payload end before observing anything later.
- [ ] With pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`, observe exactly the next `property_present` bit at that stop for each row.
- [ ] Compare bit start/value/end exactly; record false/true distribution without selecting easier rows.
- [ ] Consume zero following stream/header/payload bits; no repeated loop and no third property composition.
- [ ] Require one-bit truncation failure, post-control poison invariance and deterministic repeatability.
- [ ] Produce privacy-safe immutable evidence with exact source/oracle/corpus identities and per-file SHA256 receipt.
- [ ] Run full `mimir-replay`, workspace check/test/clippy, repository verifier and same-head normal CI.
- [ ] Require production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.
- [ ] Outcome A may open only a separate bounded production composition for this one after-second-payload control bit. No following header/payload or generic property loop.
"""
s = s.rstrip() + l_section + "\n"
write(p, s)

# -----------------------------------------------------------------------------
# MIMIR_KNOWLEDGE_GRAPH.md
# -----------------------------------------------------------------------------
p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
s = read(p)
s = rep(
    s,
    "R3.18K active published second-payload differential spec               |",
    "R3.18K published second-payload differential decision / Outcome A CLOSED\nR3.18L active following-property control-bit evidence spec                  |",
    "KG graph K/L",
)
s = rep(
    s,
    "54. `docs/continuity/MIMIR_R3_18K_EXECUTION_SPEC.md`\n55. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n56. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n57. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n58. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n59. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n60. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n61. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "54. `docs/continuity/MIMIR_R3_18K_EXECUTION_SPEC.md`\n55. `docs/continuity/MIMIR_R3_18K_DECISION.md`\n56. `docs/continuity/MIMIR_R3_18L_EXECUTION_SPEC.md`\n57. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n58. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n59. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n60. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n61. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n62. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n63. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "KG reading order",
)
s = rep(
    s,
    " -> R3.18I second-property payload contract/evidence audit: ACTIVE / READ-ONLY EVIDENCE\n      frozen continuation lane only: characterize exactly 46 Int + 1 String second payload through payload end; 47 terminators remain no-payload controls; no third property/control bit and no loop",
    f" -> R3.18I second-property payload evidence: OUTCOME A / CLOSED\n      94/94 exact / Int=46 String=1 / mismatch 0 / third-property bits 0\n -> R3.18J bounded second-property payload composition: PRODUCTION / CLOSED\n      production {PROD} / one optional Int|String second payload through exact end\n -> R3.18K published R3.18J second-payload differential: OUTCOME A / CLOSED\n      authority {K_HEAD} / {K_RUN}/{K_JOB} SUCCESS / artifact {K_ARTIFACT} / mismatch 0 / following bits 0\n -> R3.18L following-property control-bit evidence: ACTIVE / READ-ONLY\n      exact 47 continuation rows only; one following property_present bit maximum; zero following stream/header/payload bits",
    "KG decoder tail",
)
start = "## Current capability lock\n\n"
end = "\n\nR3.17H closed Outcome A without widening K2:"
if s.count(start) != 1 or s.count(end) != 1:
    raise SystemExit("KG capability lock markers unexpected")
a, rest = s.split(start, 1)
_, b = rest.split(end, 1)
cap = f"Production is R3.18J `{PROD}`. After one valid R3.18B K1 first property, the bounded chain may consume the R3.18D control, resolve the exact R3.18G `Int|String` second header, and decode at most one R3.18I-admitted second payload through its exact end. The String branch remains restricted to `net_version=10` and `is_rl_223=false`. R3.18K closed Outcome A by differentially validating this published API over the frozen 94-row lane with zero mismatch, zero witness reselection and zero following-property-bit consumption. R3.18L may now inspect exactly one `property_present` bit after a successful second payload as read-only evidence. Following stream/header/payload bits, a generalized property loop, next actor/frame iteration and lifecycle mutation remain closed."
s = a + start + cap + end + b
s = rep(
    s,
    "R3.18D is now the first dependency-valid unfinished roadmap step: publish only the production one-bit control observation after one valid R3.18B first K1 property. It must stop after that bit. A second stream/header/payload and repeated property loop remain unadmitted.",
    "Historical note: this paragraph previously named R3.18D as the first unfinished step. R3.18D through R3.18K are now closed according to the newer authority blocks above. The first unfinished canonical step is R3.18L, limited to one following property_present control bit after a successful published R3.18J second payload.",
    "KG stale D tail",
)
k_graph = f"""

## R3.18K published second-payload differential closure

```text
authority head              {K_HEAD}
authority run/job           {K_RUN} / {K_JOB} SUCCESS
exact-head normal CI        {K_CI_RUN} / {K_CI_JOB} SUCCESS
artifact                    {K_ARTIFACT}
artifact digest             {K_DIGEST}
rows                        94/94 exact
terminator / continuation   47 / 47
continuation tags           Int=46 / String=1
terminator no-lookup        47/47
real payload truncation     47/47
wrong context/tag controls  PASS / PASS
repeatability / poison      PASS / PASS
native/oracle mismatch      0
following property bits     0 consumed
witness reselection         0
privacy                     PASS
prod/Cargo/fixture/corpus/
support mutations           0/0/0/0/0
outcome                     A
next                        R3.18L following-property control-bit evidence
```
"""
s = s.rstrip() + k_graph + "\n"
write(p, s)

# -----------------------------------------------------------------------------
# Machine continuity state
# -----------------------------------------------------------------------------
p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
data = json.loads(read(p))
data["updated_date"] = "2026-08-17"
data["last_production_code_sha"] = PROD
data["last_production_milestone"] = "R3.18J"
data["last_production_milestone_name"] = "bounded native existing-actor second-property payload composition"
data["last_completed_read_only_audit"] = "R3.18K"
data["current_pass"] = "R3.18L"
data["current_pass_kind"] = "read-only evidence / following-property control bit after one published second payload"
data["current_pass_goal"] = "On the exact 47 R3.18K continuation rows, reconstruct published R3.18J through its second-payload end and compare exactly one following property_present control bit against pinned Boxcars, consuming no following stream/header/payload bits."
data["current_pass_stop_boundary"] = "After a successful R3.18J second payload, R3.18L may read exactly one following property_present bit and stop one bit later. No following stream/header/payload, repeated loop, next actor/frame/lifecycle/raw-state/event/skill/runtime/export widening."
data["closed_now"] = [
    "following property stream/header/payload after the R3.18J second payload",
    "repeated/generalized production property_present loop",
    "generic repeatedly-chainable public property cursor",
    "second-payload contexts outside exact Int and net10/non-RL223 String",
    "next actor / next frame iteration",
    "actor state table mutation",
    "raw-state extraction",
    "event extraction",
    "replay slicing",
    "skill mining",
    "counterfactual rollout execution from native replay state",
]
data["r3_18k"] = {
    "outcome": "A",
    "production_mutation": False,
    "production_sha": PROD,
    "authority_head": K_HEAD,
    "authority_run": int(K_RUN),
    "authority_job": int(K_JOB),
    "same_head_ci_run": int(K_CI_RUN),
    "same_head_ci_job": int(K_CI_JOB),
    "artifact_id": int(K_ARTIFACT),
    "artifact_size_bytes": 18744,
    "artifact_digest": K_DIGEST,
    "frozen_rows": 94,
    "terminators": 47,
    "continuations": 47,
    "continuation_int": 46,
    "continuation_string": 1,
    "terminator_no_lookup_rows": 47,
    "payload_truncation_rows": 47,
    "native_oracle_mismatch": 0,
    "following_property_bits_consumed": 0,
    "witness_reselection": 0,
    "privacy_pass": True,
    "production_cargo_fixture_corpus_support_mutation": "0/0/0/0/0",
}
nfr = data.get("next_files_to_read")
if isinstance(nfr, list):
    for item in [
        "docs/continuity/MIMIR_R3_18K_DECISION.md",
        "docs/continuity/MIMIR_R3_18L_EXECUTION_SPEC.md",
    ]:
        if item not in nfr:
            nfr.append(item)
write(p, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

# -----------------------------------------------------------------------------
# Current state is intentionally a current snapshot, so rewrite it cleanly.
# -----------------------------------------------------------------------------
current = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-17  
**Repository:** `Naveax/MIMIR`  
**Canonical main before this continuity sync:** `{MAIN}`  
**Canonical production SHA:** `{PROD}`  
**Production milestone:** `R3.18J — bounded native existing-actor second-property payload composition`  
**Completed production differential:** `R3.18K — Outcome A / 94/94 frozen rows exact / 47 terminators + 47 continuations / Int=46 String=1 / mismatch 0 / following bits 0`  
**Current exact pass:** `R3.18L — following-property control-bit evidence after one published second payload`

## 1. Truthful production boundary

R3.18J is the production authority. From one already-valid R3.18B first K1 property, production may compose the R3.18D next-property control, at most one R3.18G `Int|String` second header, and at most one R3.18I-admitted second payload through its exact end. `Int` uses the primitive scalar decoder. `String` remains limited to `net_version=10` and `is_rl_223=false` and reuses the admitted K2 String decoder.

```text
production SHA/tree                 {PROD} / 5540b6a86e53d243dabbabea223a5afa8657521c
lib.rs blob                         ee9b0c71871df7ff52275581eb7ad4c023b8ba79
R3.18J focused test blob            c5a97c5a17ae2ea292790a020673dd26a0150024
implementation run/job              31975731621 / 95234808797 SUCCESS
candidate CI                        31975907582 / 95235253244 SUCCESS
published-main CI                   31976100231 / 95235742210 SUCCESS
following property bits consumed    0
```

Production does not read the following property control bit and has no repeated/general property loop.

## 2. R3.18K closure

R3.18K Outcome A is admitted as read-only evidence over the exact immutable R3.18I 94-row lane. It differentially exercised the **published R3.18J production API**, not the lower-level payload decoders alone.

```text
authority head                      {K_HEAD}
custom evidence run/job             {K_RUN} / {K_JOB} SUCCESS
same-head normal CI                 {K_CI_RUN} / {K_CI_JOB} SUCCESS
artifact                            {K_ARTIFACT} / 18744 bytes
artifact digest                     {K_DIGEST}
rows                                94/94 exact
class split                         47 terminator / 47 continuation
continuation tags                   Int=46 / String=1
terminator no-lookup                47/47
real payload truncation             47/47
native/oracle mismatch              0
following property bits consumed    0
witness reselection                 0
privacy                             PASS
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

String wrong-context, tag-outside-`Int|String`, repeatability and post-payload poison controls all passed. R3.18K did not widen production.

## 3. R3.18L exact next pass

R3.18L is read-only following-control evidence. It uses exactly the 47 R3.18K continuation rows because only those rows have a successfully decoded second payload. For every row it must first reconstruct R3.18J through the frozen second-payload end, then observe exactly one `property_present` bit at that stop and compare start/value/end against pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b`.

It may not read the following stream ID, header or payload. It may not create a repeated property loop. Outcome A can justify only a later bounded production composition for this one after-second-payload control bit.

## 4. Still closed

```text
production following-property control after second payload
following property stream/header/payload
repeated/generalized property loop
generic repeatedly-chainable property cursor
next actor / next frame iteration
actor lifecycle mutation
raw-state extraction / events / replay slicing
skill / teacher / runtime / export widening
dependency or corpus/support expansion
```
"""
write("docs/continuity/MIMIR_CURRENT_STATE.md", current)

# -----------------------------------------------------------------------------
# Decision + next exact spec
# -----------------------------------------------------------------------------
decision = f"""# MIMIR R3.18K — Published Second-Property Payload Differential Decision

**Date:** 2026-08-17  
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**  
**Production mutation:** **NONE**  
**Production authority remains:** `{PROD}`

## Decision

R3.18K is admitted. The published R3.18J bounded second-property payload composition was differentially exercised on the exact immutable R3.18I 94-row lane with no witness reselection. All 47 terminators and all 47 continuations matched their frozen structural and payload boundaries. Continuation tags remained exactly `Int=46 / String=1`; native/oracle mismatch was zero; the following `property_present` bit was never consumed.

All 47 terminator no-post-control-lookup controls and all 47 real payload truncation controls passed. The exact String wrong-context control, a tag-outside-`Int|String` control, deterministic repeatability and post-payload poison invariance also passed. Privacy passed and production/Cargo/fixture/corpus/support mutation was `0/0/0/0/0`.

## Immutable authority

```text
pre-pass canonical main             {MAIN}
production SHA/tree                 {PROD} / 5540b6a86e53d243dabbabea223a5afa8657521c
evidence head                       {K_HEAD}
evidence workflow run/job           {K_RUN} / {K_JOB} SUCCESS
same-head normal CI run/job         {K_CI_RUN} / {K_CI_JOB} SUCCESS
artifact                            {K_ARTIFACT} / 18744 bytes
artifact digest                     {K_DIGEST}
frozen rows                         94/94
terminator / continuation           47 / 47
continuation tags                   Int=46 / String=1
terminator no-lookup                47/47
real payload truncation             47/47
native/oracle mismatch              0
following-property bits consumed    0
witness reselection                 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

### Evidence file SHA-256

```text
64ed5ce376813534cdc196e35421092db62b6d84dc244950aa51872def38151f  r3_18k_source_scope.txt
b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf  r3_18k_replay_identity.tsv
99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7  r3_18k_frozen_witnesses.json
9cf75f074c46a15823556e6f0de32f727d10845382e9631537483dbd952c388e  r3_18k_r318i_authority_sha256.txt
40854122f5c39981514077f66fbf0e51b54d0a07997dc262bb5a6b37fe309f70  r3_18k_authority_summary.json
8ca0503a453550c82fccf500834b79b25cafa6c100fda71b67aa5cb7ee0558ac  r3_18k_comparison.json
f6186113fbbcde35c7670e1415dc967eaa549ffde934625e613893cf04e7b9c9  r3_18k_negative_controls.txt
a746fe172d11d55cd274df105c6a1f65b69b114c0951df0c7c7aa5d0859418bd  r3_18k_aggregate.txt
```

## Hard stop retained

R3.18K does not admit production consumption of the following property control bit. It does not admit a following stream/header/payload, a repeated/general property loop, a generic property cursor, next actor/frame iteration, lifecycle state, raw state, events, replay slices, skills, teacher/runtime/export widening, or dependency/support-lane expansion.

## Next exact pass

`R3.18L — following-property control-bit evidence after one published second payload` may inspect exactly one `property_present` bit at the R3.18J stop on the frozen 47 continuation rows and must stop one bit later.
"""
write("docs/continuity/MIMIR_R3_18K_DECISION.md", decision)

l_spec = f"""# MIMIR R3.18L — Following-Property Control-Bit Evidence After One Published Second Payload

**Status:** ACTIVE  
**Pass type:** read-only evidence / differential boundary characterization  
**Production authority:** R3.18J `{PROD}`  
**Evidence authority:** R3.18K Outcome A  
**Production mutation:** forbidden  
**Following stream/header/payload:** forbidden  
**Repeated/general property loop:** forbidden

## 1. Goal

On the exact 47 R3.18K continuation rows, first reconstruct the published R3.18J composition through the already-proven second-payload end, then observe and differentially validate exactly one following `property_present` control bit. Stop one bit later. This pass does not decode the following stream/header/payload and does not create a loop.

## 2. Frozen authority

```text
canonical main before pass          continuity parent containing this spec
production SHA/tree                 {PROD} / 5540b6a86e53d243dabbabea223a5afa8657521c
production lib blob                 ee9b0c71871df7ff52275581eb7ad4c023b8ba79
R3.18J focused test blob            c5a97c5a17ae2ea292790a020673dd26a0150024
R3.18J implementation               31975731621 / 95234808797 SUCCESS
R3.18J candidate CI                 31975907582 / 95235253244 SUCCESS
R3.18J published CI                 31976100231 / 95235742210 SUCCESS
R3.18K evidence head                {K_HEAD}
R3.18K run/job                      {K_RUN} / {K_JOB} SUCCESS
R3.18K same-head CI                 {K_CI_RUN} / {K_CI_JOB} SUCCESS
R3.18K artifact                     {K_ARTIFACT}
R3.18K artifact digest              {K_DIGEST}
frozen source lane                  exact 47 R3.18K continuation rows
pinned Boxcars                      c70e77df7af81b436cb545d070bb90c82f562d0b
```

Before evidence, fetch fresh `main`, prove production source/test blobs remain exact, verify every receipt above and verify the replay/witness identity hashes. Do not reselect rows based on the value of the following bit.

## 3. Exact source lane

Use exactly the 47 R3.18K continuation rows. Each row already proves:

```text
first property reconstruction exact
second header exact
second payload exact
R3.18J stop == frozen second payload end
second tag distribution Int=46 / String=1
```

A row that no longer reproduces is authority drift and stops the pass. Do not replace it.

## 4. Differential observation

For every frozen row:

1. invoke the published R3.18J API and require its exact frozen result through `stop_bit`;
2. require `stop_bit == R3.18K payload_end_bit`;
3. with observation-only pinned Boxcars instrumentation, identify the next property-loop `property_present` bit at that exact global bit offset;
4. record its exact start, boolean value and end;
5. independently read exactly that one bit with evidence-only cursor logic and require exact value/end equality;
6. stop immediately after the bit.

Report the complete false/true distribution. Neither class may be dropped or preferred.

## 5. Negative controls

At minimum:

- truncate exactly before the following control bit -> explicit failure with no fabricated value;
- poison bits after the one-bit control end -> observed control result unchanged;
- repeat identical invocation -> byte-identical/equal evidence result;
- mutate the prior R3.18J stop/end relationship -> reject evidence row before following-bit observation;
- prove following stream/header/payload consumption counters remain zero.

## 6. Evidence artifact

Produce a privacy-safe immutable artifact containing:

- exact main/production/source/test/spec identities;
- R3.18K authority run/job/artifact/digest and frozen replay/witness hashes;
- pinned Boxcars SHA plus observation-only instrumentation hash;
- all 47 row identities with prior R3.18J stop and following control start/value/end, but no raw private payload windows;
- false/true distribution;
- negative-control results;
- following stream/header/payload consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- SHA-256 for every artifact file.

## 7. Required validation

- 47/47 replay identities exact;
- 47/47 published R3.18J reconstruction exact before observation;
- 47/47 oracle/evidence following-control start/value/end exact;
- deterministic double-run equality;
- R3.18J focused tests PASS;
- full `mimir-replay` PASS;
- workspace check/test/clippy PASS under Rust 1.85;
- full repository verifier PASS;
- same exact evidence head normal CI SUCCESS;
- privacy scan PASS;
- production/Cargo/fixture/corpus/support mutation `0/0/0/0/0`.

## 8. Hard stop

R3.18L may not read or resolve the following stream ID, property object, attribute tag, payload start or payload. It may not read another control bit after the one observed here, create any repeated/generalized loop, iterate the next actor/frame, mutate lifecycle state, materialize raw state/events, slice replays, mine skills, or widen runtime/export behavior.

## 9. Outcome gate

### Outcome A

All 47 frozen continuation rows reproduce R3.18J exactly and the following `property_present` start/value/end matches pinned Boxcars with zero mismatch; negatives, privacy and mutation gates pass. Then define a separate bounded production pass for exactly this one after-second-payload control bit.

### Outcome B

A reproducible boundary mismatch appears. Record the exact privacy-safe row/bit coordinates and keep the following control production boundary closed.

### Outcome C

Authority drift, witness reselection, production mutation, following stream/header/payload access, loop widening, privacy failure or validation contradiction. Stop without admission.
"""
write("docs/continuity/MIMIR_R3_18L_EXECUTION_SPEC.md", l_spec)

# -----------------------------------------------------------------------------
# Progress ledger append only
# -----------------------------------------------------------------------------
p = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
s = read(p)
entry = f"""

## 2026-08-17 — R3.18K published second-payload differential

- Outcome A / read-only evidence closed.
- Production remains `{PROD}` (R3.18J).
- Authority: `{K_HEAD}`; evidence `{K_RUN}/{K_JOB}` SUCCESS; same-head CI `{K_CI_RUN}/{K_CI_JOB}` SUCCESS.
- Artifact `{K_ARTIFACT}` / `{K_DIGEST}`.
- 94/94 exact = 47 terminators + 47 continuations; Int=46 / String=1; mismatch 0.
- 47/47 terminator no-lookup and 47/47 real payload truncation controls PASS; wrong context/tag, repeatability, poison PASS.
- Following-property bits consumed 0; witness reselection 0; privacy PASS; mutation `0/0/0/0/0`.
- Next: R3.18L following-property one-bit read-only evidence.
"""
if "## 2026-08-17 — R3.18K published second-payload differential" in s:
    raise SystemExit("ledger K entry already present")
write(p, s.rstrip() + entry + "\n")

# -----------------------------------------------------------------------------
# Next chat handoff is a current pointer; rewrite it.
# -----------------------------------------------------------------------------
handoff = f"""# MIMIR — Next Chat Handoff

Fresh canonical state after R3.18K admission:

```text
repository                    Naveax/MIMIR
production SHA                {PROD}
production milestone          R3.18J bounded second-property payload composition
last read-only audit          R3.18K Outcome A
R3.18K evidence head          {K_HEAD}
R3.18K run/job                {K_RUN} / {K_JOB} SUCCESS
R3.18K same-head CI           {K_CI_RUN} / {K_CI_JOB} SUCCESS
R3.18K artifact               {K_ARTIFACT}
R3.18K artifact digest        {K_DIGEST}
current pass                  R3.18L
current boundary              exactly one following property_present bit after one successful R3.18J second payload
```

R3.18K matched the published R3.18J API on all 94 frozen rows with zero mismatch and consumed zero following-property bits. Production still stops at the second-payload end.

For R3.18L, use exactly the 47 R3.18K continuation rows. Reconstruct R3.18J first, then compare exactly one following `property_present` bit against pinned Boxcars. Stop one bit later. Do not read the following stream/header/payload and do not create a property loop.

Start by reading `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_CURRENT_STATE.md`, `docs/continuity/MIMIR_R3_18K_DECISION.md` and `docs/continuity/MIMIR_R3_18L_EXECUTION_SPEC.md`, then follow the knowledge-graph mandatory order. Fresh source/tests and exact-SHA evidence outrank prose.
"""
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)

print("R3_18K_CONTINUITY_PATCH=PASS files=8 current_pass=R3.18L stale_current_tails_repaired")

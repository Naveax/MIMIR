#!/usr/bin/env python3
import json
from pathlib import Path

MAIN = "1b39cf1abb8b84100349bfe2540296425ef1baed"
PROD = "330ab01890a7c09eff1805e437584fb3be0a1134"
L_HEAD = "9205ac1616e686589938f952782a32f03d0d1488"
L_RUN = "31978791346"
L_JOB = "95242213413"
L_CI_RUN = "31978791304"
L_CI_JOB = "95242213357"
L_ARTIFACT = "9271817700"
L_DIGEST = "sha256:db5d196b92201a3fdfc6ee01b09510d2b05d772404772bbbffe652cad4bcfc8b"


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

# MIMIR_CONTINUE_HERE.md
p = Path("MIMIR_CONTINUE_HERE.md")
s = read(p)
s = rep(s,
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18K — published R3.18J second-property payload differential / Outcome A / 94/94 exact / Int=46 String=1 / 0 mismatch / following-property bits 0",
    "LAST_COMPLETED_READ_ONLY_AUDIT:\n  R3.18L — following-property control-bit evidence / Outcome A / 47/47 exact / false=0 true=47 / 0 mismatch / following stream+header+payload bits 0",
    "continue last audit")
s = rep(s,
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18K — published second-property payload differential / Outcome A / 47 terminators + 47 continuations / Int=46 String=1 / 0 mismatch / following property 0",
    "LAST_COMPLETED_EVIDENCE_PASS:\n  R3.18L — after-second-payload property_present evidence / Outcome A / 47 continuation rows / false=0 true=47 / 0 mismatch / no following stream/header/payload",
    "continue last evidence")
s = rep(s,
    "CURRENT_PASS:\n  R3.18L — following-property control-bit evidence after one published second payload\n\nCURRENT_PASS_TYPE:\n  read-only evidence / on the exact 47 R3.18K continuation rows, inspect exactly the one property_present bit at the published R3.18J stop and compare it to pinned Boxcars; no following stream/header/payload",
    "CURRENT_PASS:\n  R3.18M — bounded native after-second-payload control-bit composition\n\nCURRENT_PASS_TYPE:\n  production implementation / from one already-valid R3.18J second-payload result, consume exactly one following property_present bit; admit only the R3.18L-observed true context and stop one bit later",
    "continue current pass")
s = rep(s,
    "  R3.18L ACTIVE read-only evidence may inspect exactly one following property_present control bit after a successful R3.18J second payload\n  NO following stream/header/payload, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "  R3.18L CLOSED Outcome A: exact 47 continuation rows matched one following property_present bit; false=0 true=47; mismatch 0; following stream/header/payload bits consumed 0\n  R3.18M ACTIVE production implementation may compose exactly this one after-second-payload control bit, true context only; false is evidence-unobserved and must fail closed\n  NO following stream/header/payload, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",
    "continue hard stop")
l_closure = f"""R3_18L_EVIDENCE_CLOSURE:
  Outcome A / read-only / production Rust unchanged at {PROD}
  authority head: {L_HEAD}
  authority run/job: {L_RUN} / {L_JOB} SUCCESS
  exact-head normal CI: {L_CI_RUN} / {L_CI_JOB} SUCCESS
  artifact: {L_ARTIFACT} / 20906 bytes
  artifact digest: {L_DIGEST}
  frozen rows: 47/47 exact / R3.18J reconstruction 47/47 / native-oracle mismatch 0
  following control distribution: false=0 / true=47
  control truncation / repeatability / post-control poison / prior-stop mismatch negatives: PASS 47/47
  following stream/header/payload bits consumed: 0/0/0; witness reselection: 0; privacy: PASS
  MIMIR validation toolchain: rustc 1.85.0; pinned Boxcars oracle build isolated to stable rustc 1.90.0
  production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0
"""
s = insert_before(s, "R3_18K_EVIDENCE_CLOSURE:\n", l_closure, "continue L closure")
s = rep(s, "## CURRENT PASS CHECKLIST — R3.18L", "## HISTORICAL PASS CHECKLIST — R3.18L (CLOSED / OUTCOME A)", "continue L checklist")
m_append = f"""

---

# R3.18L OUTCOME A ADMITTED / ACTIVE R3.18M — 2026-08-17

```text
production code SHA = {PROD}
R3.18L evidence head = {L_HEAD}
R3.18L run/job        = {L_RUN} / {L_JOB} SUCCESS
R3.18L same-head CI   = {L_CI_RUN} / {L_CI_JOB} SUCCESS
R3.18L artifact       = {L_ARTIFACT} / {L_DIGEST}
R3.18L outcome        = A / 47 OF 47 FOLLOWING CONTROL BITS EXACT / FALSE=0 TRUE=47
ACTIVE NEXT PASS      = R3.18M — bounded native after-second-payload control-bit composition
```

R3.18L reused exactly the 47 R3.18K continuation rows and first reconstructed the published R3.18J result through its frozen second-payload end. Pinned Boxcars and an independent one-bit evidence read agreed on the following `property_present` start/value/end for all 47 rows. Every observed bit was `true`; no false row exists in the frozen authority. Therefore R3.18M may admit only the true after-second-payload control context. A false bit in this context is evidence-unobserved and must fail closed rather than being silently generalized.

## CURRENT PASS CHECKLIST — R3.18M

- [ ] Re-fetch fresh `main`; require R3.18J production source/test blobs unchanged except continuity-only commits.
- [ ] Freeze R3.18L head/run/job/CI/artifact/digest and its 47-row `false=0 / true=47` authority.
- [ ] Implement one deliberately non-generic API tied to an already-valid R3.18J second-payload result.
- [ ] Require the supplied prior result's `stop_bit` to be internally consistent with the second payload end before reading anything later.
- [ ] Read exactly one bit at that stop; require it to be `true`; false must fail closed as `unadmitted-following-control-false` (or equally explicit stable category).
- [ ] Return exact control start/end and stop one bit later on success.
- [ ] Perform zero following stream/header/payload lookup or decoding and expose no generic repeatable property cursor.
- [ ] Add focused tests: true positive, false reject, missing-bit reject, aligned/unaligned starts, prior-stop inconsistency reject, post-control poison invariance, repeatability.
- [ ] Clean production scope: `crates/mimir-replay/src/lib.rs` + one focused `crates/mimir-replay/tests/r3_18m_*.rs`; no Cargo/fixture/corpus/workflow/support changes.
- [ ] Run Rust 1.85 focused tests, full `mimir-replay`, workspace check/test/clippy, full repository verifier and exact candidate CI.
- [ ] Fresh-main ancestry audit and force=false fast-forward publication only after every gate passes.
- [ ] Published exact-main CI/readback must pass before R3.18M is production-closed.
"""
s = s.rstrip() + m_append + "\n"
write(p, s)

# Knowledge graph
p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
s = read(p)
s = rep(s,
    "R3.18K published second-payload differential decision / Outcome A CLOSED\nR3.18L active following-property control-bit evidence spec                  |",
    "R3.18K published second-payload differential decision / Outcome A CLOSED\nR3.18L following-property control-bit evidence decision / Outcome A CLOSED\nR3.18M active bounded after-second-payload control implementation spec       |",
    "KG graph L/M")
s = rep(s,
    "55. `docs/continuity/MIMIR_R3_18K_DECISION.md`\n56. `docs/continuity/MIMIR_R3_18L_EXECUTION_SPEC.md`\n57. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n58. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n59. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n60. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n61. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n62. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n63. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "55. `docs/continuity/MIMIR_R3_18K_DECISION.md`\n56. `docs/continuity/MIMIR_R3_18L_EXECUTION_SPEC.md`\n57. `docs/continuity/MIMIR_R3_18L_DECISION.md`\n58. `docs/continuity/MIMIR_R3_18M_EXECUTION_SPEC.md`\n59. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n60. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n61. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n62. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n63. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n64. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n65. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "KG reading order")
s = rep(s,
    " -> R3.18L following-property control-bit evidence: ACTIVE / READ-ONLY\n      exact 47 continuation rows only; one following property_present bit maximum; zero following stream/header/payload bits",
    f" -> R3.18L following-property control-bit evidence: OUTCOME A / CLOSED\n      authority {L_HEAD} / {L_RUN}/{L_JOB} SUCCESS / false=0 true=47 / mismatch 0 / following stream+header+payload bits 0\n -> R3.18M bounded after-second-payload control composition: ACTIVE / PRODUCTION IMPLEMENTATION\n      exact one-bit true context only; false unobserved and fail-closed; no following header/payload or loop",
    "KG decoder L/M")
old_cap = "Production is R3.18J `330ab01890a7c09eff1805e437584fb3be0a1134`. After one valid R3.18B K1 first property, the bounded chain may consume the R3.18D control, resolve the exact R3.18G `Int|String` second header, and decode at most one R3.18I-admitted second payload through its exact end. The String branch remains restricted to `net_version=10` and `is_rl_223=false`. R3.18K closed Outcome A by differentially validating this published API over the frozen 94-row lane with zero mismatch, zero witness reselection and zero following-property-bit consumption. R3.18L may now inspect exactly one `property_present` bit after a successful second payload as read-only evidence. Following stream/header/payload bits, a generalized property loop, next actor/frame iteration and lifecycle mutation remain closed."
new_cap = f"Production remains R3.18J `{PROD}`. After one valid R3.18B K1 first property, the bounded chain may consume the R3.18D control, resolve the exact R3.18G `Int|String` second header, and decode at most one R3.18I-admitted second payload through its exact end. R3.18K validated that published composition. R3.18L then closed Outcome A on exactly 47 continuation rows: the one following `property_present` bit matched pinned Boxcars on all rows with distribution false=0 / true=47 and zero following stream/header/payload consumption. R3.18M is the first unfinished canonical pass and may productionize only this observed true one-bit context. False remains unadmitted in the after-second-payload context, and following header/payload, generalized looping, next actor/frame iteration and lifecycle mutation remain closed."
s = rep(s, old_cap, new_cap, "KG capability lock")
l_graph = f"""

## R3.18L following-property control evidence closure

```text
authority head              {L_HEAD}
authority run/job           {L_RUN} / {L_JOB} SUCCESS
exact-head normal CI        {L_CI_RUN} / {L_CI_JOB} SUCCESS
artifact                    {L_ARTIFACT}
artifact digest             {L_DIGEST}
rows                        47/47 exact
prior R3.18J reconstruction 47/47
control false / true        0 / 47
native/oracle mismatch      0
control truncation          47/47 PASS
repeatability / poison      47/47 PASS / 47/47 PASS
prior-stop negative         47/47 PASS
following stream/header/
payload bits consumed       0/0/0
witness reselection         0
privacy                     PASS
MIMIR Rust floor            1.85.0
pinned Boxcars build        isolated stable rustc 1.90.0
prod/Cargo/fixture/corpus/
support mutations           0/0/0/0/0
outcome                     A
next                        R3.18M true-only one-bit production composition
```
"""
s = s.rstrip() + l_graph + "\n"
write(p, s)

# Machine state
p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
data = json.loads(read(p))
data["updated_date"] = "2026-08-17"
data["last_completed_read_only_audit"] = "R3.18L"
data["current_pass"] = "R3.18M"
data["current_pass_kind"] = "production implementation / bounded true-only following property control after one published second payload"
data["current_pass_goal"] = "From one already-valid R3.18J second-property payload result, validate its exact stop and consume exactly one following property_present bit. Admit success only for the R3.18L-observed true context; false fails closed. Stop one bit later with zero following stream/header/payload access."
data["current_pass_stop_boundary"] = "Exactly one following property_present bit after a valid R3.18J second payload. Only true is evidence-admitted (47/47); false is unobserved and must reject. No following stream/header/payload, repeated loop, actor/frame/lifecycle/raw-state/event/skill/runtime/export widening."
data["r3_18l"] = {
    "outcome": "A",
    "production_mutation": False,
    "production_sha": PROD,
    "authority_head": L_HEAD,
    "authority_run": int(L_RUN),
    "authority_job": int(L_JOB),
    "same_head_ci_run": int(L_CI_RUN),
    "same_head_ci_job": int(L_CI_JOB),
    "artifact_id": int(L_ARTIFACT),
    "artifact_size_bytes": 20906,
    "artifact_digest": L_DIGEST,
    "frozen_rows": 47,
    "control_false": 0,
    "control_true": 47,
    "r3_18j_reconstruction_exact": 47,
    "native_oracle_mismatch": 0,
    "control_truncation_rows": 47,
    "repeatability_rows": 47,
    "post_control_poison_rows": 47,
    "prior_stop_mismatch_negative_rows": 47,
    "following_stream_bits_consumed": 0,
    "following_header_bits_consumed": 0,
    "following_payload_bits_consumed": 0,
    "witness_reselection": 0,
    "privacy_pass": True,
    "mimir_rust_version": "1.85.0",
    "boxcars_build_rust_version": "1.90.0 stable isolated oracle build",
    "production_cargo_fixture_corpus_support_mutation": "0/0/0/0/0"
}
data["closed_now"] = [
    "false following property control in after-second-payload production context (R3.18L observed false=0)",
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
    "counterfactual rollout execution from native replay state"
]
for item in ["docs/continuity/MIMIR_R3_18L_DECISION.md", "docs/continuity/MIMIR_R3_18M_EXECUTION_SPEC.md"]:
    if item not in data.get("next_files_to_read", []):
        data.setdefault("next_files_to_read", []).append(item)
write(p, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

# Current state snapshot
current = f"""# MIMIR — Current Canonical State

**Continuity date:** 2026-08-17  
**Repository:** `Naveax/MIMIR`  
**Canonical main before this continuity sync:** `{MAIN}`  
**Canonical production SHA:** `{PROD}`  
**Production milestone:** `R3.18J — bounded native existing-actor second-property payload composition`  
**Completed read-only differential/evidence:** `R3.18L — Outcome A / 47/47 exact following property_present / false=0 true=47 / mismatch 0`  
**Current exact pass:** `R3.18M — bounded native after-second-payload control-bit composition`

## 1. Truthful production boundary

Production remains R3.18J. It may decode at most one optional `Int|String` second payload through its exact end. It still does not consume the following `property_present` bit.

```text
production SHA/tree                 {PROD} / 5540b6a86e53d243dabbabea223a5afa8657521c
lib.rs blob                         ee9b0c71871df7ff52275581eb7ad4c023b8ba79
R3.18J focused test blob            c5a97c5a17ae2ea292790a020673dd26a0150024
published-main CI                   31976100231 / 95235742210 SUCCESS
```

## 2. R3.18L closure

R3.18L Outcome A is admitted as read-only evidence. It reused exactly the 47 R3.18K continuation rows and reconstructed published R3.18J through the frozen second-payload end before observing one later bit.

```text
authority head                      {L_HEAD}
evidence run/job                    {L_RUN} / {L_JOB} SUCCESS
same-head normal CI                 {L_CI_RUN} / {L_CI_JOB} SUCCESS
artifact                            {L_ARTIFACT} / 20906 bytes
artifact digest                     {L_DIGEST}
rows                                47/47 exact
following control false / true      0 / 47
R3.18J reconstruction               47/47 exact
native/oracle mismatch              0
control truncation                  47/47 PASS
repeatability / post-control poison 47/47 PASS / 47/47 PASS
prior-stop mismatch negative        47/47 PASS
following stream/header/payload     0 / 0 / 0 bits consumed
witness reselection                 0
privacy                             PASS
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

The pinned Boxcars source remained exact. Its temporary oracle build was isolated to stable rustc 1.90.0 because current transitive oracle dependencies exceed Rust 1.85; MIMIR workspace validation itself ran under rustc 1.85.0. Failed v1/v2 attempts are non-authoritative tooling attempts only: v1 exposed a probe `u32`/production `u8` type mismatch; v2 incorrectly applied the MIMIR MSRV to the external oracle dependency graph. v3 is the sole R3.18L authority.

## 3. R3.18M exact next pass

R3.18M may add one deliberately non-generic production composition after an already-valid R3.18J result. It validates the prior stop, reads exactly one following `property_present` bit and succeeds only when the bit is `true`, because R3.18L observed `true=47 / false=0`. False is not evidence-admitted in this context and must fail closed. Success stops exactly one bit later. No following stream/header/payload may be read.

## 4. Still closed

```text
false after-second-payload control context
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

# Decision
decision = f"""# MIMIR R3.18L — Following-Property Control-Bit Evidence Decision

**Date:** 2026-08-17  
**Outcome:** **A — ADMITTED / READ-ONLY EVIDENCE CLOSED**  
**Production mutation:** **NONE**  
**Production authority remains:** `{PROD}`

## Decision

R3.18L is admitted. Exactly the 47 R3.18K continuation rows were reused with zero witness reselection. Every row first reproduced the published R3.18J second-property payload result through its frozen stop. Pinned Boxcars and an independent one-bit evidence read then agreed exactly on the next `property_present` start, value and end.

The observed distribution is `false=0 / true=47`. Native/oracle mismatch is zero. No following stream, header or payload bit was consumed. Truncation before the bit, post-control poison invariance, repeatability and prior-stop mismatch controls all passed 47/47. Privacy passed and production/Cargo/fixture/corpus/support mutation remained `0/0/0/0/0`.

## Immutable authority

```text
pre-pass canonical main             {MAIN}
production SHA/tree                 {PROD} / 5540b6a86e53d243dabbabea223a5afa8657521c
evidence head                       {L_HEAD}
evidence workflow run/job           {L_RUN} / {L_JOB} SUCCESS
same-head normal CI run/job         {L_CI_RUN} / {L_CI_JOB} SUCCESS
artifact                            {L_ARTIFACT} / 20906 bytes
artifact digest                     {L_DIGEST}
frozen rows                         47/47
R3.18J reconstruction               47/47 exact
control false / true                0 / 47
native/oracle mismatch              0
control truncation                  47/47 PASS
repeatability                       47/47 PASS
post-control poison                 47/47 PASS
prior-stop mismatch negative        47/47 PASS
following stream/header/payload     0/0/0 bits consumed
witness reselection                 0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
```

### Evidence file SHA-256

```text
7cbfc2e36b116ba9aac9f3daee29e7652a723e5ceb96a96e270118151e16fd7b  r3_18l_source_scope.txt
b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf  r3_18l_replay_identity.tsv
99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7  r3_18l_frozen_witnesses.json
0fc4681b94749991a226a07af58709d0074bde3ecf4eae67575512a242f44f99  r3_18l_r318k_authority_sha256.txt
107778cbfc4971ad883c53d4dd8e33d5bd0ebe5a1aadb054b42b83810cb1ca4f  r3_18l_source_summary.json
73afd57f43a2656c5d98f6c97b4c24015283c688a1e343494139ea3ba16d8950  r3_18l_targets.tsv
e607f40bdffe9a9a6df2a3546f33a22811624b6efc5ba073a2b954dd84ecb4cf  r3_18l_boxcars_instrumentation_sha256.txt
f94693fe6ae4babe7fc951013de16fc32c0279e40f1d4957943776d3f3d81381  r3_18l_control_rows.json
f30d66d3b6e5fca1525dc01d1154179cadee58747fdb5bf4dbfdaeb4bd4b59c3  r3_18l_negative_controls.txt
ad1d3b129e34a97f46d0bc3ea879a723e3e46e8d7624e2c9eb8945800b15ee19  r3_18l_aggregate.txt
28f4df430ef84149cdd33a1efc7124fb232d69abd3cb94e6d2196957268985c8  r3_18l_artifact_sha256.txt
```

## Tooling-attempt note

R3.18L v1 and v2 are non-authoritative. v1 stopped on an evidence-probe type mismatch (`u32` versus production `u8` `prop_id_bits`). v2 corrected that but incorrectly forced Rust 1.85 onto the external Boxcars dependency graph; current Boxcars transitive dependencies require a newer compiler. v3 isolates the exact pinned Boxcars source build to stable rustc 1.90.0 while all MIMIR validation remains on rustc 1.85.0. This does not add or change a production dependency.

## Admission boundary

R3.18L proves only the observed true after-second-payload control context. It does **not** prove a false after-second-payload control context because the frozen lane contains no false example. It does not admit the following stream/header/payload or a repeated property loop.

## Next exact pass

`R3.18M — bounded native after-second-payload control-bit composition` may productionize exactly one following control bit from a valid R3.18J result. Success is admitted only when that bit is `true`; false fails closed. The API must stop one bit later and may not resolve or decode anything following it.
"""
write("docs/continuity/MIMIR_R3_18L_DECISION.md", decision)

# M execution spec
m_spec = f"""# MIMIR R3.18M — Bounded Native After-Second-Payload Control-Bit Composition

**Status:** ACTIVE  
**Pass type:** production implementation  
**Evidence authority:** R3.18L Outcome A  
**Production authority before pass:** R3.18J `{PROD}`  
**Observed control context:** `true=47 / false=0`  
**Following stream/header/payload:** forbidden  
**Repeated/general property loop:** forbidden

## 1. Goal

Publish the smallest native composition justified by R3.18L. Starting only from an already-valid R3.18J result that contains one successfully decoded second payload, validate its exact stop boundary, read exactly one following `property_present` bit and stop one bit later. The only admitted success context is `true`, because R3.18L observed 47 true rows and zero false rows.

## 2. Frozen authority

```text
production SHA/tree                 {PROD} / 5540b6a86e53d243dabbabea223a5afa8657521c
production lib blob                 ee9b0c71871df7ff52275581eb7ad4c023b8ba79
R3.18J focused test blob            c5a97c5a17ae2ea292790a020673dd26a0150024
R3.18J implementation               31975731621 / 95234808797 SUCCESS
R3.18J candidate CI                 31975907582 / 95235253244 SUCCESS
R3.18J published CI                 31976100231 / 95235742210 SUCCESS
R3.18L evidence head                {L_HEAD}
R3.18L run/job                      {L_RUN} / {L_JOB} SUCCESS
R3.18L same-head CI                 {L_CI_RUN} / {L_CI_JOB} SUCCESS
R3.18L artifact                     {L_ARTIFACT}
R3.18L artifact digest              {L_DIGEST}
R3.18L rows                         47/47 exact
R3.18L control distribution         false=0 / true=47
R3.18L mismatch                     0
R3.18L following stream/header/payload bits 0/0/0
```

Before mutation, fetch fresh `main`; prove all post-production commits are continuity-only and verify the exact source/test/evidence receipts above.

## 3. Admitted production API shape

Use a deliberately non-generic API tied to an already-valid R3.18J result, conceptually:

```text
input:
  network bytes
  + &ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadV1

precondition:
  prior result contains Some(second_header)
  prior result contains Some(second_payload)
  prior stop_bit == exact second payload end/stop

read:
  control_start = prior.stop_bit
  one LSB-first property_present bit

if bit == true:
  return bounded control result
  property_present = true
  start = control_start
  end = start + 1
  stop_bit = end

if bit == false:
  fail closed as evidence-unadmitted after-second-payload false context
```

The result/API name must encode **after second payload** and **following control** semantics. Do not expose a generic cursor or chainable loop primitive.

## 4. Exact evidence allowlist

R3.18L observed:

```text
true   47
false   0
```

Therefore this composition admits success only for `true`. A false bit must not be treated as a normal terminator yet; no false witness exists for this after-second-payload boundary. A future evidence pass may separately characterize false if real frozen evidence exposes it.

## 5. Fail-closed rules

Reject atomically on:

- missing or internally inconsistent R3.18J second header/payload;
- prior `stop_bit` not equal to the exact second-payload end;
- insufficient bits at the following control position;
- observed false following bit;
- arithmetic/position overflow.

Failure must not perform any following stream lookup/header decode/payload read.

## 6. Required focused tests

At minimum:

```text
true following control -> exact start/end/stop             positive
aligned and unaligned prior stop positions                  positive
post-control poison leaves returned control unchanged       positive
repeat identical invocation                                 exact
false following control                                     reject / unadmitted context
missing control bit                                         reject atomically
prior stop inconsistent with second payload end             reject before bit read
missing second payload / malformed prior composition        reject
scope lock: zero following stream/header/payload calls      exact
scope lock: no while/for property loop in new composition   exact
```

Synthetic byte windows may exercise surgical failure cases, but the next differential audit must return to the immutable R3.18L real lane.

## 7. Clean production scope

Preferred exact scope:

1. `crates/mimir-replay/src/lib.rs`
2. one focused `crates/mimir-replay/tests/r3_18m_*.rs`

No Cargo manifest/lockfile, fixture, corpus, workflow, temporary tool, support lane or continuity file may enter the clean production commit.

## 8. Source-boundary audit

Before publication prove the new composition contains:

- exactly one following-bit read;
- explicit true-only evidence allowlist;
- explicit false rejection;
- zero following stream/header/payload decoder calls;
- no `while` or `for` property loop;
- no generic repeatedly-chainable public cursor.

## 9. Validation and publication

Required before publication:

- Rust 1.85 focused R3.18M tests;
- full `mimir-replay` suite;
- workspace check/test/clippy;
- full repository verifier;
- exact clean-candidate SHA CI;
- fresh-main ancestry audit;
- force=false fast-forward publication;
- exact published-main readback and CI.

## 10. Hard stop

R3.18M does not admit:

- false following-control success/terminator semantics in this after-second-payload context;
- following stream ID/header/payload;
- any additional `property_present` bit;
- repeated/generalized property loop;
- generic chainable property cursor;
- next actor/frame iteration;
- actor lifecycle mutation;
- raw-state/event/replay-slice/skill/runtime/export widening;
- dependency/fixture/corpus/support expansion.

## 11. Outcome gate

### Outcome A

The true-only one-bit composition is published with exact stop semantics, false fail-closed behavior, no adjacent widening and all validation gates pass. Then run a separate real-replay differential of the published R3.18M API on the immutable R3.18L 47-row lane.

### Outcome B

Implementation reveals a bounded contract mismatch. Record it and keep production at R3.18J.

### Outcome C

Any source drift, false-context widening, following header/payload access, loop/generalization, MSRV failure or validation contradiction. Stop without publication.
"""
write("docs/continuity/MIMIR_R3_18M_EXECUTION_SPEC.md", m_spec)

# Progress ledger
p = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
s = read(p)
entry = f"""

## 2026-08-17 — R3.18L following-property control-bit evidence

- Outcome A / read-only evidence closed; production remains `{PROD}`.
- Authority `{L_HEAD}`; evidence `{L_RUN}/{L_JOB}` SUCCESS; same-head CI `{L_CI_RUN}/{L_CI_JOB}` SUCCESS.
- Artifact `{L_ARTIFACT}` / `{L_DIGEST}`.
- 47/47 published R3.18J reconstructions exact before one-bit observation; control distribution false=0 / true=47; mismatch 0.
- Truncation, repeatability, post-control poison and prior-stop mismatch controls PASS 47/47.
- Following stream/header/payload consumption 0/0/0; witness reselection 0; privacy PASS; mutation `0/0/0/0/0`.
- MIMIR validation used Rust 1.85.0; pinned Boxcars oracle build was isolated to stable rustc 1.90.0 due external transitive dependency MSRV.
- Next: R3.18M true-only bounded after-second-payload control-bit production composition.
"""
if "## 2026-08-17 — R3.18L following-property control-bit evidence" in s:
    raise SystemExit("ledger L entry already present")
write(p, s.rstrip() + entry + "\n")

# Handoff
handoff = f"""# MIMIR — Next Chat Handoff

Fresh canonical state after R3.18L admission:

```text
repository                    Naveax/MIMIR
production SHA                {PROD}
production milestone          R3.18J bounded second-property payload composition
last read-only evidence       R3.18L Outcome A
R3.18L evidence head          {L_HEAD}
R3.18L run/job                {L_RUN} / {L_JOB} SUCCESS
R3.18L same-head CI           {L_CI_RUN} / {L_CI_JOB} SUCCESS
R3.18L artifact               {L_ARTIFACT}
R3.18L artifact digest        {L_DIGEST}
R3.18L control distribution   false=0 / true=47
current pass                  R3.18M
current boundary              one true-only following property_present bit after one valid R3.18J second payload
```

R3.18L reconstructed all 47 frozen R3.18K continuation rows through the published R3.18J second-payload end and matched the next one-bit control against pinned Boxcars with zero mismatch. No false row was observed, so R3.18M must reject false rather than treating it as an admitted terminator.

For R3.18M, use only a deliberately bounded API tied to a valid R3.18J result. Validate prior stop, read one bit, allow success only for true, stop one bit later, and perform no following stream/header/payload work. Clean source scope is lib.rs plus one focused test file.

Start with `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, machine/current state, `MIMIR_R3_18L_DECISION.md` and `MIMIR_R3_18M_EXECUTION_SPEC.md`, then follow mandatory reading order. Fresh source/tests and exact-SHA evidence outrank prose.
"""
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", handoff)

print("R3_18L_CONTINUITY_PATCH=PASS files=8 current_pass=R3.18M true_only_context=47 false_unadmitted")

#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(".")

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def sub_once(text, pattern, repl, label, flags=0):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"{label}: expected 1 replacement, got {n}")
    return out

BB_DECISION = """# MIMIR R3.18BB — Published R3.18BA Mixed Following-Control Differential Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / READ-ONLY DIFFERENTIAL CLOSED**
**Canonical production:** unchanged at R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Canonical continuity base:** `2bb5c48b3f627d6fe4f8ae6cb2eb2ea87408342e` / `7958e09ee5756d826307ac8b122fd748f43b8a23`

## Decision

R3.18BB closes Outcome A. Published R3.18BA matches exactly the immutable forty-row R3.18AX one-bit authority. The published BA result preserves the exact R3.18AY prerequisite and matches the frozen control start, boolean value, one-bit end, and final stop on all forty witnesses without reselection.

The frozen mixed distribution remains **false=37 / true=3**. The 37 false rows terminate at the BA stop. The exact three true rows are continuation candidates for a later separate header-evidence pass only. BB decodes no following stream ID, header, payload, or second later control.

## Exact authority

```text
production SHA/tree                    5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
continuity base/tree                   2bb5c48b3f627d6fe4f8ae6cb2eb2ea87408342e / 7958e09ee5756d826307ac8b122fd748f43b8a23
evidence head/tree                     91595db2970ad395ec048ebd9326cfa97b01b38a / 40672cd1b546bca2b73ca252d727aa88ca9faec1
workflow / runner blobs                8ae3f5418433a50ab8e0daf468c5e60015725a59 / 85f13b66d21809efc1e3f1cdd001bfdda6fc6fbe
authority run/job                      33104207616 / 98629573433 SUCCESS
same-head natural CI                   33104207621 / 98629573926 SUCCESS
artifact                               9659874105 / 9295 bytes
artifact SHA-256                       0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e
artifact manifest SHA-256              469e5e09e4299dad9d5c7990a8672b931530de68504b29a083d0dd50535d3894
AX source authority                    465a3f2fc71e5eed6f00c16a04738031bef8d82c / 33068572230/98504703417
AX artifact                            9644869549 / 18070 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
```

The downloaded authoritative ZIP matched GitHub artifact metadata byte-for-byte and its internal manifest recomputed **11/11** payload hashes successfully.

## Frozen result

```text
frozen witnesses                       40/40
published BA exact                     40/40
AY prerequisite exact                  40/40
control false                          37
control true                            3
mismatch                                0
witness reselection                     0
repeatability                          40/40 PASS
post-stop poison                       40/40 PASS
upstream AU false terminators          7/7 excluded
wrong actor                            PASS
unresolved lookup                      PASS
wrong exact context                    PASS
corrupt AY prior                       PASS
carrier truncation                     PASS / fail closed
exact pre-control truncation           inherited R3.18AX PASS 40/40
next stream/header/payload/second      0/0/0/0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                                PASS
```

All forty frozen control starts are non-byte-aligned. Therefore BB preserves R3.18AX as the exact bit-level truncation authority instead of fabricating a partial-byte EOF claim through the production `&[u8]` API.

## Superseded non-authority attempt

The first evidence head `a8ed349204d2a72f404ade717aba58fdbdfde815` / run `33103836525` is **not scientific authority**. Authority freeze and the forty-row differential/focused semantics passed, but the helper omitted the Rust 1.85 `rustfmt` component and failed before full validation. Its only artifact is the explicit non-authority failure receipt `9659612921` / 300 bytes / `sha256:987312289f9d8d73608247b37136ab488547e31ff2ba5e9d9ea866b898c061ab`. It was not rerun; v2 used a fresh sibling SHA with only the toolchain-component correction.

## Hard stop

R3.18BB admits no following header. The 37 false rows remain terminators. The exact three true rows authorize only a separate read-only evidence candidate. No following payload, second later control, generalized/repeated property cursor, next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted.

## Next gate

R3.18BC is read-only one-following-property-header evidence on exactly the three frozen BB/AX true witnesses. It must reconstruct published BA exactly, keep all 37 false rows as no-header terminators, observe exactly one following header on the three true rows through `payload_start`, compare native MIMIR structure with pinned Boxcars, discover rather than pre-assume exact header contexts/tags, and consume zero following-payload or second-control bits.
"""

BC_SPEC = """# MIMIR R3.18BC — One Following-Property-Header Evidence After Published R3.18BA Mixed Control

**Status:** ACTIVE
**Pass type:** read-only boundary evidence
**Production authority:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Differential authority:** R3.18BB `91595db2970ad395ec048ebd9326cfa97b01b38a` / `33104207616/98629573433` / artifact `9659874105` / `sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden

## Goal

Preserve exactly the immutable R3.18BB forty-row mixed-control lane. The **37 false** published-BA rows are terminators and must stop at BA. On only the exact **3 true** rows, observe one following property header through `payload_start`, compare it exactly with pinned Boxcars/native structural authority, classify the complete observed context, and stop.

This pass characterizes one header boundary only. It does not publish a following-header composition and does not decode the following payload.

## Frozen authority

```text
canonical continuity base             2bb5c48b3f627d6fe4f8ae6cb2eb2ea87408342e / 7958e09ee5756d826307ac8b122fd748f43b8a23
production SHA/tree                   5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BB evidence head/tree                 91595db2970ad395ec048ebd9326cfa97b01b38a / 40672cd1b546bca2b73ca252d727aa88ca9faec1
BB authority run/job                  33104207616 / 98629573433 SUCCESS
BB same-head CI                       33104207621 / 98629573926 SUCCESS
BB artifact                           9659874105 / 9295 / sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e
BB manifest file SHA-256              469e5e09e4299dad9d5c7990a8672b931530de68504b29a083d0dd50535d3894
BB frozen rows                        40
BB false / true                       37 / 3
BB mismatch / reselection             0 / 0
BB adjacent consumption               0/0/0/0
AX source artifact                    9644869549 / sha256:32f8b8056791280805da023e18ba73931f7caf4e2cf9e816411d4a0094bf97d9
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

Witness reselection is forbidden. Header tag/context distribution is **not** frozen in advance and must be discovered from these exact three true rows.

## Frozen continuation identities

Exactly these BB/AX true witnesses may enter the header lane:

```text
external_fixtures/sample_002.replay                                      BA stop 11224
external_fixtures/sample_003.replay                                      BA stop 7808
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay BA stop 3160
```

Every other BB witness is a false terminator and must perform zero following-header access.

## Witness classification

For all 40 BB rows:

- reconstruct the exact published R3.18BA result;
- require its control value/start/end/stop to equal BB;
- if false, classify as a terminator and stop;
- if true, require identity membership in the exact three-row continuation set above and allow exactly one header observation.

Required split: terminator rows 37; continuation rows 3; total 40. Any count or identity drift is Outcome B/C until explained.

## Positive header path — exact 3 true rows

For each true row:

1. build the existing production lookup plan;
2. reconstruct the valid published BA boundary;
3. invoke only the existing stateless existing-actor property-header primitive at the exact BA control position required by that primitive;
4. require the observed property-present bit to be true and equal the BA authority;
5. compare stream start/end/value/bound and property-ID width exactly with pinned Boxcars;
6. compare resolved property object and resolved attribute tag exactly;
7. compare complete structural/context identity, retaining version/net-version/RL223 fields actually required by the boundary;
8. compare `payload_start_bit` and header stop exactly;
9. repeat and require deterministic equality;
10. poison beginning at `payload_start` and require the returned header unchanged;
11. stop at `payload_start`.

Do not invoke any payload decoder.

## Terminator path — exact 37 false rows

For every false row, BA control must remain false and exact. No following-header success, stream/property lookup for a later property, payload boundary, or later-control access may be claimed after BA stop. Header/payload/second-control consumption remains zero.

## Evidence outputs

Report:

- all forty frozen BB identities and control reconstruction;
- exact 37 terminator identities;
- exact 3 continuation identities;
- per-true-row native and pinned-Boxcars header coordinates;
- resolved property object and attribute tag;
- stream bound and property-ID width;
- exact replay/version/net-version/RL223 context required to explain resolution;
- multiplicities of complete structural/context tuples;
- unclassified/mismatch counts.

Do not infer a Cartesian allowlist. If one or more exact header contexts appear, a later contract pass must freeze only those evidence-supported complete tuples before production composition.

## Required negative controls

At minimum:

- deterministic truncation inside a true-row following header -> fail closed;
- unresolved stream/property lookup -> reject;
- wrong actor object -> reject;
- wrong exact context where required -> reject;
- corrupt/mismatched BA prior -> reject;
- repeatability -> exact equality 3/3;
- poison beginning at `payload_start` -> header unchanged 3/3;
- false terminator no-header path -> 37/37;
- fabricated continuation identity -> reject;
- source-scope guard -> zero following-payload decoder calls and no repeated/generalized property loop;
- following payload / second later control consumption -> 0/0.

## Required gates

```text
BB witness identities                     40/40 exact
published BA reconstruction               40/40 exact
false terminators                         37/37 exact stop
true continuation rows                    3/3
true-row one-header native success        3/3
native/Boxcars header equality            3/3
resolved property object/tag              3/3 exact
payload_start / header stop               3/3 exact
header tuple classification               3/3
unclassified / mismatch                   0 / 0
witness reselection                       0
following payload bits consumed           0
second later control bits consumed        0
negative controls                         PASS
privacy                                   PASS
production/Cargo/fixture/corpus/support   0/0/0/0/0
same exact evidence-head natural CI       SUCCESS
```

Run focused boundary regressions plus Rust 1.85 fmt/check/test/clippy and the full repository verifier. Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs; reuse an equivalent exact run and never use rerun as polling.

## Hard stop

No following payload decode, no second later property control, no production header composition, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, and no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A

All three exact true-row following headers match through `payload_start`; all 37 false rows remain terminators; complete header/context classification is exact; mismatch/unclassified/reselection are zero; negatives/full validation/privacy pass; production mutation is zero; payload/second-control consumption is 0/0. Then a separate R3.18BD contract-only pass may freeze exactly the observed complete header contexts before any production composition.

### Outcome B

A bounded header/context distinction or evidence gap exists. Record it and keep production following-header composition closed.

### Outcome C

Authority/witness drift, native/oracle mismatch, false-row header access, payload/second-control consumption, production mutation, privacy failure, fabricated continuation membership, or generalized chaining. Stop without widening.
"""

p = "MIMIR_CONTINUE_HERE.md"
t = read(p)
t = sub_once(t, r"(LAST_COMPLETED_READ_ONLY_AUDIT:\n)  [^\n]+\n", r"\1  R3.18BB — published R3.18BA mixed following-control differential Outcome A / exact 40/40 / false=37 true=3 / mismatch 0 / reselection 0 / same-head CI 33104207621 / artifact 9659874105\n", "handbook last audit")
t = sub_once(t, r"(LAST_COMPLETED_EVIDENCE_PASS:\n)  [^\n]+\n", r"\1  R3.18BB — published R3.18BA differential Outcome A / exact 40/40 / false=37 true=3 / mismatch 0 / reselection 0 / same-head CI 33104207621 / artifact 9659874105\n", "handbook last evidence")
t = sub_once(t, r"(CURRENT_PASS:\n)  [^\n]+\n", r"\1  R3.18BC — one following-property-header evidence after published R3.18BA mixed control\n", "handbook current pass")
t = sub_once(t, r"(CURRENT_PASS_TYPE:\n)  [^\n]+\n", r"\1  read-only boundary evidence / preserve BB 40-row split, stop 37 false rows at BA, observe exactly one following header through payload_start on only the exact 3 true rows, and decode no following payload or second control\n", "handbook current type")
write(p, t)

p = "MIMIR_KNOWLEDGE_GRAPH.md"
t = read(p)
t = sub_once(t, r"R3\.18BB published-R3\.18BA mixed following-control differential / ACTIVE[^\n]*\n", "R3.18BB published-R3.18BA mixed following-control differential / Outcome A CLOSED\nR3.18BC one following-property-header evidence after published BA mixed control / ACTIVE\n", "KG graph BB/BC")
old_tail = """143. `docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md`
144. `docs/continuity/MIMIR_R3_18BA_DECISION.md`
145. `docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md`
146. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
147. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
148. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
149. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
150. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
151. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
152. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
new_tail = """143. `docs/continuity/MIMIR_R3_18BA_EXECUTION_SPEC.md`
144. `docs/continuity/MIMIR_R3_18BA_DECISION.md`
145. `docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md`
146. `docs/continuity/MIMIR_R3_18BB_DECISION.md`
147. `docs/continuity/MIMIR_R3_18BC_EXECUTION_SPEC.md`
148. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
149. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
150. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
151. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
152. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
153. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
154. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
if t.count(old_tail) != 1:
    raise SystemExit("KG mandatory tail mismatch")
t = t.replace(old_tail, new_tail)
if "### R3.18BB published BA mixed following-control differential: OUTCOME A / CLOSED" not in t:
    t += """

### R3.18BB published BA mixed following-control differential: OUTCOME A / CLOSED
- evidence `91595db2970ad395ec048ebd9326cfa97b01b38a` / tree `40672cd1b546bca2b73ca252d727aa88ca9faec1`; run/job `33104207616/98629573433` SUCCESS
- same-head natural CI `33104207621/98629573926` SUCCESS
- artifact `9659874105` / 9295 bytes / `sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e`; downloaded ZIP exact; inner manifest 11/11 PASS
- published BA + AY prerequisite exact 40/40; false=37 true=3; mismatch/reselection 0/0
- repeatability/poison/authority negatives PASS; adjacent stream/header/payload/second-control 0/0/0/0; mutation 0/0/0/0/0; privacy PASS
- next exact pass: R3.18BC one following-header evidence on only the exact three true rows

### R3.18BC one following-property-header evidence after published BA mixed control: ACTIVE
- immutable BB forty-row split retained: 37 false terminators / 3 true continuation candidates
- only the exact three true rows may observe one header through `payload_start`
- discover exact header contexts/tags; do not pre-freeze or inherit older context contracts
- following payload, second later control, production composition, generalized loop/cursor and semantic/runtime widening remain closed
"""
write(p, t)

p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
t = read(p)
new_override = """# 0. Current override — R3.18BA production closed / R3.18BB differential closed / R3.18BC active evidence

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BA
- `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a` remains canonical production.
- one exact R3.18AY payload authority is recomputed and validated;
- exactly one following LSB-first `property_present` bit is consumed at AY stop;
- both frozen classes are admitted: false=37 / true=3;
- the boundary stops exactly one bit later;
- all seven upstream AU false terminators remain outside BA.

## CLOSED READ-ONLY DIFFERENTIAL — R3.18BB Outcome A
- evidence `91595db2970ad395ec048ebd9326cfa97b01b38a` / `33104207616/98629573433` SUCCESS;
- same-head CI `33104207621/98629573926` SUCCESS;
- artifact `9659874105` / `sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e`;
- published BA and AY prerequisite exact 40/40;
- false=37 / true=3; mismatch/reselection 0/0;
- adjacent stream/header/payload/second-control 0/0/0/0;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.

## ACTIVE EVIDENCE-ONLY — R3.18BC
- preserve all forty BB witness identities;
- all 37 false rows terminate at BA with zero following-header access;
- only the exact three frozen true rows may observe one following property header;
- compare native structure with pinned Boxcars through `payload_start`;
- discover exact header tags/contexts without older-contract inheritance;
- stop at `payload_start`.

## CLOSED
- header access on any of the 37 BB false terminators;
- following payload consumption during R3.18BC;
- second later property-control bit;
- production following-header composition before evidence + exact-context contract closure;
- repeated/generalized property loop or generic cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

"""
t = sub_once(t, r"# 0\. Current override.*?(?=# 1\. Status vocabulary)", new_override, "boundary override", flags=re.S)
write(p, t)

p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(read(p))
state["updated_date"] = "2026-08-27"
state["last_completed_read_only_audit"] = "R3.18BB"
state["last_completed_evidence_pass"] = "R3.18BB"
state["current_pass"] = "R3.18BC"
state["current_pass_kind"] = "read-only one-following-property-header evidence on exact three R3.18BB true continuation witnesses"
state["current_pass_goal"] = "Preserve the immutable BB 40-row lane; stop 37 false rows at BA and observe exactly one following header through payload_start on only the exact 3 true rows, with native/Boxcars equality and complete context classification."
state["current_pass_stop_boundary"] = "No following payload decode, no second later control, no production header composition, no generalized cursor, and no header access on the 37 false terminators."
state["r3_18bb"] = {"outcome":"A","production_sha_unchanged":"5d2bca711f528ab1bb607104379af503ff175697","continuity_base_sha":"2bb5c48b3f627d6fe4f8ae6cb2eb2ea87408342e","evidence_head":"91595db2970ad395ec048ebd9326cfa97b01b38a","evidence_tree":"40672cd1b546bca2b73ca252d727aa88ca9faec1","authority_run":33104207616,"authority_job":98629573433,"same_head_ci_run":33104207621,"same_head_ci_job":98629573926,"artifact_id":9659874105,"artifact_size":9295,"artifact_sha256":"0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e","artifact_manifest_sha256":"469e5e09e4299dad9d5c7990a8672b931530de68504b29a083d0dd50535d3894","frozen_rows":40,"published_ba_exact":40,"ay_prerequisite_exact":40,"control_false":37,"control_true":3,"mismatch":0,"witness_reselection":0,"adjacent_consumption":{"stream":0,"header":0,"payload":0,"second_control":0},"production_cargo_fixture_corpus_support_mutation":[0,0,0,0,0],"privacy":"PASS"}
arr = state.get("next_files_to_read", [])
bb_exec = "docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md"
bb_dec = "docs/continuity/MIMIR_R3_18BB_DECISION.md"
bc_exec = "docs/continuity/MIMIR_R3_18BC_EXECUTION_SPEC.md"
for x in [bb_dec, bc_exec]:
    if x in arr:
        arr.remove(x)
if bb_exec in arr:
    idx = arr.index(bb_exec) + 1
    arr[idx:idx] = [bb_dec, bc_exec]
else:
    arr.extend([bb_dec, bc_exec])
state["next_files_to_read"] = arr
closed = state.get("closed_now", [])
for item in ["following-header access on any of the 37 R3.18BB false terminator rows","following payload after the R3.18BC one-header evidence boundary","second later property-control bit after R3.18BC","production following-header composition before R3.18BC evidence and a later exact-context contract close"]:
    if item not in closed:
        closed.append(item)
state["closed_now"] = closed
write(p, json.dumps(state, indent=2, ensure_ascii=False) + "\n")

write("docs/continuity/MIMIR_CURRENT_STATE.md", """# MIMIR — Current Canonical State

**Continuity date:** 2026-08-27
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `5d2bca711f528ab1bb607104379af503ff175697`
**Production tree:** `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production milestone:** `R3.18BA — bounded post-AY mixed following-control production`
**Last read-only evidence/audit:** `R3.18BB — Outcome A / published BA exact 40/40 / false=37 true=3 / mismatch 0 / reselection 0 / artifact 9659874105`
**Current exact pass:** `R3.18BC — one following-property-header evidence after published BA mixed control`

## Truthful boundary

R3.18BA remains canonical production. It validates/recomputes one exact R3.18AY Int/32 payload composition, begins at the AY stop, consumes exactly one following LSB-first `property_present` bit, accepts both frozen R3.18AX classes, and stops exactly one bit later.

R3.18BB independently closed Outcome A against the immutable forty-row AX authority:

```text
evidence head/tree                     91595db2970ad395ec048ebd9326cfa97b01b38a / 40672cd1b546bca2b73ca252d727aa88ca9faec1
authority run/job                      33104207616 / 98629573433 SUCCESS
same-head natural CI                   33104207621 / 98629573926 SUCCESS
artifact                               9659874105 / 9295
artifact SHA-256                       0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e
internal manifest                      11/11 PASS
published BA exact                     40/40
AY prerequisite exact                  40/40
false / true                           37 / 3
mismatch / reselection                 0 / 0
adjacent stream/header/payload/second  0/0/0/0
mutation                               0/0/0/0/0
privacy                                PASS
```

The exact pre-control bit truncation claim remains inherited from R3.18AX 40/40 because all forty control starts are non-byte-aligned; BB separately proves byte-slice carrier truncation fails closed.

## Current gate

R3.18BC is evidence-only. Preserve all forty BB identities. The 37 false rows are strict terminators and perform zero following-header access. On only the exact three frozen true rows, observe one following property header through `payload_start`, compare native MIMIR structure with pinned Boxcars, classify complete contexts/tags without pre-assuming them, and stop.

Frozen true identities:

```text
external_fixtures/sample_002.replay                                      BA stop 11224
external_fixtures/sample_003.replay                                      BA stop 7808
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay BA stop 3160
```

## Hard stop

No following payload decode, no second later control, no production following-header composition, no generalized/repeated property cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
""")

write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", """# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BA** at `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`.

R3.18BB is now **Outcome A / CLOSED**. Evidence head `91595db2970ad395ec048ebd9326cfa97b01b38a`, authority `33104207616/98629573433` SUCCESS, same-head CI `33104207621/98629573926` SUCCESS, artifact `9659874105` / 9295 bytes / `sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e`, internal manifest 11/11 PASS. Published BA and AY prerequisite are exact 40/40; false=37 / true=3; mismatch/reselection 0/0; adjacent stream/header/payload/second-control 0/0/0/0; mutation 0/0/0/0/0; privacy PASS.

The first BB helper head `a8ed349204d2a72f404ade717aba58fdbdfde815` / run `33103836525` is non-authority. Its science passed but Rust 1.85 lacked the `rustfmt` component; it was not rerun. v2 corrected only toolchain components on a fresh sibling SHA.

The active pass is **R3.18BC — one following-property-header evidence after published BA mixed control**. Preserve all 40 BB witnesses. Exactly 37 false rows terminate at BA. Only these three true rows may enter the header lane: `external_fixtures/sample_002.replay` (BA stop 11224), `external_fixtures/sample_003.replay` (7808), and `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay` (3160). Observe one header through `payload_start`, compare with pinned Boxcars, discover exact contexts/tags, and decode no following payload or second control.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.
""")

p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
t = read(p)
entry = """
## 2026-08-27 — R3.18BB — Published R3.18BA mixed following-control differential

Production base SHA: `5d2bca711f528ab1bb607104379af503ff175697`
Production commit SHA: unchanged / `5d2bca711f528ab1bb607104379af503ff175697`
Pass type: read-only published-production differential
Outcome: **A — CLOSED**

What changed:
- no production source changed;
- published R3.18BA was checked against exactly the immutable forty R3.18AX one-bit witnesses;
- the frozen mixed split remains false=37 / true=3;
- a separate R3.18BC one-header evidence lane is opened only for the exact three true witnesses.

Evidence:
- evidence head/tree `91595db2970ad395ec048ebd9326cfa97b01b38a` / `40672cd1b546bca2b73ca252d727aa88ca9faec1`;
- authority run/job `33104207616/98629573433` SUCCESS;
- same-head natural CI `33104207621/98629573926` SUCCESS;
- artifact `9659874105` / 9295 bytes / `sha256:0e5bc329e1fc89068243ad0846356ed4dbfc2ade245623385b8e84d21b4f138e`;
- downloaded ZIP exact; inner manifest 11/11 PASS;
- published BA exact 40/40; AY prerequisite exact 40/40; false=37 / true=3; mismatch 0; witness reselection 0;
- repeatability/post-stop poison 40/40; authority/context/lookup negatives PASS;
- carrier truncation fail-closed PASS; exact pre-control truncation inherited from AX PASS 40/40;
- adjacent stream/header/payload/second-control consumption 0/0/0/0;
- production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy PASS.

Important negative facts / anti-regressions:
- `a8ed349204d2a72f404ade717aba58fdbdfde815` / `33103836525` is superseded helper-only non-authority: science/focused semantics passed, but the helper lacked the Rust 1.85 `rustfmt` component before full validation;
- failure receipt `9659612921` explicitly records no scientific authority; the failed SHA was not rerun.

Boundaries opened:
- read-only R3.18BC one-following-property-header evidence on exactly three frozen true witnesses, stopping at `payload_start`.

Boundaries still closed:
- header access on 37 false terminators;
- following payload;
- second later control;
- production following-header composition before an exact-context contract;
- generalized/repeated property cursor;
- next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

Next exact pass:
- `R3.18BC — one following-property-header evidence after published BA mixed control`.

---
"""
if "## 2026-08-27 — R3.18BB — Published R3.18BA mixed following-control differential" not in t:
    if not t.endswith("\n"):
        t += "\n"
    t += entry
write(p, t)

write("docs/continuity/MIMIR_R3_18BB_DECISION.md", BB_DECISION)
write("docs/continuity/MIMIR_R3_18BC_EXECUTION_SPEC.md", BC_SPEC)

print("R3_18BB_CONTINUITY_PATCH=PASS")

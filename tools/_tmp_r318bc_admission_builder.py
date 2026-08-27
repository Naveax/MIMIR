#!/usr/bin/env python3
from pathlib import Path
import json, re

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

BC_DECISION = """# MIMIR R3.18BC — One Following-Property-Header Evidence Decision

**Date:** 2026-08-27
**Outcome:** **A — ADMITTED / READ-ONLY HEADER EVIDENCE CLOSED**
**Canonical production:** unchanged at R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Canonical continuity base:** `2296eb7eb93ac4946bb5b7152f5bc76ff4bf09d8` / `27b40170f2193d972bccf618ee6e2ef7f36806fb`

## Decision

R3.18BC closes Outcome A. The immutable R3.18BB forty-row lane is preserved exactly: all 37 false published-BA controls remain strict terminators, while only the exact three frozen true witnesses enter the following-header lane. Each true witness produces exactly one native property header matching pinned Boxcars through `payload_start`, with zero following-payload or second-later-control consumption.

Three complete eight-field structural contexts were observed. No Cartesian/component/tag-only widening is admitted by this evidence pass. Production remains R3.18BA; a separate R3.18BD contract-only pass must freeze exact context membership before production composition can be considered.

## Exact authority

```text
production SHA/tree                    5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
continuity base/tree                   2296eb7eb93ac4946bb5b7152f5bc76ff4bf09d8 / 27b40170f2193d972bccf618ee6e2ef7f36806fb
evidence head/tree                     0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
workflow blob                          e2c926f05379ff164bb5d3bfdd6f48347817a5af
runner / analyzer / extender blobs     546f3fd6e08d73834c2d405b5d7ec7cae57aaa08 / e2ebd01039af0d14f420ed2048beb158801cf658 / 06c84b5bfc4c4170e1d4268f72a62b09b09ff875
authority run/job                      33122152803 / 98691409657 SUCCESS
same-head natural CI                   33122152793 / 98691409674 SUCCESS
artifact                               9666964713 / 7795 bytes
artifact SHA-256                       88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
artifact manifest SHA-256              d9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf
manifest entries                       14/14 PASS
pinned Boxcars                         c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Frozen result

```text
BB source partition                    40/40
published BA reconstruction            40/40
false terminators                      37/37
true continuation rows                 3/3
one following header                   3/3
unique exact contexts                  3
native/oracle mismatch                 0
witness reselection                    0
repeatability                          PASS 3/3
header truncation                      PASS 3/3
corrupt BA negative                    PASS 3/3
wrong actor negative                   PASS 3/3
unresolved lookup negative             PASS 3/3
wrong context negative                 PASS 3/3
post-payload-start poison              PASS 3/3
false terminator no-header             PASS 37/37
fabricated continuation identity       PASS
following payload bits consumed        0
second later control bits consumed     0
earlier contract inheritance assumed   0
production/Cargo/fixture/corpus/support mutation 0/0/0/0/0
privacy                                PASS
```

## Exact observed contexts

Membership candidates for R3.18BD are exactly these complete tuples, each observed once:

```text
(stream_id_bound=72,  prop_id_bits=6, property_object_index=92, attribute_tag=Boolean, version_major=868, version_minor=32, net_version=10, is_rl_223=false) x1
(stream_id_bound=72,  prop_id_bits=6, property_object_index=94, attribute_tag=Boolean, version_major=868, version_minor=32, net_version=10, is_rl_223=false) x1
(stream_id_bound=110, prop_id_bits=6, property_object_index=58, attribute_tag=Float,   version_major=868, version_minor=32, net_version=10, is_rl_223=false) x1
```

Observed tags are Boolean=2 and Float=1. All three observed properties are ordinal 6. Shared components are descriptive evidence only and do not authorize component-only membership.

## Superseded non-authority seal attempt

Evidence head `a285ee75c8974f18edad1ef271897a63ea51e311` / run `33120199300` is not authority. Its science, same-head CI, manifest generation and artifact upload passed, but the job failed at the final artifact-seal comparison because the REST artifact digest includes the `sha256:` prefix while `actions/upload-artifact@v4` exposes the digest output as bare hex. The failed SHA was not rerun. The authoritative sibling `0f4d07f5...` retained the science helper blobs unchanged and corrected only the seal normalization / v2 branch trigger.

## Hard stop

R3.18BC admits no production following-header composition and no following payload. The 37 false rows remain terminators. No second later control, repeated/generalized property cursor, next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening is admitted.

## Next gate

R3.18BD is contract-only. It may freeze only the three evidence-supported complete eight-field tuples above, each with observed multiplicity one, and must preserve all 37 false terminators outside membership. No production code or payload decode belongs in R3.18BD.
"""

BD_SPEC = """# MIMIR R3.18BD — Exact Following-Header Context Contract After R3.18BC

**Status:** ACTIVE
**Pass type:** contract-only admission
**Evidence authority:** R3.18BC Outcome A
**Production authority:** R3.18BA `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`
**Production mutation:** forbidden
**Following payload decode:** forbidden
**Second later control:** forbidden

## Goal

Turn the immutable R3.18BC three-row true-sublane header observation into the narrowest boundary-specific exact-context contract. The full BB/BC lane remains forty rows: 37 false BA controls are terminators and contribute no header membership; exactly three true rows contribute exactly three observed complete contexts.

R3.18BD does not compose a header in production. It only freezes exact context membership so a later separate production pass can require that membership before composing one header.

## Frozen evidence authority

```text
canonical continuity base             2296eb7eb93ac4946bb5b7152f5bc76ff4bf09d8 / 27b40170f2193d972bccf618ee6e2ef7f36806fb
production SHA/tree                   5d2bca711f528ab1bb607104379af503ff175697 / 6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a
BC evidence head/tree                 0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
BC authority run/job                  33122152803 / 98691409657 SUCCESS
BC same-head natural CI               33122152793 / 98691409674 SUCCESS
BC artifact                           9666964713 / 7795 / sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
BC manifest SHA-256                   d9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf
BC frozen rows                        40
BC false terminators / true headers   37 / 3
BC unique exact contexts              3
BC observed tags                      Boolean=2 / Float=1
BC mismatch / reselection             0 / 0
BC payload / second-control bits      0 / 0
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

Any authority, witness, tuple, multiplicity, or terminator drift stops the pass.

## Required contract artifact

Create `docs/continuity/MIMIR_R3_18BD_ADMITTED_HEADER_CONTEXTS.json` with:

- schema version and a boundary-specific post-BA mixed-continuation contract name;
- membership policy `exact_tuple_only`;
- tuple fields exactly `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)`;
- frozen lane row count 40;
- false terminator count 37;
- observed header row count 3;
- unique exact context count 3;
- exact R3.18BC authority receipts and durable hashes;
- exactly the three observed tuples below and exact observed multiplicity 1 each;
- explicit flags that false terminators produce no header membership;
- explicit anti-widening flags against tag-only, component-only, Cartesian, versionless, RL223-field-dropping, earlier-contract inheritance, and fabricated fourth-tuple membership.

## Exact candidate membership

```text
(72,  6, 92, Boolean, 868, 32, 10, false) x1
(72,  6, 94, Boolean, 868, 32, 10, false) x1
(110, 6, 58, Float,   868, 32, 10, false) x1
```

Membership is complete eight-field equality only. Multiplicity records evidence provenance and is not a runtime frequency guarantee. Boolean-only, Float-only, ordinal-6-only, version-only, bound-only, or any Cartesian recombination is insufficient.

## Required validation and negatives

At minimum prove:

1. exact 3/3 tuple equality against immutable BC header summary;
2. exact multiplicity 1/1/1 and sum 3;
3. exact 37/37 false terminators remain outside header membership;
4. tag-only candidate rejection;
5. component-only candidate rejection;
6. fabricated Cartesian candidate rejection;
7. version-drop candidate rejection;
8. `is_rl_223` field drop and false→true flip rejection;
9. fabricated fourth tuple rejection;
10. an earlier R3.18AT/AJ/Z/P-valid but R3.18BD-absent tuple rejects at this boundary;
11. production/Cargo/fixture/corpus/support mutation remains `0/0/0/0/0`;
12. JSON/schema consistency and knowledge archive verifier PASS.

## Clean scope

Contract/continuity docs only. No Rust production source, tests, Cargo manifest/lockfile, dependency, fixture, corpus, workflow, support lane, payload decoder, or runtime/export widening belongs in the clean R3.18BD contract commit.

## Duplicate-CI rule

Before any dispatch/rerun inspect queued/waiting/in-progress runs for the same SHA/workflow/input. Reuse an equivalent run. Rerun is not polling.

## Hard stop

No production following-header composition, no following payload decode, no second later property control, no synthesized header for a false terminator, no repeated/generalized property loop/cursor, no next actor/frame/lifecycle mutation, raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

## Outcome gate

### Outcome A

Admit exactly the three eight-field contexts with multiplicities summing to 3, preserve 37 false terminators outside membership, and pass all anti-widening/mutation/archive gates. Production remains R3.18BA. A later separate R3.18BE production pass may compose exactly one following header only after a valid published BA true result, require exact R3.18BD membership, and stop at `payload_start`.

### Outcome B

A bounded tuple/multiplicity/terminator discrepancy is isolated. Admit only supported facts and keep production following-header composition closed.

### Outcome C

Authority drift, witness reselection, false-terminator header synthesis, older-contract inheritance, tuple/RL223 widening, payload/later-control access, production mutation, or generalized chaining. Stop without admission.
"""

p = "MIMIR_CONTINUE_HERE.md"
t = read(p)
t = sub_once(t, r"(LAST_COMPLETED_READ_ONLY_AUDIT:\n)  [^\n]+\n", r"\1  R3.18BC — one following-property-header evidence Outcome A / 40-row partition exact / false=37 true=3 / one-header=3/3 / contexts=3 / mismatch 0 / reselection 0 / artifact 9666964713\n", "handbook last audit")
t = sub_once(t, r"(LAST_COMPLETED_EVIDENCE_PASS:\n)  [^\n]+\n", r"\1  R3.18BC — one following-property-header evidence Outcome A / exact 3/3 native-Boxcars headers / contexts=3 / payload=0 / second-control=0 / artifact 9666964713\n", "handbook last evidence")
t = sub_once(t, r"(CURRENT_PASS:\n)  [^\n]+\n", r"\1  R3.18BD — exact following-header context contract after R3.18BC\n", "handbook current pass")
t = sub_once(t, r"(CURRENT_PASS_TYPE:\n)  [^\n]+\n", r"\1  contract-only admission / freeze exactly three BC-supported eight-field header contexts, preserve 37 false terminators outside membership, and mutate no production code\n", "handbook current type")
write(p, t)

p = "MIMIR_KNOWLEDGE_GRAPH.md"
t = read(p)
t = sub_once(t, r"R3\.18BC one following-property-header evidence after published BA mixed control / ACTIVE\n", "R3.18BC one following-property-header evidence after published BA mixed control / Outcome A CLOSED\nR3.18BD exact following-header context contract / ACTIVE\n", "KG BC/BD graph")
old_tail = """145. `docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md`
146. `docs/continuity/MIMIR_R3_18BB_DECISION.md`
147. `docs/continuity/MIMIR_R3_18BC_EXECUTION_SPEC.md`
148. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
149. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
150. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
151. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
152. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
153. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
154. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
new_tail = """145. `docs/continuity/MIMIR_R3_18BB_EXECUTION_SPEC.md`
146. `docs/continuity/MIMIR_R3_18BB_DECISION.md`
147. `docs/continuity/MIMIR_R3_18BC_EXECUTION_SPEC.md`
148. `docs/continuity/MIMIR_R3_18BC_DECISION.md`
149. `docs/continuity/MIMIR_R3_18BD_EXECUTION_SPEC.md`
150. `docs/continuity/MIMIR_PASS_PROTOCOL.md`
151. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`
152. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`
153. `MIMIR_ALL_SOURCES_SUPERBOOK.md`
154. `docs/chatgpt-archive/SOURCE_REGISTRY.md`
155. `docs/chatgpt-archive/VALIDATION_MATRIX.md`
156. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`"""
if t.count(old_tail) != 1:
    raise SystemExit("KG mandatory tail mismatch")
t = t.replace(old_tail, new_tail)
if "### R3.18BC one following-property-header evidence: OUTCOME A / CLOSED" not in t:
    t += """
 
### R3.18BC one following-property-header evidence: OUTCOME A / CLOSED
- evidence `0f4d07f5caf77ec53f5e8b512867ad17b5835ca1` / tree `a198866dc3f18ffbd5cb16e32d39dada5f4116fc`; run/job `33122152803/98691409657` SUCCESS
- same-head natural CI `33122152793/98691409674` SUCCESS
- artifact `9666964713` / 7795 bytes / `sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e`; inner manifest 14/14 PASS
- BB/BA partition exact 40/40; 37 false terminators / 3 true headers; native/Boxcars exact 3/3; unique contexts 3
- mismatch/reselection 0/0; payload/second-control 0/0; mutation 0/0/0/0/0; privacy PASS
- exact observed contexts are `(72,6,92,Boolean,868,32,10,false)`, `(72,6,94,Boolean,868,32,10,false)`, `(110,6,58,Float,868,32,10,false)`, each x1

### R3.18BD exact following-header context contract: ACTIVE
- contract-only; freeze exact eight-field membership from R3.18BC
- 37 false terminators remain outside membership
- no tag/component/Cartesian/older-contract/RL223 widening
- production remains R3.18BA; following payload and second later control remain closed
"""
write(p, t)

p = "docs/continuity/MIMIR_BOUNDARY_LOCKS.md"
t = read(p)
override = """# 0. Current override — R3.18BA production / R3.18BC evidence closed / R3.18BD contract active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BA
- canonical production remains `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`;
- one exact R3.18AY payload authority is recomputed, followed by exactly one LSB-first `property_present` bit;
- false=37 / true=3 and all seven upstream AU false terminators stay outside BA.

## CLOSED EVIDENCE — R3.18BC Outcome A
- authority `0f4d07f5caf77ec53f5e8b512867ad17b5835ca1` / `33122152803/98691409657` SUCCESS;
- same-head CI `33122152793/98691409674` SUCCESS;
- artifact `9666964713` / `sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e`;
- exact 40-row partition; 37 false terminators; exact one header on 3/3 true rows;
- exact contexts: `(72,6,92,Boolean,868,32,10,false)`, `(72,6,94,Boolean,868,32,10,false)`, `(110,6,58,Float,868,32,10,false)`;
- mismatch/reselection 0/0; following payload/second-control 0/0; mutation 0/0/0/0/0; privacy PASS.

## ACTIVE CONTRACT-ONLY — R3.18BD
- admit only exact complete eight-field tuples observed by R3.18BC;
- all 37 false rows remain terminators and cannot acquire header membership;
- exact tuple equality only; multiplicity is provenance, not a runtime frequency promise;
- reject tag-only, component-only, Cartesian, versionless, RL223-drop/flip, older-contract inheritance, and fabricated fourth tuples.

## CLOSED
- production following-header composition before R3.18BD contract closure;
- following payload and second later control;
- header membership for any of the 37 false terminators;
- contexts outside exact R3.18BD evidence-supported set;
- repeated/generalized property loop or generic cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

"""
t = sub_once(t, r"# 0\. Current override.*?(?=# 1\. Status vocabulary)", override, "boundary override", flags=re.S)
write(p, t)

p = "docs/continuity/MIMIR_CONTINUITY_STATE.json"
state = json.loads(read(p))
state["updated_date"] = "2026-08-27"
state["last_completed_read_only_audit"] = "R3.18BC"
state["last_completed_evidence_pass"] = "R3.18BC"
state["current_pass"] = "R3.18BD"
state["current_pass_kind"] = "contract-only exact following-header context admission from R3.18BC"
state["current_pass_goal"] = "Freeze exactly the three R3.18BC evidence-supported complete eight-field header contexts, preserve 37 false terminators outside membership, and admit no production composition or payload decode."
state["current_pass_stop_boundary"] = "No production following-header composition, no following payload, no second later control, no generalized cursor, and no membership outside exact R3.18BC-supported tuples."
state["r3_18bc"] = {"outcome":"A","production_sha_unchanged":"5d2bca711f528ab1bb607104379af503ff175697","continuity_base_sha":"2296eb7eb93ac4946bb5b7152f5bc76ff4bf09d8","evidence_head":"0f4d07f5caf77ec53f5e8b512867ad17b5835ca1","evidence_tree":"a198866dc3f18ffbd5cb16e32d39dada5f4116fc","authority_run":33122152803,"authority_job":98691409657,"same_head_ci_run":33122152793,"same_head_ci_job":98691409674,"artifact_id":9666964713,"artifact_size":7795,"artifact_sha256":"88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e","artifact_manifest_sha256":"d9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf","frozen_rows":40,"false_terminators":37,"true_headers":3,"unique_exact_contexts":3,"observed_tags":{"Boolean":2,"Float":1},"native_oracle_mismatch":0,"witness_reselection":0,"following_payload_bits_consumed":0,"second_later_control_bits_consumed":0,"production_cargo_fixture_corpus_support_mutation":[0,0,0,0,0],"privacy":"PASS"}
arr = state.get("next_files_to_read", [])
bc_exec = "docs/continuity/MIMIR_R3_18BC_EXECUTION_SPEC.md"
bc_dec = "docs/continuity/MIMIR_R3_18BC_DECISION.md"
bd_exec = "docs/continuity/MIMIR_R3_18BD_EXECUTION_SPEC.md"
for x in (bc_dec, bd_exec):
    while x in arr:
        arr.remove(x)
if bc_exec in arr:
    idx = arr.index(bc_exec) + 1
    arr[idx:idx] = [bc_dec, bd_exec]
else:
    arr.extend([bc_dec, bd_exec])
state["next_files_to_read"] = arr
closed = state.get("closed_now", [])
for item in ["following-header contexts outside exact R3.18BD evidence-supported eight-field membership","R3.18AT/R3.18AJ/R3.18Z/R3.18P cross-boundary header-context inheritance at R3.18BD","dropping or flipping is_rl_223 in R3.18BD membership","production following-header composition before R3.18BD contract closure","following payload after the R3.18BC one-header payload_start","second later property-control bit after R3.18BC"]:
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
**Last read-only evidence/audit:** `R3.18BC — Outcome A / one following header exact 3/3 / contexts=3 / artifact 9666964713`
**Current exact pass:** `R3.18BD — exact following-header context contract`

## Truthful boundary

R3.18BA remains canonical production. R3.18BC independently closed the next one-header evidence boundary without changing production.

```text
BC evidence head/tree                  0f4d07f5caf77ec53f5e8b512867ad17b5835ca1 / a198866dc3f18ffbd5cb16e32d39dada5f4116fc
authority run/job                      33122152803 / 98691409657 SUCCESS
same-head natural CI                   33122152793 / 98691409674 SUCCESS
artifact                               9666964713 / 7795
artifact SHA-256                       88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e
inner manifest                         14/14 PASS
source partition                       40/40
false terminators / true headers       37 / 3
native/Boxcars exact                   3/3
unique exact contexts                  3
mismatch / reselection                 0 / 0
payload / second-control bits          0 / 0
mutation                               0/0/0/0/0
privacy                                PASS
```

Exact observed complete contexts, each x1:

```text
(72,  6, 92, Boolean, 868, 32, 10, false)
(72,  6, 94, Boolean, 868, 32, 10, false)
(110, 6, 58, Float,   868, 32, 10, false)
```

Tuple fields are `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version, is_rl_223)`.

## Current gate

R3.18BD is contract-only. Freeze exact eight-field equality for only those three contexts and preserve all 37 false terminators outside membership. Reject component/tag/Cartesian/versionless/RL223/older-contract widening. Production remains R3.18BA.

## Hard stop

No production following-header composition, no following payload, no second later control, no generalized/repeated property cursor, and no next actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
""")

write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", """# MIMIR — Next Chat Handoff

Canonical production remains **R3.18BA** at `5d2bca711f528ab1bb607104379af503ff175697` / `6b5140e228c882efea8b3f5ec0b0f6abf2f49a3a`.

R3.18BC is **Outcome A / CLOSED**. Authority is `0f4d07f5caf77ec53f5e8b512867ad17b5835ca1` / `33122152803/98691409657` SUCCESS, same-head CI `33122152793/98691409674` SUCCESS, artifact `9666964713` / 7795 bytes / `sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e`, inner manifest 14/14 PASS. The immutable partition is 40/40 with 37 false terminators and 3 true headers. Native/Boxcars header equality is 3/3, unique exact contexts=3, mismatch/reselection=0/0, payload/second-control=0/0, mutation=0/0/0/0/0, privacy PASS.

Exact contexts, each observed once:
- `(72,6,92,Boolean,868,32,10,false)`
- `(72,6,94,Boolean,868,32,10,false)`
- `(110,6,58,Float,868,32,10,false)`

The superseded `a285ee75c8974f18edad1ef271897a63ea51e311` / `33120199300` run is non-authority: science passed but final artifact digest representation seal failed. It was not rerun; the authoritative sibling retained all science helper blobs unchanged and normalized only the seal.

The active pass is **R3.18BD — exact following-header context contract**. It is contract-only: freeze complete eight-field exact membership for exactly the three BC contexts, keep all 37 false terminators outside membership, and mutate no production code. Following payload, second later control and production following-header composition remain closed.

Before any dispatch/rerun inspect queued/waiting/in-progress equivalent runs and reuse the existing exact run. Rerun is never polling.
""")

p = "docs/continuity/MIMIR_PROGRESS_LEDGER.md"
t = read(p)
entry = """
## 2026-08-27 — R3.18BC — One following-property-header evidence

Production base SHA: `5d2bca711f528ab1bb607104379af503ff175697`
Production commit SHA: unchanged / `5d2bca711f528ab1bb607104379af503ff175697`
Pass type: read-only boundary evidence
Outcome: **A — CLOSED**

What changed:
- no production source changed;
- all 40 immutable BB rows were reconstructed against published BA;
- 37 false rows remained terminators with zero following-header access;
- exactly three true rows observed exactly one following header through `payload_start`;
- native MIMIR and pinned Boxcars matched 3/3;
- three complete exact contexts were discovered for a later contract-only pass.

Evidence:
- head/tree `0f4d07f5caf77ec53f5e8b512867ad17b5835ca1` / `a198866dc3f18ffbd5cb16e32d39dada5f4116fc`;
- authority `33122152803/98691409657` SUCCESS;
- same-head CI `33122152793/98691409674` SUCCESS;
- artifact `9666964713` / 7795 bytes / `sha256:88e29fbf3fcf089c117aef736b3411e70f1dd6d73c9515d52b28c325cfc5e10e`;
- inner manifest 14/14 PASS, manifest SHA-256 `d9e92e840f1b33b02dec1626dd1337a8bbf1b464656341c1ecb8dd26661ebcaf`;
- partition 40/40; false=37; true-header=3/3; unique contexts=3; mismatch/reselection=0/0;
- all required negatives PASS; payload/second-control bits 0/0; mutation 0/0/0/0/0; privacy PASS.

Exact contexts:
- `(72,6,92,Boolean,868,32,10,false)` x1;
- `(72,6,94,Boolean,868,32,10,false)` x1;
- `(110,6,58,Float,868,32,10,false)` x1.

Superseded non-authority:
- `a285ee75c8974f18edad1ef271897a63ea51e311` / run `33120199300`: science and upload passed, final metadata seal failed because API/upload digest representations differed by `sha256:` prefix; no rerun.

Boundaries opened:
- R3.18BD contract-only exact membership for the three evidence-supported eight-field tuples.

Boundaries still closed:
- production following-header composition before contract closure;
- following payload;
- second later control;
- membership for 37 false terminators;
- component/tag/Cartesian/older-contract/RL223 widening;
- generalized property cursor and semantic/runtime widening.

Next exact pass:
- `R3.18BD — exact following-header context contract`.

---
"""
if "## 2026-08-27 — R3.18BC — One following-property-header evidence" not in t:
    if not t.endswith("\n"):
        t += "\n"
    t += entry
write(p, t)

write("docs/continuity/MIMIR_R3_18BC_DECISION.md", BC_DECISION)
write("docs/continuity/MIMIR_R3_18BD_EXECUTION_SPEC.md", BD_SPEC)

print("R3_18BC_CONTINUITY_PATCH=PASS")

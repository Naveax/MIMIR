#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

BASE="b2d9feaee5d7579c88466431dd52d879cddfb70b"
PROD="fd74ba8c520ab83b808730572c41e45d6dc616e6"
O_HEAD="5046e1594b87ce2828db5faa48aceba456c3166f"
O_RUN=32017369100
O_JOB=95349613184
O_ART=9284144768
O_SIZE=25129
O_DIGEST="e6dc02f087395e2d6b5fb568233484430feba51223848367edd2c6cf15b4b94d"
O_SUMMARY_SHA="a261368f51770efee56e3d8d760390f633b6190bed81446feaf57b076189ae01"
O_HEADER_SHA="503bae96ac51ff27532fc80b5e537b3cb7ccd58cea1584a9a1f975da8a4748a9"
O_AGG_SHA="02324f5a0caa68257a0af93999245124242569f8d582ab2aba2f8119fe6cd676"
EXPECTED=[
(60,5,12,"Boolean",868,32,10,1),(60,5,13,"Boolean",868,32,10,2),(60,5,14,"ActiveActor",868,32,10,3),
(60,5,17,"Boolean",868,32,10,3),(60,5,18,"Boolean",868,32,10,3),(60,5,19,"Boolean",868,32,10,7),
(60,5,21,"Boolean",868,32,10,1),(60,5,22,"Boolean",868,32,10,2),(60,5,23,"Boolean",868,32,10,8),
(60,5,27,"ActiveActor",868,32,10,3),(60,5,30,"ActiveActor",868,32,10,2),(60,5,42,"Boolean",868,32,10,1),
(60,5,43,"Boolean",868,32,10,1),(60,5,44,"Boolean",868,32,10,3),(60,5,54,"Boolean",868,32,10,3),
(67,6,37,"Boolean",868,32,10,1),(72,6,15,"Boolean",868,32,10,2),(110,6,44,"Boolean",868,32,10,1)]

def req(c,m):
    if not c: raise SystemExit(m)
def write(p,s): p.write_text(s.rstrip()+"\n",encoding="utf-8",newline="\n")
def repl(s,a,b,label):
    req(s.count(a)==1,f"{label}: {s.count(a)} matches")
    return s.replace(a,b,1)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    req(len(sys.argv)==3,"usage ROOT O_SUMMARY")
    root=Path(sys.argv[1]); src=Path(sys.argv[2])
    req(sha(src)==O_SUMMARY_SHA,"R3.18O summary SHA drift")
    d=json.loads(src.read_text(encoding="utf-8"))
    req(d["rows"]==47 and d["witness_reselection"]==0,"O summary row/reselection drift")
    req(d["distinct_exact_header_context_tuples"]==18,"O unique tuple drift")
    got=[]
    for x in d["exact_header_context_tuple_counts"]:
        got.append((x["stream_id_bound"],x["prop_id_bits"],x["property_object_index"],x["attribute_tag"],x["version_major"],x["version_minor"],x["net_version"],x["count"]))
    req(sorted(got,key=repr)==sorted(EXPECTED,key=repr),"O tuple set/multiplicity drift")
    req(sum(x[-1] for x in got)==47,"O multiplicity sum drift")

    contexts=[{"stream_id_bound":a,"prop_id_bits":b,"property_object_index":c,"attribute_tag":t,"version_major":ma,"version_minor":mi,"net_version":nv,"observed_count":n} for a,b,c,t,ma,mi,nv,n in EXPECTED]
    contract={
      "schema_version":1,"contract":"MIMIR_R3_18P_FOLLOWING_PROPERTY_HEADER_CONTEXTS","status":"admitted",
      "admission_date":"2026-08-17","membership_policy":"exact_tuple_only",
      "tuple_fields":["stream_id_bound","prop_id_bits","property_object_index","attribute_tag","version_major","version_minor","net_version"],
      "observed_row_count":47,"unique_exact_context_count":18,
      "authority":{"base_main_sha":BASE,"production_sha":PROD,"r3_18o_evidence_head":O_HEAD,"r3_18o_run":O_RUN,"r3_18o_job":O_JOB,"r3_18o_artifact_id":O_ART,"r3_18o_artifact_size":O_SIZE,"r3_18o_artifact_sha256":O_DIGEST,"r3_18o_source_summary_sha256":O_SUMMARY_SHA,"r3_18o_header_rows_sha256":O_HEADER_SHA,"r3_18o_aggregate_sha256":O_AGG_SHA,"witness_reselection":0},
      "admitted_contexts":contexts,
      "anti_widening":{"tag_only_membership":False,"component_only_membership":False,"cartesian_product_membership":False,"versionless_membership":False,"multiplicity_is_runtime_frequency_promise":False,"contexts_outside_exact_set_admitted":False}
    }
    cp=root/"docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json"
    write(cp,json.dumps(contract,indent=2,ensure_ascii=False))
    csha=sha(cp)

    decision=f'''# MIMIR R3.18P Decision — Following-Property Header Context Contract

Date: 2026-08-17  
Outcome: **A — ADMITTED / CONTRACT-ONLY**

## Authority

- base main: `{BASE}`
- production remains: `{PROD}` (R3.18M)
- R3.18O evidence: `{O_HEAD}` / `{O_RUN}/{O_JOB}` SUCCESS
- immutable artifact: `{O_ART}` / `{O_SIZE}` bytes / `sha256:{O_DIGEST}`
- source summary: `sha256:{O_SUMMARY_SHA}`
- following-header rows: `sha256:{O_HEADER_SHA}`
- aggregate: `sha256:{O_AGG_SHA}`
- witness reselection: `0`

## Contract

Committed artifact: `docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json`  
SHA-256: `{csha}`

The contract contains exactly **18** unique structural tuples and their exact **47-row** observed multiplicities. All tuples retain full `(stream_id_bound, prop_id_bits, property_object_index, attribute_tag, version_major, version_minor, net_version)` identity. All 47 rows remain `868.32 / net10`.

Admission is **exact tuple membership only**. `Boolean` or `ActiveActor` by tag alone, any individual bound/width/object component, any Cartesian product, any versionless tuple, and any nineteenth tuple remain outside the contract.

## Validation

- immutable O source summary hash exact: PASS
- exact tuple equality: 18/18
- exact multiplicities: 18/18; sum 47
- tag-only negative: PASS
- component-only negative: PASS
- fabricated Cartesian tuple negative: PASS
- version-drop negative: PASS
- nineteenth-tuple negative: PASS
- production/Cargo/fixture/corpus/support mutation: 0/0/0/0/0

## Admission boundary

R3.18P changes no production Rust capability. It only crystallizes the evidence-supported structural domain for one following existing-actor property header. Following payload, another control bit, generalized/repeated property loops, next actor/frame and semantic/runtime layers remain closed.

## Next exact pass

**R3.18Q — bounded following-property header production composition.** It may compose only one header after a valid R3.18M true control, must require exact R3.18P tuple membership, and must stop exactly at `payload_start`.
'''
    write(root/"docs/continuity/MIMIR_R3_18P_DECISION.md",decision)
    qspec=f'''# MIMIR R3.18Q Execution Spec — Bounded Following-Property Header Production Composition

Date: 2026-08-17  
Pass type: **production / bounded composition**

## Goal

Compose exactly one following existing-actor property header after a valid R3.18M true control, using the already-published stateless header primitive and the exact R3.18P admitted structural-context contract.

## Frozen authority

- production base: `{PROD}` (R3.18M)
- R3.18P contract SHA-256: `{csha}`
- admitted domain: exactly 18 full structural tuples / 47 observed rows
- R3.18O evidence hard stop: following `payload_start`

## Allowed production behavior

1. accept only a previously valid R3.18J second-payload result;
2. reuse the published R3.18M following-control composition and require its admitted true result;
3. decode exactly one following header starting at that control stop;
4. require exact R3.18P tuple membership including version context;
5. stop exactly at the header `payload_start`;
6. preserve atomic fail-closed behavior on any boundary/context error.

## Forbidden widening

- no tag-only/component-only/Cartesian-product support;
- no following payload decode;
- no another `property_present` control bit;
- no generic/repeatable property cursor or property loop;
- no next actor/frame/lifecycle state;
- no raw-state/event/slice/skill/runtime/export widening;
- no Boxcars production dependency.

## Required validation

- focused unit tests for all 18 admitted tuple identities plus outside-contract failures;
- exact frozen 47-row native reconstruction through `payload_start`;
- truncation before header completion fails closed;
- wrong actor context and fabricated tuple fail closed;
- post-`payload_start` poison cannot affect header result;
- existing R3.18M behavior remains unchanged;
- full fmt/test/check/clippy/repository verification on exact clean candidate SHA;
- production/Cargo/fixture/corpus/support scope audit.

## Outcome rule

- **A:** bounded one-header composition is admitted and published; next pass is a published API differential before any payload widening.
- **B:** any scope/context/boundary/regression gate fails; publish nothing.
'''
    write(root/"docs/continuity/MIMIR_R3_18Q_EXECUTION_SPEC.md",qspec)

    # structured continuity
    sp=root/"docs/continuity/MIMIR_CONTINUITY_STATE.json"; st=json.loads(sp.read_text(encoding="utf-8"))
    req(st["current_pass"]=="R3.18P" and st["last_production_code_sha"]==PROD,"continuity base drift")
    st["last_completed_contract_pass"]="R3.18P"
    st["current_pass"]="R3.18Q"; st["current_pass_kind"]="bounded production following-property header composition"
    st["current_pass_goal"]="Compose exactly one following header after a valid R3.18M true control, require exact R3.18P tuple membership, and stop at payload_start."
    st["current_pass_stop_boundary"]="Exactly one following header through payload_start; no payload, another control, generalized loop, actor/frame or semantic/runtime widening."
    st["r3_18p"]={"outcome":"A — admitted / contract-only","production_source_changed":False,"production_sha":PROD,"base_main_sha":BASE,"contract_file":"docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json","contract_sha256":csha,"observed_rows":47,"unique_exact_contexts":18,"membership_policy":"exact_tuple_only","witness_reselection":0,"next_pass":"R3.18Q"}
    files=st["next_files_to_read"]; pexec="docs/continuity/MIMIR_R3_18P_EXECUTION_SPEC.md"; additions=["docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json","docs/continuity/MIMIR_R3_18P_DECISION.md","docs/continuity/MIMIR_R3_18Q_EXECUTION_SPEC.md"]
    files=[x for x in files if x not in additions]; i=files.index(pexec)+1; files[i:i]=additions; st["next_files_to_read"]=files
    write(sp,json.dumps(st,indent=2,ensure_ascii=False))

    write(root/"docs/continuity/MIMIR_CURRENT_STATE.md",f'''# MIMIR Current State

Updated: 2026-08-17

## Canonical truth

- repository: `Naveax/MIMIR`
- production code SHA: `{PROD}`
- last production milestone: **R3.18M**
- last completed evidence pass: **R3.18O / Outcome A**
- last completed contract pass: **R3.18P / Outcome A**
- active canonical pass: **R3.18Q — bounded following-property header production composition**
- frozen replay lane: **47 replays / 47 rows**

## R3.18P admitted contract

- exact structural contexts: **18**
- observed multiplicities sum: **47**
- membership: exact full tuple only
- contract SHA-256: `{csha}`
- production source changed: **no**

## Active boundary

R3.18Q may compose one following header only after a valid R3.18M true control and only when the decoded full structural tuple belongs to R3.18P. It must stop at `payload_start`. Following payload, another control, repeated/generalized loops, next actor/frame and all semantic/runtime layers remain closed.
''')
    write(root/"docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",f'''# MIMIR Next Chat Handoff — R3.18Q

Fresh-read `main`. Production remains `{PROD}` at R3.18M. R3.18P is admitted Outcome A contract-only; contract SHA-256 `{csha}`.

First unfinished canonical pass: **R3.18Q bounded following-property header production composition**.

Read the mandatory knowledge-graph order, then `docs/continuity/MIMIR_R3_18Q_EXECUTION_SPEC.md`. Compose exactly one header after a valid R3.18M true control, require exact R3.18P tuple membership, stop at `payload_start`, and keep payload/another-control/loop widening closed.
''')

    lp=root/"docs/continuity/MIMIR_PROGRESS_LEDGER.md"; ls=lp.read_text(encoding="utf-8").rstrip()+f'''\n\n## 2026-08-17 — R3.18P — Following-property header exact-context contract

Production SHA: `{PROD}` (unchanged)  
Pass type: contract-only  
Outcome: **A — ADMITTED**

- immutable R3.18O authority reverified;
- exact 18 full structural tuples admitted with exact multiplicities summing to 47;
- committed contract SHA-256 `{csha}`;
- tag/component-only, Cartesian-product, version-drop and nineteenth-tuple widening remain rejected;
- no production/Cargo/fixture/corpus/support mutation.

Next exact pass: **R3.18Q bounded following-property header production composition**; hard stop remains following `payload_start`.\n'''
    write(lp,ls)

    # KG
    kp=root/"MIMIR_KNOWLEDGE_GRAPH.md"; ks=kp.read_text(encoding="utf-8")
    ks=repl(ks,"R3.18P active following-property exact-context contract spec                               |","R3.18P following-property exact-context contract decision / Outcome A CLOSED              |\nR3.18Q active bounded following-property header production spec                              |","kg graph")
    old='''### R3.18P following-property header context contract: ACTIVE
- contract-only; production remains `fd74ba8c520ab83b808730572c41e45d6dc616e6`
- exact R3.18O 18-tuple identity + 47 multiplicities only
- no tag/component-only support, no Cartesian product, no payload/control/loop widening
'''
    new=f'''### R3.18P following-property header context contract: OUTCOME A / CLOSED
- production unchanged at `{PROD}`
- exact 18 full structural tuples / multiplicities sum 47
- contract `sha256:{csha}`; membership exact-tuple-only
- tag/component-only, Cartesian-product and versionless widening rejected

### R3.18Q bounded following-property header composition: ACTIVE
- production pass; base production remains `{PROD}` until admitted
- one header only after valid R3.18M true control; exact R3.18P membership required
- stop at payload_start; payload/another-control/loop widening closed
'''
    ks=repl(ks,old,new,"kg status")
    # rebuild mandatory order with inserts after P spec
    a=ks.index("## Mandatory reading order"); b=ks.index("\n### R3.18I payload evidence",a); sec=ks[a:b]; paths=[]
    for line in sec.splitlines():
        z=line.strip()
        if z and z[0].isdigit() and '`' in z: paths.append(z.split('`',2)[1])
    for x in additions: 
        if x in paths: paths.remove(x)
    i=paths.index(pexec)+1; paths[i:i]=additions
    rebuilt="## Mandatory reading order\n\n"+"\n".join(f"{i}. `{x}`" for i,x in enumerate(paths,1))+"\n"
    ks=ks[:a]+rebuilt+ks[b:]; write(kp,ks)

    # master handbook top and final checklist
    hp=root/"MIMIR_CONTINUE_HERE.md"; hs=hp.read_text(encoding="utf-8")
    hs=repl(hs,"LAST_COMPLETED_CONTRACT_PASS:\n  R3.17N — evidence-supported K4 gameplay-structured contract / Outcome A / 161 exact groups / zero cross-product widening","LAST_COMPLETED_CONTRACT_PASS:\n  R3.18P — following-property header exact-context contract / Outcome A / 18 exact tuples / 47 multiplicities / zero cross-product widening","continue contract")
    hs=repl(hs,"CURRENT_PASS:\n  R3.18P — following-property header exact-context contract","CURRENT_PASS:\n  R3.18Q — bounded following-property header production composition","continue pass")
    hs=repl(hs,"CURRENT_PASS_TYPE:\n  contract-only / crystallize exactly the 18 R3.18O structural context tuples and their 47-row multiplicities; production Rust frozen; no cross-product widening","CURRENT_PASS_TYPE:\n  production / compose exactly one following header after a valid R3.18M true control; exact R3.18P tuple membership; stop at payload_start","continue type")
    hs=repl(hs,"  R3.18P ACTIVE contract-only: exact 18-tuple identity + 47 multiplicities only; production unchanged\n  NO following-header production composition, following payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted",f"  R3.18P CLOSED Outcome A: exact 18-tuple contract admitted; multiplicities sum 47; contract sha256 {csha}; production unchanged\n  R3.18Q ACTIVE production pass: one following header only after valid R3.18M true control; exact R3.18P membership; stop at payload_start\n  NO following payload, another control bit, repeated/generalized property loop, next actor/frame/lifecycle/raw-state/event/replay-slice/skill/runtime/export widening is admitted","continue hard stop")
    marker="R3_18O_EVIDENCE_CLOSURE:"; idx=hs.index(marker); close=f'''R3_18P_CONTRACT_CLOSURE:\n  Outcome A / contract-only / production unchanged at {PROD}\n  exact structural contexts: 18 / observed multiplicities: 47 / witness reselection: 0\n  contract artifact: docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json\n  contract sha256: {csha}\n  membership: exact full tuple only / no tag-only, component-only, Cartesian-product or versionless widening\n  next pass: R3.18Q bounded following-property header production composition\n'''; hs=hs[:idx]+close+hs[idx:]
    final=hs.rfind("# CURRENT PASS CHECKLIST — R3.18P"); req(final>=0,"P checklist missing")
    tail=f'''# R3.18P OUTCOME A ADMITTED / ACTIVE R3.18Q — 2026-08-17

```text
production code SHA = {PROD}
R3.18P contract SHA  = {csha}
R3.18P outcome       = A / 18 EXACT CONTEXTS / 47 OBSERVED MULTIPLICITIES
ACTIVE NEXT PASS     = R3.18Q — bounded following-property header production composition
```

## CURRENT PASS CHECKLIST — R3.18Q

- [ ] Fresh-read main and require production source still exactly `{PROD}`.
- [ ] Freeze and verify `MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json` SHA-256 `{csha}`.
- [ ] Inspect the published R3.18M control API and stateless existing-actor header primitive; compose rather than duplicate parsing logic.
- [ ] Accept only one valid R3.18M true-control continuation and decode exactly one following header.
- [ ] Require exact R3.18P full-tuple membership including version context; fail closed outside it.
- [ ] Stop exactly at following `payload_start`; following payload and another-control consumption must remain zero.
- [ ] Add focused contract/boundary/truncation/wrong-context/poison tests and exact 47-row differential validation.
- [ ] No generic/repeatable property cursor or loop; no next actor/frame or semantic/runtime widening.
- [ ] Run fmt/test/check/clippy/repository verification and exact-clean-SHA CI before publication.
- [ ] Publish only by fresh-main ancestry audit + force=false, then run published-main validation/readback.
'''
    hs=hs[:final]+tail; write(hp,hs)

    # boundary current override only
    bp=root/"docs/continuity/MIMIR_BOUNDARY_LOCKS.md"; bs=bp.read_text(encoding="utf-8")
    start=bs.index("# 0. Current override — R3.18O admitted / R3.18P active"); end=bs.index("\n---\n\n# 1. Status vocabulary",start)
    over=f'''# 0. Current override — R3.18P admitted / R3.18Q active

This current override supersedes older status wording later in this historical lock file.

## OPEN / PRODUCTION
- production remains R3.18M at `{PROD}`; exactly one true following control bit is production-admitted.

## ADMITTED CONTRACT — R3.18P
- exact 18 full following-header structural tuples; observed multiplicities sum 47;
- contract `sha256:{csha}`;
- exact tuple membership only; no component-wise or Cartesian-product widening.

## ACTIVE PRODUCTION GATE — R3.18Q
- may compose exactly one following header after valid R3.18M true control;
- exact R3.18P membership required; stop at `payload_start`.

## CLOSED
- following payload; another control bit; repeated/generalized property loop; generic cursor;
- next actor/frame/lifecycle; raw state, events, slices, skills, runtime and exports.
'''
    bs=bs[:start]+over+bs[end:]; write(bp,bs)

    print(f"R3_18P_ADMISSION_PATCH=PASS contract_sha256={csha}")
if __name__=="__main__": main()

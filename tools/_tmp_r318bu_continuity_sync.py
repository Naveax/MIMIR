from pathlib import Path
import json, re

R=Path(".")
DATE="2026-09-14"
BU="43c5d6248e2ea606b2eb0fd95f5c50758c372356"
TREE="d1b7b40ed4e361d9c047e0494fb821688ef7d7b4"
PARENT="9a86252e02d383ebc2ff9665e678f4c2319f47d9"
LIB="1c4db09cff43e0ab56f5efb5e8078da3a1189937"
TEST="e6170f90b47e3f04bd798edbc61f2fa59e5213dd"
SPEC="ac1ce2120320bd552e5be24e2309fea23d5a2a50"
BUILD_RUN=34823631010
BUILD_JOB=103910607381
PR_RUN=34826521464
PR_JOB=103919838545
MAIN_RUN=34827065398
MAIN_JOB=103921549254
BR_HEAD="ff1daab35e2e75bf7446a98a07a1db67e5196dbd"
BR_ART=10267123608
BR_DIG="bf9a7c52296cea0f4d8fe6a4f64d26e8c232ea26bd0589be49ba6afa589c28d1"
BT_ART=10336951993
BT_DIG="fef0df77821475ac3ee5acb417b500aa40708a573d286d30c5c42bcf23ef473d"

def rd(p): return (R/p).read_text(encoding="utf-8")
def wr(p,s):
    q=R/p; q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(s,encoding="utf-8",newline="\n")
def one(s,a,b,label):
    if s.count(a)!=1: raise SystemExit(f"{label}: {s.count(a)}")
    return s.replace(a,b,1)

p=rd("MIMIR_CONTINUE_HERE.md")
p=one(p,"LAST_PRODUCTION_CODE_SHA:\n  5ab14575d0a698d752db35db76f3dbb300cdec8d",f"LAST_PRODUCTION_CODE_SHA:\n  {BU}","prod sha")
p=one(p,"LAST_PRODUCTION_MILESTONE:\n  R3.18BS — bounded post-BO one-following-payload production","LAST_PRODUCTION_MILESTONE:\n  R3.18BU — bounded post-BS next property-control production","prod milestone")
p=one(p,"CURRENT_PASS:\n  R3.18BU — bounded post-BS next property-control production","CURRENT_PASS:\n  R3.18BV — published-R3.18BU one-control differential","current")
p=one(p,"CURRENT_PASS_TYPE:\n  bounded production implementation / exact BT-admitted rows=2 / consume exactly one BR-observed control bit / stop immediately after that bit","CURRENT_PASS_TYPE:\n  read-only published-production differential / exact BU control rows=2 / BR identity comparison / adjacent consumption forbidden","kind")
marker="# CURRENT OVERRIDE — 2026-09-14 — R3.18BU CLOSED / R3.18BV ACTIVE"
if marker in p: raise SystemExit("master override duplicate")
p=p.rstrip()+f"""\n\n\n{marker}\n\n- canonical production: R3.18BU `{BU}` / `{TREE}` / parent `{PARENT}`.\n- exact production blobs: lib `{LIB}`; BU test `{TEST}`; execution spec `{SPEC}`.\n- builder `{BUILD_RUN}/{BUILD_JOB}` SUCCESS; validation PR #219 CLOSED UNMERGED; exact-head CI `{PR_RUN}/{PR_JOB}` SUCCESS; published-main CI `{MAIN_RUN}/{MAIN_JOB}` SUCCESS.\n- exact lane: Boolean control `[11239,11240)` = false; ActiveActor control `[3238,3239)` = true; BP false terminator excluded.\n- BV is read-only: exact BU-vs-BR value/start/end/stop/prerequisite identity, repeatability and post-stop poison only. Following stream/header/payload, second control, witness reselection, production mutation and generic cursor remain closed.\n"""
wr("MIMIR_CONTINUE_HERE.md",p)

k=rd("MIMIR_KNOWLEDGE_GRAPH.md")
k=one(k,"R3.18BU bounded post-BS next property-control production / ACTIVE\n","R3.18BU bounded post-BS next property-control production / CLOSED\nR3.18BV published-R3.18BU one-control differential / ACTIVE\n","kg chain")
k=one(k,"191. `docs/continuity/MIMIR_R3_18BU_EXECUTION_SPEC.md`\n","191. `docs/continuity/MIMIR_R3_18BU_EXECUTION_SPEC.md`\n192. `docs/continuity/MIMIR_R3_18BU_DECISION.md`\n193. `docs/continuity/MIMIR_R3_18BV_EXECUTION_SPEC.md`\n","kg order")
if "### R3.18BU bounded post-BS next property-control production: CLOSED / PUBLISHED" in k: raise SystemExit("kg duplicate")
k=k.rstrip()+f"""\n\n\n### R3.18BU bounded post-BS next property-control production: CLOSED / PUBLISHED\n- `{BU}` / `{TREE}`; exact blobs `{LIB}` / `{TEST}`.\n- builder `{BUILD_RUN}/{BUILD_JOB}`, exact-head CI `{PR_RUN}/{PR_JOB}`, published-main CI `{MAIN_RUN}/{MAIN_JOB}` all SUCCESS; PR #219 closed unmerged.\n- Boolean false `[11239,11240)` + ActiveActor true `[3238,3239)` only; one bit consumed; adjacent consumption 0.\n\n### R3.18BV published-R3.18BU one-control differential: ACTIVE\n- read-only exact two-row differential against immutable BR authority.\n- require exact published BS prerequisite, BU value/bounds/stop, repeatability and post-stop poison.\n- no following structure, second control, reselection, production mutation or generalized cursor.\n"""
wr("MIMIR_KNOWLEDGE_GRAPH.md",k)

b=rd("docs/continuity/MIMIR_BOUNDARY_LOCKS.md")
new=f"""# 0. Current override — R3.18BU production closed / R3.18BV differential active\n\n## PRODUCTION — R3.18BU\n- `{BU}` / `{TREE}` is canonical production.\n- only two exact authority rows: Boolean false `[11239,11240)` and ActiveActor true `[3238,3239)`.\n- builder `{BUILD_RUN}/{BUILD_JOB}`, exact-head CI `{PR_RUN}/{PR_JOB}`, published-main CI `{MAIN_RUN}/{MAIN_JOB}` SUCCESS.\n\n## ACTIVE READ-ONLY — R3.18BV\n- validate published BU against immutable BR on exactly those two rows; production mutation/reselection forbidden.\n\n## CLOSED\n- BP-false control access; success outside exact authority; following stream/header/payload; second later control; generalized/repeated cursor; wider runtime semantics.\n\n# 1. Status vocabulary"""
b,n=re.subn(r"(?s)# 0\. Current override — .*?\n# 1\. Status vocabulary",new,b,count=1)
if n!=1: raise SystemExit(f"boundary replace {n}")
wr("docs/continuity/MIMIR_BOUNDARY_LOCKS.md",b)

wr("docs/continuity/MIMIR_CURRENT_STATE.md",f"""# MIMIR — Current Canonical State\n\n**Continuity date:** {DATE}\n**Repository:** `Naveax/MIMIR`\n**Canonical production SHA:** `{BU}`\n**Production tree:** `{TREE}`\n**Production milestone:** `R3.18BU — bounded post-BS next property-control production`\n**Last read-only evidence/audit:** `R3.18BT — Outcome A / artifact {BT_ART}`\n**Current exact pass:** `R3.18BV — published-R3.18BU one-control differential`\n\n## Truthful boundary\n\nBU is published production. Builder `{BUILD_RUN}/{BUILD_JOB}`, validation PR #219 exact-head CI `{PR_RUN}/{PR_JOB}` and published-main CI `{MAIN_RUN}/{MAIN_JOB}` are SUCCESS. Exact lane is Boolean=false `[11239,11240)` and ActiveActor=true `[3238,3239)` after exact BS.\n\nBV is read-only and must prove exact BU/BR identity, repeatability, prerequisite identity and post-stop poison stability on those two rows.\n\n## Hard stop\n\nNo BP-false access, following stream/header/payload, second later control, reselection, generalized cursor or production mutation.\n""")

wr("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md",f"""# MIMIR — Next Chat Handoff\n\nCanonical production is **R3.18BU** `{BU}` / `{TREE}`. Builder `{BUILD_RUN}/{BUILD_JOB}`, exact-head CI `{PR_RUN}/{PR_JOB}` and published-main CI `{MAIN_RUN}/{MAIN_JOB}` are SUCCESS; PR #219 is closed unmerged.\n\nActive pass: **R3.18BV — published-R3.18BU one-control differential**. Exactly two rows only: `sample_002.replay` false `[11239,11240)` and `079_1f838...replay` true `[3238,3239)`. Compare published BU to immutable BR, including independent BS prerequisite, exact bounds/value/stop, repeatability and poison after stop. Nothing adjacent is in scope.\n""")

l=rd("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
lm="## 2026-09-14 — R3.18BU — Bounded Post-BS Next Property-Control Production"
if lm in l: raise SystemExit("ledger duplicate")
l=l.rstrip()+f"""\n\n---\n\n{lm}\nOutcome: **ADMITTED / PUBLISHED PRODUCTION**\n\nProduction `{BU}` / `{TREE}` / parent `{PARENT}`. Blobs: lib `{LIB}`, test `{TEST}`, spec `{SPEC}`. Builder `{BUILD_RUN}/{BUILD_JOB}` SUCCESS; PR #219 CLOSED UNMERGED; exact-head CI `{PR_RUN}/{PR_JOB}` SUCCESS; published-main CI `{MAIN_RUN}/{MAIN_JOB}` SUCCESS.\n\nAdmitted exact lane: Boolean false `[11239,11240)` and ActiveActor true `[3238,3239)`; BP false terminator excluded; exact BS prerequisite required; one control bit consumed; following stream/header/payload/second-control consumption 0/0/0/0; no generic cursor widening. R3.18BV opens read-only.\n"""
wr("docs/continuity/MIMIR_PROGRESS_LEDGER.md",l)

sp=R/"docs/continuity/MIMIR_CONTINUITY_STATE.json"
s=json.loads(sp.read_text(encoding="utf-8"))
s.update({
 "updated_date":DATE,
 "last_production_code_sha":BU,
 "last_production_milestone":"R3.18BU",
 "last_production_milestone_name":"bounded post-BS next property-control production",
 "current_pass":"R3.18BV",
 "current_pass_kind":"read-only published-R3.18BU one-control differential on exactly two authority rows",
 "current_pass_goal":"Validate published R3.18BU against immutable R3.18BR with exact published-BS prerequisite, control value/bounds/stop identity, repeatability and post-stop poison stability.",
 "current_pass_stop_boundary":"Stop at BU stop_bit after one control bit; consume no following stream/header/payload or second later control."
})
s["r3_18bu_admission"]={"status":"published_production","sha":BU,"tree":TREE,"parent":PARENT,"lib_blob":LIB,"test_blob":TEST,"spec_blob":SPEC,"builder_run":BUILD_RUN,"builder_job":BUILD_JOB,"validation_pr":219,"pr_ci_run":PR_RUN,"pr_ci_job":PR_JOB,"main_ci_run":MAIN_RUN,"main_ci_job":MAIN_JOB,"rows":2,"false":1,"true":1,"adjacent_consumption":0}
s["current_pass_contract"]={"pass":"R3.18BV","rows":2,"production_mutation":False,"witness_reselection":False,"must_match_br":True,"must_match_published_bs_prerequisite":True,"repeatability":True,"post_stop_poison":True,"following_structure":False,"second_control":False,"generic_cursor":False}
for f in ["docs/continuity/MIMIR_R3_18BU_DECISION.md","docs/continuity/MIMIR_R3_18BV_EXECUTION_SPEC.md"]:
    if f not in s.get("next_files_to_read",[]): s.setdefault("next_files_to_read",[]).append(f)
sp.write_text(json.dumps(s,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")

wr("docs/continuity/MIMIR_R3_18BU_DECISION.md",f"""# MIMIR R3.18BU Decision — Bounded Post-BS Next Property-Control Production\n\n**Date:** {DATE}\n**Status:** CLOSED / ADMITTED PUBLISHED PRODUCTION\n**Canonical production:** `{BU}` / `{TREE}` / parent `{PARENT}`\n\n## Receipts\n- lib/test/spec blobs: `{LIB}` / `{TEST}` / `{SPEC}`\n- builder `{BUILD_RUN}/{BUILD_JOB}` SUCCESS\n- validation PR #219 CLOSED UNMERGED\n- exact-head CI `{PR_RUN}/{PR_JOB}` SUCCESS\n- published-main CI `{MAIN_RUN}/{MAIN_JOB}` SUCCESS\n- immutable BR `{BR_HEAD}` / artifact `{BR_ART}` / `sha256:{BR_DIG}`\n- BT artifact `{BT_ART}` / `sha256:{BT_DIG}`\n\n## Admitted result\n1. `external_fixtures/sample_002.replay`: exact BS Boolean payload ends 11239; BU control `[11239,11240)` = false; stop 11240.\n2. `test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay`: exact BS ActiveActor payload ends 3238; BU control `[3238,3239)` = true; stop 3239.\n\nBU recomputes/matches exact BS, consumes exactly one checked LSB-first control bit, matches frozen BR and stops. BP false terminator and all adjacent/wider structure remain excluded.\n\n## Decision\nR3.18BU is canonical production. Open R3.18BV as read-only exact published-BU differential only.\n""")

wr("docs/continuity/MIMIR_R3_18BV_EXECUTION_SPEC.md",f"""# MIMIR R3.18BV — Published R3.18BU One-Control Differential\n\n**Status:** ACTIVE\n**Pass type:** read-only published-production differential\n**Production authority:** `{BU}` / `{TREE}`\n**Production mutation:** forbidden\n**Control authority:** R3.18BR `{BR_HEAD}` / artifact `{BR_ART}` / `sha256:{BR_DIG}`\n**Witness reselection:** forbidden\n\n## Goal\nValidate published BU on exactly two immutable rows. Require independently recomputed published BS equality, exact BR start/end/value/stop identity, repeatability and post-stop poison stability. Consume nothing adjacent.\n\n## Frozen rows\n```text\nexternal_fixtures/sample_002.replay                                      11239 -> 11240  false\ntest_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay 3238  -> 3239   true\n```\nExpected: exact=2/2, false/true=1/1, mismatch=0, reselection=0, BP-false excluded=1/1, following stream/header/payload/second-control=0/0/0/0.\n\n## Required checks\n- exact production SHA/tree/lib/test/spec and BU CI receipts;\n- reconstruct published BS independently and require BU prerequisite equality;\n- exact control start/end/stop/value against BR;\n- deterministic repeatability 2/2;\n- truncate at control start -> atomic reject; corrupt BS/context/tag/actor/fabricated row -> reject;\n- poison bits beginning at BU stop -> BU result unchanged;\n- source-scope guard: one bounded control read, no following decoder/loop;\n- focused BU regression, workspace fmt/check/test/clippy and repository verifier;\n- same-head natural CI SUCCESS; privacy-safe deterministic evidence artifact + SHA-256 manifest; no production/Cargo/fixture/corpus/support mutation.\n\n## Continuation classification\nFalse row terminates. True row is the only possible later continuation candidate. BV does not decode a following header. Outcome A alone may open a separate later one-header evidence pass on that single true row.\n\n## Hard stop\nNo following stream/header/payload, second control, generalized/repeated cursor, actor/frame/runtime widening, witness reselection or production mutation.\n\n## Outcome gate\n**A:** exact 2/2 + prerequisite 2/2 + false/true 1/1 + all negatives/validation PASS + adjacent consumption 0.\n**B:** bounded mismatch/narrower subset only; no widening.\n**C:** authority drift, published mismatch, adjacent access, mutation/privacy/generic chaining; stop.\n""")
print("R3_18BU_CONTINUITY_SYNC=PASS")

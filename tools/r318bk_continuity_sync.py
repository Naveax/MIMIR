from pathlib import Path
import json

BASE = "f4a56d53d11a0c3d59f4bd57e58688bdd9d192bf"
TREE = "07656c7a43c1afb97903ef33c1109b764fbf8b7d"
PARENT = "de8df0b2bb36454c97863d4078ce7829fd4ecb77"
LIB_BLOB = "0bfff19a7d285e07508b648dbcd5af95a31838f6"
TEST_BLOB = "1938707e60f7893768747931bf84e3bbac792d1b"
SPEC_BLOB = "12d3c92db43433871deaf2d86889b770bfd4af3d"
BUILDER_RUN = 34211911298
BUILDER_JOB = 102014640422
PR = 216
PR_CI_RUN = 34212312983
PR_CI_JOB = 102015924320
MAIN_CI_RUN = 34212774993
MAIN_CI_JOB = 102017408925


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def write(path: str, text: str):
    Path(path).write_text(text, encoding="utf-8")

# 1) Master handbook canonical fields.
p = Path("MIMIR_CONTINUE_HERE.md")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    "LAST_PRODUCTION_CODE_SHA:\n  def8e959239106e25d95091fcfcf468fec59e228\n\nLAST_PRODUCTION_MILESTONE:\n  R3.18BI — bounded post-BE one-following-payload production",
    f"LAST_PRODUCTION_CODE_SHA:\n  {BASE}\n\nLAST_PRODUCTION_MILESTONE:\n  R3.18BK — bounded post-BI next property-control production",
    "continue production authority",
)
s = replace_once(
    s,
    "CURRENT_PASS:\n  R3.18BK — bounded post-BI next property-control production\n\nCURRENT_PASS_TYPE:\n  production / validate exact published BI result, consume exactly one BH-admitted property_present bit on only three authority rows, accept false=1 and true=2, stop one bit later; following structure forbidden",
    "CURRENT_PASS:\n  R3.18BL — published-R3.18BK mixed next-control differential\n\nCURRENT_PASS_TYPE:\n  read-only published-production differential / exact 3 BH authority rows; false=1 true=2; published BI prerequisite exact; following stream/header/payload/second-control consumption forbidden",
    "continue active pass",
)
closure = f'''\n\nR3_18BK_PRODUCTION_CLOSURE:\n  Outcome A / production / exact 3 immutable BI-BG-BH authority rows\n  production SHA/tree: {BASE} / {TREE}\n  parent: {PARENT}\n  lib/test blobs: {LIB_BLOB} / {TEST_BLOB}\n  BK spec blob: {SPEC_BLOB}\n  builder: {BUILDER_RUN}/{BUILDER_JOB} SUCCESS\n  validation PR: #{PR} closed unmerged\n  exact-head PR CI: {PR_CI_RUN}/{PR_CI_JOB} SUCCESS\n  published-main CI: {MAIN_CI_RUN}/{MAIN_CI_JOB} SUCCESS\n  exact control rows: 3/3 / false=1 true=2 / one bit each\n  BE false excluded: 37 / upstream AU false excluded: 7\n  following stream/header/payload/second-control consumption: 0/0/0/0\n  production scope: exactly 2 files\n\nR3_18BL_ACTIVE:\n  published-R3.18BK one-control differential only\n  immutable BH authority: exact 3 rows / false=1 true=2\n  one false row is a terminator; two true rows are continuation candidates only after BL Outcome A\n  no following header decode during BL\n'''
if "R3_18BK_PRODUCTION_CLOSURE:" in s:
    raise SystemExit("continue BK closure already present")
s = s.rstrip() + closure + "\n"
p.write_text(s, encoding="utf-8")

# 2) Machine continuity state.
p = Path("docs/continuity/MIMIR_CONTINUITY_STATE.json")
data = json.loads(p.read_text(encoding="utf-8"))
if data.get("current_pass") != "R3.18BK":
    raise SystemExit(f"state current_pass drift: {data.get('current_pass')}")
data["last_production_code_sha"] = BASE
data["last_production_milestone"] = "R3.18BK"
data["last_production_milestone_name"] = "bounded post-BI next property-control production"
data["current_pass"] = "R3.18BL"
data["current_pass_kind"] = "read-only published-R3.18BK mixed next-control differential against immutable R3.18BH authority"
data["current_pass_goal"] = "Revalidate published R3.18BK on exactly the three immutable BH control rows with exact BI prerequisite, boolean/start/end/stop identity, false=1 true=2, repeatability, and zero following stream/header/payload/second-control consumption."
data["current_pass_stop_boundary"] = "Stop exactly at the published BK stop bit, one bit after BI payload_end_bit. No following stream/header/payload, second later control, or generalized property cursor is admitted."
files = data.get("next_files_to_read")
if not isinstance(files, list):
    raise SystemExit("next_files_to_read missing")
anchor = "docs/continuity/MIMIR_R3_18BK_EXECUTION_SPEC.md"
idx = files.index(anchor) + 1
for item in ["docs/continuity/MIMIR_R3_18BK_DECISION.md", "docs/continuity/MIMIR_R3_18BL_EXECUTION_SPEC.md"]:
    if item in files:
        raise SystemExit(f"state already contains {item}")
files[idx:idx] = ["docs/continuity/MIMIR_R3_18BK_DECISION.md", "docs/continuity/MIMIR_R3_18BL_EXECUTION_SPEC.md"]
data["r3_18bk"] = {
    "outcome": "A — admitted / production closed",
    "production_sha": BASE,
    "production_tree": TREE,
    "parent_sha": PARENT,
    "lib_blob": LIB_BLOB,
    "focused_test_blob": TEST_BLOB,
    "execution_spec_blob": SPEC_BLOB,
    "builder_run": BUILDER_RUN,
    "builder_job": BUILDER_JOB,
    "validation_pr": PR,
    "validation_pr_merged": False,
    "exact_head_pr_ci_run": PR_CI_RUN,
    "exact_head_pr_ci_job": PR_CI_JOB,
    "published_main_ci_run": MAIN_CI_RUN,
    "published_main_ci_job": MAIN_CI_JOB,
    "authority_rows": 3,
    "false": 1,
    "true": 2,
    "control_width_bits": 1,
    "be_false_excluded": 37,
    "upstream_au_false_excluded": 7,
    "following_stream_header_payload_second_control_consumption": "0/0/0/0",
    "production_scope_files": 2,
    "next_pass": "R3.18BL"
}
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# 3) Current state is intentionally compact and replaced wholesale.
write("docs/continuity/MIMIR_CURRENT_STATE.md", f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-09-08
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{BASE}`
**Production tree:** `{TREE}`
**Production milestone:** `R3.18BK — bounded post-BI next property-control production`
**Last read-only evidence/audit:** `R3.18BJ — Outcome A / published BI exact 3/3 / 37 BE-false rejected / 7 AU-false excluded / BH+later consumption=0 / artifact 10042480960`
**Last completed contract:** `R3.18BD — exact_tuple_only / 3 eight-field contexts / multiplicity 3 / contract 33dac50e525ef560490e6c996b6a00a0700ef33b86c400f5d58f84f825df2b27`
**Current exact pass:** `R3.18BL — published-R3.18BK mixed next-control differential`

## Truthful boundary

R3.18BK is canonical production. On exactly the three immutable BI/BG/BH authority rows it recomputes and validates published R3.18BI, starts at exact BI `payload_end_bit`, consumes exactly one R3.18BH-admitted `property_present` bit, accepts both observed boolean classes, and stops exactly one bit later. The frozen distribution is false=1 / true=2.

The 37 R3.18BE false terminators and 7 upstream R3.18AU false terminators remain outside BK success. BK does not consume a following stream ID, header, payload or second later control bit, and exposes no generalized property cursor.

R3.18BL must now independently differential-test the published BK result against immutable BH authority before any following-header evidence is considered. The one false row is only a terminator classification; the two true rows become continuation candidates only after BL Outcome A.

```text
production SHA/tree                    {BASE} / {TREE}
production parent                      {PARENT}
production lib/test blobs              {LIB_BLOB} / {TEST_BLOB}
BK spec blob                           {SPEC_BLOB}
BK builder                             {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
BK validation PR                      #{PR} closed unmerged
BK exact-head PR CI                   {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
BK published-main CI                  {MAIN_CI_RUN}/{MAIN_CI_JOB} SUCCESS
BK exact control rows                 3/3
BK distribution                       false=1 / true=2
BK control width                      1 bit on each row
BE false / AU false excluded          37 / 7
following stream/header/payload/control 0/0/0/0
production scope                      exactly 2 files
```

## Hard stop

R3.18BL is read-only. No following stream/header/payload, no second later control, no production mutation, no witness reselection, no generalized property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
''')

# 4) Current boundary-lock override only; historical sections below remain append-only.
p = Path("docs/continuity/MIMIR_BOUNDARY_LOCKS.md")
s = p.read_text(encoding="utf-8")
start = s.index("# 0. Current override")
end = s.index("# 1. Status vocabulary")
new_override = f'''# 0. Current override — R3.18BK production closed / R3.18BL published differential active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION — R3.18BK
- `{BASE}` / `{TREE}` is canonical production.
- exactly the three immutable BI/BG/BH authority rows are admitted.
- published BI is recomputed/validated; one BH `property_present` bit is consumed; false=1 / true=2 are both successful production data.
- start is exact BI `payload_end_bit`; stop is exactly one bit later.
- 37 BE-false and 7 upstream AU-false rows remain outside success.
- following stream/header/payload/second-control consumption is 0/0/0/0.

## CLOSED READ-ONLY AUTHORITY — R3.18BH / R3.18BJ
- BH exact 3/3 next bits: false=1 / true=2; artifact `10023482583` / `sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d`.
- BJ published-BI differential exact 3/3; artifact `10042480960` / `sha256:e9ec49453dc69c384042b67ee6e459881999478f4ab5e6fe978ce171299ff24d`.

## ACTIVE READ-ONLY PUBLISHED DIFFERENTIAL — R3.18BL
- compare published BK only against immutable BH row/value/boundary authority.
- require published BI prerequisite exact 3/3, BK exact 3/3, false=1 / true=2, mismatch/reselection 0/0.
- one false row is a terminator and two true rows are continuation candidates, but BL must not decode any following header.
- following stream/header/payload/second-control consumption and production mutation must remain zero.

## CLOSED
- following stream/header/payload after the R3.18BK control bit;
- second later property-control bit;
- following-header evidence before R3.18BL Outcome A;
- any BK success outside the exact three immutable BI/BG/BH authority rows;
- wider payload tags/contexts;
- generalized/repeated property cursor;
- actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.

'''
s = s[:start] + new_override + s[end:]
p.write_text(s, encoding="utf-8")

# 5) Handoff.
write("docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md", f'''# MIMIR — Next Chat Handoff

Canonical production is **R3.18BK** at `{BASE}` / `{TREE}`.

**R3.18BK is CLOSED / Outcome A.** It validates/recomputes the published BI prerequisite and consumes exactly one immutable BH `property_present` bit on only three authority rows. Exact distribution false=1 / true=2; start is BI payload end; end/stop is start+1. The 37 BE-false and 7 upstream AU-false rows remain excluded. Following stream/header/payload/second-control consumption is 0/0/0/0.

Production receipts: builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; validation-only PR #{PR} closed unmerged; exact-head PR CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS; published-main CI `{MAIN_CI_RUN}/{MAIN_CI_JOB}` SUCCESS. Clean production scope is exactly `crates/mimir-replay/src/lib.rs` plus `crates/mimir-replay/tests/r3_18bk_post_bi_following_control.rs`.

Active pass: **R3.18BL — Published R3.18BK Mixed Next-Control Differential**. Revalidate published BK against immutable BH on exact 3/3 rows, preserve false=1 / true=2, prove exact BI prerequisite and exact start/value/end/stop, repeatability and negatives, and keep following stream/header/payload/second-control consumption plus production mutation at zero. Do not decode a following header during BL.

Only after BL Outcome A may a separate later pass inspect one following header on exactly the two BK-true continuation rows. The BK-false row is a terminator.

Before dispatch or rerun inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. CI waiting is not a reason to duplicate the same SHA/workflow/input.
''')

# 6) Progress ledger append only.
p = Path("docs/continuity/MIMIR_PROGRESS_LEDGER.md")
s = p.read_text(encoding="utf-8")
if "R3.18BK — Bounded post-BI next property-control production Outcome A" in s:
    raise SystemExit("ledger BK already present")
s = s.rstrip() + f'''\n\n## 2026-09-08 — R3.18BK — Bounded post-BI next property-control production Outcome A

Pass type: bounded production composition
Production SHA/tree: `{BASE}` / `{TREE}`
Parent: `{PARENT}`
Lib/test blobs: `{LIB_BLOB}` / `{TEST_BLOB}`
Execution spec blob: `{SPEC_BLOB}`
Builder: `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS
Validation PR: #{PR} closed unmerged
Exact-head PR CI: `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS
Published-main CI: `{MAIN_CI_RUN}/{MAIN_CI_JOB}` SUCCESS

Admitted production result:
- exact immutable BI/BG/BH rows 3/3;
- one control bit each; false=1 / true=2, both values successful;
- control start equals published BI stop / BG payload end; end/stop equals start+1;
- published BI prerequisite recomputed and exact;
- 37 BE-false rows and 7 upstream AU-false rows excluded;
- repeatability and corrupt-prior/context/lookup/truncation/post-stop-poison/source-scope negatives PASS;
- following stream/header/payload/second-control consumption 0/0/0/0;
- clean production scope exactly 2 files; Cargo/fixture/corpus/support/helper net mutation 0.

Boundaries still closed:
- following stream/header/payload after BK;
- second later property-control bit;
- following-header evidence until BL Outcome A;
- generalized/repeated property cursor and all wider state/event/skill/runtime surfaces.

Next exact pass:
- `R3.18BL — published-R3.18BK mixed next-control differential` on immutable BH authority; no production mutation.\n'''
p.write_text(s, encoding="utf-8")

# 7) Knowledge graph root, mandatory order tail, and append-only milestone detail.
p = Path("MIMIR_KNOWLEDGE_GRAPH.md")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    "R3.18BJ published-R3.18BI one-following-payload differential / Outcome A CLOSED\nR3.18BK bounded post-BI next property-control production / ACTIVE",
    "R3.18BJ published-R3.18BI one-following-payload differential / Outcome A CLOSED\nR3.18BK bounded post-BI next property-control production / PRODUCTION CLOSED\nR3.18BL published-R3.18BK mixed next-control differential / ACTIVE",
    "KG root",
)
s = replace_once(
    s,
    "163. `docs/continuity/MIMIR_R3_18BK_EXECUTION_SPEC.md`\n164. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n165. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n166. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n167. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n168. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n169. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n170. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "163. `docs/continuity/MIMIR_R3_18BK_EXECUTION_SPEC.md`\n164. `docs/continuity/MIMIR_R3_18BK_DECISION.md`\n165. `docs/continuity/MIMIR_R3_18BL_EXECUTION_SPEC.md`\n166. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n167. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n168. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n169. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n170. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n171. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n172. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`",
    "KG mandatory tail",
)
if "### R3.18BK bounded post-BI next property-control production: PRODUCTION / CLOSED" in s:
    raise SystemExit("KG BK detail already present")
s = s.rstrip() + f'''\n\n### R3.18BK bounded post-BI next property-control production: PRODUCTION / CLOSED
- production `{BASE}` / tree `{TREE}` / parent `{PARENT}`
- lib/test blobs `{LIB_BLOB}` / `{TEST_BLOB}`; exact clean scope 2 files / 483 insertions
- builder `{BUILDER_RUN}/{BUILDER_JOB}` SUCCESS; validation-only PR #{PR} closed unmerged; exact-head PR CI `{PR_CI_RUN}/{PR_CI_JOB}` SUCCESS; published-main CI `{MAIN_CI_RUN}/{MAIN_CI_JOB}` SUCCESS
- immutable BH authority rows 3/3; false=1 / true=2; one control bit each; both values admitted
- 37 BE-false + 7 upstream AU-false excluded; following stream/header/payload/second-control 0/0/0/0
- next exact pass: R3.18BL published-BK differential; only BL Outcome A may open following-header evidence on the exact 2 true rows
'''
p.write_text(s, encoding="utf-8")

# 8) BK decision.
write("docs/continuity/MIMIR_R3_18BK_DECISION.md", f'''# MIMIR R3.18BK — Bounded Post-BI Next Property-Control Production Decision

**Date:** 2026-09-08
**Outcome:** **A — ADMITTED / PRODUCTION CLOSED**
**Canonical production:** `{BASE}` / `{TREE}`
**Parent:** `{PARENT}`

## Decision

R3.18BK closes Outcome A. Production now validates/recomputes one exact published R3.18BI payload result and consumes exactly one already-evidenced R3.18BH `property_present` control bit immediately at the BI payload end, on only the three immutable BI/BG/BH authority rows.

Both observed boolean classes are production data at this boundary: **false=1 / true=2**. The control starts exactly at `BI.stop_bit == BI.following_payload.payload_end_bit`, consumes one LSB-first bit, and ends/stops exactly one bit later. Earlier true-only control semantics are not inherited.

The 37 R3.18BE false terminators and 7 upstream R3.18AU false terminators remain outside success. Production reads no following stream ID, header, payload or second later control and exposes no repeated/generalized property cursor.

## Exact authority

```text
production SHA/tree                   {BASE} / {TREE}
parent                                {PARENT}
lib blob                              {LIB_BLOB}
focused BK test blob                  {TEST_BLOB}
BK execution spec blob                {SPEC_BLOB}
builder                               {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
validation PR                         #{PR} closed unmerged
exact-head PR CI                      {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
published-main CI                     {MAIN_CI_RUN}/{MAIN_CI_JOB} SUCCESS
BH artifact                           10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH manifest                           sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
BJ artifact                           10042480960 / sha256:e9ec49453dc69c384042b67ee6e459881999478f4ab5e6fe978ce171299ff24d
pinned Boxcars                        c70e77df7af81b436cb545d070bb90c82f562d0b
```

## Frozen production result

```text
authority rows                        3/3
false / true                          1 / 2
control width                         1 bit each
sample_002                            11231 -> 11232 / true
sample_003                            7815 -> 7816 / false
079_1f838...                          3198 -> 3199 / true
published BI prerequisite             exact 3/3
BE false excluded                     37/37
upstream AU false excluded            7/7
following stream/header/payload       0/0/0 bits
second later control                  0 bits
production scope                      exactly 2 files
```

Focused BK plus BI/BE regressions passed in the builder, full repository verification passed, exact-head PR CI passed, and published-main exact-SHA CI passed. The clean canonical commit contains no workflow/helper, Cargo/dependency, fixture/corpus, support, continuity, skill/runtime/export, or unrelated mutation.

## Sequencing consequence

The next pass is **R3.18BL — Published R3.18BK Mixed Next-Control Differential**. It is read-only and must compare the published BK result against immutable BH authority on exactly the three rows before any following-header evidence is allowed.

The false row is a terminator. The two true rows are only continuation candidates; a later separate pass may inspect one following header on those two rows only after BL Outcome A.

## Hard stop

No following stream/header/payload during BL, no second later control, no production mutation, no witness reselection, no generalized/repeated property cursor, and no actor/frame/lifecycle/raw-state/event/replay-slice/skill/counterfactual/runtime/export widening.
''')

# 9) BL execution spec.
write("docs/continuity/MIMIR_R3_18BL_EXECUTION_SPEC.md", f'''# MIMIR R3.18BL — Published R3.18BK Mixed Next-Control Differential

**Status:** ACTIVE
**Pass type:** read-only published-production differential
**Production authority:** R3.18BK `{BASE}` / `{TREE}`
**Production mutation:** forbidden
**Control authority:** immutable R3.18BH artifact `10023482583`
**Witness reselection:** forbidden

## 1. Goal

Validate published R3.18BK against exactly the three immutable R3.18BH control rows. Prove that published BK reconstructs the exact published BI prerequisite, starts at the frozen BH control start, returns the exact frozen boolean, ends/stops exactly one bit later, and consumes nothing adjacent.

The immutable distribution is **false=1 / true=2**. Both boolean classes are successful published BK results. BL itself must not decode a following stream ID, property header, payload or second later control.

## 2. Frozen authority

```text
production SHA/tree                  {BASE} / {TREE}
production parent                    {PARENT}
lib/test blobs                       {LIB_BLOB} / {TEST_BLOB}
BK execution spec blob               {SPEC_BLOB}
BK builder                           {BUILDER_RUN}/{BUILDER_JOB} SUCCESS
BK validation PR                     #{PR} closed unmerged
BK exact-head PR CI                  {PR_CI_RUN}/{PR_CI_JOB} SUCCESS
BK published-main CI                 {MAIN_CI_RUN}/{MAIN_CI_JOB} SUCCESS
BH artifact                          10023482583 / sha256:26e2bf42abe3d174949bc37b2e3e5e7e02a6caff2fa0490cbc9f3fa30626822d
BH manifest                          sha256:9eba3e774500eccf0fa1df06d98588ea945b237683594ebd0a8e89c3bad671aa
BH rows                              3
BH distribution                      false=1 / true=2
BE false terminators                 37
upstream AU false terminators        7
pinned Boxcars                       c70e77df7af81b436cb545d070bb90c82f562d0b
```

Exact BH rows:

```text
external_fixtures/sample_002.replay                                      11231 -> 11232  true
external_fixtures/sample_003.replay                                       7815 -> 7816   false
test_corpus/largest_100/079_1f838b01-66b5-4963-b62e-64f3d7dbd545.replay 3198 -> 3199   true
```

No filename/hash/path is a production support predicate. These identities are frozen differential witnesses only.

## 3. Exact differential lane

For each exact BH authority row:

1. reconstruct all published prerequisites through R3.18BI;
2. call published R3.18BK exactly once;
3. require BK embedded BI composition to equal the independently recomputed published BI result;
4. require `property_present_start_bit == BI.stop_bit == frozen BH control_start_bit`;
5. require BK boolean == frozen BH boolean;
6. require `property_present_end_bit == stop_bit == frozen BH control_end_bit == start + 1`;
7. repeat and require exact identical output;
8. poison bits beginning at BK stop and require the BK result unchanged;
9. stop without reading any following structure.

Expected totals:

```text
published BK exact                   3/3
published BI prerequisite            3/3
false / true                         1 / 2
boundary/value mismatch              0
witness reselection                  0
BE false excluded                    37/37
upstream AU false excluded           7/7
following stream/header/payload      0/0/0 bits
second later control                 0 bits
production mutation                  0
```

## 4. Required negative controls

At minimum:
- truncate exactly before the BK control bit -> reject atomically;
- corrupt/mismatch the supplied BI prior -> reject;
- wrong actor authority -> reject before BK control success;
- unresolved lookup -> reject before BK control success;
- wrong exact context -> reject;
- repeat identical invocation -> exact equality;
- poison bits beginning at BK stop -> returned one-bit result unchanged;
- all 37 BE-false terminators remain outside BK success;
- all 7 upstream AU-false terminators remain outside BK success;
- source-scope guard -> one published BI recomputation plus one control read, no generic loop/header/payload decode.

Because both booleans are admitted, flipping a frozen control bit is not an API-malformed negative. If used as a differential mutation, report it as frozen-value mismatch rather than expected API rejection.

## 5. Evidence artifact

Produce one privacy-safe immutable artifact containing:
- exact BK SHA/tree/lib/test/spec identities and CI receipts;
- exact BH artifact/digest/manifest authority;
- the three frozen witness identities and 37+7 negative-lane counts;
- per-row published-BK versus frozen-BH and independently recomputed published-BI comparison;
- exact boolean/start/end/stop summaries;
- repeatability and required negative-control results;
- adjacent-consumption counters;
- production/Cargo/fixture/corpus/support mutation counters;
- same-head normal-CI receipt;
- privacy result and SHA-256 inner manifest.

## 6. Validation

Require exact witness identity 3/3; published BK exact 3/3; published BI prerequisite exact 3/3; false=1 / true=2; mismatch/reselection 0/0; repeatability PASS; all negatives PASS; 37 BE-false rejected/excluded and 7 AU-false excluded; following stream/header/payload/second-control consumption 0/0/0/0; focused BK regressions PASS; full `mimir-replay` plus workspace fmt/check/test/clippy and repository verifier PASS; same-head normal CI SUCCESS with no duplicate equivalent run; production/Cargo/fixture/corpus/support mutation 0/0/0/0/0; privacy scan PASS.

Before dispatch or rerun, inspect queued/waiting/in-progress equivalent runs and reuse an existing exact run. Rerun is never polling.

## 7. Continuation classification

The frozen boolean controls continuation:
- the exact one false row is a terminator and must stop after BK;
- the exact two true rows are continuation candidates.

BL does not decode any following header. Only if BL closes Outcome A may a separate later pass investigate exactly one following property header on the exact two true rows, stopping at that header's payload start.

## 8. Hard stop

No following stream/header/payload, no second later control, no generalized/repeated property loop/cursor, no next actor/frame/lifecycle mutation, no raw-state/event/replay-slice/skill/counterfactual/runtime/export widening, and no production mutation.

## 9. Outcome gate

### Outcome A
Published R3.18BK is exact on all three immutable BH witnesses with false=1 / true=2, published BI prerequisite exact 3/3, mismatch/reselection 0/0, all negative/full validations PASS and adjacent consumption 0/0/0/0. A later separate read-only pass may investigate one following header on exactly the two true continuation rows.

### Outcome B
A bounded mismatch or narrower supported subset is isolated. Admit only supported facts and keep following-header evidence closed.

### Outcome C
Authority/witness drift, published mismatch, rejection of a BH-admitted boolean class, adjacent access, production mutation, privacy failure or generic chaining. Stop without widening.
''')

# Final local consistency checks.
assert Path("docs/continuity/MIMIR_R3_18BK_DECISION.md").exists()
assert Path("docs/continuity/MIMIR_R3_18BL_EXECUTION_SPEC.md").exists()
assert "R3.18BL" in Path("MIMIR_CONTINUE_HERE.md").read_text(encoding="utf-8")
assert "R3.18BL" in Path("MIMIR_KNOWLEDGE_GRAPH.md").read_text(encoding="utf-8")

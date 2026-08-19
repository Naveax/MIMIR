from pathlib import Path
import json, re, sys

AB_HEAD='b2f4b73600165b2d83389b6ce43709b64beba52a'
AB_TREE='8d36c8c7118db8c6f0d28c4ae88e0400cf4a3cd1'
AB_RUN='32230919566'
AB_JOB='96000311036'
AB_CI_RUN='32230919652'
AB_CI_JOB='96000311479'
AB_ART='9357559410'
AB_SIZE='12607'
AB_DIGEST='sha256:4b6d72b154440ee2b819f5a5ecb6fa3768e086b7ec4ba0d0c53d0e8e3ad23d99'
AB_FAILED_HEAD='f2f79e47fefbe7ee95ea5df84c78a86868f57bb3'
AB_FAILED_RUN='32229955227'
AB_FAILED_JOB='95997443235'
BASE='713298a04bbb5491286e7f4ee5bf47a5d201b28c'
BASE_TREE='5cca2c6c15013895e01ab4acf083fed59f8023da'
PROD='9392240c49f95766c214afee9865fed4155a87a4'
PROD_TREE='968520d480f78c528086e4e31b2ce307f4f8d232'
Z='81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9'

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,s): Path(p).write_text(s,encoding='utf-8',newline='\n')
def rep(s, old, new, label):
    if old not in s:
        raise SystemExit(f'missing replacement {label}')
    return s.replace(old,new,1)

def fill_template(src,dst):
    s=read(src)
    for k,v in {
        '__AB_HEAD__':AB_HEAD,'__AB_TREE__':AB_TREE,'__AB_RUN__':AB_RUN,'__AB_JOB__':AB_JOB,
        '__AB_CI_RUN__':AB_CI_RUN,'__AB_CI_JOB__':AB_CI_JOB,'__AB_ARTIFACT__':AB_ART,
        '__AB_ARTIFACT_SIZE__':AB_SIZE,'__AB_ARTIFACT_DIGEST__':AB_DIGEST,
    }.items(): s=s.replace(k,v)
    if '__AB_' in s: raise SystemExit(f'unfilled placeholder in {src}')
    write(dst,s)

fill_template('/tmp/MIMIR_R3_18AB_DECISION.template.md','docs/continuity/MIMIR_R3_18AB_DECISION.md')
fill_template('/tmp/MIMIR_R3_18AC_EXECUTION_SPEC.template.md','docs/continuity/MIMIR_R3_18AC_EXECUTION_SPEC.md')

write('docs/continuity/MIMIR_CURRENT_STATE.md', f'''# MIMIR — Current Canonical State

**Continuity date:** 2026-08-19
**Repository:** `Naveax/MIMIR`
**Canonical production SHA:** `{PROD}`
**Production tree:** `{PROD_TREE}`
**Production milestone:** `R3.18AA — bounded post-W following-header composition`
**Last read-only evidence:** `R3.18AB — Outcome A / 47/47 / 18 exact Z contexts / ActiveActor=39 Int=7 UniqueId=1 / mismatch 0 / payload-control 0/0`
**Last structural contract:** `R3.18Z — exact_tuple_only / 18 complete seven-field tuples / 47 multiplicities / R3.18P inheritance false`
**Current exact pass:** `R3.18AC — read-only post-AA following-property payload evidence`

## Truthful boundary

Production remains R3.18AA. Starting only from a valid published R3.18W true control, it decodes exactly one following existing-actor property header with the existing stateless primitive, requires complete R3.18Z exact-tuple membership and stops exactly at `payload_start`.

R3.18AB closed Outcome A on the exact immutable 47-row Y lane: published AA, frozen Y and the direct stateless native header matched 47/47; exact Z contexts reconstructed 18/18 with multiplicities 47/47; ActiveActor/Int/UniqueId were 39/7/1; mismatch, witness reselection, following-payload consumption and another-control consumption were all zero.

```text
production SHA/tree                 {PROD} / {PROD_TREE}
production lib / focused-test blobs 46523f47f94231362b60f8aee038e943e41c7972 / 7df8f84af37d771b12da1334bd195634e4cc6a54
Z contract SHA-256                  {Z}
AB evidence head/tree               {AB_HEAD} / {AB_TREE}
AB authority run/job                {AB_RUN}/{AB_JOB}
AB same-head CI                     {AB_CI_RUN}/{AB_CI_JOB}
AB artifact                         {AB_ART} / {AB_SIZE} bytes / {AB_DIGEST}
```

R3.18AC is read-only and may characterize exactly one payload beginning at the published AA `payload_start` on those same 47 rows. It must use pinned Boxcars ordinal 3 as oracle, independently prove ActiveActor/Int/UniqueId payload end/value/layout facts, and stop before another property-control bit. Production payload composition, another control and generalized property iteration remain closed.
''')

p='docs/continuity/MIMIR_BOUNDARY_LOCKS.md'; s=read(p)
start=s.index('# 0. Current override')
end=s.index('# 1. Status vocabulary')
new=f'''# 0. Current override — R3.18AB closed / R3.18AC active

This current override supersedes older status wording later in this historical lock file.

## PRODUCTION
- R3.18AA `{PROD}` / `{PROD_TREE}`: validates one published R3.18W true-control boundary, decodes exactly one following existing-actor header with the stateless primitive, requires exact R3.18Z seven-field membership, and stops at `payload_start`.

## CLOSED EVIDENCE — R3.18AB Outcome A
- exact immutable R3.18Y 47-row lane; witness reselection 0;
- published R3.18AA / frozen Y / direct stateless header exact 47/47;
- exact R3.18Z contexts 18/18 and multiplicities 47/47; ActiveActor=39 / Int=7 / UniqueId=1;
- mismatch 0; following-payload/another-control consumption 0/0; privacy PASS;
- authority `{AB_RUN}/{AB_JOB}` and same-head CI `{AB_CI_RUN}/{AB_CI_JOB}` SUCCESS; artifact `{AB_ART}` / `{AB_DIGEST}`.

## CLOSED CONTRACT — R3.18Z Outcome A
- contract `{Z}`; `exact_tuple_only`; 18 contexts / 47 multiplicities;
- tag/component/Cartesian/versionless/outside-set membership false;
- R3.18P cross-boundary inheritance false.

## ACTIVE READ-ONLY GATE — R3.18AC
- exactly the same frozen 47 AB/Y rows; witness reselection forbidden;
- start at AA `payload_start`, compare pinned Boxcars ordinal-3 payload facts to the narrow existing native primitive;
- observed header classes are ActiveActor=39 / Int=7 / UniqueId=1, but payload widths/layouts must be proven rather than inferred;
- stop at exactly one payload end; another control remains unopened; production mutation forbidden.

## CLOSED
- post-AA payload production composition; another property control; generic/repeated property cursor/loop;
- next actor/frame/lifecycle; raw state/events/slices/skills/counterfactual/runtime/export widening.

---

'''
s=s[:start]+new+s[end:]
write(p,s)

write('docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md', f'''# MIMIR — Next Chat Handoff

Canonical production remains **R3.18AA** at `{PROD}` / `{PROD_TREE}`. It composes exactly one post-W following header after a valid R3.18W true control, requires full R3.18Z exact-tuple membership, and stops at `payload_start`; no post-AA payload composition is production.

R3.18AB is **CLOSED Outcome A**. Authority `{AB_HEAD}` / tree `{AB_TREE}` / run-job `{AB_RUN}/{AB_JOB}` and same-head CI `{AB_CI_RUN}/{AB_CI_JOB}` are SUCCESS. Artifact `{AB_ART}` is `{AB_SIZE}` bytes with digest/verified ZIP SHA-256 `{AB_DIGEST}` and internal manifest 9/9. Published-AA/frozen-Y/direct-native equality is 47/47, R3.18Z exact contexts 18/18, multiplicities 47/47, ActiveActor/Int/UniqueId 39/7/1, mismatch 0, witness reselection 0, payload/control consumption 0/0, all required negatives 47/47 and privacy PASS. Initial `{AB_FAILED_HEAD}` / `{AB_FAILED_RUN}/{AB_FAILED_JOB}` was superseded because its byte-prefix truncation harness rejected only 39/47; positive/equality evidence was already 47/47 and production was unchanged.

The active pass is **R3.18AC**, read-only ordinal-3 following-property-payload evidence on exactly those same 47 rows. It must compare pinned Boxcars `c70e77df7af81b436cb545d070bb90c82f562d0b` against existing native payload primitives for ActiveActor=39, Int=7 and UniqueId=1, prove exact payload start/end/width/value and UniqueId system/layout without assuming a generic width, and stop before another property-control bit. Read `MIMIR_CONTINUE_HERE.md`, `MIMIR_KNOWLEDGE_GRAPH.md`, `docs/continuity/MIMIR_CONTINUITY_STATE.json`, `docs/continuity/MIMIR_R3_18AB_DECISION.md`, and `docs/continuity/MIMIR_R3_18AC_EXECUTION_SPEC.md` first.
''')

p='docs/continuity/MIMIR_CONTINUITY_STATE.json'; s=read(p)
for old,new,label in [
('"updated_date": "2026-08-18"','"updated_date": "2026-08-19"','date'),
('"last_completed_read_only_audit": "R3.18Y"','"last_completed_read_only_audit": "R3.18AB"','last audit'),
('"current_pass": "R3.18AB"','"current_pass": "R3.18AC"','current pass'),
('"current_pass_kind": "read-only evidence / published R3.18AA post-W following-header differential"','"current_pass_kind": "read-only evidence / post-AA ordinal-3 following-property payload discovery"','kind'),
('"current_pass_goal": "Differentially validate published R3.18AA on the exact immutable R3.18Y 47-row lane through payload_start."','"current_pass_goal": "Characterize exactly one payload beginning at published R3.18AA payload_start on the exact immutable 47-row AB/Y lane against pinned Boxcars ordinal 3."','goal'),
('"current_pass_stop_boundary": "Stop exactly at the published AA header payload_start. No following payload, another control, loop/cursor, next actor/frame or semantic/runtime/export widening."','"current_pass_stop_boundary": "Stop exactly at the one ordinal-3 payload end. No another control, loop/cursor, production payload composition, next actor/frame or semantic/runtime/export widening."','stop'),
('"last_completed_evidence_pass": "R3.18Y"','"last_completed_evidence_pass": "R3.18AB"','last evidence'),
('"last_completed_evidence_outcome": "A — one post-W following header exact on 47/47; 18 exact contexts; ActiveActor=39 Int=7 UniqueId=1; mismatch 0; payload/control 0/0."','"last_completed_evidence_outcome": "A — published R3.18AA/frozen-Y/direct-header exact 47/47; 18/18 Z contexts and 47/47 multiplicities; ActiveActor=39 Int=7 UniqueId=1; mismatch 0; payload/control 0/0."','last outcome'),
]: s=rep(s,old,new,label)
s=rep(s,'    "docs/continuity/MIMIR_R3_18AB_EXECUTION_SPEC.md",\n','    "docs/continuity/MIMIR_R3_18AB_EXECUTION_SPEC.md",\n    "docs/continuity/MIMIR_R3_18AB_DECISION.md",\n    "docs/continuity/MIMIR_R3_18AC_EXECUTION_SPEC.md",\n','reading files')
json.loads(s)
write(p,s)

print('R3_18AB_CONTINUITY_STATE=PASS')

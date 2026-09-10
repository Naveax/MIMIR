from pathlib import Path
import json,re,os
DATE='2026-09-10'
BQ_ART=10144392560
BQ_HEAD='16c43f38e740c57ae9cb90c92084002ec83815e7'
BQ_TREE='58248877a59fb0ddad707e32f92b2cec91f6b434'
BQ_RUN=34457725716
BQ_JOB=102807933610
BQ_CI_RUN=34457725700
BQ_CI_JOB=102808516101
BQ_DIGEST='sha256:52799466bcba42667c51995c1f99cc12325a7a329b5bb355561e64319f64225c'
BQ_MANIFEST='332447c57f92f6f9af84e12bf74124adfe478d225e82cdb5d4cf8e925f7a97c9'

def r(p): return Path(p).read_text(encoding='utf-8')
def w(p,s):
    q=Path(p); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(s,encoding='utf-8',newline='\n')
def one(s,a,b,label):
    if s.count(a)!=1: raise SystemExit(f'{label}: expected one, got {s.count(a)}')
    return s.replace(a,b,1)
def field(s,k,v):
    out,n=re.subn(rf'(?m)^({re.escape(k)}:\n)  .*?$',rf'\g<1>  {v}',s,count=1)
    if n!=1: raise SystemExit(f'{k}: expected one, got {n}')
    return out

def cp(env,dst): w(dst,r(os.environ[env]))
cp('DEC_FILE','docs/continuity/MIMIR_R3_18BQ_DECISION.md')
cp('BR_FILE','docs/continuity/MIMIR_R3_18BR_EXECUTION_SPEC.md')
cp('CUR_FILE','docs/continuity/MIMIR_CURRENT_STATE.md')
cp('HAND_FILE','docs/continuity/MIMIR_NEXT_CHAT_HANDOFF.md')

p='docs/continuity/MIMIR_CONTINUITY_STATE.json'; st=json.loads(r(p))
st['updated_date']=DATE; st['last_completed_read_only_audit']='R3.18BQ'; st['current_pass']='R3.18BR'
st['current_pass_kind']='read-only exactly-one-next-property-control-bit evidence on the two R3.18BQ payload rows'
st['current_pass_goal']='From each exact R3.18BQ payload_end_bit, observe exactly one next property_present bit natively and with pinned Boxcars; record false/true without prior expectation.'
st['current_pass_stop_boundary']='Stop one bit after BR control observation. No next stream/header/payload, second control, BP-false-row access or generalized cursor.'
st['r3_18bq']={'status':'closed_outcome_a','head':BQ_HEAD,'tree':BQ_TREE,'run':BQ_RUN,'job':BQ_JOB,'same_head_ci_run':BQ_CI_RUN,'same_head_ci_job':BQ_CI_JOB,'same_head_ci_count':1,'artifact':BQ_ART,'artifact_size':9464,'artifact_digest':BQ_DIGEST,'inner_manifest_sha256':BQ_MANIFEST,'bp_rows':3,'false_terminators_excluded':1,'true_payloads':2,'tags':{'Boolean':1,'ActiveActor':1},'widths':{'Boolean':1,'ActiveActor':33},'property_ordinal':7,'native_oracle_mismatch':0,'witness_reselection':0,'false_row_payload_access':0,'next_control_bits_consumed':0,'historical_payload_value_coordinate_inheritance':0}
st['r3_18br']={'status':'active_read_only_next_property_control_evidence','direct_payload_authority_artifact':BQ_ART,'target_rows':2,'excluded_bp_false_rows':1,'expected_distribution':None,'allowed_control_bits_per_row':1,'next_stream_header_payload_open':False,'second_later_control_open':False,'witness_reselection_allowed':False}
closed=st.get('closed_now',[])
x='next property-control bit after the R3.18BQ payload evidence boundary'
while x in closed: closed.remove(x)
for x in ['property-control access on the R3.18BP false terminator during R3.18BR','next stream/header/payload after the one R3.18BR control-bit evidence boundary','second later property-control bit after R3.18BR','production consumption of the R3.18BR-observed control bit before a later production pass','generalized/repeated property loop or generic cursor after R3.18BR']:
    if x not in closed: closed.append(x)
st['closed_now']=closed
reads=st.get('next_files_to_read',[]); new=['docs/continuity/MIMIR_R3_18BQ_DECISION.md','docs/continuity/MIMIR_R3_18BR_EXECUTION_SPEC.md']
for x in new:
    while x in reads: reads.remove(x)
idx=reads.index('docs/continuity/MIMIR_PASS_PROTOCOL.md') if 'docs/continuity/MIMIR_PASS_PROTOCOL.md' in reads else len(reads); reads[idx:idx]=new; st['next_files_to_read']=reads
w(p,json.dumps(st,indent=2,ensure_ascii=False)+'\n')

locks=r('docs/continuity/MIMIR_BOUNDARY_LOCKS.md'); a=locks.index('# 0. Current override'); b=locks.index('# 1. Status vocabulary')
override=f'''# 0. Current override — R3.18BQ payload evidence closed / R3.18BR next-control evidence active\n\nThis current override supersedes older status wording later in this historical lock file.\n\n## PRODUCTION — R3.18BO\n- `cbb823ce7d3fc871c35a83afc5ee21ae71945821` / `146cb78edfb434fd43e532593efce8e35ee97111` remains canonical production.\n- BQ payload composition and later control remain unconsumed in production.\n\n## CLOSED READ-ONLY PAYLOAD EVIDENCE — R3.18BQ\n- evidence `{BQ_HEAD}` / `{BQ_RUN}/{BQ_JOB}` SUCCESS; same-head CI `{BQ_CI_RUN}/{BQ_CI_JOB}` SUCCESS / count 1.\n- artifact `{BQ_ART}` / `{BQ_DIGEST}` / inner manifest `{BQ_MANIFEST}`.\n- false terminator excluded=1; true payloads=2; Boolean=1x1; ActiveActor=1x33; mismatch/reselection=0/0; next-control=0.\n\n## ACTIVE READ-ONLY NEXT-CONTROL EVIDENCE — R3.18BR\n- exactly the two BQ payload rows may reconstruct through payload end and observe one next `property_present` bit.\n- native and pinned Boxcars must match start/value/end exactly; distribution is output, not inherited.\n\n## CLOSED\n- payload/control access on the BP false terminator;\n- next stream/header/payload after BR;\n- second later control;\n- production consumption of BR control;\n- generalized/repeated cursor and wider semantics/runtime.\n\n'''
w('docs/continuity/MIMIR_BOUNDARY_LOCKS.md',locks[:a]+override+locks[b:])

m=r('MIMIR_CONTINUE_HERE.md')
m=field(m,'LAST_COMPLETED_READ_ONLY_AUDIT',f'R3.18BQ — one following payload Outcome A / true=2 / Boolean=1x1 / ActiveActor=1x33 / mismatch 0 / artifact {BQ_ART}')
m=field(m,'LAST_COMPLETED_EVIDENCE_PASS',f'R3.18BQ — exact two payloads / Boolean width1 / ActiveActor K2 width33 / mismatch=0 / next-control=0 / artifact {BQ_ART}')
m=field(m,'CURRENT_PASS','R3.18BR — next property-control bit evidence after exact BQ payload end')
m=field(m,'CURRENT_PASS_TYPE','read-only exactly-one-control-bit differential evidence / BQ payload rows=2 / unknown false-true distribution / no next stream-header-payload')
m+=f'''\n# CURRENT OVERRIDE — {DATE} — R3.18BQ CLOSED / R3.18BR ACTIVE\n\n- BQ `{BQ_HEAD}` / `{BQ_RUN}/{BQ_JOB}` SUCCESS; same-head CI `{BQ_CI_RUN}/{BQ_CI_JOB}` SUCCESS / count 1.\n- artifact `{BQ_ART}` / 9464 bytes / `{BQ_DIGEST}` / inner manifest `sha256:{BQ_MANIFEST}`.\n- exact: BP=3 / false excluded=1 / true payloads=2 / Boolean=1x1 / ActiveActor=1x33 / ordinal7=2/2 / mismatch-reselection=0/0 / false access=0 / next-control=0.\n- R3.18BR: same two payload rows only; exactly one `property_present` bit at exact payload end; distribution unknown; stop one bit later. Adjacent reads and production consumption remain closed.\n'''
w('MIMIR_CONTINUE_HERE.md',m)

kg=r('MIMIR_KNOWLEDGE_GRAPH.md')
kg=one(kg,'R3.18BQ one following payload evidence / ACTIVE','R3.18BQ one following payload evidence / Outcome A CLOSED\nR3.18BR next property-control bit evidence after exact BQ payload end / ACTIVE','kg chain')
old='''174. `docs/continuity/MIMIR_R3_18BP_EXECUTION_SPEC.md`\n175. `docs/continuity/MIMIR_R3_18BP_DECISION.md`\n176. `docs/continuity/MIMIR_R3_18BQ_EXECUTION_SPEC.md`\n177. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n178. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n179. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n180. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n181. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n182. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n183. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
new='''174. `docs/continuity/MIMIR_R3_18BP_EXECUTION_SPEC.md`\n175. `docs/continuity/MIMIR_R3_18BP_DECISION.md`\n176. `docs/continuity/MIMIR_R3_18BQ_EXECUTION_SPEC.md`\n177. `docs/continuity/MIMIR_R3_18BQ_DECISION.md`\n178. `docs/continuity/MIMIR_R3_18BR_EXECUTION_SPEC.md`\n179. `docs/continuity/MIMIR_PASS_PROTOCOL.md`\n180. `docs/continuity/MIMIR_BOUNDARY_LOCKS.md`\n181. `docs/continuity/MIMIR_EXECUTION_ROADMAP_A_TO_Z.md`\n182. `MIMIR_ALL_SOURCES_SUPERBOOK.md`\n183. `docs/chatgpt-archive/SOURCE_REGISTRY.md`\n184. `docs/chatgpt-archive/VALIDATION_MATRIX.md`\n185. `docs/chatgpt-archive/migration/HISTORICAL_TO_CURRENT_MAPPING.md`'''
kg=one(kg,old,new,'kg order')
kg+=f'''\n## CURRENT OVERRIDE — {DATE} — R3.18BQ CLOSED / R3.18BR ACTIVE\n- BQ `{BQ_HEAD}` / `{BQ_RUN}/{BQ_JOB}` SUCCESS; CI `{BQ_CI_RUN}/{BQ_CI_JOB}`; artifact `{BQ_ART}` / `{BQ_DIGEST}` / manifest `sha256:{BQ_MANIFEST}`.\n- exact: false excluded=1; true payloads=2; Boolean=1x1; ActiveActor=1x33; mismatch/reselection=0/0; false access=0; next-control=0.\n- BR: read-only exactly one next `property_present` bit at exact BQ payload end on those same two rows; distribution not pre-admitted; adjacent reads closed.\n'''
w('MIMIR_KNOWLEDGE_GRAPH.md',kg)

led=r('docs/continuity/MIMIR_PROGRESS_LEDGER.md'); anchor='## 2026-09-10 — R3.18BQ — One Following Payload Evidence'
if anchor in led: raise SystemExit('BQ ledger exists')
led+=f'''\n---\n\n{anchor}\nOutcome: **A — CLOSED / ADMITTED READ-ONLY EVIDENCE**\n\nEvidence `{BQ_HEAD}` / `{BQ_RUN}/{BQ_JOB}` SUCCESS; CI `{BQ_CI_RUN}/{BQ_CI_JOB}` SUCCESS / count 1; artifact `{BQ_ART}` / 9464 bytes / `{BQ_DIGEST}`; manifest `sha256:{BQ_MANIFEST}`. Exact 3-row authority: false excluded=1, true payloads=2, Boolean=1x1, ActiveActor=1x33, ordinal7=2/2, mismatch/reselection=0/0, false access=0, next-control=0, historical inheritance=0, mutation=0/0/0/0/0, privacy/full validation PASS.\n\nOpened R3.18BR one-next-property-control-bit evidence at the exact two BQ payload ends. Distribution remains unknown until measured; adjacent reads, BP-false access, production consumption and generalized cursor remain closed.\n'''
w('docs/continuity/MIMIR_PROGRESS_LEDGER.md',led)
print('R3_18BQ_CONTINUITY_PATCH=PASS')
print('R3_18BR_OPENED=PASS')

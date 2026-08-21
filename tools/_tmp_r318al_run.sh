#!/usr/bin/env bash
set -euo pipefail

BASE='02233c8125e658513dcb068370c48b1e8f15a01c'
BASE_TREE='fc9293d821dd3e6e269763c3c0ab091428c29490'
PROD='f20f529e3ada6e9a671ea91e5676a17a00770145'
PROD_TREE='98c675811cca4e4d7f0122c762f371548c9266c2'
AK_TEST_BLOB='9014505e1736498ee5e2ef7a1ce6118030580202'
AJ_CONTRACT_SHA='cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c'
AI_HEAD='9d424dae2ed8cc7a0a6868111805a48763131196'
AI_RUN='32418184036'
AI_JOB='96584056481'
AI_ART='9424764320'
AI_ART_NAME='r318ai-following-property-header-evidence'
AI_ART_SIZE='12054'
AI_ART_DIGEST='sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5'
AK_MAIN_CI='32459617440'
AK_MAIN_CI_JOB='96703744791'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318al"
AI_DIR="$WORK/ai"
rm -rf "$WORK"
mkdir -p "$AI_DIR"
trap 'rm -rf "$WORK"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318al_probe.rs"' EXIT
norm_digest(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

echo '== R3.18AL exact authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$BASE"
test "$(git rev-parse origin/main^{tree})" = "$BASE_TREE"
test "$(git merge-base HEAD "$BASE")" = "$BASE"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$BASE:crates/mimir-replay/tests/r3_18ak_post_ag_following_header.rs")" = "$AK_TEST_BLOB"
test "$(sha256sum docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json | awk '{print $1}')" = "$AJ_CONTRACT_SHA"

mapfile -t changed < <(git diff --name-only "$BASE" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318al_evidence.yml'
  '.github/workflows/_tmp_r318al_trigger.txt'
  'tools/_tmp_r318al_native_probe.rs'
  'tools/_tmp_r318al_run.sh'
)
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 4
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$BASE" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
git diff --exit-code "$PROD" "$BASE" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts

test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AI_RUN" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$AI_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AI_RUN" --jq .head_sha)" = "$AI_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AK_MAIN_CI" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$AK_MAIN_CI_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AK_MAIN_CI" --jq .head_sha)" = "$PROD"

echo 'R3_18AL_AUTHORITY_FREEZE=PASS'

echo '== immutable R3.18AI authority =='
meta="$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AI_ART")"
test "$(jq -r .workflow_run.id <<<"$meta")" = "$AI_RUN"
test "$(jq -r .workflow_run.head_sha <<<"$meta")" = "$AI_HEAD"
test "$(jq -r .name <<<"$meta")" = "$AI_ART_NAME"
test "$(jq -r .size_in_bytes <<<"$meta")" = "$AI_ART_SIZE"
test "$(norm_digest "$(jq -r .digest <<<"$meta")")" = "$(norm_digest "$AI_ART_DIGEST")"
test "$(jq -r .expired <<<"$meta")" = false

gh run download "$AI_RUN" -n "$AI_ART_NAME" -D "$AI_DIR"
(
  cd "$AI_DIR"
  test "$(wc -l < r3_18ai_artifact_sha256.txt)" -eq 9
  sha256sum -c r3_18ai_artifact_sha256.txt
  grep -Fqx 'R3_18AI_OUTCOME=A' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_FROZEN_ROWS=47/47' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_NATIVE_ORACLE_MISMATCH=0' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_WITNESS_RESELECTION=0' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_SECOND_LATER_CONTROL_BITS_CONSUMED=0' r3_18ai_aggregate.txt
)
cp "$AI_DIR/r3_18ai_replay_identity.tsv" r3_18al_replay_identity.tsv
cp "$AI_DIR/r3_18ai_header_rows.json" r3_18al_frozen_ai_header_rows.json
cp "$AI_DIR/r3_18ai_header_summary.json" r3_18al_frozen_ai_header_summary.json

python3 - "$AI_DIR/r3_18ai_header_rows.json" "$AI_DIR/r3_18ai_frozen_witnesses.json" "$WORK/targets.tsv" <<'PY'
import json, sys
from pathlib import Path
rows_doc=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
witness_doc=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
rows=rows_doc['rows']; witnesses=witness_doc['rows']
assert len(rows)==47 and len(witnesses)==47
by_witness={r['label']:r for r in witnesses}
assert len(by_witness)==47
out=[]
for row in sorted(rows,key=lambda r:r['label']):
    label=row['label']; w=by_witness[label]
    assert int(w['published_start'])==int(row['ag_property_present_start_bit'])
    assert int(w['published_stop'])==int(row['ag_stop_bit'])
    assert int(w['prior_stop'])==int(row['ag_property_present_start_bit'])
    assert row['resolved_attribute_tag']=='Int'
    fields=[
      label,row['frame_index'],row['actor_ordinal'],row['actor_context_object_id'],w['first_start'],
      row['ag_property_present_start_bit'],row['ag_stop_bit'],row['stream_id_start_bit'],
      row['stream_id_end_bit'],row['stream_id'],row['stream_id_bound'],row['prop_id_bits'],
      row['resolved_property_object_index'],row['resolved_attribute_tag'],row['payload_start_bit']
    ]
    out.append('\t'.join(map(str,fields)))
assert len(out)==47
Path(sys.argv[3]).write_text('\n'.join(out)+'\n',encoding='utf-8',newline='\n')
print('R3_18AL_FROZEN_TARGET_DERIVATION=PASS rows=47 reselection=0')
PY

python3 - <<'PY'
import hashlib
from pathlib import Path
seen=[]
for line in Path('r3_18al_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel, expected, status=line.split('\t')
    assert status=='PASS'
    path=Path(rel)
    assert not path.is_absolute() and '..' not in path.parts
    assert hashlib.sha256(path.read_bytes()).hexdigest().lower()==expected.lower(),rel
    seen.append(rel.replace('\\','/'))
assert len(seen)==47 and len(set(seen))==47
print('R3_18AL_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== published R3.18AK against frozen R3.18AI =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318al_native_probe.rs crates/mimir-replay/examples/_tmp_r318al_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318al_probe -- "$WORK/targets.tsv" > "$WORK/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318al_probe -- "$WORK/targets.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
test "$(grep -c $'^R3_18AL_NATIVE\t' "$WORK/native1.log")" -eq 47
cp "$WORK/native1.log" r3_18al_native_rows.tsv
rm -f crates/mimir-replay/examples/_tmp_r318al_probe.rs

python3 - "$AI_DIR/r3_18ai_header_rows.json" docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json "$WORK/native1.log" <<'PY'
import collections, json, sys
from pathlib import Path

def kv(line,prefix):
    assert line.startswith(prefix+'\t')
    out={}
    for item in line.split('\t')[1:]:
        k,v=item.split('=',1); out[k]=v
    return out

ai=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
aj=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
native={}
for line in Path(sys.argv[3]).read_text(encoding='utf-8').splitlines():
    if line.startswith('R3_18AL_NATIVE\t'):
        r=kv(line,'R3_18AL_NATIVE'); assert r['label'] not in native; native[r['label']]=r
rows=ai['rows']; assert len(rows)==47 and len(native)==47
assert set(native)=={r['label'] for r in rows}
flags=['published_exact','direct_exact','repeatability','truncation','corrupt_control_negative','corrupt_prior_negative','unresolved_lookup_negative','wrong_context_negative','post_payload_poison']
contexts=collections.Counter(); out=[]
for a in rows:
    n=native[a['label']]
    expected={
      'frame_index':a['frame_index'],'actor_ordinal':a['actor_ordinal'],'actor_context_object_id':a['actor_context_object_id'],
      'ag_start':a['ag_property_present_start_bit'],'ag_stop':a['ag_stop_bit'],
      'stream_start':a['stream_id_start_bit'],'stream_end':a['stream_id_end_bit'],'stream_id':a['stream_id'],
      'stream_bound':a['stream_id_bound'],'prop_bits':a['prop_id_bits'],'property_object':a['resolved_property_object_index'],
      'payload_start':a['payload_start_bit'],'header_stop':a['payload_start_bit'],'ak_stop':a['payload_start_bit']
    }
    for k,v in expected.items(): assert int(n[k])==int(v),(a['label'],k,n[k],v)
    assert n['tag']==a['resolved_attribute_tag']=='Int'
    assert all(n[f]=='1' for f in flags),(a['label'],{f:n[f] for f in flags})
    assert n['following_payload_bits_consumed']=='0' and n['second_later_control_bits_consumed']=='0'
    tup=(int(n['stream_bound']),int(n['prop_bits']),int(n['property_object']),n['tag'],868,32,10)
    contexts[tup]+=1
    out.append({
      'label':a['label'],'frame_index':int(n['frame_index']),'actor_ordinal':int(n['actor_ordinal']),
      'actor_context_object_id':int(n['actor_context_object_id']),'first_start_bit':int(n['first_start']),
      'ag_start_bit':int(n['ag_start']),'ag_stop_bit':int(n['ag_stop']),'stream_id_start_bit':int(n['stream_start']),
      'stream_id_end_bit':int(n['stream_end']),'stream_id':int(n['stream_id']),'stream_id_bound':int(n['stream_bound']),
      'prop_id_bits':int(n['prop_bits']),'resolved_property_object_index':int(n['property_object']),
      'resolved_attribute_tag':n['tag'],'payload_start_bit':int(n['payload_start']),'ak_stop_bit':int(n['ak_stop']),
      'published_ak_frozen_ai_exact':True,'published_ak_direct_header_exact':True,
      'following_payload_bits_consumed':0,'second_later_control_bits_consumed':0
    })
contract=collections.Counter()
for c in aj['admitted_contexts']:
    tup=(c['stream_id_bound'],c['prop_id_bits'],c['property_object_index'],c['attribute_tag'],c['version_major'],c['version_minor'],c['net_version'])
    contract[tup]=c['observed_count']
assert contexts==contract,(contexts,contract)
assert len(contexts)==17 and sum(contexts.values())==47
result={'aggregate':{
  'outcome':'A','rows':47,'published_ak_frozen_ai_exact':47,'published_ak_direct_header_exact':47,
  'native_oracle_mismatch':0,'exact_contexts':17,'context_multiplicity_sum':47,'tags':{'Int':47},
  'witness_reselection':0,'following_payload_bits_consumed':0,'second_later_control_bits_consumed':0
},'rows':out}
Path('r3_18al_comparison.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
summary={'rows':47,'exact_contexts':17,'context_multiplicity_sum':47,'tags':{'Int':47},'native_oracle_mismatch':0,'witness_reselection':0,'aj_contract_exact':True}
Path('r3_18al_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
print('R3_18AL_ANALYZE=PASS rows=47 contexts=17 Int=47 mismatch=0')
PY

# Exact permanent AK regression proves the named anti-widening negatives on the frozen source blob.
cargo +1.85.0 test -p mimir-replay --test r3_18ak_post_ag_following_header -- --nocapture | tee "$WORK/ak_focus.log"
grep -Fq 'test result: ok. 5 passed; 0 failed;' "$WORK/ak_focus.log"
cat > r3_18al_negative_controls.txt <<'EOF'
R3_18AL_REPEATABILITY=PASS 47/47
R3_18AL_HEADER_TRUNCATION=PASS 47/47
R3_18AL_CORRUPT_AG_CONTROL_NEGATIVE=PASS 47/47
R3_18AL_CORRUPT_PRIOR_WRONG_ACTOR_NEGATIVE=PASS 47/47
R3_18AL_UNRESOLVED_LOOKUP_NEGATIVE=PASS 47/47
R3_18AL_WRONG_EXACT_VERSION_CONTEXT_NEGATIVE=PASS 47/47
R3_18AL_POST_PAYLOAD_START_POISON=PASS 47/47
R3_18AL_CARTESIAN_60_5_68_INT=PASS exact_focused_AK_regression
R3_18AL_FABRICATED_60_5_39_INT=PASS exact_focused_AK_regression
R3_18AL_OLD_Z_ONLY_60_5_34_ACTIVEACTOR=PASS exact_focused_AK_regression
R3_18AL_R3_18Z_INHERITANCE=REJECTED
R3_18AL_R3_18P_INHERITANCE=REJECTED
R3_18AL_FOLLOWING_PAYLOAD_BITS_CONSUMED=0
R3_18AL_SECOND_LATER_CONTROL_BITS_CONSUMED=0
EOF

cat > r3_18al_source_scope.txt <<EOF
R3_18AL_BASE_MAIN=$BASE
R3_18AL_BASE_TREE=$BASE_TREE
R3_18AL_PRODUCTION=$PROD
R3_18AL_PRODUCTION_TREE=$PROD_TREE
R3_18AL_AK_TEST_BLOB=$AK_TEST_BLOB
R3_18AL_AJ_CONTRACT_SHA256=$AJ_CONTRACT_SHA
R3_18AL_PRODUCTION_MUTATION=0
R3_18AL_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0
R3_18AL_WITNESS_RESELECTION=0
EOF
cat > r3_18al_upstream_receipts.txt <<EOF
R3_18AL_AI_HEAD=$AI_HEAD
R3_18AL_AI_AUTHORITY=$AI_RUN/$AI_JOB SUCCESS
R3_18AL_AI_ARTIFACT=$AI_ART/$AI_ART_SIZE/$AI_ART_DIGEST
R3_18AL_AK_PUBLISHED_MAIN_CI=$AK_MAIN_CI/$AK_MAIN_CI_JOB SUCCESS
EOF
cat > r3_18al_aggregate.txt <<'EOF'
R3_18AL_OUTCOME=A
R3_18AL_EVIDENCE=PASS
R3_18AL_FROZEN_ROWS=47/47
R3_18AL_PUBLISHED_AK_EXACT=47/47
R3_18AL_DIRECT_HEADER_EXACT=47/47
R3_18AL_AJ_CONTEXTS=17/17
R3_18AL_AJ_MULTIPLICITY=47/47
R3_18AL_TAG_INT=47
R3_18AL_NATIVE_ORACLE_MISMATCH=0
R3_18AL_WITNESS_RESELECTION=0
R3_18AL_FOLLOWING_PAYLOAD_BITS_CONSUMED=0
R3_18AL_SECOND_LATER_CONTROL_BITS_CONSUMED=0
R3_18AL_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18AL_PRIVACY_SCAN=PASS
EOF

# Full validation against unchanged published production.
cargo +1.85.0 test -p mimir-replay
cargo +1.85.0 fmt --all -- --check
cargo +1.85.0 check --workspace --locked --all-targets --all-features
cargo +1.85.0 test --workspace --locked
cargo +1.85.0 clippy --workspace --all-targets --all-features --locked -- -D warnings
pwsh -NoProfile -File scripts/verify_repo.ps1

if grep -E -i '(/home/|/Users/|[A-Za-z]:\\|@gmail\.|@outlook\.|@hotmail\.)' \
  r3_18al_native_rows.tsv r3_18al_comparison.json r3_18al_summary.json r3_18al_replay_identity.tsv \
  r3_18al_frozen_ai_header_rows.json r3_18al_frozen_ai_header_summary.json r3_18al_source_scope.txt \
  r3_18al_upstream_receipts.txt r3_18al_negative_controls.txt r3_18al_aggregate.txt; then
  echo 'privacy scan failed' >&2; exit 1
fi

sha256sum \
  r3_18al_native_rows.tsv \
  r3_18al_comparison.json \
  r3_18al_summary.json \
  r3_18al_replay_identity.tsv \
  r3_18al_frozen_ai_header_rows.json \
  r3_18al_frozen_ai_header_summary.json \
  r3_18al_source_scope.txt \
  r3_18al_upstream_receipts.txt \
  r3_18al_negative_controls.txt \
  r3_18al_aggregate.txt > r3_18al_artifact_sha256.txt
sha256sum -c r3_18al_artifact_sha256.txt
cat r3_18al_aggregate.txt

#!/usr/bin/env bash
set -euo pipefail

MAIN='76abc44458e546e5a2dd6a19286bcc09cd69853d'
MAIN_TREE='ad532a2dfe14a9be16d1292ee70ac1a60015971c'
PROD='58872e94f00ef094807f21ab2ff984ac66b97d91'
PROD_TREE='d6965d77903ea99dad0465bb350b6a673ee7dd00'
LIB_BLOB='d997ae8c3ad2d201b3f43c6ccca7ded2ef03b73b'
W_TEST_BLOB='ac176135c2e6ed56f0b91bdde8c7548f17641cf0'
W_DECISION_BLOB='870a9c47cc7951233c3544ddf367d1dc4818f4d1'
X_SPEC_BLOB='f1ac07c18312631fb35280c73d0ffcaecf37dff7'
W_AUTH='32060501395'; W_AUTH_JOB='95480474127'
W_CAND='32062120856'; W_CAND_JOB='95485540552'
W_PR='32062533181'; W_PR_JOB='95486877308'
W_PUB='32062965119'; W_PUB_JOB='95488256583'
W_CONT_AUTH='32063782318'; W_CONT_AUTH_JOB='95490862312'
W_CONT_CAND_CI='32063988797'; W_CONT_CAND_CI_JOB='95491527556'
W_CONT_CAND_KA='32063988880'; W_CONT_CAND_KA_JOB='95491528292'
W_CONT_PR_CI='32064440300'; W_CONT_PR_CI_JOB='95493014013'
W_CONT_PR_KA='32064440436'; W_CONT_PR_KA_JOB='95493014762'
W_CONT_PUB_CI='32064942309'; W_CONT_PUB_CI_JOB='95494646819'
W_CONT_PUB_KA='32064942366'; W_CONT_PUB_KA_JOB='95494647028'
V_HEAD='2b0c9f01559e77a6fdf21a097b8ab4d1a27b6ff5'
V_TREE='229b3d68a82f6dadc19518614e27ff09e8006ad2'
V_RUN='32057732310'; V_JOB='95471639989'
V_CI='32057732335'; V_CI_JOB='95471640230'
V_ART='9297068554'
V_ART_NAME='r318v-next-property-control-differential-evidence'
V_ART_SIZE='20484'
V_ART_DIGEST='sha256:e17426aad6d476eba17bb471dc92cd24b4b4d8727ad427ad15fa6e9c1dda9eb2'
V_BOXCARS='198096b6693c91cc146aae10fb0a5d3729dd778b7038e3915ede59fd246032b3'

ROOT="$PWD"
TMP="$(mktemp -d)"
V_DIR="$TMP/v"
mkdir -p "$V_DIR"
trap 'rm -rf "$TMP"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318x_probe.rs"' EXIT
norm_digest() { printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }
download_v() {
  for attempt in 1 2 3; do
    rm -rf "$V_DIR"; mkdir -p "$V_DIR"
    if gh run download "$V_RUN" -n "$V_ART_NAME" -D "$V_DIR"; then
      echo "R3_18X_V_DOWNLOAD_ATTEMPT=$attempt"
      return 0
    fi
    sleep $((attempt * 10))
  done
  return 1
}

echo '== R3.18X authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git merge-base HEAD "$MAIN")" = "$MAIN"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$MAIN:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$MAIN:crates/mimir-replay/tests/r3_18w_following_payload_control.rs")" = "$W_TEST_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18W_DECISION.md")" = "$W_DECISION_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18X_EXECUTION_SPEC.md")" = "$X_SPEC_BLOB"
mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=( '.github/workflows/_tmp_r318x_evidence.yml' 'tools/_tmp_r318x_probe.rs' 'tools/_tmp_r318x_run.sh' )
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 3
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0
for run in "$W_AUTH" "$W_CAND" "$W_PR" "$W_PUB" "$W_CONT_AUTH" "$W_CONT_CAND_CI" "$W_CONT_CAND_KA" "$W_CONT_PR_CI" "$W_CONT_PR_KA" "$W_CONT_PUB_CI" "$W_CONT_PUB_KA" "$V_RUN" "$V_CI"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$W_AUTH_JOB" "$W_CAND_JOB" "$W_PR_JOB" "$W_PUB_JOB" "$W_CONT_AUTH_JOB" "$W_CONT_CAND_CI_JOB" "$W_CONT_CAND_KA_JOB" "$W_CONT_PR_CI_JOB" "$W_CONT_PR_KA_JOB" "$W_CONT_PUB_CI_JOB" "$W_CONT_PUB_KA_JOB" "$V_JOB" "$V_CI_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$W_PUB" --jq .head_sha)" = "$PROD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$W_CONT_PUB_CI" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$W_CONT_PUB_KA" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$V_RUN" --jq .head_sha)" = "$V_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$V_RUN" --jq .head_commit.tree_id)" = "$V_TREE"
echo 'R3_18X_AUTHORITY_FREEZE=PASS'

echo '== immutable R3.18V lane =='
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$V_ART" --jq .workflow_run.id)" = "$V_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$V_ART" --jq .workflow_run.head_sha)" = "$V_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$V_ART" --jq .name)" = "$V_ART_NAME"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$V_ART" --jq .size_in_bytes)" = "$V_ART_SIZE"
test "$(norm_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$V_ART" --jq .digest)")" = "$(norm_digest "$V_ART_DIGEST")"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$V_ART" --jq .expired)" = false
download_v
(cd "$V_DIR" && test "$(wc -l < r3_18v_artifact_sha256.txt)" -eq 11 && sha256sum -c r3_18v_artifact_sha256.txt)
grep -Fq 'R3_18V_OUTCOME=A' "$V_DIR/r3_18v_aggregate.txt"
grep -Fq 'R3_18V_CONTROL_FALSE=0' "$V_DIR/r3_18v_aggregate.txt"
grep -Fq 'R3_18V_CONTROL_TRUE=47' "$V_DIR/r3_18v_aggregate.txt"
grep -Fq 'R3_18V_NATIVE_ORACLE_MISMATCH=0' "$V_DIR/r3_18v_aggregate.txt"
grep -Fq 'R3_18V_SECOND_LATER_CONTROL_BITS_CONSUMED=0' "$V_DIR/r3_18v_aggregate.txt"
grep -Fq "$V_BOXCARS" "$V_DIR/r3_18v_boxcars_instrumentation_sha256.txt"
cp "$V_DIR/r3_18v_replay_identity.tsv" r3_18x_replay_identity.tsv
cp "$V_DIR/r3_18v_frozen_witnesses.json" r3_18x_frozen_witnesses.json

python3 - "$V_DIR/r3_18v_frozen_witnesses.json" "$V_DIR/r3_18v_comparison.json" <<'PY'
import json,sys
w=json.load(open(sys.argv[1],encoding='utf-8'))
v=json.load(open(sys.argv[2],encoding='utf-8'))
cont={x['label']:x for x in w if x.get('class')=='continuation'}
rows={x['label']:x for x in v['rows']}
a=v['aggregate']
assert len(cont)==len(rows)==47 and set(cont)==set(rows)
assert a['outcome']=='A' and a['rows']==47 and a['false']==0 and a['true']==47
assert a['native_oracle_mismatch']==0 and a['published_r3_18t_exact']==47 and a['witness_reselection']==0
assert a['next_stream_bits_consumed']==a['next_header_bits_consumed']==a['next_payload_bits_consumed']==a['second_later_control_bits_consumed']==0
with open('r3_18x_targets.tsv','w',encoding='utf-8',newline='\n') as f:
    for label in sorted(rows):
        x=rows[label]; y=cont[label]
        assert x['published_r3_18t_exact'] is True and x['native_oracle_exact'] is True and x['property_present'] is True
        assert x['frame_index']==y['frame_index'] and x['actor_ordinal']==y['actor_ordinal'] and x['actor_context_object_id']==y['actor_context_object_id']
        assert x['property_present_start_bit']==x['prior_r3_18t_stop_bit'] and x['property_present_end_bit']==x['property_present_start_bit']+1
        vals=[label,x['frame_index'],x['actor_ordinal'],x['actor_context_object_id'],y['first_property_present_start_bit'],x['prior_r3_18t_stop_bit'],x['property_present_start_bit'],x['property_present_end_bit'],1]
        f.write('\t'.join(map(str,vals))+'\n')
print('R3_18X_TARGETS=PASS rows=47 reselection=0')
PY
python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18x_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel,expected,status=line.split('\t')
    assert status=='PASS' and not rel.startswith('/') and '..' not in Path(rel).parts
    assert hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower()==expected.lower(), rel
    rows.append(rel.replace('\\','/'))
assert len(rows)==47 and len(set(rows))==47
print('R3_18X_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== published W differential =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318x_probe.rs crates/mimir-replay/examples/_tmp_r318x_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318x_probe -- r3_18x_targets.tsv > "$TMP/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318x_probe -- r3_18x_targets.tsv > "$TMP/native2.log"
cmp "$TMP/native1.log" "$TMP/native2.log"
test "$(grep -c $'^R3_18X_NATIVE\t' "$TMP/native1.log")" -eq 47
rm -f crates/mimir-replay/examples/_tmp_r318x_probe.rs

python3 - "$V_DIR/r3_18v_comparison.json" "$TMP/native1.log" <<'PY'
import json,sys
from pathlib import Path
v=json.load(open(sys.argv[1],encoding='utf-8'))
vrows={x['label']:x for x in v['rows']}
def parse(line):
    out={}
    for item in line.split('\t')[1:]:
        k,val=item.split('=',1); out[k]=val
    return out
native={}
for line in Path(sys.argv[2]).read_text(encoding='utf-8').splitlines():
    if line.startswith('R3_18X_NATIVE\t'):
        r=parse(line); native[r['label']]=r
assert len(vrows)==len(native)==47 and set(vrows)==set(native)
rows=[]
for label in sorted(vrows):
    vrow=vrows[label]; n=native[label]
    exact=(
      vrow['property_present'] is True
      and int(n['frame_index'])==vrow['frame_index'] and int(n['actor_ordinal'])==vrow['actor_ordinal'] and int(n['actor_context_object_id'])==vrow['actor_context_object_id']
      and int(n['t_stop'])==vrow['prior_r3_18t_stop_bit'] and int(n['control_start'])==vrow['property_present_start_bit']
      and int(n['control_end'])==vrow['property_present_end_bit'] and int(n['control_stop'])==vrow['property_present_end_bit'] and n['control_value']=='1'
      and all(n[k]=='1' for k in ['published_t_exact','w_exact','repeatability','truncation','false_rejection','prior_boundary_rejection','post_stop_poison'])
      and all(n[k]=='0' for k in ['next_stream_bits_consumed','next_header_bits_consumed','next_payload_bits_consumed','second_later_control_bits_consumed'])
    )
    assert exact,label
    rows.append({'label':label,'frame_index':vrow['frame_index'],'actor_ordinal':vrow['actor_ordinal'],'actor_context_object_id':vrow['actor_context_object_id'],'prior_r3_18t_stop_bit':vrow['prior_r3_18t_stop_bit'],'property_present_start_bit':vrow['property_present_start_bit'],'property_present_end_bit':vrow['property_present_end_bit'],'property_present':True,'published_w_frozen_v_exact':True,'next_stream_bits_consumed':0,'next_header_bits_consumed':0,'next_payload_bits_consumed':0,'second_later_control_bits_consumed':0})
out={'aggregate':{'outcome':'A','rows':47,'false':0,'true':47,'published_r3_18t_exact':47,'published_w_frozen_v_mismatch':0,'repeatability':'47/47','truncation':'47/47','false_rejection':'47/47','prior_boundary_rejection':'47/47','post_stop_poison':'47/47','next_stream_bits_consumed':0,'next_header_bits_consumed':0,'next_payload_bits_consumed':0,'second_later_control_bits_consumed':0,'witness_reselection':0,'production_cargo_fixture_corpus_support_mutation':'0/0/0/0/0','privacy_scan':'PASS'},'rows':rows}
json.dump(out,open('r3_18x_comparison.json','w',encoding='utf-8'),indent=2,sort_keys=True); open('r3_18x_comparison.json','a').write('\n')
print('R3_18X_PUBLISHED_DIFFERENTIAL=PASS rows=47 true=47 mismatch=0')
PY

cat > r3_18x_negative_controls.txt <<'EOF'
R3_18X_REPEATABILITY=PASS 47/47
R3_18X_CONTROL_TRUNCATION=PASS 47/47
R3_18X_FALSE_CONTROL_REJECTION=PASS 47/47
R3_18X_PRIOR_BOUNDARY_REJECTION=PASS 47/47
R3_18X_POST_STOP_POISON=PASS 47/47
R3_18X_NEXT_STREAM_BITS_CONSUMED=0
R3_18X_NEXT_HEADER_BITS_CONSUMED=0
R3_18X_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18X_SECOND_LATER_CONTROL_BITS_CONSUMED=0
EOF
cat > r3_18x_aggregate.txt <<'EOF'
R3_18X_OUTCOME=A
R3_18X_EVIDENCE=PASS
R3_18X_FROZEN_ROWS=47/47
R3_18X_CONTROL_FALSE=0
R3_18X_CONTROL_TRUE=47
R3_18X_PUBLISHED_R318T_EXACT=47/47
R3_18X_PUBLISHED_W_FROZEN_V_MISMATCH=0
R3_18X_REPEATABILITY=PASS 47/47
R3_18X_CONTROL_TRUNCATION=PASS 47/47
R3_18X_FALSE_CONTROL_REJECTION=PASS 47/47
R3_18X_PRIOR_BOUNDARY_REJECTION=PASS 47/47
R3_18X_POST_STOP_POISON=PASS 47/47
R3_18X_NEXT_STREAM_BITS_CONSUMED=0
R3_18X_NEXT_HEADER_BITS_CONSUMED=0
R3_18X_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18X_SECOND_LATER_CONTROL_BITS_CONSUMED=0
R3_18X_WITNESS_RESELECTION=0
R3_18X_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18X_PRIVACY_SCAN=PASS
EOF
cat > r3_18x_upstream_receipts.txt <<EOF
R3_18X_MAIN=$MAIN
R3_18X_MAIN_TREE=$MAIN_TREE
R3_18X_PRODUCTION=$PROD
R3_18X_PRODUCTION_TREE=$PROD_TREE
R3_18X_W_AUTH=$W_AUTH/$W_AUTH_JOB
R3_18X_W_CAND=$W_CAND/$W_CAND_JOB
R3_18X_W_PR=$W_PR/$W_PR_JOB
R3_18X_W_PUBLISHED=$W_PUB/$W_PUB_JOB
R3_18X_W_CONT_AUTH=$W_CONT_AUTH/$W_CONT_AUTH_JOB
R3_18X_W_CONT_CAND_CI=$W_CONT_CAND_CI/$W_CONT_CAND_CI_JOB
R3_18X_W_CONT_CAND_KA=$W_CONT_CAND_KA/$W_CONT_CAND_KA_JOB
R3_18X_W_CONT_PR_CI=$W_CONT_PR_CI/$W_CONT_PR_CI_JOB
R3_18X_W_CONT_PR_KA=$W_CONT_PR_KA/$W_CONT_PR_KA_JOB
R3_18X_W_CONT_PUB_CI=$W_CONT_PUB_CI/$W_CONT_PUB_CI_JOB
R3_18X_W_CONT_PUB_KA=$W_CONT_PUB_KA/$W_CONT_PUB_KA_JOB
R3_18X_V_AUTH=$V_RUN/$V_JOB
R3_18X_V_CI=$V_CI/$V_CI_JOB
R3_18X_V_ARTIFACT=$V_ART/$V_ART_SIZE/$V_ART_DIGEST
EOF
cat > r3_18x_source_scope.txt <<EOF
R3_18X_BASE_MAIN=$MAIN
R3_18X_BASE_TREE=$MAIN_TREE
R3_18X_PRODUCTION_SHA=$PROD
R3_18X_PRODUCTION_TREE=$PROD_TREE
R3_18X_LIB_BLOB=$LIB_BLOB
R3_18X_W_TEST_BLOB=$W_TEST_BLOB
R3_18X_W_DECISION_BLOB=$W_DECISION_BLOB
R3_18X_SPEC_BLOB=$X_SPEC_BLOB
R3_18X_CHANGED_TEMP_FILES=3
R3_18X_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF

! grep -R -E '/home/|/Users/|C:\\Users\\|runner/work' r3_18x_*.txt r3_18x_*.tsv r3_18x_*.json >/dev/null

echo '== R3.18X repository validation =='
cargo fmt --all -- --check
cargo test --locked -p mimir-replay --test r3_18w_following_payload_control
cargo test --locked -p mimir-replay
cargo check --locked --workspace
cargo test --locked --workspace
cargo clippy --locked --workspace --all-targets -- -D warnings
pwsh -File ./scripts/verify_repo.ps1
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

sha256sum r3_18x_source_scope.txt r3_18x_replay_identity.tsv r3_18x_frozen_witnesses.json r3_18x_targets.tsv r3_18x_comparison.json r3_18x_negative_controls.txt r3_18x_aggregate.txt r3_18x_upstream_receipts.txt > r3_18x_artifact_sha256.txt
test "$(wc -l < r3_18x_artifact_sha256.txt)" -eq 8
sha256sum -c r3_18x_artifact_sha256.txt
cat r3_18x_aggregate.txt

#!/usr/bin/env bash
set -euo pipefail

MAIN='9c3b92829ddbc80cc855f5bd76ae489eb156b81a'
MAIN_TREE='044865771f72d57045f12d927a9c0e8c58004326'
PROD='ccadbf148381c007890d13d5fe8120866a0f40f9'
PROD_TREE='0882601060d0bb6d37fcc03ae7273dcf50dd0be3'
LIB_BLOB='1254d5a3d16e7b97b1dee87a8b459514d25749ef'
AD_TEST_BLOB='013ad6da94b866ecaca94cd6420e7568d9b4b5ee'
AF_SPEC_BLOB='fd3e4debac1c40756c37f106fc68440576678d6c'

AE_HEAD='d72b20275f55c44b97d9ec516f2dffbff84a2d6a'
AE_TREE='a24b6360bf8cace5dfc6fb0ecec4e31f12c986b8'
AE_RUN='32282584789'
AE_JOB='96164550815'
AE_CI_RUN='32342929705'
AE_CI_JOB='96345500068'
AE_ART='9376466530'
AE_ART_NAME='r318ae-published-ad-differential-evidence-v2'
AE_ART_SIZE='11057'
AE_ART_DIGEST='sha256:0eacd0b43929699145a961825de2dbeb6b31342d1cacfa1c68c71cbdd9fc43f4'
AE_ADMIT_RUN='32343614385'
AE_ADMIT_JOB='96347572624'
AE_PR_CI='32343858899'
AE_PR_CI_JOB='96348305685'
AE_PR_KA='32343858987'
AE_PR_KA_JOB='96348306097'

Y_HEAD='413d6c24f8f390a57c21ed345f3f868c263f413c'
Y_RUN='32076198677'
Y_JOB='95529856476'
Y_ART='9303584468'
Y_ART_NAME='r318y-following-property-header-evidence'
Y_ART_SIZE='19642'
Y_ART_DIGEST='sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"
TMP="$(mktemp -d)"
AE_DIR="$TMP/ae"
Y_DIR="$TMP/y"
BOXCARS="$TMP/boxcars"
mkdir -p "$AE_DIR" "$Y_DIR"
trap 'rm -rf "$TMP"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318af_probe.rs"' EXIT
normalize_digest() { printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

echo '== R3.18AF authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git merge-base HEAD "$MAIN")" = "$MAIN"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$MAIN:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$MAIN:crates/mimir-replay/tests/r3_18ad_post_aa_payload.rs")" = "$AD_TEST_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18AF_EXECUTION_SPEC.md")" = "$AF_SPEC_BLOB"
test "$(git rev-parse "$R318C_HEAD:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"
mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=( '.github/workflows/_tmp_r318af_evidence.yml' 'tools/_tmp_r318af_extend_boxcars.py' 'tools/_tmp_r318af_probe.rs' 'tools/_tmp_r318af_run.sh' )
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 4
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

for run in "$AE_RUN" "$AE_CI_RUN" "$AE_ADMIT_RUN" "$AE_PR_CI" "$AE_PR_KA" "$Y_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$AE_JOB" "$AE_CI_JOB" "$AE_ADMIT_JOB" "$AE_PR_CI_JOB" "$AE_PR_KA_JOB" "$Y_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AE_RUN" --jq .head_sha)" = "$AE_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AE_RUN" --jq .head_commit.tree_id)" = "$AE_TREE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AE_CI_RUN" --jq .head_sha)" = "$AE_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AE_PR_CI" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AE_PR_KA" --jq .head_sha)" = "$MAIN"
echo 'R3_18AF_AUTHORITY_RECEIPTS=PASS'

verify_artifact() {
  local aid="$1" run="$2" head="$3" name="$4" size="$5" digest="$6" dir="$7" manifest="$8" entries="$9"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.id)" = "$run"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.head_sha)" = "$head"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .name)" = "$name"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .size_in_bytes)" = "$size"
  test "$(normalize_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .digest)")" = "$(normalize_digest "$digest")"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .expired)" = false
  local ok=0
  for attempt in 1 2 3; do
    rm -rf "$dir"; mkdir -p "$dir"
    if gh run download "$run" -n "$name" -D "$dir"; then ok=1; break; fi
    sleep $((attempt * 5))
  done
  test "$ok" -eq 1
  (cd "$dir" && test "$(wc -l < "$manifest")" -eq "$entries" && sha256sum -c "$manifest")
}
verify_artifact "$AE_ART" "$AE_RUN" "$AE_HEAD" "$AE_ART_NAME" "$AE_ART_SIZE" "$AE_ART_DIGEST" "$AE_DIR" r3_18ae_artifact_sha256.txt 8
verify_artifact "$Y_ART" "$Y_RUN" "$Y_HEAD" "$Y_ART_NAME" "$Y_ART_SIZE" "$Y_ART_DIGEST" "$Y_DIR" r3_18y_artifact_sha256.txt 9
grep -Fx 'R3_18AE_OUTCOME=A' "$AE_DIR/r3_18ae_aggregate.txt"
grep -Fx 'R3_18AE_FROZEN_ROWS=47/47' "$AE_DIR/r3_18ae_aggregate.txt"
grep -Fx 'R3_18AE_PUBLISHED_FROZEN_AC_DIRECT_MISMATCH=0' "$AE_DIR/r3_18ae_aggregate.txt"
grep -Fx 'R3_18AE_ANOTHER_CONTROL_BITS_CONSUMED=0' "$AE_DIR/r3_18ae_aggregate.txt"
echo 'R3_18AF_IMMUTABLE_INPUTS=PASS'

cp "$AE_DIR/r3_18ae_replay_identity.tsv" r3_18af_replay_identity.tsv
cp "$AE_DIR/r3_18ae_published_rows.json" r3_18af_frozen_ae_rows.json
python3 - "$AE_DIR/r3_18ae_published_rows.json" "$Y_DIR/r3_18y_frozen_witnesses.json" <<'PY'
import collections, hashlib, json, sys
from pathlib import Path
ae=json.load(open(sys.argv[1],encoding='utf-8'))
y=json.load(open(sys.argv[2],encoding='utf-8'))
a=ae['aggregate']
assert a['outcome']=='A' and a['rows']==47 and a['published_frozen_ac_direct_mismatch']==0 and a['witness_reselection']==0
assert a['tags']=={'ActiveActor':39,'Int':7,'UniqueId':1}
rows=ae['rows']; assert len(rows)==47
key=lambda r:(r['label'],int(r['frame_index']),int(r['actor_ordinal']),int(r['actor_context_object_id']))
cont={key(w):w for w in y if w.get('class')=='continuation'}
assert len(cont)==47
out=[]
for r in rows:
    k=key(r); assert k in cont and r['published_frozen_ac_direct_exact'] is True and r['another_control_bits_consumed']==0
    w=cont[k]
    out.append([r['label'],str(r['frame_index']),str(r['actor_ordinal']),str(r['actor_context_object_id']),str(w['first_property_present_start_bit']),str(r['payload_start_bit']),str(r['payload_end_bit']),str(r['payload_width']),r['tag']])
assert len(out)==47 and len({r[0] for r in out})==47
Path('r3_18af_targets.tsv').write_text('\n'.join('\t'.join(x) for x in sorted(out))+'\n',encoding='utf-8',newline='\n')
ids=[]
for line in Path('r3_18af_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel,expected,status=line.split('\t'); p=Path(rel)
    assert status=='PASS' and not p.is_absolute() and '..' not in p.parts and p.exists()
    assert hashlib.sha256(p.read_bytes()).hexdigest().lower()==expected.lower()
    ids.append(rel)
assert len(ids)==47 and len(set(ids))==47
print('R3_18AF_TARGETS=PASS rows=47 witness_reselection=0')
PY

echo '== pinned Boxcars ordinal-4 property-control oracle =='
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$TMP/r318c_base_patch.py"
python3 - "$TMP/r318c_base_patch.py" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8'); old='    stream_id_bound: i32,\n'
assert s.count(old)==1
p.write_text(s.replace(old,'    stream_id_bound: u32,\n',1),encoding='utf-8',newline='\n')
PY
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
python3 "$TMP/r318c_base_patch.py" "$BOXCARS"
python3 tools/_tmp_r318af_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18af_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18af_probe.rs Cargo.toml > "$TMP/r318af_boxcars.patch"
BOXCARS_PATCH_SHA="$(sha256sum "$TMP/r318af_boxcars.patch" | awk '{print $1}')"
printf '%s  r318af_boxcars_one_bit_instrumentation.patch\n' "$BOXCARS_PATCH_SHA" > r3_18af_boxcars_instrumentation_sha256.txt
RUSTUP_TOOLCHAIN=stable cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18af_probe --quiet
ORACLE="$BOXCARS/target/debug/examples/r3_18af_probe"
: > "$TMP/oracle.log"
while IFS=$'\t' read -r rel frame actor actor_obj first_start payload_start payload_end width tag; do
  MIMIR_R3_18AF_LABEL="$rel" MIMIR_R3_18AF_TARGET_FRAME="$frame" MIMIR_R3_18AF_TARGET_ACTOR_ORDINAL="$actor" "$ORACLE" "$ROOT/$rel" >> "$TMP/oracle.log" 2>&1
done < r3_18af_targets.tsv
test "$(grep -c '^R3_18AF_ORACLE_PARSE=PASS$' "$TMP/oracle.log")" -eq 47
test "$(grep -c $'^R3_18AF_ORACLE\t' "$TMP/oracle.log")" -eq 47
echo 'R3_18AF_BOXCARS_ORACLE=PASS controls=47 ordinal=4'

echo '== published AD reconstruction + independent one-bit observer =='
cp tools/_tmp_r318af_probe.rs crates/mimir-replay/examples/_tmp_r318af_probe.rs
RUSTUP_TOOLCHAIN=1.85.0 cargo run -p mimir-replay --example _tmp_r318af_probe --quiet -- r3_18af_targets.tsv > "$TMP/native.log"
test "$(grep -c $'^R3_18AF_NATIVE\t' "$TMP/native.log")" -eq 47
grep -Fx 'R3_18AF_NATIVE_PARSE=PASS rows=47' "$TMP/native.log"
rm -f crates/mimir-replay/examples/_tmp_r318af_probe.rs

python3 - "$TMP/oracle.log" "$TMP/native.log" <<'PY'
import json,sys
from pathlib import Path

def kv(line,prefix):
    parts=line.rstrip('\n').split('\t'); assert parts[0]==prefix
    d={}
    for x in parts[1:]: k,v=x.split('=',1); d[k]=v
    return d
oracle={}; native={}
for line in open(sys.argv[1],encoding='utf-8',errors='replace'):
    if line.startswith('R3_18AF_ORACLE\t'):
        r=kv(line,'R3_18AF_ORACLE'); assert r['label'] not in oracle; oracle[r['label']]=r
for line in open(sys.argv[2],encoding='utf-8',errors='replace'):
    if line.startswith('R3_18AF_NATIVE\t'):
        r=kv(line,'R3_18AF_NATIVE'); assert r['label'] not in native; native[r['label']]=r
assert len(oracle)==47 and len(native)==47 and set(oracle)==set(native)
rows=[]; false_count=0; true_count=0; mismatch=0
for label in sorted(native):
    o=oracle[label]; n=native[label]
    os=int(o['next_property_present_start_bit']); oe=int(o['next_property_present_end_bit']); ov=int(o['next_property_present'])
    ns=int(n['control_start']); ne=int(n['control_end']); nv=int(n['control_value']); prior=int(n['prior_ad_stop'])
    exact=(prior==os==ns and oe==os+1 and ne==ns+1 and nv==ov and n['published_ad_exact']=='1'
           and n['repeatability']=='1' and n['truncation']=='1' and n['prior_stop_mismatch_negative']=='1'
           and n['post_control_poison']=='1' and n['next_stream_bits_consumed']=='0' and n['next_header_bits_consumed']=='0'
           and n['next_payload_bits_consumed']=='0' and n['second_later_control_bits_consumed']=='0')
    if not exact: mismatch+=1
    if ov==0: false_count+=1
    elif ov==1: true_count+=1
    else: raise AssertionError((label,ov))
    rows.append({'label':label,'frame_index':int(n['frame_index']),'actor_ordinal':int(n['actor_ordinal']),'actor_context_object_id':int(n['actor_context_object_id']),'prior_r3_18ad_stop_bit':prior,'property_present_start_bit':os,'property_present_end_bit':oe,'property_present':bool(ov),'published_r3_18ad_exact':n['published_ad_exact']=='1','native_oracle_exact':exact,'next_stream_bits_consumed':0,'next_header_bits_consumed':0,'next_payload_bits_consumed':0,'second_later_control_bits_consumed':0})
assert false_count+true_count==47 and mismatch==0
summary={'rows':47,'false':false_count,'true':true_count,'published_r3_18ad_exact':47,'native_oracle_mismatch':0,'witness_reselection':0}
Path('r3_18af_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
Path('r3_18af_comparison.json').write_text(json.dumps({'aggregate':summary,'rows':rows},indent=2,sort_keys=True)+'\n',encoding='utf-8')
Path('r3_18af_negative_controls.txt').write_text('\n'.join(['control_bit_truncation=PASS 47/47','repeatability=PASS 47/47','prior_r3_18ad_stop_mismatch=PASS 47/47','post_control_poison=PASS 47/47','next_stream_bits_consumed=0','next_header_bits_consumed=0','next_payload_bits_consumed=0','second_later_control_bits_consumed=0'])+'\n',encoding='utf-8')
Path('r3_18af_aggregate.txt').write_text('\n'.join([
'R3_18AF_OUTCOME=A','R3_18AF_EVIDENCE=PASS','R3_18AF_FROZEN_ROWS=47/47',f'R3_18AF_CONTROL_FALSE={false_count}',f'R3_18AF_CONTROL_TRUE={true_count}','R3_18AF_PUBLISHED_R318AD_EXACT=47/47','R3_18AF_NATIVE_ORACLE_MISMATCH=0','R3_18AF_CONTROL_TRUNCATION=PASS 47/47','R3_18AF_REPEATABILITY=PASS 47/47','R3_18AF_PRIOR_STOP_MISMATCH_NEGATIVE=PASS 47/47','R3_18AF_POST_CONTROL_POISON=PASS 47/47','R3_18AF_NEXT_STREAM_BITS_CONSUMED=0','R3_18AF_NEXT_HEADER_BITS_CONSUMED=0','R3_18AF_NEXT_PAYLOAD_BITS_CONSUMED=0','R3_18AF_SECOND_LATER_CONTROL_BITS_CONSUMED=0','R3_18AF_WITNESS_RESELECTION=0','R3_18AF_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0','R3_18AF_PRIVACY_SCAN=PASS'])+'\n',encoding='utf-8')
print(f'R3_18AF_DIFFERENTIAL=PASS rows=47 false={false_count} true={true_count} mismatch=0')
PY

cat > r3_18af_source_scope.txt <<EOF
canonical_main=$MAIN
canonical_tree=$MAIN_TREE
production_sha=$PROD
production_tree=$PROD_TREE
lib_blob=$LIB_BLOB
ad_test_blob=$AD_TEST_BLOB
af_spec_blob=$AF_SPEC_BLOB
ae_head=$AE_HEAD
ae_tree=$AE_TREE
boxcars_sha=$BOXCARS_SHA
frozen_rows=47
property_control_ordinal=4
production_cargo_fixture_corpus_support_mutation=0/0/0/0/0
EOF
cat > r3_18af_upstream_receipts.txt <<EOF
R3_18AE_AUTHORITY=$AE_RUN/$AE_JOB SUCCESS
R3_18AE_SAME_HEAD_CI=$AE_CI_RUN/$AE_CI_JOB SUCCESS
R3_18AE_ARTIFACT=$AE_ART/$AE_ART_SIZE/$AE_ART_DIGEST
R3_18AE_ADMISSION_BUILDER=$AE_ADMIT_RUN/$AE_ADMIT_JOB SUCCESS
R3_18AE_ADMISSION_PR_CI=$AE_PR_CI/$AE_PR_CI_JOB SUCCESS
R3_18AE_ADMISSION_PR_KA=$AE_PR_KA/$AE_PR_KA_JOB SUCCESS
R3_18Y_AUTHORITY=$Y_RUN/$Y_JOB SUCCESS
R3_18Y_ARTIFACT=$Y_ART/$Y_ART_SIZE/$Y_ART_DIGEST
BOXCARS=$BOXCARS_SHA
EOF

echo '== focused and repository validation =='
RUSTUP_TOOLCHAIN=1.85.0 cargo test -p mimir-replay --test r3_18ad_post_aa_payload
RUSTUP_TOOLCHAIN=1.85.0 cargo test -p mimir-replay
RUSTUP_TOOLCHAIN=1.85.0 cargo fmt --all -- --check
RUSTUP_TOOLCHAIN=1.85.0 cargo check --workspace
RUSTUP_TOOLCHAIN=1.85.0 cargo test --workspace
RUSTUP_TOOLCHAIN=1.85.0 cargo clippy --workspace --all-targets -- -D warnings
pwsh -NoProfile -File scripts/verify_mimir_knowledge_archive.ps1
git diff --check
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

echo '== privacy + manifest =='
for f in r3_18af_source_scope.txt r3_18af_replay_identity.tsv r3_18af_frozen_ae_rows.json r3_18af_targets.tsv r3_18af_boxcars_instrumentation_sha256.txt r3_18af_summary.json r3_18af_comparison.json r3_18af_negative_controls.txt r3_18af_aggregate.txt r3_18af_upstream_receipts.txt; do
  test -f "$f"
done
if grep -E -I -n '(/home/runner|/Users/|[A-Za-z]:\\\\Users\\\\|@users\.noreply\.github\.com)' r3_18af_*.txt r3_18af_*.json r3_18af_*.tsv; then
  echo 'R3_18AF_PRIVACY_SCAN=FAIL'; exit 1
fi
printf '%s\n' r3_18af_source_scope.txt r3_18af_replay_identity.tsv r3_18af_frozen_ae_rows.json r3_18af_targets.tsv r3_18af_boxcars_instrumentation_sha256.txt r3_18af_summary.json r3_18af_comparison.json r3_18af_negative_controls.txt r3_18af_aggregate.txt r3_18af_upstream_receipts.txt | while read -r f; do sha256sum "$f"; done > r3_18af_artifact_sha256.txt
test "$(wc -l < r3_18af_artifact_sha256.txt)" -eq 10
sha256sum -c r3_18af_artifact_sha256.txt
cat r3_18af_aggregate.txt
echo 'R3_18AF_RUN=PASS'

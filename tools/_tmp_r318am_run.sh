#!/usr/bin/env bash
set -euo pipefail

BASE='fec9dca3cb8366108245788fc9a2b24a0c99fe94'
BASE_TREE='3bf5f68ec7df5565f78f89fd4bc2254f2a64e010'
PROD='f20f529e3ada6e9a671ea91e5676a17a00770145'
PROD_TREE='98c675811cca4e4d7f0122c762f371548c9266c2'
LIB_BLOB='a4001e631b306ba0297fb8a4abc97778f81659c2'
AK_TEST_BLOB='9014505e1736498ee5e2ef7a1ce6118030580202'
AL_DECISION_BLOB='fd4ca5f8aad98a4fe9374432d2dae5cede8e5f26'
AM_SPEC_BLOB='eeef347fd3b5eb163a21575b38ef1c7448fc550e'

AL_HEAD='06b8570a25a989651fc800a4ded900ce5e2f3dbe'
AL_TREE='2753baa23be49a819cfceb333977473864a1b02b'
AL_RUN='32469442033'
AL_JOB='96732952709'
AL_CI='32470066272'
AL_CI_JOB='96734795022'
AL_ART='9442034802'
AL_ART_NAME='r318al-published-ak-differential-evidence'
AL_SIZE='14650'
AL_DIGEST='sha256:5fcb8f796ba365193698d5d27e2e7dc0e8c221dd42d7a901e956522b7ca1f639'
AL_PROBE_BLOB='344f638d19317d54a1a2fdccf34e0d68c95c86e2'

AI_HEAD='9d424dae2ed8cc7a0a6868111805a48763131196'
AI_EXTEND_BLOB='467283224dfa51404f0819208149f963f24d8810'
R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318am"
AL_DIR="$WORK/al"
BOXCARS="$WORK/boxcars"
rm -rf "$WORK"
mkdir -p "$AL_DIR"
trap 'rm -rf "$WORK"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318am_probe.rs"' EXIT
norm_digest(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

download_al(){
  for attempt in 1 2 3; do
    rm -rf "$AL_DIR"; mkdir -p "$AL_DIR"
    if gh run download "$AL_RUN" -n "$AL_ART_NAME" -D "$AL_DIR"; then
      echo "R3_18AM_AL_DOWNLOAD_ATTEMPT=$attempt"
      return 0
    fi
    sleep $((attempt*10))
  done
  return 1
}

wait_for_base_validation(){
  for attempt in $(seq 1 60); do
    json="$(gh api -X GET "repos/$GITHUB_REPOSITORY/actions/runs?head_sha=$BASE&event=push&per_page=100")"
    ci="$(printf '%s' "$json" | jq -r '[.workflow_runs[] | select(.name=="CI" and .conclusion=="success")] | length')"
    ka="$(printf '%s' "$json" | jq -r '[.workflow_runs[] | select(.name=="Knowledge Archive Verification" and .conclusion=="success")] | length')"
    if [[ "$ci" -ge 1 && "$ka" -ge 1 ]]; then
      printf '%s' "$json" > "$WORK/base_runs.json"
      echo "R3_18AM_PUBLISHED_PARENT_VALIDATION=PASS ci=$ci knowledge_archive=$ka"
      return 0
    fi
    sleep 10
  done
  echo 'R3.18AM: published parent validation did not become successful' >&2
  return 1
}

echo '== R3.18AM exact authority freeze =='
git fetch origin main evidence/r318c-loop-control "$AL_HEAD" "$AI_HEAD" --force
test "$(git rev-parse origin/main)" = "$BASE"
test "$(git rev-parse origin/main^{tree})" = "$BASE_TREE"
test "$(git merge-base "$BASE" HEAD)" = "$BASE"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$BASE:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$BASE:crates/mimir-replay/tests/r3_18ak_post_ag_following_header.rs")" = "$AK_TEST_BLOB"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AL_DECISION.md")" = "$AL_DECISION_BLOB"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AM_EXECUTION_SPEC.md")" = "$AM_SPEC_BLOB"
test "$(git rev-parse "$AL_HEAD^{tree}")" = "$AL_TREE"
test "$(git rev-parse "$AL_HEAD:tools/_tmp_r318al_native_probe.rs")" = "$AL_PROBE_BLOB"
test "$(git rev-parse "$AI_HEAD:tools/_tmp_r318ai_extend_boxcars.py")" = "$AI_EXTEND_BLOB"
test "$(git rev-parse "$R318C_HEAD:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"

mapfile -t prod_drift < <(git diff --name-only "$PROD" "$BASE" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0
wait_for_base_validation
for pair in "$AL_RUN:$AL_JOB" "$AL_CI:$AL_CI_JOB"; do
  run="${pair%%:*}"; job="${pair##*:}"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AL_RUN" --jq .head_sha)" = "$AL_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AL_RUN" --jq .head_commit.tree_id)" = "$AL_TREE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AL_ART" --jq .workflow_run.id)" = "$AL_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AL_ART" --jq .workflow_run.head_sha)" = "$AL_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AL_ART" --jq .name)" = "$AL_ART_NAME"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AL_ART" --jq .size_in_bytes)" = "$AL_SIZE"
test "$(norm_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AL_ART" --jq .digest)")" = "$(norm_digest "$AL_DIGEST")"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AL_ART" --jq .expired)" = false
echo 'R3_18AM_AUTHORITY_FREEZE=PASS'

echo '== immutable R3.18AL lane =='
download_al
(
  cd "$AL_DIR"
  test "$(wc -l < r3_18al_artifact_sha256.txt)" -eq 10
  sha256sum -c r3_18al_artifact_sha256.txt
  grep -Fqx 'R3_18AL_OUTCOME=A' r3_18al_aggregate.txt
  grep -Fqx 'R3_18AL_FROZEN_ROWS=47/47' r3_18al_aggregate.txt
  grep -Fqx 'R3_18AL_PUBLISHED_AK_EXACT=47/47' r3_18al_aggregate.txt
  grep -Fqx 'R3_18AL_TAG_INT=47' r3_18al_aggregate.txt
  grep -Fqx 'R3_18AL_WITNESS_RESELECTION=0' r3_18al_aggregate.txt
  grep -Fqx 'R3_18AL_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' r3_18al_aggregate.txt
  grep -Fqx 'R3_18AL_SECOND_LATER_CONTROL_BITS_CONSUMED=0' r3_18al_aggregate.txt
)
cp "$AL_DIR/r3_18al_replay_identity.tsv" r3_18am_replay_identity.tsv
cp "$AL_DIR/r3_18al_native_rows.tsv" r3_18am_frozen_al_native_rows.tsv

python3 - "$AL_DIR/r3_18al_native_rows.tsv" "$WORK/targets.tsv" "$WORK/oracle_requests.tsv" <<'PY'
from pathlib import Path
import sys
src, target_out, oracle_out = map(Path, sys.argv[1:])
targets=[]; oracle=[]; seen=set()
for line in src.read_text(encoding='utf-8').splitlines():
    if not line.startswith('R3_18AL_NATIVE\t'): continue
    d={}
    for field in line.split('\t')[1:]:
        k,v=field.split('=',1); d[k]=v
    label=d['label']
    assert label not in seen; seen.add(label)
    assert d['tag']=='Int'
    assert d['published_exact']==d['direct_exact']=='1'
    assert d['following_payload_bits_consumed']==d['second_later_control_bits_consumed']=='0'
    fields=[label,d['frame_index'],d['actor_ordinal'],d['actor_context_object_id'],d['first_start'],d['ag_start'],d['ag_stop'],d['stream_start'],d['stream_end'],d['stream_id'],d['stream_bound'],d['prop_bits'],d['property_object'],d['tag'],d['payload_start']]
    targets.append('\t'.join(fields))
    oracle.append('\t'.join([label,d['frame_index'],d['actor_ordinal'],d['actor_context_object_id'],d['ag_start']]))
assert len(targets)==47 and len(seen)==47
Path(target_out).write_text('\n'.join(targets)+'\n',encoding='utf-8',newline='\n')
Path(oracle_out).write_text('\n'.join(oracle)+'\n',encoding='utf-8',newline='\n')
print('R3_18AM_FROZEN_TARGET_DERIVATION=PASS rows=47 reselection=0')
PY

python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18am_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel, expected, status = line.split('\t')
    assert status == 'PASS' and not rel.startswith('/') and '..' not in Path(rel).parts
    assert hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower() == expected.lower(), rel
    rows.append(rel.replace('\\','/'))
assert len(rows)==47 and len(set(rows))==47
print('R3_18AM_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== pinned Boxcars ordinal-4 payload oracle =='
rm -rf "$BOXCARS"
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$WORK/base_patch.py"
python3 - "$WORK/base_patch.py" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
if s.count('    stream_id_bound: i32,\n') != 1: raise SystemExit('stream bound patch shape')
s=s.replace('    stream_id_bound: i32,\n','    stream_id_bound: u32,\n',1)
s=s.replace('R3_18C','R3_18AI').replace('r3_18c','r3_18ai')
needle='                        if r3_18ai_property_ordinal == 1 {\n'
if s.count(needle)!=1: raise SystemExit('ordinal-1 inherited emission shape')
s=s.replace(needle,'                        if false && r3_18ai_property_ordinal == 1 {\n',1)
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18AM_BOXCARS_BASE_DERIVATION=PASS')
PY
python3 "$WORK/base_patch.py" "$BOXCARS"
git show "$AI_HEAD:tools/_tmp_r318ai_extend_boxcars.py" > "$WORK/ai_extend.py"
python3 "$WORK/ai_extend.py" "$BOXCARS"
python3 tools/_tmp_r318am_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18ai_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18ai_probe.rs Cargo.toml > "$WORK/r3_18am_boxcars.patch"
PATCH_SHA="$(sha256sum "$WORK/r3_18am_boxcars.patch" | awk '{print $1}')"
printf '%s  r3_18am_boxcars_payload_instrumentation.patch\n' "$PATCH_SHA" > r3_18am_boxcars_instrumentation_sha256.txt
RUSTUP_TOOLCHAIN=stable cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18ai_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18ai_probe"
test -x "$PROBE"
: > "$WORK/oracle.log"
while IFS=$'\t' read -r rel frame actor actor_object property_start; do
  MIMIR_R3_18AI_LABEL="$rel" \
  MIMIR_R3_18AI_TARGET_FRAME="$frame" \
  MIMIR_R3_18AI_TARGET_ACTOR_ORDINAL="$actor" \
  MIMIR_R3_18AI_TARGET_ACTOR_OBJECT="$actor_object" \
  MIMIR_R3_18AI_TARGET_PROPERTY_START="$property_start" \
  "$PROBE" "$ROOT/$rel" >> "$WORK/oracle.log" 2>&1
done < "$WORK/oracle_requests.tsv"
test "$(grep -c '^R3_18AI_ORACLE_PARSE=PASS$' "$WORK/oracle.log")" -eq 47
test "$(grep -c $'^R3_18AM_ORACLE\t' "$WORK/oracle.log")" -eq 47
grep $'^R3_18AM_ORACLE\t' "$WORK/oracle.log" > r3_18am_oracle_rows.tsv
echo 'R3_18AM_BOXCARS_ORACLE=PASS payloads=47 ordinal=4'

echo '== native published AK + exact one Int payload =='
git show "$AL_HEAD:tools/_tmp_r318al_native_probe.rs" > "$WORK/al_probe.rs"
python3 tools/_tmp_r318am_make_probe.py "$WORK/al_probe.rs" "$WORK/am_probe.rs"
python3 - "$WORK/am_probe.rs" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
s=s.replace(r'\\t', r'\t')
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18AM_PROBE_ESCAPE_NORMALIZATION=PASS')
PY
mkdir -p crates/mimir-replay/examples
cp "$WORK/am_probe.rs" crates/mimir-replay/examples/_tmp_r318am_probe.rs
rustup run 1.85.0 rustfmt --edition 2024 crates/mimir-replay/examples/_tmp_r318am_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318am_probe -- "$WORK/targets.tsv" > "$WORK/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318am_probe -- "$WORK/targets.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
test "$(grep -c $'^R3_18AM_NATIVE\t' "$WORK/native1.log")" -eq 47
grep $'^R3_18AM_NATIVE\t' "$WORK/native1.log" > r3_18am_native_rows.tsv
rm -f crates/mimir-replay/examples/_tmp_r318am_probe.rs

python3 tools/_tmp_r318am_analyze.py \
  "$WORK/oracle.log" "$WORK/native1.log" \
  r3_18am_payload_rows.json r3_18am_summary.json \
  r3_18am_negative_controls.txt r3_18am_aggregate.txt

echo '== focused and repository regressions =='
cargo +1.85.0 test -p mimir-replay --test r3_18ak_post_ag_following_header --quiet
cargo +1.85.0 test -p mimir-replay --quiet
pwsh -NoLogo -NoProfile -File ./scripts/verify_repo.ps1

echo '== immutable evidence receipts =='
cat > r3_18am_upstream_receipts.txt <<EOF
R3_18AM_BASE_MAIN=$BASE
R3_18AM_BASE_TREE=$BASE_TREE
R3_18AM_PRODUCTION=$PROD
R3_18AM_PRODUCTION_TREE=$PROD_TREE
R3_18AM_AL_HEAD=$AL_HEAD
R3_18AM_AL_TREE=$AL_TREE
R3_18AM_AL_AUTHORITY=$AL_RUN/$AL_JOB
R3_18AM_AL_CI=$AL_CI/$AL_CI_JOB
R3_18AM_AL_ARTIFACT=$AL_ART/$AL_SIZE/$AL_DIGEST
R3_18AM_BOXCARS=$BOXCARS_SHA
EOF
cat > r3_18am_source_scope.txt <<EOF
R3_18AM_BASE_MAIN=$BASE
R3_18AM_EVIDENCE_HEAD=$(git rev-parse HEAD)
R3_18AM_LIB_BLOB=$LIB_BLOB
R3_18AM_AK_TEST_BLOB=$AK_TEST_BLOB
R3_18AM_PRODUCTION_MUTATION=0
R3_18AM_CARGO_MUTATION=0
R3_18AM_FIXTURE_MUTATION=0
R3_18AM_CORPUS_MUTATION=0
R3_18AM_SUPPORT_MUTATION=0
R3_18AM_WITNESS_RESELECTION=0
R3_18AM_EARLIER_PAYLOAD_CONTRACT_INHERITANCE=0
EOF

python3 - <<'PY'
from pathlib import Path
bad=[]
for p in Path('.').glob('r3_18am_*'):
    if not p.is_file(): continue
    text=p.read_text(encoding='utf-8',errors='replace')
    for needle in ['/home/runner','C:\\Users\\','@users.noreply.github.com','GH_TOKEN','github_pat_']:
        if needle in text: bad.append((str(p),needle))
if bad: raise SystemExit(f'privacy failure: {bad}')
print('R3_18AM_PRIVACY_SCAN=PASS')
PY

grep -Fqx 'R3_18AM_OUTCOME=A' r3_18am_aggregate.txt
grep -Fqx 'R3_18AM_FROZEN_ROWS=47/47' r3_18am_aggregate.txt
grep -Fqx 'R3_18AM_PUBLISHED_AK_EXACT=47/47' r3_18am_aggregate.txt
grep -Fqx 'R3_18AM_TAG_INT=47' r3_18am_aggregate.txt
grep -Fqx 'R3_18AM_NATIVE_ORACLE_MISMATCH=0' r3_18am_aggregate.txt
grep -Fqx 'R3_18AM_WITNESS_RESELECTION=0' r3_18am_aggregate.txt
grep -Fqx 'R3_18AM_ANOTHER_CONTROL_BITS_CONSUMED=0' r3_18am_aggregate.txt

sha256sum \
  r3_18am_native_rows.tsv \
  r3_18am_oracle_rows.tsv \
  r3_18am_payload_rows.json \
  r3_18am_summary.json \
  r3_18am_replay_identity.tsv \
  r3_18am_frozen_al_native_rows.tsv \
  r3_18am_source_scope.txt \
  r3_18am_upstream_receipts.txt \
  r3_18am_negative_controls.txt \
  r3_18am_aggregate.txt \
  r3_18am_boxcars_instrumentation_sha256.txt \
  > r3_18am_artifact_sha256.txt

echo 'R3_18AM_EVIDENCE_RUN=PASS'

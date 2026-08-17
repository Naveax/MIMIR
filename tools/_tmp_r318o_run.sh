#!/usr/bin/env bash
set -euo pipefail

MAIN='c1d68daf989952ccf40645ca99616bccf43bb2f4'
MAIN_TREE='157dc109cf35e6be153d9675855163033e7e56fa'
PROD='fd74ba8c520ab83b808730572c41e45d6dc616e6'
PROD_TREE='6285928b3ca724c77b761e70c54f7bd0763f11f0'
LIB_BLOB='029c48e38ea0257f8cdb3fa8715bde5a789213e7'
M_TEST_BLOB='a9bd2d0a8007c8cae76a0d14ad0c11ed387fe5a6'
N_DECISION_BLOB='5a7b42a43e80d0e9119f1b06b3a2438cd541fdf9'
O_SPEC_BLOB='cb3bbd58ea83454c28c1f30c929998ff3eeda254'

N_HEAD='9bbf59745c950b7be5a5a592724f41db80874973'
N_RUN='32007040663'
N_JOB='95318554719'
N_CI_RUN='32007040500'
N_CI_JOB='95318554225'
N_ARTIFACT_ID='9280430420'
N_ARTIFACT_NAME='r318n-published-following-control-evidence'
N_ARTIFACT_DIGEST='772447a31e174355b3848605357667936ca522777d601dda504896aa0f663102'
N_ARTIFACT_SIZE='21060'

N_SOURCE_SCOPE_SHA='9736e79a375f40af4e46d82356806cfe85bb8e2d3b7007920d824ded7bed2501'
N_REPLAY_ID_SHA='b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf'
N_WITNESS_SHA='99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7'
N_L_AUTH_SHA='ec2327ad969ce26771b4c54b1c0ae3d3de4808283895f0c99ce4166f16c832b0'
N_SUMMARY_SHA='73873b4426b636ae17fc176b42ad2f3775de62dead57f95fe8bad4a1697c4138'
N_TARGETS_SHA='73afd57f43a2656c5d98f6c97b4c24015283c688a1e343494139ea3ba16d8950'
N_CONTROL_ROWS_SHA='c2bcd2fc059e2a440d39b3cc33482ff24b897e504de8cbf9ae8666136ccf91e0'
N_NEGATIVES_SHA='8961610cb0cb3b01dbab126634560abb168d128d1365856eebf90a773b544554'
N_AGGREGATE_SHA='be0ec06f766580b43ce1c4ba411baf140b5392d1b591409e31b71a06b7f8d444'
N_MANIFEST_SHA='e8a579407b0d2eebd383151859b19a92b2b2fae706841b8c355d509d3afb68d9'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318o"
N_DIR="$WORK/r318n"
BOXCARS="$WORK/boxcars"
rm -rf "$WORK"
mkdir -p "$N_DIR"

cleanup() {
  rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318o_probe.rs"
}
trap cleanup EXIT

check_sha() {
  local expected="$1"
  local file="$2"
  test "$(sha256sum "$file" | awk '{print $1}')" = "$expected"
}

echo '== R3.18O authority freeze =='
git fetch origin main evidence/r318c-loop-control --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
git merge-base --is-ancestor "$MAIN" HEAD
test "$(git merge-base "$MAIN" HEAD)" = "$MAIN"
test "$(git rev-parse "${PROD}^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${PROD}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/tests/r3_18m_following_control.rs")" = "$M_TEST_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18N_DECISION.md")" = "$N_DECISION_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18O_EXECUTION_SPEC.md")" = "$O_SPEC_BLOB"
test "$(git rev-parse origin/evidence/r318c-loop-control)" = "$R318C_HEAD"
test "$(git rev-parse "${R318C_HEAD}:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"

mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318o_evidence.yml'
  'tools/_tmp_r318o_extend_boxcars.py'
  'tools/_tmp_r318o_native_probe.rs'
  'tools/_tmp_r318o_prepare.py'
  'tools/_tmp_r318o_run.sh'
)
mapfile -t expected_sorted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 5
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${expected_sorted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

for run in "$N_RUN" "$N_CI_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$N_JOB" "$N_CI_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$N_RUN" --jq .head_sha)" = "$N_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$N_CI_RUN" --jq .head_sha)" = "$N_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$N_ARTIFACT_ID" --jq .workflow_run.id)" = "$N_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$N_ARTIFACT_ID" --jq .workflow_run.head_sha)" = "$N_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$N_ARTIFACT_ID" --jq .name)" = "$N_ARTIFACT_NAME"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$N_ARTIFACT_ID" --jq .digest)" = "sha256:$N_ARTIFACT_DIGEST"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$N_ARTIFACT_ID" --jq .size_in_bytes)" = "$N_ARTIFACT_SIZE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$N_ARTIFACT_ID" --jq .expired)" = false
echo 'R3_18O_AUTHORITY_FREEZE=PASS'

echo '== R3.18O immutable R3.18N lane =='
gh run download "$N_RUN" -n "$N_ARTIFACT_NAME" -D "$N_DIR"
check_sha "$N_SOURCE_SCOPE_SHA" "$N_DIR/r3_18n_source_scope.txt"
check_sha "$N_REPLAY_ID_SHA" "$N_DIR/r3_18n_replay_identity.tsv"
check_sha "$N_WITNESS_SHA" "$N_DIR/r3_18n_frozen_witnesses.json"
check_sha "$N_L_AUTH_SHA" "$N_DIR/r3_18n_r318l_authority_sha256.txt"
check_sha "$N_SUMMARY_SHA" "$N_DIR/r3_18n_source_summary.json"
check_sha "$N_TARGETS_SHA" "$N_DIR/r3_18n_targets.tsv"
check_sha "$N_CONTROL_ROWS_SHA" "$N_DIR/r3_18n_control_rows.json"
check_sha "$N_NEGATIVES_SHA" "$N_DIR/r3_18n_negative_controls.txt"
check_sha "$N_AGGREGATE_SHA" "$N_DIR/r3_18n_aggregate.txt"
check_sha "$N_MANIFEST_SHA" "$N_DIR/r3_18n_artifact_sha256.txt"
grep -Fq 'R3_18N_OUTCOME=A' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_FROZEN_ROWS=47/47' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_CONTROL_FALSE=0' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_CONTROL_TRUE=47' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_PUBLISHED_R318M_ORACLE_MISMATCH=0' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_WITNESS_RESELECTION=0' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_FOLLOWING_STREAM_BITS_CONSUMED=0' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_FOLLOWING_HEADER_BITS_CONSUMED=0' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' "$N_DIR/r3_18n_aggregate.txt"
grep -Fq 'R3_18N_ANOTHER_CONTROL_BITS_CONSUMED=0' "$N_DIR/r3_18n_aggregate.txt"

cp "$N_DIR/r3_18n_replay_identity.tsv" r3_18o_replay_identity.tsv
cp "$N_DIR/r3_18n_frozen_witnesses.json" r3_18o_frozen_witnesses.json
cat > r3_18o_r318n_authority_sha256.txt <<EOF
$N_SOURCE_SCOPE_SHA  r3_18n_source_scope.txt
$N_REPLAY_ID_SHA  r3_18n_replay_identity.tsv
$N_WITNESS_SHA  r3_18n_frozen_witnesses.json
$N_L_AUTH_SHA  r3_18n_r318l_authority_sha256.txt
$N_SUMMARY_SHA  r3_18n_source_summary.json
$N_TARGETS_SHA  r3_18n_targets.tsv
$N_CONTROL_ROWS_SHA  r3_18n_control_rows.json
$N_NEGATIVES_SHA  r3_18n_negative_controls.txt
$N_AGGREGATE_SHA  r3_18n_aggregate.txt
$N_MANIFEST_SHA  r3_18n_artifact_sha256.txt
EOF

python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18o_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    rel, expected, status = line.split('\t')
    if status != 'PASS':
        raise SystemExit(f'bad identity status: {rel}')
    if hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower() != expected.lower():
        raise SystemExit(f'replay identity drift: {rel}')
    rows.append(rel.replace('\\','/'))
if len(rows) != 47 or len(set(rows)) != 47:
    raise SystemExit('R3.18O replay lane is not exactly 47 unique identities')
print('R3_18O_REPLAY_IDENTITY=PASS rows=47')
PY

python3 tools/_tmp_r318o_prepare.py oracle-requests \
  "$N_DIR/r3_18n_targets.tsv" \
  "$N_DIR/r3_18n_control_rows.json" \
  "$WORK/oracle_requests.tsv"
echo 'R3_18O_WITNESS_RESELECTION=PASS count=0'

echo '== R3.18O pinned Boxcars following-header oracle =='
rm -rf "$BOXCARS"
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$WORK/boxcars_base_patch.py"
python3 - "$WORK/boxcars_base_patch.py" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')
if s.count('    stream_id_bound: i32,\n') != 1:
    raise SystemExit('unexpected inherited stream_id_bound patcher shape')
s=s.replace('    stream_id_bound: i32,\n','    stream_id_bound: u32,\n',1)
s=s.replace('R3_18C','R3_18O').replace('r3_18c','r3_18o')
needle='                        if r3_18o_property_ordinal == 1 {\n'
if s.count(needle) != 1:
    raise SystemExit('unexpected inherited ordinal-1 emission shape')
s=s.replace(needle,'                        if false && r3_18o_property_ordinal == 1 {\n',1)
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18O_BOXCARS_BASE_PATCH_DERIVATION=PASS')
PY
python3 "$WORK/boxcars_base_patch.py" "$BOXCARS"
python3 tools/_tmp_r318o_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18o_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18o_probe.rs Cargo.toml > "$WORK/r3_18o_boxcars_instrumentation.patch"
sha256sum "$WORK/r3_18o_boxcars_instrumentation.patch" > r3_18o_boxcars_instrumentation_sha256.txt
cargo +stable check --manifest-path "$BOXCARS/Cargo.toml" --example r3_18o_probe
cargo +stable build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18o_probe --quiet
echo 'R3_18O_BOXCARS_BUILD=PASS'

PROBE="$BOXCARS/target/debug/examples/r3_18o_probe"
test -x "$PROBE"
: > "$WORK/oracle.log"
while IFS=$'\t' read -r rel frame actor_ordinal actor_object property_start; do
  test -n "$rel"
  MIMIR_R3_18O_LABEL="$rel" \
  MIMIR_R3_18O_TARGET_FRAME="$frame" \
  MIMIR_R3_18O_TARGET_ACTOR_ORDINAL="$actor_ordinal" \
  MIMIR_R3_18O_TARGET_ACTOR_OBJECT="$actor_object" \
  MIMIR_R3_18O_TARGET_PROPERTY_START="$property_start" \
    "$PROBE" "$PWD/$rel" >> "$WORK/oracle.log" 2>&1
done < "$WORK/oracle_requests.tsv"
test "$(grep -c '^R3_18O_ORACLE_PARSE=PASS$' "$WORK/oracle.log")" -eq 47
test "$(grep -c $'^R3_18O_HEADER\t' "$WORK/oracle.log")" -eq 47
python3 tools/_tmp_r318o_prepare.py build \
  "$N_DIR/r3_18n_targets.tsv" \
  "$N_DIR/r3_18n_control_rows.json" \
  "$WORK/oracle.log" \
  r3_18o_targets.tsv \
  r3_18o_oracle_header_rows.json \
  r3_18o_source_summary.json
echo 'R3_18O_ORACLE_SCAN=PASS exact_target_headers=47'

echo '== R3.18O published native header differential =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318o_native_probe.rs crates/mimir-replay/examples/_tmp_r318o_probe.rs
cargo +1.85.0 build --locked -p mimir-replay --example _tmp_r318o_probe
./target/debug/examples/_tmp_r318o_probe r3_18o_targets.tsv | tee "$WORK/native1.log"
./target/debug/examples/_tmp_r318o_probe r3_18o_targets.tsv > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
rm -f crates/mimir-replay/examples/_tmp_r318o_probe.rs

python3 tools/_tmp_r318o_prepare.py analyze \
  r3_18o_targets.tsv \
  "$WORK/native1.log" \
  r3_18o_header_rows.json \
  r3_18o_negative_controls.txt \
  r3_18o_aggregate.txt

cat > r3_18o_source_scope.txt <<EOF
R3_18O_BASE_MAIN=$MAIN
R3_18O_BASE_TREE=$MAIN_TREE
R3_18O_EVIDENCE_HEAD=$(git rev-parse HEAD)
R3_18O_PRODUCTION_SHA=$PROD
R3_18O_PRODUCTION_TREE=$PROD_TREE
R3_18O_PRODUCTION_LIB_BLOB=$LIB_BLOB
R3_18O_R318M_TEST_BLOB=$M_TEST_BLOB
R3_18O_R318N_DECISION_BLOB=$N_DECISION_BLOB
R3_18O_SPEC_BLOB=$O_SPEC_BLOB
R3_18O_R318N_HEAD=$N_HEAD
R3_18O_R318N_RUN_JOB=$N_RUN/$N_JOB
R3_18O_R318N_CI_RUN_JOB=$N_CI_RUN/$N_CI_JOB
R3_18O_R318N_ARTIFACT=$N_ARTIFACT_ID
R3_18O_R318N_ARTIFACT_DIGEST=sha256:$N_ARTIFACT_DIGEST
R3_18O_R318N_ARTIFACT_SIZE=$N_ARTIFACT_SIZE
R3_18O_BOXCARS_SHA=$BOXCARS_SHA
R3_18O_CHANGED_TEMP_FILES=5
R3_18O_WITNESS_RESELECTION=0
R3_18O_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF

echo '== R3.18O regression and full repository validation =='
cargo +1.85.0 fmt --all -- --check
cargo +1.85.0 test --locked -p mimir-replay --test r3_18m_following_control -- --nocapture
cargo +1.85.0 test --locked -p mimir-replay -- --nocapture
cargo +1.85.0 check --locked --workspace --all-targets --all-features
cargo +1.85.0 test --locked --workspace
cargo +1.85.0 clippy --locked --workspace --all-targets --all-features -- -D warnings
pwsh -NoProfile -File scripts/verify_repo.ps1

git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
test ! -e crates/mimir-replay/examples/_tmp_r318o_probe.rs

echo '== R3.18O privacy and artifact manifest =='
if grep -R -n -E 'window_hex=|window_hex"|content_hex|semantic_i32=|semantic_fnv64=|account_id|platform_id' \
  r3_18o_source_scope.txt r3_18o_replay_identity.tsv r3_18o_frozen_witnesses.json \
  r3_18o_r318n_authority_sha256.txt r3_18o_boxcars_instrumentation_sha256.txt \
  r3_18o_source_summary.json r3_18o_targets.tsv r3_18o_oracle_header_rows.json \
  r3_18o_header_rows.json r3_18o_negative_controls.txt r3_18o_aggregate.txt; then
  echo 'privacy-sensitive evidence marker found'
  exit 1
fi

grep -Fq 'R3_18O_OUTCOME=A' r3_18o_aggregate.txt
grep -Fq 'R3_18O_FROZEN_ROWS=47/47' r3_18o_aggregate.txt
grep -Fq 'R3_18O_WITNESS_RESELECTION=0' r3_18o_aggregate.txt
grep -Fq 'R3_18O_FOLLOWING_HEADER_EXACT=47/47' r3_18o_aggregate.txt
grep -Fq 'R3_18O_NATIVE_ORACLE_MISMATCH=0' r3_18o_aggregate.txt
grep -Fq 'R3_18O_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' r3_18o_aggregate.txt
grep -Fq 'R3_18O_ANOTHER_CONTROL_BITS_CONSUMED=0' r3_18o_aggregate.txt
grep -Fq 'R3_18O_PRIVACY=PASS' r3_18o_aggregate.txt

for file in \
  r3_18o_source_scope.txt \
  r3_18o_replay_identity.tsv \
  r3_18o_frozen_witnesses.json \
  r3_18o_r318n_authority_sha256.txt \
  r3_18o_boxcars_instrumentation_sha256.txt \
  r3_18o_source_summary.json \
  r3_18o_targets.tsv \
  r3_18o_oracle_header_rows.json \
  r3_18o_header_rows.json \
  r3_18o_negative_controls.txt \
  r3_18o_aggregate.txt
do
  sha256sum "$file"
done > r3_18o_artifact_sha256.txt

echo 'R3_18O_EVIDENCE=PASS'

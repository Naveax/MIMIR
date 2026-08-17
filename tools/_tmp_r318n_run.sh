#!/usr/bin/env bash
set -euo pipefail

MAIN='1992ec94ab6a368e4143aad403ad6a223e3d3e5a'
MAIN_TREE='313563ebd483112ae9976d3becb93bab8402031d'
PROD='fd74ba8c520ab83b808730572c41e45d6dc616e6'
PROD_TREE='6285928b3ca724c77b761e70c54f7bd0763f11f0'
LIB_BLOB='029c48e38ea0257f8cdb3fa8715bde5a789213e7'
M_TEST_BLOB='a9bd2d0a8007c8cae76a0d14ad0c11ed387fe5a6'
M_DECISION_BLOB='5bfc03299f4a8840b236df690e19432f06e74443'
N_SPEC_BLOB='97ee7bf02bdd4153b29bfbc582d5b9e696e0db0f'

M_IMPL_HEAD='46d96c830e4d311a8a46bf6ae153f7e603d4eb15'
M_IMPL_RUN='31999687944'
M_IMPL_JOB='95297550306'
M_CAND_RUN='31999898754'
M_CAND_JOB='95298116788'
M_PUB_RUN='32000211020'
M_PUB_JOB='95298954375'

L_HEAD='9205ac1616e686589938f952782a32f03d0d1488'
L_RUN='31978791346'
L_JOB='95242213413'
L_CI_RUN='31978791304'
L_CI_JOB='95242213357'
L_ARTIFACT_ID='9271817700'
L_ARTIFACT_NAME='r318l-following-property-control-evidence'
L_ARTIFACT_DIGEST='db5d2db96429a4f2b699dca5176fc4d218f9eb9e4faa8dee813b766896f70c1c'
L_ARTIFACT_SIZE='20906'
L_DECISION_BLOB='8dd1c8860e5d733fd286e7173d623a5804d3a3c9'

L_SOURCE_SCOPE_SHA='7cbfc2e36b116ba9aac9f3daee29e7652a723e5ceb96a96e270118151e16fd7b'
L_REPLAY_ID_SHA='b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf'
L_WITNESS_SHA='99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7'
L_K_AUTH_SHA='0fc4681b94749991a226a07af58709d0074bde3ecf4eae67575512a242f44f99'
L_SUMMARY_SHA='107778cbfc4971ad883c53d4dd8e33d5bd0ebe5a1aadb054b42b83810cb1ca4f'
L_TARGETS_SHA='73afd57f43a2656c5d98f6c97b4c24015283c688a1e343494139ea3ba16d8950'
L_BOXCARS_SHA='e607f40bdffe9a9a6df2a3546f33a22811624b6efc5ba073a2b954dd84ecb4cf'
L_CONTROL_ROWS_SHA='f94693fe6ae4babe7fc951013de16fc32c0279e40f1d4957943776d3f3d81381'
L_NEGATIVES_SHA='f30d66d3b6e5fca1525dc01d1154179cadee58747fdb5bf4dbfdaeb4bd4b59c3'
L_AGGREGATE_SHA='ad1d3b129e34a97f46d0bc3ea879a723e3e46e8d7624e2c9eb8945800b15ee19'
L_MANIFEST_SHA='28f4df430ef84149cdd33a1efc7124fb232d69abd3cb94e6d2196957268985c8'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318n"
L_DIR="$WORK/r318l"
rm -rf "$WORK"
mkdir -p "$L_DIR"

cleanup() {
  rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318n_probe.rs"
}
trap cleanup EXIT

check_sha() {
  local expected="$1"
  local file="$2"
  test "$(sha256sum "$file" | awk '{print $1}')" = "$expected"
}

echo '== R3.18N authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git rev-parse HEAD^)" = "$MAIN"
test "$(git rev-parse "${PROD}^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${PROD}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/tests/r3_18m_following_control.rs")" = "$M_TEST_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18M_DECISION.md")" = "$M_DECISION_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18N_EXECUTION_SPEC.md")" = "$N_SPEC_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18L_DECISION.md")" = "$L_DECISION_BLOB"

mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318n_evidence.yml'
  'tools/_tmp_r318n_native_probe.rs'
  'tools/_tmp_r318n_prepare.py'
  'tools/_tmp_r318n_run.sh'
)
mapfile -t expected_sorted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 4
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${expected_sorted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

for run in "$M_IMPL_RUN" "$M_CAND_RUN" "$M_PUB_RUN" "$L_RUN" "$L_CI_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$M_IMPL_JOB" "$M_CAND_JOB" "$M_PUB_JOB" "$L_JOB" "$L_CI_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$M_IMPL_RUN" --jq .head_sha)" = "$M_IMPL_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$M_CAND_RUN" --jq .head_sha)" = "$PROD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$M_PUB_RUN" --jq .head_sha)" = "$PROD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$L_RUN" --jq .head_sha)" = "$L_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$L_CI_RUN" --jq .head_sha)" = "$L_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$L_ARTIFACT_ID" --jq .workflow_run.id)" = "$L_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$L_ARTIFACT_ID" --jq .workflow_run.head_sha)" = "$L_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$L_ARTIFACT_ID" --jq .name)" = "$L_ARTIFACT_NAME"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$L_ARTIFACT_ID" --jq .digest)" = "sha256:$L_ARTIFACT_DIGEST"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$L_ARTIFACT_ID" --jq .size_in_bytes)" = "$L_ARTIFACT_SIZE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$L_ARTIFACT_ID" --jq .expired)" = false
echo 'R3_18N_AUTHORITY_FREEZE=PASS'

echo '== R3.18N immutable R3.18L lane =='
gh run download "$L_RUN" -n "$L_ARTIFACT_NAME" -D "$L_DIR"
check_sha "$L_SOURCE_SCOPE_SHA" "$L_DIR/r3_18l_source_scope.txt"
check_sha "$L_REPLAY_ID_SHA" "$L_DIR/r3_18l_replay_identity.tsv"
check_sha "$L_WITNESS_SHA" "$L_DIR/r3_18l_frozen_witnesses.json"
check_sha "$L_K_AUTH_SHA" "$L_DIR/r3_18l_r318k_authority_sha256.txt"
check_sha "$L_SUMMARY_SHA" "$L_DIR/r3_18l_source_summary.json"
check_sha "$L_TARGETS_SHA" "$L_DIR/r3_18l_targets.tsv"
check_sha "$L_BOXCARS_SHA" "$L_DIR/r3_18l_boxcars_instrumentation_sha256.txt"
check_sha "$L_CONTROL_ROWS_SHA" "$L_DIR/r3_18l_control_rows.json"
check_sha "$L_NEGATIVES_SHA" "$L_DIR/r3_18l_negative_controls.txt"
check_sha "$L_AGGREGATE_SHA" "$L_DIR/r3_18l_aggregate.txt"
check_sha "$L_MANIFEST_SHA" "$L_DIR/r3_18l_artifact_sha256.txt"
grep -Fq 'R3_18L_OUTCOME=A' "$L_DIR/r3_18l_aggregate.txt"
grep -Fq 'R3_18L_FROZEN_ROWS=47/47' "$L_DIR/r3_18l_aggregate.txt"
grep -Fq 'R3_18L_CONTROL_FALSE=0' "$L_DIR/r3_18l_aggregate.txt"
grep -Fq 'R3_18L_CONTROL_TRUE=47' "$L_DIR/r3_18l_aggregate.txt"
grep -Fq 'R3_18L_NATIVE_ORACLE_MISMATCH=0' "$L_DIR/r3_18l_aggregate.txt"
grep -Fq 'R3_18L_FOLLOWING_STREAM_BITS_CONSUMED=0' "$L_DIR/r3_18l_aggregate.txt"
grep -Fq 'R3_18L_FOLLOWING_HEADER_BITS_CONSUMED=0' "$L_DIR/r3_18l_aggregate.txt"
grep -Fq 'R3_18L_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' "$L_DIR/r3_18l_aggregate.txt"
grep -Fq 'R3_18L_WITNESS_RESELECTION=0' "$L_DIR/r3_18l_aggregate.txt"

cp "$L_DIR/r3_18l_replay_identity.tsv" r3_18n_replay_identity.tsv
cp "$L_DIR/r3_18l_frozen_witnesses.json" r3_18n_frozen_witnesses.json
cat > r3_18n_r318l_authority_sha256.txt <<EOF
$L_SOURCE_SCOPE_SHA  r3_18l_source_scope.txt
$L_REPLAY_ID_SHA  r3_18l_replay_identity.tsv
$L_WITNESS_SHA  r3_18l_frozen_witnesses.json
$L_K_AUTH_SHA  r3_18l_r318k_authority_sha256.txt
$L_SUMMARY_SHA  r3_18l_source_summary.json
$L_TARGETS_SHA  r3_18l_targets.tsv
$L_BOXCARS_SHA  r3_18l_boxcars_instrumentation_sha256.txt
$L_CONTROL_ROWS_SHA  r3_18l_control_rows.json
$L_NEGATIVES_SHA  r3_18l_negative_controls.txt
$L_AGGREGATE_SHA  r3_18l_aggregate.txt
$L_MANIFEST_SHA  r3_18l_artifact_sha256.txt
EOF

python3 - <<'PY'
import hashlib
from pathlib import Path
rows = []
for line in Path('r3_18n_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    rel, expected, status = line.split('\t')
    if status != 'PASS':
        raise SystemExit(f'bad identity status: {rel}')
    if hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower() != expected.lower():
        raise SystemExit(f'replay identity drift: {rel}')
    rows.append(rel.replace('\\', '/'))
if len(rows) != 47 or len(set(rows)) != 47:
    raise SystemExit('R3.18N replay lane is not exactly 47 unique identities')
print('R3_18N_REPLAY_IDENTITY=PASS rows=47')
PY

python3 tools/_tmp_r318n_prepare.py build \
  "$L_DIR/r3_18l_targets.tsv" \
  "$L_DIR/r3_18l_control_rows.json" \
  r3_18n_targets.tsv \
  r3_18n_source_summary.json
cmp r3_18n_targets.tsv "$L_DIR/r3_18l_targets.tsv"
echo 'R3_18N_WITNESS_RESELECTION=PASS count=0'

echo '== R3.18N published R3.18M API differential =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318n_native_probe.rs crates/mimir-replay/examples/_tmp_r318n_probe.rs
cargo build --locked -p mimir-replay --example _tmp_r318n_probe
./target/debug/examples/_tmp_r318n_probe r3_18n_targets.tsv | tee "$WORK/native1.log"
./target/debug/examples/_tmp_r318n_probe r3_18n_targets.tsv > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
rm -f crates/mimir-replay/examples/_tmp_r318n_probe.rs

python3 tools/_tmp_r318n_prepare.py analyze \
  r3_18n_targets.tsv \
  "$L_DIR/r3_18l_control_rows.json" \
  "$WORK/native1.log" \
  r3_18n_control_rows.json \
  r3_18n_negative_controls.txt \
  r3_18n_aggregate.txt

cat > r3_18n_source_scope.txt <<EOF
R3_18N_BASE_MAIN=$MAIN
R3_18N_BASE_TREE=$MAIN_TREE
R3_18N_PRODUCTION_SHA=$PROD
R3_18N_PRODUCTION_TREE=$PROD_TREE
R3_18N_PRODUCTION_LIB_BLOB=$LIB_BLOB
R3_18N_R318M_TEST_BLOB=$M_TEST_BLOB
R3_18N_R318M_DECISION_BLOB=$M_DECISION_BLOB
R3_18N_SPEC_BLOB=$N_SPEC_BLOB
R3_18N_R318M_IMPL_HEAD=$M_IMPL_HEAD
R3_18N_R318M_IMPL_RUN_JOB=$M_IMPL_RUN/$M_IMPL_JOB
R3_18N_R318M_CAND_RUN_JOB=$M_CAND_RUN/$M_CAND_JOB
R3_18N_R318M_PUBLISHED_RUN_JOB=$M_PUB_RUN/$M_PUB_JOB
R3_18N_R318L_HEAD=$L_HEAD
R3_18N_R318L_RUN_JOB=$L_RUN/$L_JOB
R3_18N_R318L_CI_RUN_JOB=$L_CI_RUN/$L_CI_JOB
R3_18N_R318L_ARTIFACT=$L_ARTIFACT_ID
R3_18N_R318L_ARTIFACT_DIGEST=sha256:$L_ARTIFACT_DIGEST
R3_18N_R318L_ARTIFACT_SIZE=$L_ARTIFACT_SIZE
R3_18N_CHANGED_TEMP_FILES=4
R3_18N_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF

echo '== R3.18N regression and full repository validation =='
cargo fmt --all -- --check
cargo test --locked -p mimir-replay --test r3_18m_following_control -- --nocapture
cargo test --locked -p mimir-replay -- --nocapture
cargo check --locked --workspace --all-targets --all-features
cargo test --locked --workspace
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings
pwsh -NoProfile -File scripts/verify_repo.ps1

git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
test ! -e crates/mimir-replay/examples/_tmp_r318n_probe.rs

echo '== R3.18N privacy and artifact manifest =='
if grep -R -n -E 'window_hex=|window_hex"|content_hex|semantic_i32=|semantic_fnv64=' \
  r3_18n_source_scope.txt r3_18n_replay_identity.tsv r3_18n_frozen_witnesses.json \
  r3_18n_r318l_authority_sha256.txt r3_18n_source_summary.json r3_18n_targets.tsv \
  r3_18n_control_rows.json r3_18n_negative_controls.txt r3_18n_aggregate.txt; then
  echo 'privacy-sensitive evidence marker found'
  exit 1
fi

grep -Fq 'R3_18N_OUTCOME=A' r3_18n_aggregate.txt
grep -Fq 'R3_18N_FROZEN_ROWS=47/47' r3_18n_aggregate.txt
grep -Fq 'R3_18N_CONTROL_FALSE=0' r3_18n_aggregate.txt
grep -Fq 'R3_18N_CONTROL_TRUE=47' r3_18n_aggregate.txt
grep -Fq 'R3_18N_PUBLISHED_R318M_ORACLE_MISMATCH=0' r3_18n_aggregate.txt
grep -Fq 'R3_18N_FOLLOWING_STREAM_BITS_CONSUMED=0' r3_18n_aggregate.txt
grep -Fq 'R3_18N_FOLLOWING_HEADER_BITS_CONSUMED=0' r3_18n_aggregate.txt
grep -Fq 'R3_18N_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' r3_18n_aggregate.txt
grep -Fq 'R3_18N_ANOTHER_CONTROL_BITS_CONSUMED=0' r3_18n_aggregate.txt
grep -Fq 'R3_18N_PRIVACY=PASS' r3_18n_aggregate.txt

for file in \
  r3_18n_source_scope.txt \
  r3_18n_replay_identity.tsv \
  r3_18n_frozen_witnesses.json \
  r3_18n_r318l_authority_sha256.txt \
  r3_18n_source_summary.json \
  r3_18n_targets.tsv \
  r3_18n_control_rows.json \
  r3_18n_negative_controls.txt \
  r3_18n_aggregate.txt
do
  sha256sum "$file"
done > r3_18n_artifact_sha256.txt

echo 'R3_18N_EVIDENCE=PASS'

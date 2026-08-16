#!/usr/bin/env bash
set -euo pipefail

MAIN='0a9bdab3717aacf320459d738a322ce00415fec7'
MAIN_TREE='85199115d323205a235246029163e6cb05d8fa35'
PROD='330ab01890a7c09eff1805e437584fb3be0a1134'
PROD_TREE='5540b6a86e53d243dabbabea223a5afa8657521c'
LIB_BLOB='ee9b0c71871df7ff52275581eb7ad4c023b8ba79'
J_TEST_BLOB='c5a97c5a17ae2ea292790a020673dd26a0150024'
K_SPEC_BLOB='d360b93a357c8bf7b3bede5d0b1413399f09d983'

J_IMPL_RUN='31975731621'
J_IMPL_JOB='95234808797'
J_CAND_RUN='31975907582'
J_CAND_JOB='95235253244'
J_PUB_RUN='31976100231'
J_PUB_JOB='95235742210'
MAIN_VALID_RUN='31976421430'
MAIN_VALID_JOB='95236511260'

I_HEAD='45090a2c18fb517088bb411782bbaed0d7d68199'
I_RUN='31975063743'
I_JOB='95233164711'
I_CI_RUN='31975063703'
I_CI_JOB='95233164610'
I_ARTIFACT_ID='9270842140'
I_ARTIFACT_DIGEST='9890ed33780412a8900692a627b212d80428a08229f9f691d914c8def31e06e2'
I_ARTIFACT_NAME='r318i-second-property-payload-evidence'

I_SOURCE_SCOPE_SHA='4b4e5d32744ccaa9aedf61bcae0f39fa9e34ea0e1e43d52611de3f4c75daded5'
I_REPLAY_ID_SHA='b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf'
I_WITNESS_SHA='99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7'
I_BOXCARS_SHA='8ddda8b22e955f922eefebef90c977d0cd6897c35a7b9d45159e81f9381f2ada'
I_ORACLE_SUMMARY_SHA='54304d2e4d4ad6664e66030a79f615c1bb560055d624d43d14d6fbcdca5d9e50'
I_COMPARISON_SHA='4792a73b5bf8105e90583ab3f9d28bd6faa960f118381a480996bd8906f6f511'
I_NEGATIVES_SHA='c783053ddbcc8451eb7a7d0b73acc194b41ce2ef683b5af5a161c77294b8053e'
I_AGGREGATE_SHA='f87f990753e20b866249ceb8bbd56f11cb998bb526384c04f7c6f52280e0aff2'
I_MANIFEST_SHA='b59dbc330223f5e11476808fdb05a0a7031c0f3047b4530f684703a2b5cc688f'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318k"
I_DIR="$WORK/r318i"
rm -rf "$WORK"
mkdir -p "$I_DIR"

cleanup() {
  rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318k_probe.rs"
}
trap cleanup EXIT

echo '== R3.18K authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git rev-parse HEAD^)" = "$MAIN"
test "$(git rev-parse "${PROD}^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${PROD}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/tests/r3_18j_second_property_payload.rs")" = "$J_TEST_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18K_EXECUTION_SPEC.md")" = "$K_SPEC_BLOB"

mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318k_evidence.yml'
  'tools/_tmp_r318k_native_probe.rs'
  'tools/_tmp_r318k_prepare.py'
  'tools/_tmp_r318k_run.sh'
)
mapfile -t expected_sorted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 4
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${expected_sorted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md

mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

for run in "$J_IMPL_RUN" "$J_CAND_RUN" "$J_PUB_RUN" "$MAIN_VALID_RUN" "$I_RUN" "$I_CI_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$J_IMPL_JOB" "$J_CAND_JOB" "$J_PUB_JOB" "$MAIN_VALID_JOB" "$I_JOB" "$I_CI_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$J_CAND_RUN" --jq .head_sha)" = "$PROD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$J_PUB_RUN" --jq .head_sha)" = "$PROD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$MAIN_VALID_RUN" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$I_RUN" --jq .head_sha)" = "$I_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$I_CI_RUN" --jq .head_sha)" = "$I_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$I_ARTIFACT_ID" --jq .workflow_run.id)" = "$I_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$I_ARTIFACT_ID" --jq .workflow_run.head_sha)" = "$I_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$I_ARTIFACT_ID" --jq .digest)" = "sha256:$I_ARTIFACT_DIGEST"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$I_ARTIFACT_ID" --jq .expired)" = false
echo 'R3_18K_AUTHORITY_FREEZE=PASS'

echo '== R3.18K immutable R3.18I authority =='
gh run download "$I_RUN" -n "$I_ARTIFACT_NAME" -D "$I_DIR"
test "$(sha256sum "$I_DIR/r3_18i_source_scope.txt" | awk '{print $1}')" = "$I_SOURCE_SCOPE_SHA"
test "$(sha256sum "$I_DIR/r3_18i_replay_identity.tsv" | awk '{print $1}')" = "$I_REPLAY_ID_SHA"
test "$(sha256sum "$I_DIR/r3_18i_frozen_witnesses.json" | awk '{print $1}')" = "$I_WITNESS_SHA"
test "$(sha256sum "$I_DIR/r3_18i_boxcars_instrumentation_sha256.txt" | awk '{print $1}')" = "$I_BOXCARS_SHA"
test "$(sha256sum "$I_DIR/r3_18i_oracle_summary.json" | awk '{print $1}')" = "$I_ORACLE_SUMMARY_SHA"
test "$(sha256sum "$I_DIR/r3_18i_comparison.json" | awk '{print $1}')" = "$I_COMPARISON_SHA"
test "$(sha256sum "$I_DIR/r3_18i_negative_controls.txt" | awk '{print $1}')" = "$I_NEGATIVES_SHA"
test "$(sha256sum "$I_DIR/r3_18i_aggregate.txt" | awk '{print $1}')" = "$I_AGGREGATE_SHA"
test "$(sha256sum "$I_DIR/r3_18i_artifact_sha256.txt" | awk '{print $1}')" = "$I_MANIFEST_SHA"
grep -Fq 'R3_18I_OUTCOME=A' "$I_DIR/r3_18i_aggregate.txt"
grep -Fq 'R3_18I_NATIVE_ORACLE_MISMATCH=0' "$I_DIR/r3_18i_aggregate.txt"
grep -Fq 'R3_18I_THIRD_PROPERTY_BITS_CONSUMED=0' "$I_DIR/r3_18i_aggregate.txt"

cp "$I_DIR/r3_18i_replay_identity.tsv" r3_18k_replay_identity.tsv
cp "$I_DIR/r3_18i_frozen_witnesses.json" r3_18k_frozen_witnesses.json
cat > r3_18k_r318i_authority_sha256.txt <<EOF
$I_SOURCE_SCOPE_SHA  r3_18i_source_scope.txt
$I_REPLAY_ID_SHA  r3_18i_replay_identity.tsv
$I_WITNESS_SHA  r3_18i_frozen_witnesses.json
$I_BOXCARS_SHA  r3_18i_boxcars_instrumentation_sha256.txt
$I_ORACLE_SUMMARY_SHA  r3_18i_oracle_summary.json
$I_COMPARISON_SHA  r3_18i_comparison.json
$I_NEGATIVES_SHA  r3_18i_negative_controls.txt
$I_AGGREGATE_SHA  r3_18i_aggregate.txt
$I_MANIFEST_SHA  r3_18i_artifact_sha256.txt
EOF

python3 - <<'PY'
import hashlib
from pathlib import Path
rows = []
for line in Path('r3_18k_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    rel, expected, status = line.split('\t')
    if status != 'PASS':
        raise SystemExit(f'bad identity status: {rel}')
    actual = hashlib.sha256(Path(rel).read_bytes()).hexdigest()
    if actual.lower() != expected.lower():
        raise SystemExit(f'replay identity drift: {rel}')
    rows.append(rel.replace('\\', '/'))
if len(rows) != 47 or len(set(rows)) != 47:
    raise SystemExit('R3.18K lane is not exactly 47 unique replays')
print('R3_18K_REPLAY_IDENTITY=PASS rows=47')
PY

python3 tools/_tmp_r318k_prepare.py prepare \
  "$I_DIR/r3_18i_frozen_witnesses.json" \
  "$I_DIR/r3_18i_comparison.json" \
  "$WORK/request.tsv" \
  r3_18k_authority_summary.json

cat > r3_18k_source_scope.txt <<EOF
R3_18K_BASE_MAIN=$MAIN
R3_18K_BASE_TREE=$MAIN_TREE
R3_18K_PRODUCTION_SHA=$PROD
R3_18K_PRODUCTION_TREE=$PROD_TREE
R3_18K_PRODUCTION_LIB_BLOB=$LIB_BLOB
R3_18K_FOCUSED_TEST_BLOB=$J_TEST_BLOB
R3_18K_SPEC_BLOB=$K_SPEC_BLOB
R3_18K_R318I_HEAD=$I_HEAD
R3_18K_R318I_ARTIFACT=$I_ARTIFACT_ID
R3_18K_R318I_ARTIFACT_DIGEST=sha256:$I_ARTIFACT_DIGEST
R3_18K_CHANGED_TEMP_FILES=4
R3_18K_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF

echo '== R3.18K production API differential =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318k_native_probe.rs crates/mimir-replay/examples/_tmp_r318k_probe.rs
cargo build --locked -p mimir-replay --example _tmp_r318k_probe
./target/debug/examples/_tmp_r318k_probe "$WORK/request.tsv" | tee "$WORK/native1.log"
./target/debug/examples/_tmp_r318k_probe "$WORK/request.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
rm -f crates/mimir-replay/examples/_tmp_r318k_probe.rs

python3 tools/_tmp_r318k_prepare.py analyze \
  "$WORK/native1.log" \
  r3_18k_comparison.json \
  r3_18k_negative_controls.txt \
  r3_18k_aggregate.txt

echo '== R3.18K regression and repository validation =='
cargo fmt --all -- --check
cargo test --locked -p mimir-replay --test r3_18j_second_property_payload -- --nocapture
cargo test --locked -p mimir-replay -- --nocapture
cargo check --locked --workspace --all-targets --all-features
cargo test --locked --workspace
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings
pwsh -NoProfile -File scripts/verify_repo.ps1

git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
test ! -e crates/mimir-replay/examples/_tmp_r318k_probe.rs

echo '== R3.18K privacy and artifact receipt =='
if grep -R -n -E 'window_hex|content_hex|semantic_i32=|semantic_fnv64=' \
  r3_18k_source_scope.txt r3_18k_replay_identity.tsv r3_18k_frozen_witnesses.json \
  r3_18k_r318i_authority_sha256.txt r3_18k_authority_summary.json \
  r3_18k_comparison.json r3_18k_negative_controls.txt r3_18k_aggregate.txt; then
  echo 'privacy-sensitive evidence marker found'
  exit 1
fi

grep -Fq 'R3_18K_OUTCOME=A' r3_18k_aggregate.txt
grep -Fq 'R3_18K_FROZEN_ROWS=94/94' r3_18k_aggregate.txt
grep -Fq 'R3_18K_NATIVE_ORACLE_MISMATCH=0' r3_18k_aggregate.txt
grep -Fq 'R3_18K_FOLLOWING_PROPERTY_BITS_CONSUMED=0' r3_18k_aggregate.txt
grep -Fq 'R3_18K_PRIVACY=PASS' r3_18k_aggregate.txt

for file in \
  r3_18k_source_scope.txt \
  r3_18k_replay_identity.tsv \
  r3_18k_frozen_witnesses.json \
  r3_18k_r318i_authority_sha256.txt \
  r3_18k_authority_summary.json \
  r3_18k_comparison.json \
  r3_18k_negative_controls.txt \
  r3_18k_aggregate.txt
do
  sha256sum "$file"
done > r3_18k_artifact_sha256.txt

echo 'R3_18K_EVIDENCE=PASS'

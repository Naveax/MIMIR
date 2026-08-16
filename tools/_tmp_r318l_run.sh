#!/usr/bin/env bash
set -euo pipefail

MAIN='1b39cf1abb8b84100349bfe2540296425ef1baed'
MAIN_TREE='f4d59812239a33388af05e5797399e36b8e7cf81'
PROD='330ab01890a7c09eff1805e437584fb3be0a1134'
PROD_TREE='5540b6a86e53d243dabbabea223a5afa8657521c'
LIB_BLOB='ee9b0c71871df7ff52275581eb7ad4c023b8ba79'
J_TEST_BLOB='c5a97c5a17ae2ea292790a020673dd26a0150024'
K_DECISION_BLOB='2a50fe6e962498d2ab2589477ee104f19124ce42'
L_SPEC_BLOB='4910ad6d44ed9bb47e5e81139dd5c37575e96adc'

J_IMPL_RUN='31975731621'
J_IMPL_JOB='95234808797'
J_CAND_RUN='31975907582'
J_CAND_JOB='95235253244'
J_PUB_RUN='31976100231'
J_PUB_JOB='95235742210'

K_HEAD='926ddd88331ef0372b17b495cb06502010ab39ac'
K_RUN='31977860600'
K_JOB='95239932737'
K_CI_RUN='31977860563'
K_CI_JOB='95239932564'
K_ARTIFACT_ID='9271561853'
K_ARTIFACT_DIGEST='a455984c1149cb8f186eedb34d3e148fe45b8592c928cd9246d36cd52843262f'
K_ARTIFACT_NAME='r318k-published-second-payload-evidence'
K_PUBLISHED_VALIDATION_RUN='31978365419'
K_PUBLISHED_VALIDATION_JOB='95241179721'

K_SOURCE_SCOPE_SHA='64ed5ce376813534cdc196e35421092db62b6d84dc244950aa51872def38151f'
K_REPLAY_ID_SHA='b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf'
K_WITNESS_SHA='99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7'
K_I_AUTH_SHA='9cf75f074c46a15823556e6f0de32f727d10845382e9631537483dbd952c388e'
K_AUTH_SUMMARY_SHA='40854122f5c39981514077f66fbf0e51b54d0a07997dc262bb5a6b37fe309f70'
K_COMPARISON_SHA='8ca0503a453550c82fccf500834b79b25cafa6c100fda71b67aa5cb7ee0558ac'
K_NEGATIVES_SHA='f6186113fbbcde35c7670e1415dc967eaa549ffde934625e613893cf04e7b9c9'
K_AGGREGATE_SHA='a746fe172d11d55cd274df105c6a1f65b69b114c0951df0c7c7aa5d0859418bd'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318l"
K_DIR="$WORK/r318k"
BOXCARS="$ROOT/.tmp/boxcars-r318l"
rm -rf "$WORK" "$BOXCARS"
mkdir -p "$K_DIR"

cleanup() {
  rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318l_probe.rs"
}
trap cleanup EXIT

echo '== R3.18L authority freeze =='
git fetch origin main evidence/r318c-loop-control --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git rev-parse HEAD^)" = "$MAIN"
test "$(git rev-parse "${PROD}^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${PROD}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/tests/r3_18j_second_property_payload.rs")" = "$J_TEST_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18K_DECISION.md")" = "$K_DECISION_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18L_EXECUTION_SPEC.md")" = "$L_SPEC_BLOB"
test "$(git rev-parse origin/evidence/r318c-loop-control)" = "$R318C_HEAD"
test "$(git rev-parse "${R318C_HEAD}:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"

mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318l_evidence.yml'
  'tools/_tmp_r318l_extend_boxcars.py'
  'tools/_tmp_r318l_native_probe.rs'
  'tools/_tmp_r318l_prepare.py'
  'tools/_tmp_r318l_run.sh'
)
mapfile -t expected_sorted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 5
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${expected_sorted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

for run in "$J_IMPL_RUN" "$J_CAND_RUN" "$J_PUB_RUN" "$K_RUN" "$K_CI_RUN" "$K_PUBLISHED_VALIDATION_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$J_IMPL_JOB" "$J_CAND_JOB" "$J_PUB_JOB" "$K_JOB" "$K_CI_JOB" "$K_PUBLISHED_VALIDATION_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$K_RUN" --jq .head_sha)" = "$K_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$K_CI_RUN" --jq .head_sha)" = "$K_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$K_PUBLISHED_VALIDATION_RUN" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$K_ARTIFACT_ID" --jq .workflow_run.id)" = "$K_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$K_ARTIFACT_ID" --jq .workflow_run.head_sha)" = "$K_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$K_ARTIFACT_ID" --jq .digest)" = "sha256:$K_ARTIFACT_DIGEST"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$K_ARTIFACT_ID" --jq .expired)" = false
echo 'R3_18L_AUTHORITY_FREEZE=PASS'

echo '== R3.18L immutable R3.18K lane =='
gh run download "$K_RUN" -n "$K_ARTIFACT_NAME" -D "$K_DIR"
test "$(sha256sum "$K_DIR/r3_18k_source_scope.txt" | awk '{print $1}')" = "$K_SOURCE_SCOPE_SHA"
test "$(sha256sum "$K_DIR/r3_18k_replay_identity.tsv" | awk '{print $1}')" = "$K_REPLAY_ID_SHA"
test "$(sha256sum "$K_DIR/r3_18k_frozen_witnesses.json" | awk '{print $1}')" = "$K_WITNESS_SHA"
test "$(sha256sum "$K_DIR/r3_18k_r318i_authority_sha256.txt" | awk '{print $1}')" = "$K_I_AUTH_SHA"
test "$(sha256sum "$K_DIR/r3_18k_authority_summary.json" | awk '{print $1}')" = "$K_AUTH_SUMMARY_SHA"
test "$(sha256sum "$K_DIR/r3_18k_comparison.json" | awk '{print $1}')" = "$K_COMPARISON_SHA"
test "$(sha256sum "$K_DIR/r3_18k_negative_controls.txt" | awk '{print $1}')" = "$K_NEGATIVES_SHA"
test "$(sha256sum "$K_DIR/r3_18k_aggregate.txt" | awk '{print $1}')" = "$K_AGGREGATE_SHA"
grep -Fq 'R3_18K_OUTCOME=A' "$K_DIR/r3_18k_aggregate.txt"
grep -Fq 'R3_18K_NATIVE_ORACLE_MISMATCH=0' "$K_DIR/r3_18k_aggregate.txt"
grep -Fq 'R3_18K_FOLLOWING_PROPERTY_BITS_CONSUMED=0' "$K_DIR/r3_18k_aggregate.txt"

cp "$K_DIR/r3_18k_replay_identity.tsv" r3_18l_replay_identity.tsv
cp "$K_DIR/r3_18k_frozen_witnesses.json" r3_18l_frozen_witnesses.json
cat > r3_18l_r318k_authority_sha256.txt <<EOF
$K_SOURCE_SCOPE_SHA  r3_18k_source_scope.txt
$K_REPLAY_ID_SHA  r3_18k_replay_identity.tsv
$K_WITNESS_SHA  r3_18k_frozen_witnesses.json
$K_I_AUTH_SHA  r3_18k_r318i_authority_sha256.txt
$K_AUTH_SUMMARY_SHA  r3_18k_authority_summary.json
$K_COMPARISON_SHA  r3_18k_comparison.json
$K_NEGATIVES_SHA  r3_18k_negative_controls.txt
$K_AGGREGATE_SHA  r3_18k_aggregate.txt
EOF

python3 - <<'PY'
import hashlib
from pathlib import Path
rows = []
for line in Path('r3_18l_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    rel, expected, status = line.split('\t')
    if status != 'PASS':
        raise SystemExit(f'bad identity status: {rel}')
    if hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower() != expected.lower():
        raise SystemExit(f'replay identity drift: {rel}')
    rows.append(rel.replace('\\', '/'))
if len(rows) != 47 or len(set(rows)) != 47:
    raise SystemExit('R3.18L replay lane is not exactly 47 unique identities')
print('R3_18L_REPLAY_IDENTITY=PASS rows=47')
PY

python3 tools/_tmp_r318l_prepare.py build \
  "$K_DIR/r3_18k_frozen_witnesses.json" \
  "$K_DIR/r3_18k_comparison.json" \
  "$WORK/targets.tsv" \
  r3_18l_source_summary.json
cp "$WORK/targets.tsv" r3_18l_targets.tsv
awk -F '\t' '{print $1 "\t" $25 "\t" $26}' "$WORK/targets.tsv" > "$WORK/oracle_targets.tsv"
test "$(wc -l < "$WORK/oracle_targets.tsv" | tr -d ' ')" -eq 47

echo '== R3.18L pinned Boxcars one-bit oracle =='
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$WORK/r318c_base_patch.py"
python3 - <<'PY'
from pathlib import Path
p = Path('.tmp/r318l/r318c_base_patch.py')
s = p.read_text(encoding='utf-8')
old = '    stream_id_bound: i32,\n'
if s.count(old) != 1:
    raise SystemExit('unexpected R3.18C stream_id_bound patch shape')
s = s.replace(old, '    stream_id_bound: u32,\n', 1)
p.write_text(s, encoding='utf-8', newline='\n')
print('R3_18L_R318C_BASE_COMPAT=PASS')
PY

git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
python3 "$WORK/r318c_base_patch.py" "$BOXCARS"
python3 tools/_tmp_r318l_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18l_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18l_probe.rs Cargo.toml > "$WORK/r318l_boxcars.patch"
R318L_BOXCARS_PATCH_SHA="$(sha256sum "$WORK/r318l_boxcars.patch" | awk '{print $1}')"
printf '%s  r318l_boxcars_one_bit_instrumentation.patch\n' "$R318L_BOXCARS_PATCH_SHA" > r3_18l_boxcars_instrumentation_sha256.txt
cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18l_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18l_probe"
test -x "$PROBE"
: > "$WORK/oracle.log"
while IFS=$'\t' read -r rel frame actor; do
  test -n "$rel"
  MIMIR_R3_18L_LABEL="$rel" \
  MIMIR_R3_18L_TARGET_FRAME="$frame" \
  MIMIR_R3_18L_TARGET_ACTOR_ORDINAL="$actor" \
    "$PROBE" "$ROOT/$rel" >> "$WORK/oracle.log" 2>&1
done < "$WORK/oracle_targets.tsv"
test "$(grep -c '^R3_18L_ORACLE_PARSE=PASS$' "$WORK/oracle.log")" -eq 47
test "$(grep -c $'^R3_18L_ORACLE\t' "$WORK/oracle.log")" -eq 47
echo 'R3_18L_BOXCARS_ORACLE=PASS controls=47'

echo '== R3.18L published R3.18J reconstruction + independent one-bit observation =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318l_native_probe.rs crates/mimir-replay/examples/_tmp_r318l_probe.rs
cargo build --locked -p mimir-replay --example _tmp_r318l_probe
./target/debug/examples/_tmp_r318l_probe "$WORK/targets.tsv" | tee "$WORK/native1.log"
./target/debug/examples/_tmp_r318l_probe "$WORK/targets.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
rm -f crates/mimir-replay/examples/_tmp_r318l_probe.rs

python3 tools/_tmp_r318l_prepare.py analyze \
  "$WORK/targets.tsv" \
  "$WORK/oracle.log" \
  "$WORK/native1.log" \
  r3_18l_control_rows.json \
  r3_18l_negative_controls.txt \
  r3_18l_aggregate.txt

cat > r3_18l_source_scope.txt <<EOF
R3_18L_BASE_MAIN=$MAIN
R3_18L_BASE_TREE=$MAIN_TREE
R3_18L_PRODUCTION_SHA=$PROD
R3_18L_PRODUCTION_TREE=$PROD_TREE
R3_18L_PRODUCTION_LIB_BLOB=$LIB_BLOB
R3_18L_FOCUSED_TEST_BLOB=$J_TEST_BLOB
R3_18L_K_DECISION_BLOB=$K_DECISION_BLOB
R3_18L_SPEC_BLOB=$L_SPEC_BLOB
R3_18L_R318K_HEAD=$K_HEAD
R3_18L_R318K_ARTIFACT=$K_ARTIFACT_ID
R3_18L_R318K_ARTIFACT_DIGEST=sha256:$K_ARTIFACT_DIGEST
R3_18L_BOXCARS_SHA=$BOXCARS_SHA
R3_18L_BOXCARS_PATCH_SHA256=$R318L_BOXCARS_PATCH_SHA
R3_18L_CHANGED_TEMP_FILES=5
R3_18L_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF

echo '== R3.18L regression and full repository validation =='
cargo fmt --all -- --check
cargo test --locked -p mimir-replay --test r3_18j_second_property_payload -- --nocapture
cargo test --locked -p mimir-replay -- --nocapture
cargo check --locked --workspace --all-targets --all-features
cargo test --locked --workspace
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings
pwsh -NoProfile -File scripts/verify_repo.ps1

git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
test ! -e crates/mimir-replay/examples/_tmp_r318l_probe.rs

echo '== R3.18L privacy and artifact manifest =='
if grep -R -n -E 'window_hex=|window_hex"|content_hex|semantic_i32=|semantic_fnv64=' \
  r3_18l_source_scope.txt r3_18l_replay_identity.tsv r3_18l_frozen_witnesses.json \
  r3_18l_r318k_authority_sha256.txt r3_18l_source_summary.json r3_18l_targets.tsv \
  r3_18l_boxcars_instrumentation_sha256.txt r3_18l_control_rows.json \
  r3_18l_negative_controls.txt r3_18l_aggregate.txt; then
  echo 'privacy-sensitive evidence marker found'
  exit 1
fi

grep -Fq 'R3_18L_OUTCOME=A' r3_18l_aggregate.txt
grep -Fq 'R3_18L_FROZEN_ROWS=47/47' r3_18l_aggregate.txt
grep -Fq 'R3_18L_NATIVE_ORACLE_MISMATCH=0' r3_18l_aggregate.txt
grep -Fq 'R3_18L_FOLLOWING_STREAM_BITS_CONSUMED=0' r3_18l_aggregate.txt
grep -Fq 'R3_18L_FOLLOWING_HEADER_BITS_CONSUMED=0' r3_18l_aggregate.txt
grep -Fq 'R3_18L_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' r3_18l_aggregate.txt
grep -Fq 'R3_18L_PRIVACY=PASS' r3_18l_aggregate.txt

for file in \
  r3_18l_source_scope.txt \
  r3_18l_replay_identity.tsv \
  r3_18l_frozen_witnesses.json \
  r3_18l_r318k_authority_sha256.txt \
  r3_18l_source_summary.json \
  r3_18l_targets.tsv \
  r3_18l_boxcars_instrumentation_sha256.txt \
  r3_18l_control_rows.json \
  r3_18l_negative_controls.txt \
  r3_18l_aggregate.txt
do
  sha256sum "$file"
done > r3_18l_artifact_sha256.txt

echo 'R3_18L_EVIDENCE=PASS'

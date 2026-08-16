#!/usr/bin/env bash
set -euo pipefail

MAIN='3e1fc68eea41378bac07992b5ccfc05485edd4c6'
MAIN_TREE='0d21e6da9022e2db4a8450722a9d39d1234b3adc'
PROD='2b608aafae97b10ecbc884f99e4bd4a73abf7a5c'
PROD_TREE='b130caf211ce72577870c70d6c0d87cd006e1b29'
LIB_BLOB='5e2b9e5be9c6692e499abc97a89655c603728cef'
R318G_TEST_BLOB='d56bf97d250b426e23fec4610cbb9ead6ec8a142'
R318I_SPEC_BLOB='088b3edd9d4fac4ff1144213cf92c951de66afac'

R318H_HEAD='1db03fddabf84bfa189f983fa4a3b9110d105442'
R318H_RUN='31960174729'
R318H_JOB='95196833572'
R318H_CI_RUN='31960174713'
R318H_CI_JOB='95196833409'
R318H_ARTIFACT_ID='9267045757'
R318H_ARTIFACT_DIGEST='340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645'
R318H_PUBLISHED_CONTINUITY_RUN='31963228589'
R318H_PUBLISHED_CONTINUITY_JOB='95204290405'

R318F_HEAD='27a855a9cfb82a0294dd1601e4da01c9fdfad264'
R318F_RUN='31951039411'
R318F_JOB='95174417526'
R318F_ARTIFACT_ID='9264673141'
R318F_ARTIFACT_DIGEST='e31e09abf322b6458f9034b06efe5502bb3b7f1011dfb08c9ffd6d1b1cd1b361'
R318F_SOURCE_SCOPE_SHA='492f63c3cfcb27967426816f97858c8f4ad1d9ebb6ce40719f6d829ff3f0ea55'
R318F_IDENTITY_SHA='b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf'
R318F_BOXCARS_RECEIPT_SHA='ba0f63ca5cd09ff48e7f70141f6cc78dacc2307502af6c1e09a9695b2ba52e97'
R318F_WITNESSES_SHA='99461d2c2bf2f17dc41336d6efcd9321ce7ad6fabd2da663d8ddc3509231fdd7'
R318F_SUMMARY_SHA='bd6c4d25b02533626485e4fdb000034a39e7c2b5f559d8a09a8a4eb5e5ca80d4'
R318F_COMPARISON_SHA='53f4a9aefbfcc3d02e5a1501d2849455052c01612ddd299e795e89ad2938ddcd'
R318F_AGGREGATE_SHA='57c90cb3617461aea1a078a7b0f72ae301fd35fc9d7c4f9fe56de6d7633a4a04'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318i"
FROZEN="$WORK/frozen"
BOXCARS="$ROOT/.tmp/boxcars-r318i"
rm -rf "$WORK" "$BOXCARS"
mkdir -p "$FROZEN"

cleanup() {
  rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318i_probe.rs"
}
trap cleanup EXIT

echo '== R3.18I authority freeze =='
git fetch origin main evidence/r318f-second-property-header evidence/r318c-loop-control --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git rev-parse HEAD^)" = "$MAIN"
test "$(git rev-parse "${PROD}^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${PROD}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/tests/r3_18g_second_property_header.rs")" = "$R318G_TEST_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18I_EXECUTION_SPEC.md")" = "$R318I_SPEC_BLOB"
test "$(git rev-parse origin/evidence/r318f-second-property-header)" = "$R318F_HEAD"
test "$(git rev-parse origin/evidence/r318c-loop-control)" = "$R318C_HEAD"
test "$(git rev-parse "${R318C_HEAD}:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"

mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318i_evidence.yml'
  'tools/_tmp_r318i_analyze.py'
  'tools/_tmp_r318i_extend_boxcars.py'
  'tools/_tmp_r318i_native_probe.rs'
  'tools/_tmp_r318i_run.sh'
)
mapfile -t expected_sorted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 5
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${expected_sorted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

for id in "$R318H_RUN" "$R318H_CI_RUN" "$R318H_PUBLISHED_CONTINUITY_RUN" "$R318F_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$id" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R318H_RUN" --jq .head_sha)" = "$R318H_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$R318H_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$R318H_CI_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$R318H_PUBLISHED_CONTINUITY_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$R318H_ARTIFACT_ID" --jq .workflow_run.id)" = "$R318H_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$R318H_ARTIFACT_ID" --jq .digest)" = "sha256:$R318H_ARTIFACT_DIGEST"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R318F_RUN" --jq .head_sha)" = "$R318F_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$R318F_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$R318F_ARTIFACT_ID" --jq .workflow_run.id)" = "$R318F_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$R318F_ARTIFACT_ID" --jq .digest)" = "sha256:$R318F_ARTIFACT_DIGEST"
echo 'R3_18I_AUTHORITY_FREEZE=PASS'

echo '== R3.18I frozen R3.18F lane =='
gh run download "$R318F_RUN" -n r318f-second-property-header-evidence -D "$FROZEN"
test "$(sha256sum "$FROZEN/r3_18f_source_scope.txt" | awk '{print $1}')" = "$R318F_SOURCE_SCOPE_SHA"
test "$(sha256sum "$FROZEN/r3_18f_replay_identity.tsv" | awk '{print $1}')" = "$R318F_IDENTITY_SHA"
test "$(sha256sum "$FROZEN/r3_18f_boxcars_instrumentation_sha256.txt" | awk '{print $1}')" = "$R318F_BOXCARS_RECEIPT_SHA"
test "$(sha256sum "$FROZEN/r3_18f_selected_witnesses.json" | awk '{print $1}')" = "$R318F_WITNESSES_SHA"
test "$(sha256sum "$FROZEN/r3_18f_selection_summary.json" | awk '{print $1}')" = "$R318F_SUMMARY_SHA"
test "$(sha256sum "$FROZEN/r3_18f_comparison.json" | awk '{print $1}')" = "$R318F_COMPARISON_SHA"
test "$(sha256sum "$FROZEN/r3_18f_aggregate.txt" | awk '{print $1}')" = "$R318F_AGGREGATE_SHA"
cp "$FROZEN/r3_18f_replay_identity.tsv" r3_18i_replay_identity.tsv
cp "$FROZEN/r3_18f_selected_witnesses.json" r3_18i_frozen_witnesses.json
python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18i_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel, expected, status = line.split('\t')
    if status != 'PASS': raise SystemExit(f'bad identity status: {rel}')
    if hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower() != expected.lower():
        raise SystemExit(f'replay identity drift: {rel}')
    rows.append(rel.replace('\\','/'))
if len(rows) != 47 or len(set(rows)) != 47:
    raise SystemExit('frozen replay lane is not exactly 47 unique identities')
Path('.tmp/r318i/paths.txt').write_text(''.join(x+'\n' for x in rows), encoding='utf-8', newline='\n')
print('R3_18I_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== R3.18I pinned Boxcars payload oracle =='
git show "$R318F_HEAD:tools/_tmp_r318f_analyze.py" > "$WORK/r318f_analyze.py"
git show "$R318F_HEAD:tools/_tmp_r318f_extend_boxcars.py" > "$WORK/r318f_extend_boxcars.py"
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$WORK/r318c_base_patch.py"
python3 - <<'PY'
from pathlib import Path
p=Path('.tmp/r318i/r318c_base_patch.py')
s=p.read_text(encoding='utf-8')
if s.count('    stream_id_bound: i32,\n') != 1:
    raise SystemExit('unexpected inherited stream_id_bound patcher shape')
s=s.replace('    stream_id_bound: i32,\n','    stream_id_bound: u32,\n',1)
s=s.replace('R3_18C','R3_18F').replace('r3_18c','r3_18f')
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18I_BOXCARS_BASE_PATCH_DERIVATION=PASS')
PY

git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
python3 "$WORK/r318c_base_patch.py" "$BOXCARS"
python3 "$WORK/r318f_extend_boxcars.py" "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18f_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18f_probe.rs Cargo.toml > "$WORK/r318f_exact.patch"
test "$(sha256sum "$WORK/r318f_exact.patch" | awk '{print $1}')" = "$(awk '{print $1}' "$FROZEN/r3_18f_boxcars_instrumentation_sha256.txt")"
python3 tools/_tmp_r318i_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18f_probe.rs Cargo.toml > "$WORK/r318i_boxcars.patch"
R318I_BOXCARS_PATCH_SHA="$(sha256sum "$WORK/r318i_boxcars.patch" | awk '{print $1}')"
printf '%s  r318i_boxcars_payload_instrumentation.patch\n' "$R318I_BOXCARS_PATCH_SHA" > r3_18i_boxcars_instrumentation_sha256.txt

cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18f_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18f_probe"
test -x "$PROBE"
: > "$WORK/oracle.log"
while IFS= read -r rel; do
  test -n "$rel"
  MIMIR_R3_18F_LABEL="$rel" "$PROBE" "$ROOT/$rel" >> "$WORK/oracle.log" 2>&1
done < "$WORK/paths.txt"
test "$(grep -c '^R3_18F_ORACLE_PARSE=PASS$' "$WORK/oracle.log")" -eq 47
test "$(grep -c $'^R3_18F_ORACLE\t' "$WORK/oracle.log")" -eq 94
test "$(grep -c $'^R3_18F_SECOND\t' "$WORK/oracle.log")" -eq 47
test "$(grep -c $'^R3_18I_PAYLOAD\t' "$WORK/oracle.log")" -eq 47

python3 "$WORK/r318f_analyze.py" select \
  "$WORK/oracle.log" "$WORK/r318f_request.tsv" "$WORK/regenerated_witnesses.json" "$WORK/regenerated_summary.json"
test "$(sha256sum "$WORK/regenerated_witnesses.json" | awk '{print $1}')" = "$R318F_WITNESSES_SHA"
test "$(sha256sum "$WORK/regenerated_summary.json" | awk '{print $1}')" = "$R318F_SUMMARY_SHA"
python3 tools/_tmp_r318i_analyze.py build \
  "$WORK/r318f_request.tsv" "$WORK/oracle.log" "$WORK/r318i_request.tsv" r3_18i_oracle_summary.json
test "$(wc -l < "$WORK/r318i_request.tsv" | tr -d ' ')" -eq 94
grep -Fq '"Int": 46' r3_18i_oracle_summary.json
grep -Fq '"String": 1' r3_18i_oracle_summary.json
grep -Fq '"third_property_bits_observed": 0' r3_18i_oracle_summary.json
grep -Fq '"witness_reselection": 0' r3_18i_oracle_summary.json
echo 'R3_18I_ORACLE=PASS rows=47 payloads reselection=0 third_property=0'

echo '== R3.18I native admitted decoder differential =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318i_native_probe.rs crates/mimir-replay/examples/_tmp_r318i_probe.rs
cargo build --locked -p mimir-replay --example _tmp_r318i_probe
./target/debug/examples/_tmp_r318i_probe "$WORK/r318i_request.tsv" | tee "$WORK/native1.log"
./target/debug/examples/_tmp_r318i_probe "$WORK/r318i_request.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
rm -f crates/mimir-replay/examples/_tmp_r318i_probe.rs

grep -Fx 'R3_18I_NATIVE_ROWS=94' "$WORK/native1.log"
grep -Fx 'R3_18I_TERMINATOR_ROWS=47' "$WORK/native1.log"
grep -Fx 'R3_18I_CONTINUATION_ROWS=47' "$WORK/native1.log"
grep -Fx 'R3_18I_INT_ROWS=46' "$WORK/native1.log"
grep -Fx 'R3_18I_STRING_ROWS=1' "$WORK/native1.log"
grep -Fx 'R3_18I_TERMINATOR_NO_PAYLOAD_ROWS=47' "$WORK/native1.log"
grep -Fx 'R3_18I_PAYLOAD_TRUNCATION_ROWS=47' "$WORK/native1.log"
grep -Fx 'R3_18I_THIRD_PROPERTY_BITS_CONSUMED=0' "$WORK/native1.log"
grep -Fx 'R3_18I_MISMATCH_COUNT=0' "$WORK/native1.log"
grep -Fx 'R3_18I_WRONG_SCALAR_TAG_NEGATIVE=PASS' "$WORK/native1.log"
grep -Fx 'R3_18I_WRONG_K2_TAG_NEGATIVE=PASS' "$WORK/native1.log"
grep -Fx 'R3_18I_REPEATABILITY=PASS' "$WORK/native1.log"
grep -Fx 'R3_18I_POST_PAYLOAD_POISON=PASS' "$WORK/native1.log"
python3 tools/_tmp_r318i_analyze.py compare "$WORK/native1.log" r3_18i_comparison.json r3_18i_aggregate.txt

cat > r3_18i_negative_controls.txt <<'EOF'
terminator_no_second_payload=PASS 47/47
payload_truncation_real_rows=PASS 47/47
wrong_scalar_tag=PASS
wrong_k2_tag=PASS
repeatability=PASS
post_payload_poison_and_third_control_invariance=PASS
third_property_bits_consumed=0
EOF

EVIDENCE_HEAD="$(git rev-parse HEAD)"
EVIDENCE_TREE="$(git rev-parse HEAD^{tree})"
cat > r3_18i_source_scope.txt <<EOF
canonical_main=$MAIN
canonical_main_tree=$MAIN_TREE
production_sha=$PROD
production_tree=$PROD_TREE
production_lib_blob=$LIB_BLOB
r318g_test_blob=$R318G_TEST_BLOB
r318i_spec_blob=$R318I_SPEC_BLOB
r318h_evidence_head=$R318H_HEAD
r318h_run=$R318H_RUN
r318h_job=$R318H_JOB
r318h_same_head_ci_run=$R318H_CI_RUN
r318h_same_head_ci_job=$R318H_CI_JOB
r318h_artifact=$R318H_ARTIFACT_ID
r318h_artifact_digest=sha256:$R318H_ARTIFACT_DIGEST
r318f_evidence_head=$R318F_HEAD
r318f_run=$R318F_RUN
r318f_job=$R318F_JOB
r318f_artifact=$R318F_ARTIFACT_ID
r318f_artifact_digest=sha256:$R318F_ARTIFACT_DIGEST
r318f_replay_identity_sha256=$R318F_IDENTITY_SHA
r318f_frozen_witnesses_sha256=$R318F_WITNESSES_SHA
pinned_boxcars=$BOXCARS_SHA
r318i_boxcars_patch_sha256=$R318I_BOXCARS_PATCH_SHA
evidence_head=$EVIDENCE_HEAD
evidence_tree=$EVIDENCE_TREE
production_mutation=0
cargo_lock_manifest_mutation=0
fixture_mutation=0
corpus_mutation=0
support_script_mutation=0
witness_reselection=0
third_property_bits_consumed=0
EOF

echo '== R3.18I focused/full regression =='
cargo test --locked -p mimir-replay --test r3_17c_scalar_attribute_decoder
cargo test --locked -p mimir-replay --test r3_17g_k2_attribute_decoder
cargo test --locked -p mimir-replay --test r3_18g_second_property_header
cargo test --locked -p mimir-replay
cargo check --locked --workspace
cargo test --locked --workspace
cargo clippy --locked --workspace --all-targets -- -D warnings
pwsh -NoProfile -File scripts/verify_repo.ps1

echo '== R3.18I mutation/privacy gates =='
test -z "$(git diff --name-only "$MAIN" HEAD -- crates Cargo.toml Cargo.lock)"
test -z "$(git diff --name-only "$MAIN" HEAD -- external_fixtures)"
test -z "$(git diff --name-only "$MAIN" HEAD -- test_corpus)"
test -z "$(git diff --name-only "$MAIN" HEAD -- scripts)"
# No private raw payload windows or raw String semantic values may enter the artifact.
if grep -R -n -E 'window_hex=|R3_18I_PAYLOAD\t|semantic_i32=|semantic_fnv64=' \
  r3_18i_source_scope.txt r3_18i_replay_identity.tsv r3_18i_frozen_witnesses.json \
  r3_18i_boxcars_instrumentation_sha256.txt r3_18i_oracle_summary.json \
  r3_18i_comparison.json r3_18i_negative_controls.txt r3_18i_aggregate.txt; then
  echo 'privacy-safe artifact check failed' >&2
  exit 1
fi
cat >> r3_18i_aggregate.txt <<'EOF'
R3_18I_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18I_PRIVACY=PASS
EOF

sha256sum \
  r3_18i_source_scope.txt \
  r3_18i_replay_identity.tsv \
  r3_18i_frozen_witnesses.json \
  r3_18i_boxcars_instrumentation_sha256.txt \
  r3_18i_oracle_summary.json \
  r3_18i_comparison.json \
  r3_18i_negative_controls.txt \
  r3_18i_aggregate.txt | tee r3_18i_artifact_sha256.txt

echo '== R3.18I final aggregate =='
cat r3_18i_aggregate.txt
echo 'R3_18I_EVIDENCE_ORCHESTRATION=PASS'

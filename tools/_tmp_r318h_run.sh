#!/usr/bin/env bash
set -euo pipefail

MAIN='63f5de4e49abaf76fe6441a255a1a6770388a63c'
MAIN_TREE='0cc556eca506034e2871b201b824d120dfa85880'
PROD='2b608aafae97b10ecbc884f99e4bd4a73abf7a5c'
PROD_TREE='b130caf211ce72577870c70d6c0d87cd006e1b29'
LIB_BLOB='5e2b9e5be9c6692e499abc97a89655c603728cef'
R318G_TEST_BLOB='d56bf97d250b426e23fec4610cbb9ead6ec8a142'
R318H_SPEC_BLOB='4b3eacad1698b22c421adda6af4a5142ced291e6'

R318G_IMPLEMENTATION_RUN='31957142924'
R318G_NORMAL_CI_RUN='31957142895'
R318G_EXACT_VALIDATOR_RUN='31957646865'
R318G_PUBLISHED_VALIDATOR_RUN='31957892048'

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

mkdir -p .tmp/r318h/frozen

echo '== R3.18H authority freeze =='
git fetch origin main evidence/r318f-second-property-header evidence/r318c-loop-control
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git rev-parse HEAD^)" = "$MAIN"
test "$(git rev-parse "${PROD}^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${PROD}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${MAIN}:crates/mimir-replay/tests/r3_18g_second_property_header.rs")" = "$R318G_TEST_BLOB"
test "$(git rev-parse "${PROD}:crates/mimir-replay/tests/r3_18g_second_property_header.rs")" = "$R318G_TEST_BLOB"
test "$(git rev-parse "${MAIN}:docs/continuity/MIMIR_R3_18H_EXECUTION_SPEC.md")" = "$R318H_SPEC_BLOB"
test "$(git rev-parse origin/evidence/r318f-second-property-header)" = "$R318F_HEAD"
test "$(git rev-parse origin/evidence/r318c-loop-control)" = "$R318C_HEAD"
test "$(git rev-parse "${R318C_HEAD}:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"

mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0
mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318h_evidence.yml'
  'tools/_tmp_r318h_analyze.py'
  'tools/_tmp_r318h_native_probe.rs'
  'tools/_tmp_r318h_run.sh'
)
mapfile -t expected_sorted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 4
if [ "$(printf '%s\n' "${changed[@]}")" != "$(printf '%s\n' "${expected_sorted[@]}")" ]; then
  printf 'unexpected R3.18H evidence scope\nactual:\n%s\nexpected:\n%s\n' "$(printf '%s\n' "${changed[@]}")" "$(printf '%s\n' "${expected_sorted[@]}")"
  exit 1
fi
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md

for id in "$R318G_IMPLEMENTATION_RUN" "$R318G_NORMAL_CI_RUN" "$R318G_EXACT_VALIDATOR_RUN" "$R318G_PUBLISHED_VALIDATOR_RUN" "$R318F_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$id" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R318F_RUN" --jq .head_sha)" = "$R318F_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$R318F_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$R318F_ARTIFACT_ID" --jq .workflow_run.id)" = "$R318F_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$R318F_ARTIFACT_ID" --jq .digest)" = "sha256:$R318F_ARTIFACT_DIGEST"

echo 'R3_18H_AUTHORITY_FREEZE=PASS'

echo '== R3.18H frozen R3.18F artifact =='
gh run download "$R318F_RUN" -n r318f-second-property-header-evidence -D .tmp/r318h/frozen
test "$(sha256sum .tmp/r318h/frozen/r3_18f_source_scope.txt | awk '{print $1}')" = "$R318F_SOURCE_SCOPE_SHA"
test "$(sha256sum .tmp/r318h/frozen/r3_18f_replay_identity.tsv | awk '{print $1}')" = "$R318F_IDENTITY_SHA"
test "$(sha256sum .tmp/r318h/frozen/r3_18f_boxcars_instrumentation_sha256.txt | awk '{print $1}')" = "$R318F_BOXCARS_RECEIPT_SHA"
test "$(sha256sum .tmp/r318h/frozen/r3_18f_selected_witnesses.json | awk '{print $1}')" = "$R318F_WITNESSES_SHA"
test "$(sha256sum .tmp/r318h/frozen/r3_18f_selection_summary.json | awk '{print $1}')" = "$R318F_SUMMARY_SHA"
test "$(sha256sum .tmp/r318h/frozen/r3_18f_comparison.json | awk '{print $1}')" = "$R318F_COMPARISON_SHA"
test "$(sha256sum .tmp/r318h/frozen/r3_18f_aggregate.txt | awk '{print $1}')" = "$R318F_AGGREGATE_SHA"
cp .tmp/r318h/frozen/r3_18f_replay_identity.tsv r3_18h_replay_identity.tsv
cp .tmp/r318h/frozen/r3_18f_selected_witnesses.json r3_18h_frozen_witnesses.json
python - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18h_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    rel,expected,status=line.split('\t')
    if status!='PASS':
        raise SystemExit(f'bad frozen identity status: {rel}')
    h=hashlib.sha256(Path(rel).read_bytes()).hexdigest()
    if h.lower()!=expected.lower():
        raise SystemExit(f'frozen replay drift: {rel}')
    rows.append(rel.replace('\\','/'))
if len(rows)!=47 or len(set(rows))!=47:
    raise SystemExit('frozen replay identity is not exactly 47 unique rows')
Path('.tmp/r318h/paths.txt').write_text(''.join(x+'\n' for x in rows),encoding='utf-8',newline='\n')
print('R3_18H_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== R3.18H exact R3.18F oracle regeneration =='
git show "$R318F_HEAD:tools/_tmp_r318f_analyze.py" > .tmp/r318h/r318f_analyze.py
git show "$R318F_HEAD:tools/_tmp_r318f_extend_boxcars.py" > .tmp/r318h/r318f_extend_boxcars.py
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > .tmp/r318h/r318c_base_patch.py
python - <<'PY'
from pathlib import Path
p=Path('.tmp/r318h/r318c_base_patch.py')
s=p.read_text(encoding='utf-8')
if s.count('    stream_id_bound: i32,\n') != 1:
    raise SystemExit('unexpected inherited stream_id_bound patcher shape')
s=s.replace('    stream_id_bound: i32,\n','    stream_id_bound: u32,\n',1)
s=s.replace('R3_18C','R3_18F').replace('r3_18c','r3_18f')
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18H_BOXCARS_BASE_PATCH_DERIVATION=PASS')
PY
BOXCARS="$PWD/.tmp/boxcars-r318h"
rm -rf "$BOXCARS"
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
python .tmp/r318h/r318c_base_patch.py "$BOXCARS"
python .tmp/r318h/r318f_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18f_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18f_probe.rs Cargo.toml > .tmp/r318h/r318f_boxcars_instrumentation.patch
test "$(sha256sum .tmp/r318h/r318f_boxcars_instrumentation.patch | awk '{print $1}')" = "$(awk '{print $1}' .tmp/r318h/frozen/r3_18f_boxcars_instrumentation_sha256.txt)"
cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18f_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18f_probe"
test -x "$PROBE"
: > .tmp/r318h/oracle.log
while IFS= read -r rel; do
  test -n "$rel"
  MIMIR_R3_18F_LABEL="$rel" "$PROBE" "$PWD/$rel" >> .tmp/r318h/oracle.log 2>&1
done < .tmp/r318h/paths.txt
test "$(grep -c '^R3_18F_ORACLE_PARSE=PASS$' .tmp/r318h/oracle.log)" -eq 47
test "$(grep -c $'^R3_18F_ORACLE\t' .tmp/r318h/oracle.log)" -eq 94
test "$(grep -c $'^R3_18F_SECOND\t' .tmp/r318h/oracle.log)" -eq 47
python .tmp/r318h/r318f_analyze.py select \
  .tmp/r318h/oracle.log \
  .tmp/r318h/native_request.tsv \
  .tmp/r318h/regenerated_witnesses.json \
  .tmp/r318h/regenerated_summary.json
test "$(wc -l < .tmp/r318h/native_request.tsv | tr -d ' ')" -eq 94
test "$(sha256sum .tmp/r318h/regenerated_witnesses.json | awk '{print $1}')" = "$R318F_WITNESSES_SHA"
test "$(sha256sum .tmp/r318h/regenerated_summary.json | awk '{print $1}')" = "$R318F_SUMMARY_SHA"
{
  echo "pinned_boxcars=$BOXCARS_SHA"
  echo "frozen_r318f_witnesses_sha256=$R318F_WITNESSES_SHA"
  echo "regenerated_witnesses_sha256=$(sha256sum .tmp/r318h/regenerated_witnesses.json | awk '{print $1}')"
  echo "frozen_r318f_selection_summary_sha256=$R318F_SUMMARY_SHA"
  echo "regenerated_selection_summary_sha256=$(sha256sum .tmp/r318h/regenerated_summary.json | awk '{print $1}')"
  echo 'witness_reselection=0'
} > r3_18h_oracle_regeneration.txt
echo 'R3_18H_ORACLE_REGENERATION=PASS rows=94 reselection=0'

echo '== R3.18H published R3.18G production differential =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318h_native_probe.rs crates/mimir-replay/examples/_tmp_r318h_probe.rs
cargo build --locked -p mimir-replay --example _tmp_r318h_probe
target/debug/examples/_tmp_r318h_probe .tmp/r318h/native_request.tsv | tee .tmp/r318h/native1.log
target/debug/examples/_tmp_r318h_probe .tmp/r318h/native_request.tsv > .tmp/r318h/native2.log
cmp .tmp/r318h/native1.log .tmp/r318h/native2.log
test "$(grep -c $'^R3_18H_NATIVE\t' .tmp/r318h/native1.log)" -eq 94
grep -Fx 'R3_18H_NATIVE_ROWS=94' .tmp/r318h/native1.log
grep -Fx 'R3_18H_TERMINATOR_ROWS=47' .tmp/r318h/native1.log
grep -Fx 'R3_18H_CONTINUATION_ROWS=47' .tmp/r318h/native1.log
grep -Fx 'R3_18H_TERMINATOR_NO_LOOKUP_ROWS=47' .tmp/r318h/native1.log
grep -Fx 'R3_18H_HEADER_TRUNCATION_ROWS=32' .tmp/r318h/native1.log
grep -Fx 'R3_18H_UNRESOLVED_STREAM_NEGATIVE=PASS' .tmp/r318h/native1.log
grep -Fx 'R3_18H_TAG_OUTSIDE_INT_STRING_NEGATIVE=PASS' .tmp/r318h/native1.log
grep -Fx 'R3_18H_SECOND_PAYLOAD_BITS_CONSUMED=0' .tmp/r318h/native1.log
grep -Fx 'R3_18H_THIRD_PROPERTY_BITS_CONSUMED=0' .tmp/r318h/native1.log
python tools/_tmp_r318h_analyze.py \
  r3_18h_frozen_witnesses.json \
  .tmp/r318h/native1.log \
  r3_18h_comparison.json \
  r3_18h_aggregate.txt \
  r3_18h_negative_controls.txt
rm crates/mimir-replay/examples/_tmp_r318h_probe.rs
git checkout -- crates/mimir-replay/src crates/mimir-replay/tests

echo '== R3.18H production regression gates =='
cargo test --locked -p mimir-replay --test r3_18g_second_property_header
cargo test --locked -p mimir-replay
cargo check --locked --workspace --all-targets --all-features
cargo test --locked --workspace --all-targets --all-features
cargo clippy --locked --workspace --all-targets --all-features -- -D warnings
pwsh -NoProfile -File scripts/verify_repo.ps1

echo '== R3.18H privacy / mutation gates =='
python - <<'PY'
from pathlib import Path
files=[
 'r3_18h_replay_identity.tsv','r3_18h_frozen_witnesses.json','r3_18h_oracle_regeneration.txt',
 'r3_18h_comparison.json','r3_18h_aggregate.txt','r3_18h_negative_controls.txt'
]
for name in files:
    text=Path(name).read_text(encoding='utf-8')
    for forbidden in ['window_hex','native_request.tsv','/home/runner/work/','D:\\\\a\\\\MIMIR']:
        if forbidden in text:
            raise SystemExit(f'privacy-safe artifact violation {name}: {forbidden}')
print('R3_18H_PRIVACY_SCAN=PASS')
PY
mapfile -t final_prod_diff < <(git diff --name-only "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md | sort)
test "${#final_prod_diff[@]}" -eq 0

{
  echo "canonical_main=$MAIN"
  echo "canonical_main_tree=$MAIN_TREE"
  echo "production_sha=$PROD"
  echo "production_tree=$PROD_TREE"
  echo "lib_blob=$LIB_BLOB"
  echo "r318g_test_blob=$R318G_TEST_BLOB"
  echo "r318h_spec_blob=$R318H_SPEC_BLOB"
  echo "r318g_implementation_run=$R318G_IMPLEMENTATION_RUN"
  echo "r318g_same_trigger_normal_ci_run=$R318G_NORMAL_CI_RUN"
  echo "r318g_exact_candidate_validator_run=$R318G_EXACT_VALIDATOR_RUN"
  echo "r318g_published_main_validator_run=$R318G_PUBLISHED_VALIDATOR_RUN"
  echo "r318f_evidence_head=$R318F_HEAD"
  echo "r318f_evidence_run=$R318F_RUN"
  echo "r318f_evidence_job=$R318F_JOB"
  echo "r318f_artifact_id=$R318F_ARTIFACT_ID"
  echo "r318f_artifact_digest=sha256:$R318F_ARTIFACT_DIGEST"
  echo "pinned_boxcars=$BOXCARS_SHA"
  echo "frozen_replay_identity_sha256=$R318F_IDENTITY_SHA"
  echo "frozen_witnesses_sha256=$R318F_WITNESSES_SHA"
  echo "evidence_head=$(git rev-parse HEAD)"
  echo 'production_mutation=0'
  echo 'cargo_mutation=0'
  echo 'fixture_mutation=0'
  echo 'corpus_mutation=0'
  echo 'support_mutation=0'
} > r3_18h_source_scope.txt

for f in \
  r3_18h_source_scope.txt \
  r3_18h_replay_identity.tsv \
  r3_18h_frozen_witnesses.json \
  r3_18h_oracle_regeneration.txt \
  r3_18h_comparison.json \
  r3_18h_negative_controls.txt \
  r3_18h_aggregate.txt; do
  sha256sum "$f"
done > r3_18h_receipt_sha256.txt

grep -Fx 'R3_18H_OUTCOME=A' r3_18h_aggregate.txt
grep -Fx 'R3_18H_NATIVE_ORACLE_MISMATCH_COUNT=0' r3_18h_aggregate.txt
grep -Fx 'R3_18H_SECOND_PAYLOAD_BITS_CONSUMED=0' r3_18h_aggregate.txt
grep -Fx 'R3_18H_THIRD_PROPERTY_BITS_CONSUMED=0' r3_18h_aggregate.txt
grep -Fx 'R3_18H_PRIVACY=PASS' r3_18h_aggregate.txt
grep -Fx 'R3_18H_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0' r3_18h_aggregate.txt

echo 'R3_18H_EVIDENCE=PASS'
cat r3_18h_aggregate.txt
cat r3_18h_receipt_sha256.txt

#!/usr/bin/env bash
set -euo pipefail

BASE_MAIN='3a10ee59ba42722b59ca6c5b816205f6e5d603ea'
BASE_TREE='ff8049a18431977e054652a0836217fcc39d84a7'
PROD_SHA='4adadd185783954c7fb6ad67db14b77b377cdde5'
PROD_TREE='67b1969eaff49d2913b88b3921f27b1bd7fe8193'
LIB_BLOB='42bc3fd3e8ea6bd1d15df82e4c6d8809b8443662'
R316B_TEST_BLOB='0fea53e1758e7b0b5f8d2a14b98cbce5feb400c2'
R318B_TEST_BLOB='927e9a2c834115d1c918fa96fb6d0690bd03965e'
R318D_TEST_BLOB='2f5b188cc5b3ce8200c9961d964f1dc66b3ab49b'
R318F_SPEC_BLOB='e6b92ea5628f107112a088421f318cd45a384e87'
R318E_EVIDENCE_HEAD='aae03a7fdec85e30be3954d14ffdc8cd1d86121e'
R318E_EVIDENCE_RUN='31949407736'
R318E_NORMAL_CI_RUN='31949407685'
R318E_ARTIFACT_ID='9264243765'
R318E_ARTIFACT_DIGEST='005afc3c97bd6bdb9aef69be993538fd813e30481923c59beefcf37e71cdfc9b'
R318E_CONTINUITY_RUN='31950169605'
R318E_CONTINUITY_EXACT_RUN='31950397556'
R318E_CONTINUITY_PUBLISHED_RUN='31950634411'
R318C_EVIDENCE_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
LANE_COMMIT='4cd21ea6db14c9becc11c17149af9201071859bc'
PATHS_SHA='2ecbeea804f193796a539baee1e968719f03c0cd706efff0c22a61e6ef943dae'
IDENTITY_SHA='b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

mkdir -p .tmp/r318f

echo '== R3.18F authority freeze =='
git fetch origin main evidence/r318e-control-differential evidence/r318c-loop-control evidence/r317a-primitive-scalar-attributes
test "$(git rev-parse origin/main)" = "$BASE_MAIN"
test "$(git rev-parse origin/main^{tree})" = "$BASE_TREE"
test "$(git rev-parse "${PROD_SHA}^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "${BASE_MAIN}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${PROD_SHA}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "${BASE_MAIN}:crates/mimir-replay/tests/r3_16b_property_header.rs")" = "$R316B_TEST_BLOB"
test "$(git rev-parse "${BASE_MAIN}:crates/mimir-replay/tests/r3_18b_single_k1_property.rs")" = "$R318B_TEST_BLOB"
test "$(git rev-parse "${BASE_MAIN}:crates/mimir-replay/tests/r3_18d_next_property_control.rs")" = "$R318D_TEST_BLOB"
test "$(git rev-parse "${BASE_MAIN}:docs/continuity/MIMIR_R3_18F_EXECUTION_SPEC.md")" = "$R318F_SPEC_BLOB"
test "$(git rev-parse origin/evidence/r318e-control-differential)" = "$R318E_EVIDENCE_HEAD"
test "$(git rev-parse origin/evidence/r318c-loop-control)" = "$R318C_EVIDENCE_HEAD"
test "$(git rev-parse "${R318C_EVIDENCE_HEAD}:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"
test "$(git rev-parse origin/evidence/r317a-primitive-scalar-attributes)" = "$LANE_COMMIT"

mapfile -t prod_drift < <(git diff --name-only "$PROD_SHA" "$BASE_MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

mapfile -t changed < <(git diff --name-only "$BASE_MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318f_evidence.yml'
  'tools/_tmp_r318f_analyze.py'
  'tools/_tmp_r318f_extend_boxcars.py'
  'tools/_tmp_r318f_native_probe.rs'
  'tools/_tmp_r318f_run.sh'
)
mapfile -t expected_sorted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 5
if [ "$(printf '%s\n' "${changed[@]}")" != "$(printf '%s\n' "${expected_sorted[@]}")" ]; then
  printf 'unexpected evidence scope\nactual:\n%s\nexpected:\n%s\n' "$(printf '%s\n' "${changed[@]}")" "$(printf '%s\n' "${expected_sorted[@]}")"
  exit 1
fi
git diff --exit-code "$BASE_MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md

for id in "$R318E_EVIDENCE_RUN" "$R318E_NORMAL_CI_RUN" "$R318E_CONTINUITY_RUN" "$R318E_CONTINUITY_EXACT_RUN" "$R318E_CONTINUITY_PUBLISHED_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$id" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R318E_EVIDENCE_RUN" --jq .head_sha)" = "$R318E_EVIDENCE_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R318E_NORMAL_CI_RUN" --jq .head_sha)" = "$R318E_EVIDENCE_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$R318E_ARTIFACT_ID" --jq .workflow_run.id)" = "$R318E_EVIDENCE_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$R318E_ARTIFACT_ID" --jq .digest)" = "sha256:$R318E_ARTIFACT_DIGEST"

git show "$LANE_COMMIT:tools/_tmp_r317a_paths.txt" > .tmp/r318f/paths.txt
git show "$LANE_COMMIT:tools/_tmp_r317a_identity.tsv" > .tmp/r318f/identity.tsv
test "$(sha256sum .tmp/r318f/paths.txt | awk '{print $1}')" = "$PATHS_SHA"
test "$(sha256sum .tmp/r318f/identity.tsv | awk '{print $1}')" = "$IDENTITY_SHA"
python - <<'PY'
import hashlib
from pathlib import Path
paths=[x.strip().replace('\\','/') for x in Path('.tmp/r318f/paths.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
ids={}
for line in Path('.tmp/r318f/identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    rel,sha,status=line.split('\t')
    rel=rel.replace('\\','/')
    if status!='PASS':
        raise SystemExit(f'bad identity status {rel}')
    ids[rel]=sha.lower()
if len(paths)!=47 or len(set(paths))!=47 or set(paths)!=set(ids):
    raise SystemExit('frozen replay lane is not exactly 47 unique rows')
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):
            h.update(chunk)
    return h.hexdigest()
for rel in paths:
    if digest(rel)!=ids[rel]:
        raise SystemExit(f'replay SHA mismatch: {rel}')
Path('r3_18f_replay_identity.tsv').write_text(
    ''.join(f'{p}\t{ids[p]}\tPASS\n' for p in paths), encoding='utf-8', newline='\n'
)
print('R3_18F_REPLAY_IDENTITY=PASS rows=47')
PY
{
  echo "canonical_main=$BASE_MAIN"
  echo "canonical_tree=$BASE_TREE"
  echo "production_sha=$PROD_SHA"
  echo "production_tree=$PROD_TREE"
  echo "lib_blob=$LIB_BLOB"
  echo "r316b_test_blob=$R316B_TEST_BLOB"
  echo "r318b_test_blob=$R318B_TEST_BLOB"
  echo "r318d_test_blob=$R318D_TEST_BLOB"
  echo "r318f_spec_blob=$R318F_SPEC_BLOB"
  echo "r318e_evidence_head=$R318E_EVIDENCE_HEAD"
  echo "r318e_evidence_run=$R318E_EVIDENCE_RUN"
  echo "r318e_normal_ci_run=$R318E_NORMAL_CI_RUN"
  echo "r318e_artifact_id=$R318E_ARTIFACT_ID"
  echo "r318e_artifact_digest=$R318E_ARTIFACT_DIGEST"
  echo "r318e_continuity_published_run=$R318E_CONTINUITY_PUBLISHED_RUN"
  echo "r318c_evidence_head=$R318C_EVIDENCE_HEAD"
  echo "lane_commit=$LANE_COMMIT"
  echo "replay_identity_sha256=$IDENTITY_SHA"
  echo 'production_mutation=0'
  echo 'cargo_mutation=0'
  echo 'fixture_mutation=0'
  echo 'corpus_mutation=0'
  echo 'support_mutation=0'
} > r3_18f_source_scope.txt
echo 'R3_18F_AUTHORITY_FREEZE=PASS'

echo '== R3.18F pinned Boxcars oracle =='
BOXCARS="$PWD/.tmp/boxcars-r318f"
rm -rf "$BOXCARS"
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
git show "$R318C_EVIDENCE_HEAD:tools/_tmp_r318c_patch.py" > .tmp/r318f/boxcars_base_patch.py
python - <<'PY'
from pathlib import Path
p=Path('.tmp/r318f/boxcars_base_patch.py')
s=p.read_text(encoding='utf-8')
if s.count('    stream_id_bound: i32,\n') != 1:
    raise SystemExit('unexpected inherited stream_id_bound patcher shape')
s=s.replace('    stream_id_bound: i32,\n','    stream_id_bound: u32,\n',1)
s=s.replace('R3_18C','R3_18F').replace('r3_18c','r3_18f')
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18F_BOXCARS_BASE_PATCH_DERIVATION=PASS')
PY
python .tmp/r318f/boxcars_base_patch.py "$BOXCARS"
python tools/_tmp_r318f_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18f_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18f_probe.rs Cargo.toml > r3_18f_boxcars_instrumentation.patch
sha256sum r3_18f_boxcars_instrumentation.patch > r3_18f_boxcars_instrumentation_sha256.txt
cargo check --manifest-path "$BOXCARS/Cargo.toml" --example r3_18f_probe
cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18f_probe --quiet
echo 'R3_18F_BOXCARS_BUILD=PASS'

echo '== R3.18F exact 47 replay scan / 94 source + 47 second-header rows =='
PROBE="$BOXCARS/target/debug/examples/r3_18f_probe"
test -x "$PROBE"
: > .tmp/r318f/oracle.log
while IFS= read -r rel; do
  test -n "$rel"
  MIMIR_R3_18F_LABEL="$rel" "$PROBE" "$PWD/$rel" >> .tmp/r318f/oracle.log 2>&1
done < .tmp/r318f/paths.txt
test "$(grep -c '^R3_18F_ORACLE_PARSE=PASS$' .tmp/r318f/oracle.log)" -eq 47
test "$(grep -c $'^R3_18F_ORACLE\t' .tmp/r318f/oracle.log)" -eq 94
test "$(grep -c $'^R3_18F_SECOND\t' .tmp/r318f/oracle.log)" -eq 47
python tools/_tmp_r318f_analyze.py select \
  .tmp/r318f/oracle.log \
  .tmp/r318f/native_request.tsv \
  r3_18f_selected_witnesses.json \
  r3_18f_selection_summary.json
test "$(wc -l < .tmp/r318f/native_request.tsv | tr -d ' ')" -eq 94
echo 'R3_18F_ORACLE_SCAN=PASS source_rows=94 second_headers=47'

echo '== R3.18F published native header differential =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318f_native_probe.rs crates/mimir-replay/examples/_tmp_r318f_probe.rs
cargo build --locked -p mimir-replay --example _tmp_r318f_probe
target/debug/examples/_tmp_r318f_probe .tmp/r318f/native_request.tsv | tee .tmp/r318f/native1.log
target/debug/examples/_tmp_r318f_probe .tmp/r318f/native_request.tsv > .tmp/r318f/native2.log
cmp .tmp/r318f/native1.log .tmp/r318f/native2.log
test "$(grep -c $'^R3_18F_NATIVE\t' .tmp/r318f/native1.log)" -eq 94
grep -q '^R3_18F_HEADER_TRUNCATION_ROWS=' .tmp/r318f/native1.log
grep -Fx 'R3_18F_UNRESOLVED_STREAM_SYNTHETIC=PASS' .tmp/r318f/native1.log
grep -Fx 'R3_18F_TERMINATOR_NO_LOOKUP_SYNTHETIC=PASS' .tmp/r318f/native1.log
rm crates/mimir-replay/examples/_tmp_r318f_probe.rs
git checkout -- crates/mimir-replay/src crates/mimir-replay/tests
echo 'R3_18F_NATIVE_REPEATABILITY=PASS rows=94'

echo '== R3.18F production regressions =='
cargo test --locked -p mimir-replay --test r3_16b_property_header
cargo test --locked -p mimir-replay --test r3_18b_single_k1_property
cargo test --locked -p mimir-replay --test r3_18d_next_property_control
echo 'R3_18F_PRODUCTION_REGRESSION=PASS'

echo '== R3.18F compare =='
python tools/_tmp_r318f_analyze.py compare \
  r3_18f_selected_witnesses.json \
  .tmp/r318f/native1.log \
  r3_18f_selection_summary.json \
  "$PWD"
grep -Fx 'R3_18F_EVIDENCE=PASS' r3_18f_aggregate.txt
grep -Fx 'R3_18F_R3_18E_WITNESS_RECONSTRUCTION=94/94' r3_18f_aggregate.txt
grep -Fx 'R3_18F_CONTINUATION_HEADER_NATIVE=47/47' r3_18f_aggregate.txt
grep -Fx 'R3_18F_MISMATCH_COUNT=0' r3_18f_aggregate.txt
grep -Fx 'R3_18F_SECOND_PAYLOAD_BITS_CONSUMED=0' r3_18f_aggregate.txt
grep -Fx 'R3_18F_THIRD_PROPERTY_BITS_CONSUMED=0' r3_18f_aggregate.txt
echo 'R3_18F_NATIVE_ORACLE_COMPARE=PASS'

echo '== R3.18F full repository verifier =='
pwsh -NoProfile -File scripts/verify_repo.ps1
echo 'R3_18F_FULL_REPOSITORY_VERIFIER=PASS'

echo '== R3.18F privacy and mutation hard stop =='
git fetch origin main
test "$(git rev-parse origin/main)" = "$BASE_MAIN"
test "$(git rev-parse "${BASE_MAIN}:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
git diff --exit-code "$BASE_MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
test -z "$(git ls-files --others --exclude-standard -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs)"
python - <<'PY'
import json
from pathlib import Path
selected=json.loads(Path('r3_18f_selected_witnesses.json').read_text(encoding='utf-8'))
if len(selected)!=94:
    raise SystemExit('selected row count != 94')
forbidden={'window_hex','raw_payload','player_name','account_name','title_text'}
continuations=0
terminators=0
for row in selected:
    bad=forbidden & set(row)
    if bad:
        raise SystemExit(f'privacy-forbidden selected keys: {bad}')
    if len(row['first_payload_sha256'])!=64 or len(row['control_bit_sha256'])!=64:
        raise SystemExit('missing durable first/control hashes')
    if row['class']=='continuation':
        continuations += 1
        if not isinstance(row['second_header'],dict) or len(row['second_header']['header_sha256'])!=64:
            raise SystemExit('missing durable second-header hash')
    else:
        terminators += 1
        if row['second_header'] is not None:
            raise SystemExit('terminator unexpectedly has second-header object')
if (continuations,terminators)!=(47,47):
    raise SystemExit('privacy lane class counts drift')
comparison=json.loads(Path('r3_18f_comparison.json').read_text(encoding='utf-8'))
assert comparison['native_oracle_mismatch_count']==0
assert comparison['selected_rows']==94
assert comparison['continuation_header_native_success']=='47/47'
assert comparison['second_payload_bits_consumed']==0
assert comparison['third_property_bits_consumed']==0
assert comparison['header_truncation_rows']>=1
print('R3_18F_PRIVACY_HARD_STOP=PASS')
PY
sha256sum \
  r3_18f_source_scope.txt \
  r3_18f_replay_identity.tsv \
  r3_18f_boxcars_instrumentation_sha256.txt \
  r3_18f_selected_witnesses.json \
  r3_18f_selection_summary.json \
  r3_18f_comparison.json \
  r3_18f_aggregate.txt \
  > r3_18f_receipt_sha256.txt
echo 'R3_18F_MUTATION_GATE=PASS production/Cargo/fixture/corpus/support=0/0/0/0/0'

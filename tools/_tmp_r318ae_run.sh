#!/usr/bin/env bash
set -euo pipefail

: "${R318AE_CANONICAL_MAIN:?missing R318AE_CANONICAL_MAIN}"
: "${R318AE_CANONICAL_TREE:?missing R318AE_CANONICAL_TREE}"
: "${R318AE_AD_DECISION_BLOB:?missing R318AE_AD_DECISION_BLOB}"
: "${R318AE_AE_SPEC_BLOB:?missing R318AE_AE_SPEC_BLOB}"

MAIN="$R318AE_CANONICAL_MAIN"
MAIN_TREE="$R318AE_CANONICAL_TREE"
PROD='ccadbf148381c007890d13d5fe8120866a0f40f9'
PROD_TREE='0882601060d0bb6d37fcc03ae7273dcf50dd0be3'
PROD_PARENT='671cd19a7d034b1377de5bed1dfd36600f45c8d7'
LIB_BLOB='1254d5a3b0299677f6661712c371aacf27cdb45d'
AD_TEST_BLOB='013ad6da300cd88f7821b18634736e016af63276'
Z_SHA='81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9'

AC_HEAD='62bc43dd12dbde48fb503cccd4da46dfcf6ae252'
AC_TREE='9d5b550b4bb93688db9f3a67583067adb32425f6'
AC_RUN='32237834815'; AC_JOB='96021661994'; AC_CI='32237834813'; AC_CI_JOB='96021661894'
AC_RECEIPT='32238679393'; AC_RECEIPT_JOB='96024251802'
AC_ART='9359697636'; AC_NAME='r318ac-post-aa-ordinal3-payload-evidence'; AC_SIZE='12010'
AC_DIGEST='sha256:a6914044dfd8991d74b95caeb3507fb2469175c4458c5b50b55395b8ea67b9df'

Y_HEAD='413d6c24f8f390a57c21ed345f3f868c263f413c'
Y_RUN='32076198677'; Y_JOB='95529856476'; Y_ART='9303584468'
Y_NAME='r318y-following-property-header-evidence'
Y_DIGEST='sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29'

AD_BUILDER='32241956973'; AD_BUILDER_JOB='96034261394'
AD_PR_CI='32242293315'; AD_PR_CI_JOB='96035296746'
AD_CLEAN_CI='32242994502'; AD_CLEAN_CI_JOB='96038355071'
AD_MAIN_CI='32242742010'; AD_MAIN_CI_JOB='96036666443'
AD_RECEIPT='32243135866'; AD_RECEIPT_JOB='96037860121'

ROOT="$PWD"
TMP="$(mktemp -d)"
AC_DIR="$TMP/ac"
Y_DIR="$TMP/y"
WORK="$TMP/work"
mkdir -p "$AC_DIR" "$Y_DIR" "$WORK"
trap 'rm -rf "$TMP"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318ae_probe.rs"' EXIT

norm(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }
download_art(){
  local run="$1" name="$2" dir="$3"
  for attempt in 1 2 3; do
    rm -rf "$dir"; mkdir -p "$dir"
    if gh run download "$run" -n "$name" -D "$dir"; then return 0; fi
    test "$attempt" -lt 3
    sleep $((attempt*10))
  done
}

 echo '== R3.18AE canonical authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse "$MAIN^{tree}")" = "$MAIN_TREE"
test "$(git merge-base "$PROD" "$MAIN")" = "$PROD"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$PROD^")" = "$PROD_PARENT"
test "$(git rev-parse "$PROD:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/tests/r3_18ad_post_aa_payload.rs")" = "$AD_TEST_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18AD_DECISION.md")" = "$R318AE_AD_DECISION_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18AE_EXECUTION_SPEC.md")" = "$R318AE_AE_SPEC_BLOB"
git show "$MAIN:docs/continuity/MIMIR_R3_18Z_ADMITTED_HEADER_CONTEXTS.json" > "$WORK/z.json"
test "$(sha256sum "$WORK/z.json" | awk '{print $1}')" = "$Z_SHA"
test "$(git rev-parse "$AC_HEAD^{tree}")" = "$AC_TREE"

for run in "$AC_RUN" "$AC_CI" "$AC_RECEIPT" "$Y_RUN" "$AD_BUILDER" "$AD_PR_CI" "$AD_CLEAN_CI" "$AD_MAIN_CI" "$AD_RECEIPT"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$AC_JOB" "$AC_CI_JOB" "$AC_RECEIPT_JOB" "$Y_JOB" "$AD_BUILDER_JOB" "$AD_PR_CI_JOB" "$AD_CLEAN_CI_JOB" "$AD_MAIN_CI_JOB" "$AD_RECEIPT_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AC_RUN" --jq .head_sha)" = "$AC_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AC_CI" --jq .head_sha)" = "$AC_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AD_PR_CI" --jq .head_sha)" = "$PROD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AD_CLEAN_CI" --jq .head_sha)" = "$PROD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AD_MAIN_CI" --jq .head_sha)" = "$PROD"

for spec in \
  "$AC_ART|$AC_RUN|$AC_HEAD|$AC_NAME|$AC_SIZE|$AC_DIGEST|$AC_DIR" \
  "$Y_ART|$Y_RUN|$Y_HEAD|$Y_NAME|na|$Y_DIGEST|$Y_DIR"; do
  IFS='|' read -r aid run head name size digest dir <<<"$spec"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.id)" = "$run"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.head_sha)" = "$head"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .name)" = "$name"
  test "$(norm "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .digest)")" = "$(norm "$digest")"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .expired)" = false
  if [[ "$size" != na ]]; then test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .size_in_bytes)" = "$size"; fi
  download_art "$run" "$name" "$dir"
done
(cd "$AC_DIR" && test "$(wc -l < r3_18ac_artifact_sha256.txt)" -eq 10 && sha256sum -c r3_18ac_artifact_sha256.txt)
(cd "$Y_DIR" && test "$(wc -l < r3_18y_artifact_sha256.txt)" -eq 9 && sha256sum -c r3_18y_artifact_sha256.txt)
python3 - <<'PY' "$AC_DIR/r3_18ac_payload_summary.json"
import json, sys
s=json.load(open(sys.argv[1],encoding='utf-8'))
assert s['outcome']=='A' and s['rows']==47 and s['oracle_native_mismatch']==0
assert s['witness_reselection']==0 and s['another_control_bits_consumed']==0
assert s['tags']=={'ActiveActor':39,'Int':7,'UniqueId':1}
assert s['unique_id_layouts']==[{'count':1,'payload_width':80,'remote_kind':'Steam','system_id':1}]
print('R3_18AE_AC_FROZEN_AUTHORITY=PASS')
PY

echo '== R3.18AE frozen target reconstruction =='
python3 tools/_tmp_r318ae_driver.py prepare "$AC_DIR" "$Y_DIR" "$WORK/targets.tsv"
test "$(wc -l < "$WORK/targets.tsv")" -eq 47

echo '== R3.18AE published R3.18AD differential =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318ae_probe.rs crates/mimir-replay/examples/_tmp_r318ae_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318ae_probe -- "$WORK/targets.tsv" > "$WORK/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318ae_probe -- "$WORK/targets.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
test "$(grep -c $'^R3_18AE_ROW\t' "$WORK/native1.log")" -eq 47
python3 tools/_tmp_r318ae_driver.py analyze "$WORK/native1.log"
rm -f crates/mimir-replay/examples/_tmp_r318ae_probe.rs

cat > r3_18ae_upstream_receipts.txt <<EOF
R3_18AE_CANONICAL_MAIN=$MAIN
R3_18AE_CANONICAL_TREE=$MAIN_TREE
R3_18AE_PRODUCTION=$PROD
R3_18AE_PRODUCTION_TREE=$PROD_TREE
R3_18AE_AC_AUTH=$AC_RUN/$AC_JOB
R3_18AE_AC_CI=$AC_CI/$AC_CI_JOB
R3_18AE_AC_RECEIPT=$AC_RECEIPT/$AC_RECEIPT_JOB
R3_18AE_AC_ARTIFACT=$AC_ART/$AC_SIZE/$AC_DIGEST
R3_18AE_Y_ARTIFACT=$Y_ART/$Y_DIGEST
R3_18AE_AD_BUILDER=$AD_BUILDER/$AD_BUILDER_JOB
R3_18AE_AD_PR_CI=$AD_PR_CI/$AD_PR_CI_JOB
R3_18AE_AD_CLEAN_CI=$AD_CLEAN_CI/$AD_CLEAN_CI_JOB
R3_18AE_AD_MAIN_CI=$AD_MAIN_CI/$AD_MAIN_CI_JOB
R3_18AE_AD_RECEIPT=$AD_RECEIPT/$AD_RECEIPT_JOB
R3_18AE_Z_CONTRACT=$Z_SHA
EOF
cat > r3_18ae_source_scope.txt <<EOF
R3_18AE_CANONICAL_MAIN=$MAIN
R3_18AE_CANONICAL_TREE=$MAIN_TREE
R3_18AE_PRODUCTION_SHA=$PROD
R3_18AE_PRODUCTION_TREE=$PROD_TREE
R3_18AE_LIB_BLOB=$LIB_BLOB
R3_18AE_AD_TEST_BLOB=$AD_TEST_BLOB
R3_18AE_AD_DECISION_BLOB=$R318AE_AD_DECISION_BLOB
R3_18AE_EXECUTION_SPEC_BLOB=$R318AE_AE_SPEC_BLOB
R3_18AE_FROZEN_ROWS=47
R3_18AE_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF

! grep -R -E '/home/|/Users/|C:\\Users\\|runner/work' r3_18ae_*.txt r3_18ae_*.tsv r3_18ae_*.json >/dev/null

echo '== R3.18AE repository validation =='
cargo fmt --all -- --check
cargo test --locked -p mimir-replay --test r3_18ad_post_aa_payload
cargo test --locked -p mimir-replay --test r3_18aa_post_w_following_header
cargo test --locked -p mimir-replay --test r3_17g_k2_attribute_decoder
cargo test --locked -p mimir-replay --test r3_17c_scalar_attribute_decoder
cargo test --locked -p mimir-replay
cargo check --locked --workspace --all-targets
cargo test --locked --workspace
cargo clippy --locked --workspace --all-targets -- -D warnings
pwsh -NoProfile -File ./scripts/verify_repo.ps1

git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs AGENTS.md MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
sha256sum \
  r3_18ae_source_scope.txt \
  r3_18ae_replay_identity.tsv \
  r3_18ae_frozen_ac_rows.json \
  r3_18ae_published_rows.json \
  r3_18ae_payload_summary.json \
  r3_18ae_negative_controls.txt \
  r3_18ae_aggregate.txt \
  r3_18ae_upstream_receipts.txt > r3_18ae_artifact_sha256.txt
test "$(wc -l < r3_18ae_artifact_sha256.txt)" -eq 8
sha256sum -c r3_18ae_artifact_sha256.txt
cat r3_18ae_aggregate.txt

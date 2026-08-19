#!/usr/bin/env bash
set -euo pipefail
MAIN='f34413e00518b73cf3768cd1914eda8c728306df'
MAIN_TREE='cce54b2040c2a83ebbcce3b31250df5bc82102ca'
PROD='9392240c49f95766c214afee9865fed4155a87a4'
PROD_TREE='968520d480f78c528086e4e31b2ce307f4f8d232'
LIB_BLOB='46523f47f94231362b60f8aee038e943e41c7972'
AA_TEST_BLOB='7df8f84af37d771b12da1334bd195634e4cc6a54'
AC_SPEC_BLOB='bb65dcf14e85c121337ede95619673cc9a5c0b09'
AB_DECISION_BLOB='39c572e302cfab3b87e247f3e3bd441f0c67fbf4'
Z_SHA='81f3072628ef78bcd71dacc1e31b5211aa0de9c32e922e01112b20f4df1425d9'
AB_HEAD='b2f4b73600165b2d83389b6ce43709b64beba52a'
AB_RUN='32230919566'; AB_JOB='96000311036'; AB_CI='32230919652'; AB_CI_JOB='96000311479'
AB_ART='9357559410'; AB_NAME='r318ab-published-aa-following-header-differential-evidence'; AB_SIZE='12607'
AB_DIGEST='sha256:4b6d72b154440ee2b819f5a5ecb6fa3768e086b7ec4ba0d0c53d0e8e3ad23d99'
Y_HEAD='413d6c24f8f390a57c21ed345f3f868c263f413c'; Y_RUN='32076198677'; Y_JOB='95529856476'; Y_ART='9303584468'
Y_NAME='r318y-following-property-header-evidence'; Y_DIGEST='sha256:46f3253cd50c95cfc05a39f2b45ed647b3d45d3951b0af78da3cf03803fcfd29'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'; BOXCARS_FRAME='6f2ff153d3a27cdacccc65e3f23851489077a7d8'; BOXCARS_ATTR='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'
R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
ROOT="$PWD"; TMP="$(mktemp -d)"; AB_DIR="$TMP/ab"; Y_DIR="$TMP/y"; WORK="$TMP/work"; BOXCARS="$TMP/boxcars"
mkdir -p "$AB_DIR" "$Y_DIR" "$WORK"
trap 'rm -rf "$TMP"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318ac_probe.rs"' EXIT
norm(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }
download_art(){ local run="$1" name="$2" dir="$3"; for attempt in 1 2 3; do rm -rf "$dir"; mkdir -p "$dir"; if gh run download "$run" -n "$name" -D "$dir"; then return 0; fi; test "$attempt" -lt 3; sleep $((attempt*10)); done; }
echo '== R3.18AC authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse "$MAIN^{tree}")" = "$MAIN_TREE"
test "$(git merge-base "$PROD" "$MAIN")" = "$PROD"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$MAIN:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$MAIN:crates/mimir-replay/tests/r3_18aa_post_w_following_header.rs")" = "$AA_TEST_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18AC_EXECUTION_SPEC.md")" = "$AC_SPEC_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18AB_DECISION.md")" = "$AB_DECISION_BLOB"
git show "$MAIN:docs/continuity/MIMIR_R3_18Z_ADMITTED_HEADER_CONTEXTS.json" > "$WORK/z.json"
test "$(sha256sum "$WORK/z.json" | awk '{print $1}')" = "$Z_SHA"
mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=('.github/workflows/_tmp_r318ac_evidence.yml' 'tools/_tmp_r318ac_boxcars.py' 'tools/_tmp_r318ac_driver.py' 'tools/_tmp_r318ac_probe.rs' 'tools/_tmp_r318ac_run.sh')
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 5
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs AGENTS.md MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort); test "${#prod_drift[@]}" -eq 0
for run in "$AB_RUN" "$AB_CI" "$Y_RUN"; do test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success; done
for job in "$AB_JOB" "$AB_CI_JOB" "$Y_JOB"; do test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success; done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AB_RUN" --jq .head_sha)" = "$AB_HEAD"
for spec in "$AB_ART|$AB_RUN|$AB_HEAD|$AB_NAME|$AB_SIZE|$AB_DIGEST|$AB_DIR" "$Y_ART|$Y_RUN|$Y_HEAD|$Y_NAME|na|$Y_DIGEST|$Y_DIR"; do
 IFS='|' read -r aid run head name size digest dir <<<"$spec"
 test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.id)" = "$run"
 test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.head_sha)" = "$head"
 test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .name)" = "$name"
 test "$(norm "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .digest)")" = "$(norm "$digest")"
 test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .expired)" = false
 if [[ "$size" != na ]]; then test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .size_in_bytes)" = "$size"; fi
 download_art "$run" "$name" "$dir"
done
(cd "$AB_DIR" && test "$(wc -l < r3_18ab_artifact_sha256.txt)" -eq 9 && sha256sum -c r3_18ab_artifact_sha256.txt)
(cd "$Y_DIR" && test "$(wc -l < r3_18y_artifact_sha256.txt)" -eq 9 && sha256sum -c r3_18y_artifact_sha256.txt)
python3 tools/_tmp_r318ac_driver.py prepare "$Y_DIR" "$AB_DIR" "$WORK/targets.tsv"
awk -F '\t' 'BEGIN{OFS="\t"}{print $1,$2,$3,$4,$6}' "$WORK/targets.tsv" > "$WORK/oracle_requests.tsv"
test "$(wc -l < "$WORK/oracle_requests.tsv")" -eq 47
echo 'R3_18AC_AUTHORITY_FREEZE=PASS'
echo '== pinned Boxcars ordinal-3 payload oracle =='
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"; git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME"; test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR"
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$WORK/base_patch.py"
python3 - "$WORK/base_patch.py" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
assert s.count('    stream_id_bound: i32,\n')==1
s=s.replace('    stream_id_bound: i32,\n','    stream_id_bound: u32,\n',1)
s=s.replace('R3_18C','R3_18Y').replace('r3_18c','r3_18y')
needle='                        if r3_18y_property_ordinal == 1 {\n'; assert s.count(needle)==1
s=s.replace(needle,'                        if false && r3_18y_property_ordinal == 1 {\n',1)
p.write_text(s,encoding='utf-8',newline='\n')
PY
python3 "$WORK/base_patch.py" "$BOXCARS"; git show "$Y_HEAD:tools/_tmp_r318y_extend_boxcars.py" > "$WORK/y_extend.py"; python3 "$WORK/y_extend.py" "$BOXCARS"; python3 tools/_tmp_r318ac_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18y_probe.rs; git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18y_probe.rs Cargo.toml > "$WORK/ac_boxcars.patch"
sha256sum "$WORK/ac_boxcars.patch" | sed 's#  .*#  r318ac_boxcars_payload_instrumentation.patch#' > r3_18ac_boxcars_instrumentation_sha256.txt
RUSTUP_TOOLCHAIN=stable cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18y_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18y_probe"; test -x "$PROBE"; : > "$WORK/oracle.log"
while IFS=$'\t' read -r rel frame actor actor_object property_start; do MIMIR_R3_18Y_LABEL="$rel" MIMIR_R3_18Y_TARGET_FRAME="$frame" MIMIR_R3_18Y_TARGET_ACTOR_ORDINAL="$actor" MIMIR_R3_18Y_TARGET_ACTOR_OBJECT="$actor_object" MIMIR_R3_18Y_TARGET_PROPERTY_START="$property_start" "$PROBE" "$ROOT/$rel" >> "$WORK/oracle.log" 2>&1; done < "$WORK/oracle_requests.tsv"
test "$(grep -c $'^R3_18AC_ORACLE\t' "$WORK/oracle.log")" -eq 47
echo 'R3_18AC_BOXCARS_ORACLE=PASS rows=47'
echo '== native AA boundary + one payload primitive =='
mkdir -p crates/mimir-replay/examples; cp tools/_tmp_r318ac_probe.rs crates/mimir-replay/examples/_tmp_r318ac_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318ac_probe -- "$WORK/targets.tsv" > "$WORK/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318ac_probe -- "$WORK/targets.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"; test "$(grep -c $'^R3_18AC_NATIVE\t' "$WORK/native1.log")" -eq 47; rm -f crates/mimir-replay/examples/_tmp_r318ac_probe.rs
python3 tools/_tmp_r318ac_driver.py analyze "$WORK/oracle.log" "$WORK/native1.log"
cat > r3_18ac_upstream_receipts.txt <<EOF
R3_18AC_MAIN=$MAIN
R3_18AC_MAIN_TREE=$MAIN_TREE
R3_18AC_PRODUCTION=$PROD
R3_18AC_PRODUCTION_TREE=$PROD_TREE
R3_18AC_AB_AUTH=$AB_RUN/$AB_JOB
R3_18AC_AB_CI=$AB_CI/$AB_CI_JOB
R3_18AC_AB_ARTIFACT=$AB_ART/$AB_SIZE/$AB_DIGEST
R3_18AC_Y_ARTIFACT=$Y_ART/$Y_DIGEST
R3_18AC_BOXCARS=$BOXCARS_SHA
R3_18AC_Z_CONTRACT=$Z_SHA
EOF
cat > r3_18ac_source_scope.txt <<EOF
R3_18AC_BASE_MAIN=$MAIN
R3_18AC_BASE_TREE=$MAIN_TREE
R3_18AC_PRODUCTION_SHA=$PROD
R3_18AC_PRODUCTION_TREE=$PROD_TREE
R3_18AC_LIB_BLOB=$LIB_BLOB
R3_18AC_AA_TEST_BLOB=$AA_TEST_BLOB
R3_18AC_AB_DECISION_BLOB=$AB_DECISION_BLOB
R3_18AC_SPEC_BLOB=$AC_SPEC_BLOB
R3_18AC_CHANGED_TEMP_FILES=5
R3_18AC_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF
! grep -R -E '/home/|/Users/|C:\\Users\\|runner/work' r3_18ac_*.txt r3_18ac_*.tsv r3_18ac_*.json >/dev/null
echo '== R3.18AC validation =='
cargo fmt --all -- --check
cargo test --locked -p mimir-replay --test r3_18aa_post_w_following_header
cargo test --locked -p mimir-replay --test r3_17g_k2_attribute_decoder
cargo test --locked -p mimir-replay --test r3_17c_scalar_attribute_decoder
pwsh -File ./scripts/verify_repo.ps1
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs AGENTS.md MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
sha256sum r3_18ac_source_scope.txt r3_18ac_replay_identity.tsv r3_18ac_frozen_ab_rows.json r3_18ac_boxcars_instrumentation_sha256.txt r3_18ac_payload_rows.json r3_18ac_payload_summary.json r3_18ac_unique_id_layout.json r3_18ac_negative_controls.txt r3_18ac_aggregate.txt r3_18ac_upstream_receipts.txt > r3_18ac_artifact_sha256.txt
test "$(wc -l < r3_18ac_artifact_sha256.txt)" -eq 10; sha256sum -c r3_18ac_artifact_sha256.txt; cat r3_18ac_aggregate.txt

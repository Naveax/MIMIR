#!/usr/bin/env bash
set -euo pipefail

MAIN='d0f2678271984acf5dc69f6456ccaaf443bb3113'
MAIN_TREE='0c2694f49427d34c5219eb921ed1c8c66cae30d5'
PROD='58872e94f00ef094807f21ab2ff984ac66b97d91'
PROD_TREE='d6965d77903ea99dad0465bb350b6a673ee7dd00'
LIB_BLOB='d997ae8c3ad2d201b3f43c6ccca7ded2ef03b73b'
W_TEST_BLOB='ac176135c2e6ed56f0b91bdde8c7548f17641cf0'
X_DECISION_BLOB='d9498deb66b70b6a79cf073af6f21065d4f6e3d5'
Y_SPEC_BLOB='a66fa6cc2aac081f552b2f1ab99146ca3dd0b72f'

X_HEAD='75259a9b3705b16b21d89b975ee584a7765e8134'; X_TREE='fe90b38c98039cd1dde05b96613645d0ab69a8a9'
X_RUN='32065498170'; X_JOB='95496521378'; X_CI='32065498109'; X_CI_JOB='95496518762'
X_ART='9299790869'; X_ART_NAME='r318x-published-following-payload-control-differential-evidence'; X_SIZE='19761'; X_DIGEST='sha256:ac32daa92d88f1753da34123d074dcd8f3c98c58fdeb0b91f89cb837ea02ebff'
X_ADM='32066091573'; X_ADM_JOB='95498450308'
X_CAND_CI='32066205293'; X_CAND_CI_JOB='95498811907'; X_CAND_KA='32066205348'; X_CAND_KA_JOB='95498812246'
X_PR_CI='32066574561'; X_PR_CI_JOB='95499992890'; X_PR_KA='32066575338'; X_PR_KA_JOB='95499994716'
X_PUB_CI='32066987127'; X_PUB_CI_JOB='95501289757'; X_PUB_KA='32066988370'; X_PUB_KA_JOB='95501294185'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"; WORK="$ROOT/.tmp/r318y"; X_DIR="$WORK/x"; BOXCARS="$WORK/boxcars"
rm -rf "$WORK"; mkdir -p "$X_DIR"
trap 'rm -rf "$WORK"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318y_probe.rs"' EXIT
norm_digest(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }
download_x(){ for attempt in 1 2 3; do rm -rf "$X_DIR"; mkdir -p "$X_DIR"; if gh run download "$X_RUN" -n "$X_ART_NAME" -D "$X_DIR"; then echo "R3_18Y_X_DOWNLOAD_ATTEMPT=$attempt"; return 0; fi; sleep $((attempt*10)); done; return 1; }

echo '== R3.18Y authority freeze =='
git fetch origin main evidence/r318c-loop-control --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git merge-base HEAD "$MAIN")" = "$MAIN"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$MAIN:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$MAIN:crates/mimir-replay/tests/r3_18w_following_payload_control.rs")" = "$W_TEST_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18X_DECISION.md")" = "$X_DECISION_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18Y_EXECUTION_SPEC.md")" = "$Y_SPEC_BLOB"
test "$(git rev-parse origin/evidence/r318c-loop-control)" = "$R318C_HEAD"
test "$(git rev-parse "$R318C_HEAD:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"
mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=( '.github/workflows/_tmp_r318y_evidence.yml' 'tools/_tmp_r318y_analyze.py' 'tools/_tmp_r318y_extend_boxcars.py' 'tools/_tmp_r318y_native_probe.rs' 'tools/_tmp_r318y_run.sh' )
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 5
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort); test "${#prod_drift[@]}" -eq 0
for run in "$X_RUN" "$X_CI" "$X_ADM" "$X_CAND_CI" "$X_CAND_KA" "$X_PR_CI" "$X_PR_KA" "$X_PUB_CI" "$X_PUB_KA"; do test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success; done
for job in "$X_JOB" "$X_CI_JOB" "$X_ADM_JOB" "$X_CAND_CI_JOB" "$X_CAND_KA_JOB" "$X_PR_CI_JOB" "$X_PR_KA_JOB" "$X_PUB_CI_JOB" "$X_PUB_KA_JOB"; do test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success; done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$X_RUN" --jq .head_sha)" = "$X_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$X_RUN" --jq .head_commit.tree_id)" = "$X_TREE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$X_PUB_CI" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$X_PUB_KA" --jq .head_sha)" = "$MAIN"
echo 'R3_18Y_AUTHORITY_FREEZE=PASS'

echo '== immutable R3.18X lane =='
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$X_ART" --jq .workflow_run.id)" = "$X_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$X_ART" --jq .workflow_run.head_sha)" = "$X_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$X_ART" --jq .name)" = "$X_ART_NAME"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$X_ART" --jq .size_in_bytes)" = "$X_SIZE"
test "$(norm_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$X_ART" --jq .digest)")" = "$(norm_digest "$X_DIGEST")"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$X_ART" --jq .expired)" = false
download_x
(cd "$X_DIR" && test "$(wc -l < r3_18x_artifact_sha256.txt)" -eq 8 && sha256sum -c r3_18x_artifact_sha256.txt)
grep -Fqx 'R3_18X_OUTCOME=A' "$X_DIR/r3_18x_aggregate.txt"
grep -Fqx 'R3_18X_FROZEN_ROWS=47/47' "$X_DIR/r3_18x_aggregate.txt"
grep -Fqx 'R3_18X_CONTROL_TRUE=47' "$X_DIR/r3_18x_aggregate.txt"
grep -Fqx 'R3_18X_PUBLISHED_W_FROZEN_V_MISMATCH=0' "$X_DIR/r3_18x_aggregate.txt"
cp "$X_DIR/r3_18x_replay_identity.tsv" r3_18y_replay_identity.tsv
cp "$X_DIR/r3_18x_frozen_witnesses.json" r3_18y_frozen_witnesses.json
cp "$X_DIR/r3_18x_targets.tsv" "$WORK/targets.tsv"
python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18y_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel,expected,status=line.split('\t'); assert status=='PASS' and not rel.startswith('/') and '..' not in Path(rel).parts
    assert hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower()==expected.lower(), rel
    rows.append(rel.replace('\\','/'))
assert len(rows)==47 and len(set(rows))==47
print('R3_18Y_REPLAY_IDENTITY=PASS rows=47')
PY
awk -F '\t' 'BEGIN{OFS="\t"}{print $1,$2,$3,$4,$7}' "$WORK/targets.tsv" > "$WORK/oracle_requests.tsv"
test "$(wc -l < "$WORK/oracle_requests.tsv")" -eq 47

echo '== pinned Boxcars ordinal-3 header oracle =='
rm -rf "$BOXCARS"; git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
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
s=s.replace('R3_18C','R3_18Y').replace('r3_18c','r3_18y')
needle='                        if r3_18y_property_ordinal == 1 {\n'
if s.count(needle)!=1: raise SystemExit('ordinal-1 inherited emission shape')
s=s.replace(needle,'                        if false && r3_18y_property_ordinal == 1 {\n',1)
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18Y_BOXCARS_BASE_DERIVATION=PASS')
PY
python3 "$WORK/base_patch.py" "$BOXCARS"
python3 tools/_tmp_r318y_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18y_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18y_probe.rs Cargo.toml > "$WORK/r3_18y_boxcars.patch"
Y_PATCH_SHA="$(sha256sum "$WORK/r3_18y_boxcars.patch" | awk '{print $1}')"
printf '%s  r3_18y_boxcars_header_instrumentation.patch\n' "$Y_PATCH_SHA" > r3_18y_boxcars_instrumentation_sha256.txt
RUSTUP_TOOLCHAIN=stable cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18y_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18y_probe"; test -x "$PROBE"; : > "$WORK/oracle.log"
while IFS=$'\t' read -r rel frame actor actor_object property_start; do
  MIMIR_R3_18Y_LABEL="$rel" MIMIR_R3_18Y_TARGET_FRAME="$frame" MIMIR_R3_18Y_TARGET_ACTOR_ORDINAL="$actor" MIMIR_R3_18Y_TARGET_ACTOR_OBJECT="$actor_object" MIMIR_R3_18Y_TARGET_PROPERTY_START="$property_start" "$PROBE" "$ROOT/$rel" >> "$WORK/oracle.log" 2>&1
done < "$WORK/oracle_requests.tsv"
test "$(grep -c '^R3_18Y_ORACLE_PARSE=PASS$' "$WORK/oracle.log")" -eq 47
test "$(grep -c $'^R3_18Y_HEADER\t' "$WORK/oracle.log")" -eq 47
echo 'R3_18Y_BOXCARS_ORACLE=PASS headers=47'

echo '== native published W + one header primitive =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318y_native_probe.rs crates/mimir-replay/examples/_tmp_r318y_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318y_probe -- "$WORK/targets.tsv" > "$WORK/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318y_probe -- "$WORK/targets.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
test "$(grep -c $'^R3_18Y_NATIVE\t' "$WORK/native1.log")" -eq 47
rm -f crates/mimir-replay/examples/_tmp_r318y_probe.rs
python3 tools/_tmp_r318y_analyze.py "$WORK/oracle.log" "$WORK/native1.log" r3_18y_header_rows.json r3_18y_header_summary.json r3_18y_negative_controls.txt r3_18y_aggregate.txt

cat > r3_18y_upstream_receipts.txt <<EOF
R3_18Y_MAIN=$MAIN
R3_18Y_MAIN_TREE=$MAIN_TREE
R3_18Y_PRODUCTION=$PROD
R3_18Y_PRODUCTION_TREE=$PROD_TREE
R3_18Y_X_AUTH=$X_RUN/$X_JOB
R3_18Y_X_CI=$X_CI/$X_CI_JOB
R3_18Y_X_ADMISSION=$X_ADM/$X_ADM_JOB
R3_18Y_X_CANDIDATE_CI=$X_CAND_CI/$X_CAND_CI_JOB
R3_18Y_X_CANDIDATE_KA=$X_CAND_KA/$X_CAND_KA_JOB
R3_18Y_X_PR_CI=$X_PR_CI/$X_PR_CI_JOB
R3_18Y_X_PR_KA=$X_PR_KA/$X_PR_KA_JOB
R3_18Y_X_PUBLISHED_CI=$X_PUB_CI/$X_PUB_CI_JOB
R3_18Y_X_PUBLISHED_KA=$X_PUB_KA/$X_PUB_KA_JOB
R3_18Y_X_ARTIFACT=$X_ART/$X_SIZE/$X_DIGEST
EOF
cat > r3_18y_source_scope.txt <<EOF
R3_18Y_BASE_MAIN=$MAIN
R3_18Y_BASE_TREE=$MAIN_TREE
R3_18Y_PRODUCTION_SHA=$PROD
R3_18Y_PRODUCTION_TREE=$PROD_TREE
R3_18Y_LIB_BLOB=$LIB_BLOB
R3_18Y_W_TEST_BLOB=$W_TEST_BLOB
R3_18Y_X_DECISION_BLOB=$X_DECISION_BLOB
R3_18Y_SPEC_BLOB=$Y_SPEC_BLOB
R3_18Y_BOXCARS_SHA=$BOXCARS_SHA
R3_18Y_BOXCARS_INSTRUMENTATION_SHA256=$Y_PATCH_SHA
R3_18Y_CHANGED_TEMP_FILES=5
R3_18Y_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF
! grep -R -E '/home/|/Users/|C:\\Users\\|runner/work' r3_18y_*.txt r3_18y_*.tsv r3_18y_*.json >/dev/null

echo '== R3.18Y validation =='
cargo fmt --all -- --check
cargo test --locked -p mimir-replay --test r3_18w_following_payload_control
cargo test --locked -p mimir-replay
cargo check --locked --workspace
cargo test --locked --workspace
cargo clippy --locked --workspace --all-targets -- -D warnings
pwsh -File ./scripts/verify_repo.ps1
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
sha256sum r3_18y_source_scope.txt r3_18y_replay_identity.tsv r3_18y_frozen_witnesses.json r3_18y_boxcars_instrumentation_sha256.txt r3_18y_header_rows.json r3_18y_header_summary.json r3_18y_negative_controls.txt r3_18y_aggregate.txt r3_18y_upstream_receipts.txt > r3_18y_artifact_sha256.txt
test "$(wc -l < r3_18y_artifact_sha256.txt)" -eq 9
sha256sum -c r3_18y_artifact_sha256.txt
cat r3_18y_aggregate.txt
python3 - <<'PY'
import json
x=json.load(open('r3_18y_header_summary.json',encoding='utf-8'))
print('R3_18Y_CONTEXT_SUMMARY',json.dumps({'unique_exact_contexts':x['unique_exact_contexts'],'tags':x['tags']},sort_keys=True))
PY

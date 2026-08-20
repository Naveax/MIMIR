#!/usr/bin/env bash
set -euo pipefail

BASE='b419503b5ceb8c44af207f645232570b1c9f2e6d'
BASE_TREE='8bcdedf47233b0e6db605c6c532677d0f8166801'
PROD='2d351e8ceb601e2fbe515d2977b2103a4b2c7976'
PROD_TREE='4123820ce6537f2d4942cd0b5f72b52e43b96c1d'
LIB_BLOB='db923ebcb419d278f4ab0144fe7ed15b298b60fa'
AG_TEST_BLOB='3f3e1c8f3f6deb7f2558862a1032f8a102131443'
AI_SPEC_BLOB='dd064744b86ce4718d389c2bd4bf080b962b16d7'
AH_DECISION_BLOB='0645afccaf1fa40050349d869309ce3c95640184'

AH_HEAD='7389831c626c078d60178c94461ac39e5f427bd5'
AH_TREE='6121bd7d0fab5a5a338a75343d92f11876f71c8b'
AH_RUN='32405516670'
AH_JOB='96543562860'
AH_CI='32406901661'
AH_CI_JOB='96547992406'
AH_ART='9420166543'
AH_ART_NAME='r318ah-published-ag-differential-evidence'
AH_SIZE='11686'
AH_DIGEST='sha256:b7b9100489a7ae20a959450d0d80fbcda281aee288a00d0c7edd18930cc60df1'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318ai"
AH_DIR="$WORK/ah"
BOXCARS="$WORK/boxcars"
rm -rf "$WORK"
mkdir -p "$AH_DIR"
trap 'rm -rf "$WORK"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318ai_probe.rs"' EXIT
norm_digest(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

download_ah(){
  for attempt in 1 2 3; do
    rm -rf "$AH_DIR"; mkdir -p "$AH_DIR"
    if gh run download "$AH_RUN" -n "$AH_ART_NAME" -D "$AH_DIR"; then
      echo "R3_18AI_AH_DOWNLOAD_ATTEMPT=$attempt"
      return 0
    fi
    sleep $((attempt*10))
  done
  return 1
}

echo '== R3.18AI authority freeze =='
git fetch origin main evidence/r318c-loop-control --force
test "$(git rev-parse origin/main)" = "$BASE"
test "$(git rev-parse origin/main^{tree})" = "$BASE_TREE"
test "$(git merge-base HEAD "$BASE")" = "$BASE"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$BASE:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$BASE:crates/mimir-replay/tests/r3_18ag_post_ad_payload_control.rs")" = "$AG_TEST_BLOB"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AI_EXECUTION_SPEC.md")" = "$AI_SPEC_BLOB"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AH_DECISION.md")" = "$AH_DECISION_BLOB"
test "$(git rev-parse origin/evidence/r318c-loop-control)" = "$R318C_HEAD"
test "$(git rev-parse "$R318C_HEAD:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"

mapfile -t changed < <(git diff --name-only "$BASE" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318ai_evidence.yml'
  '.github/workflows/_tmp_r318ai_trigger.txt'
  'tools/_tmp_r318ai_analyze.py'
  'tools/_tmp_r318ai_extend_boxcars.py'
  'tools/_tmp_r318ai_native_probe.rs'
  'tools/_tmp_r318ai_run.sh'
)
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 6
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$BASE" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$BASE" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

for pair in "$AH_RUN:$AH_JOB" "$AH_CI:$AH_CI_JOB"; do
  run="${pair%%:*}"; job="${pair##*:}"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AH_RUN" --jq .head_sha)" = "$AH_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AH_RUN" --jq .head_commit.tree_id)" = "$AH_TREE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AH_CI" --jq .head_sha)" = "$AH_HEAD"
echo 'R3_18AI_AUTHORITY_FREEZE=PASS'

echo '== immutable R3.18AH lane =='
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AH_ART" --jq .workflow_run.id)" = "$AH_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AH_ART" --jq .workflow_run.head_sha)" = "$AH_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AH_ART" --jq .name)" = "$AH_ART_NAME"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AH_ART" --jq .size_in_bytes)" = "$AH_SIZE"
test "$(norm_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AH_ART" --jq .digest)")" = "$(norm_digest "$AH_DIGEST")"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AH_ART" --jq .expired)" = false
download_ah
(
  cd "$AH_DIR"
  test "$(wc -l < r3_18ah_artifact_sha256.txt)" -eq 9
  sha256sum -c r3_18ah_artifact_sha256.txt
  grep -Fqx 'R3_18AH_OUTCOME=A' r3_18ah_aggregate.txt
  grep -Fqx 'R3_18AH_FROZEN_ROWS=47/47' r3_18ah_aggregate.txt
  grep -Fqx 'R3_18AH_PUBLISHED_AG_EXACT=47/47' r3_18ah_aggregate.txt
  grep -Fqx 'R3_18AH_CONTROL_FALSE=0' r3_18ah_aggregate.txt
  grep -Fqx 'R3_18AH_CONTROL_TRUE=47' r3_18ah_aggregate.txt
  grep -Fqx 'R3_18AH_WITNESS_RESELECTION=0' r3_18ah_aggregate.txt
)
cp "$AH_DIR/r3_18ah_replay_identity.tsv" r3_18ai_replay_identity.tsv
cp "$AH_DIR/r3_18ah_comparison.json" r3_18ai_frozen_witnesses.json

python3 - "$AH_DIR/r3_18ah_frozen_af_targets.tsv" "$AH_DIR/r3_18ah_comparison.json" "$WORK/targets.tsv" "$WORK/oracle_requests.tsv" <<'PY'
import json, sys
from pathlib import Path
src, comp_path, target_out, oracle_out = map(Path, sys.argv[1:])
comp = json.loads(comp_path.read_text(encoding='utf-8'))
rows = comp['rows']
by_label = {r['label']: r for r in rows}
assert len(rows) == 47 and len(by_label) == 47
out=[]; oracle=[]; seen=set()
for line in src.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    f=line.split('\t'); assert len(f)==9, f
    label, frame, actor_ord, actor_obj, first_start, payload_start, payload_end, width, tag=f
    assert label not in seen; seen.add(label)
    r=by_label[label]
    assert int(payload_end)==int(r['prior_stop'])==int(r['frozen_prior_stop'])
    assert r['published_value'] is True and r['frozen_value'] is True
    assert int(r['published_start'])==int(r['frozen_start'])
    assert int(r['published_end'])==int(r['frozen_end'])==int(r['published_stop'])
    out.append('\t'.join(map(str,[label,frame,actor_ord,actor_obj,first_start,r['prior_stop'],r['published_start'],r['published_end'],r['published_stop']])))
    oracle.append('\t'.join(map(str,[label,frame,actor_ord,actor_obj,r['published_start']])))
assert len(out)==47 and len(seen)==47
Path(target_out).write_text('\n'.join(out)+'\n',encoding='utf-8',newline='\n')
Path(oracle_out).write_text('\n'.join(oracle)+'\n',encoding='utf-8',newline='\n')
print('R3_18AI_FROZEN_TARGET_DERIVATION=PASS rows=47 reselection=0')
PY

python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18ai_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel, expected, status = line.split('\t')
    assert status == 'PASS' and not rel.startswith('/') and '..' not in Path(rel).parts
    assert hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower() == expected.lower(), rel
    rows.append(rel.replace('\\','/'))
assert len(rows)==47 and len(set(rows))==47
print('R3_18AI_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== pinned Boxcars ordinal-4 header oracle =='
rm -rf "$BOXCARS"
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
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
s=s.replace('R3_18C','R3_18AI').replace('r3_18c','r3_18ai')
needle='                        if r3_18ai_property_ordinal == 1 {\n'
if s.count(needle)!=1: raise SystemExit('ordinal-1 inherited emission shape')
s=s.replace(needle,'                        if false && r3_18ai_property_ordinal == 1 {\n',1)
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18AI_BOXCARS_BASE_DERIVATION=PASS')
PY
python3 "$WORK/base_patch.py" "$BOXCARS"
python3 tools/_tmp_r318ai_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18ai_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18ai_probe.rs Cargo.toml > "$WORK/r3_18ai_boxcars.patch"
AI_PATCH_SHA="$(sha256sum "$WORK/r3_18ai_boxcars.patch" | awk '{print $1}')"
printf '%s  r3_18ai_boxcars_header_instrumentation.patch\n' "$AI_PATCH_SHA" > r3_18ai_boxcars_instrumentation_sha256.txt
RUSTUP_TOOLCHAIN=stable cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18ai_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18ai_probe"
test -x "$PROBE"
: > "$WORK/oracle.log"
while IFS=$'\t' read -r rel frame actor actor_object property_start; do
  MIMIR_R3_18AI_LABEL="$rel" \
  MIMIR_R3_18AI_TARGET_FRAME="$frame" \
  MIMIR_R3_18AI_TARGET_ACTOR_ORDINAL="$actor" \
  MIMIR_R3_18AI_TARGET_ACTOR_OBJECT="$actor_object" \
  MIMIR_R3_18AI_TARGET_PROPERTY_START="$property_start" \
  "$PROBE" "$ROOT/$rel" >> "$WORK/oracle.log" 2>&1
done < "$WORK/oracle_requests.tsv"
test "$(grep -c '^R3_18AI_ORACLE_PARSE=PASS$' "$WORK/oracle.log")" -eq 47
test "$(grep -c $'^R3_18AI_HEADER\t' "$WORK/oracle.log")" -eq 47
echo 'R3_18AI_BOXCARS_ORACLE=PASS headers=47 ordinal=4'

echo '== native published AG + one stateless header =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318ai_native_probe.rs crates/mimir-replay/examples/_tmp_r318ai_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318ai_probe -- "$WORK/targets.tsv" > "$WORK/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318ai_probe -- "$WORK/targets.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
test "$(grep -c $'^R3_18AI_NATIVE\t' "$WORK/native1.log")" -eq 47
rm -f crates/mimir-replay/examples/_tmp_r318ai_probe.rs
python3 tools/_tmp_r318ai_analyze.py "$WORK/oracle.log" "$WORK/native1.log" r3_18ai_header_rows.json r3_18ai_header_summary.json r3_18ai_negative_controls.txt r3_18ai_aggregate.txt

cat > r3_18ai_upstream_receipts.txt <<EOF
R3_18AI_BASE_MAIN=$BASE
R3_18AI_BASE_TREE=$BASE_TREE
R3_18AI_PRODUCTION=$PROD
R3_18AI_PRODUCTION_TREE=$PROD_TREE
R3_18AI_AH_HEAD=$AH_HEAD
R3_18AI_AH_TREE=$AH_TREE
R3_18AI_AH_AUTH=$AH_RUN/$AH_JOB
R3_18AI_AH_CI=$AH_CI/$AH_CI_JOB
R3_18AI_AH_ARTIFACT=$AH_ART/$AH_SIZE/$AH_DIGEST
EOF
cat > r3_18ai_source_scope.txt <<EOF
R3_18AI_BASE_MAIN=$BASE
R3_18AI_BASE_TREE=$BASE_TREE
R3_18AI_PRODUCTION_SHA=$PROD
R3_18AI_PRODUCTION_TREE=$PROD_TREE
R3_18AI_LIB_BLOB=$LIB_BLOB
R3_18AI_AG_TEST_BLOB=$AG_TEST_BLOB
R3_18AI_SPEC_BLOB=$AI_SPEC_BLOB
R3_18AI_AH_DECISION_BLOB=$AH_DECISION_BLOB
R3_18AI_BOXCARS_SHA=$BOXCARS_SHA
R3_18AI_BOXCARS_INSTRUMENTATION_SHA256=$AI_PATCH_SHA
R3_18AI_CHANGED_TEMP_FILES=6
R3_18AI_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
EOF
! grep -R -E '/home/|/Users/|C:\\Users\\|runner/work' r3_18ai_*.txt r3_18ai_*.tsv r3_18ai_*.json >/dev/null

echo '== R3.18AI validation =='
cargo fmt --all -- --check
cargo test --locked -p mimir-replay --test r3_16b_property_header
cargo test --locked -p mimir-replay --test r3_18ag_post_ad_payload_control
cargo test --locked -p mimir-replay
cargo check --locked --workspace
cargo test --locked --workspace
cargo clippy --locked --workspace --all-targets -- -D warnings
pwsh -File ./scripts/verify_repo.ps1
git diff --exit-code "$BASE" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
sha256sum r3_18ai_source_scope.txt r3_18ai_replay_identity.tsv r3_18ai_frozen_witnesses.json r3_18ai_boxcars_instrumentation_sha256.txt r3_18ai_header_rows.json r3_18ai_header_summary.json r3_18ai_negative_controls.txt r3_18ai_aggregate.txt r3_18ai_upstream_receipts.txt > r3_18ai_artifact_sha256.txt
test "$(wc -l < r3_18ai_artifact_sha256.txt)" -eq 9
sha256sum -c r3_18ai_artifact_sha256.txt
cat r3_18ai_aggregate.txt
python3 - <<'PY'
import json
x=json.load(open('r3_18ai_header_summary.json',encoding='utf-8'))
print('R3_18AI_CONTEXT_SUMMARY',json.dumps({'unique_exact_contexts':x['unique_exact_contexts'],'tags':x['tags']},sort_keys=True))
PY

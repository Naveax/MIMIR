#!/usr/bin/env bash
set -euo pipefail

BASE='02233c8125e658513dcb068370c48b1e8f15a01c'
BASE_TREE='fc9293d821dd3e6e269763c3c0ab091428c29490'
PROD='f20f529e3ada6e9a671ea91e5676a17a00770145'
PROD_TREE='98c675811cca4e4d7f0122c762f371548c9266c2'
LIB_BLOB='a4001e631b306ba0297fb8a4abc97778f81659c2'
AK_TEST_BLOB='9014505e1736498ee5e2ef7a1ce6118030580202'
AL_SPEC_BLOB='d079d0f20e939a7f5f5a80c55bb8897032610567'
AJ_CONTRACT_BLOB='013d0709cc7df8e1ee79167995448b1cd8058137'
AJ_CONTRACT_SHA256='cc85f9330b6d4190817d61c094d97bd00afbce770cb743170c195499d5bbc55c'

AK_PUBLISHED_CI='32459617440'
AK_PUBLISHED_CI_JOB='96703744791'
AI_HEAD='9d424dae2ed8cc7a0a6868111805a48763131196'
AI_RUN='32418184036'
AI_JOB='96584056481'
AI_CI='32420217393'
AI_CI_JOB='96590396395'
AI_ART='9424764320'
AI_ART_NAME='r318ai-following-property-header-evidence'
AI_ART_SIZE='12054'
AI_ART_DIGEST='sha256:ce5cd54908cd4c75228f94e9ea3520bef1c03766bdbbba028a708e51485494a5'

ROOT="$PWD"
WORK="$ROOT/.tmp/r318al"
AI_DIR="$WORK/ai"
rm -rf "$WORK"
mkdir -p "$AI_DIR"
trap 'rm -rf "$WORK"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318al_probe.rs"' EXIT

norm_digest(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

download_ai(){
  for attempt in 1 2 3; do
    rm -rf "$AI_DIR"; mkdir -p "$AI_DIR"
    if gh run download "$AI_RUN" -n "$AI_ART_NAME" -D "$AI_DIR"; then
      echo "R3_18AL_AI_DOWNLOAD_ATTEMPT=$attempt"
      return 0
    fi
    sleep $((attempt*10))
  done
  return 1
}

echo '== R3.18AL authority freeze =='
git fetch --no-tags origin main --force
test "$(git rev-parse origin/main)" = "$BASE"
test "$(git rev-parse origin/main^{tree})" = "$BASE_TREE"
test "$(git merge-base HEAD "$BASE")" = "$BASE"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$BASE:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$BASE:crates/mimir-replay/tests/r3_18ak_post_ag_following_header.rs")" = "$AK_TEST_BLOB"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AL_EXECUTION_SPEC.md")" = "$AL_SPEC_BLOB"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json")" = "$AJ_CONTRACT_BLOB"
test "$(sha256sum docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json | awk '{print $1}')" = "$AJ_CONTRACT_SHA256"

mapfile -t changed < <(git diff --name-only "$BASE" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318al_evidence.yml'
  '.github/workflows/_tmp_r318al_trigger.txt'
  'tools/_tmp_r318al_analyze.py'
  'tools/_tmp_r318al_native_probe.rs'
  'tools/_tmp_r318al_run.sh'
)
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 5
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$BASE" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$BASE" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

for pair in "$AK_PUBLISHED_CI:$AK_PUBLISHED_CI_JOB" "$AI_RUN:$AI_JOB" "$AI_CI:$AI_CI_JOB"; do
  run="${pair%%:*}"; job="${pair##*:}"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AI_RUN" --jq .head_sha)" = "$AI_HEAD"
echo 'R3_18AL_AUTHORITY_FREEZE=PASS'

echo '== immutable R3.18AI lane =='
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AI_ART" --jq .workflow_run.id)" = "$AI_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AI_ART" --jq .workflow_run.head_sha)" = "$AI_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AI_ART" --jq .name)" = "$AI_ART_NAME"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AI_ART" --jq .size_in_bytes)" = "$AI_ART_SIZE"
test "$(norm_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AI_ART" --jq .digest)")" = "$(norm_digest "$AI_ART_DIGEST")"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$AI_ART" --jq .expired)" = false
download_ai
(
  cd "$AI_DIR"
  test "$(wc -l < r3_18ai_artifact_sha256.txt)" -eq 9
  sha256sum -c r3_18ai_artifact_sha256.txt
  grep -Fqx 'R3_18AI_OUTCOME=A' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_FROZEN_ROWS=47/47' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_NATIVE_ORACLE_MISMATCH=0' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_WITNESS_RESELECTION=0' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' r3_18ai_aggregate.txt
  grep -Fqx 'R3_18AI_SECOND_LATER_CONTROL_BITS_CONSUMED=0' r3_18ai_aggregate.txt
)
cp "$AI_DIR/r3_18ai_replay_identity.tsv" r3_18al_replay_identity.tsv
cp "$AI_DIR/r3_18ai_frozen_witnesses.json" r3_18al_frozen_ai_witnesses.json
cp "$AI_DIR/r3_18ai_header_rows.json" r3_18al_frozen_ai_header_rows.json

python3 - "$AI_DIR/r3_18ai_frozen_witnesses.json" "$AI_DIR/r3_18ai_header_rows.json" "$WORK/targets.tsv" <<'PY'
import json, sys
from pathlib import Path

witness_path, header_path, out_path = map(Path, sys.argv[1:])
wdoc = json.loads(witness_path.read_text(encoding='utf-8'))
hdoc = json.loads(header_path.read_text(encoding='utf-8'))
wrows = {r['label']: r for r in wdoc['rows']}
hrows = {r['label']: r for r in hdoc['rows']}
assert len(wrows) == 47 and len(hrows) == 47 and set(wrows) == set(hrows)
out = []
for label in sorted(hrows):
    w = wrows[label]
    h = hrows[label]
    assert h['native_oracle_exact'] is True
    assert int(h['following_payload_bits_consumed']) == 0
    assert int(h['second_later_control_bits_consumed']) == 0
    assert int(w['published_start']) == int(h['ag_property_present_start_bit'])
    assert int(w['published_end']) == int(h['ag_stop_bit'])
    assert int(w['published_stop']) == int(h['ag_stop_bit'])
    assert w['published_value'] is True
    fields = [
        label,
        h['frame_index'],
        h['actor_ordinal'],
        h['actor_context_object_id'],
        w['first_start'],
        w['prior_stop'],
        h['ag_property_present_start_bit'],
        h['ag_stop_bit'],
        h['ag_stop_bit'],
        h['ag_property_present_start_bit'],
        h['ag_stop_bit'],
        h['stream_id_start_bit'],
        h['stream_id_end_bit'],
        h['stream_id'],
        h['stream_id_bound'],
        h['prop_id_bits'],
        h['resolved_property_object_index'],
        h['resolved_attribute_tag'],
        h['payload_start_bit'],
        h['header_stop_bit'],
    ]
    out.append('\t'.join(map(str, fields)))
Path(out_path).write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')
print('R3_18AL_TARGET_DERIVATION=PASS rows=47 witness_reselection=0')
PY

python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18al_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    rel, expected, status = line.split('\t')
    assert status == 'PASS'
    p = Path(rel)
    assert not p.is_absolute() and '..' not in p.parts
    assert hashlib.sha256(p.read_bytes()).hexdigest().lower() == expected.lower(), rel
    rows.append(rel.replace('\\','/'))
assert len(rows) == 47 and len(set(rows)) == 47
print('R3_18AL_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== published R3.18AK vs frozen R3.18AI =='
mkdir -p crates/mimir-replay/examples
cp tools/_tmp_r318al_native_probe.rs crates/mimir-replay/examples/_tmp_r318al_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318al_probe -- "$WORK/targets.tsv" > "$WORK/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318al_probe -- "$WORK/targets.tsv" > "$WORK/native2.log"
cmp "$WORK/native1.log" "$WORK/native2.log"
test "$(grep -c $'^R3_18AL_NATIVE\t' "$WORK/native1.log")" -eq 47
grep -F $'R3_18AL_NATIVE_AGG\t' "$WORK/native1.log"
rm -f crates/mimir-replay/examples/_tmp_r318al_probe.rs

python3 tools/_tmp_r318al_analyze.py \
  "$AI_DIR/r3_18ai_header_rows.json" \
  "$WORK/native1.log" \
  docs/continuity/MIMIR_R3_18AJ_ADMITTED_HEADER_CONTEXTS.json \
  r3_18al_comparison.json \
  r3_18al_header_summary.json \
  r3_18al_negative_controls.txt \
  r3_18al_aggregate.txt \
  R3.18AI

echo '== focused and repository validation =='
cargo +1.85.0 test -p mimir-replay --test r3_18ak_post_ag_following_header -- --nocapture
pwsh -NoLogo -NoProfile -File scripts/verify_repo.ps1

cat > r3_18al_upstream_receipts.txt <<EOF
R3_18AL_BASE_MAIN=$BASE
R3_18AL_BASE_TREE=$BASE_TREE
R3_18AL_PRODUCTION=$PROD
R3_18AL_PRODUCTION_TREE=$PROD_TREE
R3_18AL_AK_PUBLISHED_CI=$AK_PUBLISHED_CI/$AK_PUBLISHED_CI_JOB
R3_18AL_AI_HEAD=$AI_HEAD
R3_18AL_AI_AUTH=$AI_RUN/$AI_JOB
R3_18AL_AI_CI=$AI_CI/$AI_CI_JOB
R3_18AL_AI_ARTIFACT=$AI_ART/$AI_ART_SIZE/$AI_ART_DIGEST
R3_18AL_AJ_CONTRACT_SHA256=$AJ_CONTRACT_SHA256
EOF

cat > r3_18al_source_scope.txt <<EOF
R3_18AL_BASE_MAIN=$BASE
R3_18AL_BASE_TREE=$BASE_TREE
R3_18AL_PRODUCTION=$PROD
R3_18AL_PRODUCTION_TREE=$PROD_TREE
R3_18AL_PRODUCTION_LIB_BLOB=$LIB_BLOB
R3_18AL_AK_TEST_BLOB=$AK_TEST_BLOB
R3_18AL_EXECUTION_SPEC_BLOB=$AL_SPEC_BLOB
R3_18AL_AJ_CONTRACT_BLOB=$AJ_CONTRACT_BLOB
R3_18AL_PRODUCTION_SOURCE_MUTATION=0
R3_18AL_CARGO_MUTATION=0
R3_18AL_FIXTURE_MUTATION=0
R3_18AL_CORPUS_MUTATION=0
R3_18AL_SUPPORT_MUTATION=0
EOF

for file in \
  r3_18al_source_scope.txt \
  r3_18al_replay_identity.tsv \
  r3_18al_frozen_ai_witnesses.json \
  r3_18al_frozen_ai_header_rows.json \
  r3_18al_comparison.json \
  r3_18al_header_summary.json \
  r3_18al_negative_controls.txt \
  r3_18al_aggregate.txt \
  r3_18al_upstream_receipts.txt
do
  if grep -E -i '(/home/runner|/Users/|[A-Z]:\\\\|github_pat_|ghp_|Bearer[[:space:]])' "$file"; then
    echo "privacy scan failed: $file" >&2
    exit 1
  fi
done
grep -Fqx 'R3_18AL_PRIVACY_SCAN=PASS' r3_18al_aggregate.txt

sha256sum \
  r3_18al_source_scope.txt \
  r3_18al_replay_identity.tsv \
  r3_18al_frozen_ai_witnesses.json \
  r3_18al_frozen_ai_header_rows.json \
  r3_18al_comparison.json \
  r3_18al_header_summary.json \
  r3_18al_negative_controls.txt \
  r3_18al_aggregate.txt \
  r3_18al_upstream_receipts.txt \
  > r3_18al_artifact_sha256.txt

test "$(wc -l < r3_18al_artifact_sha256.txt)" -eq 9
sha256sum -c r3_18al_artifact_sha256.txt
grep -Fqx 'R3_18AL_OUTCOME=A' r3_18al_aggregate.txt
grep -Fqx 'R3_18AL_PUBLISHED_AK_EXACT=47/47' r3_18al_aggregate.txt
grep -Fqx 'R3_18AL_DIRECT_HEADER_EXACT=47/47' r3_18al_aggregate.txt
grep -Fqx 'R3_18AL_NATIVE_ORACLE_MISMATCH=0' r3_18al_aggregate.txt
grep -Fqx 'R3_18AL_WITNESS_RESELECTION=0' r3_18al_aggregate.txt
grep -Fqx 'R3_18AL_AJ_CONTRACT_EXACT=PASS' r3_18al_aggregate.txt
grep -Fqx 'R3_18AL_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' r3_18al_aggregate.txt
grep -Fqx 'R3_18AL_SECOND_LATER_CONTROL_BITS_CONSUMED=0' r3_18al_aggregate.txt
echo 'R3_18AL_EVIDENCE_COMPLETE=PASS'

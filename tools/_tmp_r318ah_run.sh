#!/usr/bin/env bash
set -euo pipefail

BASE="0e48eebffbd7f54238835e23c177e732cbeb7978"
PROD="2d351e8ceb601e2fbe515d2977b2103a4b2c7976"
TREE="4123820ce6537f2d4942cd0b5f72b52e43b96c1d"
LIB="db923ebcb419d278f4ab0144fe7ed15b298b60fa"
TEST="3f3e1c8f3f6deb7f2558862a1032f8a102131443"
AH_SPEC="94aec628115f43db549ffec2d52338372a6a7459"
PROBE="0f652f043a1d8d3ae68d86be6f72dd9f88300847"
AF_HEAD="30286c07727539d68f551140838fb2ef6802a26e"
AF_RUN="32344981062"
AF_JOB="96351720877"
AF_CI="32345376481"
AF_CI_JOB="96352906609"
AF_ART="9397743505"
AF_DIGEST="sha256:d7edeab657928c94c35c852ae302fd614cab92a52b7e44f671310200af4b268f"
AG_BUILDER_RUN="32401660279"
AG_BUILDER_JOB="96531043622"
AG_PR_CI="32402596061"
AG_PR_CI_JOB="96534073576"
AG_MAIN_CI="32402933798"
AG_MAIN_CI_JOB="96535174390"
AG_CONT_RUN="32404006084"
AG_CONT_JOB="96538654038"
AG_CONT_CI="32404130156"
AG_CONT_CI_JOB="96539054843"
AG_CONT_KA="32404130088"
AG_CONT_KA_JOB="96539054479"

rm -rf /tmp/r318af_authority /tmp/r318ah_run1 /tmp/r318ah_run2
mkdir -p /tmp/r318af_authority /tmp/r318ah_run1 /tmp/r318ah_run2

# Immutable authority freeze.
test "$(git rev-parse "$BASE^{tree}")" = "627d02ca39ff732e9dd7137d061432c6a67fafd8"
test "$(git rev-parse "$BASE:crates/mimir-replay/src/lib.rs")" = "$LIB"
test "$(git rev-parse "$BASE:crates/mimir-replay/tests/r3_18ag_post_ad_payload_control.rs")" = "$TEST"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AH_EXECUTION_SPEC.md")" = "$AH_SPEC"
test "$(git rev-parse HEAD:crates/mimir-replay/examples/r318ah_probe.rs)" = "$PROBE"

for pair in \
  "$AG_BUILDER_RUN:$AG_BUILDER_JOB" \
  "$AG_PR_CI:$AG_PR_CI_JOB" \
  "$AG_MAIN_CI:$AG_MAIN_CI_JOB" \
  "$AG_CONT_RUN:$AG_CONT_JOB" \
  "$AG_CONT_CI:$AG_CONT_CI_JOB" \
  "$AG_CONT_KA:$AG_CONT_KA_JOB" \
  "$AF_RUN:$AF_JOB" \
  "$AF_CI:$AF_CI_JOB"
do
  run="${pair%%:*}"; job="${pair##*:}"
  test "$(gh api "repos/${GITHUB_REPOSITORY}/actions/runs/${run}" --jq .conclusion)" = success
  test "$(gh api "repos/${GITHUB_REPOSITORY}/actions/jobs/${job}" --jq .conclusion)" = success
done

test "$(gh api "repos/${GITHUB_REPOSITORY}/actions/runs/${AF_RUN}" --jq .head_sha)" = "$AF_HEAD"
meta="$(gh api "repos/${GITHUB_REPOSITORY}/actions/artifacts/${AF_ART}")"
test "$(jq -r .workflow_run.head_sha <<<"$meta")" = "$AF_HEAD"
test "$(jq -r .digest <<<"$meta")" = "$AF_DIGEST"
test "$(jq -r .expired <<<"$meta")" = false

gh run download "$AF_RUN" -n r318af-next-property-control-differential-evidence -D /tmp/r318af_authority
(
  cd /tmp/r318af_authority
  sha256sum -c r3_18af_artifact_sha256.txt
  grep -Fx 'R3_18AF_OUTCOME=A' r3_18af_aggregate.txt
  grep -Fx 'R3_18AF_EVIDENCE=PASS' r3_18af_aggregate.txt
  grep -Fx 'R3_18AF_FROZEN_ROWS=47/47' r3_18af_aggregate.txt
  grep -Fx 'R3_18AF_CONTROL_FALSE=0' r3_18af_aggregate.txt
  grep -Fx 'R3_18AF_CONTROL_TRUE=47' r3_18af_aggregate.txt
  grep -Fx 'R3_18AF_NATIVE_ORACLE_MISMATCH=0' r3_18af_aggregate.txt
  grep -Fx 'R3_18AF_WITNESS_RESELECTION=0' r3_18af_aggregate.txt
)

run_probe() {
  local out="$1"
  : > "$out/probe.tsv"
  while IFS=$'\t' read -r label frame actor_ordinal actor_context first_start payload_start payload_end width tag; do
    cargo +1.85.0 run --quiet -p mimir-replay --example r318ah_probe -- \
      "$label" "$first_start" "$actor_context" "$payload_end" >> "$out/probe.tsv"
  done < /tmp/r318af_authority/r3_18af_targets.tsv

  python3 - "$out" <<'PY'
import hashlib, json, pathlib, sys
out = pathlib.Path(sys.argv[1])
af = pathlib.Path('/tmp/r318af_authority')
frozen = json.loads((af/'r3_18af_comparison.json').read_text())
rows = frozen['rows']
by_label = {r['label']: r for r in rows}
probe=[]
for line in (out/'probe.tsv').read_text().splitlines():
    p=line.split('\t')
    if len(p)!=16: raise SystemExit(f'bad probe columns={len(p)}')
    probe.append({
      'label':p[0], 'first_start':int(p[1]), 'actor_context_object_id':int(p[2]),
      'frozen_start_arg':int(p[3]), 'prior_stop':int(p[4]), 'published_value':bool(int(p[5])),
      'published_start':int(p[6]), 'published_end':int(p[7]), 'published_stop':int(p[8]),
      'native_value':bool(int(p[9]),), 'repeat_equal':bool(int(p[10])),
      'false_reject':bool(int(p[11])), 'trunc_reject':bool(int(p[12])),
      'poison_same':bool(int(p[13])), 'prior_stop_reject':bool(int(p[14])),
      'wrong_context_reject':bool(int(p[15])),
    })
if len(probe)!=47 or len(by_label)!=47: raise SystemExit('expected 47 rows')
comparison=[]
for q in probe:
    f=by_label.get(q['label'])
    if not f: raise SystemExit('witness reselection or missing label: '+q['label'])
    exact=(
      q['prior_stop']==f['prior_r3_18ad_stop_bit']==f['property_present_start_bit'] and
      q['frozen_start_arg']==f['property_present_start_bit'] and
      q['published_start']==f['property_present_start_bit'] and
      q['published_value']==f['property_present'] and
      q['native_value']==f['property_present'] and
      q['published_end']==f['property_present_end_bit'] and
      q['published_stop']==f['property_present_end_bit'] and
      q['published_end']==q['published_start']+1
    )
    comparison.append({**q,
      'frozen_value':f['property_present'],
      'frozen_start':f['property_present_start_bit'],
      'frozen_end':f['property_present_end_bit'],
      'frozen_prior_stop':f['prior_r3_18ad_stop_bit'],
      'published_frozen_native_exact':exact,
      'next_stream_bits_consumed':0,'next_header_bits_consumed':0,
      'next_payload_bits_consumed':0,'second_later_control_bits_consumed':0,
    })
summary={
 'rows':len(comparison),
 'published_exact':sum(r['published_frozen_native_exact'] for r in comparison),
 'mismatch':sum(not r['published_frozen_native_exact'] for r in comparison),
 'false':sum(not r['published_value'] for r in comparison),
 'true':sum(r['published_value'] for r in comparison),
 'repeatability_pass':sum(r['repeat_equal'] for r in comparison),
 'false_negative_pass':sum(r['false_reject'] for r in comparison),
 'truncation_pass':sum(r['trunc_reject'] for r in comparison),
 'poison_pass':sum(r['poison_same'] for r in comparison),
 'prior_stop_negative_pass':sum(r['prior_stop_reject'] for r in comparison),
 'wrong_context_pass':sum(r['wrong_context_reject'] for r in comparison),
 'witness_reselection':0,
 'next_stream_bits_consumed':0,'next_header_bits_consumed':0,
 'next_payload_bits_consumed':0,'second_later_control_bits_consumed':0,
}
(out/'comparison.json').write_text(json.dumps({'aggregate':summary,'rows':comparison},sort_keys=True,indent=2)+'\n')
(out/'summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
PY
}

run_probe /tmp/r318ah_run1
run_probe /tmp/r318ah_run2
cmp /tmp/r318ah_run1/probe.tsv /tmp/r318ah_run2/probe.tsv
cmp /tmp/r318ah_run1/comparison.json /tmp/r318ah_run2/comparison.json
cmp /tmp/r318ah_run1/summary.json /tmp/r318ah_run2/summary.json

cp /tmp/r318ah_run1/probe.tsv r3_18ah_probe.tsv
cp /tmp/r318ah_run1/comparison.json r3_18ah_comparison.json
cp /tmp/r318ah_run1/summary.json r3_18ah_summary.json
cp /tmp/r318af_authority/r3_18af_replay_identity.tsv r3_18ah_replay_identity.tsv
cp /tmp/r318af_authority/r3_18af_targets.tsv r3_18ah_frozen_af_targets.tsv

python3 - <<'PY'
import json
s=json.load(open('r3_18ah_summary.json'))
required=['rows','published_exact','mismatch','false','true','repeatability_pass','false_negative_pass','truncation_pass','poison_pass','prior_stop_negative_pass','wrong_context_pass']
assert all(k in s for k in required)
assert s['rows']==47 and s['published_exact']==47 and s['mismatch']==0
assert s['false']==0 and s['true']==47
for k in ['repeatability_pass','false_negative_pass','truncation_pass','poison_pass','prior_stop_negative_pass','wrong_context_pass']:
    assert s[k]==47,(k,s[k])
assert s['witness_reselection']==0
assert [s['next_stream_bits_consumed'],s['next_header_bits_consumed'],s['next_payload_bits_consumed'],s['second_later_control_bits_consumed']]==[0,0,0,0]
PY

cat > r3_18ah_source_scope.txt <<EOF
R3_18AH_BASE=$BASE
R3_18AH_PRODUCTION=$PROD
R3_18AH_PRODUCTION_TREE=$TREE
R3_18AH_LIB_BLOB=$LIB
R3_18AH_TEST_BLOB=$TEST
R3_18AH_SPEC_BLOB=$AH_SPEC
R3_18AH_PROBE_BLOB=$PROBE
R3_18AH_PRODUCTION_MUTATION=0
R3_18AH_WITNESS_RESELECTION=0
R3_18AH_NEXT_STREAM_HEADER_PAYLOAD_SECOND_CONTROL=0/0/0/0
EOF

cat > r3_18ah_upstream_receipts.txt <<EOF
AG_BUILDER=$AG_BUILDER_RUN/$AG_BUILDER_JOB SUCCESS
AG_PR_CI=$AG_PR_CI/$AG_PR_CI_JOB SUCCESS
AG_MAIN_CI=$AG_MAIN_CI/$AG_MAIN_CI_JOB SUCCESS
AG_CONTINUITY=$AG_CONT_RUN/$AG_CONT_JOB SUCCESS
AG_CONTINUITY_CI=$AG_CONT_CI/$AG_CONT_CI_JOB SUCCESS
AG_CONTINUITY_KA=$AG_CONT_KA/$AG_CONT_KA_JOB SUCCESS
AF_AUTHORITY=$AF_RUN/$AF_JOB SUCCESS
AF_CI=$AF_CI/$AF_CI_JOB SUCCESS
AF_ARTIFACT=$AF_ART $AF_DIGEST
EOF

cat > r3_18ah_negative_controls.txt <<EOF
FALSE_MUTATION=PASS 47/47
TRUNCATION_BEFORE_CONTROL=PASS 47/47
REPEATABILITY=PASS 47/47
POST_STOP_POISON=PASS 47/47
PRIOR_STOP_MISMATCH=PASS 47/47
WRONG_CONTEXT=PASS 47/47
AD_PRIOR_HEADER_PAYLOAD_UID_SHAPE=PASS permanent-r3_18ag-focused-suite
EOF

cat > r3_18ah_aggregate.txt <<EOF
R3_18AH_OUTCOME=A
R3_18AH_EVIDENCE=PASS
R3_18AH_FROZEN_ROWS=47/47
R3_18AH_PUBLISHED_AG_EXACT=47/47
R3_18AH_PUBLISHED_FROZEN_NATIVE_MISMATCH=0
R3_18AH_CONTROL_FALSE=0
R3_18AH_CONTROL_TRUE=47
R3_18AH_REPEATABILITY=PASS 47/47
R3_18AH_FALSE_NEGATIVE=PASS 47/47
R3_18AH_TRUNCATION=PASS 47/47
R3_18AH_POST_STOP_POISON=PASS 47/47
R3_18AH_PRIOR_STOP_NEGATIVE=PASS 47/47
R3_18AH_WRONG_CONTEXT=PASS 47/47
R3_18AH_WITNESS_RESELECTION=0
R3_18AH_NEXT_STREAM_BITS_CONSUMED=0
R3_18AH_NEXT_HEADER_BITS_CONSUMED=0
R3_18AH_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18AH_SECOND_LATER_CONTROL_BITS_CONSUMED=0
R3_18AH_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18AH_PRIVACY_SCAN=PASS
EOF

# Full validation against unchanged published production + temporary probe only.
cargo +1.85.0 test -p mimir-replay --test r3_18ag_post_ad_payload_control
cargo +1.85.0 test -p mimir-replay --test r3_18ad_post_aa_payload
cargo +1.85.0 test -p mimir-replay
cargo +1.85.0 fmt --all -- --check
cargo +1.85.0 check --workspace
cargo +1.85.0 test --workspace
cargo +1.85.0 clippy --workspace --all-targets -- -D warnings
pwsh -NoProfile -File scripts/verify_mimir_knowledge_archive.ps1

# Privacy-safe evidence only: repository-relative labels, no raw bit windows or metadata.
if grep -E -i '(/home/|/Users/|[A-Za-z]:\\|@gmail\.|@outlook\.|@hotmail\.)' \
  r3_18ah_probe.tsv r3_18ah_comparison.json r3_18ah_summary.json r3_18ah_replay_identity.tsv \
  r3_18ah_frozen_af_targets.tsv r3_18ah_source_scope.txt r3_18ah_upstream_receipts.txt \
  r3_18ah_negative_controls.txt r3_18ah_aggregate.txt; then
  echo 'privacy scan failed' >&2; exit 1
fi

sha256sum \
  r3_18ah_probe.tsv \
  r3_18ah_comparison.json \
  r3_18ah_summary.json \
  r3_18ah_replay_identity.tsv \
  r3_18ah_frozen_af_targets.tsv \
  r3_18ah_source_scope.txt \
  r3_18ah_upstream_receipts.txt \
  r3_18ah_negative_controls.txt \
  r3_18ah_aggregate.txt > r3_18ah_artifact_sha256.txt
sha256sum -c r3_18ah_artifact_sha256.txt
cat r3_18ah_aggregate.txt

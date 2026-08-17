#!/usr/bin/env bash
set -euo pipefail

MAIN='196771bfc4193a9abf40f50577fbcebd37d0f131'
MAIN_TREE='cbd655c600252c82ceb9d9d0db8a0c4942e7d45b'
PROD='f41c59d26ed6c810a640b4fa8cd76129decb32aa'
PROD_TREE='606db4b5778e5218f2bd0117cc5dd72d7f3e37a5'
LIB_BLOB='b01b1e8629a4f4bc2452e67024ffb0d064bf58fb'
Q_TEST_BLOB='4bb65af1d533752edc062202192232d6f1d4239c'
Q_DECISION_BLOB='ae2afbd945e445cddfd003665e23f7508e4d4b08'
R_SPEC_BLOB='0f70ce8ab6a646486a98e724fde36bab346cc90a'
STATE_BLOB='0f0eaf3bb75fc099a7b046e3d5c7888f449a4751'
P_CONTRACT_SHA='0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b'

Q_AUTH_RUN='32026722346'
Q_AUTH_JOB='95377559363'
Q_AUTH_ART='9287413927'
Q_AUTH_ART_DIGEST='sha256:1d4ae41e506a69e49ff58372ac0774c6257cbace96a3219bf6ab3ba5f68bf9bb'
Q_CANDIDATE_CI='32027055064'
Q_PUBLISHED_CI='32027421491'
CONT_AUTH_RUN='32028031055'
CONT_PR_CI='32028321873'
CONT_PR_KA='32028321870'
CONT_PUBLISHED_CI='32028671371'
CONT_PUBLISHED_KA='32028671332'

O_HEAD='5046e1594b87ce2828db5faa48aceba456c3166f'
O_TREE='74fb036dfde837e3ecb7e459da00df9ff6c22e28'
O_RUN='32017369100'
O_JOB='95349613184'
O_ART='9284144768'
O_ART_SIZE='25129'
O_ART_DIGEST='sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d'
O_SUMMARY_SHA='f1bc285db764a71091c904e74a82c28e369cec1e62bed1b7ae503effef4824bc'
O_HEADER_SHA='599657a154498451d6317bf148da7bcf6e7077f35315426023da526a955ee2a4'
O_AGG_SHA='170bad20b7d3d11596f879865a1380ade3910eba069311bec7e6d51eae2a4233'
O_PROBE_SOURCE='f3e2ad006413e1357102697d7eb0e5cc24e3cefd'
EVIDENCE_BRANCH='evidence/r318r-published-following-header-v1'

ROOT="$PWD"
TMP="$(mktemp -d)"
O_DIR="$TMP/o"
mkdir -p "$O_DIR"
trap 'rm -rf "$TMP"' EXIT

echo '== R3.18R authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git merge-base HEAD "$MAIN")" = "$MAIN"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$MAIN:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$MAIN:crates/mimir-replay/tests/r3_18q_following_header.rs")" = "$Q_TEST_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/tests/r3_18q_following_header.rs")" = "$Q_TEST_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18Q_DECISION.md")" = "$Q_DECISION_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18R_EXECUTION_SPEC.md")" = "$R_SPEC_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_CONTINUITY_STATE.json")" = "$STATE_BLOB"
git show "$MAIN:docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json" > "$TMP/r3_18p_contract.json"
test "$(sha256sum "$TMP/r3_18p_contract.json" | awk '{print $1}')" = "$P_CONTRACT_SHA"

mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0
mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318r_evidence.yml'
  'tools/_tmp_r318r_run.sh'
)
mapfile -t expected_sorted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 2
if [ "$(printf '%s\n' "${changed[@]}")" != "$(printf '%s\n' "${expected_sorted[@]}")" ]; then
  printf 'unexpected R3.18R evidence scope\nactual:\n%s\nexpected:\n%s\n' "$(printf '%s\n' "${changed[@]}")" "$(printf '%s\n' "${expected_sorted[@]}")"
  exit 1
fi
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

for id in "$Q_AUTH_RUN" "$Q_CANDIDATE_CI" "$Q_PUBLISHED_CI" "$CONT_AUTH_RUN" "$CONT_PR_CI" "$CONT_PR_KA" "$CONT_PUBLISHED_CI" "$CONT_PUBLISHED_KA" "$O_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$id" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$Q_AUTH_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$O_JOB" --jq .conclusion)" = success
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$CONT_PUBLISHED_CI" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$CONT_PUBLISHED_KA" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$Q_AUTH_ART" --jq .digest)" = "$Q_AUTH_ART_DIGEST"

echo 'R3_18R_AUTHORITY_FREEZE=PASS'

echo '== immutable R3.18O source lane =='
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$O_ART" --jq .workflow_run.id)" = "$O_RUN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$O_ART" --jq .workflow_run.head_sha)" = "$O_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$O_ART" --jq .size_in_bytes)" = "$O_ART_SIZE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$O_ART" --jq .digest)" = "$O_ART_DIGEST"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$O_ART" --jq .expired)" = false
gh run download "$O_RUN" -n r318o-following-property-header-evidence -D "$O_DIR"
test "$(wc -l < "$O_DIR/r3_18o_artifact_sha256.txt")" -eq 11
(cd "$O_DIR" && sha256sum -c r3_18o_artifact_sha256.txt)
test "$(sha256sum "$O_DIR/r3_18o_source_summary.json" | awk '{print $1}')" = "$O_SUMMARY_SHA"
test "$(sha256sum "$O_DIR/r3_18o_header_rows.json" | awk '{print $1}')" = "$O_HEADER_SHA"
test "$(sha256sum "$O_DIR/r3_18o_aggregate.txt" | awk '{print $1}')" = "$O_AGG_SHA"
python3 - "$O_DIR/r3_18o_source_summary.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
assert d['rows']==47
assert d['distinct_exact_header_context_tuples']==18
assert d['witness_reselection']==0
assert d['observer_following_payload_bits_consumed']==0
assert d['observer_another_control_bits_consumed']==0
print('R3_18R_O_SOURCE_SUMMARY=PASS rows=47 contexts=18 reselection=0')
PY
cp "$O_DIR/r3_18o_replay_identity.tsv" r3_18r_replay_identity.tsv
cp "$O_DIR/r3_18o_frozen_witnesses.json" r3_18r_frozen_witnesses.json
python3 - <<'PY'
import hashlib
from pathlib import Path
seen=[]
for line in Path('r3_18r_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    rel,expected,status=line.split('\t')
    assert status=='PASS', rel
    assert not rel.startswith('/') and '..' not in Path(rel).parts, rel
    got=hashlib.sha256(Path(rel).read_bytes()).hexdigest()
    assert got.lower()==expected.lower(), rel
    seen.append(rel.replace('\\','/'))
assert len(seen)==47 and len(set(seen))==47
print('R3_18R_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== derive published-Q probe from frozen R3.18O probe =='
git show "$O_PROBE_SOURCE:tools/_tmp_r318o_native_probe.rs" > "$TMP/probe.rs"
python3 - "$TMP/probe.rs" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected one match, got {n}')
    s=s.replace(old,new,1)

once(
    'ReplayNetworkK2DecodeContextV1, ReplayNetworkLookupPlanReader,',
    'ReplayNetworkK2DecodeContextV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader,',
    'K3 import',
)
once(
    '    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,\n',
    '    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,\n    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1,\n',
    'Q function import',
)
for old,new,label in [
    ('        let _version_major: u32 = f[36].parse()?;','        let version_major: i32 = f[36].parse()?;','major'),
    ('        let _version_minor: u32 = f[37].parse()?;','        let version_minor: i32 = f[37].parse()?;','minor'),
    ('        let _net_version: u32 = f[38].parse()?;','        let net_version: i32 = f[38].parse()?;','net'),
]:
    once(old,new,label)
needle='''        header_count += 1;\n\n        let repeated = decode_replay_network_existing_actor_first_property_header_v1('''
insert='''        header_count += 1;\n\n        let q = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(\n            &network,\n            &decoded,\n            &plan,\n            ReplayNetworkK3DecodeContextV1 {\n                version_major,\n                version_minor,\n                net_version,\n                is_rl_223: false,\n            },\n        )?;\n        if q.control != control || q.following_header != following || q.stop_bit != expected_payload_start {\n            return Err(format!("{label}: published R3.18Q mismatch").into());\n        }\n\n        let q_repeated = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(\n            &network,\n            &decoded,\n            &plan,\n            ReplayNetworkK3DecodeContextV1 {\n                version_major,\n                version_minor,\n                net_version,\n                is_rl_223: false,\n            },\n        )?;\n        let q_repeatability = q_repeated == q;\n\n        let q_trunc_bytes = usize::try_from(control.property_present_start_bit / 8)?;\n        let q_truncation = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(\n            &network[..q_trunc_bytes.min(network.len())],\n            &decoded,\n            &plan,\n            ReplayNetworkK3DecodeContextV1 {\n                version_major,\n                version_minor,\n                net_version,\n                is_rl_223: false,\n            },\n        ).is_err();\n\n        let mut q_wrong_actor_prior = decoded.clone();\n        q_wrong_actor_prior\n            .header_composition\n            .second_header\n            .as_mut()\n            .ok_or("missing second header for wrong-actor negative")?\n            .actor_object_index = u32::MAX;\n        let q_wrong_actor = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(\n            &network,\n            &q_wrong_actor_prior,\n            &plan,\n            ReplayNetworkK3DecodeContextV1 {\n                version_major,\n                version_minor,\n                net_version,\n                is_rl_223: false,\n            },\n        ).is_err();\n\n        let mut q_unresolved_plan = plan.clone();\n        let actor_slot = q_unresolved_plan\n            .object_lookups\n            .get_mut(usize::try_from(actor_object)?)\n            .ok_or("missing actor lookup slot")?;\n        *actor_slot = None;\n        let q_unresolved_lookup = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(\n            &network,\n            &decoded,\n            &q_unresolved_plan,\n            ReplayNetworkK3DecodeContextV1 {\n                version_major,\n                version_minor,\n                net_version,\n                is_rl_223: false,\n            },\n        ).is_err();\n\n        let q_wrong_version = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(\n            &network,\n            &decoded,\n            &plan,\n            ReplayNetworkK3DecodeContextV1 {\n                version_major,\n                version_minor: version_minor - 1,\n                net_version,\n                is_rl_223: false,\n            },\n        ).is_err();\n\n        let mut q_poisoned = network.clone();\n        for offset in 0..16u64 {\n            set_bit(&mut q_poisoned, expected_payload_start + offset, offset % 2 == 0)\n                .map_err(std::io::Error::other)?;\n        }\n        let q_poisoned_result = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(\n            &q_poisoned,\n            &decoded,\n            &plan,\n            ReplayNetworkK3DecodeContextV1 {\n                version_major,\n                version_minor,\n                net_version,\n                is_rl_223: false,\n            },\n        )?;\n        let q_poison_invariant = q_poisoned_result == q;\n\n        println!(\n            "R3_18R_Q\\tlabel={label}\\tstream_bound={expected_stream_bound}\\tprop_bits={expected_prop_bits}\\tproperty_object={expected_property_object}\\ttag={expected_tag}\\tversion_major={version_major}\\tversion_minor={version_minor}\\tnet_version={net_version}\\tpresent_start={expected_present_start}\\tpresent_end={expected_present_end}\\tpayload_start={expected_payload_start}\\tq_equal=1\\tq_repeatability={}\\tq_truncation={}\\tq_wrong_actor={}\\tq_unresolved_lookup={}\\tq_wrong_version={}\\tq_poison_invariant={}\\tfollowing_payload_bits_consumed=0\\tanother_control_bits_consumed=0",\n            u8::from(q_repeatability),\n            u8::from(q_truncation),\n            u8::from(q_wrong_actor),\n            u8::from(q_unresolved_lookup),\n            u8::from(q_wrong_version),\n            u8::from(q_poison_invariant),\n        );\n\n        let repeated = decode_replay_network_existing_actor_first_property_header_v1('''
once(needle,insert,'published Q insertion')
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18R_PROBE_DERIVATION=PASS')
PY

mkdir -p crates/mimir-replay/examples
cp "$TMP/probe.rs" crates/mimir-replay/examples/_tmp_r318r_probe.rs
cargo +1.85.0 fmt --all
cargo +1.85.0 build --locked -p mimir-replay --example _tmp_r318r_probe
./target/debug/examples/_tmp_r318r_probe "$O_DIR/r3_18o_targets.tsv" | tee "$TMP/native1.log"
./target/debug/examples/_tmp_r318r_probe "$O_DIR/r3_18o_targets.tsv" > "$TMP/native2.log"
cmp "$TMP/native1.log" "$TMP/native2.log"
test "$(grep -c $'^R3_18R_Q\t' "$TMP/native1.log")" -eq 47
test "$(grep -c $'^R3_18O_NATIVE\t' "$TMP/native1.log")" -eq 47
grep $'^R3_18R_Q\t' "$TMP/native1.log" > r3_18r_published_q_rows.tsv
rm -f crates/mimir-replay/examples/_tmp_r318r_probe.rs
rmdir crates/mimir-replay/examples 2>/dev/null || true
cargo +1.85.0 fmt --all -- --check

echo '== independent contract/multiplicity and negative analysis =='
python3 - "$TMP/r3_18p_contract.json" <<'PY'
from collections import Counter
from pathlib import Path
import json,sys
contract=json.load(open(sys.argv[1],encoding='utf-8'))
keys=('stream_id_bound','prop_id_bits','property_object_index','attribute_tag','version_major','version_minor','net_version')
expected=Counter()
for row in contract['admitted_contexts']:
    t=tuple(row[k] for k in keys)
    expected[t]=row['observed_count']
assert len(expected)==18 and sum(expected.values())==47

rows=[]
for line in Path('r3_18r_published_q_rows.tsv').read_text(encoding='utf-8').splitlines():
    parts=line.split('\t')
    assert parts[0]=='R3_18R_Q'
    d={}
    for item in parts[1:]:
        k,v=item.split('=',1)
        d[k]=v
    for flag in ('q_equal','q_repeatability','q_truncation','q_wrong_actor','q_unresolved_lookup','q_wrong_version','q_poison_invariant'):
        assert d[flag]=='1',(d['label'],flag,d[flag])
    assert d['following_payload_bits_consumed']=='0'
    assert d['another_control_bits_consumed']=='0'
    assert not d['label'].startswith('/') and '..' not in Path(d['label']).parts
    t=(int(d['stream_bound']),int(d['prop_bits']),int(d['property_object']),d['tag'],int(d['version_major']),int(d['version_minor']),int(d['net_version']))
    rows.append((d,t))
observed=Counter(t for _,t in rows)
assert len(rows)==47
assert observed==expected,(observed,expected)
assert sum(1 for d,_ in rows if d['tag']=='Boolean')==39
assert sum(1 for d,_ in rows if d['tag']=='ActiveActor')==8
assert all((int(d['version_major']),int(d['version_minor']),int(d['net_version']))==(868,32,10) for d,_ in rows)

comparison={
  'outcome':'A',
  'published_q_rows':47,
  'native_oracle_mismatch':0,
  'r3_18m_control_equality':'47/47',
  'stateless_header_equality':'47/47',
  'r3_18p_exact_contract_equality':'18/18 contexts; 47/47 multiplicities',
  'boolean_rows':39,
  'active_actor_rows':8,
  'version':'868.32/net10',
  'q_repeatability':'47/47',
  'q_truncation_negative':'47/47',
  'q_wrong_actor_negative':'47/47',
  'q_unresolved_lookup_negative':'47/47',
  'q_wrong_version_negative':'47/47',
  'q_post_payload_poison_invariance':'47/47',
  'following_payload_bits_consumed':0,
  'another_control_bits_consumed':0,
  'witness_reselection':0,
}
Path('r3_18r_comparison.json').write_text(json.dumps(comparison,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
Path('r3_18r_negative_controls.txt').write_text(
    'q_truncation_negative=47/47\n'
    'q_wrong_actor_negative=47/47\n'
    'q_unresolved_lookup_negative=47/47\n'
    'q_wrong_version_negative=47/47\n'
    'q_repeatability=47/47\n'
    'q_post_payload_poison_invariance=47/47\n'
    'fabricated_cartesian_negative=PASS(permanent_r3_18q_focused_test)\n'
    'component_tag_version_widening_negative=PASS(permanent_r3_18q_focused_test)\n',
    encoding='utf-8',newline='\n'
)
print('R3_18R_CONTRACT_AND_NEGATIVES=PASS contexts=18 rows=47')
PY

echo '== permanent tests and repository validation =='
cargo +1.85.0 test --locked -p mimir-replay r3_18q -- --nocapture
cargo +1.85.0 test --locked -p mimir-replay
pwsh -NoProfile -File scripts/verify_repo.ps1
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

echo '== privacy-safe immutable evidence =='
cat > r3_18r_source_scope.txt <<EOF
main=$MAIN
main_tree=$MAIN_TREE
production=$PROD
production_tree=$PROD_TREE
lib_blob=$LIB_BLOB
q_test_blob=$Q_TEST_BLOB
q_decision_blob=$Q_DECISION_BLOB
r_spec_blob=$R_SPEC_BLOB
state_blob=$STATE_BLOB
r3_18p_contract_sha256=$P_CONTRACT_SHA
q_authority_run=$Q_AUTH_RUN
q_authority_job=$Q_AUTH_JOB
q_authority_artifact=$Q_AUTH_ART
q_authority_artifact_digest=$Q_AUTH_ART_DIGEST
q_candidate_ci=$Q_CANDIDATE_CI
q_published_ci=$Q_PUBLISHED_CI
continuity_authority=$CONT_AUTH_RUN
continuity_pr_ci=$CONT_PR_CI
continuity_pr_knowledge_archive=$CONT_PR_KA
continuity_published_ci=$CONT_PUBLISHED_CI
continuity_published_knowledge_archive=$CONT_PUBLISHED_KA
r3_18o_head=$O_HEAD
r3_18o_tree=$O_TREE
r3_18o_run=$O_RUN
r3_18o_job=$O_JOB
r3_18o_artifact=$O_ART
r3_18o_artifact_size=$O_ART_SIZE
r3_18o_artifact_digest=$O_ART_DIGEST
r3_18o_source_summary_sha256=$O_SUMMARY_SHA
r3_18o_header_rows_sha256=$O_HEADER_SHA
r3_18o_aggregate_sha256=$O_AGG_SHA
witness_reselection=0
production_mutation=0
cargo_mutation=0
fixture_mutation=0
corpus_mutation=0
support_mutation=0
EOF
cat > r3_18r_aggregate.txt <<'EOF'
R3_18R_OUTCOME=A
R3_18R_PUBLISHED_Q_ROWS=47/47
R3_18R_EXACT_CONTEXTS=18/18
R3_18R_EXACT_MULTIPLICITIES=47/47
R3_18R_R318M_CONTROL_EQUAL=47/47
R3_18R_STATELESS_HEADER_EQUAL=47/47
R3_18R_NATIVE_ORACLE_MISMATCH=0
R3_18R_BOOLEAN_ROWS=39
R3_18R_ACTIVE_ACTOR_ROWS=8
R3_18R_VERSION=868.32/net10
R3_18R_Q_TRUNCATION_NEGATIVE=47/47
R3_18R_Q_WRONG_ACTOR_NEGATIVE=47/47
R3_18R_Q_UNRESOLVED_LOOKUP_NEGATIVE=47/47
R3_18R_Q_WRONG_VERSION_NEGATIVE=47/47
R3_18R_Q_REPEATABILITY=47/47
R3_18R_Q_POST_PAYLOAD_POISON_INVARIANCE=47/47
R3_18R_FABRICATED_CARTESIAN_NEGATIVE=PASS
R3_18R_COMPONENT_TAG_VERSION_WIDENING_NEGATIVE=PASS
R3_18R_WITNESS_RESELECTION=0
R3_18R_FOLLOWING_PAYLOAD_BITS_CONSUMED=0
R3_18R_ANOTHER_CONTROL_BITS_CONSUMED=0
R3_18R_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18R_PRIVACY_SCAN=PASS
EOF
cat > r3_18r_upstream_receipts.txt <<EOF
R3_18Q_AUTHORITY=$Q_AUTH_RUN/$Q_AUTH_JOB SUCCESS
R3_18Q_CANDIDATE_CI=$Q_CANDIDATE_CI SUCCESS
R3_18Q_PUBLISHED_CI=$Q_PUBLISHED_CI SUCCESS
R3_18Q_CONTINUITY_AUTHORITY=$CONT_AUTH_RUN SUCCESS
R3_18Q_CONTINUITY_PR_CI=$CONT_PR_CI SUCCESS
R3_18Q_CONTINUITY_PR_KA=$CONT_PR_KA SUCCESS
R3_18Q_CONTINUITY_PUBLISHED_CI=$CONT_PUBLISHED_CI SUCCESS
R3_18Q_CONTINUITY_PUBLISHED_KA=$CONT_PUBLISHED_KA SUCCESS
R3_18O_AUTHORITY=$O_RUN/$O_JOB SUCCESS
R3_18O_ARTIFACT=$O_ART/$O_ART_SIZE/$O_ART_DIGEST
R3_18P_CONTRACT_SHA256=$P_CONTRACT_SHA
EOF

artifact_files=(
  r3_18r_source_scope.txt
  r3_18r_replay_identity.tsv
  r3_18r_frozen_witnesses.json
  r3_18r_upstream_receipts.txt
  r3_18r_published_q_rows.tsv
  r3_18r_comparison.json
  r3_18r_negative_controls.txt
  r3_18r_aggregate.txt
)
for f in "${artifact_files[@]}"; do test -s "$f"; done
if grep -R -nE '(/home/runner|/tmp/|github_pat_|ghp_|Authorization:|Bearer |[A-Za-z]:\\\\)' "${artifact_files[@]}"; then
  echo 'privacy scan found forbidden host/token/path material' >&2
  exit 1
fi
if grep -R -nE '(payload_hex|raw_payload|raw_bytes|window_hex|payload_window)' "${artifact_files[@]}"; then
  echo 'privacy scan found forbidden raw payload material' >&2
  exit 1
fi
sha256sum "${artifact_files[@]}" > r3_18r_artifact_sha256.txt
test "$(wc -l < r3_18r_artifact_sha256.txt)" -eq 8
sha256sum -c r3_18r_artifact_sha256.txt

grep -Fx 'R3_18R_OUTCOME=A' r3_18r_aggregate.txt
grep -Fx 'R3_18R_NATIVE_ORACLE_MISMATCH=0' r3_18r_aggregate.txt
grep -Fx 'R3_18R_WITNESS_RESELECTION=0' r3_18r_aggregate.txt
grep -Fx 'R3_18R_FOLLOWING_PAYLOAD_BITS_CONSUMED=0' r3_18r_aggregate.txt
grep -Fx 'R3_18R_ANOTHER_CONTROL_BITS_CONSUMED=0' r3_18r_aggregate.txt
grep -Fx 'R3_18R_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0' r3_18r_aggregate.txt

echo 'R3_18R_EVIDENCE=PASS'

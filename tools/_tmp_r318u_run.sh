#!/usr/bin/env bash
set -euo pipefail

MAIN='7db2b554611ba27ddf0b98d64f562e9b07011a9f'
MAIN_TREE='8d52bfd710009b12812fd6dd2f38f2fe338c50c3'
PROD='c2765ab9f04f9c981a6868cb6503bdf0e339ce1b'
PROD_TREE='a6f27fe606cd3446da02ef1cb8cf53fff071e383'
LIB_BLOB='cf992670b461e9d923e773ed375bef2b42aea20d'
T_TEST_BLOB='430676ec118fa0755a9c64abc0067bf5c5c88d05'
U_SPEC_BLOB='817515187d89f86a823591bdb6ecce4c386c85d8'
P_CONTRACT_SHA='0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b'
EVIDENCE_BRANCH='evidence/r318u-published-following-payload-v1'

T_IMPL_RUN='32049639448'
T_IMPL_JOB='95445637593'
T_CANDIDATE_CI='32049893219'
T_CANDIDATE_CI_JOB='95446478223'
T_PR_CI='32050205389'
T_PR_CI_JOB='95447503058'
T_PUBLISHED_CI='32050650336'
T_PUBLISHED_CI_JOB='95448937493'
T_CONT_AUTH='32051158916'
T_CONT_AUTH_JOB='95450585726'
T_CONT_CANDIDATE_CI='32051250164'
T_CONT_CANDIDATE_CI_JOB='95450878920'
T_CONT_CANDIDATE_KA='32051250148'
T_CONT_CANDIDATE_KA_JOB='95450878863'
T_CONT_PR_CI='32051617042'
T_CONT_PR_CI_JOB='95452073170'
T_CONT_PR_KA='32051617085'
T_CONT_PR_KA_JOB='95452073277'
T_CONT_PUBLISHED_CI='32054515011'
T_CONT_PUBLISHED_CI_JOB='95461460326'
T_CONT_PUBLISHED_KA='32054514981'
T_CONT_PUBLISHED_KA_JOB='95461461824'

S_HEAD='7fed9a90d2cb1e356b2a388503650b434d7f3f87'
S_TREE='c552e5ef2cb8e7d1cb3b4022b3ff1ec6dc763989'
S_RUN='32047433925'
S_JOB='95438466699'
S_CI_RUN='32047433876'
S_CI_JOB='95438466663'
S_ART='9293436309'
S_ART_NAME='r318s-following-property-payload-evidence'
S_ART_SIZE='18955'
S_ART_DIGEST='sha256:dac07647e288bfc3b177000e1bfa6b9cfd892b80fd77d46c2f4974a3832cf422'

O_HEAD='5046e1594b87ce2828db5faa48aceba456c3166f'
O_RUN='32017369100'
O_JOB='95349613184'
O_ART='9284144768'
O_ART_NAME='r318o-following-property-header-evidence'
O_ART_SIZE='25129'
O_ART_DIGEST='sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d'
O_PROBE_SOURCE='f3e2ad006413e1357102697d7eb0e5cc24e3cefd'

ROOT="$PWD"
TMP="$(mktemp -d)"
S_DIR="$TMP/s"
O_DIR="$TMP/o"
mkdir -p "$S_DIR" "$O_DIR"
trap 'rm -rf "$TMP"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318u_probe.rs"' EXIT

normalize_digest() { printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

echo '== R3.18U authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git merge-base HEAD "$MAIN")" = "$MAIN"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$MAIN:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$MAIN:crates/mimir-replay/tests/r3_18t_following_payload.rs")" = "$T_TEST_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/tests/r3_18t_following_payload.rs")" = "$T_TEST_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18U_EXECUTION_SPEC.md")" = "$U_SPEC_BLOB"
git show "$MAIN:docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json" > r3_18u_contract.json
test "$(sha256sum r3_18u_contract.json | awk '{print $1}')" = "$P_CONTRACT_SHA"

mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=( '.github/workflows/_tmp_r318u_evidence.yml' 'tools/_tmp_r318u_run.sh' )
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 2
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

for run in \
  "$T_IMPL_RUN" "$T_CANDIDATE_CI" "$T_PR_CI" "$T_PUBLISHED_CI" \
  "$T_CONT_AUTH" "$T_CONT_CANDIDATE_CI" "$T_CONT_CANDIDATE_KA" "$T_CONT_PR_CI" "$T_CONT_PR_KA" "$T_CONT_PUBLISHED_CI" "$T_CONT_PUBLISHED_KA" \
  "$S_RUN" "$S_CI_RUN" "$O_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in \
  "$T_IMPL_JOB" "$T_CANDIDATE_CI_JOB" "$T_PR_CI_JOB" "$T_PUBLISHED_CI_JOB" \
  "$T_CONT_AUTH_JOB" "$T_CONT_CANDIDATE_CI_JOB" "$T_CONT_CANDIDATE_KA_JOB" "$T_CONT_PR_CI_JOB" "$T_CONT_PR_KA_JOB" "$T_CONT_PUBLISHED_CI_JOB" "$T_CONT_PUBLISHED_KA_JOB" \
  "$S_JOB" "$S_CI_JOB" "$O_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done

test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$T_PUBLISHED_CI" --jq .head_sha)" = "$PROD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$T_CONT_PUBLISHED_CI" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$T_CONT_PUBLISHED_KA" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$S_RUN" --jq .head_sha)" = "$S_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$S_RUN" --jq .head_commit.tree_id)" = "$S_TREE"
echo 'R3_18U_AUTHORITY_FREEZE=PASS'

echo '== frozen S/O artifacts =='
for spec in \
  "$S_ART|$S_RUN|$S_HEAD|$S_ART_NAME|$S_ART_SIZE|$S_ART_DIGEST|$S_DIR" \
  "$O_ART|$O_RUN|$O_HEAD|$O_ART_NAME|$O_ART_SIZE|$O_ART_DIGEST|$O_DIR"; do
  IFS='|' read -r aid run head name size digest dir <<< "$spec"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.id)" = "$run"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.head_sha)" = "$head"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .name)" = "$name"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .size_in_bytes)" = "$size"
  test "$(normalize_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .digest)")" = "$(normalize_digest "$digest")"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .expired)" = false
  gh run download "$run" -n "$name" -D "$dir"
done
(cd "$S_DIR" && test "$(wc -l < r3_18s_artifact_sha256.txt)" -eq 9 && sha256sum -c r3_18s_artifact_sha256.txt)
(cd "$O_DIR" && test "$(wc -l < r3_18o_artifact_sha256.txt)" -eq 11 && sha256sum -c r3_18o_artifact_sha256.txt)
cp "$S_DIR/r3_18s_replay_identity.tsv" r3_18u_replay_identity.tsv
cp "$S_DIR/r3_18s_frozen_witnesses.json" r3_18u_frozen_witnesses.json
cp "$S_DIR/r3_18s_oracle_summary.json" r3_18u_s_oracle_summary.json

python3 - "$S_DIR/r3_18s_comparison.json" "$O_DIR/r3_18o_header_rows.json" r3_18u_contract.json <<'PY'
import collections,json,sys
s_path,h_path,c_path=sys.argv[1:]
s=json.load(open(s_path,encoding='utf-8'))
h=json.load(open(h_path,encoding='utf-8'))
c=json.load(open(c_path,encoding='utf-8'))
assert s['aggregate']['outcome']=='A' and s['aggregate']['rows']==47 and s['aggregate']['exact_contexts']==18
assert s['aggregate']['boolean_rows']==39 and s['aggregate']['active_actor_rows']==8
assert s['aggregate']['boolean_width_bits']==1 and s['aggregate']['active_actor_width_bits']==33
assert s['aggregate']['oracle_native_mismatch']==0 and s['aggregate']['witness_reselection']==0
assert s['aggregate']['another_control_bits_consumed']==0
assert len(s['rows'])==47 and all(x['oracle_native_exact'] for x in s['rows'])
assert len(h['rows'])==47 and h['aggregate']['native_oracle_mismatch']==0 and h['aggregate']['witness_reselection']==0
fields=('stream_id_bound','prop_id_bits','property_object_index','attribute_tag','version_major','version_minor','net_version')
def contract_tuple(x): return tuple(x[k] for k in fields)
contract=collections.Counter({contract_tuple(x):x['observed_count'] for x in c['admitted_contexts']})
observed=collections.Counter()
for x in h['rows']:
    observed[(x['stream_id_bound'],x['prop_id_bits'],x['resolved_property_object_index'],x['resolved_attribute_tag'],x['version_major'],x['version_minor'],x['net_version'])]+=1
assert contract==observed and len(contract)==18 and sum(contract.values())==47
assert c['membership_policy']=='exact_tuple_only' and c['unique_exact_context_count']==18 and c['observed_row_count']==47
assert all(v is False for v in c['anti_widening'].values())
print('R3_18U_FROZEN_S_AND_CONTRACT=PASS rows=47 contexts=18 reselection=0')
PY

python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18u_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel,expected,status=line.split('\t')
    assert status=='PASS' and not rel.startswith('/') and '..' not in Path(rel).parts
    assert hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower()==expected.lower(), rel
    rows.append(rel.replace('\\','/'))
assert len(rows)==47 and len(set(rows))==47
print('R3_18U_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== derive published T probe =='
git show "$O_PROBE_SOURCE:tools/_tmp_r318o_native_probe.rs" > "$TMP/native.rs"
python3 - "$TMP/native.rs" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected one match, got {n}')
    s=s.replace(old,new,1)
once('ReplayNetworkK2DecodeContextV1, ReplayNetworkLookupPlanReader,',
     'ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1, ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,', 'imports')
once('    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,\n',
     '    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,\n    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1,\n', 'function')
for old,new,label in [
 ('        let _version_major: u32 = f[36].parse()?;','        let version_major: i32 = f[36].parse()?;','major'),
 ('        let _version_minor: u32 = f[37].parse()?;','        let version_minor: i32 = f[37].parse()?;','minor'),
 ('        let _net_version: u32 = f[38].parse()?;','        let net_version: i32 = f[38].parse()?;','net'),
]: once(old,new,label)
needle='''        header_count += 1;\n\n        let repeated = decode_replay_network_existing_actor_first_property_header_v1('''
insert=r'''        header_count += 1;

        let u_context = ReplayNetworkK3DecodeContextV1 {
            version_major,
            version_minor,
            net_version,
            is_rl_223: false,
        };
        let published = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network, &decoded, &plan, u_context,
        )?;
        if published.header_composition.control != control
            || published.header_composition.following_header != following
            || published.header_composition.stop_bit != expected_payload_start
        {
            return Err(format!("{label}: published R3.18T header composition mismatch").into());
        }
        let tag = following.resolved_attribute_tag.ok_or("missing following tag")?;
        let (payload_start, payload_end, payload_width, semantic_bool, semantic_active, semantic_actor) = match &published.following_payload {
            ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::Boolean(value) => {
                if tag != ReplayNetworkAttributeTagV1::Boolean {
                    return Err(format!("{label}: published Boolean variant/tag mismatch").into());
                }
                let semantic = match &value.value {
                    ReplayNetworkPrimitiveScalarValueV1::Boolean(v) => *v,
                    other => return Err(format!("{label}: published Boolean semantic variant {other:?}").into()),
                };
                (value.payload_start_bit, value.payload_end_bit, u64::from(value.payload_width), if semantic {"1"} else {"0"}.to_owned(), "na".to_owned(), "na".to_owned())
            }
            ReplayNetworkExistingActorAfterFirstPrimitiveSecondPropertyPayloadFollowingPayloadValueV1::ActiveActor(value) => {
                if tag != ReplayNetworkAttributeTagV1::ActiveActor {
                    return Err(format!("{label}: published ActiveActor variant/tag mismatch").into());
                }
                let (active, actor) = match &value.value {
                    ReplayNetworkK2ValueV1::ActiveActor { active, actor } => (*active, *actor),
                    other => return Err(format!("{label}: published ActiveActor semantic variant {other:?}").into()),
                };
                (value.payload_start_bit, value.payload_end_bit, value.payload_width, "na".to_owned(), if active {"1"} else {"0"}.to_owned(), actor.to_string())
            }
        };
        if payload_start != expected_payload_start || published.stop_bit != payload_end {
            return Err(format!("{label}: published R3.18T payload boundary mismatch").into());
        }
        let repeated_published = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network, &decoded, &plan, u_context,
        )?;
        let published_repeatability = repeated_published == published;

        let required_bytes = usize::try_from(payload_end.div_ceil(8))?;
        let trunc_len = required_bytes.saturating_sub(1).min(network.len());
        let truncation_negative = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network[..trunc_len], &decoded, &plan, u_context,
        ).is_err();

        let mut bad_actor_prior = decoded.clone();
        bad_actor_prior.header_composition.second_header.as_mut().ok_or("missing second header for wrong-actor negative")?.actor_object_index = u32::MAX;
        let wrong_actor_negative = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network, &bad_actor_prior, &plan, u_context,
        ).is_err();

        let actor_lookup_index = usize::try_from(actor_object)?;
        let mut unresolved_plan = plan.clone();
        if actor_lookup_index >= unresolved_plan.object_lookups.len() {
            return Err(format!("{label}: actor lookup index outside plan").into());
        }
        unresolved_plan.object_lookups[actor_lookup_index] = None;
        let unresolved_lookup_negative = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network, &decoded, &unresolved_plan, u_context,
        ).is_err();

        let wrong_context_negative = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network,
            &decoded,
            &plan,
            ReplayNetworkK3DecodeContextV1 { version_major, version_minor: version_minor - 1, net_version, is_rl_223: false },
        ).is_err();

        let mut fabricated_plan = plan.clone();
        let fabricated_entry = fabricated_plan.object_lookups.get_mut(actor_lookup_index).and_then(Option::as_mut).ok_or("missing actor lookup for fabricated context")?;
        let fabricated_property = fabricated_entry.properties.iter_mut().find(|property| property.stream_id == expected_stream_id).ok_or("missing following property for fabricated context")?;
        fabricated_property.object_index = if fabricated_property.object_index == 0 { 1 } else { 0 };
        let fabricated_context_negative = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &network, &decoded, &fabricated_plan, u_context,
        ).is_err();

        let mut poisoned = network.clone();
        for offset in 0..16u64 {
            set_bit(&mut poisoned, published.stop_bit + offset, offset % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let after_poison = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &poisoned, &decoded, &plan, u_context,
        )?;
        let post_payload_poison = after_poison == published;

        if !published_repeatability || !truncation_negative || !wrong_actor_negative || !unresolved_lookup_negative || !wrong_context_negative || !fabricated_context_negative || !post_payload_poison {
            return Err(format!("{label}: R3.18U published negative/repeatability failure").into());
        }

        println!(
            "R3_18U_PUBLISHED\tlabel={label}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\ttag={:?}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_bool={}\tsemantic_active={}\tsemantic_actor={}\theader_identity=1\trepeatability=1\ttruncation=1\twrong_actor=1\tunresolved_lookup=1\twrong_context=1\tfabricated_context=1\tpost_payload_poison=1\tanother_control_bits_consumed=0",
            _frame_index,
            _actor_ordinal,
            actor_object,
            expected_present_start,
            tag,
            payload_start,
            payload_end,
            payload_width,
            semantic_bool,
            semantic_active,
            semantic_actor,
        );

        let repeated = decode_replay_network_existing_actor_first_property_header_v1('''
once(needle,insert,'published insertion')
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18U_PUBLISHED_PROBE_DERIVATION=PASS')
PY
mkdir -p crates/mimir-replay/examples
cp "$TMP/native.rs" crates/mimir-replay/examples/_tmp_r318u_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318u_probe -- "$O_DIR/r3_18o_targets.tsv" > "$TMP/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318u_probe -- "$O_DIR/r3_18o_targets.tsv" > "$TMP/native2.log"
cmp "$TMP/native1.log" "$TMP/native2.log"
test "$(grep -c $'^R3_18U_PUBLISHED\t' "$TMP/native1.log")" -eq 47
rm crates/mimir-replay/examples/_tmp_r318u_probe.rs

echo '== exact published-T versus frozen-S comparison =='
python3 - "$S_DIR/r3_18s_comparison.json" "$O_DIR/r3_18o_header_rows.json" "$TMP/native1.log" r3_18u_contract.json <<'PY'
import collections,json,sys
s_path,h_path,native_path,c_path=sys.argv[1:]
def parse(path,prefix):
    out={}
    for line in open(path,encoding='utf-8',errors='replace'):
        if not line.startswith(prefix+'\t'): continue
        row={}
        for item in line.rstrip('\n').split('\t')[1:]:
            k,v=item.split('=',1); row[k]=v
        assert row['label'] not in out
        out[row['label']]=row
    return out
s=json.load(open(s_path,encoding='utf-8'))
h=json.load(open(h_path,encoding='utf-8'))
c=json.load(open(c_path,encoding='utf-8'))
native=parse(native_path,'R3_18U_PUBLISHED')
srows={x['label']:x for x in s['rows']}
hrows={x['label']:x for x in h['rows']}
assert len(native)==len(srows)==len(hrows)==47 and set(native)==set(srows)==set(hrows)
rows=[]; tags=collections.Counter(); contexts=collections.Counter()
for label in sorted(srows):
    frozen=srows[label]; n=native[label]; hh=hrows[label]
    assert n['tag']==frozen['tag']==hh['resolved_attribute_tag']
    assert int(n['frame_index'])==frozen['frame_index']
    assert int(n['actor_ordinal'])==frozen['actor_ordinal']
    assert int(n['actor_context_object_id'])==frozen['actor_context_object_id']
    assert int(n['property_present_start_bit'])==frozen['property_present_start_bit']
    assert int(n['payload_start_bit'])==frozen['payload_start_bit']==hh['payload_start_bit']
    assert int(n['payload_end_bit'])==frozen['payload_end_bit']
    assert int(n['payload_width'])==frozen['payload_width']
    assert n['semantic_bool']==frozen['semantic_bool']
    assert n['semantic_active']==frozen['semantic_active']
    assert n['semantic_actor']==frozen['semantic_actor']
    for key in ['header_identity','repeatability','truncation','wrong_actor','unresolved_lookup','wrong_context','fabricated_context','post_payload_poison']:
        assert n[key]=='1', (label,key,n[key])
    assert n['another_control_bits_consumed']=='0'
    tags[n['tag']]+=1
    contexts[(hh['stream_id_bound'],hh['prop_id_bits'],hh['resolved_property_object_index'],hh['resolved_attribute_tag'],hh['version_major'],hh['version_minor'],hh['net_version'])]+=1
    rows.append({
      'label':label,'frame_index':int(n['frame_index']),'actor_ordinal':int(n['actor_ordinal']),
      'actor_context_object_id':int(n['actor_context_object_id']),'property_present_start_bit':int(n['property_present_start_bit']),
      'tag':n['tag'],'payload_start_bit':int(n['payload_start_bit']),'payload_end_bit':int(n['payload_end_bit']),
      'payload_width':int(n['payload_width']),'semantic_bool':n['semantic_bool'],'semantic_active':n['semantic_active'],
      'semantic_actor':n['semantic_actor'],'published_t_frozen_s_exact':True,'header_identity':True,
      'repeatability':True,'truncation_negative':True,'wrong_actor_negative':True,'unresolved_lookup_negative':True,
      'wrong_context_negative':True,'fabricated_context_negative':True,'post_payload_poison_invariant':True,
      'another_control_bits_consumed':0,
    })
contract=collections.Counter()
for x in c['admitted_contexts']:
    contract[(x['stream_id_bound'],x['prop_id_bits'],x['property_object_index'],x['attribute_tag'],x['version_major'],x['version_minor'],x['net_version'])]=x['observed_count']
assert contexts==contract and len(contexts)==18 and sum(contexts.values())==47
assert tags==collections.Counter({'Boolean':39,'ActiveActor':8}), tags
result={'aggregate':{
 'outcome':'A','rows':47,'exact_contexts':18,'boolean_rows':39,'active_actor_rows':8,
 'boolean_width_bits':1,'active_actor_width_bits':33,'published_t_frozen_s_mismatch':0,'header_identity':'47/47',
 'witness_reselection':0,'repeatability':'47/47','truncation_negative':'47/47','wrong_actor_negative':'47/47',
 'unresolved_lookup_negative':'47/47','wrong_context_negative':'47/47','fabricated_context_negative':'47/47',
 'post_payload_poison_invariance':'47/47','another_control_bits_consumed':0,
 'production_cargo_fixture_corpus_support_mutation':'0/0/0/0/0','privacy_scan':'PASS'},
 'rows':rows}
json.dump(result,open('r3_18u_comparison.json','w',encoding='utf-8'),indent=2,sort_keys=True); open('r3_18u_comparison.json','a').write('\n')
json.dump({'rows':47,'exact_contexts':18,'tags':dict(sorted(tags.items())),'widths':{'Boolean':1,'ActiveActor':33},'published_t_frozen_s_mismatch':0,'witness_reselection':0},open('r3_18u_summary.json','w',encoding='utf-8'),indent=2,sort_keys=True); open('r3_18u_summary.json','a').write('\n')
print('R3_18U_PUBLISHED_DIFFERENTIAL=PASS rows=47 contexts=18 mismatch=0 Boolean=39 ActiveActor=8')
PY

cat > r3_18u_negative_controls.txt <<'EOF'
R3_18U_REPEATABILITY=47/47
R3_18U_TRUNCATION_NEGATIVE=47/47
R3_18U_WRONG_ACTOR_NEGATIVE=47/47
R3_18U_UNRESOLVED_LOOKUP_NEGATIVE=47/47
R3_18U_WRONG_EXACT_CONTEXT_NEGATIVE=47/47
R3_18U_FABRICATED_CONTEXT_NEGATIVE=47/47
R3_18U_POST_PAYLOAD_AND_NEXT_CONTROL_POISON_INVARIANCE=47/47
R3_18U_ANOTHER_CONTROL_BITS_CONSUMED=0
EOF
cat > r3_18u_aggregate.txt <<'EOF'
R3_18U_OUTCOME=A
R3_18U_FROZEN_ROWS=47/47
R3_18U_EXACT_CONTEXTS=18/18
R3_18U_BOOLEAN_ROWS=39
R3_18U_ACTIVE_ACTOR_ROWS=8
R3_18U_BOOLEAN_WIDTH_BITS=1
R3_18U_ACTIVE_ACTOR_WIDTH_BITS=33
R3_18U_PUBLISHED_T_FROZEN_S_MISMATCH=0
R3_18U_HEADER_IDENTITY=47/47
R3_18U_WITNESS_RESELECTION=0
R3_18U_REPEATABILITY=47/47
R3_18U_TRUNCATION_NEGATIVE=47/47
R3_18U_WRONG_ACTOR_NEGATIVE=47/47
R3_18U_UNRESOLVED_LOOKUP_NEGATIVE=47/47
R3_18U_WRONG_EXACT_CONTEXT_NEGATIVE=47/47
R3_18U_FABRICATED_CONTEXT_NEGATIVE=47/47
R3_18U_POST_PAYLOAD_AND_NEXT_CONTROL_POISON_INVARIANCE=47/47
R3_18U_ANOTHER_CONTROL_BITS_CONSUMED=0
R3_18U_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18U_PRIVACY_SCAN=PASS
EOF

printf '%s\n' "${changed[@]}" > r3_18u_source_scope.txt
cat > r3_18u_upstream_receipts.txt <<EOF
MAIN=$MAIN
MAIN_TREE=$MAIN_TREE
PRODUCTION=$PROD
PRODUCTION_TREE=$PROD_TREE
LIB_BLOB=$LIB_BLOB
T_TEST_BLOB=$T_TEST_BLOB
R318P_CONTRACT_SHA256=$P_CONTRACT_SHA
R318T_IMPLEMENTATION=$T_IMPL_RUN/$T_IMPL_JOB
R318T_CANDIDATE_CI=$T_CANDIDATE_CI/$T_CANDIDATE_CI_JOB
R318T_PR_CI=$T_PR_CI/$T_PR_CI_JOB
R318T_PUBLISHED_CI=$T_PUBLISHED_CI/$T_PUBLISHED_CI_JOB
R318T_CONTINUITY_AUTHORITY=$T_CONT_AUTH/$T_CONT_AUTH_JOB
R318T_CONTINUITY_PUBLISHED_CI=$T_CONT_PUBLISHED_CI/$T_CONT_PUBLISHED_CI_JOB
R318T_CONTINUITY_PUBLISHED_KA=$T_CONT_PUBLISHED_KA/$T_CONT_PUBLISHED_KA_JOB
R318S_HEAD_TREE=$S_HEAD/$S_TREE
R318S_AUTHORITY=$S_RUN/$S_JOB
R318S_ARTIFACT=$S_ART/$S_ART_SIZE/$S_ART_DIGEST
R318O_ARTIFACT=$O_ART/$O_ART_SIZE/$O_ART_DIGEST
EOF

python3 - <<'PY'
from pathlib import Path
for path in ['r3_18u_comparison.json','r3_18u_summary.json','r3_18u_negative_controls.txt','r3_18u_aggregate.txt','r3_18u_source_scope.txt','r3_18u_upstream_receipts.txt','r3_18u_contract.json']:
    text=Path(path).read_text(encoding='utf-8')
    assert '/home/' not in text and '/Users/' not in text and '\\Users\\' not in text
    assert 'window_hex=' not in text and 'raw_payload' not in text
print('R3_18U_PRIVACY_SCAN=PASS')
PY

echo '== validation =='
cargo +1.85.0 test -p mimir-replay --test r3_18t_following_payload
cargo +1.85.0 test -p mimir-replay
cargo +1.85.0 check --workspace --all-targets
cargo +1.85.0 test --workspace --all-targets
cargo +1.85.0 clippy --workspace --all-targets -- -D warnings
pwsh -File ./scripts/verify_repo.ps1

git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

files=(
 r3_18u_source_scope.txt
 r3_18u_replay_identity.tsv
 r3_18u_frozen_witnesses.json
 r3_18u_upstream_receipts.txt
 r3_18u_contract.json
 r3_18u_s_oracle_summary.json
 r3_18u_summary.json
 r3_18u_comparison.json
 r3_18u_negative_controls.txt
 r3_18u_aggregate.txt
)
: > r3_18u_artifact_sha256.txt
for file in "${files[@]}"; do sha256sum "$file" >> r3_18u_artifact_sha256.txt; done
sha256sum -c r3_18u_artifact_sha256.txt
cat r3_18u_aggregate.txt
echo 'R3_18U_EVIDENCE=PASS'

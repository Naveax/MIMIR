#!/usr/bin/env bash
set -euo pipefail

MAIN='f2b644389b9d18c95fa13fd1ba5a32ce32d1145e'
MAIN_TREE='efd0b7f5cae288a11a2ff9f0a9bca301d664a3c0'
PROD='f41c59d26ed6c810a640b4fa8cd76129decb32aa'
PROD_TREE='606db4b5778e5218f2bd0117cc5dd72d7f3e37a5'
LIB_BLOB='b01b1e8629a4f4bc2452e67024ffb0d064bf58fb'
S_SPEC_BLOB='53c8d97d717cbca8a222bb8613f2670c64aab0d5'
R_DECISION_BLOB='1b3983f3d65443bfabfad2665ea27b5d16a2fa6b'
P_CONTRACT_SHA='0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b'

R_HEAD='47bf441f2c795702e4ee75c66b4dbe710ccc9a9c'
R_TREE='0dd95a0f8d4e8729191176d1e2614cbafd75d80e'
R_RUN='32044430149'
R_JOB='95429267025'
R_CI_RUN='32044430126'
R_CI_JOB='95429266690'
R_ART='9292549978'
R_ART_NAME='r318r-published-following-header-differential-evidence'
R_ART_SIZE='18820'
R_ART_DIGEST='sha256:142a2480f38a7ddc4f74e73dd9ce84ed70ccd740645f05d2e90579825927220f'
R_ADMISSION_RUN='32045289930'
R_ADMISSION_JOB='95431702360'
R_CANDIDATE_CI='32045389127'
R_CANDIDATE_KA='32045389181'
R_PR_CI='32045699374'
R_PR_KA='32045699384'
R_PUBLISHED_CI='32046037269'
R_PUBLISHED_KA='32046037338'

O_HEAD='5046e1594b87ce2828db5faa48aceba456c3166f'
O_RUN='32017369100'
O_JOB='95349613184'
O_ART='9284144768'
O_ART_NAME='r318o-following-property-header-evidence'
O_ART_SIZE='25129'
O_ART_DIGEST='sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d'
O_PROBE_SOURCE='f3e2ad006413e1357102697d7eb0e5cc24e3cefd'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'
EVIDENCE_BRANCH='evidence/r318s-following-payload-v1'

ROOT="$PWD"
TMP="$(mktemp -d)"
O_DIR="$TMP/o"
R_DIR="$TMP/r"
BOXCARS="$TMP/boxcars"
mkdir -p "$O_DIR" "$R_DIR"
trap 'rm -rf "$TMP"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318s_probe.rs"' EXIT

normalize_digest() { printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

echo '== R3.18S authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git merge-base HEAD "$MAIN")" = "$MAIN"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$MAIN:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18S_EXECUTION_SPEC.md")" = "$S_SPEC_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18R_DECISION.md")" = "$R_DECISION_BLOB"
git show "$MAIN:docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json" > "$TMP/r3_18p_contract.json"
test "$(sha256sum "$TMP/r3_18p_contract.json" | awk '{print $1}')" = "$P_CONTRACT_SHA"

mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=(
  '.github/workflows/_tmp_r318s_evidence.yml'
  'tools/_tmp_r318s_extend_boxcars.py'
  'tools/_tmp_r318s_run.sh'
)
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 3
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md
mapfile -t prod_drift < <(git diff --name-only "$PROD" "$MAIN" -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts | sort)
test "${#prod_drift[@]}" -eq 0

for run in "$R_RUN" "$R_CI_RUN" "$R_ADMISSION_RUN" "$R_CANDIDATE_CI" "$R_CANDIDATE_KA" "$R_PR_CI" "$R_PR_KA" "$R_PUBLISHED_CI" "$R_PUBLISHED_KA" "$O_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$R_JOB" "$R_CI_JOB" "$R_ADMISSION_JOB" "$O_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R_RUN" --jq .head_sha)" = "$R_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R_RUN" --jq .head_commit.tree_id)" = "$R_TREE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R_PUBLISHED_CI" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$R_PUBLISHED_KA" --jq .head_sha)" = "$MAIN"

echo 'R3_18S_AUTHORITY_FREEZE=PASS'

echo '== frozen upstream artifacts =='
for spec in \
  "$R_ART|$R_RUN|$R_HEAD|$R_ART_NAME|$R_ART_SIZE|$R_ART_DIGEST|$R_DIR" \
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
(cd "$O_DIR" && test "$(wc -l < r3_18o_artifact_sha256.txt)" -eq 11 && sha256sum -c r3_18o_artifact_sha256.txt)
(cd "$R_DIR" && test "$(wc -l < r3_18r_artifact_sha256.txt)" -eq 8 && sha256sum -c r3_18r_artifact_sha256.txt)
cp "$O_DIR/r3_18o_replay_identity.tsv" r3_18s_replay_identity.tsv
cp "$O_DIR/r3_18o_frozen_witnesses.json" r3_18s_frozen_witnesses.json
python3 - "$O_DIR/r3_18o_header_rows.json" "$R_DIR/r3_18r_comparison.json" <<'PY'
import json,sys
h=json.load(open(sys.argv[1],encoding='utf-8'))
r=json.load(open(sys.argv[2],encoding='utf-8'))
assert len(h['rows'])==47 and h['aggregate']['distinct_exact_header_context_tuples']==18
assert all(x['native_oracle_exact'] for x in h['rows'])
assert all(x['following_payload_bits_consumed']==0 and x['another_control_bits_consumed']==0 for x in h['rows'])
assert r['aggregate']['rows']==47 and r['aggregate']['distinct_exact_header_context_tuples']==18
assert r['aggregate']['published_q_native_mismatch']==0
print('R3_18S_UPSTREAM_LANE=PASS rows=47 contexts=18 reselection=0')
PY
python3 - <<'PY'
import hashlib
from pathlib import Path
rows=[]
for line in Path('r3_18s_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel,expected,status=line.split('\t')
    assert status=='PASS' and not rel.startswith('/') and '..' not in Path(rel).parts
    assert hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower()==expected.lower(), rel
    rows.append(rel.replace('\\','/'))
assert len(rows)==47 and len(set(rows))==47
print('R3_18S_REPLAY_IDENTITY=PASS rows=47')
PY

echo '== pinned Boxcars payload oracle =='
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$TMP/boxcars_base_patch.py"
python3 - "$TMP/boxcars_base_patch.py" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
assert s.count('    stream_id_bound: i32,\n')==1
s=s.replace('    stream_id_bound: i32,\n','    stream_id_bound: u32,\n',1)
s=s.replace('R3_18C','R3_18O').replace('r3_18c','r3_18o')
needle='                        if r3_18o_property_ordinal == 1 {\n'
assert s.count(needle)==1
s=s.replace(needle,'                        if false && r3_18o_property_ordinal == 1 {\n',1)
p.write_text(s,encoding='utf-8',newline='\n')
PY
python3 "$TMP/boxcars_base_patch.py" "$BOXCARS"
git show "$O_HEAD:tools/_tmp_r318o_extend_boxcars.py" > "$TMP/r318o_extend.py"
python3 "$TMP/r318o_extend.py" "$BOXCARS"
python3 tools/_tmp_r318s_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18o_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18o_probe.rs Cargo.toml > "$TMP/r318s_boxcars.patch"
sha256sum "$TMP/r318s_boxcars.patch" | sed 's#  .*#  r318s_boxcars_payload_instrumentation.patch#' > r3_18s_boxcars_instrumentation_sha256.txt
cargo +stable build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18o_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18o_probe"
test -x "$PROBE"
python3 - "$O_DIR/r3_18o_targets.tsv" "$TMP/oracle_requests.tsv" <<'PY'
import sys
src,dst=sys.argv[1:]
out=[]
for line in open(src,encoding='utf-8'):
    if not line.strip(): continue
    f=line.rstrip('\n').split('\t'); assert len(f)==39
    out.append('\t'.join([f[0],f[24],f[25],f[1],f[26]]))
assert len(out)==47
open(dst,'w',encoding='utf-8',newline='\n').write('\n'.join(out)+'\n')
PY
: > "$TMP/oracle.log"
while IFS=$'\t' read -r rel frame actor_ordinal actor_object property_start; do
  MIMIR_R3_18O_LABEL="$rel" \
  MIMIR_R3_18O_TARGET_FRAME="$frame" \
  MIMIR_R3_18O_TARGET_ACTOR_ORDINAL="$actor_ordinal" \
  MIMIR_R3_18O_TARGET_ACTOR_OBJECT="$actor_object" \
  MIMIR_R3_18O_TARGET_PROPERTY_START="$property_start" \
    "$PROBE" "$ROOT/$rel" >> "$TMP/oracle.log" 2>&1
done < "$TMP/oracle_requests.tsv"
test "$(grep -c $'^R3_18S_ORACLE\t' "$TMP/oracle.log")" -eq 47

echo '== derive native payload candidate probe =='
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
     'ReplayNetworkK2DecodeContextV1, ReplayNetworkK2ValueV1, ReplayNetworkK3DecodeContextV1, ReplayNetworkLookupPlanReader, ReplayNetworkPrimitiveScalarValueV1,', 'imports')
once('    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,\n',
     '    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_control_v1,\n    decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1,\n    decode_replay_network_k2_v1,\n    decode_replay_network_primitive_scalar_v1,\n', 'functions')
for old,new,label in [
 ('        let _version_major: u32 = f[36].parse()?;','        let version_major: i32 = f[36].parse()?;','major'),
 ('        let _version_minor: u32 = f[37].parse()?;','        let version_minor: i32 = f[37].parse()?;','minor'),
 ('        let _net_version: u32 = f[38].parse()?;','        let net_version: i32 = f[38].parse()?;','net'),
]: once(old,new,label)
needle='''        header_count += 1;\n\n        let repeated = decode_replay_network_existing_actor_first_property_header_v1('''
insert=r'''        header_count += 1;

        let q_context = ReplayNetworkK3DecodeContextV1 {
            version_major,
            version_minor,
            net_version,
            is_rl_223: false,
        };
        let q = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
            &network, &decoded, &plan, q_context,
        )?;
        if q.control != control || q.following_header != following || q.stop_bit != expected_payload_start {
            return Err(format!("{label}: R3.18Q reconstruction mismatch").into());
        }
        let q_wrong_version = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_header_v1(
            &network,
            &decoded,
            &plan,
            ReplayNetworkK3DecodeContextV1 {
                version_major,
                version_minor: version_minor - 1,
                net_version,
                is_rl_223: false,
            },
        ).is_err();
        if !q_wrong_version {
            return Err(format!("{label}: wrong exact structural/version context was not rejected").into());
        }

        let payload_start = q.stop_bit;
        let k2 = ReplayNetworkK2DecodeContextV1 { net_version, is_rl_223: false };
        let tag = following.resolved_attribute_tag.ok_or("missing following tag")?;
        let (payload_end, payload_width, semantic_bool, semantic_active, semantic_actor, repeatability_payload, truncation, wrong_decoder, post_payload_poison) = match tag {
            ReplayNetworkAttributeTagV1::Boolean => {
                let value = decode_replay_network_primitive_scalar_v1(&network, payload_start, tag)?;
                let semantic = match value.value {
                    ReplayNetworkPrimitiveScalarValueV1::Boolean(v) => v,
                    _ => return Err("Boolean decoder returned wrong value variant".into()),
                };
                let repeated_value = decode_replay_network_primitive_scalar_v1(&network, payload_start, tag)?;
                let required_bytes = usize::try_from(value.payload_end_bit.div_ceil(8))?;
                let trunc_len = required_bytes.saturating_sub(1).min(network.len());
                let trunc = decode_replay_network_primitive_scalar_v1(&network[..trunc_len], payload_start, tag).is_err();
                let wrong = decode_replay_network_k2_v1(&network, payload_start, tag, k2).is_err();
                let mut poisoned = network.clone();
                for offset in 0..16u64 {
                    set_bit(&mut poisoned, value.payload_end_bit + offset, offset % 2 == 0)
                        .map_err(std::io::Error::other)?;
                }
                let poisoned_value = decode_replay_network_primitive_scalar_v1(&poisoned, payload_start, tag)?;
                (value.payload_end_bit, u64::from(value.payload_width), if semantic {"1"} else {"0"}.to_owned(), "na".to_owned(), "na".to_owned(), repeated_value == value, trunc, wrong, poisoned_value == value)
            }
            ReplayNetworkAttributeTagV1::ActiveActor => {
                let value = decode_replay_network_k2_v1(&network, payload_start, tag, k2)?;
                let (active, actor) = match value.value {
                    ReplayNetworkK2ValueV1::ActiveActor { active, actor } => (active, actor),
                    _ => return Err("ActiveActor decoder returned wrong value variant".into()),
                };
                let repeated_value = decode_replay_network_k2_v1(&network, payload_start, tag, k2)?;
                let required_bytes = usize::try_from(value.payload_end_bit.div_ceil(8))?;
                let trunc_len = required_bytes.saturating_sub(1).min(network.len());
                let trunc = decode_replay_network_k2_v1(&network[..trunc_len], payload_start, tag, k2).is_err();
                let wrong = decode_replay_network_primitive_scalar_v1(&network, payload_start, tag).is_err();
                let mut poisoned = network.clone();
                for offset in 0..16u64 {
                    set_bit(&mut poisoned, value.payload_end_bit + offset, offset % 2 == 0)
                        .map_err(std::io::Error::other)?;
                }
                let poisoned_value = decode_replay_network_k2_v1(&poisoned, payload_start, tag, k2)?;
                (value.payload_end_bit, value.payload_width, "na".to_owned(), if active {"1"} else {"0"}.to_owned(), actor.to_string(), repeated_value == value, trunc, wrong, poisoned_value == value)
            }
            other => return Err(format!("{label}: unsupported R3.18S payload tag {other:?}").into()),
        };
        if !repeatability_payload || !truncation || !wrong_decoder || !post_payload_poison {
            return Err(format!("{label}: R3.18S negative/repeatability failure").into());
        }
        println!(
            "R3_18S_NATIVE\tlabel={label}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tproperty_present_start_bit={}\ttag={:?}\tpayload_start_bit={}\tpayload_end_bit={}\tpayload_width={}\tsemantic_bool={}\tsemantic_active={}\tsemantic_actor={}\tq_wrong_context=1\trepeatability=1\ttruncation=1\twrong_decoder=1\tpost_payload_poison=1\tmalformed_domain=total_fixed_width_no_invalid_full_width_pattern\tanother_control_bits_consumed=0",
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
once(needle,insert,'payload insertion')
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18S_NATIVE_PROBE_DERIVATION=PASS')
PY
cp "$TMP/native.rs" crates/mimir-replay/examples/_tmp_r318s_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318s_probe -- "$O_DIR/r3_18o_targets.tsv" > "$TMP/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318s_probe -- "$O_DIR/r3_18o_targets.tsv" > "$TMP/native2.log"
cmp "$TMP/native1.log" "$TMP/native2.log"
test "$(grep -c $'^R3_18S_NATIVE\t' "$TMP/native1.log")" -eq 47
rm crates/mimir-replay/examples/_tmp_r318s_probe.rs

echo '== exact oracle/native comparison =='
python3 - "$O_DIR/r3_18o_header_rows.json" "$TMP/oracle.log" "$TMP/native1.log" <<'PY'
import json,sys,collections
header_path,oracle_path,native_path=sys.argv[1:]
def parse(path,prefix):
    out={}
    for line in open(path,encoding='utf-8',errors='replace'):
        if not line.startswith(prefix+'\t'): continue
        row={}
        for item in line.rstrip('\n').split('\t')[1:]:
            k,v=item.split('=',1); row[k]=v
        key=row['label']
        assert key not in out, key
        out[key]=row
    return out
oracle=parse(oracle_path,'R3_18S_ORACLE')
native=parse(native_path,'R3_18S_NATIVE')
h=json.load(open(header_path,encoding='utf-8'))
headers={r['label']:r for r in h['rows']}
assert len(headers)==len(oracle)==len(native)==47 and set(headers)==set(oracle)==set(native)
rows=[]; tags=collections.Counter(); contexts=collections.Counter()
for label in sorted(headers):
    hh=headers[label]; o=oracle[label]; n=native[label]
    for k in ['tag','payload_start_bit','payload_end_bit','payload_width','semantic_bool','semantic_active','semantic_actor']:
        assert o[k]==n[k], (label,k,o[k],n[k])
    assert o['tag']==hh['resolved_attribute_tag']
    assert int(o['payload_start_bit'])==hh['payload_start_bit']
    assert n['q_wrong_context']=='1' and n['repeatability']=='1' and n['truncation']=='1' and n['wrong_decoder']=='1' and n['post_payload_poison']=='1'
    assert n['another_control_bits_consumed']=='0'
    expected_width=1 if o['tag']=='Boolean' else 33
    assert int(o['payload_width'])==expected_width
    tags[o['tag']]+=1
    contexts[(hh['stream_id_bound'],hh['prop_id_bits'],hh['resolved_property_object_index'],hh['resolved_attribute_tag'],hh['version_major'],hh['version_minor'],hh['net_version'])]+=1
    rows.append({
      'label':label,'frame_index':int(o['frame_index']),'actor_ordinal':int(o['actor_ordinal']),
      'actor_context_object_id':int(o['actor_context_object_id']),'property_present_start_bit':int(o['property_present_start_bit']),
      'tag':o['tag'],'payload_start_bit':int(o['payload_start_bit']),'payload_end_bit':int(o['payload_end_bit']),
      'payload_width':int(o['payload_width']),'semantic_bool':o['semantic_bool'],'semantic_active':o['semantic_active'],
      'semantic_actor':o['semantic_actor'],'oracle_native_exact':True,'repeatability':True,'truncation_negative':True,
      'wrong_decoder_negative':True,'wrong_exact_context_negative':True,'post_payload_poison_invariant':True,
      'malformed_domain':'total_fixed_width_no_invalid_full_width_pattern','another_control_bits_consumed':0,
    })
assert tags==collections.Counter({'Boolean':39,'ActiveActor':8}), tags
assert len(contexts)==18
result={'aggregate':{
 'outcome':'A','rows':47,'exact_contexts':18,'boolean_rows':39,'active_actor_rows':8,
 'boolean_width_bits':1,'active_actor_width_bits':33,'oracle_native_mismatch':0,'witness_reselection':0,
 'repeatability':'47/47','truncation_negative':'47/47','wrong_decoder_negative':'47/47','wrong_exact_context_negative':'47/47',
 'post_payload_poison_invariance':'47/47','malformed_domain':'fixed-width total domain; no invalid full-width bit pattern exists',
 'another_control_bits_consumed':0,'production_cargo_fixture_corpus_support_mutation':'0/0/0/0/0','privacy_scan':'PASS'},
 'rows':rows}
json.dump(result,open('r3_18s_comparison.json','w',encoding='utf-8'),indent=2,sort_keys=True); open('r3_18s_comparison.json','a').write('\n')
json.dump({'rows':47,'exact_contexts':18,'tags':dict(sorted(tags.items())),'widths':{'Boolean':1,'ActiveActor':33},'witness_reselection':0},open('r3_18s_oracle_summary.json','w',encoding='utf-8'),indent=2,sort_keys=True); open('r3_18s_oracle_summary.json','a').write('\n')
print('R3_18S_ORACLE_NATIVE_COMPARISON=PASS rows=47 contexts=18 mismatch=0 Boolean=39 ActiveActor=8')
PY

cat > r3_18s_negative_controls.txt <<'EOF'
R3_18S_REPEATABILITY=47/47
R3_18S_TRUNCATION_NEGATIVE=47/47
R3_18S_WRONG_DECODER_NEGATIVE=47/47
R3_18S_WRONG_EXACT_CONTEXT_NEGATIVE=47/47
R3_18S_POST_PAYLOAD_AND_NEXT_CONTROL_POISON_INVARIANCE=47/47
R3_18S_MALFORMED_DOMAIN=TOTAL_FIXED_WIDTH_NO_INVALID_FULL_WIDTH_PATTERN
R3_18S_ANOTHER_CONTROL_BITS_CONSUMED=0
EOF
cat > r3_18s_aggregate.txt <<'EOF'
R3_18S_OUTCOME=A
R3_18S_FROZEN_ROWS=47/47
R3_18S_EXACT_CONTEXTS=18/18
R3_18S_BOOLEAN_ROWS=39
R3_18S_ACTIVE_ACTOR_ROWS=8
R3_18S_BOOLEAN_WIDTH_BITS=1
R3_18S_ACTIVE_ACTOR_WIDTH_BITS=33
R3_18S_ORACLE_NATIVE_MISMATCH=0
R3_18S_WITNESS_RESELECTION=0
R3_18S_REPEATABILITY=47/47
R3_18S_TRUNCATION_NEGATIVE=47/47
R3_18S_WRONG_DECODER_NEGATIVE=47/47
R3_18S_WRONG_EXACT_CONTEXT_NEGATIVE=47/47
R3_18S_POST_PAYLOAD_AND_NEXT_CONTROL_POISON_INVARIANCE=47/47
R3_18S_MALFORMED_DOMAIN=TOTAL_FIXED_WIDTH_NO_INVALID_FULL_WIDTH_PATTERN
R3_18S_ANOTHER_CONTROL_BITS_CONSUMED=0
R3_18S_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18S_PRIVACY_SCAN=PASS
EOF

printf '%s\n' "${changed[@]}" > r3_18s_source_scope.txt
cat > r3_18s_upstream_receipts.txt <<EOF
MAIN=$MAIN
MAIN_TREE=$MAIN_TREE
PRODUCTION=$PROD
PRODUCTION_TREE=$PROD_TREE
R318P_CONTRACT_SHA256=$P_CONTRACT_SHA
R318R_HEAD=$R_HEAD
R318R_TREE=$R_TREE
R318R_RUN_JOB=$R_RUN/$R_JOB
R318R_ARTIFACT=$R_ART/$R_ART_SIZE/$R_ART_DIGEST
R318R_PUBLISHED_CI=$R_PUBLISHED_CI
R318R_PUBLISHED_KA=$R_PUBLISHED_KA
R318O_ARTIFACT=$O_ART/$O_ART_SIZE/$O_ART_DIGEST
BOXCARS_SHA=$BOXCARS_SHA
EOF

python3 - <<'PY'
from pathlib import Path
for path in ['r3_18s_comparison.json','r3_18s_oracle_summary.json','r3_18s_negative_controls.txt','r3_18s_aggregate.txt','r3_18s_source_scope.txt','r3_18s_upstream_receipts.txt']:
    text=Path(path).read_text(encoding='utf-8')
    assert '/home/' not in text and '/Users/' not in text and '\\Users\\' not in text
    assert 'window_hex=' not in text
print('R3_18S_PRIVACY_SCAN=PASS')
PY

echo '== validation =='
cargo +1.85.0 test -p mimir-replay --test r3_18q_following_header
cargo +1.85.0 test -p mimir-replay
cargo +1.85.0 check --workspace --all-targets
cargo +1.85.0 test --workspace --all-targets
cargo +1.85.0 clippy --workspace --all-targets -- -D warnings
pwsh -File ./scripts/verify_repo.ps1

git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

files=(
 r3_18s_source_scope.txt
 r3_18s_replay_identity.tsv
 r3_18s_frozen_witnesses.json
 r3_18s_upstream_receipts.txt
 r3_18s_boxcars_instrumentation_sha256.txt
 r3_18s_oracle_summary.json
 r3_18s_comparison.json
 r3_18s_negative_controls.txt
 r3_18s_aggregate.txt
)
: > r3_18s_artifact_sha256.txt
for file in "${files[@]}"; do sha256sum "$file" >> r3_18s_artifact_sha256.txt; done
sha256sum -c r3_18s_artifact_sha256.txt
cat r3_18s_aggregate.txt
echo 'R3_18S_EVIDENCE=PASS'

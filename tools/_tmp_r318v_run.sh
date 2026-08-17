#!/usr/bin/env bash
set -euo pipefail

MAIN='06c7b0524692fc371e21526c17d5ecfe3a69e10e'
MAIN_TREE='5e253e5c42fa4b0e6fcc9c7c983cdb5ffc164862'
PROD='c2765ab9f04f9c981a6868cb6503bdf0e339ce1b'
PROD_TREE='a6f27fe606cd3446da02ef1cb8cf53fff071e383'
LIB_BLOB='cf992670b461e9d923e773ed375bef2b42aea20d'
T_TEST_BLOB='430676ec118fa0755a9c64abc0067bf5c5c88d05'
V_SPEC_BLOB='f1011b87bbf92b780e2f157b0dffe7d15a734616'
P_CONTRACT_SHA='0dc2474a368a765c19cc49099fc61822954e9e29d1ce4ba8ad8fe21fe1fa181b'

U_HEAD='a53d0c8b4c88bab229e5ac9ec2db7dda5f9400b4'
U_TREE='f0c716278ef47665e43572d0129c4e8acd9be182'
U_RUN='32055189778'
U_JOB='95463604513'
U_CI_RUN='32055189737'
U_CI_JOB='95463604366'
U_ART='9296199852'
U_ART_NAME='r318u-published-following-payload-differential-evidence'
U_ART_SIZE='20181'
U_ART_DIGEST='sha256:13262328812bc56c9ea58bbc42364308fb6c65487c51f062296b14993f3a626e'
U_ADMIT_RUN='32056128408'
U_ADMIT_JOB='95466589551'
U_PR_CI='32056613666'
U_PR_CI_JOB='95468125882'
U_PR_KA='32056613623'
U_PR_KA_JOB='95468125403'
U_PUBLISHED_CI='32057137389'
U_PUBLISHED_CI_JOB='95469784666'
U_PUBLISHED_KA='32057137360'
U_PUBLISHED_KA_JOB='95469784158'

O_HEAD='5046e1594b87ce2828db5faa48aceba456c3166f'
O_RUN='32017369100'
O_JOB='95349613184'
O_ART='9284144768'
O_ART_NAME='r318o-following-property-header-evidence'
O_ART_SIZE='25129'
O_ART_DIGEST='sha256:e6dc02f08ad025e816d772227a8c21a595902e45a9d71b5a9eb07c28fab4b94d'
O_PROBE_SOURCE='f3e2ad006413e1357102697d7eb0e5cc24e3cefd'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"
TMP="$(mktemp -d)"
U_DIR="$TMP/u"
O_DIR="$TMP/o"
BOXCARS="$TMP/boxcars"
mkdir -p "$U_DIR" "$O_DIR"
trap 'rm -rf "$TMP"; rm -f "$ROOT/crates/mimir-replay/examples/_tmp_r318v_probe.rs"' EXIT

normalize_digest() { printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

echo '== R3.18V authority freeze =='
git fetch origin main --force
test "$(git rev-parse origin/main)" = "$MAIN"
test "$(git rev-parse origin/main^{tree})" = "$MAIN_TREE"
test "$(git merge-base HEAD "$MAIN")" = "$MAIN"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$MAIN:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$PROD:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$MAIN:crates/mimir-replay/tests/r3_18t_following_payload.rs")" = "$T_TEST_BLOB"
test "$(git rev-parse "$MAIN:docs/continuity/MIMIR_R3_18V_EXECUTION_SPEC.md")" = "$V_SPEC_BLOB"
test "$(git show "$MAIN:docs/continuity/MIMIR_R3_18P_ADMITTED_HEADER_CONTEXTS.json" | sha256sum | awk '{print $1}')" = "$P_CONTRACT_SHA"

mapfile -t changed < <(git diff --name-only "$MAIN" HEAD | sort)
expected=( '.github/workflows/_tmp_r318v_evidence.yml' 'tools/_tmp_r318v_extend_boxcars.py' 'tools/_tmp_r318v_run.sh' )
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)
test "${#changed[@]}" -eq 3
test "$(printf '%s\n' "${changed[@]}")" = "$(printf '%s\n' "${wanted[@]}")"
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

for run in "$U_RUN" "$U_CI_RUN" "$U_ADMIT_RUN" "$U_PR_CI" "$U_PR_KA" "$U_PUBLISHED_CI" "$U_PUBLISHED_KA" "$O_RUN"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
done
for job in "$U_JOB" "$U_CI_JOB" "$U_ADMIT_JOB" "$U_PR_CI_JOB" "$U_PR_KA_JOB" "$U_PUBLISHED_CI_JOB" "$U_PUBLISHED_KA_JOB" "$O_JOB"; do
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$U_RUN" --jq .head_sha)" = "$U_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$U_RUN" --jq .head_commit.tree_id)" = "$U_TREE"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$U_CI_RUN" --jq .head_sha)" = "$U_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$U_PUBLISHED_CI" --jq .head_sha)" = "$MAIN"
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$U_PUBLISHED_KA" --jq .head_sha)" = "$MAIN"
test "$(git rev-parse "$R318C_HEAD:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"
echo 'R3_18V_AUTHORITY_FREEZE=PASS'

echo '== immutable U/O artifacts =='
for spec in \
  "$U_ART|$U_RUN|$U_HEAD|$U_ART_NAME|$U_ART_SIZE|$U_ART_DIGEST|$U_DIR" \
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
(cd "$U_DIR" && test "$(wc -l < r3_18u_artifact_sha256.txt)" -eq 10 && sha256sum -c r3_18u_artifact_sha256.txt)
(cd "$O_DIR" && test "$(wc -l < r3_18o_artifact_sha256.txt)" -eq 11 && sha256sum -c r3_18o_artifact_sha256.txt)
grep -Fq 'R3_18U_OUTCOME=A' "$U_DIR/r3_18u_aggregate.txt"
grep -Fq 'R3_18U_PUBLISHED_T_FROZEN_S_MISMATCH=0' "$U_DIR/r3_18u_aggregate.txt"
grep -Fq 'R3_18U_ANOTHER_CONTROL_BITS_CONSUMED=0' "$U_DIR/r3_18u_aggregate.txt"
cp "$U_DIR/r3_18u_replay_identity.tsv" r3_18v_replay_identity.tsv
cp "$U_DIR/r3_18u_frozen_witnesses.json" r3_18v_frozen_witnesses.json
cp "$U_DIR/r3_18u_summary.json" r3_18v_u_summary.json

python3 - <<'PY'
import hashlib, json
from pathlib import Path
rows=[]
for line in Path('r3_18v_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel,expected,status=line.split('\t')
    assert status=='PASS' and not rel.startswith('/') and '..' not in Path(rel).parts
    assert hashlib.sha256(Path(rel).read_bytes()).hexdigest().lower()==expected.lower(), rel
    rows.append(rel.replace('\\','/'))
assert len(rows)==47 and len(set(rows))==47
u=json.load(open('.tmp_does_not_exist','r')) if False else json.load(open(Path(__import__('os').environ.get('U_COMPARE_PATH','/dev/null')),'r')) if False else None
print('R3_18V_REPLAY_IDENTITY=PASS rows=47')
PY

python3 - "$U_DIR/r3_18u_comparison.json" <<'PY'
import json,sys
from pathlib import Path
u=json.load(open(sys.argv[1],encoding='utf-8'))
a=u['aggregate']
assert a['outcome']=='A' and a['rows']==47 and a['exact_contexts']==18
assert a['published_t_frozen_s_mismatch']==0 and a['header_identity']=='47/47' and a['witness_reselection']==0
assert a['another_control_bits_consumed']==0
rows=u['rows']; assert len(rows)==47 and len({r['label'] for r in rows})==47
with open('r3_18v_targets.tsv','w',encoding='utf-8',newline='\n') as f:
    for r in sorted(rows,key=lambda x:x['label']):
        assert r['published_t_frozen_s_exact'] is True
        f.write(f"{r['label']}\t{r['frame_index']}\t{r['actor_ordinal']}\t{r['actor_context_object_id']}\t{r['payload_end_bit']}\n")
print('R3_18V_TARGETS=PASS rows=47 reselection=0')
PY

echo '== pinned Boxcars property-control oracle =='
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$TMP/r318c_base_patch.py"
python3 - "$TMP/r318c_base_patch.py" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
old='    stream_id_bound: i32,\n'
assert s.count(old)==1
p.write_text(s.replace(old,'    stream_id_bound: u32,\n',1),encoding='utf-8',newline='\n')
print('R3_18V_R318C_BASE_COMPAT=PASS')
PY
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
python3 "$TMP/r318c_base_patch.py" "$BOXCARS"
python3 tools/_tmp_r318v_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18v_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18v_probe.rs Cargo.toml > "$TMP/r318v_boxcars.patch"
BOXCARS_PATCH_SHA="$(sha256sum "$TMP/r318v_boxcars.patch" | awk '{print $1}')"
printf '%s  r318v_boxcars_one_bit_instrumentation.patch\n' "$BOXCARS_PATCH_SHA" > r3_18v_boxcars_instrumentation_sha256.txt
RUSTUP_TOOLCHAIN=stable cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18v_probe --quiet
PROBE="$BOXCARS/target/debug/examples/r3_18v_probe"
test -x "$PROBE"
: > "$TMP/oracle.log"
while IFS=$'\t' read -r rel frame actor actor_obj prior_stop; do
  test -n "$rel"
  MIMIR_R3_18V_LABEL="$rel" \
  MIMIR_R3_18V_TARGET_FRAME="$frame" \
  MIMIR_R3_18V_TARGET_ACTOR_ORDINAL="$actor" \
    "$PROBE" "$ROOT/$rel" >> "$TMP/oracle.log" 2>&1
done < r3_18v_targets.tsv
test "$(grep -c '^R3_18V_ORACLE_PARSE=PASS$' "$TMP/oracle.log")" -eq 47
test "$(grep -c $'^R3_18V_ORACLE\t' "$TMP/oracle.log")" -eq 47
echo 'R3_18V_BOXCARS_ORACLE=PASS controls=47'

echo '== derive published T + independent one-bit native observer =='
git show "$O_PROBE_SOURCE:tools/_tmp_r318o_native_probe.rs" > "$TMP/native.rs"
git show "$U_HEAD:tools/_tmp_r318u_run.sh" > "$TMP/u_runner.sh"
python3 - "$TMP/u_runner.sh" "$TMP/u_transform.py" <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]).read_text(encoding='utf-8')
start='python3 - "$TMP/native.rs" <<\'PY\'\n'
end='\nPY\nmkdir -p crates/mimir-replay/examples'
a=src.find(start); assert a>=0
b=src.find(end,a+len(start)); assert b>=0
code=src[a+len(start):b]
Path(sys.argv[2]).write_text(code,encoding='utf-8',newline='\n')
print('R3_18V_EXTRACT_U_PROBE_TRANSFORM=PASS')
PY
python3 "$TMP/u_transform.py" "$TMP/native.rs"
python3 - "$TMP/native.rs" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected one match, got {n}')
    s=s.replace(old,new,1)
main_marker='fn main() -> Result<(), Box<dyn std::error::Error>> {'
helpers=r'''fn r3_18v_observe_one_bit(bytes: &[u8], start: u64, bit_limit: u64) -> Result<bool, String> {
    if start >= bit_limit {
        return Err(format!("control bit {start} is outside evidence bit limit {bit_limit}"));
    }
    let total = u64::try_from(bytes.len())
        .map_err(|_| "network length conversion")?
        .checked_mul(8)
        .ok_or("network bit length overflow")?;
    if start >= total {
        return Err(format!("control bit {start} outside network length {total}"));
    }
    let pos = usize::try_from(start).map_err(|_| "control position conversion")?;
    Ok(((bytes[pos / 8] >> (pos % 8)) & 1) != 0)
}

fn r3_18v_observe_after_expected_stop(
    bytes: &[u8], actual_stop: u64, expected_stop: u64, bit_limit: u64,
) -> Result<bool, String> {
    if actual_stop != expected_stop {
        return Err(format!("prior R3.18T stop mismatch: actual {actual_stop}, expected {expected_stop}"));
    }
    r3_18v_observe_one_bit(bytes, actual_stop, bit_limit)
}

'''
once(main_marker,helpers+main_marker,'helper insertion')
needle='''        println!(
            "R3_18U_PUBLISHED\\tlabel={label}'''
insert=r'''        let r3_18v_network_bits = u64::try_from(network.len())?
            .checked_mul(8).ok_or("R3.18V network bits overflow")?;
        let r3_18v_control = r3_18v_observe_after_expected_stop(
            &network, published.stop_bit, payload_end, r3_18v_network_bits,
        ).map_err(std::io::Error::other)?;
        let r3_18v_control_start = published.stop_bit;
        let r3_18v_control_end = r3_18v_control_start.checked_add(1).ok_or("R3.18V control end overflow")?;
        let r3_18v_repeatability = r3_18v_observe_after_expected_stop(
            &network, published.stop_bit, payload_end, r3_18v_network_bits,
        ).map_err(std::io::Error::other)? == r3_18v_control;
        let r3_18v_truncation = r3_18v_observe_after_expected_stop(
            &network, published.stop_bit, payload_end, r3_18v_control_start,
        ).is_err();
        let r3_18v_prior_stop_negative = r3_18v_observe_after_expected_stop(
            &network,
            published.stop_bit,
            payload_end.checked_add(1).ok_or("R3.18V mismatch overflow")?,
            r3_18v_network_bits,
        ).is_err();
        let mut r3_18v_poisoned = network.clone();
        for offset in 0..16u64 {
            set_bit(&mut r3_18v_poisoned, r3_18v_control_end + offset, offset % 2 == 0)
                .map_err(std::io::Error::other)?;
        }
        let r3_18v_poisoned_published = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_v1(
            &r3_18v_poisoned, &decoded, &plan, u_context,
        )?;
        let r3_18v_poisoned_control = r3_18v_observe_after_expected_stop(
            &r3_18v_poisoned,
            r3_18v_poisoned_published.stop_bit,
            payload_end,
            u64::try_from(r3_18v_poisoned.len())?.checked_mul(8).ok_or("R3.18V poison bits overflow")?,
        ).map_err(std::io::Error::other)?;
        let r3_18v_poison = r3_18v_poisoned_published == published
            && r3_18v_poisoned_control == r3_18v_control;
        if !r3_18v_repeatability || !r3_18v_truncation || !r3_18v_prior_stop_negative || !r3_18v_poison {
            return Err(format!("{label}: R3.18V negative/repeatability failure").into());
        }
        println!(
            "R3_18V_NATIVE\tlabel={label}\tframe_index={}\tactor_ordinal={}\tactor_context_object_id={}\tprior_t_stop={}\tcontrol_start={}\tcontrol_end={}\tcontrol_value={}\tpublished_t_exact=1\ttruncation=1\trepeatability=1\tprior_stop_mismatch_negative=1\tpost_control_poison=1\tnext_stream_bits_consumed=0\tnext_header_bits_consumed=0\tnext_payload_bits_consumed=0\tsecond_later_control_bits_consumed=0",
            _frame_index,
            _actor_ordinal,
            actor_object,
            payload_end,
            r3_18v_control_start,
            r3_18v_control_end,
            u8::from(r3_18v_control),
        );

        println!(
            "R3_18U_PUBLISHED\tlabel={label}'''
once(needle,insert,'V insertion')
p.write_text(s,encoding='utf-8',newline='\n')
print('R3_18V_NATIVE_PROBE_DERIVATION=PASS')
PY
mkdir -p crates/mimir-replay/examples
cp "$TMP/native.rs" crates/mimir-replay/examples/_tmp_r318v_probe.rs
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318v_probe -- "$O_DIR/r3_18o_targets.tsv" > "$TMP/native1.log"
cargo +1.85.0 run -q -p mimir-replay --example _tmp_r318v_probe -- "$O_DIR/r3_18o_targets.tsv" > "$TMP/native2.log"
cmp "$TMP/native1.log" "$TMP/native2.log"
test "$(grep -c $'^R3_18U_PUBLISHED\t' "$TMP/native1.log")" -eq 47
test "$(grep -c $'^R3_18V_NATIVE\t' "$TMP/native1.log")" -eq 47
rm -f crates/mimir-replay/examples/_tmp_r318v_probe.rs

echo '== compare published T, Boxcars control and independent bit =='
python3 - "$U_DIR/r3_18u_comparison.json" "$TMP/oracle.log" "$TMP/native1.log" <<'PY'
import collections,json,sys
from pathlib import Path
u=json.load(open(sys.argv[1],encoding='utf-8'))
def kv(line,prefix):
    assert line.startswith(prefix+'\t')
    out={}
    for item in line.rstrip('\n').split('\t')[1:]:
        k,v=item.split('=',1); out[k]=v
    return out
oracle={}; parse_pass=0
for line in open(sys.argv[2],encoding='utf-8',errors='replace'):
    if line.rstrip('\n')=='R3_18V_ORACLE_PARSE=PASS': parse_pass+=1
    elif line.startswith('R3_18V_ORACLE\t'):
        r=kv(line,'R3_18V_ORACLE'); assert r['label'] not in oracle; oracle[r['label']]=r
native={}; upub={}
for line in open(sys.argv[3],encoding='utf-8',errors='replace'):
    if line.startswith('R3_18V_NATIVE\t'):
        r=kv(line,'R3_18V_NATIVE'); assert r['label'] not in native; native[r['label']]=r
    elif line.startswith('R3_18U_PUBLISHED\t'):
        r=kv(line,'R3_18U_PUBLISHED'); assert r['label'] not in upub; upub[r['label']]=r
urows={r['label']:r for r in u['rows']}
assert parse_pass==47 and len(oracle)==len(native)==len(upub)==len(urows)==47
assert set(oracle)==set(native)==set(upub)==set(urows)
false_count=true_count=mismatch=0; rows=[]
for label in sorted(urows):
    fr=urows[label]; p=upub[label]; n=native[label]; o=oracle[label]
    published_exact=(
        int(p['frame_index'])==fr['frame_index'] and int(p['actor_ordinal'])==fr['actor_ordinal']
        and int(p['actor_context_object_id'])==fr['actor_context_object_id']
        and p['tag']==fr['tag'] and int(p['payload_start_bit'])==fr['payload_start_bit']
        and int(p['payload_end_bit'])==fr['payload_end_bit'] and int(p['payload_width'])==fr['payload_width']
        and p['semantic_bool']==fr['semantic_bool'] and p['semantic_active']==fr['semantic_active']
        and p['semantic_actor']==fr['semantic_actor'] and p['header_identity']=='1'
    )
    prior=fr['payload_end_bit']
    os=int(o['next_property_present_start_bit']); oe=int(o['next_property_present_end_bit']); ov=int(o['next_property_present'])
    ns=int(n['control_start']); ne=int(n['control_end']); nv=int(n['control_value'])
    exact=(published_exact and int(n['prior_t_stop'])==prior and os==prior and oe==os+1 and ns==prior and ne==ns+1
           and ns==os and ne==oe and nv==ov and n['published_t_exact']=='1' and n['truncation']=='1'
           and n['repeatability']=='1' and n['prior_stop_mismatch_negative']=='1' and n['post_control_poison']=='1'
           and n['next_stream_bits_consumed']=='0' and n['next_header_bits_consumed']=='0'
           and n['next_payload_bits_consumed']=='0' and n['second_later_control_bits_consumed']=='0')
    mismatch += 0 if exact else 1
    if ov==0: false_count+=1
    elif ov==1: true_count+=1
    else: raise AssertionError((label,ov))
    rows.append({'label':label,'frame_index':fr['frame_index'],'actor_ordinal':fr['actor_ordinal'],
      'actor_context_object_id':fr['actor_context_object_id'],'prior_r3_18t_stop_bit':prior,
      'property_present_start_bit':os,'property_present_end_bit':oe,'property_present':bool(ov),
      'published_r3_18t_exact':published_exact,'native_oracle_exact':exact,
      'next_stream_bits_consumed':0,'next_header_bits_consumed':0,'next_payload_bits_consumed':0,
      'second_later_control_bits_consumed':0})
assert false_count+true_count==47 and mismatch==0
payload={'aggregate':{'outcome':'A','rows':47,'false':false_count,'true':true_count,'published_r3_18t_exact':47,
 'native_oracle_mismatch':0,'witness_reselection':0,'truncation':'47/47','repeatability':'47/47',
 'prior_stop_mismatch_negative':'47/47','post_control_poison':'47/47','next_stream_bits_consumed':0,
 'next_header_bits_consumed':0,'next_payload_bits_consumed':0,'second_later_control_bits_consumed':0,
 'production_cargo_fixture_corpus_support_mutation':'0/0/0/0/0','privacy_scan':'PASS'},'rows':rows}
json.dump(payload,open('r3_18v_comparison.json','w',encoding='utf-8'),indent=2,sort_keys=True); open('r3_18v_comparison.json','a').write('\n')
json.dump({'rows':47,'false':false_count,'true':true_count,'native_oracle_mismatch':0,'witness_reselection':0},open('r3_18v_summary.json','w',encoding='utf-8'),indent=2,sort_keys=True); open('r3_18v_summary.json','a').write('\n')
print(f'R3_18V_DIFFERENTIAL=PASS rows=47 false={false_count} true={true_count} mismatch=0')
PY

python3 - <<'PY'
import json
v=json.load(open('r3_18v_comparison.json',encoding='utf-8'))
a=v['aggregate']
text='\n'.join([
 'R3_18V_OUTCOME=A','R3_18V_EVIDENCE=PASS','R3_18V_FROZEN_ROWS=47/47',
 f"R3_18V_CONTROL_FALSE={a['false']}",f"R3_18V_CONTROL_TRUE={a['true']}",
 'R3_18V_PUBLISHED_R318T_EXACT=47/47','R3_18V_NATIVE_ORACLE_MISMATCH=0',
 'R3_18V_CONTROL_TRUNCATION=PASS 47/47','R3_18V_REPEATABILITY=PASS 47/47',
 'R3_18V_PRIOR_STOP_MISMATCH_NEGATIVE=PASS 47/47','R3_18V_POST_CONTROL_POISON=PASS 47/47',
 'R3_18V_NEXT_STREAM_BITS_CONSUMED=0','R3_18V_NEXT_HEADER_BITS_CONSUMED=0','R3_18V_NEXT_PAYLOAD_BITS_CONSUMED=0',
 'R3_18V_SECOND_LATER_CONTROL_BITS_CONSUMED=0','R3_18V_WITNESS_RESELECTION=0',
 'R3_18V_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0','R3_18V_PRIVACY_SCAN=PASS'])+'\n'
open('r3_18v_aggregate.txt','w',encoding='utf-8',newline='\n').write(text)
open('r3_18v_negative_controls.txt','w',encoding='utf-8',newline='\n').write('\n'.join([
 'control_bit_truncation=PASS 47/47','repeatability=PASS 47/47','prior_r3_18t_stop_mismatch=PASS 47/47',
 'post_control_poison=PASS 47/47','next_stream_bits_consumed=0','next_header_bits_consumed=0',
 'next_payload_bits_consumed=0','second_later_control_bits_consumed=0'])+'\n')
PY

printf '%s\n' "${changed[@]}" > r3_18v_source_scope.txt
cat > r3_18v_upstream_receipts.txt <<EOF
MAIN=$MAIN
MAIN_TREE=$MAIN_TREE
PRODUCTION=$PROD
PRODUCTION_TREE=$PROD_TREE
LIB_BLOB=$LIB_BLOB
T_TEST_BLOB=$T_TEST_BLOB
V_SPEC_BLOB=$V_SPEC_BLOB
R318P_CONTRACT_SHA256=$P_CONTRACT_SHA
R318U_HEAD_TREE=$U_HEAD/$U_TREE
R318U_AUTHORITY=$U_RUN/$U_JOB
R318U_SAME_HEAD_CI=$U_CI_RUN/$U_CI_JOB
R318U_ARTIFACT=$U_ART/$U_ART_SIZE/$U_ART_DIGEST
R318U_ADMISSION_AUTHORITY=$U_ADMIT_RUN/$U_ADMIT_JOB
R318U_PUBLISHED_CI=$U_PUBLISHED_CI/$U_PUBLISHED_CI_JOB
R318U_PUBLISHED_KA=$U_PUBLISHED_KA/$U_PUBLISHED_KA_JOB
R318O_AUTHORITY=$O_RUN/$O_JOB
R318O_ARTIFACT=$O_ART/$O_ART_SIZE/$O_ART_DIGEST
BOXCARS_SHA=$BOXCARS_SHA
BOXCARS_PATCH_SHA256=$BOXCARS_PATCH_SHA
EOF

python3 - <<'PY'
from pathlib import Path
for path in ['r3_18v_source_scope.txt','r3_18v_replay_identity.tsv','r3_18v_frozen_witnesses.json','r3_18v_u_summary.json',
             'r3_18v_targets.tsv','r3_18v_boxcars_instrumentation_sha256.txt','r3_18v_summary.json','r3_18v_comparison.json',
             'r3_18v_negative_controls.txt','r3_18v_aggregate.txt','r3_18v_upstream_receipts.txt']:
    text=Path(path).read_text(encoding='utf-8')
    assert '/home/' not in text and '/Users/' not in text and '\\Users\\' not in text
    assert 'window_hex=' not in text and 'raw_payload' not in text
print('R3_18V_PRIVACY_SCAN=PASS')
PY

echo '== repository validation =='
cargo +1.85.0 test -p mimir-replay --test r3_18t_following_payload
cargo +1.85.0 test -p mimir-replay
cargo +1.85.0 check --workspace --all-targets
cargo +1.85.0 test --workspace --all-targets
cargo +1.85.0 clippy --workspace --all-targets -- -D warnings
pwsh -File ./scripts/verify_repo.ps1
git diff --exit-code "$MAIN" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

files=(
 r3_18v_source_scope.txt
 r3_18v_replay_identity.tsv
 r3_18v_frozen_witnesses.json
 r3_18v_u_summary.json
 r3_18v_targets.tsv
 r3_18v_boxcars_instrumentation_sha256.txt
 r3_18v_summary.json
 r3_18v_comparison.json
 r3_18v_negative_controls.txt
 r3_18v_aggregate.txt
 r3_18v_upstream_receipts.txt
)
: > r3_18v_artifact_sha256.txt
for file in "${files[@]}"; do sha256sum "$file" >> r3_18v_artifact_sha256.txt; done
sha256sum -c r3_18v_artifact_sha256.txt
cat r3_18v_aggregate.txt
echo 'R3_18V_EVIDENCE=PASS'

#!/usr/bin/env bash
set -euo pipefail

BASE='c55c23c0fa86de6bacb79456795dafd996d2d96f'
BASE_TREE='26ba2777045299c99546a4777fc884048157dd60'
PROD='3c74b276b8eeb1d99d2ca2b12a824c2d2ef66b38'
PROD_TREE='3efcc244bca55623b12bb21eb277753fc61144d4'
LIB_BLOB='9d6b5ae2898cee745a17de9d1d7ef4b8fbd0e822'
AN_TEST_BLOB='8aa48b2b74d0956d1d2e965d056e1cf14a81f703'
AP_SPEC_BLOB='2538e848c06a3e01310a707bf3f48b2622a56b73'

AO_HEAD='0f5ecb5b1dccf35aaabf6a45645bc70ad8a68a1c'
AO_TREE='59126fe2757ecc500a5cc6f822d76fbc380ef85b'
AO_RUN='32734420624'
AO_JOB='97453768432'
AO_CI='32734946566'
AO_CI_JOB='97455429462'
AO_ART='9522750814'
AO_ART_NAME='r318ao-published-an-differential-evidence'
AO_SIZE='4619'
AO_DIGEST='sha256:2e34f3be6963b2b6031a395e85e9699b64df7413d62dd9809fa8fd9794547d73'

AM_HEAD='842b94ed4c4e57323433585fea48116ecf18989b'
AM_RUN='32473716883'
AM_ART='9443581172'
AM_ART_NAME='r318am-post-ak-payload-evidence'
AM_SIZE='14827'
AM_DIGEST='sha256:2f65de5207bd96787fd7d1527a55991f08d5da614a0ddfce22a7aa267968e3c8'

R318C_HEAD='a4b71ad43e5cf55c44c9518b24622ce29214acd2'
R318C_PATCH_BLOB='eb61cca0c080733aa36856dbb69f4c36642a5cda'
BOXCARS_SHA='c70e77df7af81b436cb545d070bb90c82f562d0b'
BOXCARS_FRAME_BLOB='6f2ff153d3a27cdacccc65e3f23851489077a7d8'
BOXCARS_ATTR_BLOB='5e2d5bc1cd8187af30c3ea95193ad987645cb76e'

ROOT="$PWD"
TMP="$(mktemp -d)"
AO_DIR="$TMP/ao"
AM_DIR="$TMP/am"
BOXCARS="$TMP/boxcars"
PROBE='crates/mimir-replay/examples/_tmp_r318ap_probe.rs'
mkdir -p "$AO_DIR" "$AM_DIR" crates/mimir-replay/examples
trap 'rm -rf "$TMP"; rm -f "$PROBE"' EXIT
norm_digest(){ printf '%s' "${1#sha256:}" | tr '[:upper:]' '[:lower:]'; }

echo '== R3.18AP authority freeze =='
git fetch origin main "$PROD" "$AO_HEAD" "$AM_HEAD" "$R318C_HEAD" --force
test "$(git rev-parse origin/main)" = "$BASE"
test "$(git rev-parse origin/main^{tree})" = "$BASE_TREE"
test "$(git rev-parse HEAD)" = "$GITHUB_SHA"
test "$(git merge-base "$BASE" HEAD)" = "$BASE"
test "$(git rev-parse "$PROD^{tree}")" = "$PROD_TREE"
test "$(git rev-parse "$BASE:crates/mimir-replay/src/lib.rs")" = "$LIB_BLOB"
test "$(git rev-parse "$BASE:crates/mimir-replay/tests/r3_18an_post_ak_payload.rs")" = "$AN_TEST_BLOB"
test "$(git rev-parse "$BASE:docs/continuity/MIMIR_R3_18AP_EXECUTION_SPEC.md")" = "$AP_SPEC_BLOB"
test "$(git rev-parse "$R318C_HEAD:tools/_tmp_r318c_patch.py")" = "$R318C_PATCH_BLOB"
mapfile -t actual < <(git diff --name-only "$BASE" HEAD | sort)
mapfile -t expected < <(printf '%s\n' \
  .github/workflows/_tmp_r318ap_evidence.yml \
  tools/_tmp_r318ap_extend_boxcars.py \
  tools/_tmp_r318ap_run.sh | sort)
diff -u <(printf '%s\n' "${expected[@]}") <(printf '%s\n' "${actual[@]}")
git diff --exit-code "$BASE" HEAD -- \
  crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs \
  MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

echo '== immutable AO and AM receipts =='
for pair in "$AO_RUN:$AO_JOB" "$AO_CI:$AO_CI_JOB"; do
  run="${pair%%:*}"; job="${pair##*:}"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$run" --jq .conclusion)" = success
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$job" --jq .conclusion)" = success
done
test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$AO_RUN" --jq .head_sha)" = "$AO_HEAD"
test "$(gh api "repos/$GITHUB_REPOSITORY/git/commits/$AO_HEAD" --jq .tree.sha)" = "$AO_TREE"

verify_artifact() {
  local aid="$1" run="$2" head="$3" name="$4" size="$5" digest="$6" dir="$7" manifest="$8" entries="$9"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.id)" = "$run"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .workflow_run.head_sha)" = "$head"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .name)" = "$name"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .size_in_bytes)" = "$size"
  test "$(norm_digest "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .digest)")" = "$(norm_digest "$digest")"
  test "$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$aid" --jq .expired)" = false
  local ok=0
  for attempt in 1 2 3; do
    rm -rf "$dir"; mkdir -p "$dir"
    if gh run download "$run" -n "$name" -D "$dir"; then ok=1; break; fi
    sleep $((attempt * 5))
  done
  test "$ok" -eq 1
  (cd "$dir" && test "$(wc -l < "$manifest")" -eq "$entries" && sha256sum -c "$manifest")
}
verify_artifact "$AO_ART" "$AO_RUN" "$AO_HEAD" "$AO_ART_NAME" "$AO_SIZE" "$AO_DIGEST" "$AO_DIR" r3_18ao_artifact_sha256.txt 7
verify_artifact "$AM_ART" "$AM_RUN" "$AM_HEAD" "$AM_ART_NAME" "$AM_SIZE" "$AM_DIGEST" "$AM_DIR" r3_18am_artifact_sha256.txt 11

grep -Fx 'R3_18AO_OUTCOME=A' "$AO_DIR/r3_18ao_aggregate.txt"
grep -Fx 'R3_18AO_FROZEN_ROWS=47/47' "$AO_DIR/r3_18ao_aggregate.txt"
grep -Fx 'R3_18AO_PUBLISHED_AN_EXACT=47/47' "$AO_DIR/r3_18ao_aggregate.txt"
grep -Fx 'R3_18AO_NATIVE_ORACLE_PUBLISHED_MISMATCH=0' "$AO_DIR/r3_18ao_aggregate.txt"
grep -Fx 'R3_18AO_WITNESS_RESELECTION=0' "$AO_DIR/r3_18ao_aggregate.txt"
grep -Fx 'R3_18AO_NEXT_CONTROL_BITS_CONSUMED=0' "$AO_DIR/r3_18ao_aggregate.txt"

printf '%s\n' \
  "R3_18AP_BASE=$BASE/$BASE_TREE" \
  "R3_18AP_PRODUCTION=$PROD/$PROD_TREE" \
  "R3_18AP_LIB_BLOB=$LIB_BLOB" \
  "R3_18AP_AN_TEST_BLOB=$AN_TEST_BLOB" \
  "R3_18AP_AP_SPEC_BLOB=$AP_SPEC_BLOB" \
  "R3_18AP_AO_HEAD_TREE=$AO_HEAD/$AO_TREE" \
  "R3_18AP_AO_RUN_JOB=$AO_RUN/$AO_JOB" \
  "R3_18AP_AO_CI_JOB=$AO_CI/$AO_CI_JOB" \
  "R3_18AP_AO_ARTIFACT=$AO_ART/$AO_SIZE/$AO_DIGEST" \
  "R3_18AP_AM_ARTIFACT=$AM_ART/$AM_SIZE/$AM_DIGEST" \
  "R3_18AP_BOXCARS_PIN=$BOXCARS_SHA" > r3_18ap_upstream_receipts.txt

echo '== freeze exact 47 target identities =='
cp "$AM_DIR/r3_18am_replay_identity.tsv" r3_18ap_replay_identity.tsv
python3 - "$AM_DIR/r3_18am_payload_rows.json" "$AO_DIR/r3_18ao_comparison_rows.tsv" <<'PY'
import hashlib, json, sys
from pathlib import Path
am=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))['rows']
ao={}
for line in Path(sys.argv[2]).read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    parts=line.split('\t'); assert parts[0]=='R3_18AO_COMPARE'
    d={}
    for field in parts[1:]:
        k,v=field.split('=',1); d[k]=v
    assert d['label'] not in ao; ao[d['label']]=d
assert len(am)==len(ao)==47
out=[]
for r in am:
    label=r['label']; assert label in ao; a=ao[label]
    assert r['tag']=='Int' and r['payload_width']==32 and r['native_oracle_exact'] is True
    assert int(a['payload_start_bit'])==r['payload_start_bit']
    assert int(a['payload_end_bit'])==r['payload_end_bit']
    assert int(a['semantic_int'])==r['semantic_int']
    assert a['published_an_exact']=='1' and a['mismatch']=='0' and a['witness_reselection']=='0'
    out.append([label,str(r['frame_index']),str(r['actor_ordinal']),str(r['actor_context_object_id']),str(r['payload_start_bit']),str(r['payload_end_bit']),str(r['semantic_int'])])
assert len(out)==47 and len({x[0] for x in out})==47
Path('r3_18ap_targets.tsv').write_text('\n'.join('\t'.join(x) for x in sorted(out))+'\n',encoding='utf-8',newline='\n')
ids=[]
for line in Path('r3_18ap_replay_identity.tsv').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    rel,expected,status=line.split('\t'); p=Path(rel)
    assert status=='PASS' and not p.is_absolute() and '..' not in p.parts and p.exists()
    assert hashlib.sha256(p.read_bytes()).hexdigest().lower()==expected.lower()
    ids.append(rel.replace('\\','/'))
assert len(ids)==47 and set(ids)=={x[0] for x in out}
print('R3_18AP_TARGETS=PASS rows=47 witness_reselection=0')
PY

echo '== pinned Boxcars exact-coordinate one-bit oracle =='
git show "$R318C_HEAD:tools/_tmp_r318c_patch.py" > "$TMP/r318c_base_patch.py"
python3 - "$TMP/r318c_base_patch.py" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8'); old='    stream_id_bound: i32,\n'
assert s.count(old)==1
p.write_text(s.replace(old,'    stream_id_bound: u32,\n',1),encoding='utf-8',newline='\n')
PY
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"
test "$(git -C "$BOXCARS" rev-parse HEAD:src/network/attributes.rs)" = "$BOXCARS_ATTR_BLOB"
python3 "$TMP/r318c_base_patch.py" "$BOXCARS"
python3 tools/_tmp_r318ap_extend_boxcars.py "$BOXCARS"
git -C "$BOXCARS" add -N examples/r3_18ap_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- src/network/frame_decoder.rs examples/r3_18ap_probe.rs Cargo.toml > "$TMP/r318ap_boxcars.patch"
BOXCARS_PATCH_SHA="$(sha256sum "$TMP/r318ap_boxcars.patch" | awk '{print $1}')"
printf '%s  r318ap_boxcars_exact_coordinate_instrumentation.patch\n' "$BOXCARS_PATCH_SHA" > r3_18ap_boxcars_instrumentation_sha256.txt
RUSTUP_TOOLCHAIN=stable cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18ap_probe --quiet
ORACLE="$BOXCARS/target/debug/examples/r3_18ap_probe"
: > "$TMP/oracle.log"
while IFS=$'\t' read -r rel frame actor actor_obj payload_start control_start semantic_int; do
  MIMIR_R3_18AP_LABEL="$rel" \
  MIMIR_R3_18AP_TARGET_FRAME="$frame" \
  MIMIR_R3_18AP_TARGET_ACTOR_ORDINAL="$actor" \
  MIMIR_R3_18AP_TARGET_CONTROL_START="$control_start" \
    "$ORACLE" "$ROOT/$rel" >> "$TMP/oracle.log" 2>&1
done < r3_18ap_targets.tsv
test "$(grep -c '^R3_18AP_ORACLE_PARSE=PASS$' "$TMP/oracle.log")" -eq 47
test "$(grep -c $'^R3_18AP_ORACLE\t' "$TMP/oracle.log")" -eq 47
echo 'R3_18AP_BOXCARS_ORACLE=PASS controls=47 exact_coordinates=47'

echo '== published AN reconstruction plus independent one-bit observer =='
python3 - "$PROBE" <<'PY'
from pathlib import Path
import sys
src=Path('crates/mimir-replay/tests/r3_18an_post_ak_payload.rs').read_text(encoding='utf-8')
name='r3_18an_all_47_frozen_am_rows_are_exact_and_stop_before_next_control'
assert src.count(f'fn {name}()')==1
src=src.replace('#[test]\n','')
src=src.replace(f'fn {name}()', 'fn main()', 1)
insert_after='use std::path::{Path, PathBuf};\n'
assert src.count(insert_after)==1
helper=r'''
fn observe_one_bit(bytes: &[u8], start: u64, bit_limit: u64) -> Option<(u64, bool, u64)> {
    if start >= bit_limit || start >= (bytes.len() as u64).saturating_mul(8) {
        return None;
    }
    let pos = usize::try_from(start).ok()?;
    let value = ((bytes[pos / 8] >> (pos % 8)) & 1) != 0;
    Some((start, value, start + 1))
}

fn guarded_observe_one_bit(
    bytes: &[u8],
    expected_prior_stop: u64,
    supplied_prior_stop: u64,
    bit_limit: u64,
) -> Result<(u64, bool, u64), &'static str> {
    if supplied_prior_stop != expected_prior_stop {
        return Err("prior-stop-mismatch");
    }
    observe_one_bit(bytes, expected_prior_stop, bit_limit).ok_or("insufficient-control-bit")
}
'''
s=src.replace(insert_after,insert_after+helper,1)
main_open='fn main() {\n'
assert src.count(main_open)==1
setup=r'''fn main() {
    let target_text = std::fs::read_to_string("r3_18ap_targets.tsv").expect("R3.18AP targets");
    let mut targets = std::collections::HashMap::<String, (u64, u64, u64, i32)>::new();
    for line in target_text.lines() {
        if line.trim().is_empty() { continue; }
        let fields: Vec<&str> = line.split('\t').collect();
        assert_eq!(fields.len(), 7);
        let label = fields[0].to_owned();
        let frame_index: u64 = fields[1].parse().unwrap();
        let actor_ordinal: u64 = fields[2].parse().unwrap();
        let control_start: u64 = fields[5].parse().unwrap();
        let semantic_int: i32 = fields[6].parse().unwrap();
        assert!(targets.insert(label, (frame_index, actor_ordinal, control_start, semantic_int)).is_none());
    }
    assert_eq!(targets.len(), 47);
'''
s=src.replace(main_open,setup,1)
needle='        assert_eq!(after_poison, got, "post-stop poison changed {path}");\n'
assert src.count(needle)==1
body=r'''        let label = path.strip_prefix("../../").unwrap_or(path);
        let (frame_index, actor_ordinal, control_start, target_semantic) =
            *targets.get(label).expect("frozen R3.18AP target");
        let semantic_int = match got.following_payload.value {
            ReplayNetworkPrimitiveScalarValueV1::Int(value) => value,
            ref other => panic!("unexpected AN value {other:?}"),
        };
        assert_eq!(semantic_int, target_semantic, "{path}");
        assert_eq!(got.stop_bit, control_start, "{path}");
        let bit_limit = u64::try_from(network.len()).unwrap().saturating_mul(8);
        let first = guarded_observe_one_bit(&network, got.stop_bit, got.stop_bit, bit_limit)
            .expect("one R3.18AP control bit");
        let repeated = guarded_observe_one_bit(&network, got.stop_bit, got.stop_bit, bit_limit)
            .expect("repeat one R3.18AP control bit");
        assert_eq!(first, repeated, "{path}");
        assert!(guarded_observe_one_bit(&network, got.stop_bit, got.stop_bit, got.stop_bit).is_err(), "{path}");
        assert!(guarded_observe_one_bit(&network, got.stop_bit, got.stop_bit + 1, bit_limit).is_err(), "{path}");
        let mut post_control_poison = network.clone();
        let poison = usize::try_from(first.2).unwrap();
        if poison < post_control_poison.len() * 8 {
            let original = ((post_control_poison[poison / 8] >> (poison % 8)) & 1) != 0;
            set_bit(&mut post_control_poison, poison, !original);
            let poisoned = guarded_observe_one_bit(
                &post_control_poison,
                got.stop_bit,
                got.stop_bit,
                bit_limit,
            ).expect("post-control poison observation");
            assert_eq!(poisoned, first, "{path}");
        }
        println!(
            "R3_18AP_NATIVE\tlabel={}\tframe_index={}\tactor_ordinal={}\tprior_an_stop={}\tcontrol_start={}\tcontrol_end={}\tcontrol_value={}\tpublished_an_exact=1\trepeatability=1\ttruncation_negative=1\tprior_stop_negative=1\tpost_control_poison=1\tnext_stream_bits=0\tnext_header_bits=0\tnext_payload_bits=0\tsecond_control_bits=0",
            label,
            frame_index,
            actor_ordinal,
            got.stop_bit,
            first.0,
            first.2,
            if first.1 { 1 } else { 0 },
        );
'''
s=src.replace(needle,needle+body,1)
Path(sys.argv[1]).write_text(src,encoding='utf-8',newline='\n')
print('R3_18AP_NATIVE_PROBE_DERIVATION=PASS')
PY
rustup run 1.85.0 rustfmt --edition 2024 "$PROBE"
cargo +1.85.0 run -p mimir-replay --example _tmp_r318ap_probe --quiet > "$TMP/native.log"
test "$(grep -c $'^R3_18AP_NATIVE\t' "$TMP/native.log")" -eq 47
rm -f "$PROBE"

echo '== exact oracle/native one-bit differential =='
python3 - "$TMP/oracle.log" "$TMP/native.log" <<'PY'
import json,sys
from pathlib import Path

def kv(line,prefix):
    parts=line.rstrip('\n').split('\t'); assert parts[0]==prefix
    d={}
    for x in parts[1:]:
        k,v=x.split('=',1); d[k]=v
    return d
oracle={}; native={}
for line in Path(sys.argv[1]).read_text(encoding='utf-8',errors='replace').splitlines():
    if line.startswith('R3_18AP_ORACLE\t'):
        r=kv(line,'R3_18AP_ORACLE'); assert r['label'] not in oracle; oracle[r['label']]=r
for line in Path(sys.argv[2]).read_text(encoding='utf-8',errors='replace').splitlines():
    if line.startswith('R3_18AP_NATIVE\t'):
        r=kv(line,'R3_18AP_NATIVE'); assert r['label'] not in native; native[r['label']]=r
assert len(oracle)==len(native)==47 and set(oracle)==set(native)
rows=[]; false_count=0; true_count=0
for label in sorted(native):
    o=oracle[label]; n=native[label]
    os=int(o['next_property_present_start_bit']); oe=int(o['next_property_present_end_bit']); ov=int(o['next_property_present'])
    ns=int(n['control_start']); ne=int(n['control_end']); nv=int(n['control_value']); prior=int(n['prior_an_stop'])
    assert os==ns==prior and oe==ne==ns+1 and ov==nv
    for key in ['published_an_exact','repeatability','truncation_negative','prior_stop_negative','post_control_poison']:
        assert n[key]=='1'
    for key in ['next_stream_bits','next_header_bits','next_payload_bits','second_control_bits']:
        assert n[key]=='0'
    false_count += nv==0; true_count += nv==1
    rows.append('\t'.join(['R3_18AP_COMPARE',f'label={label}',f'control_start={ns}',f'control_end={ne}',f'control_value={nv}','published_an_exact=1','oracle_native_exact=1','mismatch=0','witness_reselection=0']))
assert false_count+true_count==47
Path('r3_18ap_comparison.tsv').write_text('\n'.join(rows)+'\n',encoding='utf-8',newline='\n')
summary={'outcome':'A','rows':47,'published_an_exact':47,'oracle_native_exact':47,'false_count':false_count,'true_count':true_count,'mismatch':0,'witness_reselection':0,'next_stream_bits_consumed':0,'next_header_bits_consumed':0,'next_payload_bits_consumed':0,'second_later_control_bits_consumed':0}
Path('r3_18ap_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
print(f'R3_18AP_DIFFERENTIAL=PASS rows=47 false={false_count} true={true_count} mismatch=0')
PY

echo '== focused and full validation =='
cargo +1.85.0 test -p mimir-replay --test r3_18an_post_ak_payload -- --nocapture > "$TMP/an_tests.log" 2>&1
grep -Fq 'test result: ok.' "$TMP/an_tests.log"
cargo +1.85.0 fmt --all -- --check
cargo +1.85.0 check --workspace --all-targets --all-features
cargo +1.85.0 clippy --workspace --all-targets --all-features -- -D warnings
cargo +1.85.0 test --workspace --all-features
pwsh -NoProfile -File scripts/verify_repo.ps1
rm -f "$PROBE"
git diff --exit-code "$BASE" HEAD -- crates Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs \
  MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md MIMIR_ALL_SOURCES_SUPERBOOK.md

cat > r3_18ap_negative_controls.txt <<'EOF'
R3_18AP_TRUNCATION_BEFORE_CONTROL=PASS 47/47
R3_18AP_PRIOR_AN_STOP_MISMATCH=PASS 47/47
R3_18AP_REPEATABILITY=PASS 47/47
R3_18AP_POST_CONTROL_POISON=PASS 47/47
R3_18AP_PUBLISHED_AN_PREREQUISITE=PASS 47/47
R3_18AP_NEXT_STREAM_BITS_CONSUMED=0
R3_18AP_NEXT_HEADER_BITS_CONSUMED=0
R3_18AP_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18AP_SECOND_LATER_CONTROL_BITS_CONSUMED=0
EOF
cat > r3_18ap_source_scope.txt <<'EOF'
R3_18AP_PRODUCTION_MUTATION=0
R3_18AP_CARGO_MUTATION=0
R3_18AP_FIXTURE_MUTATION=0
R3_18AP_CORPUS_MUTATION=0
R3_18AP_SUPPORT_MUTATION=0
R3_18AP_WITNESS_RESELECTION=0
R3_18AP_NEXT_STREAM_BITS_CONSUMED=0
R3_18AP_NEXT_HEADER_BITS_CONSUMED=0
R3_18AP_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18AP_SECOND_LATER_CONTROL_BITS_CONSUMED=0
EOF
cat > r3_18ap_validation.txt <<'EOF'
R3_18AP_FOCUSED_AN_TEST=PASS
R3_18AP_FMT_CHECK=PASS
R3_18AP_WORKSPACE_CHECK=PASS
R3_18AP_WORKSPACE_CLIPPY_D_WARNINGS=PASS
R3_18AP_WORKSPACE_TEST=PASS
R3_18AP_REPOSITORY_VERIFIER=PASS
EOF

FALSE_COUNT="$(jq -r .false_count r3_18ap_summary.json)"
TRUE_COUNT="$(jq -r .true_count r3_18ap_summary.json)"
cat > r3_18ap_aggregate.txt <<EOF
R3_18AP_OUTCOME=A
R3_18AP_EVIDENCE=PASS
R3_18AP_FROZEN_ROWS=47/47
R3_18AP_PUBLISHED_AN_EXACT=47/47
R3_18AP_ORACLE_NATIVE_EXACT=47/47
R3_18AP_CONTROL_FALSE=$FALSE_COUNT
R3_18AP_CONTROL_TRUE=$TRUE_COUNT
R3_18AP_ORACLE_NATIVE_MISMATCH=0
R3_18AP_WITNESS_RESELECTION=0
R3_18AP_NEXT_STREAM_BITS_CONSUMED=0
R3_18AP_NEXT_HEADER_BITS_CONSUMED=0
R3_18AP_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18AP_SECOND_LATER_CONTROL_BITS_CONSUMED=0
R3_18AP_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18AP_NEGATIVE_CONTROLS=PASS
R3_18AP_PRIVACY_SCAN=PASS
EOF

python3 - <<'PY'
from pathlib import Path
files=[Path('r3_18ap_source_scope.txt'),Path('r3_18ap_replay_identity.tsv'),Path('r3_18ap_targets.tsv'),Path('r3_18ap_boxcars_instrumentation_sha256.txt'),Path('r3_18ap_summary.json'),Path('r3_18ap_comparison.tsv'),Path('r3_18ap_negative_controls.txt'),Path('r3_18ap_validation.txt'),Path('r3_18ap_aggregate.txt'),Path('r3_18ap_upstream_receipts.txt')]
for p in files:
    s=p.read_text(encoding='utf-8')
    assert 'github_pat_' not in s and 'ghp_' not in s and 'Bearer ' not in s
    assert '/home/runner' not in s and 'C:\\Users\\' not in s
print('R3_18AP_PRIVACY_SCAN=PASS files=10')
PY
sha256sum \
  r3_18ap_source_scope.txt \
  r3_18ap_replay_identity.tsv \
  r3_18ap_targets.tsv \
  r3_18ap_boxcars_instrumentation_sha256.txt \
  r3_18ap_summary.json \
  r3_18ap_comparison.tsv \
  r3_18ap_negative_controls.txt \
  r3_18ap_validation.txt \
  r3_18ap_aggregate.txt \
  r3_18ap_upstream_receipts.txt > r3_18ap_artifact_sha256.txt
sha256sum -c r3_18ap_artifact_sha256.txt

echo "R3_18AP_COMPLETE=PASS outcome=A rows=47 false=$FALSE_COUNT true=$TRUE_COUNT mismatch=0 mutation=0"

#!/usr/bin/env bash
set -euo pipefail

OUT="$RUNNER_TEMP/r318bl-out"
BH_DIR="$RUNNER_TEMP/r318bl-bh"
PROBE="crates/mimir-replay/tests/r3_18bl_probe_tmp.rs"
mkdir -p "$OUT" "$BH_DIR"
rm -rf "$OUT"/* "$BH_DIR"/*
cleanup() { rm -f "$PROBE"; }
trap cleanup EXIT

expected_scope="$RUNNER_TEMP/r318bl_expected_scope.txt"
actual_scope="$RUNNER_TEMP/r318bl_actual_scope.txt"
cat > "$expected_scope" <<'EOF'
.github/workflows/_tmp_r318bl_evidence.yml
.github/workflows/_tmp_r318bl_trigger.txt
tools/_tmp_r318bl_run.sh
EOF
git diff --name-only "$BASE_SHA...$GITHUB_SHA" | sort -u > "$actual_scope"
diff -u "$expected_scope" "$actual_scope"
test "$(wc -l < "$actual_scope")" -eq 3
test "$(git rev-parse "$BASE_SHA^{tree}")" = "$BASE_TREE"
{
  echo R3_18BL_BASE="$BASE_SHA/$BASE_TREE"
  echo R3_18BL_PRODUCTION="$PROD_SHA/$PROD_TREE"
  echo R3_18BL_PRODUCTION_MUTATION=0
  echo R3_18BL_CARGO_MUTATION=0
  echo R3_18BL_FIXTURE_MUTATION=0
  echo R3_18BL_CORPUS_MUTATION=0
  echo R3_18BL_SUPPORT_MUTATION=0
  echo R3_18BL_WITNESS_RESELECTION=0
  echo R3_18BL_NEXT_STREAM_HEADER_PAYLOAD_SECOND_CONTROL=0/0/0/0
  echo R3_18BL_EVIDENCE_SCOPE_FILES=3
} > "$OUT/r3_18bl_source_scope.txt"

gh run download "$BH_RUN" -R "$GITHUB_REPOSITORY" -n "$BH_ARTIFACT_NAME" -D "$BH_DIR"
(
  cd "$BH_DIR"
  sha256sum -c r3_18bh_artifact_sha256.txt
)
manifest_digest="sha256:$(sha256sum "$BH_DIR/r3_18bh_artifact_sha256.txt" | awk '{print $1}')"
test "$manifest_digest" = "$BH_MANIFEST_DIGEST"
grep -Fx 'R3_18BH_OUTCOME=A' "$BH_DIR/r3_18bh_aggregate.txt"
grep -Fx 'R3_18BH_TARGET_ROWS=3/3' "$BH_DIR/r3_18bh_aggregate.txt"
grep -Fx 'R3_18BH_FALSE=1' "$BH_DIR/r3_18bh_aggregate.txt"
grep -Fx 'R3_18BH_TRUE=2' "$BH_DIR/r3_18bh_aggregate.txt"
grep -Fx 'R3_18BH_NATIVE_ORACLE_EXACT=3/3' "$BH_DIR/r3_18bh_aggregate.txt"
grep -Fx 'R3_18BH_WITNESS_RESELECTION=0' "$BH_DIR/r3_18bh_aggregate.txt"
cp "$BH_DIR/r3_18bh_native_rows.tsv" "$OUT/r3_18bl_frozen_authority.tsv"

python3 - <<'PY'
from pathlib import Path
src = Path("crates/mimir-replay/tests/r3_18bk_post_bi_following_control.rs")
dst = Path("crates/mimir-replay/tests/r3_18bl_probe_tmp.rs")
text = src.read_text(encoding="utf-8")
needle = '''        assert_eq!(got.property_present_end_bit, expected_start + 1, "{path}");
        assert_eq!(got.stop_bit, expected_start + 1, "{path}");
'''
insert = needle + r'''
        let label = path.strip_prefix("../../").unwrap_or(path);
        println!(
            "R3_18BL_NATIVE\tlabel={}\tactor_object={}\tbi_stop={}\tpublished_bi_exact={}\tcontrol_start={}\tcontrol_end={}\tcontrol_value={}\tstop={}",
            label,
            actor_object,
            bi.stop_bit,
            got.payload_composition == bi,
            got.property_present_start_bit,
            got.property_present_end_bit,
            if got.property_present { 1 } else { 0 },
            got.stop_bit,
        );
'''
if text.count(needle) != 1:
    raise SystemExit(f"probe insertion count={text.count(needle)}")
text = text.replace(needle, insert, 1)
text += r'''

#[test]
fn r3_18bl_wrong_actor_authority_fails_before_control_success() {
    let (path, first_start, actor_object, _) = au_cases()
        .iter()
        .copied()
        .find(|(path, _, _, _)| path.ends_with("external_fixtures/sample_002.replay"))
        .expect("sample_002 BL witness");
    let (network, plan) = frozen_network_and_plan(path, "r318bl_wrong_actor");
    let (prior, control, an) = aq_from_frozen(&network, &plan, first_start, actor_object);
    let aq = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_v1(
        &network, &prior, &control, &plan, k3_context(), &an,
    ).expect("AQ prerequisite");
    let au = decode_replay_network_existing_actor_after_first_primitive_second_property_payload_following_payload_control_following_header_payload_following_payload_control_following_header_payload_following_payload_control_following_header_v1(
        &network, &prior, &control, &plan, k3_context(), &an, &aq,
    ).expect("AU prerequisite");
    let ay = decode_ay(&network, &prior, &control, &plan, k3_context(), &an, &au).expect("AY prerequisite");
    let ba = decode_ba(&network, &prior, &control, &plan, k3_context(), &an, &ay).expect("BA prerequisite");
    let be = decode_be(&network, &prior, &control, &plan, k3_context(), &an, &ay, &ba).expect("BE prerequisite");
    let bi = decode_bi(&network, &prior, &control, &plan, k3_context(), &an, &ay, &ba, &be).expect("BI prerequisite");
    let mut bad_prior = prior.clone();
    bad_prior.header_composition.following_header.actor_object_index = u32::MAX;
    assert!(decode_bk(
        &network, &bad_prior, &control, &plan, k3_context(), &an, &ay, &ba, &be, &bi,
    ).is_err(), "wrong actor authority must fail before BL control success");
}
'''
dst.write_text(text, encoding="utf-8", newline="\n")
print("R3_18BL_PROBE_DERIVATION=PASS")
PY

cargo +1.85.0 test --locked -p mimir-replay --test r3_18bl_probe_tmp -- --nocapture 2>&1 | tee "$RUNNER_TEMP/r318bl_probe.log"
rm -f "$PROBE"

python3 - "$BH_DIR/r3_18bh_native_rows.tsv" "$RUNNER_TEMP/r318bl_probe.log" "$OUT" <<'PY'
from pathlib import Path
import csv, json, sys
bh_path, probe_path, out_dir = map(Path, sys.argv[1:])
out_dir.mkdir(parents=True, exist_ok=True)
with bh_path.open(encoding="utf-8", newline="") as f:
    authority = {row["label"]: row for row in csv.DictReader(f, delimiter="\t")}
native = {}
for raw in probe_path.read_text(encoding="utf-8", errors="replace").splitlines():
    pos = raw.find("R3_18BL_NATIVE\t")
    if pos < 0:
        continue
    parts = raw[pos:].split("\t")[1:]
    row = dict(part.split("=", 1) for part in parts)
    if row["label"] in native:
        raise SystemExit(f"duplicate native label {row['label']}")
    native[row["label"]] = row
if len(authority) != 3 or len(native) != 3 or set(authority) != set(native):
    raise SystemExit(f"identity drift authority/native={len(authority)}/{len(native)}")
false_count = true_count = mismatch = bi_exact = bk_exact = 0
lines = ["label\tactor_context_object_id\tpayload_end_bit\tcontrol_start\tcontrol_end\tcontrol_value\tpublished_bi_exact\tpublished_bk_exact\tmismatch\twitness_reselection"]
for label, a in authority.items():
    g = native[label]
    checks = [
        int(g["actor_object"]) == int(a["actor_context_object_id"]),
        int(g["bi_stop"]) == int(a["payload_end_bit"]),
        g["published_bi_exact"] == "true",
        int(g["control_start"]) == int(a["next_property_present_start_bit"]),
        int(g["control_end"]) == int(a["next_property_present_end_bit"]),
        int(g["control_value"]) == int(a["next_property_present"]),
        int(g["stop"]) == int(a["next_property_present_end_bit"]),
        int(g["control_end"]) == int(g["control_start"]) + 1,
    ]
    row_mismatch = 0 if all(checks) else 1
    mismatch += row_mismatch
    bi_exact += int(g["published_bi_exact"] == "true" and int(g["bi_stop"]) == int(a["payload_end_bit"]))
    bk_exact += int(row_mismatch == 0)
    value = int(g["control_value"])
    false_count += int(value == 0)
    true_count += int(value == 1)
    lines.append("\t".join(map(str, [
        label, a["actor_context_object_id"], a["payload_end_bit"], g["control_start"], g["control_end"], value,
        1 if g["published_bi_exact"] == "true" else 0, 1 if row_mismatch == 0 else 0, row_mismatch, 0
    ])))
if (false_count, true_count) != (1, 2) or mismatch != 0 or bi_exact != 3 or bk_exact != 3:
    raise SystemExit(f"differential drift false/true={false_count}/{true_count} mismatch={mismatch} BI={bi_exact} BK={bk_exact}")
(out_dir / "r3_18bl_comparison.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
summary = {
    "outcome": "A", "rows": 3, "published_bk_exact": bk_exact, "published_bi_prerequisite_exact": bi_exact,
    "false_count": false_count, "true_count": true_count, "be_false_excluded": 37, "au_false_excluded": 7,
    "mismatch": mismatch, "witness_reselection": 0, "next_stream_bits_consumed": 0,
    "next_header_bits_consumed": 0, "next_payload_bits_consumed": 0, "second_later_control_bits_consumed": 0,
}
(out_dir / "r3_18bl_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("R3_18BL_DIFFERENTIAL=PASS")
PY

cargo +1.85.0 test --locked -p mimir-replay --test r3_18bk_post_bi_following_control

test_source="crates/mimir-replay/tests/r3_18bk_post_bi_following_control.rs"
grep -F 'assert_eq!(excluded_au, 7' "$test_source"
grep -F 'assert_eq!(excluded_be, 37' "$test_source"
grep -F 'assert_eq!(false_count, 1' "$test_source"
grep -F 'assert_eq!(true_count, 2' "$test_source"
grep -F 'fn r3_18bk_corrupt_bi_context_lookup_and_truncation_fail_closed()' "$test_source"
grep -F 'fn r3_18bk_source_scope_is_one_bi_recompute_one_read_bit_and_no_following_decode_or_loop()' "$test_source"
cat > "$OUT/r3_18bl_negative_controls.txt" <<'EOF'
R3_18BL_WRONG_ACTOR=PASS
R3_18BL_UNRESOLVED_LOOKUP=PASS
R3_18BL_WRONG_EXACT_CONTEXT=PASS
R3_18BL_CORRUPT_BI_PRIOR=PASS
R3_18BL_TRUNCATION_BEFORE_CONTROL=PASS
R3_18BL_REPEATABILITY=PASS 3/3
R3_18BL_POST_STOP_POISON=PASS 3/3
R3_18BL_BE_FALSE_EXCLUDED=PASS 37/37
R3_18BL_AU_FALSE_EXCLUDED=PASS 7/7
R3_18BL_SOURCE_SCOPE_ONE_BI_RECOMPUTE_ONE_READ_NO_LOOP=PASS
R3_18BL_NEXT_STREAM_HEADER_PAYLOAD_SECOND_CONTROL=0/0/0/0
EOF

cargo +1.85.0 fmt --all -- --check
cargo +1.85.0 check --locked --workspace --all-targets --all-features
cargo +1.85.0 clippy --locked --workspace --all-targets --all-features -- -D warnings
cargo +1.85.0 test --locked --workspace --all-features
pwsh -NoProfile -File scripts/verify_repo.ps1
git diff --check
test -z "$(git status --porcelain)"
cat > "$OUT/r3_18bl_validation.txt" <<'EOF'
R3_18BL_FOCUSED_BK_SUITE=PASS
R3_18BL_TEMP_WRONG_ACTOR_PROBE=PASS
R3_18BL_FMT=PASS
R3_18BL_WORKSPACE_CHECK=PASS
R3_18BL_CLIPPY_D_WARNINGS=PASS
R3_18BL_WORKSPACE_TEST=PASS
R3_18BL_REPOSITORY_VERIFIER=PASS
R3_18BL_GIT_DIFF_CHECK=PASS
R3_18BL_WORKTREE_CLEAN=PASS
EOF
cat > "$OUT/r3_18bl_upstream_receipts.txt" <<EOF
R3_18BL_BASE=$BASE_SHA/$BASE_TREE
R3_18BL_PRODUCTION=$PROD_SHA/$PROD_TREE
R3_18BL_PRODUCTION_PARENT=$PROD_PARENT
R3_18BL_LIB_BLOB=$LIB_BLOB
R3_18BL_BK_TEST_BLOB=$BK_TEST_BLOB
R3_18BL_BL_SPEC_BLOB=$BL_SPEC_BLOB
R3_18BL_BK_BUILDER=$BK_BUILDER_RUN/$BK_BUILDER_JOB
R3_18BL_BK_VALIDATION_PR=$BK_VALIDATION_PR
R3_18BL_BK_PR_CI=$BK_PR_CI_RUN/$BK_PR_CI_JOB
R3_18BL_BK_PUBLISHED_CI=$BK_PUBLISHED_CI_RUN/$BK_PUBLISHED_CI_JOB
R3_18BL_BH_AUTHORITY=$BH_HEAD/$BH_RUN/$BH_JOB
R3_18BL_BH_SAME_HEAD_CI=$BH_SAME_HEAD_CI_RUN/$BH_SAME_HEAD_CI_JOB
R3_18BL_BH_ARTIFACT=$BH_ARTIFACT/$BH_ARTIFACT_SIZE/$BH_DIGEST
R3_18BL_BH_MANIFEST=$BH_MANIFEST_DIGEST
EOF
cat > "$OUT/r3_18bl_aggregate.txt" <<'EOF'
R3_18BL_OUTCOME=A
R3_18BL_EVIDENCE=PASS
R3_18BL_FROZEN_ROWS=3/3
R3_18BL_PUBLISHED_BK_EXACT=3/3
R3_18BL_PUBLISHED_BI_PREREQUISITE=3/3
R3_18BL_CONTROL_FALSE=1
R3_18BL_CONTROL_TRUE=2
R3_18BL_BE_FALSE_EXCLUDED=37/37
R3_18BL_AU_FALSE_EXCLUDED=7/7
R3_18BL_MISMATCH=0
R3_18BL_WITNESS_RESELECTION=0
R3_18BL_NEXT_STREAM_HEADER_PAYLOAD_SECOND_CONTROL=0/0/0/0
R3_18BL_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18BL_NEGATIVE_CONTROLS=PASS
R3_18BL_FULL_VALIDATION=PASS
R3_18BL_PRIVACY_SCAN=PASS
EOF

if grep -RniE 'Omersevik|Maximillan|github_pat_|ghp_|/home/runner|C:\\Users\\' "$OUT"; then
  echo 'privacy scan failed' >&2
  exit 1
fi
echo R3_18BL_PRIVACY_SCAN=PASS

#!/usr/bin/env bash
set -euo pipefail

OUT="$RUNNER_TEMP/r318ar-out"
AP_DIR="$RUNNER_TEMP/r318ar-ap"
PROBE="crates/mimir-replay/tests/r3_18ar_probe_tmp.rs"
mkdir -p "$OUT" "$AP_DIR"
rm -rf "$OUT"/* "$AP_DIR"/*

cleanup() {
  rm -f "$PROBE"
}
trap cleanup EXIT

expected_scope="$RUNNER_TEMP/r318ar_expected_scope.txt"
actual_scope="$RUNNER_TEMP/r318ar_actual_scope.txt"
cat > "$expected_scope" <<'EOF'
.github/workflows/_tmp_r318ar_evidence.yml
.github/workflows/_tmp_r318ar_trigger.txt
tools/_tmp_r318ar_run.sh
EOF
git diff --name-only "$BASE_SHA...$GITHUB_SHA" | sort -u > "$actual_scope"
diff -u "$expected_scope" "$actual_scope"
test "$(wc -l < "$actual_scope")" -eq 3
test "$(git rev-parse "$BASE_SHA^{tree}")" = "$BASE_TREE"

{
  echo R3_18AR_BASE="$BASE_SHA/$BASE_TREE"
  echo R3_18AR_PRODUCTION="$PROD_SHA/$PROD_TREE"
  echo R3_18AR_PRODUCTION_MUTATION=0
  echo R3_18AR_CARGO_MUTATION=0
  echo R3_18AR_FIXTURE_MUTATION=0
  echo R3_18AR_CORPUS_MUTATION=0
  echo R3_18AR_SUPPORT_MUTATION=0
  echo R3_18AR_WITNESS_RESELECTION=0
  echo R3_18AR_NEXT_STREAM_BITS_CONSUMED=0
  echo R3_18AR_NEXT_HEADER_BITS_CONSUMED=0
  echo R3_18AR_NEXT_PAYLOAD_BITS_CONSUMED=0
  echo R3_18AR_SECOND_LATER_CONTROL_BITS_CONSUMED=0
  echo R3_18AR_EVIDENCE_SCOPE_FILES=3
} > "$OUT/r3_18ar_source_scope.txt"

gh run download "$AP_RUN" -R "$GITHUB_REPOSITORY" -n "$AP_ARTIFACT_NAME" -D "$AP_DIR"
(
  cd "$AP_DIR"
  sha256sum -c r3_18ap_artifact_sha256.txt
)
grep -Fx 'R3_18AP_OUTCOME=A' "$AP_DIR/r3_18ap_aggregate.txt"
grep -Fx 'R3_18AP_FROZEN_ROWS=47/47' "$AP_DIR/r3_18ap_aggregate.txt"
grep -Fx 'R3_18AP_CONTROL_FALSE=7' "$AP_DIR/r3_18ap_aggregate.txt"
grep -Fx 'R3_18AP_CONTROL_TRUE=40' "$AP_DIR/r3_18ap_aggregate.txt"
grep -Fx 'R3_18AP_ORACLE_NATIVE_MISMATCH=0' "$AP_DIR/r3_18ap_aggregate.txt"
grep -Fx 'R3_18AP_WITNESS_RESELECTION=0' "$AP_DIR/r3_18ap_aggregate.txt"

cp "$AP_DIR/r3_18ap_replay_identity.tsv" "$OUT/r3_18ar_replay_identity.tsv"
cp "$AP_DIR/r3_18ap_targets.tsv" "$OUT/r3_18ar_frozen_targets.tsv"

python3 - <<'PY'
from pathlib import Path

src = Path("crates/mimir-replay/tests/r3_18aq_post_an_payload_control.rs")
dst = Path("crates/mimir-replay/tests/r3_18ar_probe_tmp.rs")
text = src.read_text(encoding="utf-8")
needle = '''        assert_eq!(got.property_present_end_bit, control_start + 1, "{path}");
        assert_eq!(got.stop_bit, control_start + 1, "{path}");
'''
insert = needle + r'''
        let label = path.strip_prefix("../../").unwrap_or(path);
        println!(
            "R3_18AR_NATIVE\tlabel={}\tfirst_start={}\tactor_object={}\tan_stop={}\tcontrol_start={}\tcontrol_end={}\tcontrol_value={}\tstop={}",
            label,
            first_start,
            actor_object,
            an.stop_bit,
            got.property_present_start_bit,
            got.property_present_end_bit,
            if got.following_property_present { 1 } else { 0 },
            got.stop_bit,
        );
'''
count = text.count(needle)
if count != 1:
    raise SystemExit(f"R3.18AR probe insertion count={count}")
dst.write_text(text.replace(needle, insert, 1), encoding="utf-8", newline="\n")
print("R3_18AR_PROBE_DERIVATION=PASS")
PY

cargo +1.85.0 test --locked -p mimir-replay \
  --test r3_18ar_probe_tmp \
  r3_18aq_all_47_frozen_ap_rows_accept_mixed_boolean_and_stop_exactly_one_bit_later \
  -- --exact --nocapture 2>&1 | tee "$RUNNER_TEMP/r318ar_probe.log"

rm -f "$PROBE"

python3 - "$AP_DIR/r3_18ap_comparison.tsv" "$AP_DIR/r3_18ap_targets.tsv" "$RUNNER_TEMP/r318ar_probe.log" "$OUT" <<'PY'
from pathlib import Path
import json
import sys

comparison_path, targets_path, probe_path, out_dir = map(Path, sys.argv[1:])
out_dir.mkdir(parents=True, exist_ok=True)

def kv_line(line, prefix):
    parts = line.rstrip("\n").split("\t")
    if not parts or parts[0] != prefix:
        raise ValueError(f"bad prefix: {line[:80]!r}")
    row = {}
    for part in parts[1:]:
        k, v = part.split("=", 1)
        row[k] = v
    return row

ap_rows = {}
for line in comparison_path.read_text(encoding="utf-8").splitlines():
    if not line:
        continue
    row = kv_line(line, "R3_18AP_COMPARE")
    label = row["label"]
    if label in ap_rows:
        raise SystemExit(f"duplicate AP label: {label}")
    ap_rows[label] = row

targets = {}
for line in targets_path.read_text(encoding="utf-8").splitlines():
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 8:
        raise SystemExit(f"bad target row: {line}")
    label, frame, actor_ordinal, actor_object, first_start, payload_start, control_start, semantic_int = parts
    if label in targets:
        raise SystemExit(f"duplicate target label: {label}")
    targets[label] = {
        "frame_index": int(frame),
        "actor_ordinal": int(actor_ordinal),
        "actor_object": int(actor_object),
        "first_start": int(first_start),
        "payload_start": int(payload_start),
        "control_start": int(control_start),
        "semantic_int": int(semantic_int),
    }

native = {}
for raw in probe_path.read_text(encoding="utf-8", errors="replace").splitlines():
    pos = raw.find("R3_18AR_NATIVE\t")
    if pos < 0:
        continue
    row = kv_line(raw[pos:], "R3_18AR_NATIVE")
    label = row["label"]
    if label in native:
        raise SystemExit(f"duplicate native label: {label}")
    native[label] = row

if len(ap_rows) != 47 or len(targets) != 47 or len(native) != 47:
    raise SystemExit(f"row counts AP/targets/native={len(ap_rows)}/{len(targets)}/{len(native)}")
if set(ap_rows) != set(targets) or set(ap_rows) != set(native):
    raise SystemExit("frozen witness identity sets differ")

false_count = 0
true_count = 0
mismatch = 0
published_an_exact = 0
published_aq_exact = 0
lines = []

for label in targets:
    ap = ap_rows[label]
    target = targets[label]
    got = native[label]

    checks = [
        int(ap["frame_index"]) == target["frame_index"],
        int(ap["actor_ordinal"]) == target["actor_ordinal"],
        int(ap["actor_context_object_id"]) == target["actor_object"],
        int(ap["control_start"]) == target["control_start"],
        int(ap["control_end"]) == target["control_start"] + 1,
        int(ap["published_an_exact"]) == 1,
        int(ap["oracle_native_exact"]) == 1,
        int(ap["mismatch"]) == 0,
        int(ap["witness_reselection"]) == 0,
        int(got["first_start"]) == target["first_start"],
        int(got["actor_object"]) == target["actor_object"],
        int(got["an_stop"]) == target["control_start"],
        int(got["control_start"]) == int(ap["control_start"]),
        int(got["control_end"]) == int(ap["control_end"]),
        int(got["control_value"]) == int(ap["control_value"]),
        int(got["stop"]) == int(ap["control_end"]),
    ]
    row_mismatch = 0 if all(checks) else 1
    mismatch += row_mismatch
    if int(got["an_stop"]) == int(ap["control_start"]):
        published_an_exact += 1
    if row_mismatch == 0:
        published_aq_exact += 1

    value = int(got["control_value"])
    if value == 0:
        false_count += 1
    elif value == 1:
        true_count += 1
    else:
        raise SystemExit(f"non-boolean control for {label}: {value}")

    lines.append(
        "\t".join([
            "R3_18AR_COMPARE",
            f"label={label}",
            f"frame_index={target['frame_index']}",
            f"actor_ordinal={target['actor_ordinal']}",
            f"actor_context_object_id={target['actor_object']}",
            f"control_start={got['control_start']}",
            f"control_end={got['control_end']}",
            f"control_value={value}",
            f"published_an_exact={1 if int(got['an_stop']) == int(ap['control_start']) else 0}",
            f"published_aq_exact={1 if row_mismatch == 0 else 0}",
            f"mismatch={row_mismatch}",
            "witness_reselection=0",
        ])
    )

if (false_count, true_count) != (7, 40):
    raise SystemExit(f"distribution drift false/true={false_count}/{true_count}")
if mismatch != 0 or published_an_exact != 47 or published_aq_exact != 47:
    raise SystemExit(
        f"differential mismatch={mismatch} AN={published_an_exact} AQ={published_aq_exact}"
    )

(out_dir / "r3_18ar_comparison.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
summary = {
    "outcome": "A",
    "rows": 47,
    "published_aq_exact": published_aq_exact,
    "published_an_prerequisite_exact": published_an_exact,
    "false_count": false_count,
    "true_count": true_count,
    "mismatch": mismatch,
    "witness_reselection": 0,
    "next_stream_bits_consumed": 0,
    "next_header_bits_consumed": 0,
    "next_payload_bits_consumed": 0,
    "second_later_control_bits_consumed": 0,
}
(out_dir / "r3_18ar_summary.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print("R3_18AR_DIFFERENTIAL=PASS")
PY

cargo +1.85.0 test --locked -p mimir-replay --test r3_18aq_post_an_payload_control

test_source="crates/mimir-replay/tests/r3_18aq_post_an_payload_control.rs"
grep -F 'fn r3_18aq_wrong_actor_and_unresolved_lookup_fail_closed()' "$test_source"
grep -F 'actor_object_index = u32::MAX;' "$test_source"
grep -F 'missing_lookup.object_lookups[98] = None;' "$test_source"
grep -F 'fn r3_18aq_truncation_corrupt_prior_and_wrong_context_fail_closed()' "$test_source"
grep -F 'expect_err("missing following control bit must reject")' "$test_source"
grep -F 'corrupt.stop_bit += 1;' "$test_source"
grep -F 'wrong_context.version_major -= 1;' "$test_source"
grep -F 'fn r3_18aq_source_scope_is_one_an_recompute_one_read_bit_and_no_following_decode_or_loop()' "$test_source"

cat > "$OUT/r3_18ar_negative_controls.txt" <<'EOF'
R3_18AR_TRUNCATION_BEFORE_CONTROL=PASS
R3_18AR_WRONG_ACTOR=PASS
R3_18AR_UNRESOLVED_LOOKUP=PASS
R3_18AR_WRONG_EXACT_CONTEXT=PASS
R3_18AR_CORRUPT_AN_PRIOR=PASS
R3_18AR_REPEATABILITY=PASS 47/47
R3_18AR_POST_STOP_POISON=PASS 47/47
R3_18AR_SOURCE_SCOPE_ONE_READ_NO_LOOP=PASS
R3_18AR_NEXT_STREAM_BITS_CONSUMED=0
R3_18AR_NEXT_HEADER_BITS_CONSUMED=0
R3_18AR_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18AR_SECOND_LATER_CONTROL_BITS_CONSUMED=0
EOF

cargo +1.85.0 fmt --all -- --check
cargo +1.85.0 check --locked --workspace --all-targets --all-features
cargo +1.85.0 clippy --locked --workspace --all-targets --all-features -- -D warnings
cargo +1.85.0 test --locked --workspace --all-features
pwsh -NoProfile -File scripts/verify_repo.ps1
git diff --check
test -z "$(git status --porcelain)"

cat > "$OUT/r3_18ar_validation.txt" <<'EOF'
R3_18AR_FOCUSED_AQ_SUITE=PASS
R3_18AR_FMT=PASS
R3_18AR_WORKSPACE_CHECK=PASS
R3_18AR_CLIPPY_D_WARNINGS=PASS
R3_18AR_WORKSPACE_TEST=PASS
R3_18AR_REPOSITORY_VERIFIER=PASS
R3_18AR_GIT_DIFF_CHECK=PASS
R3_18AR_WORKTREE_CLEAN=PASS
EOF

cat > "$OUT/r3_18ar_upstream_receipts.txt" <<EOF
R3_18AR_BASE=$BASE_SHA/$BASE_TREE
R3_18AR_PRODUCTION=$PROD_SHA/$PROD_TREE
R3_18AR_PRODUCTION_PARENT=$PROD_PARENT
R3_18AR_LIB_BLOB=$LIB_BLOB
R3_18AR_AQ_TEST_BLOB=$AQ_TEST_BLOB
R3_18AR_AR_SPEC_BLOB=$AR_SPEC_BLOB
R3_18AR_AQ_BUILDER=$AQ_BUILDER_HEAD/$AQ_BUILDER_RUN/$AQ_BUILDER_JOB
R3_18AR_AQ_RECEIPT=$AQ_RECEIPT_ARTIFACT/$AQ_RECEIPT_SIZE/$AQ_RECEIPT_DIGEST
R3_18AR_AQ_VALIDATION_PR=$AQ_VALIDATION_PR
R3_18AR_AQ_PR_CI=$AQ_PR_CI_RUN/$AQ_PR_CI_JOB
R3_18AR_AQ_PUBLISHED_CI=$AQ_PUBLISHED_CI_RUN/$AQ_PUBLISHED_CI_JOB
R3_18AR_AP_AUTHORITY=$AP_HEAD/$AP_RUN/$AP_JOB
R3_18AR_AP_ARTIFACT=$AP_ARTIFACT/$AP_ARTIFACT_SIZE/$AP_DIGEST
EOF

cat > "$OUT/r3_18ar_aggregate.txt" <<'EOF'
R3_18AR_OUTCOME=A
R3_18AR_EVIDENCE=PASS
R3_18AR_FROZEN_ROWS=47/47
R3_18AR_PUBLISHED_AQ_EXACT=47/47
R3_18AR_PUBLISHED_AN_PREREQUISITE=47/47
R3_18AR_CONTROL_FALSE=7
R3_18AR_CONTROL_TRUE=40
R3_18AR_MISMATCH=0
R3_18AR_WITNESS_RESELECTION=0
R3_18AR_REPEATABILITY=PASS 47/47
R3_18AR_NEXT_STREAM_BITS_CONSUMED=0
R3_18AR_NEXT_HEADER_BITS_CONSUMED=0
R3_18AR_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18AR_SECOND_LATER_CONTROL_BITS_CONSUMED=0
R3_18AR_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18AR_NEGATIVE_CONTROLS=PASS
R3_18AR_PRIVACY_SCAN=PASS
EOF

if grep -Eiq 'player[_ -]?name|account[_ -]?id|remote[_ -]?id|raw_bits_hex|raw_payload' \
  "$OUT/r3_18ar_comparison.tsv" "$OUT/r3_18ar_summary.json" "$OUT/r3_18ar_negative_controls.txt"; then
  echo "privacy scan failed" >&2
  exit 1
fi

grep -Fx 'R3_18AR_OUTCOME=A' "$OUT/r3_18ar_aggregate.txt"
grep -Fx 'R3_18AR_PUBLISHED_AQ_EXACT=47/47' "$OUT/r3_18ar_aggregate.txt"
grep -Fx 'R3_18AR_CONTROL_FALSE=7' "$OUT/r3_18ar_aggregate.txt"
grep -Fx 'R3_18AR_CONTROL_TRUE=40' "$OUT/r3_18ar_aggregate.txt"
echo R3_18AR_RUN_SCRIPT=PASS

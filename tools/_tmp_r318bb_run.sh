#!/usr/bin/env bash
set -euo pipefail

OUT="$RUNNER_TEMP/r318bb-out"
AX_DIR="$RUNNER_TEMP/r318bb-ax"
PROBE="crates/mimir-replay/tests/r3_18bb_probe_tmp.rs"
mkdir -p "$OUT" "$AX_DIR"
rm -rf "$OUT"/* "$AX_DIR"/*

cleanup() { rm -f "$PROBE"; }
trap cleanup EXIT

cat > "$RUNNER_TEMP/r318bb_expected_scope.txt" <<'EOF'
.github/workflows/r318bb-published-ba-v1.yml
tools/_tmp_r318bb_run.sh
EOF
git diff --name-only "$BASE_SHA...$GITHUB_SHA" | sort -u > "$RUNNER_TEMP/r318bb_actual_scope.txt"
diff -u "$RUNNER_TEMP/r318bb_expected_scope.txt" "$RUNNER_TEMP/r318bb_actual_scope.txt"
test "$(wc -l < "$RUNNER_TEMP/r318bb_actual_scope.txt")" -eq 2
test "$(git rev-parse "$BASE_SHA^{tree}")" = "$BASE_TREE"

{
  echo R3_18BB_BASE="$BASE_SHA/$BASE_TREE"
  echo R3_18BB_PRODUCTION="$PROD_SHA/$PROD_TREE"
  echo R3_18BB_PRODUCTION_MUTATION=0
  echo R3_18BB_CARGO_MUTATION=0
  echo R3_18BB_FIXTURE_MUTATION=0
  echo R3_18BB_CORPUS_MUTATION=0
  echo R3_18BB_SUPPORT_MUTATION=0
  echo R3_18BB_WITNESS_RESELECTION=0
  echo R3_18BB_NEXT_STREAM_BITS_CONSUMED=0
  echo R3_18BB_NEXT_HEADER_BITS_CONSUMED=0
  echo R3_18BB_NEXT_PAYLOAD_BITS_CONSUMED=0
  echo R3_18BB_SECOND_LATER_CONTROL_BITS_CONSUMED=0
  echo R3_18BB_EVIDENCE_SCOPE_FILES=2
} > "$OUT/r3_18bb_source_scope.txt"

gh run download "$AX_RUN" -R "$GITHUB_REPOSITORY" -n "$AX_ARTIFACT_NAME" -D "$AX_DIR"
(
  cd "$AX_DIR"
  sha256sum -c r3_18ax_artifact_sha256.txt
)
grep -Fx 'R3_18AX_OUTCOME=A' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_FROZEN_ROWS=40/40' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_CONTROL_FALSE=37' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_CONTROL_TRUE=3' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_ORACLE_NATIVE_MISMATCH=0' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_WITNESS_RESELECTION=0' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_NEXT_STREAM_BITS_CONSUMED=0' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_NEXT_HEADER_BITS_CONSUMED=0' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_NEXT_PAYLOAD_BITS_CONSUMED=0' "$AX_DIR/r3_18ax_aggregate.txt"
grep -Fx 'R3_18AX_SECOND_LATER_CONTROL_BITS_CONSUMED=0' "$AX_DIR/r3_18ax_aggregate.txt"

cp "$AX_DIR/r3_18ax_replay_identity.tsv" "$OUT/r3_18bb_replay_identity.tsv"
cp "$AX_DIR/r3_18ax_comparison.tsv" "$OUT/r3_18bb_frozen_ax.tsv"

python3 - <<'PY'
from pathlib import Path
src = Path("crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs")
dst = Path("crates/mimir-replay/tests/r3_18bb_probe_tmp.rs")
text = src.read_text(encoding="utf-8")
needle = '''        assert_eq!(got.property_present_end_bit, ay.stop_bit + 1, "{path}");
        assert_eq!(got.stop_bit, ay.stop_bit + 1, "{path}");
'''
insert = needle + r'''
        let label = path.strip_prefix("../../").unwrap_or(path);
        println!(
            "R3_18BB_NATIVE\tlabel={}\tay_stop={}\tcontrol_start={}\tcontrol_end={}\tcontrol_value={}\tstop={}",
            label,
            ay.stop_bit,
            got.property_present_start_bit,
            got.property_present_end_bit,
            if got.following_property_present { 1 } else { 0 },
            got.stop_bit,
        );
'''
count = text.count(needle)
if count != 1:
    raise SystemExit(f"R3.18BB probe insertion count={count}")
dst.write_text(text.replace(needle, insert, 1), encoding="utf-8", newline="\n")
print("R3_18BB_PROBE_DERIVATION=PASS")
PY

cargo +1.85.0 test --locked -p mimir-replay \
  --test r3_18bb_probe_tmp \
  r3_18ba_exact_40_ay_rows_accept_mixed_boolean_and_stop_exactly_one_bit_later \
  -- --exact --nocapture 2>&1 | tee "$RUNNER_TEMP/r318bb_probe.log"
rm -f "$PROBE"

python3 - "$AX_DIR/r3_18ax_comparison.tsv" "$RUNNER_TEMP/r318bb_probe.log" "$OUT" <<'PY'
from pathlib import Path
import json, sys
ax_path, probe_path, out_dir = map(Path, sys.argv[1:])
out_dir.mkdir(parents=True, exist_ok=True)

def parse_kv(line, prefix):
    parts = line.rstrip("\n").split("\t")
    if not parts or parts[0] != prefix:
        raise ValueError(line[:100])
    row = {}
    for part in parts[1:]:
        key, value = part.split("=", 1)
        row[key] = value
    return row

ax = {}
for line in ax_path.read_text(encoding="utf-8").splitlines():
    if not line:
        continue
    row = parse_kv(line, "R3_18AX_COMPARE")
    label = row["label"]
    if label in ax:
        raise SystemExit(f"duplicate AX label {label}")
    ax[label] = row

native = {}
for raw in probe_path.read_text(encoding="utf-8", errors="replace").splitlines():
    pos = raw.find("R3_18BB_NATIVE\t")
    if pos < 0:
        continue
    row = parse_kv(raw[pos:], "R3_18BB_NATIVE")
    label = row["label"]
    if label in native:
        raise SystemExit(f"duplicate BA label {label}")
    native[label] = row

if len(ax) != 40 or len(native) != 40:
    raise SystemExit(f"row counts AX/BA={len(ax)}/{len(native)}")
if set(ax) != set(native):
    raise SystemExit(f"witness identity mismatch: {sorted(set(ax) ^ set(native))}")

false_count = true_count = mismatch = ay_exact = ba_exact = 0
lines = []
for label in ax:
    frozen, got = ax[label], native[label]
    checks = [
        int(frozen["aw_payload_exact"]) == 1,
        int(frozen["oracle_native_exact"]) == 1,
        int(frozen["mismatch"]) == 0,
        int(frozen["witness_reselection"]) == 0,
        int(got["ay_stop"]) == int(frozen["payload_end"]),
        int(got["control_start"]) == int(frozen["control_start"]),
        int(got["control_end"]) == int(frozen["control_end"]),
        int(got["control_value"]) == int(frozen["control_value"]),
        int(got["stop"]) == int(frozen["control_end"]),
        int(got["control_end"]) == int(got["control_start"]) + 1,
    ]
    row_mismatch = 0 if all(checks) else 1
    mismatch += row_mismatch
    if int(got["ay_stop"]) == int(frozen["payload_end"]): ay_exact += 1
    if row_mismatch == 0: ba_exact += 1
    value = int(got["control_value"])
    if value == 0: false_count += 1
    elif value == 1: true_count += 1
    else: raise SystemExit(f"non-boolean control {label}: {value}")
    lines.append("\t".join([
        "R3_18BB_COMPARE", f"label={label}", f"payload_end={frozen['payload_end']}",
        f"control_start={got['control_start']}", f"control_end={got['control_end']}",
        f"control_value={value}", f"ay_prerequisite_exact={1 if int(got['ay_stop']) == int(frozen['payload_end']) else 0}",
        f"published_ba_exact={1 if row_mismatch == 0 else 0}", f"mismatch={row_mismatch}",
        "witness_reselection=0"
    ]))

if (false_count, true_count) != (37, 3):
    raise SystemExit(f"distribution drift false/true={false_count}/{true_count}")
if mismatch != 0 or ay_exact != 40 or ba_exact != 40:
    raise SystemExit(f"differential mismatch={mismatch} AY={ay_exact} BA={ba_exact}")
(out_dir / "r3_18bb_comparison.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
summary = {"outcome":"A","rows":40,"published_ba_exact":ba_exact,"ay_prerequisite_exact":ay_exact,
           "false_count":false_count,"true_count":true_count,"mismatch":mismatch,"witness_reselection":0,
           "next_stream_bits_consumed":0,"next_header_bits_consumed":0,"next_payload_bits_consumed":0,
           "second_later_control_bits_consumed":0}
(out_dir / "r3_18bb_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("R3_18BB_DIFFERENTIAL=PASS")
PY

cargo +1.85.0 test --locked -p mimir-replay --test r3_18ba_post_ay_payload_control

test_source="crates/mimir-replay/tests/r3_18ba_post_ay_payload_control.rs"
grep -F 'fn r3_18ba_exact_40_ay_rows_accept_mixed_boolean_and_stop_exactly_one_bit_later()' "$test_source"
grep -F 'assert_eq!(excluded, 7' "$test_source"
grep -F 'assert_eq!(false_count, 37' "$test_source"
grep -F 'assert_eq!(true_count, 3' "$test_source"
grep -F 'fn r3_18ba_prerequisite_corruption_truncation_and_context_drift_fail_closed()' "$test_source"
grep -F 'actor_object_index = u32::MAX;' "$test_source"
grep -F 'missing_lookup.object_lookups[98] = None;' "$test_source"
grep -F 'wrong_context.version_major -= 1;' "$test_source"
grep -F 'fn r3_18ba_source_scope_is_one_ay_recompute_one_read_bit_and_no_following_decode_or_loop()' "$test_source"

cat > "$OUT/r3_18bb_negative_controls.txt" <<'EOF'
R3_18BB_UPSTREAM_FALSE_TERMINATORS_EXCLUDED=PASS 7/7
R3_18BB_TRUNCATION_FAIL_CLOSED=PASS
R3_18BB_WRONG_ACTOR=PASS
R3_18BB_UNRESOLVED_LOOKUP=PASS
R3_18BB_WRONG_EXACT_CONTEXT=PASS
R3_18BB_CORRUPT_AY_PRIOR=PASS
R3_18BB_REPEATABILITY=PASS 40/40
R3_18BB_POST_STOP_POISON=PASS 40/40
R3_18BB_SOURCE_SCOPE_ONE_READ_NO_LOOP=PASS
R3_18BB_NEXT_STREAM_BITS_CONSUMED=0
R3_18BB_NEXT_HEADER_BITS_CONSUMED=0
R3_18BB_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18BB_SECOND_LATER_CONTROL_BITS_CONSUMED=0
EOF

cargo +1.85.0 fmt --all -- --check
cargo +1.85.0 check --locked --workspace --all-targets --all-features
cargo +1.85.0 clippy --locked --workspace --all-targets --all-features -- -D warnings
cargo +1.85.0 test --locked --workspace --all-features
pwsh -NoProfile -File scripts/verify_repo.ps1
git diff --check
test -z "$(git status --porcelain)"

cat > "$OUT/r3_18bb_validation.txt" <<'EOF'
R3_18BB_FOCUSED_BA_SUITE=PASS
R3_18BB_FMT=PASS
R3_18BB_WORKSPACE_CHECK=PASS
R3_18BB_CLIPPY_D_WARNINGS=PASS
R3_18BB_WORKSPACE_TEST=PASS
R3_18BB_REPOSITORY_VERIFIER=PASS
R3_18BB_GIT_DIFF_CHECK=PASS
R3_18BB_WORKTREE_CLEAN=PASS
EOF

cat > "$OUT/r3_18bb_upstream_receipts.txt" <<EOF
R3_18BB_BASE=$BASE_SHA/$BASE_TREE
R3_18BB_PRODUCTION=$PROD_SHA/$PROD_TREE
R3_18BB_PRODUCTION_PARENT=$PROD_PARENT
R3_18BB_LIB_BLOB=$LIB_BLOB
R3_18BB_BA_TEST_BLOB=$BA_TEST_BLOB
R3_18BB_BA_DECISION_BLOB=$BA_DECISION_BLOB
R3_18BB_BB_SPEC_BLOB=$BB_SPEC_BLOB
R3_18BB_BA_BUILDER=$BA_BUILDER_RUN/$BA_BUILDER_JOB
R3_18BB_BA_PR_CI=$BA_PR_CI_RUN/$BA_PR_CI_JOB
R3_18BB_BA_CANDIDATE_CI=$BA_CANDIDATE_CI_RUN/$BA_CANDIDATE_CI_JOB
R3_18BB_BA_PUBLISHED_CI=$BA_PUBLISHED_CI_RUN/$BA_PUBLISHED_CI_JOB
R3_18BB_CONTINUITY_CI=$CONTINUITY_CI_RUN/$CONTINUITY_CI_JOB
R3_18BB_CONTINUITY_KA=$CONTINUITY_KA_RUN/$CONTINUITY_KA_JOB
R3_18BB_AX_AUTHORITY=$AX_HEAD/$AX_RUN/$AX_JOB
R3_18BB_AX_ARTIFACT=$AX_ARTIFACT/$AX_ARTIFACT_SIZE/$AX_DIGEST
EOF

cat > "$OUT/r3_18bb_aggregate.txt" <<'EOF'
R3_18BB_OUTCOME=A
R3_18BB_EVIDENCE=PASS
R3_18BB_FROZEN_ROWS=40/40
R3_18BB_PUBLISHED_BA_EXACT=40/40
R3_18BB_AY_PREREQUISITE_EXACT=40/40
R3_18BB_CONTROL_FALSE=37
R3_18BB_CONTROL_TRUE=3
R3_18BB_MISMATCH=0
R3_18BB_WITNESS_RESELECTION=0
R3_18BB_NEXT_STREAM_BITS_CONSUMED=0
R3_18BB_NEXT_HEADER_BITS_CONSUMED=0
R3_18BB_NEXT_PAYLOAD_BITS_CONSUMED=0
R3_18BB_SECOND_LATER_CONTROL_BITS_CONSUMED=0
R3_18BB_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0
R3_18BB_NEGATIVE_CONTROLS=PASS
R3_18BB_PRIVACY_SCAN=PASS
EOF

if grep -R -nE '/home/|/Users/|[A-Za-z]:\\\\Users\\\\|@gmail\.com|@hotmail\.com' "$OUT"; then
  echo 'privacy-sensitive path/email found' >&2
  exit 1
fi

(
  cd "$OUT"
  sha256sum r3_18bb_source_scope.txt r3_18bb_replay_identity.tsv r3_18bb_frozen_ax.tsv \
    r3_18bb_summary.json r3_18bb_comparison.tsv r3_18bb_negative_controls.txt \
    r3_18bb_validation.txt r3_18bb_upstream_receipts.txt r3_18bb_aggregate.txt \
    > r3_18bb_artifact_sha256.txt
)

echo R3_18BB_RUNNER=PASS

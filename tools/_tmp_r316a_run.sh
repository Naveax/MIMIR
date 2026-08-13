#!/usr/bin/env bash
set -euo pipefail

BASE_SHA="76cbcc2094189e637e135f8c7d99e999e32311a0"
PRODUCTION_SHA="bf4bccff82203ed049d33e942681fed07f23beb4"
PRODUCTION_SOURCE_BLOB="f64a5e0d66962f41026b2eb10e176219d4529931"
BOXCARS_SHA="c70e77df7af81b436cb545d070bb90c82f562d0b"
BOXCARS_FRAME_BLOB="6f2ff153d3a27cdacccc65e3f23851489077a7d8"
R315A_PATCHER_BLOB="c67fca03897a2995845097f39d62ab4a68dca340"
PATHS_SHA="2ecbeea804f193796a539baee1e968719f03c0cd706efff0c22a61e6ef943dae"
IDENTITY_SHA="b02488b13cd6374219bbb89f884b03f8356f3744f930e39b2279df34859015cf"

printf 'R3_16A_HEAD=%s\n' "$(git rev-parse HEAD)"
test "$(git rev-parse HEAD:crates/mimir-replay/src/lib.rs)" = "$PRODUCTION_SOURCE_BLOB"
git diff --exit-code "$BASE_SHA"..HEAD -- \
  crates/mimir-replay/src/lib.rs crates/mimir-replay/Cargo.toml \
  Cargo.toml Cargo.lock external_fixtures test_corpus

git diff --name-only "$BASE_SHA"..HEAD | sort > r3_16a_source_scope.txt
printf 'base_sha=%s\nproduction_sha=%s\nproduction_source_blob=%s\nproduction_mutation_count=0\ncargo_mutation_count=0\n' \
  "$BASE_SHA" "$PRODUCTION_SHA" "$PRODUCTION_SOURCE_BLOB" >> r3_16a_source_scope.txt

# Pin the admitted R3.15D selector/identity projection byte-for-byte.
test "$(sha256sum tools/_tmp_r316a_r315d_paths.txt | awk '{print $1}')" = "$PATHS_SHA"
test "$(sha256sum tools/_tmp_r316a_r315d_identity.tsv | awk '{print $1}')" = "$IDENTITY_SHA"
mkdir -p .tmp/r315d
cp tools/_tmp_r316a_r315d_paths.txt .tmp/r315d/r3_15d_paths.txt
cp tools/_tmp_r316a_r315d_identity.tsv .tmp/r315d/r3_15d_replay_identity.tsv
python tools/_tmp_r316a_prepare.py "$PWD" .tmp/r315d

# Reuse the previously green R3.15A Boxcars instrumentation as an exact base.
BOXCARS="$RUNNER_TEMP/boxcars-r316a"
git clone --quiet https://github.com/nickbabcock/boxcars.git "$BOXCARS"
git -C "$BOXCARS" checkout --quiet --detach "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" rev-parse HEAD)" = "$BOXCARS_SHA"
test "$(git -C "$BOXCARS" hash-object src/network/frame_decoder.rs)" = "$BOXCARS_FRAME_BLOB"

git fetch --quiet origin agent/evidence-next:refs/remotes/origin/agent/evidence-next
git show origin/agent/evidence-next:tools/_tmp_evidence_next.py > "$RUNNER_TEMP/r315a_base.py"
test "$(git hash-object "$RUNNER_TEMP/r315a_base.py")" = "$R315A_PATCHER_BLOB"
python "$RUNNER_TEMP/r315a_base.py" patch-boxcars "$BOXCARS"
python tools/_tmp_r316a_patch.py "$BOXCARS"

git -C "$BOXCARS" add -N examples/r3_15a_probe.rs
git -C "$BOXCARS" diff --check
git -C "$BOXCARS" diff --binary -- \
  src/network/frame_decoder.rs examples/r3_15a_probe.rs \
  > r3_16a_boxcars_instrumentation.patch
sha256sum r3_16a_boxcars_instrumentation.patch > r3_16a_boxcars_instrumentation_sha256.txt
sha256sum tools/_tmp_r316a_patch.py tools/_tmp_r316a_prepare.py \
  tools/_tmp_r316a_select.py tools/_tmp_r316a_compare.py \
  > r3_16a_driver_sha256.txt

cargo check --manifest-path "$BOXCARS/Cargo.toml" --example r3_15a_probe
cargo test --manifest-path "$BOXCARS/Cargo.toml" --lib --quiet
cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_15a_probe --quiet

PROBE="$BOXCARS/target/debug/examples/r3_15a_probe"
test -x "$PROBE"
: > r3_16a_boxcars.log
while IFS= read -r rel; do
  test -n "$rel"
  MIMIR_R3_15A_LABEL="$rel" "$PROBE" "$PWD/$rel" >> r3_16a_boxcars.log 2>&1
done < r3_16a_paths.txt

test "$(grep -c '^R3_15A_ORACLE_PARSE=PASS$' r3_16a_boxcars.log)" -eq 47
test "$(grep -c '^R3_16A_PROPERTY' r3_16a_boxcars.log)" -eq 47
python tools/_tmp_r316a_select.py r3_16a_boxcars.log
sha256sum r3_16a_boxcars.log > r3_16a_boxcars_log_sha256.txt

# Independent comparison against the already-admitted production inherited lookup plan.
cargo fmt --all -- --check
cargo build --locked -p mimir-replay --example _tmp_r316a_lookup
MIMIR_PROBE="target/debug/examples/_tmp_r316a_lookup"
test -x "$MIMIR_PROBE"
: > r3_16a_mimir.log
while IFS=$'\t' read -r rel actor_object_id stream_id; do
  test -n "$rel"
  "$MIMIR_PROBE" "$rel" "$actor_object_id" "$stream_id" >> r3_16a_mimir.log
done < r3_16a_mimir_queries.tsv

test "$(grep -c '^R3_16A_MIMIR' r3_16a_mimir.log)" -eq 47
python tools/_tmp_r316a_compare.py r3_16a_mimir.log
grep -Fx 'R3_16A_OUTCOME=A' r3_16a_aggregate.txt
grep -Fx 'R3_16A_EVIDENCE=PASS' r3_16a_aggregate.txt

# Final immutable-boundary audit.
test "$(git rev-parse HEAD:crates/mimir-replay/src/lib.rs)" = "$PRODUCTION_SOURCE_BLOB"
git diff --exit-code "$BASE_SHA"..HEAD -- \
  crates/mimir-replay/src/lib.rs crates/mimir-replay/Cargo.toml \
  Cargo.toml Cargo.lock external_fixtures test_corpus
printf 'R3_16A_PRODUCTION_MUTATION=0\nR3_16A_CARGO_MUTATION=0\n'
cat r3_16a_aggregate.txt

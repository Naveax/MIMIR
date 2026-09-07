from pathlib import Path
import sys

src = Path(sys.argv[1])
out = Path(sys.argv[2])
s = src.read_text(encoding="utf-8")


def rep(old: str, new: str, label: str) -> None:
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly one match, got {n}")
    s = s.replace(old, new, 1)


rep(
    "name: R3.18BG One Following Primitive Payload Evidence v1",
    "name: R3.18BG One Following Primitive Payload Evidence v2",
    "workflow name",
)
rep(
    "evidence/r318bg-one-payload-v1",
    "evidence/r318bg-one-payload-v2",
    "branch",
)
rep(
    "group: r318bg-one-payload-v1",
    "group: r318bg-one-payload-v2",
    "concurrency",
)

anchor = "      BG_COMPARE_BLOB: 3b2d029cacb2f5beac23ff623e925fe227734348\n"
insert = anchor + """
      V1_FAILURE_HEAD: e0bdfd091a7f0fef14bdd0fc33f5cf108dfd5f39
      V1_FAILURE_RUN: '34107643273'
      V1_FAILURE_JOB: '101696239712'
      V1_FAILURE_ARTIFACT: '10013181984'
      V1_FAILURE_ARTIFACT_NAME: r318bg-non-authority-failure-receipt
      V1_FAILURE_DIGEST: sha256:866683754c1b186aabfd3d64b062f07388105cfb837cb31d64c70626c8739c0e
"""
rep(anchor, insert, "v1 failure env")

freeze_anchor = "          echo R3_18BG_AUTHORITY_FREEZE=PASS\n"
freeze_insert = """          test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$V1_FAILURE_RUN" --jq .head_sha)" = "$V1_FAILURE_HEAD"
          test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$V1_FAILURE_RUN" --jq .status)" = completed
          test "$(gh api "repos/$GITHUB_REPOSITORY/actions/runs/$V1_FAILURE_RUN" --jq .conclusion)" = failure
          test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$V1_FAILURE_JOB" --jq .run_id)" = "$V1_FAILURE_RUN"
          test "$(gh api "repos/$GITHUB_REPOSITORY/actions/jobs/$V1_FAILURE_JOB" --jq .conclusion)" = failure
          v1_meta="$(gh api "repos/$GITHUB_REPOSITORY/actions/artifacts/$V1_FAILURE_ARTIFACT")"
          test "$(jq -r .name <<<"$v1_meta")" = "$V1_FAILURE_ARTIFACT_NAME"
          test "$(jq -r .digest <<<"$v1_meta" | tr '[:upper:]' '[:lower:]')" = "$(printf '%s' "$V1_FAILURE_DIGEST" | tr '[:upper:]' '[:lower:]')"
          test "$(jq -r .workflow_run.id <<<"$v1_meta")" = "$V1_FAILURE_RUN"
          test "$(jq -r .workflow_run.head_sha <<<"$v1_meta")" = "$V1_FAILURE_HEAD"
          echo R3_18BG_V1_NON_AUTHORITY_FAILURE_FREEZE=PASS
          echo R3_18BG_AUTHORITY_FREEZE=PASS
"""
rep(freeze_anchor, freeze_insert, "failure freeze")

old_scope = """      - name: Record immutable scope and privacy
        shell: bash
        run: |
          set -euo pipefail
          OUT="$RUNNER_TEMP/r318bg-out"
          mapfile -t actual < <(git diff --name-only "$MAIN_SHA" "$GITHUB_SHA" | sort)
          mapfile -t expected < <(printf '%s\\n' .github/workflows/r318bg-one-payload-v1.yml | sort)
          diff -u <(printf '%s\\n' "${expected[@]}") <(printf '%s\\n' "${actual[@]}")
          git diff --exit-code "$MAIN_SHA" "$GITHUB_SHA" -- crates/mimir-replay/src crates/mimir-replay/tests Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
          test -z "$(git status --porcelain --untracked-files=all)"
          cat > "$OUT/r3_18bg_source_scope.txt" <<'EOF'
          R3_18BG_COMMIT_SCOPE=workflow-only
          R3_18BG_PRODUCTION_MUTATION=0
          R3_18BG_CARGO_MUTATION=0
          R3_18BG_FIXTURE_MUTATION=0
          R3_18BG_CORPUS_MUTATION=0
          R3_18BG_SUPPORT_MUTATION=0
          R3_18BG_PAYLOAD_DECODERS_PER_TARGET=1
          R3_18BG_NEXT_CONTROL_DECODERS=0
          R3_18BG_GENERALIZED_PROPERTY_LOOP=0
          EOF
          if grep -R -E '/home/runner|C:\\\\Users\\\\|Omersevik095|79841922\\+Naveax' "$OUT" --exclude='r3_18bg_boxcars_instrumentation.patch' >/dev/null; then
            echo 'privacy scan found disallowed runner/user material' >&2
            exit 1
          fi
          echo R3_18BG_PRIVACY_SCAN=PASS >> "$OUT/r3_18bg_aggregate.txt"
          echo R3_18BG_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0 >> "$OUT/r3_18bg_aggregate.txt"
          echo R3_18BG_SCOPE_PRIVACY=PASS
"""
new_scope = """      - name: Record immutable workflow scope
        shell: bash
        run: |
          set -euo pipefail
          OUT="$RUNNER_TEMP/r318bg-out"
          mapfile -t actual < <(git diff --name-only "$MAIN_SHA" "$GITHUB_SHA" | sort)
          mapfile -t expected < <(printf '%s\\n' .github/workflows/r318bg-one-payload-v2.yml | sort)
          diff -u <(printf '%s\\n' "${expected[@]}") <(printf '%s\\n' "${actual[@]}")
          git diff --exit-code "$MAIN_SHA" "$GITHUB_SHA" -- crates/mimir-replay/src crates/mimir-replay/tests Cargo.toml Cargo.lock external_fixtures test_corpus scripts docs MIMIR_CONTINUE_HERE.md MIMIR_KNOWLEDGE_GRAPH.md
          test -z "$(git status --porcelain --untracked-files=all)"
          cat > "$OUT/r3_18bg_source_scope.txt" <<'EOF'
          R3_18BG_COMMIT_SCOPE=workflow-only
          R3_18BG_PRODUCTION_MUTATION=0
          R3_18BG_CARGO_MUTATION=0
          R3_18BG_FIXTURE_MUTATION=0
          R3_18BG_CORPUS_MUTATION=0
          R3_18BG_SUPPORT_MUTATION=0
          R3_18BG_PAYLOAD_DECODERS_PER_TARGET=1
          R3_18BG_NEXT_CONTROL_DECODERS=0
          R3_18BG_GENERALIZED_PROPERTY_LOOP=0
          EOF
          echo R3_18BG_SCOPE=PASS
"""
rep(old_scope, new_scope, "scope/privacy step")

upstream_anchor = "          R3_18BG_BF_SAME_HEAD_CI=$BF_CI_RUN/$BF_CI_JOB SUCCESS\n"
upstream_insert = upstream_anchor + "          R3_18BG_V1_NON_AUTHORITY_FAILURE=$V1_FAILURE_RUN/$V1_FAILURE_JOB artifact=$V1_FAILURE_ARTIFACT\n"
rep(upstream_anchor, upstream_insert, "v1 receipt")

old_manifest = """          (\n            cd "$OUT"\n            sha256sum \\
              r3_18bg_aggregate.txt \\
              r3_18bg_bf_aggregate.txt \\
              r3_18bg_bf_header_authority.json \\
              r3_18bg_boxcars_instrumentation.patch \\
              r3_18bg_boxcars_instrumentation_sha256.txt \\
              r3_18bg_comparison.tsv \\
              r3_18bg_evidence_identity.txt \\
              r3_18bg_native_rows.tsv \\
              r3_18bg_negative_controls.txt \\
              r3_18bg_oracle_rows.tsv \\
              r3_18bg_replay_identity.tsv \\
              r3_18bg_same_head_ci_receipt.txt \\
              r3_18bg_source_scope.txt \\
              r3_18bg_summary.json \\
              r3_18bg_targets.tsv \\
              r3_18bg_upstream_receipts.txt \\
              r3_18bg_validation.txt \\
              > r3_18bg_artifact_sha256.txt\n            sha256sum -c r3_18bg_artifact_sha256.txt\n          )\n          echo R3_18BG_ARTIFACT_FINALIZE=PASS\n"""
new_manifest = """          AUTH="$RUNNER_TEMP/r318bg-authority"
          rm -rf "$AUTH"
          mkdir -p "$AUTH"
          files=(
            r3_18bg_aggregate.txt
            r3_18bg_bf_aggregate.txt
            r3_18bg_bf_header_authority.json
            r3_18bg_boxcars_instrumentation.patch
            r3_18bg_boxcars_instrumentation_sha256.txt
            r3_18bg_comparison.tsv
            r3_18bg_evidence_identity.txt
            r3_18bg_native_rows.tsv
            r3_18bg_negative_controls.txt
            r3_18bg_oracle_rows.tsv
            r3_18bg_replay_identity.tsv
            r3_18bg_same_head_ci_receipt.txt
            r3_18bg_source_scope.txt
            r3_18bg_summary.json
            r3_18bg_targets.tsv
            r3_18bg_upstream_receipts.txt
            r3_18bg_validation.txt
          )
          for f in "${files[@]}"; do
            test -f "$OUT/$f"
            cp "$OUT/$f" "$AUTH/$f"
          done
          test "$(find "$AUTH" -maxdepth 1 -type f | wc -l)" -eq 17
          if grep -R -E '/home/runner|C:\\\\Users\\\\|Omersevik095|79841922\\+Naveax|gh[pousr]_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|(?i)(password|secret|token)[[:space:]]*[:=][[:space:]]*[^[:space:]]+' "$AUTH" >/dev/null; then
            echo 'privacy scan found disallowed material in curated authority set' >&2
            grep -R -n -E '/home/runner|C:\\\\Users\\\\|Omersevik095|79841922\\+Naveax' "$AUTH" || true
            exit 1
          fi
          echo R3_18BG_PRIVACY_SCAN=PASS >> "$OUT/r3_18bg_aggregate.txt"
          echo R3_18BG_PRODUCTION_CARGO_FIXTURE_CORPUS_SUPPORT_MUTATION=0/0/0/0/0 >> "$OUT/r3_18bg_aggregate.txt"
          cp "$OUT/r3_18bg_aggregate.txt" "$AUTH/r3_18bg_aggregate.txt"
          if grep -R -E '/home/runner|C:\\\\Users\\\\|Omersevik095|79841922\\+Naveax|gh[pousr]_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY' "$AUTH" >/dev/null; then
            echo 'post-finalization privacy scan failed' >&2
            exit 1
          fi
          (
            cd "$AUTH"
            sha256sum "${files[@]}" > r3_18bg_artifact_sha256.txt
            sha256sum -c r3_18bg_artifact_sha256.txt
          )
          echo R3_18BG_CURATED_AUTHORITY_FILES=17
          echo R3_18BG_EPHEMERAL_LOGS_EXCLUDED=native.log,oracle.log,oracle_kv.tsv,oracle_requests.tsv
          echo R3_18BG_SCOPE_PRIVACY=PASS
          echo R3_18BG_ARTIFACT_FINALIZE=PASS
"""
rep(old_manifest, new_manifest, "curated manifest")

rep(
    "name: r318bg-one-following-primitive-payload-evidence\n          path: ${{ runner.temp }}/r318bg-out/",
    "name: r318bg-one-following-primitive-payload-evidence-v2\n          path: ${{ runner.temp }}/r318bg-authority/",
    "authority artifact upload",
)
rep(
    "name: r318bg-non-authority-failure-receipt\n          path: ${{ runner.temp }}/r318bg-failure/",
    "name: r318bg-v2-non-authority-failure-receipt\n          path: ${{ runner.temp }}/r318bg-failure/",
    "failure artifact upload",
)

# Safety assertions: no broad raw-output privacy scan or raw-output upload may survive.
assert 'grep -R -E \'/home/runner' not in s.split('      - name: Bind exact evidence head to unique natural CI')[0]
assert 'path: ${{ runner.temp }}/r318bg-out/' not in s
assert 'r318bg-one-payload-v1' not in s
assert 'evidence/r318bg-one-payload-v1' not in s
assert 'R3_18BG_CURATED_AUTHORITY_FILES=17' in s
assert 'r318bg-one-following-primitive-payload-evidence-v2' in s
out.write_text(s, encoding="utf-8", newline="\n")
print("R3_18BG_V2_PATCH=PASS curated_authority=17 raw_logs_excluded=4 v1_failure_bound=1")

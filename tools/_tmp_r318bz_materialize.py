from __future__ import annotations

from pathlib import Path
import argparse

TOKENS = {
    '__BASE_SHA__': 'base_sha',
    '__BASE_TREE__': 'base_tree',
    '__BY_PUBLISHED_SHA__': 'by_published_sha',
    '__BY_PUBLISHED_TREE__': 'by_published_tree',
    '__BY_CANDIDATE_SHA__': 'by_candidate_sha',
    '__BY_LIB_BLOB__': 'by_lib_blob',
    '__BY_TEST_BLOB__': 'by_test_blob',
    '__BY_PR_CI_RUN__': 'by_pr_ci_run',
    '__BY_PR_CI_JOB__': 'by_pr_ci_job',
    '__BY_MAIN_CI_RUN__': 'by_main_ci_run',
    '__BY_MAIN_CI_JOB__': 'by_main_ci_job',
    '__BASE_MAIN_CI_RUN__': 'base_main_ci_run',
    '__BASE_MAIN_CI_JOB__': 'base_main_ci_job',
    '__BASE_MAIN_KNOWLEDGE_RUN__': 'base_main_knowledge_run',
    '__BASE_MAIN_KNOWLEDGE_JOB__': 'base_main_knowledge_job',
}

parser = argparse.ArgumentParser()
parser.add_argument('--template', required=True)
parser.add_argument('--output', required=True)
for arg in TOKENS.values():
    parser.add_argument('--' + arg.replace('_', '-'), dest=arg, required=True)
args = parser.parse_args()

text = Path(args.template).read_text(encoding='utf-8')

old_env = """      BASE_SHA: __BY_PUBLISHED_SHA__
      BASE_TREE: __BY_PUBLISHED_TREE__
      LIB_BLOB: __BY_LIB_BLOB__
      BY_TEST_BLOB: __BY_TEST_BLOB__
      BY_PR_CI_RUN: '__BY_PR_CI_RUN__'
      BY_PR_CI_JOB: '__BY_PR_CI_JOB__'
      BY_PR_KNOWLEDGE_RUN: '__BY_PR_KNOWLEDGE_RUN__'
      BY_PR_KNOWLEDGE_JOB: '__BY_PR_KNOWLEDGE_JOB__'
      BY_MAIN_CI_RUN: '__BY_MAIN_CI_RUN__'
      BY_MAIN_CI_JOB: '__BY_MAIN_CI_JOB__'
      BY_MAIN_KNOWLEDGE_RUN: '__BY_MAIN_KNOWLEDGE_RUN__'
      BY_MAIN_KNOWLEDGE_JOB: '__BY_MAIN_KNOWLEDGE_JOB__'
"""
new_env = """      BASE_SHA: __BASE_SHA__
      BASE_TREE: __BASE_TREE__
      PROD_SHA: __BY_PUBLISHED_SHA__
      PROD_TREE: __BY_PUBLISHED_TREE__
      CANDIDATE_SHA: __BY_CANDIDATE_SHA__
      LIB_BLOB: __BY_LIB_BLOB__
      BY_TEST_BLOB: __BY_TEST_BLOB__
      BY_PR_CI_RUN: '__BY_PR_CI_RUN__'
      BY_PR_CI_JOB: '__BY_PR_CI_JOB__'
      BY_MAIN_CI_RUN: '__BY_MAIN_CI_RUN__'
      BY_MAIN_CI_JOB: '__BY_MAIN_CI_JOB__'
      BASE_MAIN_CI_RUN: '__BASE_MAIN_CI_RUN__'
      BASE_MAIN_CI_JOB: '__BASE_MAIN_CI_JOB__'
      BASE_MAIN_KNOWLEDGE_RUN: '__BASE_MAIN_KNOWLEDGE_RUN__'
      BASE_MAIN_KNOWLEDGE_JOB: '__BASE_MAIN_KNOWLEDGE_JOB__'
"""
if text.count(old_env) != 1:
    raise SystemExit(f'expected one legacy authority env block, got {text.count(old_env)}')
text = text.replace(old_env, new_env)

old_freeze = """          eq \"$(git rev-parse HEAD^)\" \"$BASE_SHA\"
          eq \"$(git rev-parse \"$BASE_SHA^{tree}\")\" \"$BASE_TREE\"
          eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/branches/main\" --jq .commit.sha)\" \"$BASE_SHA\"
          mapfile -t changed < <(git diff --name-only \"$BASE_SHA...$GITHUB_SHA\" | sort)
          test \"${#changed[@]}\" -eq 1
          test \"${changed[0]}\" = '.github/workflows/_tmp_r318bz_published_by_differential.yml'
          eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/contents/crates/mimir-replay/src/lib.rs?ref=$BASE_SHA\" --jq .sha)\" \"$LIB_BLOB\"
          eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/contents/crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs?ref=$BASE_SHA\" --jq .sha)\" \"$BY_TEST_BLOB\"
          for pair in \\
            \"$BY_PR_CI_RUN:$BY_PR_CI_JOB\" \\
            \"$BY_PR_KNOWLEDGE_RUN:$BY_PR_KNOWLEDGE_JOB\" \\
            \"$BY_MAIN_CI_RUN:$BY_MAIN_CI_JOB\" \\
            \"$BY_MAIN_KNOWLEDGE_RUN:$BY_MAIN_KNOWLEDGE_JOB\"; do
            run=\"${pair%%:*}\"; job=\"${pair##*:}\"
            eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/actions/runs/$run\" --jq .head_sha)\" \"$BASE_SHA\"
            eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/actions/runs/$run\" --jq .conclusion)\" success
            eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/actions/jobs/$job\" --jq .conclusion)\" success
          done
"""
new_freeze = """          check_run() {
            local run=\"$1\" job=\"$2\" sha=\"$3\"
            eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/actions/runs/$run\" --jq .head_sha)\" \"$sha\"
            eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/actions/runs/$run\" --jq .status)\" completed
            eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/actions/runs/$run\" --jq .conclusion)\" success
            eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/actions/jobs/$job\" --jq .run_id)\" \"$run\"
            eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/actions/jobs/$job\" --jq .conclusion)\" success
          }
          eq \"$(git rev-parse HEAD^)\" \"$BASE_SHA\"
          eq \"$(git rev-parse \"$BASE_SHA^{tree}\")\" \"$BASE_TREE\"
          eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/branches/main\" --jq .commit.sha)\" \"$BASE_SHA\"
          eq \"$(git rev-parse \"$PROD_SHA^{tree}\")\" \"$PROD_TREE\"
          eq \"$(git merge-base \"$BASE_SHA\" \"$PROD_SHA\")\" \"$PROD_SHA\"
          mapfile -t changed < <(git diff --name-only \"$BASE_SHA...$GITHUB_SHA\" | sort)
          test \"${#changed[@]}\" -eq 1
          test \"${changed[0]}\" = '.github/workflows/_tmp_r318bz_published_by_differential.yml'
          eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/contents/crates/mimir-replay/src/lib.rs?ref=$PROD_SHA\" --jq .sha)\" \"$LIB_BLOB\"
          eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/contents/crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs?ref=$PROD_SHA\" --jq .sha)\" \"$BY_TEST_BLOB\"
          eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/contents/crates/mimir-replay/src/lib.rs?ref=$BASE_SHA\" --jq .sha)\" \"$LIB_BLOB\"
          eq \"$(gh api \"repos/${GITHUB_REPOSITORY}/contents/crates/mimir-replay/tests/r3_18by_post_bu_following_header.rs?ref=$BASE_SHA\" --jq .sha)\" \"$BY_TEST_BLOB\"
          check_run \"$BY_PR_CI_RUN\" \"$BY_PR_CI_JOB\" \"$CANDIDATE_SHA\"
          check_run \"$BY_MAIN_CI_RUN\" \"$BY_MAIN_CI_JOB\" \"$PROD_SHA\"
          check_run \"$BASE_MAIN_CI_RUN\" \"$BASE_MAIN_CI_JOB\" \"$BASE_SHA\"
          check_run \"$BASE_MAIN_KNOWLEDGE_RUN\" \"$BASE_MAIN_KNOWLEDGE_JOB\" \"$BASE_SHA\"
"""
if text.count(old_freeze) != 1:
    raise SystemExit(f'expected one legacy freeze block, got {text.count(old_freeze)}')
text = text.replace(old_freeze, new_freeze)

old_receipt = '          printf \'%s\\n\' "published_by_sha=$BASE_SHA" "published_by_tree=$BASE_TREE"'
new_receipt = '          printf \'%s\\n\' "published_by_sha=$PROD_SHA" "published_by_tree=$PROD_TREE" "continuity_base_sha=$BASE_SHA" "continuity_base_tree=$BASE_TREE"'
if text.count(old_receipt) != 1:
    raise SystemExit(f'expected one upstream receipt prefix, got {text.count(old_receipt)}')
text = text.replace(old_receipt, new_receipt)

for token, attr in TOKENS.items():
    value = str(getattr(args, attr))
    count = text.count(token)
    if count == 0:
        raise SystemExit(f'missing template token after normalization: {token}')
    text = text.replace(token, value)

legacy_tokens = [
    '__BY_PR_KNOWLEDGE_RUN__', '__BY_PR_KNOWLEDGE_JOB__',
    '__BY_MAIN_KNOWLEDGE_RUN__', '__BY_MAIN_KNOWLEDGE_JOB__',
]
remaining = [token for token in list(TOKENS) + legacy_tokens if token in text]
if remaining:
    raise SystemExit(f'unresolved template tokens: {remaining}')
Path(args.output).write_text(text, encoding='utf-8', newline='\n')

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
for token, attr in TOKENS.items():
    value = str(getattr(args, attr))
    count = text.count(token)
    if count == 0:
        raise SystemExit(f'missing template token: {token}')
    text = text.replace(token, value)

remaining = [token for token in TOKENS if token in text]
if remaining:
    raise SystemExit(f'unresolved template tokens: {remaining}')
Path(args.output).write_text(text, encoding='utf-8', newline='\n')

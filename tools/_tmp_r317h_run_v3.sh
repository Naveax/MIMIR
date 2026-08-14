#!/usr/bin/env bash
set -euo pipefail
mkdir -p .tmp
cp tools/_tmp_r317h_run.sh .tmp/r317h_run_v3.sh
python - <<'PY'
from pathlib import Path
p = Path('.tmp/r317h_run_v3.sh')
s = p.read_text(encoding='utf-8')
s = s.replace(
    "PATCH_SHA256='d3261462d7b83f3864254bf04ead6cf4c5e6d9c023f4d123be90c48befe32700'",
    "PATCH_BLOB='e6a551154a90ba7fa2cf5b887c9a8cfb9cfe933c'",
)
s = s.replace(
    'git show "$EVIDENCE_HEAD:tools/_tmp_r317e_patch.py" > .tmp/r317h/r317e_patch.py\n'
    'test "$(sha256sum .tmp/r317h/r317e_patch.py | awk \'{print $1}\')" = "$PATCH_SHA256"',
    'test "$(git rev-parse "$EVIDENCE_HEAD:tools/_tmp_r317e_patch.py")" = "$PATCH_BLOB"\n'
    'git show "$EVIDENCE_HEAD:tools/_tmp_r317e_patch.py" > .tmp/r317h/r317e_patch.py',
)
if 'PATCH_SHA256' in s:
    raise SystemExit('failed to replace file SHA check')
if 'PATCH_BLOB' not in s:
    raise SystemExit('missing blob identity')
p.write_text(s, encoding='utf-8', newline='\n')
PY
bash .tmp/r317h_run_v3.sh

#!/usr/bin/env bash
set -euo pipefail

V1='9c2bc511fd20a6ef194fa3ecdce3ebb1ebf5bd3a'
TMP="${RUNNER_TEMP:-/tmp}/r318i_v2_orchestration.sh"

git fetch origin evidence/r318i-second-property-payload-v1 --force
test "$(git rev-parse origin/evidence/r318i-second-property-payload-v1)" = "$V1"
git show "$V1:tools/_tmp_r318i_run.sh" > "$TMP"

env R318I_V2_TMP="$TMP" python3 - <<'PY'
import os
from pathlib import Path
p = Path(os.environ['R318I_V2_TMP'])
s = p.read_text(encoding='utf-8')
pairs = [
    ("MAIN='3e1fc68eea41378bac07992b5ccfc05485edd4c6'", "MAIN='3257d32fbc617b6dae7bb42d41629639acf6ce95'"),
    ("MAIN_TREE='0d21e6da9022e2db4a8450722a9d39d1234b3adc'", "MAIN_TREE='9afee5526db01c2e1b2939ee605b9744d490a07b'"),
    ("R318I_SPEC_BLOB='088b3edd9d4fac4ff1144213cf92c951de66afac'", "R318I_SPEC_BLOB='ebb3077b3e1e02d51d528cad60792d36fa098d0e'"),
    ("R318H_ARTIFACT_DIGEST='340f75e21be2e0fc5592584e3b6c3d42ea759fa13ae934d85570486068e89645'", "R318H_ARTIFACT_DIGEST='340f75e22875cb5b00d66f2b4b05bbd6aa9c1a64625d79d0fb5bd0dcc104bb79'"),
    ("R318H_PUBLISHED_CONTINUITY_RUN='31963228589'", "R318H_PUBLISHED_CONTINUITY_RUN='31965245337'"),
    ("R318H_PUBLISHED_CONTINUITY_JOB='95204290405'", "R318H_PUBLISHED_CONTINUITY_JOB='95209317665'"),
]
for old, new in pairs:
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'R3.18I v2 authority replacement count={count}: {old}')
    s = s.replace(old, new, 1)
for old, _ in pairs:
    if old in s:
        raise SystemExit(f'R3.18I v2 stale authority remains: {old}')
for _, new in pairs:
    if s.count(new) != 1:
        raise SystemExit(f'R3.18I v2 corrected authority count != 1: {new}')
p.write_text(s, encoding='utf-8', newline='\n')
print('R3_18I_V2_AUTHORITY_PATCH=PASS replacements=6')
PY

exec bash "$TMP"

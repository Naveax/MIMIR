#!/usr/bin/env bash
set -euo pipefail

V1='7e1b05a8537d97a76334e8dd6edf65f353e908c6'
TMP="${RUNNER_TEMP:-/tmp}/r318l_v1_runner.sh"

git show "$V1:tools/_tmp_r318l_run.sh" > "$TMP"

python3 - <<'PY'
from pathlib import Path
p = Path('tools/_tmp_r318l_native_probe.rs')
s = p.read_text(encoding='utf-8')
old = '        let second_prop_bits: u32 = f[18].parse()?;\n'
new = '        let second_prop_bits: u8 = f[18].parse()?;\n'
count = s.count(old)
if count != 1:
    raise SystemExit(f'R3.18L v2 prop_id_bits fix count={count}')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8', newline='\n')
print('R3_18L_V2_PROP_ID_BITS_FIX=PASS u32_to_u8')
PY

rustc --version | grep -F 'rustc 1.85.0 '
cargo --version | grep -F 'cargo 1.85.'
echo 'R3_18L_V2_RUST_FLOOR=PASS 1.85.0'

exec bash "$TMP"

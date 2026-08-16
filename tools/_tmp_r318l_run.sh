#!/usr/bin/env bash
set -euo pipefail

V1='7e1b05a8537d97a76334e8dd6edf65f353e908c6'
TMP="${RUNNER_TEMP:-/tmp}/r318l_v1_runner.sh"

git show "$V1:tools/_tmp_r318l_run.sh" > "$TMP"

python3 - <<'PY'
from pathlib import Path

probe = Path('tools/_tmp_r318l_native_probe.rs')
s = probe.read_text(encoding='utf-8')
old = '        let second_prop_bits: u32 = f[18].parse()?;\n'
new = '        let second_prop_bits: u8 = f[18].parse()?;\n'
count = s.count(old)
if count != 1:
    raise SystemExit(f'R3.18L v3 prop_id_bits fix count={count}')
probe.write_text(s.replace(old, new, 1), encoding='utf-8', newline='\n')

runner = Path("${RUNNER_TEMP:-/tmp}/r318l_v1_runner.sh")
PY

python3 - "$TMP" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text(encoding='utf-8')
old = 'cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18l_probe --quiet\n'
new = 'RUSTUP_TOOLCHAIN=stable cargo build --manifest-path "$BOXCARS/Cargo.toml" --example r3_18l_probe --quiet\n'
count = s.count(old)
if count != 1:
    raise SystemExit(f'R3.18L v3 Boxcars toolchain isolation count={count}')
p.write_text(s.replace(old, new, 1), encoding='utf-8', newline='\n')
print('R3_18L_V3_BOXCARS_TOOLCHAIN_ISOLATION=PASS oracle=stable mimir=1.85.0')
PY

rustc --version | grep -F 'rustc 1.85.0 '
cargo --version | grep -F 'cargo 1.85.'
rustc +stable --version
echo 'R3_18L_V3_MIMIR_RUST_FLOOR=PASS 1.85.0'
echo 'R3_18L_V3_PROP_ID_BITS_FIX=PASS u32_to_u8'

exec bash "$TMP"

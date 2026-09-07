from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text(encoding='utf-8')
old = "|(?i)(password|secret|token)[[:space:]]*[:=][[:space:]]*[^[:space:]]+' \"$AUTH\" >/dev/null; then"
new = "' \"$AUTH\" >/dev/null || grep -R -Ei '(password|secret|token)[[:space:]]*[:=][[:space:]]*[^[:space:]]+' \"$AUTH\" >/dev/null; then"
if s.count(old) != 1:
    raise SystemExit(f'case-insensitive privacy patch: expected one match, got {s.count(old)}')
s = s.replace(old, new, 1)
if '(?i)' in s:
    raise SystemExit('inline regex flag survived')
if "grep -R -Ei '(password|secret|token)" not in s:
    raise SystemExit('separate secret-assignment scan missing')
p.write_text(s, encoding='utf-8', newline='\n')
print('R3_18BG_V2_PRIVACY_REGEX_FIX=PASS')

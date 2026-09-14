from pathlib import Path

path = Path('crates/mimir-replay/src/lib.rs')
source = path.read_text(encoding='utf-8')
begin_marker = '// R3.18BU PRE-ADMISSION BEGIN bounded post-BS next property-control'
end_marker = '// R3.18BU PRE-ADMISSION END bounded post-BS next property-control'
w_anchor = '/// Read exactly one R3.18V-admitted control bit after a valid R3.18T following payload.'

begin = source.find(begin_marker)
if begin < 0:
    raise SystemExit('BU block not found after staging')
end_start = source.find(end_marker, begin)
if end_start < 0:
    raise SystemExit('BU end marker not found after staging')
end = end_start + len(end_marker)
while end < len(source) and source[end] in '\r\n':
    end += 1

block = source[begin:end].strip('\r\n') + '\n\n'
without = source[:begin].rstrip() + '\n' + source[end:].lstrip('\r\n')
anchor = without.find(w_anchor)
if anchor < 0:
    raise SystemExit('R3.18W tail anchor not found')
if without.find(w_anchor, anchor + 1) >= 0:
    raise SystemExit('R3.18W tail anchor is not unique')

relocated = without[:anchor] + block + without[anchor:]
if relocated.find(begin_marker) > relocated.find(w_anchor):
    raise SystemExit('BU relocation did not precede W tail function')
if relocated.count(begin_marker) != 1 or relocated.count(end_marker) != 1:
    raise SystemExit('BU marker multiplicity drift')

path.write_text(relocated, encoding='utf-8')
print('R3.18BU block relocated before legacy R3.18W EOF scope')
